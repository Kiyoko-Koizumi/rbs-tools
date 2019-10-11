# Err flg
import pandas as pd
import numpy as np
import datetime

def SPC_U03_Master_Err():

    path = '//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/temp_data/'
    print(datetime.datetime.now())

    new_slide = pd.DataFrame(pd.read_csv(path + 'New_Unit_Slide.txt', sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    new_slide['new_slide_no'] = new_slide['new_slide_no'].astype(int)
    h_order = ({'Subsidiary Code': 0, 'Product Code': 1, 'err': 2})

    df = pd.DataFrame(new_slide[['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'sales', 'purchase']])
    df['Min.Val.1'] = df['Min.Val.1'].astype(float)
    df['sales'] = df['sales'].astype(float)
    df['purchase'] = df['purchase'].astype(float)
    df.loc[:, 'err'] = ''
    dfe = pd.DataFrame()
    df3 = pd.DataFrame()

    # Slide1 Sales=0 and Purchase>0 err_1
    df0 = pd.DataFrame(df.query('sales == 0 and purchase > 0'))
    df0.loc[:, 'err'] = '1'
    dfe = dfe.append(df0, sort=False)

    # Slide1 Sales>0 and Purchase=0 err_1
    df0 = pd.DataFrame(df.query('sales > 0 and purchase == 0'))
    df0.loc[:, 'err'] = '1'
    dfe = dfe.append(df0, sort=False)
    dfe.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'err'], keep='first', inplace=True)
    dfe = dfe.loc[:, h_order]
    dfe = dfe.reset_index(drop=True)

    # Sales(n) < Sales(n+1) err_2
    m = max(new_slide['new_slide_no'])
    df2 = pd.DataFrame(new_slide[['Subsidiary Code', 'Product Code', 'Min.Val.1']])
    dfs = pd.DataFrame(new_slide[['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'sales']])
    dfs = pd.DataFrame(dfs.set_index(['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1']).unstack(level=2))

    dfscol = []
    for n in range(1, m + 1):
        dfscol.append('sales' + str(n))
    dfs.columns = dfscol
    for i in range(1, m):
        dfs.loc[:, 'Check' + str(i)] = 0
        dfs['Check' + str(i)] = np.float32(dfs['sales' + str(i+1)]) - np.float32(dfs['sales' + str(i)])
    df2 = pd.merge(df2, dfs, on=['Subsidiary Code', 'Product Code'])
    df2.loc[:, 'err'] = ''  # カラム追加

    for i in range(1, m):
        df3 = pd.DataFrame(df3.append(df2[(df2['Check' + str(i)] > 0)], sort=False))
    df3['err'] = '2'
    dfe = dfe.append(df3[['Subsidiary Code', 'Product Code', 'err']])
    dfe.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'err'], keep='first', inplace=True) # 重複削除

    # Purchase(n) < Purchase(n+1) err_3
    df3 = df3[:0]
    m = max(new_slide['new_slide_no'])
    df2 = pd.DataFrame(new_slide[['Subsidiary Code', 'Product Code', 'Min.Val.1']])
    dfs = pd.DataFrame(new_slide[['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'purchase']])
    dfs = pd.DataFrame(dfs.set_index(['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1']).unstack(level=2))

    dfscol = []
    for n in range(1, m + 1):
        dfscol.append('purchase' + str(n))
    dfs.columns = dfscol
    for i in range(1, m):
        dfs.loc[:, 'Check' + str(i)] = 0
        dfs['Check' + str(i)] = np.float32(dfs['purchase' + str(i+1)]) - np.float32(dfs['purchase' + str(i)])
    df2 = pd.merge(df2, dfs, on=['Subsidiary Code', 'Product Code'])
    df2.loc[:, 'err'] = ''  # カラム追加

    for i in range(1, m):
        df3 = pd.DataFrame(df3.append(df2[(df2['Check' + str(i)] > 0)], sort=False))
    df3['err'] = '3'
    dfe = dfe.append(df3[['Subsidiary Code', 'Product Code', 'err']])
    dfe.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'err'], keep='first', inplace=True) # 重複削除

    # errがあれば、横展開
    dferr = pd.DataFrame()
    if len(dfe) > 0:
        dferr = pd.DataFrame(pd.crosstab([dfe['Subsidiary Code'], dfe['Product Code']], 'err_' + dfe['err']))
        for i in range(1, 4):
            if 'err_' + str(i) in dferr.columns:
                print('err_' + str(i))
            else:
                dferr['err_' + str(i)] = ''

    # New_Unit_Slideのsales/purchaseをマスタ名称に変更
    new_slide = (new_slide.rename(columns={'sales': 'Slide Sales Unit Price ', 'purchase': 'Slide Purchase Unit Price '}))

    # 各カラムを横に展開
    new_slide['new_slide_no'] = new_slide['new_slide_no'].astype(int)
    col = ({'Slide Sales Unit Price ', 'Slide Purchase Unit Price '})

    dfz = pd.DataFrame(new_slide[['Subsidiary Code', 'Product Code', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5']])
    dfz.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'], keep='first', inplace=True) # 重複削除

    for col in col:
        dfs = pd.DataFrame(new_slide[['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5', col]])
        dfs = dfs.set_index(['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5']).unstack(level=2)
        dfscol = []
        for n in range(1, 11):
            dfscol.append(col+str(n))
        dfs.columns = dfscol
        dfz = pd.DataFrame(pd.merge(dfz, dfs, on=['Subsidiary Code', 'Product Code', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5']))

    # ヘッダ並び順作成
    p_order = ['Subsidiary Code', 'Product Code', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5']
    for n in range(1, 11):
        col = ['Slide Sales Unit Price ', 'Slide Purchase Unit Price ']
        for col in col:
            p_order.append(col + str(n))
    dfz = dfz.reindex(columns=p_order)

    # errがあれば、横展開したスライドデータに追加
    if len(dferr) > 0:
        dfz = pd.merge(dfz, dferr, on=('Subsidiary Code', 'Product Code'), how='left')

    dfz.to_csv(path + 'Unit_Price_Product_Slide.txt', sep='\t', encoding='utf_16', index=False)  # 出力

    print(datetime.datetime.now())
    print('fin')

if __name__ == '__main__':
    SPC_U03_Master_Err()

