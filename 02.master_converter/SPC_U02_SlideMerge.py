# New Slideデータ作成
import pandas as pd
import numpy as np
import datetime

def SPC_U02_SlideMerge():
    path = '//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/temp_data/'
    print(datetime.datetime.now())
    # zetta_slide=02_Zetta_Slide.py　spc_slide=03_SPC_Slide.py
    zetta_slide = (pd.read_csv(path + 'Zetta_U_Slide.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    spc_slide = (pd.read_csv(path + 'SPC_U_Slide.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    slide_marge = pd.DataFrame()

    # ■Step1 ZettaとSPCのMin.ValをMarge
    h_order=({'Subsidiary Code': 0, 'Product Code': 1, 'new_slide_no': 2, 'Min.Val.1': 3, 'Min.Val.2': 4,
              'Min.Val.3': 5, 'Min.Val.4': 6, 'Min.Val.5': 7, 'sales': 8, 'purchase': 9})  # Header並び順
    df = pd.DataFrame(columns=h_order)
    z = (zetta_slide[['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5']])
    s = (spc_slide[['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5']])
    df = df.append([z, s], sort=False)
    df.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3',
                               'Min.Val.4', 'Min.Val.5'], keep='first', inplace=True)     # 念のため、重複削除

    df = pd.merge(df, zetta_slide, on=('Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1'), how='left')
    df = pd.merge(df, spc_slide, on=('Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1'), how='left')
    df.drop(columns=['Min.Val.2_y', 'Min.Val.3_y', 'Min.Val.4_y', 'Min.Val.5_y', 'sales_x', 'purchase_x',
                     'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'], inplace=True)    # 不要な列を削除
    df = df.rename(columns={'Min.Val.2_x': 'Min.Val.2', 'Min.Val.3_x': 'Min.Val.3', 'Min.Val.4_x': 'Min.Val.4',
                            'Min.Val.5_x': 'Min.Val.5', 'sales_y': 'sales', 'purchase_y': 'purchase'})   # カラム名変更

    df = df.reindex(columns=h_order)
    df = df.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1'], ascending=True)  # 並べ替え
    #df = df.replace(np.nan, 0, regex=True)  # 空白を0に置き換え
    df['sales'] = df['sales'].astype(float)
    df['purchase'] = df['purchase'].astype(float)

    dfs = pd.DataFrame(df[['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5']])
    dfs = dfs.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1', 'new_slide_no'], ascending=True)

    # 現法コード・商品コード以外をfloat mergeのため型を合わせる
    for f in range(2, len(dfs.columns)):
        dfs[dfs.columns[f]] = dfs[dfs.columns[f]].astype(float)

    # ■Step2　sales空白を埋める　上から下に（例：minval 18がNullのとき、minval 16 のsalse
    nn = pd.DataFrame()
    yes = pd.DataFrame()

    #nn = df.loc[df['sales'] == 0]
    #yes = df.loc[df['sales'] > 0]

    nn = df.loc[df['sales'].isnull()]
    yes = df.loc[df['sales'].notnull()]

    z = pd.DataFrame(pd.merge(nn, yes, on=('Subsidiary Code', 'Product Code', 'new_slide_no'), suffixes=['_n', '_y'], how='inner'))  # 空白データと空白無しデータを結合

    z['Min.Val.1_n'] = z['Min.Val.1_n'].astype(float)
    z['Min.Val.1_y'] = z['Min.Val.1_y'].astype(float)
    z['sa'] = z['Min.Val.1_y'] - z['Min.Val.1_n']  # 空白データのMin.Val.1と空白無しデータのMin.Val.1の差を算出
    z['sa'] = z['sa'].astype(float)
    z['new_slide_no'] = z['new_slide_no'].astype(int)
    z.drop(z.index[z.sa > 0], inplace=True)    # 差が0より大きいものは削除
    z.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1_n'], keep='first', inplace=True)  # 念のため、重複削除

    z.drop(columns=['Min.Val.1_y', 'Min.Val.2_y', 'Min.Val.3_y','Min.Val.4_y', 'Min.Val.5_y', 'sales_n', 'purchase_n', 'sa'], inplace=True)    # 不要な列を削除
    # sales_y = sales
    z = z.rename(columns={'Min.Val.1_n': 'Min.Val.1', 'Min.Val.2_n': 'Min.Val.2', 'Min.Val.3_n': 'Min.Val.3',
                          'Min.Val.4_n': 'Min.Val.4', 'Min.Val.5_n': 'Min.Val.5', 'sales_y': 'sales', 'purchase_y': 'purchase'})   # カラム名変更
    zz = pd.DataFrame(pd.concat([z, yes], sort=True, copy=True))

    zz.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'], keep='first', inplace=True)
    zz = zz.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1', 'new_slide_no'], ascending=True)

    zz = zz.reindex(columns=h_order)
    zz = zz.drop(columns=['purchase'])
    zz.reset_index(drop=True, inplace=True)

    # 現法コード・商品コード以外をfloat mergeのため型を合わせる
    for f in range(2, len(zz.columns)):
        zz[zz.columns[f]] = zz[zz.columns[f]].astype(float)

    dfs = pd.merge(dfs, zz, on=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'], how='left')

    # ■Step3　purchase空白を埋める 上から下に（例：minval 18がNullのとき、minval 16 のpurchase
    #nn = df.loc[df['purchase'] == 0]
    #yes = df.loc[df['purchase'] > 0]

    nn = df.loc[df['purchase'].isnull()]
    yes = df.loc[df['purchase'].notnull()]

    s = pd.DataFrame(pd.merge(nn, yes, on=('Subsidiary Code', 'Product Code', 'new_slide_no'), suffixes=['_n', '_y'], how='inner'))  # 空白データと空白無しデータを結合

    s['Min.Val.1_n'] = s['Min.Val.1_n'].astype(float)
    s['Min.Val.1_y'] = s['Min.Val.1_y'].astype(float)
    s['sa'] = s['Min.Val.1_y'] - s['Min.Val.1_n']  # 空白データのMin.Val.1と空白無しデータのMin.Val.1の差を算出
    s['sa'] = s['sa'].astype(float)
    s['new_slide_no'] = s['new_slide_no'].astype(int)
    s.drop(s.index[s.sa > 0], inplace=True)    # 差が0より大きいものは削除

    s.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1_n'], keep='first', inplace=True)    # 念のため、重複削除
    # purchase_y = purchase
    s = s.rename(columns={'Min.Val.1_n': 'Min.Val.1', 'Min.Val.2_n': 'Min.Val.2', 'Min.Val.3_n': 'Min.Val.3',
                          'Min.Val.4_n': 'Min.Val.4', 'Min.Val.5_n': 'Min.Val.5', 'purchase_y': 'purchase'})   # カラム名変更

    ss = pd.DataFrame(pd.concat([s, yes], sort=True))

    ss = ss.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1', 'new_slide_no'], ascending=True)
    ss.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'], keep='first', inplace=True)

    ss = ss.reindex(columns=h_order)
    ss = ss.drop(columns=['sales'])
    ss.reset_index(drop=True, inplace=True)

    # 現法コード・商品コード以外をfloat mergeのため型を合わせる
    for f in range(2, len(ss.columns)):
        ss[ss.columns[f]] = ss[ss.columns[f]].astype(float)

    dfs = pd.merge(dfs, ss, on=('Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'), how='left')
    #dfs = dfs.replace(np.nan, 0, regex=True)  # 空白を0に置き換え

    # データフレームを空にする
    zz[:0]
    ss[:0]
    nn[:0]
    yes[:0]

    # ■Step4　sales/purchase空白を埋める 下から上に（例：minval 16がNullのとき、minval 18 のsales/purchase
    #nn = dfs.loc[dfs['sales'] == 0]
    #yes = dfs.loc[dfs['sales'] > 0]

    nn = dfs.loc[dfs['sales'].isnull()]
    yes = dfs.loc[dfs['sales'].notnull()]

    if len(nn) > 0:
        z = pd.DataFrame(pd.merge(nn, yes, on=('Subsidiary Code', 'Product Code', 'new_slide_no'), suffixes=['_n', '_y'], how='inner'))  # 空白データと空白無しデータを結合
        z = z.drop(columns=['purchase_n', 'purchase_y'])
        z['Min.Val.1_n'] = z['Min.Val.1_n'].astype(float)
        z['Min.Val.1_y'] = z['Min.Val.1_y'].astype(float)
        z['sa'] = z['Min.Val.1_y'] - z['Min.Val.1_n']  # 空白データのMin.Val.1と空白無しデータのMin.Val.1の差を算出
        z['sa'] = z['sa'].astype(float)
        z['new_slide_no'] = z['new_slide_no'].astype(int)
        z = z.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1_n', 'new_slide_no', 'sa'], ascending=True)  # 差を昇順に並び替え
        z.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1_n'], keep='first', inplace=True)  # 念のため、重複削除
        # sales_y = sales
        z = z.rename(columns={'Min.Val.1_n': 'Min.Val.1', 'Min.Val.2_n': 'Min.Val.2', 'Min.Val.3_n': 'Min.Val.3',
                              'Min.Val.4_n': 'Min.Val.4', 'Min.Val.5_n': 'Min.Val.5', 'sales_y': 'sales'})   # カラム名変更

        zz = pd.DataFrame(pd.concat([z, yes], sort=True))
        zz = zz.drop(columns=['Min.Val.1_y', 'Min.Val.2_y', 'Min.Val.3_y', 'Min.Val.4_y', 'Min.Val.5_y', 'sales_n', 'purchase', 'sa'])
        zz.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'], keep='first', inplace=True)

    else:
        zz = pd.DataFrame(dfs[['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5', 'sales']])

    zz = zz.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1', 'new_slide_no'], ascending=True)
    zz.reset_index(drop=True, inplace=True)
    zz = zz.reindex(columns=h_order)
    zz = zz.drop(columns=['purchase'])

    nn[:0]
    yes[:0]
    #nn = dfs.loc[dfs['purchase'] == 0]
    #yes = dfs.loc[dfs['purchase'] > 0]

    nn = dfs.loc[dfs['purchase'].isnull()]
    yes = dfs.loc[dfs['purchase'].notnull()]

    if len(nn) > 0:
        s = pd.DataFrame(pd.merge(nn, yes, on=('Subsidiary Code', 'Product Code', 'new_slide_no'), suffixes=['_n', '_y'], how='inner'))  # 空白データと空白無しデータを結合
        s = s.drop(columns=['sales_n', 'sales_y'])
        s['Min.Val.1_n'] = s['Min.Val.1_n'].astype(float)
        s['Min.Val.1_y'] = s['Min.Val.1_y'].astype(float)
        s['sa'] = s['Min.Val.1_y'] - s['Min.Val.1_n']  # 空白データのMin.Val.1と空白無しデータのMin.Val.1の差を算出
        s['sa'] = s['sa'].astype(float)
        s['new_slide_no'] = s['new_slide_no'].astype(int)
        s = s.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1_n', 'new_slide_no', 'sa'], ascending=True)  # 差を昇順に並び替え
        s.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1_n'], keep='first', inplace=True)  # 念のため、重複削除
        # purchase_y = purchase
        s = s.rename(columns={'Min.Val.1_n': 'Min.Val.1', 'Min.Val.2_n': 'Min.Val.2', 'Min.Val.3_n': 'Min.Val.3',
                              'Min.Val.4_n': 'Min.Val.4', 'Min.Val.5_n': 'Min.Val.5', 'purchase_y': 'purchase'})   # カラム名変更

        ss = pd.DataFrame(pd.concat([s, yes], sort=True))
        ss = ss.drop(columns=['Min.Val.1_y', 'Min.Val.2_y', 'Min.Val.3_y', 'Min.Val.4_y', 'Min.Val.5_y', 'purchase_n', 'sales', 'sa'])
        ss.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'], keep='first', inplace=True)

    else:
        ss = pd.DataFrame(dfs[['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5', 'purchase']])

    ss = ss.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1', 'new_slide_no'], ascending=True)
    ss.reset_index(drop=True, inplace=True)
    ss = ss.reindex(columns=h_order)
    ss = ss.drop(columns=['sales'])

    df = pd.merge(zz, ss, on=('Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'))
    #df = df.replace(np.nan, 0, regex=True)  # 空白を0に置き換え
    df['new_slide_no'] = df['new_slide_no'].astype(int)
    df.to_csv(path + 'New_Unit_Slide.txt', sep='\t', encoding='utf_16', index=False)  # 出力

    print(datetime.datetime.now())
    print('Fin')
if __name__ == '__main__':
    SPC_U02_SlideMerge()