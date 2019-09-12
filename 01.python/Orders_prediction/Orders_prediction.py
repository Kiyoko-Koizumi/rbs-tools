# coding: utf-8
# Orders prediction 新規作成 2019/2/15
# 0.2マルチコア化
# 0.3Excelの計算方法を踏襲
# 0.4 再開　マルチプロセスを導入
# 大口除く,Excelと一致確認済み
# 当日受注分は除く　対応済み
# 20回ずつプロセスを回す処理でsの繰り返しを19に設定　S+1(q)=20のため
# mod計算間違っており修正
# 長期連休時明けの受注増加考慮
# FCを受注月でなく出荷月でやる

# モジュールのインポート
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import csv
from typing import List

import pandas as pd
import datetime as dt
import tkinter as tk
import tkinter.ttk as ttk
import threading
from dateutil.relativedelta import relativedelta
import pandas.tseries.offsets as offsets
from multiprocessing import Pool
import multiprocessing as multi
import datetime

def getFACI_CD():
    # SELECTボタンが押されたときの動き
    def getitemcode():
        root.withdraw()
        root.quit()

    # 抽出したい製造グループを指定する
    # GUIの作成
    # サプライヤ選択肢を作成
    list_pg = ['7017', '3764', '0FCN', 'SPCM']
    year_l = ['2017', '2018', '2019', '2020', '2021', '2022']
    month_l = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    day_l = []

    for a in range(1, 32):
        day_l.append(str(a))

    # ルートフレームの作成
    root = tk.Tk()
    label1 = tk.Label(root, text="【サプライヤを選択】", font=("", 12), height=2)
    label2 = tk.Label(root, text="【受注データ利用期間　開始日】", font=("", 12), height=2)
    label3 = tk.Label(root, text="【受注データ利用期間　終了日】", font=("", 12), height=2)
    label4 = tk.Label(root, text="【予測データ作成期間　開始日】", font=("", 12), height=2)
    label5 = tk.Label(root, text="【予測データ作成期間　終了日】", font=("", 12), height=2)
    label6 = tk.Label(root, text="年", font=("", 12), height=2)
    label7 = tk.Label(root, text="月", font=("", 12), height=2)
    label8 = tk.Label(root, text="日", font=("", 12), height=2)
    label9 = tk.Label(root, text="年", font=("", 12), height=2)
    label10 = tk.Label(root, text="月", font=("", 12), height=2)
    label11 = tk.Label(root, text="日", font=("", 12), height=2)
    label12 = tk.Label(root, text="年", font=("", 12), height=2)
    label13 = tk.Label(root, text="月", font=("", 12), height=2)
    label14 = tk.Label(root, text="日", font=("", 12), height=2)
    label15 = tk.Label(root, text="年", font=("", 12), height=2)
    label16 = tk.Label(root, text="月", font=("", 12), height=2)
    label17 = tk.Label(root, text="日", font=("", 12), height=2)

    # コンボボックスの作成(rootに配置,リストの値を編集不可(readonly)に設定)

    combo_l = []
    for c in range(13):
        combo = ttk.Combobox(root, state='readonly', width=10)
        combo_l.append(combo)

    # リストの値を設定
    combo_l[0]["values"] = list_pg
    for c in range(1, 5):
        combo_l[c]["values"] = year_l
    for c in range(5, 9):
        combo_l[c]["values"] = month_l
    for c in range(9, 13):
        combo_l[c]["values"] = day_l

    # デフォルトの値を食費(index=0)に設定
    for c in range(13):
        combo_l[c].current(0)

    # コンボボックスの配置
    label1.grid(row=0, column=0)
    combo_l[0].grid(row=0, column=1)
    label2.grid(row=4, column=0)
    combo_l[1].grid(row=4, column=1)
    combo_l[5].grid(row=4, column=3)
    combo_l[9].grid(row=4, column=5)
    label6.grid(row=4, column=2)
    label7.grid(row=4, column=4)
    label8.grid(row=4, column=6)
    label3.grid(row=6, column=0)
    combo_l[2].grid(row=6, column=1)
    combo_l[6].grid(row=6, column=3)
    combo_l[10].grid(row=6, column=5)
    label9.grid(row=6, column=2)
    label10.grid(row=6, column=4)
    label11.grid(row=6, column=6)
    label4.grid(row=8, column=0)
    combo_l[3].grid(row=8, column=1)
    combo_l[7].grid(row=8, column=3)
    combo_l[11].grid(row=8, column=5)
    label12.grid(row=8, column=2)
    label13.grid(row=8, column=4)
    label14.grid(row=8, column=6)
    label5.grid(row=10, column=0)
    combo_l[4].grid(row=10, column=1)
    combo_l[8].grid(row=10, column=3)
    combo_l[12].grid(row=10, column=5)
    label15.grid(row=10, column=2)
    label16.grid(row=10, column=4)
    label17.grid(row=10, column=6)

    # ボタンの作成（コールバックコマンドには、コンボボックスの値を取得する処理を定義）
    button = tk.Button(root, text="select",
                       command=lambda: getitemcode())
    # ボタンの配置
    button.grid(row=11, column=6)

    root.mainloop()
    result = [combo_l[0].get(), combo_l[1].get(), combo_l[2].get(),
              combo_l[3].get(), combo_l[4].get(), combo_l[5].get(),
              combo_l[6].get(),
              combo_l[7].get(), combo_l[8].get(), combo_l[9].get(),
              combo_l[10].get(), combo_l[11].get(), combo_l[12].get()]
    return result


