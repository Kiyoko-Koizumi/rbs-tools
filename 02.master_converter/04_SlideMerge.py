# New Slideデータ作成
import pandas as pd
import numpy as np
import datetime
path='//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/temp_data/'
print(datetime.datetime.now())
# zetta_slide=02_Zetta_Slide.py　spc_slide=03_SPC_Slide.py
zetta_slide = (pd.read_csv(path + 'Zetta_Slide.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
spc_slide = (pd.read_csv(path + 'SPC_Slide.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
slide_marge = pd.DataFrame()

# ■Step1 ZettaとSPCの数量帯をMarge
# Zetta_Slideを基準に結合
h_order=({'Subsidiary Code': 0, 'Product Code': 1, 'slide_no': 2, 'spc_slide_no': 3, 'qty': 4})  # Header並び順
df = pd.DataFrame(columns=h_order)

df = pd.merge(zetta_slide, spc_slide, on=('Subsidiary Code', 'Product Code', 'qty'), how='left')

# ヘッダー名変更
df = (df.rename(columns={'data_x': 'data'}))
df.drop(columns=['data_y'], inplace=True)    #不要な列を削除

# Zetta_SlideとSPC_Slideデータを追加し、重複を削除、data=spcのみを抽出
df1 = pd.DataFrame(columns=h_order)
df1 = df1.append(zetta_slide, sort=False)
df1 = df1.append(spc_slide, sort=False)

df1.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'qty'], keep='first', inplace=True) # 重複データ削除　先頭行残す
df1 = (df1.query('data == "spc"'))  # data=spcで抽出
df=df.append(df1, sort=False)    # dfに追加

# df2=ZettaスライドとSPCスライドをマージしたデータ
slide_marge = df.loc[:,h_order]
slide_marge['qty'] = slide_marge['qty'].astype(int) # qtyを数値
slide_marge = slide_marge.sort_values(by=['Subsidiary Code', 'Product Code', 'qty'], ascending=True)  # 並べ替え
df = slide_marge

# ■Step2　zetta slide_no空白を埋める

h_order={'Subsidiary Code': 0, 'Product Code': 1, 'slide_no': 2, 'qty': 3}
yes = pd.DataFrame(df[df['slide_no'].notnull()])    # slide_no(Zetta)の空白無しを抽出 例　[  1   5  20  35  50  51 100 101 150 301]
nn = pd.DataFrame(df[df['slide_no'].isnull()]) # slide_no(Zetta)の空白を抽出 例　[201]

z = pd.DataFrame(pd.merge(nn, yes, on=('Subsidiary Code', 'Product Code'), suffixes=['_n', '_y'], how='inner')) # 空白データと空白無しデータを結合
z['qty_n'] = z['qty_n'].astype(int)
z['qty_y'] = z['qty_y'].astype(int)
z['sa'] = z['qty_y'] - z['qty_n']  #　空白データの数量と空白無しデータの数量の差を算出
z['sa'] = z['sa'].astype(int)
z['slide_no_y'] = z['slide_no_y'].astype(int)
z.drop(z.index[z.sa > 0], inplace=True)    #　差が0より大きいものは削除
z = z.sort_values(by=['qty_y'], ascending=False)  #　空白無しデータの数量を降順に並び替え
z.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'qty_n'], keep='first', inplace=True)  #　重複削除
z['slide_no_n'] = z['slide_no_y'] #　空白スライド番号に空白無しデータのスライド番号を追加
z = z.rename(columns={'slide_no_n':'slide_no', 'spc_slide_no_n':'spc_slide_no', 'qty_n':'qty'})   # カラム名変更

zz = pd.DataFrame()
zz = pd.concat([z, yes], sort=True)
zz['qty'] = zz['qty'].astype(int)
zz = zz.sort_values(by=['Subsidiary Code', 'Product Code', 'qty'], ascending=True)
#zz.drop_duplicates(subset=['Subsidiary Code','Product Code','qty'],keep='first',inplace=True)
zz = zz.loc[:, h_order]
#zz.to_csv(path + 'zz_Slide.csv', sep='\t', encoding='utf_16', index=False)  # 出力

