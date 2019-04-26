#0.2 ファイル選択ダイアログの追加と、それに伴うファイル読み込みソースの変更
# git向けにファイル名変更
# M単毀損を削除
# M単毀損削除条件を修正
# UFなしやランダムにREC抽出しグローバル番号が重複に対応

##pandasを呼び出す
import pandas as pd
import os
import sys
import csv

csv.field_size_limit(1000000000)

# カレントディレクトリを変更
os.chdir("/data/rbs/mps/012.warifuri_kikan/input")

#複数ファイル選択
list_f=os.listdir("/data/rbs/mps/012.warifuri_kikan/input")

l_name=[]
for r in range(0,len(list_f)):
    l=os.path.basename(list_f[r])
    l_name.append(l)

#フォルダ内の取得対象ファイルをリスト型変数で取得する
list=[]
for f in range(len(l_name)):
    list.append(pd.read_csv(l_name[f],delimiter='\t', encoding='utf-8', dtype='object', index_col=None))
#ヘッダーの順番が変わってしまうので、戻す
df=list[0]
header=df.columns
df=pd.concat(list,sort=False)
df.loc[:,header]

#大口ｄｆと受注ｄｆを作る
args=sys.argv
test=df.fillna({'見積回答SSD':0,'顧客希望納期':0})
df=test.astype({'見積回答SSD':int,'顧客希望納期':int})
y=args[1]+' <= 顧客希望納期 <='+ args[2]
data=df.query(y)

#MC_CDの”NA”が消えてしまうので、NAを書き込む
#https://note.nkmk.me/python-pandas-where-mask/
data.loc[data['グローバル番号'].str[:2] == "NA",'ＭＣコード']="NA"

#実績仕入先コードにあるFCNT・FCNXを0FCNに変換する
#http://sinhrks.hatenablog.com/entry/2014/11/15/230705
data.loc[data['実績仕入先コード'].isin(["FCNT","FCNX"]),'実績仕入先コード']="0FCN"

# M単毀損なし
# 発注現法仕入値をfloatへ
data=data.astype({'発注現法仕入値':float})
jri_cost = data[data['従来生産拠点フラグ'] == '1']
jri_cost = jri_cost.rename(columns={'発注現法仕入値': '従来拠点着荷コスト'})
jri_cost = jri_cost.loc[:, ['番号', '顧客希望納期', '従来拠点着荷コスト']]
# 新番号を付与
jri_cost.reset_index(inplace=True, drop=True)
jri_cost.reset_index(inplace=True, drop=False)
jri_cost = jri_cost.rename(columns={'index': '新番号'})
data = pd.merge(data, jri_cost, on=['番号', '顧客希望納期'], how='left')
data['番号'] = data['新番号']
# M単毀損行を削除 nullの場合は見積りデータなので残す
data = data[((data['発注現法仕入値'] <= data['従来拠点着荷コスト']) | data['従来拠点着荷コスト'].isnull())]
data.drop(['新番号', '従来拠点着荷コスト'], axis=1, inplace=True)
data = data.round({'発注現法仕入値': 3})

# R.B.S対象3764,0FCN,SPCM,MJP
# MJPは残し、それ以外の現法は従来データのみ残す
data = data[((data['現法コード'] == 'MJP') | (data['従来生産拠点フラグ'] == '1') | (data['見積有効日'].notnull()))]
# 従来がどこか出す
jri_cost = data[data['従来生産拠点フラグ'] == '1']
jri_cost = jri_cost.rename(columns={'RBS_受注現法仕入先コード': '従来拠点'})
jri_cost = jri_cost.loc[::, ['番号', '従来拠点']]
data = pd.merge(data, jri_cost, on='番号', how='left')
# 従来が3764,0FCN、SPCMでないR.B.S候補は削除 nullの場合は見積りデータなので残す
data = data[(((data['従来拠点'] == '7017') & (data['RBS_受注現法仕入先コード'] == '7017')) |
             ((data['従来拠点'] == 'SPCM') & ((data['RBS_受注現法仕入先コード'] == '3764') | (data['RBS_受注現法仕入先コード'] == '0FCN') | (data['RBS_受注現法仕入先コード'] == 'SPCM'))) |
             ((data['従来拠点'] == '3764') & ((data['RBS_受注現法仕入先コード'] == '3764') | (data['RBS_受注現法仕入先コード'] == '0FCN') | (data['RBS_受注現法仕入先コード'] == 'SPCM'))) |
             ((data['従来拠点'] == '0FCN') & ((data['RBS_受注現法仕入先コード'] == '3764') | (data['RBS_受注現法仕入先コード'] == '0FCN') | (data['RBS_受注現法仕入先コード'] == 'SPCM'))) |
               data['従来拠点'].isnull())]
data.drop(['従来拠点'], axis=1, inplace=True)

# 受注日時順に並べ替え
data.reset_index(inplace=True,drop=True)
data = data.sort_values(['JST変換受注日・JST変換見積回答日', 'JST変換受注時間・JST変換見積回答時間', '番号'])

os.chdir("/data/rbs/mps/012.warifuri_kikan/output")
#アウトプット

data.to_csv("check_input.tsv",sep="\t",index=False)

print('finish!')
