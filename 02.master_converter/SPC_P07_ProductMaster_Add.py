# Product Master 出力　Product.txt　Product_Slide.txt
import pandas as pd
import numpy as np
import Header
import Type
import datetime
import openpyxl

def SPC_P07_ProductMaster_Add():

    print(datetime.datetime.now())
    path='//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/'

    p = (pd.read_csv(path + 'temp_data/Product.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    s = (pd.read_csv(path + 'temp_data/Product_Slide.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    h = (pd.read_csv(path + 'temp_data/h_Product.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))

    df = pd.DataFrame(s)
    dfe = pd.DataFrame()
    dfo = pd.DataFrame()
    dfp = pd.DataFrame()
    for i in range(0, 8):   # err除くためにfloatに変更
        df['err_' + str(i)] = df['err_' + str(i)].astype(float)

    dfe = df.query('err_0 != 1 and (err_1 == 1 or err_2 == 1 or err_3 == 1 or err_4 == 1 or err_5 == 1 or err_6 == 1 or err_7 == 1 or err_8 == 1)')    # err データ over除く
    dfo = df.query('err_0 == 1')    # over err データ
    df = df.query('err_0 != 1 and err_1 != 1 and err_2 != 1 and err_3 != 1 and err_4 != 1 and err_5 != 1 and err_6 != 1 and err_7 != 1 and err_8 !=1')  # errなし

    # Unit Price Check <> 0 and errなし　単価マスタ作成用に「non_err_Product.txt」出力
    dfn = pd.DataFrame(pd.merge(df, p, on=('Subsidiary Code', 'Product Code')))
    dfn = dfn.rename(columns={'Unit Price Check': 'unit_check'})
    dfn = dfn.query('unit_check != "0"')
    dfn = (dfn[['Subsidiary Code', 'Product Code', 'unit_check']])
    dfn.to_csv(path + 'temp_data/non_err_Product.txt', sep='\t', encoding='utf_16', index=False)

    col = list(df.columns)  # Product_Slideのカラム名
    col2 = list(Header.Header())    # Headerのカラム名
    col3 = (set(col) - set(col2))   # HeaderにはないProduct_Slideのカラム名　例：Slide Qty 11

    err_h = list(Header.Header())
    err_h[len(err_h):len(err_h)] = ('err_0', 'err_1', 'err_2', 'err_3', 'err_4', 'err_5', 'err_6', 'err_7', 'err_8', 'err_8_C')

    for col3 in col3:
        df.drop(columns=[col3], inplace=True)    # 不要な列を削除

    df1 = pd.DataFrame(pd.merge(p, df, on=('Subsidiary Code', 'Product Code'), how='inner'))
    df2 = pd.DataFrame([], columns=Header.Header())
    df2 = df2.append(df1, sort=False)

    dfe = pd.merge(p, dfe, on=('Subsidiary Code', 'Product Code'), how='inner')
    dfp = p[['Subsidiary Code', 'Product Code', 'Production LT', 'Min Qty of Big Order', 'Max Qty of Big Order']]    # Over_Listに項目追加

    # 現法毎にファイル出力
    sub = list(set(df2['Subsidiary Code'])) # 現法コードをリストにセット　重複除く

    df3 = pd.DataFrame()
    err = pd.DataFrame()
    over = pd.DataFrame()
    overp = pd.DataFrame()

    for i in range(0, len(sub)):
        df3 = df3[:0]
        err = err[:0]
        over = over[:0]
        overp = overp[:0]
        df3 = df3.append(h, sort=False) # h_Product.txt Header XXX 追加
        df3 = df3.append(df2.loc[df2['Subsidiary Code'] == sub[i]], sort=False)
        df3 = df3.loc[:, col2]   # カラム並べ替え Header()でなぜかできないので・・・listを指定したらできた！！
        df3.to_csv(path + 'Update_txt/' + sub[i] + '_Product.txt', sep='\t', encoding='utf_16', index=False)  # Product Master 現法毎に出力　フォルダ「Update_txt」

        df3 = df3.astype(Type.type())   # 検証用
        df3 = df3.replace('nan', '')
        df3.to_excel(path + 'Update_txt/' + sub[i] + '_Product.xlsx', na_rep='', index=False)  # 検証用
        print(sub[i])

        if len(dfe.loc[dfe['Subsidiary Code'] == sub[i]]) > 0:  # err_listを現法毎にExcelに出力 フォルダ「Err_Excel」
            err = err.append(h, sort=False)
            err = err.append(dfe.loc[dfe['Subsidiary Code'] == sub[i]], sort=False)
            err = err.astype(Type.type())
            err = err.replace('nan', '')    # 文字列の「nan」を空白に置き換え ★mergeやqueryを使うと文字列のnanになることがある
            #err = err.replace(np.nan, '', regex=True)
            err = err.reindex(columns=err_h)

            writer = pd.ExcelWriter(path + 'Err_Excel/' + sub[i] + '_err_Product.xlsx', engine='xlsxwriter')
            err.to_excel(writer, sheet_name='Err_List', na_rep='', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Err_List']
            # フォーマットの設定　ヘッダが勝手に太字＆罫線になるので設定変更
            fmt = workbook.add_format({'bold': False, 'border': 0})
            # カラム名のフォーマット
            [worksheet.write(0, col_num, col_value, fmt) for col_num, col_value in enumerate(err.columns.values, 0)]
            writer.save()

        if len(dfo.loc[dfo['Subsidiary Code'] == sub[i]]) > 0:  # over_listを現法毎にExcelに出力
            over = over.append(dfo.loc[dfo['Subsidiary Code'] == sub[i]], sort=False)  # Over_Listシート
            over = pd.merge(dfp, dfo, on=['Subsidiary Code', 'Product Code'], how='inner')
            over = over.drop(['err_0', 'err_1', 'err_2', 'err_3', 'err_4', 'err_5', 'err_6', 'err_7', 'err_8', 'err_8_C'], axis=1)

            for f in range(2, len(over.columns)):   # Over_Listの型変更　現法コード・商品コード以外をfloat
                over[over.columns[f]] = over[over.columns[f]].astype(float)
            dfo = pd.merge(p, dfo, on=('Subsidiary Code', 'Product Code'), how='inner')  # Productシート
            overp = overp.append(h, sort=False)
            overp = overp.append(dfo.loc[dfo['Subsidiary Code'] == sub[i]], sort=False)
            overp = overp.reindex(columns=err_h)
            overp = overp.astype(Type.type())
            overp = overp.replace('nan', '')    # 文字列の「nan」を空白に置き換え ★mergeやqueryを使うと文字列のnanになることがある

            with pd.ExcelWriter(path + 'Err_Excel/' + sub[i] + '_over_Product.xlsx') as writer:
                over.to_excel(writer, sheet_name='Over_List', index=False)
                overp.to_excel(writer, sheet_name='Product', index=False)

                workbook = writer.book
                fmt = workbook.add_format({'bold': False, 'border': 0})
                worksheet = writer.sheets['Over_List']
                [worksheet.write(0, col_num, col_value, fmt) for col_num, col_value in enumerate(over.columns.values, 0)]

                worksheet = writer.sheets['Product']
                [worksheet.write(0, col_num, col_value, fmt) for col_num, col_value in enumerate(overp.columns.values, 0)]
    print('SPC_P07_ProductMaster_Add')
    print(datetime.datetime.now())

if __name__ == '__main__':
    SPC_P07_ProductMaster_Add()