# ■Step3　spc slide_no空白を埋める
h_order={'Subsidiary Code':0, 'Product Code':1, 'spc_slide_no':2, 'qty':3}
yes = pd.DataFrame(df[df['spc_slide_no'].notnull()])    # spc_slide_noの空白無しを抽出
nn = pd.DataFrame(df[df['spc_slide_no'].isnull()]) # spc_slide_noの空白を抽出
s = pd.DataFrame(pd.merge(nn, yes, on=('Subsidiary Code', 'Product Code'), suffixes=['_n', '_y'], how='inner')) # 空白データと空白無しデータを結合
s['qty_n'] = s['qty_n'].astype(int)
s['qty_y'] = s['qty_y'].astype(int)
s['sa'] = s['qty_y'] - s['qty_n']  #　空白データの数量と空白無しデータの数量の差を算出
s['sa'] = s['sa'].astype(int)
s['spc_slide_no_y'] = s['spc_slide_no_y'].astype(int)
s.drop(s.index[s.sa > 0], inplace=True)    #　差が0より大きいものは削除
s = s.sort_values(by=['qty_y'], ascending=False)  #　空白無しデータの数量を降順に並び替え
s.drop_duplicates(subset=['Subsidiary Code','Product Code','qty_n'],keep='first', inplace=True)  #　重複削除
s['spc_slide_no_n'] = s['spc_slide_no_y'] #　空白スライド番号に空白無しデータのスライド番号を追加
s = s.rename(columns={'slide_no_n':'slide_no', 'spc_slide_no_n':'spc_slide_no', 'qty_n':'qty'})   # カラム名変更

ss = pd.DataFrame()
ss = pd.concat([s, yes], sort=True)
ss['qty'] = ss['qty'].astype(int)
ss = ss.sort_values(by=['Subsidiary Code', 'Product Code', 'qty'], ascending=True)
#ss.drop_duplicates(subset=['Subsidiary Code','Product Code','qty'],keep='first',inplace=True)
ss = ss.loc[:, h_order]
#ss.to_csv(path + 'ss_Slide.csv', sep='\t', encoding='utf_16', index=False)   # 出力

sz = pd.DataFrame(pd.merge(ss, zz))    # slide_no(Zetta)とspc_slide_noを結合
l_order={'Subsidiary Code':0, 'Product Code':1, 'new_slide_no':2, 'slide_no':3, 'spc_slide_no':4, 'qty':5}
sz.loc[:, 'new_slide_no'] = '' # カラム追加
sz = sz.loc[:, l_order]   # カラム並べ替え
sz['qty'] = sz['qty'].astype(int)
sz = sz.sort_values(by=['Subsidiary Code', 'Product Code', 'qty'])
sz['new_slide_no'] = sz.groupby(['Subsidiary Code','Product Code']).cumcount()+1  # 現法コードと商品コードでグループ化　new_slide_noを付ける
sz.to_csv(path + 'SZ_Slide.txt', sep='\t', encoding='utf_16', index=False)  # 出力
sz = (pd.read_csv(path + 'SZ_Slide.txt' ,sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))

# ■Step4 Zetta_Sales、SPC_Purchase他データを追加

new_slide = pd.DataFrame()
n_order=({'Subsidiary Code':0, 'Product Code':1, 'new_slide_no':2, 'slide_no':3, 'spc_slide_no':4,
          'Slide Qty ':7, 'Slide Sales Pc/Unit ':8, 'Slide Purchase Pc/Unit ':9, 'Slide Production LT ':10,
          'Slide Days TS ':11, 'Alt Dsct Rt:S ':12, 'Alt Dsct Rt:P ':13, 'Express L Dsct Rt:S ':14, 'Express L Dsct Rt:P ':15,
          'Express L Slide Days ':16, 'Unit Price Check':17, 'min_order':18, 'max_order':19})

