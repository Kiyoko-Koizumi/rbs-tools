# coding: utf-8
# Orders creation 新規作成 2019/3/8
# 0.2マルチコア化
# no_change_dateの仕様に合わせる 2019/7/25
# pre_inputデータの仕様に合わせる　2019/08/01

# モジュールのインポート
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import csv
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
import random
from multiprocessing import Pool
import multiprocessing as multi

def read_so():
    # ファイル選択ダイアログの表示
    root = tkinter.Tk()
    root.withdraw()
    fTyp = [("", "*")]
    iDir = os.path.abspath(os.path.dirname(__file__))

    # 受注実績データの取得
    # ここの1行を変更 askopenfilename → askopenfilenames
    file = tkinter.filedialog.askopenfilenames(filetypes=fTyp, initialdir=iDir, title='受注実績データの取得')

    # 選択ファイルリスト作成
    list_f = list(file)

    if len(list_f) != 0:
        # 1つ目のファイルを開く
        f_name = os.path.basename(list_f[0])
        f_pass = os.path.dirname(list_f[0])

        # 必要な列のみ読み込む
        order = pd.read_csv(f_pass + '/' + f_name, sep='\t', encoding='utf-8', dtype=object, engine='python', error_bad_lines=False)

        # ファイルを繰り返し開き結合する
        for r in range(1, len(list_f)):
            f_name = os.path.basename(list_f[r])
            print(f_name)
            order_add = pd.read_csv(f_pass + '/' + f_name, sep='\t', encoding='utf-8', dtype=object, engine='python',
                                    error_bad_lines=False)
            # ファイルを追加する
            order = order.append(order_add, sort=False)

        # MASTER_SUPPLIER_FLGのみにする pre_input仕様ではskip
        # order = order[order['従来生産拠点フラグ'] == '1']
        # 見積りデータを除く
        order = order[order['見積有効日'].isnull()]
        # 受注日のカラム名を変更
        order = order.rename(columns={'受注日・見積回答日': '受注日'})
        # 受注日、出荷日をdate形式へ変更
        order = order.astype({'受注日': str, '受注実績SSD': str, '数量': int})
        order.loc[:, '受注日'] = order['受注日'].str[0:4] + '-' + order['受注日'].str[4:6] + '-' + order['受注日'].str[6:8]
        order.loc[:, '顧客希望納期'] = order['顧客希望納期'].str[0:4] + '-' + order['顧客希望納期'].str[4:6] + '-' + order['顧客希望納期'].str[
                                                                                                   6:8]
        # 受注日と顧客希望納期をdate形式に変換
        order.loc[:, '受注日'] = pd.to_datetime(order['受注日'])
        order.loc[:, '顧客希望納期'] = pd.to_datetime(order['顧客希望納期'])
        order.loc[:, 'key'] = None
        order.loc[:, '納期属性'] = None
    else:
        order = pd.DataFrame()

    return order


def holidays(sub_name, local_pass):
    # 非稼働日データを読み込む
    nowork_day = pd.read_csv(local_pass + 'nowork_day.csv', encoding='utf-8', dtype='object', index_col=None)

    # 各現法、拠点の非稼働日をリスト化
    calendar_name = ['CAAAA', 'GAAAA', 'NAAAA', 'DAAAA', 'JAAAA', 'KAAAA', 'QAAAA', '5AAAA', 'MAAAA', 'SAAAA', 'HAAAA',
                     'TAAAA', 'UAAAA', 'VAAAA', '5AAAA', '5AAAA', 'C8677', '50SPC']
    calendar_dict = {}
    for i in range(0, len(sub_name)):
        noworkday_df = nowork_day[nowork_day['CALENDAR_CD'] == calendar_name[i]]
        noworkday_df = noworkday_df.loc[::, ['OFF_DATE']]
        noworkday_df = noworkday_df.T
        noworkday_list = noworkday_df.values.tolist()
        nowork_day_w = noworkday_list[0]
        # カレンダのリストのstrを1行ずつdate形式に変換
        for x in range(0, len(nowork_day_w)):
            nowork_day_w[x] = dt.datetime.strptime(nowork_day_w[x], "%Y-%m-%d")
        calendar_dict[sub_name[i]] = nowork_day_w
    return calendar_dict


