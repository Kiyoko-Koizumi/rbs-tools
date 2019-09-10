# Access作成ファイルとPython作成ファイルのチェック
import pandas as pd
import numpy as np
import datetime

path='//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/Data_Check/'

ac = pd.DataFrame(pd.read_excel(path + 'Zetta_USA_Product.xlsx', sheet_name='Product', dtype=str))   # 文字列で読み込み
py = pd.DataFrame(pd.read_excel(path + 'SPC_USA_Product.xlsx', sheet_name='Product', dtype=str))    # 文字列で読み込み
print(datetime.datetime.now())
c = (len(ac.columns))   # 基準とするデータのカラム数カウント
ac = ac.fillna('') # nanを空白に変換
py = py.fillna('') # nanを空白に変換

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
        ac['data'] = 'new'
        df = df.append(ac.loc[ac['Inner Code'] == a[0]], sort=False)
        py['data'] = 'old'
        df = df.append(py.loc[py['Inner Code'] == a[0]], sort=False)
    print(i)
df = df.loc[:, h]
df.to_excel(path + 'test_check.xlsx', index=False)  # 検証用
print(datetime.datetime.now())
print('fin')