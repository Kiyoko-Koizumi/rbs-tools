# coding: utf-8
# PRODUCTION_THRESHOLD 新規作成 2019/6/3
# AIO追加

# モジュールのインポート
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import csv
from typing import List
import glob
import pandas as pd
import datetime as dt
import tkinter as tk
import tkinter.ttk as ttk
import threading
from dateutil.relativedelta import relativedelta
import pandas.tseries.offsets as offsets
from multiprocessing import Pool
import multiprocessing as multi

def supp_couont(d, sub_name, calendar_dict, THRESHOLD):
    THRESHOLD = THRESHOLD[THRESHOLD['SUPPLIER_CD'] == sub_name[d]].copy()
    if len(THRESHOLD):
        for s in range(len(THRESHOLD)):
            if THRESHOLD.iloc[s, 9].strftime('%Y-%m-%d') in calendar_dict[sub_name[d]]:
                THRESHOLD.iloc[s, 10] = 0
            else:
                THRESHOLD.iloc[s, 10] = 1
            THRESHOLD.iloc[s, 9] = THRESHOLD.iloc[s, 9] .strftime('%Y%m%d')
        # 上限、下限、納期遅延ラインの非稼働日を0に
        THRESHOLD = THRESHOLD.astype({'PRODUCTION_ABILITY_MAX': int, 'PRODUCTION_ABILITY_MIN': int, 'DUE_DATE_DELAYED_LINE': int, 'others': int})
        THRESHOLD.loc[:,'PRODUCTION_ABILITY_MAX'] = THRESHOLD['PRODUCTION_ABILITY_MAX'] * THRESHOLD['others']
        THRESHOLD.loc[:,'PRODUCTION_ABILITY_MIN'] = THRESHOLD['PRODUCTION_ABILITY_MIN'] * THRESHOLD['others']
        THRESHOLD.loc[:,'DUE_DATE_DELAYED_LINE'] = THRESHOLD['DUE_DATE_DELAYED_LINE'] * THRESHOLD['others']
    # 日付_yをBASE_DATEへ
    THRESHOLD = THRESHOLD.rename(columns={'日付_y': 'BASE_DATE'})
    THRESHOLD = THRESHOLD.loc[:,['SUBSIDIARY_CD', 'SUPPLIER_CD', 'FACILITY_CD', 'BASE_DATE', 'PRODUCTION_ABILITY_MAX', 'PRODUCTION_ABILITY_MIN', 'DUE_DATE_DELAYED_LINE']]
    return THRESHOLD


def wrapper(args):
    # 複数の引数を渡すためwrapperを経由
    # 現法毎にFC数量になるまでランダムに取り込む
    return supp_couont(*args)