# 数量比率を算出するdefを作成
def qtyratio(s):
    return (s / s.sum().round(3))


# 数量比率を算出するdefを作成
def qtyave(s):
    return (s / s.mean())


# 受注予測を入れるdataframeを作成
def Sub_func(s, so_day_list, sd_day_list, noukizokusei_list, calendar_dict, sub_name):
    # 受注日稼働flgを作成
    so_day_workflg = []
    for x in range(len(so_day_list)):
        cell = so_day_list[x]
        if cell.strftime('%Y-%m-%d') in calendar_dict[sub_name[s]]:
            so_day_workflg.append(0)
        else:
            so_day_workflg.append(1)
    # リストからpredictionを作成
    prediction = pd.DataFrame(
        data={
            '受注日': so_day_list,
            '受注日稼働flg': so_day_workflg,
            '出荷日': sd_day_list,
            '納期属性': noukizokusei_list
        },
        columns=['受注日', '受注日稼働flg', '出荷日', '納期属性']
    )
    # 現法コードを作成
    prediction.loc[:, '現法コード'] = sub_name[s]
    # 出荷日稼働flgを作成
    prediction.loc[:, '出荷日稼働flg'] = 1
    return prediction


def pre_sum2(d, Pre_S, prediction):
    print(d)
    SO_day = Pre_S + dt.timedelta(days=d)
    SO_day_list = []
    pre_qty_list = []
    for k in range(0, 73):
        SD_day = SO_day + dt.timedelta(days=k)
        pre_a = prediction[prediction['受注日'] >= SO_day.strftime('%Y-%m-%d')]
        pre_a = pre_a[pre_a['出荷日'] <= SD_day.strftime('%Y-%m-%d')]
        pre_qty = pre_a['数量'].sum()
        SO_day_list.append(SO_day.strftime('%Y%m%d'))
        pre_qty_list.append(pre_qty)
    ADD_DAYS = list(range(0, 73))
    pre_c = pd.DataFrame(
        data={
            'BASE_DATE': SO_day_list,
            'BASE_DATE_ADD_DAYS': ADD_DAYS,
            'PREDICTION_QUANTITY': pre_qty_list
        },
        columns=['BASE_DATE', 'BASE_DATE_ADD_DAYS', 'PREDICTION_QUANTITY']
    )
    pre_c = pre_c.astype({'BASE_DATE_ADD_DAYS': int, 'PREDICTION_QUANTITY': float})
    return pre_c


