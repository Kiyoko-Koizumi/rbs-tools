# Err flg
import pandas as pd
import numpy as np
import datetime

def SPC_P05_ProductMaster_Err():

    r_path = 'C:/temp/■Python_SPC_Master/'  # ★作業用ローカルフォルダ
    path = '//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/temp_data/'  # ★共通ファイル保存先
    print(datetime.datetime.now())
    # over_slide・sales(n)<sales(n+1)・purchase(n)<purchase(n+1)・slide1=(sales=0 and purchase>0) or (sales>0 and purchase=0)
    new_slide = (pd.read_csv(path + 'New_Slide.txt', sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    new_slide['new_slide_no'] = new_slide['new_slide_no'].astype(int)
    p_zetta = (pd.read_csv(path + 'Zetta_Product.txt', sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))   # 重量式エラーチェックのため

    h_order = ({'Subsidiary Code': 0, 'Product Code': 1, 'err': 2})

    # df Errデータ格納
    df = pd.DataFrame(new_slide.query('new_slide_no > 10'))  # Over_Slide_Check err_0
    df['err'] = '0'   # Over_slide
    df.drop_duplicates(subset=['Subsidiary Code', 'Product Code'], keep='first', inplace=True)
    df = df.loc[:, h_order]

    # df1 現法コードと商品コードでグループ化
    df1 = pd.DataFrame(new_slide)
    df1.drop_duplicates(subset=['Subsidiary Code', 'Product Code'], keep='first', inplace=True)
    df1 = df1.loc[:, ['Subsidiary Code', 'Product Code']]
    df1 = df1.reset_index(drop=True)
    n = len(df1)

    # Slide1 Sales=0 and Purchase>0 err_1
    df3 = pd.DataFrame(new_slide.rename(columns={'Slide Sales Pc/Unit ': 'sales', 'Slide Purchase Pc/Unit ': 'purchase', 'Unit Price Check': 'unit', 'Slide Qty ': 'qty'}))
    df3['sales'] = df3['sales'].astype(float)
    df3['purchase'] = df3['purchase'].astype(float)

    df3.loc[:, 'err'] = ''
    df3 = df3.query('new_slide_no == 1 and sales  == 0 and purchase >0')
    df3['err'] = '1'
    df = df.append(df3, sort=False)

    # Slide1 Sales>0 and Purchase=0 err_1
    df3 = df3.query('new_slide_no == 1 and sales  > 0 and purchase ==0')
    df3['err'] = '1'
    df = df.append(df3, sort=False)

    df.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'err'], keep='first', inplace=True)
    df = df.loc[:, h_order]
    df = df.reset_index(drop=True)

    # 単価チェック区分=0 sales=0 and purchase>0 err_2
    df3 = df3.query('unit == 0 and sales  == 0 and purchase >0')
    df3['err'] = '2'
    df = df.append(df3, sort=False)

    df.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'err'], keep='first', inplace=True)
    df = df.loc[:, h_order]
    df = df.reset_index(drop=True)

    # 重量式なし
    df3 = pd.DataFrame(p_zetta[p_zetta['型式'].isnull()]) # 重量式リストの「型式」空白を抽出
    df3['err'] = '3'
    df = df.append(df3, sort=False)
    df = df.loc[:, h_order]
    df = df.reset_index(drop=True)

    # Sales(n) < Sales(n+1) err_4
    df3 = df3[:0]
    m = max(new_slide['new_slide_no'])
    df2 = pd.DataFrame(new_slide[['Subsidiary Code', 'Product Code']])
    dfs = pd.DataFrame(new_slide[['Subsidiary Code', 'Product Code', 'new_slide_no', 'Slide Sales Pc/Unit ']])
    dfs = pd.DataFrame(dfs.set_index(['Subsidiary Code', 'Product Code', 'new_slide_no']).unstack(level=2))
    # dfs = dfs.fillna(0)
    dfscol = []
    for n in range(1, m + 1):
        dfscol.append('Slide Sales Pc/Unit ' + str(n))
    dfs.columns = dfscol
    for i in range(1, m):
        dfs.loc[:, 'Check' + str(i)] = 0
        dfs['Check' + str(i)] = np.float32(dfs['Slide Sales Pc/Unit ' + str(i+1)]) - np.float32(dfs['Slide Sales Pc/Unit ' + str(i)])
    df2 = pd.merge(df2, dfs, on=['Subsidiary Code', 'Product Code'])
    df2.loc[:, 'err'] = ''  # カラム追加

    for i in range(1, m):
        df3 = df3.append(df2[(df2['Check' + str(i)] > 0)], sort=False)
    df3['err'] = '4'
    df = df.append(df3[['Subsidiary Code', 'Product Code', 'err']])
    df.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'err'], keep='first', inplace=True) # 重複削除

    # Purchase(n) < Purchase(n+1) err_5
    df3 = df3[:0]
    m = max(new_slide['new_slide_no'])
    df2 = pd.DataFrame(new_slide[['Subsidiary Code', 'Product Code']])
    dfs = pd.DataFrame(new_slide[['Subsidiary Code', 'Product Code', 'new_slide_no', 'Slide Purchase Pc/Unit ']])
    dfs = pd.DataFrame(dfs.set_index(['Subsidiary Code', 'Product Code', 'new_slide_no']).unstack(level=2))
    # dfs = dfs.fillna(0)
    dfscol = []
    for n in range(1, m + 1):
        dfscol.append('Slide Purchase Pc/Unit ' + str(n))
    dfs.columns = dfscol
    for i in range(1, m):
        dfs.loc[:, 'Check' + str(i)] = 0
        dfs['Check' + str(i)] = np.float32(dfs['Slide Purchase Pc/Unit ' + str(i+1)]) - np.float32(dfs['Slide Purchase Pc/Unit ' + str(i)])
    df2 = pd.merge(df2, dfs, on=['Subsidiary Code', 'Product Code'])
    df2.loc[:, 'err'] = ''  # カラム追加

    for i in range(1, m):
        df3 = df3.append(df2[(df2['Check' + str(i)] > 0)], sort=False)
    df3['err'] = '5'
    df = df.append(df3[['Subsidiary Code', 'Product Code', 'err']])
    df.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'err'], keep='first', inplace=True)   # 重複削除

    # CatalogDays(n)＞CatalogDays(n+1) err_6
    df3 = df3[:0]
    m = max(new_slide['new_slide_no'])
    df2 = pd.DataFrame(new_slide[['Subsidiary Code', 'Product Code']])
    dfs = pd.DataFrame(new_slide[['Subsidiary Code', 'Product Code', 'new_slide_no', 'Slide Days TS ']])
    dfs['Slide Days TS '] = dfs['Slide Days TS '].astype(int)
    dfs = pd.DataFrame(dfs.set_index(['Subsidiary Code', 'Product Code', 'new_slide_no']).unstack(level=2))
    # dfs = dfs.fillna(0)
    dfscol = []
    for n in range(1, m + 1):
        dfscol.append('Slide Days TS ' + str(n))
    dfs.columns = dfscol
    for i in range(1, m):
        dfs.loc[:, 'Check' + str(i)] = 0
        dfs['Check' + str(i)] = (dfs['Slide Days TS ' + str(i)]) - (dfs['Slide Days TS ' + str(i + 1)])
    df2 = pd.merge(df2, dfs, on=['Subsidiary Code', 'Product Code'])
    df2.loc[:, 'err'] = ''  # カラム追加

    for i in range(1, m):
        df3 = df3.append(df2[(df2['Check' + str(i)] > 0)], sort=False)
    df3['err'] = '6'
    df = df.append(df3[['Subsidiary Code', 'Product Code', 'err']])
    df.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'err'], keep='first', inplace=True) # 重複削除

    # 中口数量に製作日数・カタログ納期が入っていない　err_7
    df3 = new_slide
    df3 = df3.rename(columns={'Slide Qty ': 'qty', 'Slide Days TS ': 'days_ts'})
    df3['min_order'] = df3['min_order'].astype(int)
    df3['max_order'] = df3['max_order'].astype(int)
    df3['qty'] = df3['qty'].astype(int)
    df3['days_ts'] = df3['days_ts'].astype(int)
    df3 = df3.query('max_order - min_order >0')
    df3 = df3.query('qty >= min_order and qty < max_order')
    df2 = df3[['Subsidiary Code', 'Product Code']]
    df3 = df3.groupby(['Subsidiary Code', 'Product Code']).days_ts.agg(['sum'])
    df2 = pd.DataFrame(pd.merge(df2, df3, on=('Subsidiary Code', 'Product Code'), how='inner'))
    df2['err'] = ''
    df2 = df2.query('sum == "0"').copy()
    df2.loc[:, 'err'] = '7'
    df = df.append(df2[['Subsidiary Code', 'Product Code', 'err']])

    # Product_Slide.txtにエラーフラグを追加
    p_zetta = (pd.read_csv(path + 'Product_Slide.txt', sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    dfs = pd.DataFrame(pd.crosstab([df['Product Code'], df['Subsidiary Code']], 'err_' + df['err']))    # err 0～7のクロス集計

    for i in range(0, 7):   # err_1～7のカラムチェック　無しはカラム名追加
        if 'err_' + str(i) in dfs.columns:
            print('err_' + str(i))
        else:
            dfs['err_' + str(i)] = ''

    dfs = dfs.sort_index(axis=1)    # カラム名並び替え

    p_err = pd.merge(p_zetta, dfs, on=('Subsidiary Code', 'Product Code'), how='left')
    p_err.to_csv(path + 'Product_Slide.txt', sep='\t', encoding='utf_16', index=False)  # 出力

    print('SPC_P05_ProductMaster_Err')
    print(datetime.datetime.now())

if __name__ == '__main__':
    SPC_P05_ProductMaster_Err()