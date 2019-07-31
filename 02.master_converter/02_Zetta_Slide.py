# Zetta Product 複数ファイルよりSlideデータ抽出　test：GRM/USA
import glob
import pandas as pd
import Header

path='//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/'

# SPC_Product.txt」データ読み込み
spc_product = (pd.read_csv(path + 'temp_data/SPC_Target.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))

files = glob.glob(path + 'Zetta_Product/*.txt')
lists=[]
for file in files:
    lists.append(file.replace(path + 'Zetta_Product',''))

n=len(lists)

h_order={'Subsidiary Code':0,'Product Code':1,'slide_no':2, 'qty':3, 'sales':4, 'purchase':5, 'production':6, 'days_ts':7, 'rt_s':8, 'rt_p':9}  # Header並び順
zetta_slide = pd.DataFrame(columns=h_order)   # スライド出力用
# zetta_data1を00_Header.pyで並び順を変更
#zetta_data1 = Header.Header()    # ALLデータ出力用
zetta_data1 = pd.DataFrame([],columns=Header.Header())    # ALLデータ出力用 こっちの記述でも出来ました。何となくしっくりくるのでこちらで。

for l in range(0, n):
    zetta = (pd.read_csv(path + 'Zetta_Product/' + lists[l],sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    zetta_data = pd.merge(zetta, spc_product, on=['Subsidiary Code', 'Product Code'])  # 立上データの現法コードと型式が一致する現法データ

    zetta_data1 = zetta_data1.append(zetta_data,sort=False)

    for i in range(1, 11):
        i = str(i)
        zetta_data2 = (zetta_data[['Subsidiary Code', 'Product Code', 'Slide Qty ' + i, 'Slide Sales Pc/Unit ' + i, 'Slide Purchase Pc/Unit ' + i,
                                   'Slide Production LT ' + i, 'Slide Days TS ' + i, 'Alt Dsct Rt:S ' + i, 'Alt Dsct Rt:P ' + i]])
# 列見出し変更（統一） カラム名並びは「h_order」にて解消
        zetta_data3 = (zetta_data2.rename(columns={'slide_no':'slide_no','Slide Qty ' + i: 'qty',
                                                   'Slide Sales Pc/Unit ' + i: 'sales','Slide Purchase Pc/Unit ' + i: 'purchase',
                                                   'Slide Production LT ' + i: 'production','Slide Days TS ' + i: 'days_ts', 'Alt Dsct Rt:S ' + i: 'rt_s','Alt Dsct Rt:P ' + i: 'rt_p'}))
        zetta_data3['slide_no'] = i
        zetta_slide = zetta_slide.append(zetta_data3,sort=False)

# 「temp_data」フォルダに作成
zetta_slide.drop_duplicates(subset=['Product Code','qty', 'Subsidiary Code'],keep='first',inplace=True) # 型式・現法コード・数量の重複データ削除　先頭行残す
zetta_slide = (zetta_slide.query('qty > "0"'))  # 数量スライド>0で抽出
zetta_slide.to_csv(path + 'temp_data/Zetta_Slide.txt', sep='\t', encoding='utf_16', index=False)    # Zetta_Slide.txt スライドデータのみ出力

zetta_data1.drop(columns=['分析コード','立上日','仕入先'],inplace=True)    #不要な列を削除
zetta_data1.to_csv(path + 'temp_data/Zetta_Product.txt', sep='\t', encoding='utf_16', index=False)  # Zetta_Product.txt　ALL出力
print('Fin')
