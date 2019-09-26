# Access作成ファイルとPython作成ファイルのチェック
import pandas as pd
import numpy as np
import datetime

path='//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/Data_Check/'

#ac = pd.DataFrame(pd.read_csv(path + 'Product_Master_GRMプーリFCN_ECAL.txt',sep='\t', encoding='utf_16', dtype=str, engine='python', error_bad_lines=False))   # 文字列で読み込み
#py = pd.DataFrame(pd.read_csv(path + 'FCN_to_ECAL_GRM03622710_Productmst_hou.txt',sep='\t', encoding='utf_16', dtype=str, engine='python', error_bad_lines=False))   # 文字列で読み込み
ac = pd.DataFrame(pd.read_excel(path + 'Zetta_USA_Product.xlsx', sheet_name='Product', dtype=str))    # 文字列で読み込み
py = pd.DataFrame(pd.read_excel(path + 'SPC_USA_Product.xlsx', sheet_name='Product', dtype=str))    # 文字列で読み込み
print(datetime.datetime.now())
c = (len(ac.columns))   # 基準とするデータのカラム数カウント
ac = ac.fillna('') # nanを空白に変換
py = py.fillna('') # nanを空白に変換
ac = ac.sort_values(by='Inner Code')
py = py.sort_values(by='Inner Code')
ac_list = []
py_list = []
ac_list = ac
py_list = py
non_list = []
non_list =(ac_list != py_list)
print(non_list)
#df = pd.DataFrame()
#df = ac == py
#df.to_csv(path + 'test.csv',sep='\t', encoding='utf_16', index=False)  # 検証用
#df['check'] = np.sum(ac == py)
#print(df['check'])
print(datetime.datetime.now())

inner = pd.DataFrame(ac['Inner Code'])

l = len(inner)
h = list(ac.columns)
h.append('data')

df = pd.DataFrame([], columns=h)
df['data'] = ''
dfi = pd.DataFrame([])

for i in range(1, l):
    dfi = inner.loc[[i]]
    a = np.array(dfi['Inner Code'])
    acd = np.array(ac.loc[ac['Inner Code'] == a[0]])
    pyd = np.array(py.loc[py['Inner Code'] == a[0]])
    col = (acd == pyd)
    if np.sum(col) < c: # true=1 false=0 sumをとるとカラム数より小さい＝falseがある
        #print((col == False).sum())
        ac['data'] = 'maru'
        df = df.append(ac.loc[ac['Inner Code'] == a[0]], sort=False)
        py['data'] = 'how'
        df = df.append(py.loc[py['Inner Code'] == a[0]], sort=False)
    print(i)
df = df.loc[:, h]
df.to_excel(path + 'fcn_ecal_check.xlsx', index=False)  # 検証用
print(datetime.datetime.now())
print('fin')