new_slide = pd.merge(sz, zetta_slide, on=['Subsidiary Code', 'Product Code', 'slide_no'])    # Zetta_Slide.txt
new_slide = pd.merge(new_slide, spc_slide, on=['Subsidiary Code', 'Product Code', 'spc_slide_no'])    # SPC_Slide.txt
#new_slide.to_csv(path + 'new_slide_Slide.txt', sep='\t', encoding='utf_16', index=False)  # 出力

# カラム名をマスターカラム名に変更
new_slide = (new_slide.rename(columns={'qty_x': 'Slide Qty ', 'sales': 'Slide Sales Pc/Unit ','purchase':'Slide Purchase Pc/Unit ',
                                        'production':'Slide Production LT ','days_ts':'Slide Days TS ','rt_s':'Alt Dsct Rt:S ','rt_p':'Alt Dsct Rt:P ',
                                        'l_rt_s':'Express L Dsct Rt:S ','l_rt_p':'Express L Dsct Rt:P ','l_days':'Express L Slide Days '}))

new_slide.astype({'Slide Qty ': int, 'Slide Sales Pc/Unit ': float,'Slide Purchase Pc/Unit ': float,
                    'Slide Production LT ': int,'Slide Days TS ': int,'Alt Dsct Rt:S ': int,'Alt Dsct Rt:P ': int,
                    'Express L Dsct Rt:S ': float,'Express L Dsct Rt:P ': float,'Express L Slide Days ': int})

new_slide = new_slide.loc[:, n_order]
new_slide.to_csv(path + 'New_Slide.txt', sep='\t', encoding='utf_16', index=False)  # 出力

# 各カラムを横に展開　Over Slide含む
new_slide = (pd.read_csv(path + 'New_Slide.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
new_slide['new_slide_no'] = new_slide['new_slide_no'].astype(int)
m = max(new_slide['new_slide_no'])
print(m)
col=({'Slide Qty ', 'Slide Sales Pc/Unit ', 'Slide Purchase Pc/Unit ', 'Slide Production LT ',
      'Slide Days TS ', 'Alt Dsct Rt:S ', 'Alt Dsct Rt:P ', 'Express L Dsct Rt:S ', 'Express L Dsct Rt:P ', 'Express L Slide Days '})

dfz = pd.DataFrame(new_slide[['Subsidiary Code', 'Product Code']])
dfz.drop_duplicates(subset=['Subsidiary Code', 'Product Code'], keep='first', inplace=True) # 重複削除

for col in col:
    dfs = pd.DataFrame(new_slide[['Subsidiary Code', 'Product Code', 'new_slide_no', col]])
    dfs = dfs.set_index(['Subsidiary Code', 'Product Code', 'new_slide_no']).unstack(level=2)
    dfscol = []
    #dfs = pd.DataFrame(pd.pivot_table(new_slide,values=col,index=['Subsidiary Code', 'Product Code'], columns='new_slide_no',aggfunc='max')) Pivotは遅いのでやめた
    for n in range(1, m + 1):
        dfscol.append(col+str(n))
    dfs.columns = dfscol
    dfz = pd.DataFrame(pd.merge(dfz, dfs, on=['Subsidiary Code', 'Product Code']))

#dfz.to_csv(path + 'dfz_Slide.txt', sep='\t', encoding='utf_16', index=False)  # 出力

# ヘッダ並び順作成
p_order=['Subsidiary Code', 'Product Code']
for n in range(1, m + 1):
    col = ['Slide Qty ', 'Slide Sales Pc/Unit ', 'Slide Purchase Pc/Unit ', 'Slide Production LT ', 'Slide Days TS ']
    for col in col:
        p_order.append(col+str(n))
for n in range(1, m + 1):
    col = ['Alt Dsct Rt:S ', 'Alt Dsct Rt:P ']
    for col in col:
        p_order.append(col + str(n))
for n in range(1, m + 1):
    col = ['Express L Dsct Rt:S ', 'Express L Dsct Rt:P ', 'Express L Slide Days ']
    for col in col:
        p_order.append(col + str(n))

dfz = dfz.loc[:, p_order]
dfz.to_csv(path + 'Product_Slide.txt', sep='\t', encoding='utf_16', index=False)  # 出力
print(datetime.datetime.now())
print('Fin')