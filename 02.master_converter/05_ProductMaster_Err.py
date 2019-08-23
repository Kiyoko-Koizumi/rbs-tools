# Err flg
import pandas as pd
import numpy as np
path='//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/temp_data/'

# over_slide・sales(n)<sales(n+1)・purchase(n)<purchase(n+1)・slide1=(sales=0 and purchase>0) or (sales>0 and purchase=0)
new_slide = (pd.read_csv(path + 'New_Slide.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
new_slide['new_slide_no'] = new_slide['new_slide_no'].astype(int)
p_zetta = (pd.read_csv(path + 'Zetta_Product.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))   # 重量式エラーチェックのため

h_order=({'Subsidiary Code':0,'Product Code':1,'err':2})

# df Errデータ格納
df = pd.DataFrame(new_slide.query('new_slide_no > 10'))  # Over_Slide_Check
df['err'] = '6'   # Over_slide
df.drop_duplicates(subset=['Subsidiary Code', 'Product Code'],keep='first',inplace=True)
df = df.loc[:, h_order]

# df1 現法コードと商品コードでグループ化
df1 = pd.DataFrame(new_slide)
df1.drop_duplicates(subset=['Subsidiary Code', 'Product Code'],keep='first',inplace=True)
df1 = df1.loc[:,['Subsidiary Code','Product Code']]
df1 = df1.reset_index(drop=True)
n = len(df1)

# Slide1 Sales=0 and Purchase>0 err_1
df3 = pd.DataFrame(new_slide.rename(columns={'Slide Sales Pc/Unit ': 'sales', 'Slide Purchase Pc/Unit ': 'purchase', 'Unit Price Check':'unit'}))
df3['sales'] = df3['sales'].astype(float)
df3['purchase'] = df3['purchase'].astype(float)
df3.loc[:, 'err'] = ''
df3 = df3.query('new_slide_no == 1 and sales  == 0 and purchase >0')
df3['err'] = '1'
df = df.append(df3,sort=False)

# Slide1 Sales>0 and Purchase=0 err_1
df3 = df3.query('new_slide_no == 1 and sales  > 0 and purchase ==0')
df3['err'] = '1'
df = df.append(df3,sort=False)

df.drop_duplicates(subset=['Subsidiary Code', 'Product Code','err'],keep='first',inplace=True)
df = df.loc[:, h_order]
df = df.reset_index(drop=True)

# 単価チェック区分=0 sales=0 and purchase>0
df3 = df3.query('unit == 0 and sales  == 0 and purchase >0')
df3['err'] = '2'
df = df.append(df3,sort=False)

df.drop_duplicates(subset=['Subsidiary Code', 'Product Code','err'],keep='first',inplace=True)
df = df.loc[:, h_order]
df = df.reset_index(drop=True)

# 重量式なし
df3 = pd.DataFrame(p_zetta[p_zetta['型式'].isnull()]) # 重量式リストの「型式」空白を抽出
df3['err'] = '3'
df = df.append(df3,sort=False)
df = df.loc[:, h_order]
df = df.reset_index(drop=True)

# Sales(n) < Sales(n+1) と Purchase(n) < Purchase(n+1) Check err_4とerr_5
for i in range(0, n):
    dfs = df1.loc[[i]]
    df2 = pd.merge(dfs, new_slide, on=['Subsidiary Code', 'Product Code'])
    df2 = df2.loc[:,['Subsidiary Code','Product Code','new_slide_no','Slide Sales Pc/Unit ','Slide Purchase Pc/Unit ']]
    df2['Slide Sales Pc/Unit '] = df2['Slide Sales Pc/Unit '].astype(float)
    df2['new_slide_no'] = df2['new_slide_no'].astype(int)
    df2 = df2.sort_values(by=['Subsidiary Code','Product Code','new_slide_no'], ascending=True)
    o = len(df2)

    for j in range(0, o):
        s1 = pd.DataFrame(df2.loc[j:j])
        s2 = pd.DataFrame(df2.loc[j+1:j+1])
        s = np.float32(s1['Slide Sales Pc/Unit '])-np.float32(s2['Slide Sales Pc/Unit '])
        p = np.float32(s1['Slide Purchase Pc/Unit ']) - np.float32(s2['Slide Purchase Pc/Unit '])
        s1.loc[:, 'err'] = ''  # カラム追加
        if s.size > 0 and s < 0 :
            s1['err'] = '4' # Sales Err
            df = df.append(s1,sort=False)
            break
        if p.size > 0 and p < 0 :
            s1['err'] = '5' # Purchase Err
            df = df.append(s1, sort=False)
            break
        s = []
        p = []

# Product_Slide.txtにエラーフラグを追加
p_zetta = (pd.read_csv(path + 'Product_Slide.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
dfs = pd.DataFrame(pd.crosstab([df['Product Code'], df['Subsidiary Code']], 'err_' + df['err']))
for i in range(1, 7):   # err_1～6のカラムチェック　無しはカラム名追加
    if 'err_' + str(i) in dfs.columns:
        print('err_' + str(i))
    else:
        dfs['err_' + str(i)] = ''

p_err = pd.merge(p_zetta, dfs, on=('Subsidiary Code', 'Product Code'), how='left')
p_err.to_csv(path + 'Product_Slide.txt', sep='\t', encoding='utf_16', index=False)  # 出力
print('fin')