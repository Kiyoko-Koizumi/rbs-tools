# coding: utf-8
# PRODUCTION_THRESHOLD 新規作成 2019/6/3
#

# モジュールのインポート
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import csv
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
from multiprocessing import Pool
import multiprocessing as multi
import numpy as np
import openpyxl
import glob

# ダブルコーテーション置き換え
def check_wq(list_f):
    for i in range(0,len(list_f)):
        f_name = os.path.basename(list_f[i])
        f_pass = os.path.dirname(list_f[i])
        os.chdir(f_pass)
        with open(f_name, 'r', encoding=font) as f:
            file = f.read()
            if '"' in file:
                file = file.replace('"', '')
                f_name = 'new_' + f_name
                st = open(f_name, 'w', encoding=font)
                st.write(file)
                st.close()
                list_f[i] = f_pass + '/' + f_name


#ファイル選択
def read_data():

    # ファイル選択ダイアログの表示
    root = tkinter.Tk()
    root.withdraw()
    fTyp = [("", "*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    tkinter.messagebox.showinfo('ファイル選択', '[③FBR需給一覧(SD-33371)_モニター用.xlsx] を選択してください')
    # データの取得
    # ここの1行を変更 askopenfilename → askopenfilenames
    file = tkinter.filedialog.askopenfilenames(filetypes=fTyp, initialdir=iDir)

    # 選択ファイルリスト作成
    list_f = list(file)


    # 1つ目のファイルを開く
    f_name = os.path.basename(list_f[0])
    f_pass = os.path.dirname(list_f[0])
    os.chdir(f_pass)

    # ファイルを開く
    order = pd.read_excel(f_name, dtype=object)

    #"の置き換え
    #check_wq(list_f)


    return order


#日付を基にデータを整える
def supp_couont(d, sub_name, calendar_dict, FBR):
    FBR = FBR[FBR['管理Gr'] == sub_name[d]].copy()
    for s in range(len(FBR)):
        if FBR.iloc[s, 17].strftime('%Y-%m-%d') in calendar_dict[sub_name[d]]:
            FBR.iloc[s, 18] = 0
        else:
            FBR.iloc[s, 18] = 1
        FBR.iloc[s, 17] = FBR.iloc[s, 17].strftime('%Y-%m-%d')

    FBR = FBR.loc[:,
          ['日付 の年、月', '製造GR', '内製', '管理Gr', '需要予測数', '生産能力（実力値）', '生産能力（投資済）', '補正値（DLO移管）', '補正値（ECAL戻し）',
           '補正値（FCN売上対策）', '補正値（R.B.S）', '補正値（TENEO移管）', '補正値（メーカー握り）', '補正値（在庫先行発注）', '生産能力（実力値）不足分　',
           '生産能力（投資済）不足分　','日付_y', ]]
    return FBR


def wrapper(args):
    # 複数の引数を渡すためwrapperを経由
    # 現法毎にFC数量になるまでランダムに取り込む
    return supp_couont(*args)


if __name__ == '__main__':
     # from tqdm import tqdm
    csv.field_size_limit(1000000000)

font = 'utf-8'
# font='shift_jisx0213'

# スクリプトのあるディレクトリの絶対パスを取得
script_pass = os.path.dirname(os.path.abspath(__name__))

# ③FBR需給一覧(SD-33371)_モニター用を読み込む
FBR = read_data()
#カンマを取る
FBR = FBR.apply(lambda x: x.str.replace(',', ''))
# NULL値を0に置換
FBR = FBR.fillna(0.0)

#FBRデータの中に日付、YEAR、MONTHを作成(YEAR MONTHはKEYとして利用するため)
FBR.loc[:, '日付'] = pd.to_datetime((FBR['日付 の年、月'] + '1日'), format='%Y年%m月%d日')
FBR['YEAR'] = FBR['日付'].dt.year
FBR['MONTH'] = FBR['日付'].dt.month
# 開始日と終了日を取得
Tgt_E = FBR['日付'].max()
Tgt_S = FBR['日付'].min()
Tgt_E = Tgt_E + relativedelta(months=1) - dt.timedelta(days=1)

# 日付用のデータフレーム(days)を作成
days = pd.DataFrame({'日付': [], 'flag': []})
count = 0
while Tgt_E >= Tgt_S:
    days.loc[count] = [Tgt_S, None]
    count += 1
    Tgt_S = Tgt_S + dt.timedelta(days=1)
# 日付をDatetimeIndexとし年、月のindexを追加
days = days.set_index('日付')
days = days.set_index([days.index.year, days.index.month, days.index])
days.index.names = ['YEAR','MONTH','日付']
days = days.reset_index()
# YEAR/MONTHをキーにFBRとdaysを結合
FBR = pd.merge(FBR, days, on=['YEAR','MONTH'], how='left')
# 日付 の年、月の表記を変える
FBR['日付 の年、月'] = [x.strftime('%Y{0}%m{1}%d{2}').format(*'年月日') for x in FBR['日付_y']]
#不要な値をデータフレームから削除
FBR = FBR.drop(['YEAR','MONTH','日付_x','flag','稼働日数'],axis=1)

#カレンダーフォルダにデータがあるものの処理
#Excelの読み込み、稼働日反映を行う
# 結果を入れるデータフレームを用意
calendar_all = pd.DataFrame()
files=glob.glob('//172.24.81.161/share/F加工企業体/生産計画/共用/FBR資料/稼働日カレンダー/*.xlsx')
for file in files:
    input_file_name = (file)
    input_book = pd.ExcelFile(input_file_name)
    # Excelブック内の各シートの名前をリストで取得
    input_sheet_name = input_book.sheet_names
    # カラム追加のためにシート名取得
    sheet_name = input_book.sheet_names[0]
    #縦連結のために月ごとにDataFrameとしてsheetを読込、
    df1 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[1, 4])
    df1 = df1.rename(columns={'日': '日付_y','稼動':'稼働日数'})
    df2 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[7, 10])
    df2 = df2.rename(columns={'日.1': '日付_y','稼動.1':'稼働日数'})
    df3 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[13,16])
    df3 = df3.rename(columns={'日.2': '日付_y','稼動.2':'稼働日数'})
    df4 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[19,22])
    df4 = df4.rename(columns={'日.3': '日付_y','稼動.3':'稼働日数'})
    df5 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[25,28])
    df5 = df5.rename(columns={'日.4': '日付_y','稼動.4':'稼働日数'})
    df6 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[31,34])
    df6 = df6.rename(columns={'日.5': '日付_y','稼動.5':'稼働日数'})
    df7 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[37,40])
    df7 = df7.rename(columns={'日.6': '日付_y','稼動.6':'稼働日数'})
    df8 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[43,46])
    df8 = df8.rename(columns={'日.7': '日付_y','稼動.7':'稼働日数'})
    df9 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[49,52])
    df9 = df9.rename(columns={'日.8': '日付_y','稼動.8':'稼働日数'})
    df10 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[55,58])
    df10 = df10.rename(columns={'日.9': '日付_y','稼動.9':'稼働日数'})
    df11 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[61,64])
    df11 = df11.rename(columns={'日.10': '日付_y','稼動.10':'稼働日数'})
    df12 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[67,70])
    df12 = df12.rename(columns={'日.11': '日付_y','稼動.11':'稼働日数'})

    vertical = pd.concat([df1, df2,df3, df4,df5, df6,df7, df8,df9, df10,df11, df12])
    for index, row in vertical.iterrows():
       vertical['Supplier'] = sheet_name
    calendar_all = calendar_all.append(vertical, ignore_index=True)

