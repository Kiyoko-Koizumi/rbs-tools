# ZettaとSPCそれぞれ参照項目の設定
import pandas as pd
import numpy as np
import Header_U
import Type_U
import datetime

def SPC_U04_MasterMerge_Add():

    print(datetime.datetime.now())
    path='//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/'

    z_p = (pd.read_csv(path + 'temp_data/Zetta_U_Product.txt', sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    s_p = (pd.read_csv(path + 'temp_data/SPC_U_Product.txt', sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    u_s = (pd.read_csv(path + 'temp_data/Unit_Price_Product_Slide.txt', sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    h = (pd.read_csv(path + 'temp_data/h_U_Product.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    df = pd.DataFrame(pd.merge(z_p, s_p, on='Product Code', suffixes=['_z', '_s'], how='left'))

    # カラム名末尾「_z」=Zetta　「_s」=Spc
    dfs = pd.DataFrame()
    dfs['Process Mode'] = df['Process Mode_s']   # 処理区分　z/sどちらでも良い
    dfs['Master ID'] = df['Master ID_s']  # 登録区分　z/sどちらでも良い
    dfs['Subsidiary Code'] = df['Subsidiary Code_z']  # 現法コード
    dfs['Inner Code'] = df['Inner Code_z']  # インナーコード
    dfs['Product Code'] = df['Product Code']  # 商品コード
    dfs['Purchase Unit Price Currency Code '] = 'USD'   # 仕入単価通貨コード
    dfs['Supplier Code'] = ''   # 仕入先コード
    dfs['Cost Ratio'] = df['Cost Ratio_z']  # 仕入掛け率
    dfs['Plate Flag'] = df['Plate Flag_s']    # プレート区分
    dfs['Position 1'] = df['Position 1_z']  # パラメータ位置１
    dfs['Position 2'] = df['Position 2_z']  # パラメータ位置２
    dfs['Position 3'] = df['Position 3_z']  # パラメータ位置３
    dfs['Position 4'] = df['Position 4_z']  # パラメータ位置４
    dfs['Position 5'] = df['Position 5_z']  # パラメータ位置５
    dfs['Rounding Place'] = df['Rounding Place_s']  # 計算単位
    dfs['Rounding Method'] = df['Rounding Method_s']  # 丸め

    dfs.drop_duplicates(subset=['Subsidiary Code', 'Product Code'], keep='first', inplace=True)

    # slideデータと結合
    df = pd.DataFrame(pd.merge(dfs, u_s, on=('Subsidiary Code', 'Product Code')))

    col2 = list(Header_U.Header())    # Headerのカラム名
    err_h = list(Header_U.Header())
    err_h[len(err_h):len(err_h)] = ('err_1', 'err_2', 'err_3')

    # 現法毎にファイル出力
    sub = list(set(dfs['Subsidiary Code'])) # 現法コードをリストにセット　重複除く

    # errカラムがあるか調べる
    err_col = ['err_1', 'err_2', 'err_3']
    u_data = pd.DataFrame()
    e_data = pd.DataFrame()
    # errカラムがあれば、err分はExcel・err無しはtxtへ出力　errカラムがなければ全てtxtへ
    if (len((set(df.columns) & set(err_col)))) == 3:
        for i in range(1, 4):  # err除くためにfloatに変更
            df['err_' + str(i)] = df['err_' + str(i)].astype(float)
        u_data = pd.DataFrame(df.query('err_1 != 1 and err_2 != 1 and err_3 != 1'))  # errなしデータ
        e_data = pd.DataFrame(df.query('err_1 == 1 or err_2 == 1 or err_3 == 1'))  # errありデータ
    else:
        u_data = pd.DataFrame(df)
    print(len(e_data))
    # 現法毎に出力
    dfu = pd.DataFrame()
    dfe = pd.DataFrame()
    for i in range(0, len(sub)):
        dfu = dfu[:0]
        dfu = dfu.append(h, sort=False) # h_Product.txt Header XXX 追加
        dfu = dfu.append(u_data.loc[u_data['Subsidiary Code'] == sub[i]], sort=False)
        dfu = dfu.loc[:, col2]   # カラム並べ替え Header()でなぜかできないので・・・listを指定したらできた！！
        dfu.to_csv(path + 'Update_txt/' + sub[i] + '_U_Product.txt', sep='\t', encoding='utf_16', index=False)  # Product Master 現法毎に出力　フォルダ「Update_txt」

        dfu = dfu.astype(Type_U.type())   # 検証用
        dfu = dfu.replace('nan', '')
        dfu.to_excel(path + 'Update_txt/' + sub[i] + '_U_Product.xlsx', na_rep='', index=False)  # 検証用
        print(sub[i])
        if len(e_data) == 0:
            print('err_non')
        else:
            if len(e_data.loc[e_data['Subsidiary Code'] == sub[i]]) > 0:  # err_listを現法毎にExcelに出力 フォルダ「Err_Excel」
                dfe = dfe[:0]
                dfe = dfe.append(h, sort=False)
                dfe = dfe.append(e_data.loc[e_data['Subsidiary Code'] == sub[i]], sort=False)
                dfe = dfe.astype(Type_U.type())
                dfe = dfe.replace('nan', '')    # 文字列の「nan」を空白に置き換え ★mergeやqueryを使うと文字列のnanになることがある
                dfe = dfe.reindex(columns=err_h)

                writer = pd.ExcelWriter(path + 'Err_Excel/' + sub[i] + '_err_U_Product.xlsx', engine='xlsxwriter')
                dfe.to_excel(writer, sheet_name='Err_List', na_rep='', index=False)
                workbook = writer.book
                worksheet = writer.sheets['Err_List']
                # フォーマットの設定　ヘッダが勝手に太字＆罫線になるので設定変更
                fmt = workbook.add_format({'bold': False, 'border': 0})
                # カラム名のフォーマット
                [worksheet.write(0, col_num, col_value, fmt) for col_num, col_value in enumerate(dfe.columns.values, 0)]
                writer.save()

    print(datetime.datetime.now())
    print('fin')

if __name__ == '__main__':
    SPC_U04_MasterMerge_Add()