def noki_zokusei(i, order, sub_name, calendar_dict):
    df = order[order['現法コード'] == sub_name[i]].copy()
    df.reset_index(inplace=True, drop=True)
    # 現法毎に納期属性をつける
    df.loc[:, '納期属性'] = [(z - y).days - len(list(filter(lambda x: y <= x <= z, calendar_dict[sub_name[i]]))) for y, z in
                         zip(df['受注日'], df['顧客希望納期'])]
    return df


def wrapper1(args):
    # 複数の引数を渡すためwrapperを経由
    return noki_zokusei(*args)


def devide_sub(order, sub_name, calendar_dict, order_dict):
    pool = Pool(multi.cpu_count() - 2)
    list1 = [(i, order, sub_name, calendar_dict) for i in range(14)]
    Output = pool.map(wrapper1, list1)
    pool.close()
    for i in range(14):
        order_dict[sub_name[i]] = Output[i]
    return order_dict


def ramdom_order_sub(i, S, year, month, SUPPLIER_CD, order, sub_name, calendar_dict, FC, header):
    df1 = order[order['現法コード'] == sub_name[i]].copy()
    df1.reset_index(inplace=True, drop=True)
    FC_Sub = FC[(FC['year'] == year) & (FC['month'] == month) & (FC['SUBSIDIARY_CD'] == sub_name[i]) & (
            FC['SUPPLIER_CD'] == SUPPLIER_CD[S])]
    FC_tgt = FC_Sub['FC'].sum()
    FC_tgt_ck = int(FC_tgt)
    gyo = len(df1)
    df_sub = pd.DataFrame(columns=header)
    # FCに至るまでランダムにRECを抜き出す
    # SubのRECが0である場合はスキップ
    if ((gyo != 0) & (FC_tgt_ck != 0)):
        df_sub = df_sub.astype({'数量': int})
        while df_sub['数量'].sum() < FC_tgt:
            No = random.randint(0, gyo - 1)
            df_sub = df_sub.append(df1.iloc[No], sort=False)
        df_sub.reset_index(inplace=True, drop=True)

        # 曜日毎に出荷日を当てる
        # 出荷日のdfを作成
        count = 0
        SD_df = pd.DataFrame({'出荷日': [], 'key': [], '新規受注日': []})
        SD_df = SD_df.astype({'key': int})
        Pre_S = year + "-" + month + "-1"
        Pre_S = dt.datetime.strptime(Pre_S, '%Y-%m-%d')
        Pre_E = Pre_S + relativedelta(months=1) - dt.timedelta(days=1)

        for d in range(0, (Pre_E - Pre_S).days + 1):
            SD_day = Pre_S + dt.timedelta(days=d)
            if len(list(filter(lambda x: SD_day == x, calendar_dict[sub_name[i]]))) != 1:
                SD_df.loc[count] = [SD_day, None, None]
                count += 1

        # 新規出荷日と過去RECを結合するキーを作成
        for w in range(len(SD_df)):
            SD_df.iat[w, 1] = w

        for w in range(len(df_sub)):
            df_sub.iat[w, 18] = random.randint(0, len(SD_df) - 1)

        df_sub = pd.merge(df_sub, SD_df, on=['key'], how='left')
        df_sub.loc[:, '新規受注日'] = [(z - dt.timedelta(days=y)) for z, y in zip(df_sub['出荷日'], df_sub['納期属性'])]
        for index, row in df_sub.iterrows():
            while row.納期属性 != ((row.出荷日 - row.新規受注日).days - len(
                    list(filter(lambda x: row.新規受注日 <= x <= row.出荷日, calendar_dict[sub_name[i]])))):
                row.新規受注日 = row.新規受注日 - dt.timedelta(days=1)
                df_sub.at[index, '新規受注日'] = row.新規受注日
            while row.新規受注日 in calendar_dict[sub_name[i]]:
                row.新規受注日 = row.新規受注日 - dt.timedelta(days=1)
                df_sub.at[index, '新規受注日'] = row.新規受注日

        df_sub.loc[:, '受注日'] = [x.strftime('%Y%m%d') for x in df_sub['新規受注日']]
        df_sub.loc[:, '顧客希望納期'] = [x.strftime('%Y%m%d') for x in df_sub['出荷日']]
        df_sub.drop(['新規受注日', '出荷日'], axis=1, inplace=True)
    print(SUPPLIER_CD[S] + '/' + year + '/' + month + '/' + sub_name[i] + '/' + str(df_sub['数量'].sum()))
    return df_sub