# J2グループとSPCNewを作成
# calendar_allを複製
add_calendar = calendar_all.copy()
add_calendar = add_calendar[((add_calendar['Supplier'] == 'SPC') | (add_calendar['Supplier'] == 'FCN') | (
            add_calendar['Supplier'] == '駿河阿見') | (add_calendar['Supplier'] == 'その他メーカー'))]
add_calendar = add_calendar.replace({'SPC': 'SPCNew', 'FCN': 'J2FCN', '駿河阿見': 'J2駿河阿見', 'その他メーカー': 'J2その他'})

#全管理Grのカレンダーを作成
fixed_calendar = pd.concat([calendar_all, add_calendar], sort=True)
fixed_calendar = fixed_calendar.loc[:, ['稼働日数','日付_y', 'Supplier' ]]

# FBR帳票用サプライヤー名ファイルの読み込み
SP_name = pd.read_csv('//172.24.81.161/share/F加工企業体/生産計画/共用/FBR資料/稼働日カレンダー/SP_name.csv', encoding='utf-8',dtype='object', index_col=None)
#calendarのカラムを管理Grに揃える
calendar = pd.merge(fixed_calendar, SP_name, on=['Supplier'], how='left')


#FBRと結合するために、データ型を揃える
calendar = calendar.loc[:, ['日付_y', '稼働日数', '管理Gr']]
calendar['日付_y'] = calendar['日付_y'].astype(str)
calendar['日付_y'] = calendar['日付_y'].str[:11]
calendar['日付_y'] = pd.to_datetime(calendar['日付_y'], errors='coerce')

