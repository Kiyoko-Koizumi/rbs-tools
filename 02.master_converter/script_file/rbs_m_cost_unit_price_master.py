# coding: utf-8
# 新規作成　2019/10/10

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
                print(f_pass + '/' + f_name + 'にダブルコーテーションが含まれるため置き換えて上書き保存します')
                f_name_row = 'row_' + f_name
                st = open(f_pass + '/' + f_name_row, 'w', encoding=font)
                st.write(file)
                st.close()
                file = file.replace('"', '')
                # st = open(f_pass + '/' + f_name, 'w', encoding=font)
                f.write(file)


def read_data(title, font):
    # ファイル選択ダイアログの表示
    root = tkinter.Tk()
    root.withdraw()
    fTyp = [("", "*")]
    iDir = '../RBS_M_COST_Master/product_and_mlt_master/input/'

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


def rbs_m_cost_master():
    csv.field_size_limit(1000000000)

    # スクリプトのあるディレクトリの絶対パスを取得
    script_pass = os.path.dirname(os.path.abspath(__name__))
    local_pass = script_pass + '/'
    out_pass = '../RBS_M_COST_Master/unit_price_master/output/'

    font = 'utf-8'

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

    # 必要なカラムだけにする
    if data_s == 'zetta':
        # XXX行を除く
        product_master = product_master_m[product_master_m['Subsidiary Code'] != 'XXX']
        product_mlt = product_mlt_m[product_mlt_m['Subsidiary Code'] != 'XXX']

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

    # RBS_MCOST商品別仕入先数量スライドマスタに必要なカラムのみにする
    product_master = product_master.iloc[:, [0, 1, 2, 3, 4, 89, 13, 18, 23, 28, 33, 38, 43, 48, 53, 58]]
    product_mlt = product_mlt.iloc[:, [0, 1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]]

    # 商品マスタと商品別仕入先マスタのカラム名をM_COSTに合わせる
    for slide in range(1, 11):
        product_master_column = 'Slide Purchase Pc/Unit ' + str(slide)
        product_mlt_column = 'Slide Purchase Unit Price ' + str(slide)
        product_m_cost_master_column = 'Slide Manufacturing Cost ' + str(slide)
        product_master = product_master.rename(columns={product_master_column: product_m_cost_master_column})
        product_master = product_master.rename(columns={product_mlt_column: product_m_cost_master_column})

    # 商品マスタと商品別仕入先マスタを結合する
    product_m_cost_master = product_master.append(product_mlt, sort=False)

    # 仕入先コードを限定
    # 指定のグループによってR.B.S対象サプライヤを選択する
    if pgname == 'LS':
        product_m_cost_master = product_m_cost_master[(product_m_cost_master['Supplier Code'] == '7017') |
                                                      (product_m_cost_master['Supplier Code'] == '3764') |
                                                      (product_m_cost_master['Supplier Code'] == 'ECAL') |
                                                      (product_m_cost_master['Supplier Code'] == 'FCNX') |
                                                      (product_m_cost_master['Supplier Code'] == '0FCN') |
                                                      (product_m_cost_master['Supplier Code'] == 'SPCM')]
    elif pgname == 'LP' or pgname == 'TP':
        product_m_cost_master = product_m_cost_master[(product_m_cost_master['Supplier Code'] == '0143') | (
                product_m_cost_master['Supplier Code'] == '0AIO') | (product_m_cost_master['Supplier Code'] == 'SPCM')]

    # スライド製造原価通貨コードを入れる
    product_m_cost_master.loc[((product_m_cost_master['Supplier Code'] == 'ECAL') |
                               (product_m_cost_master['Supplier Code'] == '7017') |
                               (product_m_cost_master['Supplier Code'] == '3764') |
                               (product_m_cost_master['Supplier Code'] == '0143')), 'スライド製造原価通貨コード'] = 'JPY'
    product_m_cost_master.loc[((product_m_cost_master['Supplier Code'] == '0FCN') |
                               (product_m_cost_master['Supplier Code'] == '0AIO') |
                               (product_m_cost_master['Supplier Code'] == '0TYO') |
                               (product_m_cost_master['Supplier Code'] == 'FCNX') |
                               (product_m_cost_master['Supplier Code'] == 'AIOX') |
                               (product_m_cost_master['Supplier Code'] == 'TYOX') |
                               (product_m_cost_master['Supplier Code'] == 'FCNT') |
                               (product_m_cost_master['Supplier Code'] == 'AIOT') |
                               (product_m_cost_master['Supplier Code'] == 'TYOT')), 'スライド製造原価通貨コード'] = 'RMB'
    product_m_cost_master.loc[((product_m_cost_master['Supplier Code'] == 'SPCM')), 'スライド製造原価通貨コード'] = 'USD'

    # PKで重複削除
    product_m_cost_master.drop_duplicates(subset=['Subsidiary Code', 'Inner Code', 'Product Code', 'Supplier Code'], keep='first', inplace=True)

    # R.B.S対象インナーコードの限定
    # 数量スライド毎の原価の入れ替え

    # 現法毎にファイル出力
    sub_name = ['CHN', 'GRM', 'HKG', 'IND', 'JKT', 'KOR', 'MEX', 'MJP', 'MYS', 'SGP', 'THA', 'TIW', 'USA', 'VNM']
    for v in sub_name:
        sub_up = product_m_cost_master[product_m_cost_master['Subsidiary Code'] == v].copy()
        if len(sub_up) > 0:
            sub_up_name = v + '_rbs_product_multi_supp_slide_m_cost_master.txt'
            sub_up.to_csv(out_pass + sub_up_name, sep='\t', encoding='utf_16', quotechar='"', line_terminator='\r\n', index=False)

    print('Finish!')


if __name__ == '__main__':
    rbs_m_cost_master()
