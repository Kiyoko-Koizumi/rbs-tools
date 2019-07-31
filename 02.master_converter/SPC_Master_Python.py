# python test
import glob
import pandas as pd
path='//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/'
#path='C:/Users/Reiko_Tsushima/PycharmProjects/untitled/SPC_Master_Python/'

# ファイルを開く zetta=現法ファイル　spc=駿河見積ファイル　excel=立上ファイル
excel = pd.read_excel(path + 'SPC_Global_inner/190711_SPCマスタ作成依頼.xlsx', dtype=object)
zetta = (pd.read_csv(path + 'Zetta_Product/PRODUCT_20190711151128_1_4.txt',
                    sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
spc = (pd.read_csv(path + 'SPC_Master/PRODUCT/PRODUCT_Master_KOR_03721101_商マス対応版.txt',
                    sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))

# 立上データ出力
SUBSIDIARY_CD=['CHN','KOR','TIW','SGP','MYS','THA','USA','GRM','VNM','JKT','IND']
df3 = pd.DataFrame([],columns=['分析コード', 'Product Code', '立上日', '仕入先', 'Subsidiary Code'])

for SUBSIDIARY_CD in SUBSIDIARY_CD:
    data = (excel[['分析コード','型式',SUBSIDIARY_CD+'立上日',SUBSIDIARY_CD+'仕入先']])
    df = pd.DataFrame(data)
    df2 = df.rename(columns={'型式':'Product Code',SUBSIDIARY_CD+'立上日':'立上日',SUBSIDIARY_CD+'仕入先':'仕入先'})  #列見出し変更（統一）
    df2['Subsidiary Code']=SUBSIDIARY_CD  #「現法コード」列追加
    df2 = df2.query('立上日 == 190712')    # 日付指定をどうするか？
    if len(df2)>0:
        df3 = df3.append(df2)

if len(df3)>0:
    # 　「temp_data」フォルダに作成
    df3.to_csv(path + 'temp_data/SPC_Product.txt',sep='\t',encoding='utf_16',index=False)
    print('Finish!')
else:
    print('Not Found')

# 上記の「SPC_Product.txt」データ読み込み
spc_product = (pd.read_csv(path + 'temp_data/SPC_Product.txt',
                    sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))

# zetta 抽出
zetta_data = pd.merge(zetta,spc_product,on=['Subsidiary Code','Product Code'])  # 立上データの現法コードと型式が一致する現法データ
zetta_data = pd.DataFrame(zetta_data)
zetta_slide = pd.DataFrame(columns={'Subsidiary Code','Product Code','qty','sales','purchase','production','days_ts','rt_s','rt_p','slide_no','data'})

for i in range(1,11):
    i = str(i)
    zetta_data2 = (zetta_data[['Subsidiary Code','Product Code','Slide Qty ' + i,'Slide Sales Pc/Unit ' + i,'Slide Purchase Pc/Unit ' + i,
                               'Slide Production LT ' + i,'Slide Days TS ' + i,'Alt Dsct Rt:S ' + i,'Alt Dsct Rt:P ' + i]])
# 列見出し変更（統一） ★列見出し統一したのにカラム名がソートされる
    zetta_data3 = (zetta_data2.rename(columns={'Slide Qty ' + i:'qty','Slide Sales Pc/Unit ' + i:'sales','Slide Purchase Pc/Unit ' + i:'purchase',
                                               'Slide Production LT ' + i:'production','Slide Days TS ' + i:'days_ts','Alt Dsct Rt:S ' + i:'rt_s','Alt Dsct Rt:P ' + i:'rt_p'}))
    zetta_data3['slide_no'] = i
    zetta_data3['data']='zetta'
    zetta_slide=zetta_slide.append(zetta_data3)

#「temp_data」フォルダに作成
# ★アラートが出る
    zetta_slide.drop_duplicates(subset=['Product Code', 'qty', 'Subsidiary Code'], keep='first',
                                inplace=True)  # 型式・現法コード・数量の重複データ削除　先頭行残す
    zetta_slide = (zetta_slide.query('qty > "0"'))  # 数量スライド>0で抽出
    zetta_slide.to_csv(path + 'temp_data/Zetta_Slide.txt', sep='\t', encoding='utf_16', index=False)