def wrapper2(args):
    # 複数の引数を渡すためwrapperを経由
    # 現法毎にFC数量になるまでランダムに取り込む
    return ramdom_order_sub(*args)


def random_order(S, order, sub_name, calendar_dict, FC):
    SUPPLIER_CD = ['3764', '7017', '0FCN', 'SPCM']
    year = '2019'
    # RBS_受注現法仕入先コードにするか実績仕入先コードにするか要検討  pre_input仕様では実績仕入先コード
    order = order[order['実績仕入先コード'] == SUPPLIER_CD[S]]
    # データを入れるdfを定義
    header = order.columns
    mk_order = pd.DataFrame(columns=header)

    for m in range(3, 13):
        month = str(m)

        # プロセスを 14個つくり現法毎にプロセスを分ける
        pool = Pool(multi.cpu_count() - 2)
        list2 = [(i, S, year, month, SUPPLIER_CD, order, sub_name, calendar_dict, FC, header) for i in range(14)]
        mk_order_m = pool.map(wrapper2, list2)
        pool.close()

        for i in range(14):
            mk_order = mk_order.append(mk_order_m[i], sort=False)

    year = '2020'

    for m in range(1, 4):
        month = str(m)

        # プロセスを 14個つくり現法毎にプロセスを分ける
        pool = Pool(multi.cpu_count() - 2)
        list2 = [(i, S, year, month, SUPPLIER_CD, order, sub_name, calendar_dict, FC, header) for i in range(14)]
        mk_order_m = pool.map(wrapper2, list2)
        pool.close()

        for i in range(14):
            mk_order = mk_order.append(mk_order_m[i], sort=False)
    return mk_order

