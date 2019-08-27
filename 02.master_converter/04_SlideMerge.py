# New Slideデータ作成
import pandas as pd
import numpy as np
path='//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/temp_data/'

# zetta_slide=02_Zetta_Slide.py　spc_slide=03_SPC_Slide.py
zetta_slide = (pd.read_csv(path + 'Zetta_Slide.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
spc_slide = (pd.read_csv(path + 'SPC_Slide.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
slide_marge = pd.DataFrame()

#■■■ Step1 ZettaとSPCの数量帯をMarge　■■■
# Zetta_Slideを基準に結合
h_order=({'Subsidiary Code':0,'Product Code':2,'slide_no':3, 'spc_slide_no':4, 'qty':5})  # Header並び順
df = pd.DataFrame(columns=h_order)

df = pd.merge(zetta_slide,spc_slide,on=('Subsidiary Code','Product Code','qty'), how='left')

# ヘッダー名変更
df = (df.rename(columns={'data_x': 'data'}))
df.drop(columns=['data_y'],inplace=True)    #不要な列を削除

# Zetta_SlideとSPC_Slideデータを追加し、重複を削除、data=spcのみを抽出
df1 = pd.DataFrame(columns=h_order)
df1 = df1.append(zetta_slide, sort=False)
df1 = df1.append(spc_slide, sort=False)

df1.drop_duplicates(subset=['Subsidiary Code','Product Code','qty'],keep='first',inplace=True) # 重複データ削除　先頭行残す
df1 = (df1.query('data == "spc"'))  # data=spcで抽出
df=df.append(df1,sort=False)    # dfに追加

# df2=ZettaスライドとSPCスライドをマージしたデータ
slide_marge = df.loc[:,h_order]
slide_marge['qty'] = slide_marge['qty'].astype(int) # qtyを数値
slide_marge = slide_marge.sort_values(by=['Subsidiary Code','Product Code','qty'], ascending=True)  # 並べ替え
#slide_marge.to_csv(path + 'slide_marge.txt', sep='\t', encoding='utf_16', index=False)  # test出力　呼び出しはしていない


#■■■ Step2 Step1でMargeされた数量帯のSlide番号を埋める　■■■
# margeしたデータ 例　[  1   5  20  35  50  51 100 101 150 201 301 501] [201と501]はSPCにはあるが、Zettaにはない
df = slide_marge
# slide_no(Zetta)の空白ではないデータを抽出
dfz = pd.DataFrame(df[df['slide_no'].notnull()])

# slide_no(Zetta)=Nullのデータ
df1 = pd.DataFrame(df[df['slide_no'].isnull()]) # slide_no(Zetta)の空白を抽出
df2 = df1.reset_index()
n = len(df2)
df2['qty'] = df2['qty'].astype(int)  # qtyを数値に変換
dfz1 = pd.DataFrame()
df4 = pd.DataFrame()
df5 = pd.DataFrame()
df6 = pd.DataFrame()
df7 = pd.DataFrame()

h_order={'Subsidiary Code':0,'Product Code':1,'slide_no':2,'qty':3}

for i in range(0, n):
    dfs = df2.loc[[i]]   # 空白ありのデータ=SPC
    #dfs = df2.loc[:, i]  # 空白ありのデータ=SPC
    m = len(dfs)
    dfs['qty'] = dfs['qty'].astype(int)
    a = np.array(dfs['qty'])
    #print(a)    # 空白の数量　例　[201]

    dfz1 = pd.merge(dfz, dfs, on=('Subsidiary Code', 'Product Code'), how='inner')  # 空白ありのデータ＝空ではないデータ
    dfz1['qty_x'] = dfz1['qty_x'].astype(int)
    b = np.array(dfz1['qty_x'])
    #print(b)    # 空白の数量を除いた数量　例　[  1   5  20  35  50  51 100 101 150 301]

    dfz2 = (dfz1.rename(columns={'qty_x': 'qty', 'slide_no_x': 'slide_no'}))
    df4 = pd.DataFrame(df4.append(dfz2,sort=False))
    df4 = df4.loc[:, h_order]

    c = (b[b < a].max())
    #print(c)    # 空白数量より小さい、Max数量　例　150

    df3 = (dfz2[dfz2['qty'] == c].copy())  # 空白なしデータより数量=c(150)を抽出
    df3.loc[:, 'qty'] = a  # 空白なしデータの数量を空白の数量に変更 例　150→201

    df4 = df4.append(df3,sort=False)    # 空白を埋めたデータを追加
    df4 = df4.sort_values(by=['qty'], ascending=True)   # 数量で並べ替え

df4 = df4.loc[:, h_order]
df4.drop_duplicates(subset=['Subsidiary Code','Product Code','qty'],keep='first',inplace=True) # 同一商品で空白が複数あると、その回数分データが作成されるので重複削除

df = df.loc[:, h_order]
df5 = pd.concat([df4,df])   # df4=空白を埋めたデータ　df=ALLデータ　を縦結合
df5['qty'] = df5['qty'].astype(int) # qtyを数値
df5 = df5.sort_values(by=['Subsidiary Code','Product Code','qty'], ascending=True)  # 並べ替え　※並べ替えをしないと重複削除されなかった
df5.drop_duplicates(subset=['Subsidiary Code','Product Code','qty'],keep='first',inplace=True) # 重複削除

#df5.to_csv(path + 'tsm_zetta.txt', sep='\t', encoding='utf_16', index=False)  # 出力
print('zetta fin')

# ★★★　SPC処理
print('spc start')
#df = pd.DataFrame(pd.read_csv(path + 'slide_marge.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
# spc_slide_no(SPC)の空白ではないデータを抽出
df = slide_marge
dfz = pd.DataFrame(df[df['spc_slide_no'].notnull()])

# spc_slide_no(SPC)=Nullのデータ
df1 = pd.DataFrame(df[df['spc_slide_no'].isnull()]) # slide_no(Zetta)の空白を抽出
df2 = df1.reset_index()
n = len(df2)
df2['qty'] = df2['qty'].astype(int)  # qtyを数値に変換
dfz1 = pd.DataFrame()
df4 = pd.DataFrame()

h_order={'Subsidiary Code':0,'Product Code':1,'spc_slide_no':2,'qty':3}

for i in range(0, n):
    dfs = df2.loc[[i]]   # 空白ありのデータ=SPC
    #dfs = df2.loc[:, i]  # 空白ありのデータ=SPC
    m = len(dfs)
    dfs['qty'] = dfs['qty'].astype(int)
    a = np.array(dfs['qty'])
    #print(a)    # 空白の数量　例　[201]

    dfz1 = pd.merge(dfz, dfs, on=('Subsidiary Code', 'Product Code'), how='inner')  # 空白ありのデータ＝空ではないデータ
    dfz1['qty_x'] = dfz1['qty_x'].astype(int)
    b = np.array(dfz1['qty_x'])
    #print(b)    # 空白の数量を除いた数量　例　[  1   5  20  35  50  51 100 101 150 301]

    dfz2 = (dfz1.rename(columns={'qty_x': 'qty', 'spc_slide_no_x': 'spc_slide_no'}))
    df4 = df4.append(dfz2,sort=False)
    df4 = df4.loc[:, h_order]

    c = (b[b < a].max())
    #print(c)    # 空白数量より小さい、Max数量　例　150

    df3 = (dfz2[dfz2['qty'] == c].copy())  # 空白なしデータより数量=c(150)を抽出
    df3.loc[:, 'qty'] = a  # 空白なしデータの数量を空白の数量に変更 例　150→201

    df4 = df4.append(df3,sort=False)    # 空白を埋めたデータを追加
    df4 = df4.sort_values(by=['qty'], ascending=True)   # 数量で並べ替え

df4 = df4.loc[:, h_order]
df4.drop_duplicates(subset=['Subsidiary Code','Product Code','qty'],keep='first',inplace=True) # 同一商品で空白が複数あると、その回数分データが作成されるので重複削除

df = df.loc[:, h_order]
df6 = pd.concat([df4,df])   # df4=空白を埋めたデータ　df=ALLデータ　を縦結合
df6['qty'] = df6['qty'].astype(int) # qtyを数値
df6 = df6.sort_values(by=['Subsidiary Code','Product Code','qty'], ascending=True)  # 並べ替え　※並べ替えをしないと重複削除されなかった
df6.drop_duplicates(subset=['Subsidiary Code','Product Code','qty'],keep='first',inplace=True) # 重複削除

df7 = pd.merge(df5, df6)    # slide_no(Zetta)とspc_slide_noを結合
l_order={'Subsidiary Code':0,'Product Code':1,'new_slide_no':2,'slide_no':3,'spc_slide_no':4,'qty':5}
df7.loc[:, 'new_slide_no'] = '' # カラム追加
df7 = df7.loc[:, l_order]   # カラム並べ替え
df7['new_slide_no'] = df7.groupby(['Subsidiary Code','Product Code']).cumcount()+1  # 現王コードと商品コードでグループ化　new_slide_noを付ける
#df7.to_csv(path + 'tsm_spc.txt', sep='\t', encoding='utf_16', index=False)  # 出力

#■■■ Step3 Step2にZetta_Sales、SPC_Purchase他データを追加　■■■

new_slide = pd.DataFrame()
n_order=({'Subsidiary Code':0, 'Product Code':1, 'new_slide_no':2, 'slide_no':3, 'spc_slide_no':4,
          'Slide Qty ':7, 'Slide Sales Pc/Unit ':8, 'Slide Purchase Pc/Unit ':9, 'Slide Production LT ':10,
          'Slide Days TS ':11, 'Alt Dsct Rt:S ':12, 'Alt Dsct Rt:P ':13, 'Express L Dsct Rt:S ':14, 'Express L Dsct Rt:P ':15,
          'Express L Slide Days ':16, 'Unit Price Check':17})

new_slide = pd.merge(df7, zetta_slide, on=['Subsidiary Code','Product Code','slide_no'])    # Zetta_Slide.txt
new_slide = pd.merge(new_slide, spc_slide, on=['Subsidiary Code','Product Code','spc_slide_no'])    # SPC_Slide.txt

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
m = max(new_slide['new_slide_no'])
col=({'Slide Qty ','Slide Sales Pc/Unit ','Slide Purchase Pc/Unit ','Slide Production LT ',
      'Slide Days TS ','Alt Dsct Rt:S ','Alt Dsct Rt:P ','Express L Dsct Rt:S ','Express L Dsct Rt:P ',
          'Express L Slide Days '})

for col in col:
    dfs = pd.DataFrame(pd.pivot_table(new_slide,values=col,index=['Subsidiary Code','Product Code'], columns='new_slide_no',aggfunc='max'))
    for n in range(1, m + 1):
        dfs = dfs.rename(columns={n:col+str(n)})
    dfz = pd.merge(dfz, dfs, on=['Subsidiary Code','Product Code'])

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
    col = ['Express L Dsct Rt:S ', 'Express L Dsct Rt:P ','Express L Slide Days ']
    for col in col:
        p_order.append(col + str(n))
#print(p_order)

spc_slide = spc_slide[['Subsidiary Code','Product Code']]
spc_slide.drop_duplicates(subset=['Subsidiary Code','Product Code'],keep='first',inplace=True) # 重複削除
dfz = pd.merge(dfz, spc_slide, on=['Subsidiary Code','Product Code'])

dfz.drop(columns=['slide_no','spc_slide_no','qty'],inplace=True)    #不要な列を削除
dfz.drop_duplicates(subset=['Subsidiary Code','Product Code'],keep='first',inplace=True) # 重複削除
dfz = dfz.loc[:, p_order]
dfz.to_csv(path + 'Product_Slide.txt', sep='\t', encoding='utf_16', index=False)  # 出力
print('Fin')