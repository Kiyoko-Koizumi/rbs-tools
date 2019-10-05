# SPC Product SlideデータとMaster抽出　★★　製作日数・カタログ納期（スライド含む）をSPCデータを抽出しているが、現法に変更の可能性有　★★
import glob
import pandas as pd
import numpy as np
import Header
import datetime

path='//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/'
print(datetime.datetime.now())
# SPC_Product.txt」データ読み込み
spc_product = (pd.read_csv(path + 'temp_data/SPC_Target.txt', sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
days_ts = (pd.read_excel(path + 'temp_master/Days_Ts.xlsx'))    # 製作日数・カタログ納期・当日受注締時刻

# フォルダからtxtファイル名抽出　フルパス
files = glob.glob(path + 'SPC_Master/PRODUCT/*.txt')
lists = []
for file in files:
    # 　フルパスからファイル名のみ抽出
    lists.append(file.replace(path + 'SPC_Master/PRODUCT', ''))
n=len(lists)

h_order=({'Subsidiary Code': 0, 'Product Code': 1, 'Unit Price Check': 2, 'min_order': 3, 'max_order': 4,
          'spc_slide_no': 5, 'qty': 6, 'production': 7, 'days_ts': 8, 'purchase': 9, 'rt_p': 10, 'l_rt_p': 11, 'l_days': 12, 'data': 13})  # スライドHeader並び順
spc_slide = pd.DataFrame(columns=h_order)   # スライド出力用
spc_data1 = pd.DataFrame([], columns=Header.Header())    # ALLデータ出力用

for l in range(0, n):
    spc = (pd.read_csv(path + 'SPC_Master/PRODUCT/' + lists[l], sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    spc_data = pd.merge(spc, spc_product, on=['Product Code'])  # 立上データの現法コードと型式が一致する現法データ
    spc_data1 = spc_data1.append(spc_data)

    for i in range(1, 11):
        i = str(i)
        spc_data2 = (spc_data[['Subsidiary Code_y', 'Product Code', 'Unit Price Check', 'Min Qty of Big Order', 'Max Qty of Big Order', 'Slide Qty ' + i, 'Slide Purchase Pc/Unit ' + i,
                               'Slide Production LT ' + i, 'Slide Days TS ' + i, 'Alt Dsct Rt:P ' + i, 'Express L Dsct Rt:P ' + i, 'Express L Slide Days ' + i]])
        # 列見出し変更（統一） カラム名並びは「h_order」にて解消
        # Subsidiary Code_yは立上データの現法コード
        spc_data3 = (spc_data2.rename(columns={'Subsidiary Code_y': 'Subsidiary Code', 'Min Qty of Big Order': 'min_order', 'Max Qty of Big Order': 'max_order', 'slide_no': 'spc_slide_no',
                                               'Slide Qty ' + i: 'qty', 'Slide Purchase Pc/Unit ' + i: 'purchase',
                                               'Slide Production LT ' + i: 'production', 'Slide Days TS ' + i: 'days_ts', 'Alt Dsct Rt:P ' + i: 'rt_p',
                                               'Express L Dsct Rt:P ' + i: 'l_rt_p', 'Express L Slide Days ' + i: 'l_days'}))
        spc_data3['l_rt_p'] = 0
        spc_data3['l_days'] = 0
        spc_data3['spc_slide_no'] = i
        spc_data3['data'] = 'spc'
        spc_slide = spc_slide.append(spc_data3, sort=False)  # sort=Falseでアラートが消える

# 「temp_data」フォルダに作成
spc_slide.drop_duplicates(subset=['Product Code', 'qty', 'Subsidiary Code'], keep='first', inplace=True) # 型式・数量の重複データ削除　先頭行残す
spc_slide = (spc_slide.query('qty > "0"'))  # 数量スライド>0で抽出

# Days_Ts.xlsx結合 製作日数・カタログ納期更新
# 1Rec単位で更新をしたがRec数が増えたら遅いので変更
spc_slide = pd.merge(spc_slide, days_ts, on=['Subsidiary Code'])

spc_slide['qty'] = spc_slide['qty'].astype(int)
spc_slide['max_order'] = spc_slide['max_order'].astype(int)
spc_slide['production'] = spc_slide['production'].astype(int)
spc_slide['DaysTS'] = spc_slide['DaysTS'].astype(int)

# 数量>=大口上限数量 製作日数・カタログ納期を「99」にする　カタログ納期は下記①で処理される
spc_slide.loc[(spc_slide.qty >= spc_slide.max_order), 'production'] = 99
spc_slide.loc[(spc_slide.qty >= spc_slide.max_order), 'days_ts'] = 99

spc_slide['c'] = spc_slide['production'] - spc_slide['DaysTS']  # C＝製作日数―輸出日数
spc_slide['d'] = spc_slide['production'] + spc_slide['DaysTS']  # d＝製作日数＋輸出日数
spc_slide['a'] = spc_slide['production']    # a＝製作日数
spc_slide['c'] = spc_slide['c'].astype(int)
spc_slide['d'] = spc_slide['d'].astype(int)
data = spc_slide.copy()

# ①カタログ納期
data.loc[(data.d > 0) & (data.d < 99), 'days_ts'] = data['d']
data.loc[(data.d > 99), 'days_ts'] = 99
data.loc[(data.a == 0) | (data.a == 99), 'days_ts'] = data['production']

# ②製作日数
data.loc[(data.production == 99), 'production'] = data['c']
data.loc[(data.production != 99), 'production'] = data['production']

# 1Rec単位で書いたが・・・・ちょぉ～遅い！！！
#df2 = pd.DataFrame()
#n = len(spc_slide)
#for i in range(0, n):
#    df = spc_slide.loc[[i]]
#    df['production'] = df['production'].astype(int)
#    df['DaysTS'] = df['DaysTS'].astype(int)
#    a = np.array(df['production'])  # 製作日数
#    b = np.array(df['DaysTS'])  # Days_Ts.xlsxの輸送日数
#    c = a - b   # 製作日数用　製作日数-輸送日数
#    d = a + b   # カタログ納期用　製作日数+輸送日数
    # 製作日数＝製作日数が99の時、製作日数-[DaysTS](輸送日数)、それ以外は製作日数
#    if a == 99:
#        df['production'] = c
#    else:
#        df['production'] = a
    # カタログ納期＝製作日数が0 Or 99の時、製作日数、 製作日数+[Days_TS](輸送日数)>99の時、99、それ以外は製作日数+[Days_TS](輸送日数)
#    if a == 0 or a == 99:
#        df['days_ts'] = a
#    elif d > 0 and d < 99:
#        df['days_ts'] = d
#    elif d > 99:
#        df['days_ts'] = 99
#    df2 = df2.append(df, sort=False)
data.drop(columns=['c', 'd', 'a'], inplace=True)    # 不要な列を削除
# data.loc[:, 'h_order']
data.to_csv(path + 'temp_data/SPC_Slide.txt', sep='\t', encoding='utf_16', index=False)    # SPC_Slide.txt スライドデータのみ出力

spc_data1 = spc_data1.rename(columns={'Subsidiary Code_x': 'Subsidiary Code'})
spc_data1.drop(columns=['分析コード', '立上日', '仕入先', 'Subsidiary Code_y'], inplace=True)    # 不要な列を削除
spc_data1.drop_duplicates(subset=['Product Code'], keep='first', inplace=True)  # 型式の重複データ削除　先頭行残す
spc_data1.to_csv(path + 'temp_data/SPC_Product.txt', sep='\t', encoding='utf_16', index=False)  # SPC_Product.txt　ALL出力

print('Fin')
print(datetime.datetime.now())