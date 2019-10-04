# New Slideデータ作成
import pandas as pd
import numpy as np
import datetime
path = '//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/temp_data/'
print(datetime.datetime.now())
# zetta_slide=02_Zetta_Slide.py　spc_slide=03_SPC_Slide.py
zetta_slide = (pd.read_csv(path + 'Zetta_U_Slide.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
spc_slide = (pd.read_csv(path + 'SPC_U_Slide.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
slide_marge = pd.DataFrame()

# ■Step1 ZettaとSPCのMin.ValをMarge
h_order=({'Subsidiary Code': 0, 'Product Code': 1, 'new_slide_no': 2, 'Min.Val.1': 3, 'Min.Val.2': 4, 'Min.Val.3': 5, 'Min.Val.4': 6, 'Min.Val.5': 7, 'sales': 8, 'purchase': 9})  # Header並び順
df = pd.DataFrame(columns=h_order)
z = (zetta_slide[['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5']])
s = (spc_slide[['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5']])
df = df.append([z, s], sort=False)
df.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'], keep='first', inplace=True)     # 重複削除

df = pd.merge(df, zetta_slide, on=('Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1'), how='left')
df = pd.merge(df, spc_slide, on=('Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1'), how='left')
df.drop(columns=['Min.Val.2_y', 'Min.Val.3_y', 'Min.Val.4_y', 'Min.Val.5_y', 'sales_x', 'purchase_x', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'], inplace=True)    # 不要な列を削除
df = df.rename(columns={'Min.Val.2_x': 'Min.Val.2', 'Min.Val.3_x': 'Min.Val.3', 'Min.Val.4_x': 'Min.Val.4', 'Min.Val.5_x': 'Min.Val.5', 'sales_y': 'sales', 'purchase_y': 'purchase'})   # カラム名変更
df = df.loc[:, h_order]
df = df.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1'], ascending=True)  # 並べ替え
dfs = pd.DataFrame(df[['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5']])
dfs = dfs.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1', 'new_slide_no'], ascending=True)

# ■Step2　sales空白を埋める　上から下に（例：minval 18がNullのとき、minval 16 のsalse
nn = pd.DataFrame(df[df['sales'].isnull()])
yes = pd.DataFrame(df[df['sales'].notnull()])

z = pd.DataFrame(pd.merge(nn, yes, on=('Subsidiary Code', 'Product Code', 'new_slide_no'), suffixes=['_n', '_y'], how='inner')) # 空白データと空白無しデータを結合

z['Min.Val.1_n'] = z['Min.Val.1_n'].astype(float)
z['Min.Val.1_y'] = z['Min.Val.1_y'].astype(float)
z['sa'] = z['Min.Val.1_y'] - z['Min.Val.1_n']  #　空白データのMin.Val.1と空白無しデータのMin.Val.1の差を算出
z['sa'] = z['sa'].astype(float)
z['new_slide_no'] = z['new_slide_no'].astype(int)
z.drop(z.index[z.sa > 0], inplace=True)    #　差が0より大きいものは削除
z.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1_n'], keep='first', inplace=True)  # 重複削除
z.loc[z['sa'] < 0, 'sales_n'] = z['sales_y']
z = z.rename(columns={'Min.Val.1_n': 'Min.Val.1', 'Min.Val.2_n': 'Min.Val.2', 'Min.Val.3_n': 'Min.Val.3', 'Min.Val.4_n': 'Min.Val.4', 'Min.Val.5_n': 'Min.Val.5', 'sales_n': 'sales'})   # カラム名変更

zz = pd.DataFrame(pd.concat([z, yes], sort=True))
zz.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'], keep='first', inplace=True)
zz.reset_index(drop=True,inplace=True)

zz = zz.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1', 'new_slide_no'], ascending=True)

zz = zz.loc[:, h_order]
zz = zz.drop(columns=['purchase'])

# 出力しないとsalesがちゃんと反映されない・・・なぜ？結合Keyが多いから？
#zz.to_csv(path + 'U_zz_Slide.txt', sep='\t', encoding='utf_16', index=False)  # 出力
#zz = pd.DataFrame(pd.read_csv(path + 'U_zz_Slide.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
#dfs = pd.merge(dfs, zz, on=('Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'), how='left')    #, 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'

# right_index/reft_indexをTrueにしたらできた！
dfs = pd.merge(dfs, zz, right_index=True, left_index=True)
dfs = dfs.rename(columns={'Subsidiary Code_x': 'Subsidiary Code', 'Product Code_x': 'Product Code', 'new_slide_no_x': 'new_slide_no',
                          'Min.Val.1_x': 'Min.Val.1', 'Min.Val.2_x': 'Min.Val.2', 'Min.Val.3_x': 'Min.Val.3',
                          'Min.Val.4_x': 'Min.Val.4', 'Min.Val.5_x': 'Min.Val.5'})   # カラム名変更
dfs.drop(columns=['Subsidiary Code_y', 'Product Code_y', 'new_slide_no_y', 'Min.Val.1_y', 'Min.Val.2_y', 'Min.Val.3_y',
                  'Min.Val.4_y', 'Min.Val.5_y'], inplace=True)    #不要な列を削除

# ■Step3　purchase空白を埋める 上から下に（例：minval 18がNullのとき、minval 16 のpurchase
nn = pd.DataFrame(df[df['purchase'].isnull()])
yes = pd.DataFrame(df[df['purchase'].notnull()])

s = pd.DataFrame(pd.merge(nn, yes, on=('Subsidiary Code', 'Product Code', 'new_slide_no'), suffixes=['_n', '_y'], how='inner')) # 空白データと空白無しデータを結合

s['Min.Val.1_n'] = s['Min.Val.1_n'].astype(float)
s['Min.Val.1_y'] = s['Min.Val.1_y'].astype(float)
s['sa'] = s['Min.Val.1_y'] - s['Min.Val.1_n']  # 空白データのMin.Val.1と空白無しデータのMin.Val.1の差を算出
s['sa'] = s['sa'].astype(float)
s['new_slide_no'] = s['new_slide_no'].astype(int)
s.drop(s.index[s.sa > 0], inplace=True)    # 差が0より大きいものは削除

s.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1_n'], keep='first', inplace=True)  # 重複削除
s.loc[s['sa'] < 0, 'purchase_n'] = s['purchase_y']
s = s.rename(columns={'Min.Val.1_n': 'Min.Val.1', 'Min.Val.2_n': 'Min.Val.2', 'Min.Val.3_n': 'Min.Val.3', 'Min.Val.4_n': 'Min.Val.4', 'Min.Val.5_n': 'Min.Val.5', 'purchase_n': 'purchase'})   # カラム名変更

ss = pd.DataFrame(pd.concat([s, yes], sort=True))

ss = ss.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1', 'new_slide_no'], ascending=True)
ss.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'], keep='first', inplace=True)
ss.reset_index(drop=True,inplace=True)

ss = ss.loc[:, h_order]
ss = ss.drop(columns=['sales'])

dfs = pd.merge(dfs, ss, on=('Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'), how='left')

# データフレームを空にする
zz[:0]
ss[:0]
nn[:0]
yes[:0]

# ■Step4　sales/purchase空白を埋める 下から上に（例：minval 16がNullのとき、minval 18 のsales/purchase
nn = pd.DataFrame(dfs[dfs['sales'].isnull()])
yes = pd.DataFrame(dfs[dfs['sales'].notnull()])

if len(nn) > 0:
    z = pd.DataFrame(pd.merge(nn, yes, on=('Subsidiary Code', 'Product Code', 'new_slide_no'), suffixes=['_n', '_y'], how='inner')) # 空白データと空白無しデータを結合
    z = z.drop(columns=['purchase_n', 'purchase_y'])
    z['Min.Val.1_n'] = z['Min.Val.1_n'].astype(float)
    z['Min.Val.1_y'] = z['Min.Val.1_y'].astype(float)
    z['sa'] = z['Min.Val.1_y'] - z['Min.Val.1_n']  # 空白データのMin.Val.1と空白無しデータのMin.Val.1の差を算出
    z['sa'] = z['sa'].astype(float)
    z['new_slide_no'] = z['new_slide_no'].astype(int)
    z = z.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1_n', 'new_slide_no', 'sa'], ascending=True)
    z.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1_n'], keep='first', inplace=True)  # 重複削除
    z['sales_n'] = z['sales_y']
    z = z.rename(columns={'Min.Val.1_n': 'Min.Val.1', 'Min.Val.2_n': 'Min.Val.2', 'Min.Val.3_n': 'Min.Val.3', 'Min.Val.4_n': 'Min.Val.4', 'Min.Val.5_n': 'Min.Val.5', 'sales_n': 'sales'})   # カラム名変更

    zz = pd.DataFrame(pd.concat([z, yes], sort=True))
    zz = zz.drop(columns=['Min.Val.1_y', 'Min.Val.2_y', 'Min.Val.3_y', 'Min.Val.4_y', 'Min.Val.5_y', 'sales_y', 'purchase', 'sa'])
    zz.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'], keep='first', inplace=True)

else:
    zz = pd.DataFrame(dfs[['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5', 'sales']])

zz = zz.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1', 'new_slide_no'], ascending=True)
zz.reset_index(drop=True, inplace=True)
zz = zz.reindex(columns=h_order)
zz = zz.drop(columns=['purchase'])

nn[:0]
yes[:0]
nn = pd.DataFrame(dfs[dfs['purchase'].isnull()])
yes = pd.DataFrame(dfs[dfs['purchase'].notnull()])

if len(nn) > 0:
    s = pd.DataFrame(pd.merge(nn, yes, on=('Subsidiary Code', 'Product Code', 'new_slide_no'), suffixes=['_n', '_y'], how='inner')) # 空白データと空白無しデータを結合
    s = s.drop(columns=['sales_n', 'sales_y'])
    s['Min.Val.1_n'] = s['Min.Val.1_n'].astype(float)
    s['Min.Val.1_y'] = s['Min.Val.1_y'].astype(float)
    s['sa'] = s['Min.Val.1_y'] - s['Min.Val.1_n']  # 空白データのMin.Val.1と空白無しデータのMin.Val.1の差を算出
    s['sa'] = s['sa'].astype(float)
    s['new_slide_no'] = s['new_slide_no'].astype(int)
    s = s.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1_n', 'new_slide_no', 'sa'], ascending=True)
    s.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1_n'], keep='first', inplace=True)  # 重複削除
    s['purchase_n'] = s['purchase_y']
    s = s.rename(columns={'Min.Val.1_n': 'Min.Val.1', 'Min.Val.2_n': 'Min.Val.2', 'Min.Val.3_n': 'Min.Val.3', 'Min.Val.4_n': 'Min.Val.4', 'Min.Val.5_n': 'Min.Val.5', 'purchase_n': 'purchase'})   # カラム名変更

    ss = pd.DataFrame(pd.concat([s, yes], sort=True))
    ss = ss.drop(columns=['Min.Val.1_y', 'Min.Val.2_y', 'Min.Val.3_y', 'Min.Val.4_y', 'Min.Val.5_y', 'purchase_y', 'sales', 'sa'])
    ss.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5'], keep='first', inplace=True)
    #ss.to_csv(path + 'ss_us_Slide.csv', sep='\t', encoding='utf_16', index=False)  # 出力

else:
    ss = pd.DataFrame(dfs[['Subsidiary Code', 'Product Code', 'new_slide_no', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5', 'purchase']])

ss = ss.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1', 'new_slide_no'], ascending=True)
ss.reset_index(drop=True, inplace=True)
ss = ss.reindex(columns=h_order)
ss = ss.drop(columns=['sales'])

df = pd.merge(zz, ss, right_index=True, left_index=True)
df = df.rename(columns={'Subsidiary Code_x': 'Subsidiary Code', 'Product Code_x': 'Product Code', 'new_slide_no_x': 'new_slide_no',
                          'Min.Val.1_x': 'Min.Val.1', 'Min.Val.2_x': 'Min.Val.2', 'Min.Val.3_x': 'Min.Val.3',
                          'Min.Val.4_x': 'Min.Val.4', 'Min.Val.5_x': 'Min.Val.5'})   # カラム名変更
df.drop(columns=['Subsidiary Code_y', 'Product Code_y', 'new_slide_no_y', 'Min.Val.1_y', 'Min.Val.2_y', 'Min.Val.3_y',
                  'Min.Val.4_y', 'Min.Val.5_y'], inplace=True)    # 不要な列を削除

df.to_csv(path + 'Unit_Slide.csv', sep='\t', encoding='utf_16', index=False)  # 出力
print(datetime.datetime.now())
print('Fin')