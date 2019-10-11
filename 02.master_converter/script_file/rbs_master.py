# coding: utf-8
# master summary 新規作成 2019/4/22
# INNER7のフィルタをskip　2019/07/16
# grp_rbs作成ステップを新規追加　2019/07/17

# モジュールのインポート
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import csv
import pandas as pd
import tkinter as tk
import tkinter.ttk as ttk


def inner7(local_pass, font):
    # SELECTボタンが押されたときの動き
    def getitemcode():
        root.withdraw()
        root.quit()

    # R.B.S対象ファミリーを選択
    list_pg = ['LS', 'LP', 'TP']

    # 抽出したい製造グループを指定する
    # GUIの作成
    # ルートフレームの作成
    root = tk.Tk()
    root.deiconify()
    root.title('select')
    label1 = tk.Label(root, text="【製造GRを選択】", font=("", 16), height=2)
    label1.pack(fill="x")

    # コンボボックスの作成(rootに配置,リストの値を編集不可(readonly)に設定)
    combo = ttk.Combobox(root, state='readonly')
    # リストの値を設定
    combo["values"] = list_pg
    # デフォルトの値を(index=0)に設定
    combo.current(0)
    # コンボボックスの配置
    combo.pack()

    # ボタンの作成（コールバックコマンドには、コンボボックスの値を取得する処理を定義）
    button2 = tk.Button(root, text="select", command=lambda: getitemcode())
    # ボタンの配置
    button2.pack()
    root.mainloop()
    result = combo.get()
    return result


# ダブルコーテーション置き換え
def check_wq(list_f, font):
    for i in range(0, len(list_f)):
        f_name = os.path.basename(list_f[i])
        f_pass = os.path.dirname(list_f[i])
        with open(f_pass + '/' + f_name, 'r', encoding=font) as f:
            file = f.read()
            if '"' in file:
                print(f_pass + '/' + f_name + 'にダブルコーテーションが含まれるため置き換えて新規に保存します')
                file = file.replace('"', '')
                f_name = 'new_' + f_name
                st = open(f_pass + '/' + f_name, 'w', encoding=font)
                st.write(file)
                st.close()
                list_f[i] = f_pass + '/' + f_name


def read_data(title, font):
    # ファイル選択ダイアログの表示
    root = tkinter.Tk()
    root.withdraw()
    fTyp = [("", "*")]
    iDir = '../RBS_Master/input/'

    # 受注実績データの取得
    # ここの1行を変更 askopenfilename → askopenfilenames
    tkinter.messagebox.showinfo('マスタまとめプログラム', title + 'を選択してください！')
    file = tkinter.filedialog.askopenfilenames(filetypes=fTyp, initialdir=iDir)

    # 選択ファイルリスト作成
    list_f = list(file)

    check_wq(list_f, font)

    # 1つ目のファイルを開く
    f_name = os.path.basename(list_f[0])
    f_pass = os.path.dirname(list_f[0])

    # 必要な列のみ読み込む
    order = pd.read_csv(f_pass + '/' + f_name, sep='\t', encoding=font, dtype=object, engine='python', error_bad_lines=False)

    # ファイルを繰り返し開き結合する
    for r in range(1, len(list_f)):
        f_name = os.path.basename(list_f[r])
        order_add = pd.read_csv(f_pass + '/' + f_name, sep='\t', encoding=font, dtype=object, engine='python', error_bad_lines=False)
        # ファイルを追加する
        order = order.append(order_add, sort=False)
    order.reset_index(drop=True, inplace=True)

    return order


def DATA_SEL():
    # SELECTボタンが押されたときの動き
    def getitemcode(item_name):
        global sorce
        sorce = item_name
        root.withdraw()
        root.quit()

    # GUIの作成
    # ルートフレームの作成
    root = tk.Tk()
    root.deiconify()
    root.title('データソース選択')
    # ボタンの作成（コールバックコマンドには、コンボボックスの値を取得する処理を定義）
    button_a = tk.Button(root, text="ZETTA", command=lambda: getitemcode('zetta'))
    button_b = tk.Button(root, text="ミスミダウンロードサイト", command=lambda: getitemcode('DLsite'))
    # ボタンの配置
    button_a.pack()
    button_b.pack()

    root.mainloop()
    return sorce


