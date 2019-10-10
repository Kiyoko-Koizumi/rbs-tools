# coding: utf-8
# Orders creation FY21 新規作成 2019/4/8
# 0.2マルチコア化
# 受注をランダムにアップトレンドダウントレンドを作成、日付は2019年
# inputデータは割振り処理前のデータを想定
# 実績仕入先とR.B.S仕入先の違いを補正
# 現法毎のFCを元に作成

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

    tkinter.messagebox.showinfo('Orders_creation_no_change_date', '元となるデータとFCデータを選んでください！')

    fTyp = [("", "*")]
    iDir = os.path.abspath(os.path.dirname(__file__))

    # 受注実績データの取得
    # ここの1行を変更 askopenfilename → askopenfilenames
    file = tkinter.filedialog.askopenfilenames(filetypes=fTyp, initialdir=iDir, title='元となるデータを選んでください！')

    # 選択ファイルリスト作成
    list_f = list(file)

    if len(list_f) != 0:
        # 1つ目のファイルを開く
        f_name = os.path.basename(list_f[0])
        f_pass = os.path.dirname(list_f[0])

        # 必要な列のみ読み込む
        order = pd.read_csv(f_pass + '/' + f_name, sep='\t', encoding='utf-8', dtype=object, engine='python', error_bad_lines=False)
    else:
        order = pd.DataFrame()
    return order

def read_fc():
    # ファイル選択ダイアログの表示
    # root = tkinter.Tk()
    # root.withdraw()
    fTyp = [("", "*")]
    iDir = os.path.abspath(os.path.dirname(__file__))

    # 受注実績データの取得
    # ここの1行を変更 askopenfilename → askopenfilenames
    file = tkinter.filedialog.askopenfilenames(filetypes=fTyp, initialdir=iDir, title='FCとなるCSVデータを選んでください！')

    # 選択ファイルリスト作成
    list_f = list(file)

    if len(list_f) != 0:
        # 1つ目のファイルを開く
        f_name = os.path.basename(list_f[0])
        f_pass = os.path.dirname(list_f[0])

        # 必要な列のみ読み込む
        fc = pd.read_csv(f_pass + '/' + f_name, sep=',', encoding='utf-8', dtype=object, index_col=None)
    return fc


def ramdom_order_sub(S, year, month, SUPPLIER_CD, order_count, FC, header):
    # 顧客希望納期の期間でRECを限定する
    order_count.loc[:, '顧客希望納期'] = pd.to_datetime(order_count['顧客希望納期'])
    Pre_S = year + "-" + month + "-1"
    Pre_S = dt.datetime.strptime(Pre_S, '%Y-%m-%d')
    Pre_E = Pre_S + relativedelta(months=1) - dt.timedelta(days=1)
    sub_name = ['CHN', 'GRM', 'HKG', 'IND', 'JKT', 'KOR', 'MEX', 'MJP', 'MYS', 'SGP', 'THA', 'TIW', 'USA', 'VNM',
                '0143', '3764', '7017', '0FCN', '0AIO', 'SPCM']
    df_sub_sum = pd.DataFrame(columns=header)

    # 現法毎に実施する
    for v in range(0, 14):
        df1 = order_count[((order_count['顧客希望納期'] >= Pre_S) &
                           (order_count['顧客希望納期'] <= Pre_E) &
                           (order_count['現法コード'] == sub_name[v]))].copy()
        df1.reset_index(inplace=True, drop=True)
        FC_Sub = FC[(FC['year'] == year) &
                    (FC['month'] == month) &
                    (FC['SUPPLIER_CD'] == SUPPLIER_CD[S]) &
                    (FC['SUBSIDIARY_CD'] == sub_name[v])]
        FC_tgt = FC_Sub['FC'].sum()
        FC_tgt_ck = int(FC_tgt)
        gyo = len(df1)
        df_sub = pd.DataFrame(columns=header)
        print(SUPPLIER_CD[S] + '/' + year + "/" + month + "/" + sub_name[v])
        # FCに至るまでランダムにRECを抜き出す
        # SubのRECが0である場合はスキップ
        if ((gyo != 0) & (FC_tgt_ck != 0)):
            df_sub = df_sub.astype({'数量': int})
            while df_sub['数量'].sum() < FC_tgt:
                No = random.randint(0, gyo - 1)
                df_sub = df_sub.append(df1.iloc[No], sort=False)
            # FC数量通りになっているか確認の出力
            print(SUPPLIER_CD[S] + '/' + year + "/" + month + "/" + sub_name[v] + '/' + str(df_sub['数量'].sum()))
            df_sub_sum = df_sub_sum.append(df_sub, sort=False)

    df_sub_sum.reset_index(inplace=True, drop=True)
    return df_sub_sum