def PRODUCTION_THRESHOLD():

    # from tqdm import tqdm
    csv.field_size_limit(1000000000)

    font = 'utf-8'
    # font='shift_jisx0213'

    # スクリプトのあるディレクトリの絶対パスを取得
    script_pass = os.path.dirname(os.path.abspath(__name__))
    # ファイル名を取得
    file = glob.glob(script_pass + '/Production_threshold/' + 'PRODUCTION_THRESHOLD_*.csv')
    if len(file)>0:
        file_name = os.path.basename(file[0])
        file_cd = file_name.replace('PRODUCTION_THRESHOLD_', '')
        file_cd = file_cd.replace('.csv', '')

        # PRODUCTION_THRESHOLD.csvデータ取り込み
        THRESHOLD = pd.read_csv(script_pass + '/Production_threshold/' + file_name, encoding=font, dtype='object', index_col=None)
        # 開始日と終了日を取得
        THRESHOLD.loc[:,'日付'] = pd.to_datetime((THRESHOLD['year'] + '/' + THRESHOLD['month'] + '/01'), format='%Y/%m/%d')
        Tgt_E = THRESHOLD['日付'].max()
        Tgt_S = THRESHOLD['日付'].min()
        Tgt_E = Tgt_E + relativedelta(months=1) - dt.timedelta(days=1)
        THRESHOLD = THRESHOLD.astype({'year': int, 'month': int})

        # 日付用のデータフレームを作成
        days = pd.DataFrame({'日付': [], 'others': []})
        count = 0
        while Tgt_E >= Tgt_S:
            days.loc[count] = [Tgt_S, None]
            count += 1
            Tgt_S = Tgt_S + dt.timedelta(days=1)
        # 日付をDatetimeIndexとし年、月、曜日のindexを追加
        days = days.set_index('日付')
        days = days.set_index([days.index.year, days.index.month, days.index])
        days.index.names = ['year', 'month', '日付']
        days = days.reset_index()
        # year、monthをキーにTHRESHOLDとdaysを結合
        THRESHOLD = pd.merge(THRESHOLD, days, on=['year', 'month'], how='left')

        # 非稼働日データを読み込む
        nowork_day = pd.read_csv(script_pass + '/Production_threshold/nowork_day.csv', encoding=font, dtype='object', index_col=None)

        # 各現法、拠点の非稼働日をリスト化
        sub_name = ['CHN', 'GRM', 'HKG', 'IND', 'JKT', 'KOR', 'MEX', 'MJP', 'MYS', 'SGP', 'THA', 'TIW', 'USA', 'VNM', '7017', '3764', '0FCN', '0AIO','SPCM', '0143']
        calendar_name = ['CAAAA', 'GAAAA', 'NAAAA', 'DAAAA', 'JAAAA', 'KAAAA', 'QAAAA', '5AAAA', 'MAAAA', 'SAAAA', 'HAAAA', 'TAAAA', 'UAAAA', 'VAAAA', '5AAAA', '5AAAA', 'C8677', 'C8677', '50SPC', '5AAAA']
        calendar_dict ={}
        for i in range(0,len(sub_name)):
            noworkday_df = nowork_day[nowork_day['CALENDAR_CD'] == calendar_name[i]]
            noworkday_df = noworkday_df.loc[::, ['OFF_DATE']]
            noworkday_df = noworkday_df.T
            noworkday_list = noworkday_df.values.tolist()
            calendar_dict[sub_name[i]] = noworkday_list[0]

        # 日付とサプライヤコード毎に稼働日フラグをつける
        # 並列処理
        pool = Pool(multi.cpu_count() - 2)
        list = [(d, sub_name, calendar_dict, THRESHOLD) for d in range(14, 20)]
        THRESHOLD_p = pool.map(wrapper, list)
        pool.close()
        THRESHOLD_SUM = pd.DataFrame({'SUBSIDIARY_CD': [], 'SUPPLIER_CD': [], 'FACILITY_CD': [], 'BASE_DATE':[], 'PRODUCTION_ABILITY_MAX':[], 'PRODUCTION_ABILITY_MIN':[], 'DUE_DATE_DELAYED_LINE':[]})
        for d in range(6):
            THRESHOLD_SUM = THRESHOLD_SUM.append(THRESHOLD_p[d], sort=False)

        # 空欄を埋める
        THRESHOLD_SUM.loc[:, 'UPD_COUNT'] = '0'
        THRESHOLD_SUM.loc[:, 'DEL_FLG'] = '0'
        Today = "'" + dt.datetime.today().strftime("%Y-%m-%d") + "'"
        THRESHOLD_SUM.loc[:, 'REG_TIME'] = Today
        THRESHOLD_SUM.loc[:, 'REG_USR'] = file_cd
        THRESHOLD_SUM.loc[:, 'UPD_TIME'] = Today
        THRESHOLD_SUM.loc[:, 'UPD_USR'] = file_cd

        # 加工済みデータ作成
        PROCESSED_DATA = THRESHOLD_SUM.copy()
        # 加工済みデータへ加工 加工済み本数上限と下限の平均値
        PROCESSED_DATA.loc[:, 'PROCESSED_QUANTITY'] = ((PROCESSED_DATA['PRODUCTION_ABILITY_MAX'] + PROCESSED_DATA[
            'PRODUCTION_ABILITY_MIN']) / 2)
        PROCESSED_DATA = PROCESSED_DATA.astype({'PROCESSED_QUANTITY': int})
        PROCESSED_DATA.loc[:, 'PROCESSED_DATE'] = PROCESSED_DATA['BASE_DATE']
        PROCESSED_DATA = PROCESSED_DATA.loc[:, ['SUBSIDIARY_CD', 'SUPPLIER_CD', 'FACILITY_CD', 'PROCESSED_DATE', 'PROCESSED_QUANTITY',
                                                'UPD_COUNT', 'DEL_FLG', 'REG_USR', 'REG_TIME', 'UPD_USR', 'UPD_TIME']]

        # ファイルアウトプット
        f_name = 'cap_' + file_cd + '.tsv'
        THRESHOLD_SUM.to_csv(script_pass + '/Production_threshold/' + f_name, sep='\t', encoding=font, quotechar='"', line_terminator='\n', index=False)

        # ファイルアウトプット
        f_name = 'pcd_' + file_cd + '.tsv'
        PROCESSED_DATA.to_csv(script_pass + '/Production_threshold/' + f_name, sep='\t', encoding=font, quotechar='"', line_terminator='\n', index=False)

    print('割付数量・加工済数量作成 Finish!')

if __name__ == '__main__':
    PRODUCTION_THRESHOLD()