def rbs_master():
    # from tqdm import tqdm
    csv.field_size_limit(1000000000)

    # スクリプトのあるディレクトリの絶対パスを取得
    script_pass = os.path.dirname(os.path.abspath(__name__))
    local_pass = script_pass + '/'
    out_pass = '../RBS_Master/output/'

    font = 'utf-8'
    # font='shift_jisx0213'

    # inner7マスタで任意のグループのみを抽出→skip
    # 指定のグループによってR.B.S対象サプライヤを選択する
    pgname = inner7(local_pass, font)

    # ZETTAダウンロードデータかミスミダウンロードサイトか選ぶ
    data_s = DATA_SEL()

    # ZETTAからのダウンロードの場合、font='utf_16'へ
    if data_s == 'zetta':
        font = 'utf_16'

    # 商品マスタデータを読み込む
    product_master_m = read_data('商品マスタ', font)
    # 商品別仕入先マスタデータを読み込む
    product_mlt_m = read_data('商品別仕入先マスタ', font)

    font = 'utf_8'

    # 商品別仕入先マスタのheaderを読み込む

    prod_mlt_supp_header = pd.read_csv('../RBS_Master/config/prod_mlt_supp_header.tsv', sep='\t', encoding=font, dtype=object,
                                       engine='python', error_bad_lines=False)

    # 必要なカラムだけにする
    if data_s == 'zetta':
        product_master = product_master_m.iloc[:, [2, 3, 4, 5, 88, 89, 112, 116]]
        product_mlt = product_mlt_m.iloc[:, [2, 3, 4, 6, 7]]
        # XXX行を除く
        product_master = product_master[product_master['Subsidiary Code'] != 'XXX']
        product_mlt = product_mlt[product_mlt['現法コード'] != 'XXX']
        product_mlt = product_mlt.rename(columns={'現法コード': 'Subsidiary Code',
                                                  'インナーコード': 'Inner Code',
                                                  '商品コード': 'Product Code',
                                                  'ＭC/置場コード': 'MC_PLANT_CD',
                                                  '仕入先コード': 'Supplier Code'})
        product_master.loc[:, 'CLASSIFY_CD'] = 'ZETTAマスタのためデータなし'
        product_mlt.loc[:, 'CLASSIFY_CD'] = 'ZETTAマスタのためデータなし'

    elif data_s == 'DLsite':
        # ダウンロードサイトからのデータの場合上記に変わり以下を実行
        product_master_m = product_master_m.rename(columns={'SUBSIDIARY_CD': 'Subsidiary Code',
                                                        'INNER_CD': 'Inner Code',
                                                        'PRODUCT_CD': 'Product Code',
                                                        'STOCK_DIV': 'Stock / MTO',
                                                        'SLIDE_QTY1': 'Slide Qty 1',
                                                        'SLIDE_QTY2': 'Slide Qty 2',
                                                        'SLIDE_QTY3': 'Slide Qty 3',
                                                        'SLIDE_QTY4': 'Slide Qty 4',
                                                        'SLIDE_QTY5': 'Slide Qty 5',
                                                        'SLIDE_QTY6': 'Slide Qty 6',
                                                        'SLIDE_QTY7': 'Slide Qty 7',
                                                        'SLIDE_QTY8': 'Slide Qty 8',
                                                        'SLIDE_QTY9': 'Slide Qty 9',
                                                        'SLIDE_QTY10': 'Slide Qty 10',
                                                        'Q_RANK_DIV': 'Prod Mst for Alt Supplier',
                                                        'SUPPLIER_CD': 'Supplier Code',
                                                        'PRODUCT_ASSORT': 'Product Special Flg',
                                                        'SO_STOP_FLG': 'SO Suspension'})
        product_mlt_m = product_mlt_m.rename(columns={'SUBSIDIARY_CD': 'Subsidiary Code',
                                                  'INNER_CD': 'Inner Code',
                                                  'PRODUCT_CD': 'Product Code',
                                                  'SUPPLIER_CD': 'Supplier Code'})
        product_master = product_master_m.iloc[:, [0, 1, 2, 3, 84, 86, 87, 110, 114]]
        product_mlt = product_mlt_m.iloc[:, [0, 1, 2, 4, 5, 59]]
        # 指定のグループによってR.B.S対象分析コードを限定する
        if pgname == 'LS':
            product_master = product_master[product_master['CLASSIFY_CD'] == '03721101']
        elif pgname == 'LP':
            product_master = product_master[product_master['CLASSIFY_CD'] == '03722108']
        elif pgname == 'TP':
            product_master = product_master[product_master['CLASSIFY_CD'] == '03622710']

    # 在庫品、販売中止、海外顧客用のインナーは除く
    product_master = product_master[
        (product_master['Stock / MTO'] == '1') & (product_master['Product Special Flg'] == '0') & (
                product_master['SO Suspension'] == '0')]

    # 商品マスタで通常販売及びQランク登録されているインナーのみにする
    # 現法とインナーコードのリストを作成
    product_master_l = product_master[(product_master['Prod Mst for Alt Supplier'] != '0')]  # 利用されていない商品別仕入先マスタを削除
    product_master_l = product_master_l.iloc[:, [0, 1, 4]]  # 商品区分のため、分析コード追加
    product_master_l.drop_duplicates(inplace=True)
    product_mlt = pd.merge(product_mlt, product_master_l, on=['Subsidiary Code', 'Inner Code', 'CLASSIFY_CD'],
                           how='inner')

    # 商品マスタにQランク00を登録する
    product_master['MC_PLANT_CD'] = '00'

    # 商品マスタと商品別仕入先マスタをマージする
    product_master.drop(['Stock / MTO', 'Prod Mst for Alt Supplier', 'Product Special Flg', 'SO Suspension'], axis=1,
                        inplace=True)
    product_master = product_master.append(product_mlt, sort=False)
    product_master = product_master[product_master['Supplier Code'].notnull()]
    product_master.reset_index(drop=True, inplace=True)

    # inner7マスタを指定のグループだけにする→skip
    '''
    Inner7_M = Inner7_M.loc[:, ['製造GR', 'インナー7']]
    Inner7_M.drop_duplicates(keep='first', inplace=True)  # 重複削除
    Inner7_M = Inner7_M[Inner7_M['製造GR'] == pg_name]

    product_master['インナー7'] = product_master['Inner Code'].str[0:7]
    product_master = pd.merge(product_master, Inner7_M, on='インナー7', how='inner')
    product_master.drop(['インナー7', '製造GR'], axis=1, inplace=True)

    product_master.reset_index(drop=True, inplace=True)
    '''

    # マルチカラム化のために重複削除
    product_master.drop_duplicates(inplace=True)

    # 現法をインデックス化
    grp_sub = product_master.set_index(['Product Code', 'Inner Code', 'MC_PLANT_CD', 'Subsidiary Code', 'CLASSIFY_CD'],
                                       inplace=False)

    # 現法をマルチカラム化
    grp_sub = grp_sub.unstack('MC_PLANT_CD')
    grp_sub = grp_sub.unstack('Subsidiary Code')
    grp_sub = grp_sub.swaplevel(axis=1).sort_index(axis=1)
    grp_sub.dropna(axis=1, how='all', inplace=True)

    # 仕入先をインデックス化
    # 現法情報削除、重複削除
    grp_supp = product_master.copy()
    grp_supp['Subsidiary Code'] = '1'
    grp_supp.drop(['MC_PLANT_CD'], axis=1, inplace=True)
    grp_supp.drop_duplicates(inplace=True)

    # 仕入先コードを限定
    # 指定のグループによってR.B.S対象サプライヤを選択する
    if pgname == 'LS':
        grp_supp = grp_supp[(grp_supp['Supplier Code'] == '7017') | (grp_supp['Supplier Code'] == '3764') | (
                grp_supp['Supplier Code'] == '0FCN') | (grp_supp['Supplier Code'] == 'SPCM')]
    elif pgname == 'LP' or pgname == 'TP':
        grp_supp = grp_supp[(grp_supp['Supplier Code'] == '0143') | (
                grp_supp['Supplier Code'] == '0AIO') | (grp_supp['Supplier Code'] == 'SPCM')]

    # 仕入先コードを限定 product_masterにも
    # 指定のグループによってR.B.S対象サプライヤを選択する
    if pgname == 'LS':
        product_master = product_master[
            (product_master['Supplier Code'] == '7017') | (product_master['Supplier Code'] == '3764') | (
                    product_master['Supplier Code'] == '0FCN') | (product_master['Supplier Code'] == 'SPCM') | (
                    product_master['Supplier Code'] == 'ECAL') | (
                    product_master['Supplier Code'] == 'FCNX') | (product_master['Supplier Code'] == 'FCNT')]
    elif pgname == 'LP' or pgname == 'TP':
        product_master = product_master[(product_master['Supplier Code'] == '0143') | (
                product_master['Supplier Code'] == '0AIO') | (product_master['Supplier Code'] == 'SPCM') | (
                                                product_master['Supplier Code'] == 'ECAL') | (
                                                product_master['Supplier Code'] == 'AIOX') | (
                                                    product_master['Supplier Code'] == 'AIOT')]

    # new_mlt用にrbs_product_masterをkeep
    rbs_product_mlt = product_master.copy()

    # 管理単位コードの作成
    managed_unit_cd_dict = {'LS': 'Z10', 'TP': 'P10', 'LP': 'I10'}

    grp_supp_temp = grp_supp.copy()
    grp_supp = grp_supp.set_index(['Product Code', 'Inner Code', 'Supplier Code', 'CLASSIFY_CD'], inplace=False)

    # 現法をマルチカラム化
    grp_supp = grp_supp.unstack('Supplier Code')
    grp_supp = grp_supp.swaplevel(axis=1).sort_index(axis=1)
    grp_supp.dropna(axis=1, how='all', inplace=True)

    # product_masterから'Subsidiary Code', 'Product Code'のみの既存マスタにおけるR.B.S対象リストを作成
    rbs_product_master = product_master.copy()
    # MC_PLANT_CDが00（商品マスタ）→商品別仕入先マスタの順で並んでいる前提で重複削除
    rbs_product_master.drop_duplicates(subset=['Subsidiary Code', 'Product Code'], keep='first', inplace=True)
    # 既存マスタを'MC_PLANT_CD'='00'で表現
    rbs_product_master.loc[:, 'MC_PLANT_CD'] = '00'

    # grp_supp_tempのSubsidiary Code,Inner Code,CLASSIFY_CDを削除,Supplier Codeの名前を変更する
    grp_supp_temp.drop(['Subsidiary Code', 'Inner Code', 'CLASSIFY_CD'], axis=1, inplace=True)
    grp_supp_temp = grp_supp_temp.rename(columns={'Supplier Code': 'Supplier Code2'})

    # rbs_product_masterとgrp_supp_tempをProduct_Codeをキーにして結合
    rbs_product_master2 = pd.merge(rbs_product_master, grp_supp_temp, on=['Product Code'], how='inner')

    # MC_PLANT_CDにSupplier Codeを転記、その後削除
    rbs_product_master2['MC_PLANT_CD'] = rbs_product_master2['Supplier Code2']
    rbs_product_master2.drop(['Supplier Code2'], axis=1, inplace=True)

    # rbs_product_masterとrbs_product_master2を結合
    rbs_product_master = rbs_product_master.append(rbs_product_master2, sort=False)

    # 仕入先コードをMC_PLANT_CDに合わせて書き換え
    rbs_product_master.loc[(((rbs_product_master['MC_PLANT_CD'] == '0143') | (
            rbs_product_master['MC_PLANT_CD'] == '0269') | (
                                     rbs_product_master['MC_PLANT_CD'] == '7017') | (
                                     rbs_product_master['MC_PLANT_CD'] == '3764')) & (
                                    rbs_product_master['Subsidiary Code'] != 'MJP')), 'Supplier Code'] = 'ECAL'
    rbs_product_master.loc[((rbs_product_master['MC_PLANT_CD'] == '0143') & (
            rbs_product_master['Subsidiary Code'] == 'MJP')), 'Supplier Code'] = '0143'
    rbs_product_master.loc[((rbs_product_master['MC_PLANT_CD'] == '0269') & (
            rbs_product_master['Subsidiary Code'] == 'MJP')), 'Supplier Code'] = '0269'
    rbs_product_master.loc[((rbs_product_master['MC_PLANT_CD'] == '0AIO') & (
            rbs_product_master['Subsidiary Code'] != 'CHN')), 'Supplier Code'] = 'AIOX'
    rbs_product_master.loc[((rbs_product_master['MC_PLANT_CD'] == '0AIO') & (
            rbs_product_master['Subsidiary Code'] == 'CHN')), 'Supplier Code'] = '0AIO'
    rbs_product_master.loc[((rbs_product_master['MC_PLANT_CD'] == '7017') & (
            rbs_product_master['Subsidiary Code'] == 'MJP')), 'Supplier Code'] = '7017'
    rbs_product_master.loc[((rbs_product_master['MC_PLANT_CD'] == '3764') & (
            rbs_product_master['Subsidiary Code'] == 'MJP')), 'Supplier Code'] = '3764'
    rbs_product_master.loc[((rbs_product_master['MC_PLANT_CD'] == '0FCN') & (
            rbs_product_master['Subsidiary Code'] != 'CHN')), 'Supplier Code'] = 'FCNX'
    rbs_product_master.loc[((rbs_product_master['MC_PLANT_CD'] == '0FCN') & (
            rbs_product_master['Subsidiary Code'] == 'CHN')), 'Supplier Code'] = '0FCN'
    rbs_product_master.loc[(rbs_product_master['MC_PLANT_CD'] == 'SPCM'), 'Supplier Code'] = 'SPCM'

    # rbs_product_masterとrbs_product_mltの差分を確認し、差分が新たに商品別仕入先マスタ作成必要なもの
    # R.B.S対象インナーに限定するためのProduct Codeに限定
    rbs_product = rbs_product_master['Product Code']  # Seriesを作成
    rbs_product.drop_duplicates(keep='first', inplace=True)
    # rbs_product_mltをrbs_productでフィルタ
    rbs_product_mlt = rbs_product_mlt[rbs_product_mlt['Product Code'].isin(rbs_product)]
    new_mlt = rbs_product_master.append(rbs_product_mlt, sort=False)
    new_mlt.reset_index(drop=True, inplace=True)
    new_mlt.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'Supplier Code'], keep='first', inplace=True)

    # マルチカラム化のために重複削除
    rbs_product_master.reset_index(drop=True, inplace=True)
    rbs_product_master.drop_duplicates(inplace=True)

    # R.B.Sオーダー振替設定マスタ用dfの作成
    m_rbs_order_transfer = rbs_product_master.loc[:, ['Subsidiary Code', 'Inner Code']].copy()
    m_rbs_order_transfer = m_rbs_order_transfer.rename(
        columns={'Subsidiary Code': 'SUBSIDIARY_CD', 'Inner Code': 'INNER_CD'})
    m_rbs_order_transfer.loc[:, 'EFFECTIVE_DATE_FROM'] = ''
    m_rbs_order_transfer.loc[:, 'EFFECTIVE_DATE_TO'] = ''
    m_rbs_order_transfer.loc[:, 'TRANSFER_CHK_DAYS'] = ''
    m_rbs_order_transfer.loc[:, 'Process Mode'] = ''
    m_rbs_order_transfer.loc[:, 'Master ID'] = ''
    m_rbs_order_transfer = m_rbs_order_transfer.loc[:,
                           ['Process Mode', 'Master ID', 'SUBSIDIARY_CD', 'INNER_CD', 'EFFECTIVE_DATE_FROM',
                            'EFFECTIVE_DATE_TO', 'TRANSFER_CHK_DAYS']]

    # R.B.S商品別仕入先マスタ用dfの作成
    m_rbs_product_multi_supplier = rbs_product_master.loc[:, ['Subsidiary Code', 'Inner Code', 'Supplier Code']].copy()
    m_rbs_product_multi_supplier = m_rbs_product_multi_supplier.rename(
        columns={'Subsidiary Code': 'SUBSIDIARY_CD', 'Inner Code': 'INNER_CD', 'Supplier Code': 'SUPPLIER_CD'})
    m_rbs_product_multi_supplier.loc[:, 'MANAGED_UNIT_CD'] = managed_unit_cd_dict[pgname]
    m_rbs_product_multi_supplier.loc[:, 'RBS_FLG'] = '0'
    # 'SUBSIDIARY_CD', 'INNER_CD'の重複する行のみR.B.S_FLG=1
    m_rbs_product_multi_supplier.loc[
        m_rbs_product_multi_supplier.duplicated(subset=['SUBSIDIARY_CD', 'INNER_CD'], keep=False), 'RBS_FLG'] = '1'
    m_rbs_product_multi_supplier.loc[:, 'Process Mode'] = ''
    m_rbs_product_multi_supplier.loc[:, 'Master ID'] = ''
    m_rbs_product_multi_supplier = m_rbs_product_multi_supplier.loc[:,
                                   ['Process Mode', 'Master ID', 'SUBSIDIARY_CD', 'INNER_CD', 'SUPPLIER_CD',
                                    'MANAGED_UNIT_CD', 'RBS_FLG']]

    # 現法をインデックス化
    grp_rbs = rbs_product_master.set_index(
        ['Product Code', 'Inner Code', 'MC_PLANT_CD', 'Subsidiary Code', 'CLASSIFY_CD'], inplace=False)

    # 現法をマルチカラム化
    grp_rbs = grp_rbs.unstack('MC_PLANT_CD')
    grp_rbs = grp_rbs.unstack('Subsidiary Code')
    grp_rbs = grp_rbs.swaplevel(axis=1).sort_index(axis=1)
    grp_rbs.dropna(axis=1, how='all', inplace=True)

    # 商品別仕入先マスタのYY作成必要なリストを出力
    # 商品マスタから数量スライドを抽出
    product_master_slide = product_master_m.loc[:, ['Subsidiary Code',
                                                    'Inner Code',
                                                    'Slide Qty 1',
                                                    'Slide Qty 2',
                                                    'Slide Qty 3',
                                                    'Slide Qty 4',
                                                    'Slide Qty 5',
                                                    'Slide Qty 6',
                                                    'Slide Qty 7',
                                                    'Slide Qty 8',
                                                    'Slide Qty 9',
                                                    'Slide Qty 10']]
    # A調達は簡単なのでロジックで作成
    prod_mlt_supp = new_mlt.loc[:, ['Subsidiary Code', 'Product Code', 'Inner Code', 'Supplier Code']]
    prod_mlt_supp.loc[:, 'Process Mode'] = '4'
    prod_mlt_supp.loc[:, 'Master ID'] = '18'
    prod_mlt_supp.loc[:, 'MC/Plant Code'] = 'YY'
    prod_mlt_supp.loc[:, 'Express T Purchase Unit Price'] = '0'
    prod_mlt_supp.loc[:, 'Express A Purchase Unit Price'] = '0'
    prod_mlt_supp.loc[:, 'Plant Express A Purchase Unit Price'] = '0'
    prod_mlt_supp.loc[:, 'Express B Purchase Unit Price'] = '0'
    prod_mlt_supp.loc[:, 'Express C Purchase Unit Price'] = '0'
    prod_mlt_supp.loc[:, 'Production LT for Stock'] = '0'
    prod_mlt_supp.loc[:, 'Apply TI to Plant 1'] = '0'
    prod_mlt_supp.loc[:, 'Apply TI to Plant 2'] = '0'
    prod_mlt_supp.loc[:, 'Apply TI to Plant 3'] = '0'
    prod_mlt_supp.loc[:, 'Apply TI to Plant 4'] = '0'
    prod_mlt_supp.loc[:, 'Apply TI to Plant 5'] = '0'
    prod_mlt_supp.loc[:, 'SO Cancel Charge Rate'] = '0'
    prod_mlt_supp.loc[:, '1st Day After SO Cancel Charge Rate'] = '0'
    prod_mlt_supp.loc[:, '3rd Days After SO Cancel Charge Rate'] = '0'
    prod_mlt_supp.loc[:, 'Express A Direct Shipment Flg'] = '0'
    prod_mlt_supp.loc[:, 'Express B Direct Shipment Flg'] = '0'
    prod_mlt_supp.loc[:, 'Express C Direct Shipment Flg'] = '0'
    prod_mlt_supp.loc[:, 'Express T Direct Shipment Flg'] = '0'
    prod_mlt_supp.loc[:, 'Express T Production LT'] = '0'
    prod_mlt_supp.loc[:, 'Express A Production LT'] = '0'
    prod_mlt_supp.loc[:, 'Express B Production LT'] = '0'
    prod_mlt_supp.loc[:, 'Express C Production LT'] = '0'
    prod_mlt_supp.loc[((prod_mlt_supp['Supplier Code'] == 'ECAL') | (prod_mlt_supp['Supplier Code'] == 'FCNX') | (
                prod_mlt_supp['Supplier Code'] == 'AIOX') | (prod_mlt_supp['Supplier Code'] == 'FCNT') | (
                                  prod_mlt_supp['Supplier Code'] == 'AIOT')), 'Purchase Mode'] = 'A'
    prod_mlt_supp.loc[((prod_mlt_supp['Supplier Code'] == '7017') | (prod_mlt_supp['Supplier Code'] == '3764') | (
                prod_mlt_supp['Supplier Code'] == '0143') | (prod_mlt_supp['Supplier Code'] == 'SPCM') | (
                prod_mlt_supp['Supplier Code'] == '0FCN') | (prod_mlt_supp['Supplier Code'] == '0AIO')), 'Purchase Mode'] = 'B'
    prod_mlt_supp.loc[prod_mlt_supp['Purchase Mode'] == 'A', 'Production LT'] = '0'

    # 数量スライドの代入
    prod_mlt_supp = pd.merge(prod_mlt_supp, product_master_slide, on=['Subsidiary Code', 'Inner Code'], how='left')
    for slide in range(1,11):
        slide_qty = 'Slide Qty ' + str(slide)
        spsu = 'Slide Purchase Unit Price ' + str(slide)
        splt = 'Slide Production LT ' + str(slide)
        prod_mlt_supp.loc[((prod_mlt_supp['Purchase Mode'] == 'A') & (prod_mlt_supp[slide_qty].notnull())), spsu] = '0'
        prod_mlt_supp.loc[((prod_mlt_supp['Purchase Mode'] == 'A') & (prod_mlt_supp[slide_qty].notnull())), splt] = '0'
        prod_mlt_supp.drop([slide_qty], axis=1, inplace=True)

    # ファイルアウトプット
    f_name = pgname + '_grp_sub.tsv'
    grp_sub.to_csv(out_pass + f_name, sep='\t', encoding=font, index=True)
    f_name = pgname + '_grp_supp.tsv'
    grp_supp.to_csv(out_pass + f_name, sep='\t', encoding=font, index=True)
    f_name = pgname + '_grp_rbs.tsv'
    grp_rbs.to_csv(out_pass + f_name, sep='\t', encoding=font, index=True)

    # 現法毎にファイル出力
    sub_name = ['CHN', 'GRM', 'HKG', 'IND', 'JKT', 'KOR', 'MEX', 'MJP', 'MYS', 'SGP', 'THA', 'TIW', 'USA', 'VNM']
    for v in sub_name:
        sub_up1 = m_rbs_order_transfer[m_rbs_order_transfer['SUBSIDIARY_CD'] == v].copy()
        sub_up2 = m_rbs_product_multi_supplier[m_rbs_product_multi_supplier['SUBSIDIARY_CD'] == v].copy()
        prod_mlt_supp_a = prod_mlt_supp[((prod_mlt_supp['Subsidiary Code'] == v) & (prod_mlt_supp['Purchase Mode'] == 'A'))].copy()
        prod_mlt_supp_b = prod_mlt_supp[((prod_mlt_supp['Subsidiary Code'] == v) & (prod_mlt_supp['Purchase Mode'] == 'B'))].copy()
        if len(sub_up1) > 0:
            sub_up_name = v + '_m_rbs_order_transfer.txt'
            sub_up1.to_csv(out_pass + sub_up_name, sep='\t', encoding='utf_16', quotechar='"', line_terminator='\r\n', index=False)
        if len(sub_up2) > 0:
            sub_up_name = v + '_m_rbs_product_multi_supplier.txt'
            sub_up2.to_csv(out_pass + sub_up_name, sep='\t', encoding='utf_16', quotechar='"', line_terminator='\r\n', index=False)
        if len(prod_mlt_supp_a) > 0:
            prod_mlt_supp_a = prod_mlt_supp_header.append(prod_mlt_supp_a, sort=False)
            prod_mlt_supp_a_name = v + '_m_product_multi_supplier_A.txt'
            prod_mlt_supp_a.to_csv(out_pass + prod_mlt_supp_a_name, sep='\t', encoding='utf_16', quotechar='"', line_terminator='\r\n', index=False)
        if len(prod_mlt_supp_b) > 0:
            prod_mlt_supp_b = prod_mlt_supp_header.append(prod_mlt_supp_b, sort=False)
            prod_mlt_supp_b_name = v + '_m_product_multi_supplier_B.txt'
            prod_mlt_supp_b.to_csv(out_pass + prod_mlt_supp_b_name, sep='\t', encoding='utf_16', quotechar='"', line_terminator='\r\n', index=False)

    print('Finish!')


if __name__ == '__main__':
    rbs_master()
