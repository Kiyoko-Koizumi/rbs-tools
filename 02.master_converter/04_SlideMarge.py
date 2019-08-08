# New Slideデータ作成
import pandas as pd
import numpy as np
path='//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/temp_data/'

zetta_slide = (pd.read_csv(path + 'Zetta_Slide.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
spc_slide = (pd.read_csv(path + 'SPC_Slide.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))

# Zetta_Slideを基準に結合
h_order=({'Subsidiary Code':0,'Stock / MTO':1,'Min Qty of Big Order':2,'Product Code':3,'slide_no':4, 'spc_slide_no':5, 'qty':6})  # Header並び順
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
df2 = df.loc[:,h_order]
df2.to_csv(path + 'slide_marge.txt', sep='\t', encoding='utf_16', index=False)  # test出力　呼び出しはしていない

# New Slide Noをふりたい
#n_order=({'Subsidiary Code':0,'Product Code':1,'new_slide_no':2, 'qty':3})

# df3=df2の現法コードと商品コードでグループ化（重複削除）
#df3 = df2.loc[:,['Subsidiary Code','Product Code']]
#df3.drop_duplicates(subset=['Subsidiary Code','Product Code'],keep='first',inplace=True)


print('Fin')