def Orders_creation_change_date():

    sub_name = ['CHN', 'GRM', 'HKG', 'IND', 'JKT', 'KOR', 'MEX', 'MJP', 'MYS', 'SGP', 'THA', 'TIW', 'USA', 'VNM',
                '7017', '3764', '0FCN', 'SPCM']

    csv.field_size_limit(1000000000)

    font = 'utf-8'
    # font='shift_jisx0213'

    # スクリプトのあるディレクトリの絶対パスを取得
    script_pass = os.path.dirname(os.path.abspath(__name__))
    if __name__ == '__main__':
        local_pass = script_pass + '/'
    else:
        local_pass = script_pass + '/Orders_creation/'

    # 受注データ読み込み
    order = read_so()
    if len(order) != 0:
        header = order.columns

        # 必要なカラムだけにする
        order = order.loc[:, ['番号',
                              '現法コード',
                              'グローバル番号',
                              '受注日',
                              '受注時間・見積回答時間',
                              'アンフィット種別',
                              '得意先コード',
                              '直送先コード',
                              'ＭＣコード',
                              'インナーコード',
                              '商品コード',
                              '実績現法コード',
                              '実績仕入先コード',
                              '実績管理単位コード',
                              '受注実績SSD',
                              '数量',
                              '納入区分',
                              '顧客希望納期',
                              'key',
                              '納期属性']]

        # 各現法、拠点の非稼働日をリスト化
        calendar_dict = holidays(sub_name, local_pass)

        # 現法毎のFCを取り込む
        FC = pd.read_csv(local_pass + 'FC.csv', encoding=font, dtype='object', index_col=None)
        FC = FC.astype({'FC': int})

        # 現法毎に納期属性を設定する
        order_dict = {}
        order_dict = devide_sub(order, sub_name, calendar_dict, order_dict)

        '''
        # 現法毎の受注比率を算出
        order_subratio = order.groupby(['現法コード', '実績仕入先コード'], as_index=False)['数量'].sum()
        order_suppratio = order.groupby(['実績仕入先コード'], as_index=False)['数量'].sum()
        order_subratio = pd.merge(order_subratio, order_suppratio, on=['実績仕入先コード'], how='left')
        order_subratio['ratio'] = (order_subratio['数量_x']/order_subratio['数量_y']).round(3)
        order_subratio.drop(['数量_x', '数量_y'], axis=1, inplace=True)
    
        # FCに受注比率を乗算
        FC = pd.merge(FC, order_subratio, on=['実績仕入先コード'], how='left')
        FC.loc[:, 'FC'] = FC['FC'] * FC['ratio']
        '''

        # order_dictをorderにまとめる
        order = order_dict[sub_name[0]]
        for i in range(1,14):
            order = order.append(order_dict[sub_name[i]], sort=False)

        # 拠点毎にforで繰り返す
        mk_order = pd.DataFrame(columns=header)
        for S in range(0, 4):
            df = random_order(S, order, sub_name, calendar_dict, FC)
            # データをmk_orderに追加する
            mk_order = mk_order.append(df, sort=False)

        # 番号を振り直す
        mk_order.reset_index(inplace=True, drop=True)
        mk_order.drop('番号', axis=1, inplace=True)
        mk_order.reset_index(inplace=True)
        mk_order = mk_order.rename(columns={'index': '番号'})

        # 受注実績SSDに顧客希望納期を上書きする（日付を変えたあとでは受注実績SSDに意味がないため）
        mk_order.loc[:, '受注実績SSD'] = mk_order['顧客希望納期']
        # 受注日のカラム名を元に戻す
        mk_order = mk_order.rename(columns={'受注日': '受注日・見積回答日'})
        # 不要カラムを除く
        mk_order.drop(['key', '納期属性'], axis=1, inplace=True)

        # ファイルアウトプット
        # 日付毎に分ける
        mk_order = mk_order.astype({'顧客希望納期': int})
        # 1Q
        y = '20190401' + ' <= 顧客希望納期 <=' + '20190630'
        data = mk_order.query(y)
        f_name = 'mk_order_' + '1Q' + '.tsv'
        data.to_csv(local_pass + f_name, sep='\t', encoding=font, quotechar='"', line_terminator='\n', index=False)
        # 2Q
        y = '20190701' + ' <= 顧客希望納期 <=' + '20190930'
        data = mk_order.query(y)
        f_name = 'mk_order_' + '2Q' + '.tsv'
        data.to_csv(local_pass + f_name, sep='\t', encoding=font, quotechar='"', line_terminator='\n', index=False)
        # 3Q
        y = '20191001' + ' <= 顧客希望納期 <=' + '20191231'
        data = mk_order.query(y)
        f_name = 'mk_order_' + '3Q' + '.tsv'
        data.to_csv(local_pass + f_name, sep='\t', encoding=font, quotechar='"', line_terminator='\n', index=False)
        # 4Q
        y = '20200101' + ' <= 顧客希望納期 <=' + '20200331'
        data = mk_order.query(y)
        f_name = 'mk_order_' + '4Q' + '.tsv'
        data.to_csv(local_pass + f_name, sep='\t', encoding=font, quotechar='"', line_terminator='\n', index=False)
    print('ダミーオーダー作成　日付変更あり Finish!')

if __name__ == '__main__':
    Orders_creation_change_date()
