# Zetta Product 複数ファイルよりSlideデータとMaster抽出　test：GRM/USA
import glob
import pandas as pd
import numpy as np
import Header

path='//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/'

# SPC_Product.txt」データ読み込み
spc_product = (pd.read_csv(path + 'temp_data/SPC_Target.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
days_ts = (pd.read_excel(path + 'temp_master/Days_Ts.xlsx'))    # 製作日数・カタログ納期・当日受注締時刻
weight = pd.read_excel(path + 'temp_master/【提出用】ベトナム重量ロジック★最終アップリスト_CC.xlsx', dtype=object) # 重量式

# フォルダからtxtファイル名抽出　フルパス
files = glob.glob(path + 'Zetta_Product/*.txt')
lists=[]
for file in files:
    # 　フルパスからファイル名のみ抽出
    lists.append(file.replace(path + 'Zetta_Product',''))

n=len(lists)

h_order=({'Subsidiary Code':0,'Product Code':1,'slide_no':2, 'qty':3, 'sales':4,
           'production':5, 'days_ts':6, 'rt_s':7,'l_rt_s':8,'data':9})  # Header並び順
zetta_slide = pd.DataFrame()   # スライド出力用
# zetta_data1をHeader.pyで並び順を変更
#zetta_data1 = Header.Header()    # ALLデータ出力用
zetta_data1 = pd.DataFrame([],columns=Header.Header())    # ALLデータ出力用 こっちの記述でも出来ました。何となくしっくりくるのでこちらで。

for l in range(0, n):
    zetta = (pd.read_csv(path + 'Zetta_Product/' + lists[l],sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    zetta_data = pd.merge(zetta, spc_product, on=['Subsidiary Code', 'Product Code'])  # 立上データの現法コードと型式が一致する現法データ
    zetta_data1 = zetta_data1.append(zetta_data,sort=False)

    for i in range(1, 11):
        i = str(i)
        zetta_data2 = (zetta_data[['Subsidiary Code', 'Product Code', 'Slide Qty ' + i, 'Slide Sales Pc/Unit ' + i,
                                   'Slide Production LT ' + i, 'Slide Days TS ' + i, 'Alt Dsct Rt:S ' + i, 'Express L Dsct Rt:S ' + i]])
# 列見出し変更（統一） カラム名並びは「h_order」にて解消
        zetta_data3 = (zetta_data2.rename(columns={'slide_no':'slide_no','Slide Qty ' + i: 'qty','Slide Sales Pc/Unit ' + i: 'sales',
                                                   'Slide Production LT ' + i: 'production','Slide Days TS ' + i: 'days_ts',
                                                   'Alt Dsct Rt:S ' + i: 'rt_s','Express L Dsct Rt:S ' + i:'l_rt_s'}))
        zetta_data3['l_rt_s'] = 0
        zetta_data3['slide_no'] = i
        zetta_data3['data']='zetta'
        zetta_slide = zetta_slide.append(zetta_data3,sort=False)

zetta_slide.drop_duplicates(subset=['Product Code','qty', 'Subsidiary Code'],keep='first',inplace=True) # 型式・現法コード・数量の重複データ削除　先頭行残す
zetta_slide = (zetta_slide.query('qty > "0"'))  # 数量スライド>0で抽出

h_product = pd.DataFrame(zetta[zetta['Subsidiary Code'] == 'XXX'])  # ヘッダ抽出
h_product.to_csv(path + 'temp_data/h_Product.txt', sep='\t', encoding='utf_16', index=False)  # h_Product.txt　ヘッダ出力

# Days_Ts.xlsx結合 製作日数・カタログ納期更新
# 1Rec単位で更新をしているがRec数が増えたら遅くなるのか？
zetta_slide = pd.merge(zetta_slide, days_ts,on=['Subsidiary Code'])

df2 = pd.DataFrame()
n = len(zetta_slide)
for i in range(0, n):
    df = zetta_slide.loc[[i]]
    df['production'] = df['production'].astype(int)
    df['DaysTS'] = df['DaysTS'].astype(int)
    df['GTI_Order_Close'] = df['GTI_Order_Close'].astype(int)
    a = np.array(df['production'])  # 製作日数
    b = np.array(df['DaysTS'])  # Days_Ts.xlsxの輸送日数
    c = a - b   # 製作日数用　製作日数-輸送日数
    d = a + b   # カタログ納期用　製作日数+輸送日数
    # 製作日数＝製作日数が99の時、製作日数-[DaysTS](輸送日数)、それ以外は製作日数
    if a == 99:
        df['production'] = c
    else:
        df['production'] = a
    # カタログ納期＝製作日数が0 Or 99の時、製作日数、 製作日数+[Days_TS](輸送日数)>99の時、99、それ以外は製作日数+[Days_TS](輸送日数)
    if a == 0 or a == 99:
        df['days_ts'] = a
    elif d > 0 and d < 99:
        df['days_ts'] = d
    elif d > 99:
        df['days_ts'] = 99
    df2 = df2.append(df, sort=False)

df2= df2.loc[:, h_order]   # カラム並べ替え
df2.to_csv(path + 'temp_data/Zetta_Slide.txt', sep='\t', encoding='utf_16', index=False)    # Zetta_Slide.txt スライドデータのみ出力

# 重量式項目追加
zetta_data1 = pd.merge(zetta_data1, weight, left_on='Product Code', right_on='型式', how='left')

# Days_Ts.excel 項目追加
zetta_data1 = pd.merge(zetta_data1, days_ts, on='Subsidiary Code', how='left')

zetta_data1.drop(columns=['分析コード_x','立上日','仕入先','分析コード_y','分析コード名称','インナーコード','Weight Coefficient_y','Weight_Round前'],inplace=True)    #不要な列を削除
zetta_data1 = zetta_data1.rename(columns={'Weight_x':'Weight','Weight Calc Mode_x': 'Weight Calc Mode','Weight Coefficient_x': 'Weight Coefficient','Weight Calc_x':'Weight Calc'})
zetta_data1.to_csv(path + 'temp_data/Zetta_Product.txt', sep='\t', encoding='utf_16', index=False)  # Zetta_Product.txt　ALL出力
print('Fin')