def wrapper(args):
    # 複数の引数を渡すためwrapperを経由
    # 現法毎に受注予測データを作成
    return Sub_func(*args)


def wrapper3(args):
    # 複数の引数を渡すためwrapperを経由
    # 現法毎に受注予測データを作成
    return pre_sum2(*args)


def Orders_prediction():

    # from tqdm import tqdm
    csv.field_size_limit(1000000000)

    font = 'utf-8'
    # font='shift_jisx0213'

    # スクリプトのあるディレクトリの絶対パスを取得
    script_pass = os.path.dirname(os.path.abspath(__name__))
    if __name__ == '__main__':
        local_pass = script_pass + '/'
    else:
        local_pass = script_pass + '/Orders_prediction/'

    # ファイル選択ダイアログの表示
    root = tk.Tk()
    root.withdraw()
    fTyp = [("","*")]
    iDir = local_pass

    # 受注実績データの取得
    # ここの1行を変更 askopenfilename → askopenfilenames
    file = tkinter.filedialog.askopenfilenames(filetypes=fTyp, initialdir=iDir, title='受注実績データの取得')

    if len(file) != 0:
        # 選択ファイルリスト作成
        list_f = list(file)

        # リストボックスの作成を実行
        result = getFACI_CD()

        pg_name = result[0]
        check_list = [result[5], result[6], result[7], result[8], result[9], result[10], result[11], result[12]]
        for c in range(len(check_list)):
            if len(check_list[c]) == 1:
                check_list[c] = '0' + check_list[c]

        Tgt_S = result[1] + check_list[0] + check_list[4]
        Tgt_E = result[2] + check_list[1] + check_list[5]
        Pre_S = result[3] + check_list[2] + check_list[6]
        Pre_E = result[4] + check_list[3] + check_list[7]

        # 1つ目のファイルを開く
        f_name = os.path.basename(list_f[0])
        f_pass = os.path.dirname(list_f[0])

        # 必要な列のみ読み込む
        print(f_pass + '/' + f_name)
        order = pd.read_csv(f_pass + '/' + f_name, sep='\t', encoding=font, dtype=object, engine='python', error_bad_lines=False,
                            usecols=['番号', '現法コード', 'グローバル番号', '受注日・見積回答日', '受注時間・見積回答時間', 'JST変換受注日・JST変換見積回答日',
                                     'JST変換受注時間・JST変換見積回答時間', '見積有効日', '見積有効時間', 'JST変換見積有効日', 'JST変換見積有効時間',
                                     'アンフィット種別', '得意先コード', '直送先コード', 'ＭＣコード', 'インナーコード', '商品コード', '実績現法コード', '実績仕入先コード',
                                     '実績管理単位コード', 'ACE仕入先コード', 'ACE仕入先カテゴリコード', '受注実績SSD', '見積回答SSD', '数量', '納入区分',
                                     '顧客希望納期'])

        # ファイルを繰り返し開き結合する
        for r in range(1, len(list_f)):
            f_name = os.path.basename(list_f[r])
            print(f_name)
            order_add = pd.read_csv(f_pass + '/' + f_name, sep='\t', encoding=font, dtype=object, engine='python',
                                    error_bad_lines=False,
                                    usecols=['番号', '現法コード', 'グローバル番号', '受注日・見積回答日', '受注時間・見積回答時間',
                                             'JST変換受注日・JST変換見積回答日', 'JST変換受注時間・JST変換見積回答時間', '見積有効日', '見積有効時間',
                                             'JST変換見積有効日', 'JST変換見積有効時間', 'アンフィット種別', '得意先コード', '直送先コード', 'ＭＣコード',
                                             'インナーコード', '商品コード', '実績現法コード', '実績仕入先コード', '実績管理単位コード', 'ACE仕入先コード',
                                             'ACE仕入先カテゴリコード', '受注実績SSD', '見積回答SSD', '数量', '納入区分', '顧客希望納期'])
            # ファイルを追加する
            order = order.append(order_add, sort=False)

        # 時間を表示
        dt_now = datetime.datetime.now()
        print(dt_now)

        # 非稼働日データを読み込む
        nowork_day = pd.read_csv(local_pass + 'nowork_day.csv', encoding=font, dtype='object', index_col=None)

        # 各現法、拠点の非稼働日をリスト化
        sub_name = ['CHN', 'GRM', 'HKG', 'IND', 'JKT', 'KOR', 'MEX', 'MJP', 'MYS', 'SGP', 'THA', 'TIW', 'USA', 'VNM',
                    '7017', '3764', '0FCN', 'SPCM']
        calendar_name = ['CAAAA', 'GAAAA', 'NAAAA', 'DAAAA', 'JAAAA', 'KAAAA', 'QAAAA', '5AAAA', 'MAAAA', 'SAAAA',
                         'HAAAA', 'TAAAA', 'UAAAA', 'VAAAA', '5AAAA', '5AAAA', 'C8677', '50SPC']
        calendar_dict = {}
        for i in range(0, len(sub_name)):
            noworkday_df = nowork_day[nowork_day['CALENDAR_CD'] == calendar_name[i]]
            noworkday_df = noworkday_df.loc[::, ['OFF_DATE']]
            noworkday_df = noworkday_df.T
            noworkday_list = noworkday_df.values.tolist()
            calendar_dict[sub_name[i]] = noworkday_list[0]

        # 見積りデータを除く
        order = order[order['見積有効日'].isnull()]

        # 受注日・見積回答日の名前を変える
        order = order.rename(columns={'受注日・見積回答日': '受注日'})
        order = order.astype({'受注日': int, '受注実績SSD': int})

        # 出荷実績SSDデータ利用期間に限定する
        # 基本的に受注予測は受注日でのサマリ
        # 条件を作成
        condition = Tgt_S + ' <= 受注日 <= ' + Tgt_E
        order = order.query(condition)
        # orderのサプライヤコードが指定のサプライヤのものだけにする
        order = order[order['実績仕入先コード'] == pg_name]

        # 受注日、出荷日をdate形式へ変更
        order = order.astype({'受注日': str, '受注実績SSD': str})
        order['受注日'] = order['受注日'].str[0:4] + '-' + order['受注日'].str[4:6] + '-' + order['受注日'].str[6:8]
        order['受注実績SSD'] = order['受注実績SSD'].str[0:4] + '-' + order['受注実績SSD'].str[4:6] + '-' + order['受注実績SSD'].str[6:8]

        # 受注曜日カラムを追加
        order['weekday'] = [dt.datetime.strptime(x, "%Y-%m-%d").strftime('%a') for x in order['受注日']]

        # 受注日と受注実績SSDをdate形式に変換
        order['受注日'] = pd.to_datetime(order['受注日'])
        order['受注実績SSD'] = pd.to_datetime(order['受注実績SSD'])

        # 受注日をDatetimeIndexとし年、月、曜日のindexを追加
        order = order.set_index('受注日')
        order = order.set_index([order.index.year, order.index.month, order.index])
        order.index.names = ['year', 'month', '受注日']
        order = order.reset_index()

        # 納期属性カラムを追加
        # 非稼働日カレンダを指定
        nowork_day_w = calendar_dict[pg_name][:]

        # カレンダのリストのstrを1行ずつdate形式に変換
        for i in range(0, len(nowork_day_w)):
            nowork_day_w[i] = dt.datetime.strptime(nowork_day_w[i], "%Y-%m-%d")

        # 納期属性を計算
        order['納期属性'] = [(z - y).days - len(list(filter(lambda x: y <= x <= z, nowork_day_w))) for y, z in
                         zip(order['受注日'], order['受注実績SSD'])]

        # 納期属性を73以上は全て73,0未満のRECは0へ（削除も検討？正しくない）
        order.loc[order['納期属性'] > 73, '納期属性'] = 73
        order.loc[order['納期属性'] < 0, '納期属性'] = 0
        # order = order.query('納期属性 >= 0')
        order = order.astype({'数量': int})

        # 現法毎の実績,稼働日数を集計
        # 現法毎の年間数量を集計

        order_subtotal = order.groupby(['year', 'month'], as_index=False)['数量'].sum()
        order_subtotal = order_subtotal.astype({'year': str, 'month': str})
        # order_subtotalを割る製造拠点の稼働日を集計
        order_subtotal['開始日'] = pd.to_datetime((order_subtotal['year'] + '/' + order_subtotal['month'] + '/01'),
                                               format='%Y/%m/%d')
        order_subtotal['終了日'] = order_subtotal['開始日'] + offsets.MonthBegin(1)
        order_subtotal['月稼働日'] = [(z - y).days - len(list(filter(lambda x: y <= x < z, nowork_day_w))) for y, z in
                                  zip(order_subtotal['開始日'], order_subtotal['終了日'])]
        order_subtotal['月平均本数'] = (order_subtotal['数量'] / order_subtotal['月稼働日']).round(3)

        # 現法毎の期間中の受注数量比を算出
        order_subratio = order.groupby(['year', '現法コード'], as_index=False)['数量'].sum()
        order_subratio['合計'] = order_subtotal['数量'].sum()
        order_subratio['ratio'] = (order_subratio['数量'] / order_subratio['合計']).round(3)
        order_subratio.drop(['数量', '合計'], axis=1, inplace=True)

        # 月ごとの数量合計に現法比率をかける yearのtypeを統一する
        order_subtotal = order_subtotal.astype({'year': int, 'month': int})
        order_subtotal = pd.merge(order_subtotal, order_subratio, on=['year'], how='left')
        order_subtotal['月平均本数'] = (order_subtotal['月平均本数'] * order_subtotal['ratio']).round(3)

        # とりあえず実績をFCの数値をして利用する
        # FCを実績で作成する場合は期間を出荷日で規定
        # しかし受注予測は受注日で規定　Tgt_S,Eを使ったフィルタリングでは不足
        # とはいえ基本的にFCは外から入れることにする
        # 不要列削除
        # order_subtotal.drop(['数量', '開始日', '終了日', '月稼働日', 'ratio'], axis=1, inplace=True)
        # FC = order_subtotal

        # FCデータ取り込み
        FC = pd.read_csv(local_pass + 'FC.csv', encoding=font, dtype='object', index_col=None)
        # header名の変更
        FC = FC.rename(columns={'SUBSIDIARY_CD': '現法コード'})
        # SUPPLIER_CDの指定
        FC = FC[FC['SUPPLIER_CD'] == pg_name]
        FC = FC.astype({'year': str, 'month': str, 'FC': float})

        # FCを割る製造拠点の稼働日を集計しFCを日当り数量へ
        FC['開始日'] = pd.to_datetime((FC['year'] + '/' + FC['month'] + '/01'), format='%Y/%m/%d')
        FC['終了日'] = FC['開始日'] + offsets.MonthBegin(1)
        FC['月稼働日'] = [(z - y).days - len(list(filter(lambda x: y <= x < z, nowork_day_w))) for y, z in
                      zip(FC['開始日'], FC['終了日'])]
        FC['月平均本数'] = (FC['FC'] / FC['月稼働日']).round(3)
        FC = FC.astype({'year': int, 'month': int})

        # 曜日ごとの稼働日をカウント
        Tgt_S = dt.datetime.strptime(Tgt_S, '%Y%m%d')
        Tgt_E = dt.datetime.strptime(Tgt_E, '%Y%m%d')
        week_count = pd.DataFrame({'count': [], 'weekday': []})
        count = 0
        while Tgt_S <= Tgt_E:
            if not Tgt_S.strftime('%Y-%m-%d') in calendar_dict[pg_name]:
                weekday = Tgt_S.strftime('%a')
                week_count.loc[count] = [Tgt_S, weekday]
                count += 1
            Tgt_S = Tgt_S + dt.timedelta(days=1)
        week_count = week_count.groupby(['weekday'], as_index=False).count()

        # 曜日指数計算
        # 日付毎に数量を集計
        # 大口を除く
        order_small = order[order['アンフィット種別'] == '0']
        order_day = order_small.groupby(['現法コード', 'weekday', '受注日'], as_index=False)['数量'].sum()
        order_week = order_day.groupby(['現法コード', 'weekday'], as_index=False)['数量'].sum()
        order_week = pd.merge(order_week, week_count, on=['weekday'], how='left')
        order_week.loc[order_week['count'] != 0, '数量'] = order_week['数量'] / order_week['count']
        order_week.loc[order_week['count'] == 0, '数量'] = 0
        order_week1 = order_week[order_week['weekday'] != 'Sun']
        order_week1 = order_week1.groupby(['現法コード', 'weekday'])['数量'].sum()
        order_week1 = order_week1.groupby(['現法コード']).transform(qtyave)
        order_week2 = order_week.groupby(['現法コード', 'weekday'])['数量'].sum()
        order_week2 = order_week2.groupby(['現法コード']).transform(qtyave)
        order_week1 = order_week1.reset_index()
        order_week2 = order_week2.reset_index()
        order_week2 = order_week2[order_week2['weekday'] == 'Sun']
        order_week1 = order_week1.append(order_week2, sort=False)
        order_week1 = order_week1.rename(columns={'数量': 'week_ratio'})

        # 現法、曜日、納期属性の箱を用意
        base_sh = pd.read_csv(local_pass + 'base_sh.csv', encoding=font, index_col=None, dtype={'数量': int, '納期属性': int})

        # 現法、曜日、納期属性毎の数量を合計
        order_A = order[order['アンフィット種別'] == '0']  # 大口を除く
        order_A = order_A.groupby(['現法コード', 'weekday', '納期属性'])['数量'].sum()
        order_A = order_A.groupby(['現法コード', 'weekday']).transform(qtyratio)
        order_A = order_A.reset_index()

        # base_shと結合し0を補足
        base_sh = pd.merge(base_sh, order_A, on=['現法コード', 'weekday', '納期属性'], how='outer')
        base_sh.loc[base_sh['数量_y'].notnull(), '数量_x'] = base_sh['数量_y']
        base_sh = base_sh.rename(columns={'数量_x': '数量'})
        base_sh.drop(['数量_y'], axis=1, inplace=True)
        base_sh = base_sh.round({'数量': 4})
        base_sh = base_sh.rename(columns={'数量': 'n_ratio'})

        # 小口比率を計算
        small_ratio = order.groupby(['現法コード'], as_index=False)['数量'].sum()
        small_ratio_A = order[order['アンフィット種別'] == '0']  # 大口を除く
        small_ratio_A = small_ratio_A.groupby(['現法コード'], as_index=False)['数量'].sum()
        small_ratio = pd.merge(small_ratio_A, small_ratio, on=['現法コード'], how='right')
        small_ratio.loc[small_ratio['数量_x'].isnull(), '数量_x'] = 0
        small_ratio['small_ratio'] = small_ratio['数量_x'] / small_ratio['数量_y']
        small_ratio.drop(['数量_x', '数量_y'], axis=1, inplace=True)

        # 開始日終了日をdate形式に
        Pre_S = dt.datetime.strptime(Pre_S, '%Y%m%d')
        Pre_E = dt.datetime.strptime(Pre_E, '%Y%m%d')

        # 受注日のリストを作成
        day_list = [Pre_S]
        day_n = Pre_S
        while day_n <= Pre_E:
            day_list.append(day_n)
            day_n = day_n + datetime.timedelta(days=1)
            # prediction = pd.date_range(start=Pre_S, end=Pre_E, freq='D', name='受注日')
            # prediction = prediction.to_series()
            # prediction = pd.DataFrame(prediction)
        # 受注日*出荷日のリストを作成
        so_day_list = []
        sd_day_list = []
        noukizokusei = list(range(73))
        noukizokusei_list = []
        for nouki in range(len(day_list)):
            for n in range(73):
                so_day_list.append(day_list[nouki])
            noukizokusei_list.extend(noukizokusei)
        # 受注日と納期属性から出荷日を作成
        for nouki_b in range(len(so_day_list)):
            sd_day = so_day_list[nouki_b] + datetime.timedelta(days=noukizokusei_list[nouki_b])
            # 出荷日稼働flgを作成し非稼働日なら+1する
            while sd_day.strftime('%Y-%m-%d') in calendar_dict[pg_name]:
                sd_day = sd_day + dt.timedelta(days=1)
            sd_day_list.append(sd_day)

        # マルチプロセス処理の結果を入れるdfを作成
        prediction_sum = pd.DataFrame({'現法コード': [], '受注日': [], '受注日稼働flg': [], '出荷日': [], '出荷日稼働flg': [], '納期属性': []})
        # 現法毎にマルチプロセスで処理
        pool = Pool(multi.cpu_count() - 2)
        list1 = [(x, so_day_list, sd_day_list, noukizokusei_list, calendar_dict, sub_name) for x in range(14)]
        pre_list = pool.map(wrapper, list1)
        pool.close()

        # 返り値がlist形式で格納しされるのでfor文で結合
        for x in range(14):
            prediction_sum = prediction_sum.append(pre_list[x], sort=False)

        # 受注曜日カラムを追加
        prediction = prediction_sum
        prediction['weekday'] = [x.strftime('%a') for x in prediction['受注日']]

        '''
        # 受注日をDatetimeIndexとし年、月、曜日のindexを追加
        prediction = prediction.set_index('受注日')
        prediction = prediction.set_index([prediction.index.year, prediction.index.month, prediction.index])
        prediction.index.names = ['year_so', 'month_so', '受注日']
        prediction = prediction.reset_index()
        '''
        # 出荷日をDatetimeIndexとし年、月、曜日のindexを追加
        prediction = prediction.set_index('出荷日')
        prediction = prediction.set_index([prediction.index.year, prediction.index.month, prediction.index])
        prediction.index.names = ['year', 'month', '出荷日']
        prediction = prediction.reset_index()

        # FCを結合
        prediction = pd.merge(prediction, FC, on=['現法コード', 'year', 'month'], how='left')
        # 曜日比率を結合
        prediction = pd.merge(prediction, order_week1, on=['現法コード', 'weekday'], how='left')
        # 納期属性を結合
        prediction = pd.merge(prediction, base_sh, on=['現法コード', 'weekday', '納期属性'], how='left')
        # 小口比率を追加
        prediction = pd.merge(prediction, small_ratio, on=['現法コード'], how='left')
        # ブランクを0で埋める
        prediction.loc[prediction['月平均本数'].isnull(), '月平均本数'] = 0
        prediction.loc[prediction['week_ratio'].isnull(), 'week_ratio'] = 0

        # 現法毎日当たり数量を算出
        prediction['数量'] = prediction['受注日稼働flg'] * prediction['出荷日稼働flg'] * prediction['月平均本数'] * prediction[
            'week_ratio'] * prediction['n_ratio'] * prediction['small_ratio']
        prediction = prediction.round({'数量': 3})

        # 受注日と出荷日毎のデータを出力
        f_name = pg_name + '_prediction_row.tsv'
        prediction.to_csv(local_pass + f_name, sep='\t', encoding=font, quotechar='"', line_terminator='\n', index=False)

        # 受注日*出荷日毎の数量を合計 日付の型をあとで修正
        prediction = prediction.groupby(['受注日', '出荷日'], as_index=False)['数量'].sum()
        prediction['受注日'] = pd.to_datetime(prediction['受注日'])

        q, mod = divmod(((Pre_E - Pre_S).days + 1), 20)
        FACILITY_DICT = {}
        FACILITY_DICT['7017'] = ['MJP', '7017', 'MAL']
        FACILITY_DICT['3764'] = ['MJP', '3764', 'AAL']
        FACILITY_DICT['0FCN'] = ['CHN', '0FCN', 'FAL']
        FACILITY_DICT['SPCM'] = ['VNM', 'SPCM', 'SAL']

        FACILITY_L = FACILITY_DICT[pg_name]

        # ■受注予測(d)　対象日から見た予測数量積み上げ分
        # マルチプロセス対応 マルチプロセス回数は20回とする
        pre_c = pd.DataFrame({'BASE_DATE': [], 'BASE_DATE_ADD_DAYS': [], 'PREDICTION_QUANTITY': []})
        pre_c = pre_c.astype({'BASE_DATE_ADD_DAYS': int, 'PREDICTION_QUANTITY': float})
        # q*20パート
        for s in range(0, q):
            pool = Pool(multi.cpu_count() - 2)
            list3 = [(d, Pre_S, prediction) for d in range((20 * s), (20 * s + 20))]
            prediction_sum3 = pool.map(wrapper3, list3)
            pool.close()
            for d in range(0, 20):
                pre_c = pre_c.append(prediction_sum3[d], sort=False)
        # modパート
        pool = Pool(multi.cpu_count() - 2)
        list3 = [(d, Pre_S, prediction) for d in range((20 * q), (20 * q + mod))]
        prediction_sum4 = pool.map(wrapper3, list3)
        pool.close()
        for d in range(0, mod):
            pre_c = pre_c.append(prediction_sum4[d], sort=False)

        pre_c.reset_index(drop=True, inplace=True)

        Today = "'" + dt.datetime.today().strftime("%Y-%m-%d") + "'"
        pre_c.loc[:, 'SUBSIDIARY_CD'] = FACILITY_L[0]
        pre_c.loc[:, 'SUPPLIER_CD'] = FACILITY_L[1]
        pre_c.loc[:, 'FACILITY_CD'] = FACILITY_L[2]
        pre_c.loc[:, 'UPD_COUNT'] = '0'
        pre_c.loc[:, 'DEL_FLG'] = '0'
        pre_c.loc[:, 'REG_USR'] = None
        pre_c.loc[:, 'REG_TIME'] = Today
        pre_c.loc[:, 'UPD_USR'] = None
        pre_c.loc[:, 'UPD_TIME'] = Today

        prediction = pre_c
        prediction = prediction.loc[:,
                     ['SUBSIDIARY_CD', 'SUPPLIER_CD', 'FACILITY_CD', 'BASE_DATE', 'BASE_DATE_ADD_DAYS',
                      'PREDICTION_QUANTITY', 'UPD_COUNT', 'DEL_FLG', 'REG_USR', 'REG_TIME', 'UPD_USR', 'UPD_TIME']]

        '''
        # FACILITY_CD_ratioを読み込み、他の設備の予測も作成する
        FACI_r = pd.read_csv('FACILITY_CD_ratio.tsv', sep='\t', encoding=font, dtype=object, engine='python', error_bad_lines=False)
        FACI_r = FACI_r.astype({'ratio': float})
        prediction = pd.merge(prediction, FACI_r, on=['SUBSIDIARY_CD', 'SUPPLIER_CD'], how='left')
        prediction['PREDICTION_QUANTITY'] = (prediction['PREDICTION_QUANTITY'] * prediction['ratio']).round(2)
        prediction.drop(['FACILITY_CD_AL', 'ratio'], axis=1, inplace=True)
        prediction = prediction.loc[:,['SUBSIDIARY_CD', 'SUPPLIER_CD', 'FACILITY_CD', 'BASE_DATE', 'BASE_DATE_ADD_DAYS', 'PREDICTION_QUANTITY', 'UPD_COUNT', 'DEL_FLG', 'REG_USR', 'REG_TIME', 'UPD_USR', 'UPD_TIME']]
        '''

        # ファイルアウトプット
        prediction = prediction.round({'PREDICTION_QUANTITY': 3})

        f_name = pg_name + '_prediction.tsv'
        prediction.to_csv(local_pass + f_name, sep='\t', encoding=font, quotechar='"', line_terminator='\n', index=False)

        # 時間を表示
        dt_now = datetime.datetime.now()
        print(dt_now)

    print('受注予測作成 Finish!')

if __name__ == '__main__':
    Orders_prediction()