#管理Gr分の稼働日を反映
FBR_SUM = pd.merge(FBR, calendar, on=['日付_y', '管理Gr'], how='left')

# 稼働日に基づいて需要予測などの値を修正
FBR_SUM = FBR_SUM.astype(
         {'需要予測数': np.float64, '生産能力（実力値）': np.float64, '稼働日数': np.float64, '生産能力（投資済）': np.float64,
          '補正値（DLO移管）': np.float64, '補正値（ECAL戻し）': np.float64, '補正値（FCN売上対策）': np.float64, '補正値（R.B.S）': np.float64,
          '補正値（TENEO移管）': np.float64, '補正値（メーカー握り）': np.float64, '補正値（在庫先行発注）': np.float64, '生産能力（実力値）不足分　': np.float64,
          '生産能力（投資済）不足分　': np.float64})
FBR_SUM.loc[:, '需要予測数'] = FBR_SUM['需要予測数'] * FBR_SUM['稼働日数']
FBR_SUM.loc[:, '生産能力（実力値）'] = FBR_SUM['生産能力（実力値）'] * FBR_SUM['稼働日数']
FBR_SUM.loc[:, '生産能力（投資済）'] = FBR_SUM['生産能力（投資済）'] * FBR_SUM['稼働日数']
FBR_SUM.loc[:, '補正値（DLO移管）'] = FBR_SUM['補正値（DLO移管）'] * FBR_SUM['稼働日数']
FBR_SUM.loc[:, '補正値（ECAL戻し）'] = FBR_SUM['補正値（ECAL戻し）'] * FBR_SUM['稼働日数']
FBR_SUM.loc[:, '補正値（FCN売上対策）'] = FBR_SUM['補正値（FCN売上対策）'] * FBR_SUM['稼働日数']
FBR_SUM.loc[:, '補正値（R.B.S）'] = FBR_SUM['補正値（R.B.S）'] * FBR_SUM['稼働日数']
FBR_SUM.loc[:, '補正値（TENEO移管）'] = FBR_SUM['補正値（TENEO移管）'] * FBR_SUM['稼働日数']
FBR_SUM.loc[:, '補正値（メーカー握り）'] = FBR_SUM['補正値（メーカー握り）'] * FBR_SUM['稼働日数']
FBR_SUM.loc[:, '補正値（在庫先行発注）'] = FBR_SUM['補正値（在庫先行発注）'] * FBR_SUM['稼働日数']
FBR_SUM.loc[:, '生産能力（実力値）不足分　'] = FBR_SUM['生産能力（実力値）不足分　'] * FBR_SUM['稼働日数']
FBR_SUM.loc[:, '生産能力（投資済）不足分　'] = FBR_SUM['生産能力（投資済）不足分　'] * FBR_SUM['稼働日数']


FBR_SUM = FBR_SUM.loc[:,
          ['日付 の年、月', '製造GR', '内製', '管理Gr', '稼働日数', '需要予測数', '生産能力（実力値）', '生産能力（投資済）', '補正値（DLO移管）', '補正値（ECAL戻し）',
                '補正値（FCN売上対策）', '補正値（R.B.S）', '補正値（TENEO移管）', '補正値（メーカー握り）', '補正値（在庫先行発注）', '生産能力（実力値）不足分　',
                '生産能力（投資済）不足分　']]


#ファイルアウトプット
FBR_SUM.to_excel('③FBR需給一覧(SD-33371)_モニター用.xlsx' , index=False)
print('DONE!!')