def wrapper2(args):
    # 複数の引数を渡すためwrapperを経由
    # 現法毎にFC数量になるまでランダムに取り込む
    return ramdom_order_sub(*args)


def random_order(S, order_count, FC):
    SUPPLIER_CD = ['0143', '3764', '7017', '0FCN', '0AIO', 'SPCM']
    # RBS_受注現法仕入先コードにするか実績仕入先コードにするか要検討
    order_count = order_count[order_count['RBS_受注現法仕入先コード'] == SUPPLIER_CD[S]]
    # データを入れるdfを定義
    header = order_count.columns
    mk_order = pd.DataFrame(columns=header)

    # プロセスを 月の数だけつくり月毎にプロセスを分ける
    year = '2018'
    pool = Pool(multi.cpu_count() - 2)
    list2 = [(S, year, str(m + 3), SUPPLIER_CD, order_count, FC, header) for m in range(10)]
    mk_order_m = pool.map(wrapper2, list2)
    pool.close()
    for i in range(10):
        mk_order = mk_order.append(mk_order_m[i], sort=False)

    year = '2019'
    pool = Pool(multi.cpu_count() - 2)
    list2 = [(S, year, str(m + 1), SUPPLIER_CD, order_count, FC, header) for m in range(3)]
    mk_order_m = pool.map(wrapper2, list2)
    pool.close()
    for i in range(3):
        mk_order = mk_order.append(mk_order_m[i], sort=False)

    return mk_order

def Orders_creation_no_change_date():

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

        header_def = order.columns
        order = order.astype({'数量': float})

        # MASTER_SUPPLIER_FLGのみにする
        order_count = order[order['従来生産拠点フラグ'] == '1']
        # 見積りデータを除く
        order_count = order_count[order_count['見積有効日'].isnull()]
        # RBS仕入先が空白のRECは従来仕入先をコピー　RBS仕入先を使ってフィルタする
        order_count.loc[order_count['RBS_受注現法仕入先コード'].isnull(), 'RBS_受注現法仕入先コード'] = order_count['実績仕入先コード']

        # 番号と現法コード、数量、従来仕入先,顧客希望納期だけにする
        order_count = order_count.loc[:, ['番号', '現法コード', '数量', 'RBS_受注現法仕入先コード', '顧客希望納期']]
        order_count.reset_index(inplace=True, drop=True)
        header = order_count.columns


        # 現法毎のFCを取り込む
        FC = read_fc()
        FC = FC.astype({'FC': int})

        # 日付と拠点毎にデータを分割しFCデータの数量だけRECを抽出する

        # 拠点毎にforで繰り返す(2019)
        mk_order_sum = pd.DataFrame(columns=header)
        for S in range(0, 6):
            df = random_order(S, order_count, FC)
            mk_order_sum = mk_order_sum.append(df, sort=False)

        # 新番号のカラム名を追加する
        mk_order_sum.reset_index(inplace=True, drop=True)
        mk_order_sum.reset_index(inplace=True, drop=False)
        mk_order_sum = mk_order_sum.rename(columns={'index': '新番号'})
        # 不要カラムを除く
        mk_order_sum.drop(['現法コード', '数量', 'RBS_受注現法仕入先コード', '顧客希望納期'], axis=1, inplace=True)

        # 追加する番号のRECをorder情報から作成する
        order = pd.merge(mk_order_sum, order, on=['番号'], how='left')
        order = order.astype({'番号': int})
        # 番号重複しないよう新しい番号を作成
        order.loc[:,'番号'] = order['新番号']
        # 不要カラムを除く
        order.drop(['新番号'], axis=1, inplace=True)

        # indexを振り直す
        order.reset_index(inplace=True, drop=True)

        # 受注日時順に並べ替え
        order = order.sort_values(['JST変換受注日・JST変換見積回答日', 'JST変換受注時間・JST変換見積回答時間', '番号'])
        # MCコードの”NA”が消えてしまうので、NAを書き込む
        order.loc[order['グローバル番号'].str[:2] == "NA", 'ＭＣコード'] = "NA"
        # headerをもとの順に並び替える
        order = order.reindex(columns=header_def)

        # 数量を整数にする
        order = order.astype({'番号': int, '数量': int})
        # ファイルアウトプット
        f_name = 'new_check_input.tsv'
        order.to_csv(local_pass + f_name, sep='\t', encoding=font, quotechar='"', line_terminator='\n', index=False)

    print('ダミーオーダー作成　日付変更なし Finish!')

if __name__ == '__main__':
    Orders_creation_no_change_date()