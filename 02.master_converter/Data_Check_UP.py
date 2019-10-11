
# ★★　単価マスターのみ　ヘッダが一致・Innerが一致するもののみを対象にしてください！！　★★
import pandas as pd
import numpy as np
import csv
import Type_U
import datetime
print(datetime.datetime.now())

# ★★　チェックするファイルを保存するフォルダを下記に指定してください！！　★★
# ★★　必ず同じフォルダに保存してください！！ フォルダの「\」は「/」にしてください！！　★★
path = '//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/Data_Check/'

# ★★　基準となるtxtファイル名を変えてください！！　↓（緑色のここ）　★★
b = pd.DataFrame(pd.read_csv(path + 'USA_U_Product.txt',sep='\t', encoding='utf_16', dtype=str, engine='python', error_bad_lines=False))
# ★★　チェック対象となるtxtファイル名を変えてください！！　↓（緑色のここ）　★★
a = pd.DataFrame(pd.read_excel(path + '03722108_USA_UnitPrice.xlsx', sheet_name='UnitPrice①', dtype=str))    # 文字列で読み込み
#b = pd.DataFrame(pd.read_csv(path + '03722108_USA_UnitPrice.txt', sep='\t', encoding='utf_16', dtype=str, engine='python', error_bad_lines=False))

a = a.sort_values(by='Inner Code')
b = b.sort_values(by='Inner Code')

a = a.astype(Type_U.type())   # データ型をそろえる
a = a.fillna('')
a.to_csv(path + 'A_product.txt', sep='\t', encoding='utf_16', index=False)

b = b.astype(Type_U.type())   # データ型をそろえる
b = b.fillna('')
b.to_csv(path + 'B_product.txt', sep='\t', encoding='utf_16', index=False)

dictB ={}
h = []
with open(path + 'A_product.txt', encoding='utf_16') as fileB:
        reader = csv.reader(fileB, delimiter='\t')
        reader = csv.reader((line.replace('\0','') for line in fileB))
        for row in reader:
            for sel in row:
                dictB[sel] = True

df = pd.DataFrame()
df2 = pd.DataFrame()
df3 = pd.DataFrame()
with open(path + 'B_product.txt', encoding='utf_16') as fileA:
    reader = csv.reader(fileA, delimiter='\t')
    reader = csv.reader((line.replace('\0', '') for line in fileA))
    for row in reader:
        for sel in row:
            if sel not in dictB:
                df = df.append(pd.Series(sel.split('\t')), ignore_index=True, sort=False)

df = df[df[2] != 'XXX']
if len(df) == 0:
    print('Congratulations!')   # 不一致がない！！
else:
    df2 = df2.append(df[[3]], sort=False)
    df2 = df2.rename(columns={3: 'Inner Code'})
    a = pd.DataFrame(pd.read_csv(path + 'A_product.txt',sep='\t', encoding='utf_16', dtype=str, engine='python', error_bad_lines=False))
    b = pd.DataFrame(pd.read_csv(path + 'B_product.txt',sep='\t', encoding='utf_16', dtype=str, engine='python', error_bad_lines=False))
    a['data'] = 'A'
    b['data'] = 'B'
    a = pd.merge(df2, a, how='inner')
    b = pd.merge(df2, b, how='inner')
    df3 = df3.append(a, sort=False)
    df3 = df3.append(b, sort=False)

    df3.drop_duplicates(subset=['Inner Code', 'Product Code', 'Min.Val.1', 'data'], keep='first', inplace=True)  # 重複削除
    df3 = df3.sort_values(by=['Inner Code', 'Min.Val.1', 'data'])

    # ★★　出力するExcelファイル名を変えてください！！（緑色の部分）　★★
    # ★★　不一致が多いとエラーの可能性あり　4G超え　★★
    df3.to_excel(path + 'spc_usa_check3.xlsx', index=False)

print(datetime.datetime.now())
print('fin')