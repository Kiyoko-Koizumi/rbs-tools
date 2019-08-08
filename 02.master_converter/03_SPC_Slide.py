# SPC Product SlideデータとMaster抽出
import glob
import pandas as pd
import Header

path='//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/'

# SPC_Product.txt」データ読み込み
spc_product = (pd.read_csv(path + 'temp_data/SPC_Target.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))

# フォルダからtxtファイル名抽出　フルパス
files = glob.glob(path + 'SPC_Master/PRODUCT/*.txt')
lists=[]
for file in files:
    # 　フルパスからファイル名のみ抽出
    lists.append(file.replace(path + 'SPC_Master/PRODUCT',''))
n=len(lists)

h_order={'Subsidiary Code':0,'Product Code':1,'spc_slide_no':2, 'qty':3,'purchase':4, 'rt_p':5,'l_rt_p':6,'l_days':7,'data':8}  # スライドHeader並び順
spc_slide = pd.DataFrame(columns=h_order)   # スライド出力用
spc_data1=pd.DataFrame([],columns=Header.Header())    # ALLデータ出力用

for l in range(0, n):
    spc = (pd.read_csv(path + 'SPC_Master/PRODUCT/' + lists[l],sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    spc_data = pd.merge(spc, spc_product, on=['Product Code'])  # 立上データの現法コードと型式が一致する現法データ
    spc_data1=spc_data1.append(spc_data)

    for i in range(1, 11):
        i = str(i)
        spc_data2 = (spc_data[['Subsidiary Code_y','Product Code', 'Slide Qty ' + i, 'Slide Purchase Pc/Unit ' + i,
                               'Alt Dsct Rt:P ' + i,'Express L Dsct Rt:P ' + i, 'Express L Slide Days ' + i]])
        # 列見出し変更（統一） カラム名並びは「h_order」にて解消
        # Subsidiary Code_yは立上データの現法コード
        spc_data3 = (spc_data2.rename(columns={'Subsidiary Code_y':'Subsidiary Code','slide_no':'spc_slide_no','Slide Qty ' + i: 'qty','Slide Purchase Pc/Unit ' + i: 'purchase',
                                               'Alt Dsct Rt:P ' + i: 'rt_p','Express L Dsct Rt:P ' + i:'l_rt_p', 'Express L Slide Days ' + i:'l_days'}))
        spc_data3['spc_slide_no'] = i
        spc_data3['data'] = 'spc'
        spc_slide = spc_slide.append(spc_data3,sort=False)  # sort=Falseでアラートが消える

# 「temp_data」フォルダに作成
spc_slide.drop_duplicates(subset=['Product Code', 'qty', 'Subsidiary Code'],keep='first',inplace=True) # 型式・数量の重複データ削除　先頭行残す
spc_slide = (spc_slide.query('qty > "0"'))  # 数量スライド>0で抽出
spc_slide.to_csv(path + 'temp_data/SPC_Slide.txt', sep='\t', encoding='utf_16', index=False)    # SPC_Slide.txt スライドデータのみ出力

spc_data1.drop(columns=['分析コード','立上日','仕入先','Subsidiary Code_y'],inplace=True)    #不要な列を削除
spc_data1.drop_duplicates(subset=['Product Code'],keep='first',inplace=True) # 型式の重複データ削除　先頭行残す
spc_data1.to_csv(path + 'temp_data/SPC_Product.txt', sep='\t', encoding='utf_16', index=False)  # SPC_Product.txt　ALL出力

print('Fin')
