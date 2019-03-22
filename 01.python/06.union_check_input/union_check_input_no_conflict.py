#0.2 ファイル選択ダイアログの追加と、それに伴うファイル読み込みソースの変更
# git向けにファイル名変更
# M単毀損を削除

##pandasを呼び出す
import pandas as pd
import os
import sys
import csv

csv.field_size_limit(1000000000)

# カレントディレクトリを変更
os.chdir("/data/rbs/mps/割振り処理期間データ抽出/input")

#複数ファイル選択
list_f=os.listdir("/data/rbs/mps/割振り処理期間データ抽出/input")

l_name=[]
for r in range(0,len(list_f)):
    l=os.path.basename(list_f[r])
    l_name.append(l)


#
#フォルダ内の取得対象ファイルをリスト型変数で取得する
#glob_files=glob.glob(file_pass)
#list=[]
#リスト型で渡されたファイル名をすべてマージする
#for f in glob_files:
#    list.append(pd.read_excel(f,dtype='object'))
list=[]
for f in range(len(l_name)):
    list.append(pd.read_csv(l_name[f],delimiter='\t', encoding='utf-8', dtype='object', index_col=None))
    #dtype='object'
    #low_memory=False
#ヘッダーの順番が変わってしまうので、戻す
df=list[0]
header=df.columns
df=pd.concat(list,sort=False)
df.loc[:,header]
#df.ix[:,header]


#tsvを読み込む
#df = pd.read_table(glob_a)
#print(df.columns)


#大口ｄｆと受注ｄｆを作る
args=sys.argv
test=df.fillna({'見積回答SSD':0,'顧客希望納期':0})
df=test.astype({'見積回答SSD':int,'顧客希望納期':int})
x=args[1]+' < 見積回答SSD <'+args[2]
y=args[1]+' < 顧客希望納期 <'+ args[2]
omd=df.query(x)
df_omd=omd[['グローバル番号']]
df_omd=df_omd[~df_omd.duplicated(subset='グローバル番号')]
df_omd.reset_index(inplace=True,drop=True)
df_omd.reset_index(inplace=True)
df_omd=df_omd.rename(columns={'index':'番号'})
omd.drop('番号',axis=1,inplace=True)
omd=pd.merge(df_omd,omd,on='グローバル番号',how='left')
l=len(df_omd)
print(l)
sod=df.query(y)
df_sod=sod[['番号','グローバル番号']]
df_sod=df_sod[~df_sod.duplicated(subset='グローバル番号')]
df_sod=df_omd.append(df_sod)

df_sod.reset_index(inplace=True,drop=True)
df_sod=df_sod[l:]
df_sod.drop('番号',axis=1,inplace=True)
df_sod.reset_index(inplace=True)
df_sod=df_sod.rename(columns={'index':'番号'})

sod.drop('番号',axis=1,inplace=True)
sod=pd.merge(df_sod,sod,on='グローバル番号',how='left')

#結合する
data=pd.concat([omd,sod])
data = data.loc[:,header]

#MC_CDの”NA”が消えてしまうので、NAを書き込む
#https://note.nkmk.me/python-pandas-where-mask/
data.loc[data['グローバル番号'].str[:2] == "NA",'ＭＣコード']="NA"

#実績仕入先コードにあるFCNT・FCNXを0FCNに変換する
#http://sinhrks.hatenablog.com/entry/2014/11/15/230705
data.loc[data['実績仕入先コード'].isin(["FCNT","FCNX"]),'実績仕入先コード']="0FCN"

# M単毀損なし
jri_cost = data[data['従来生産拠点フラグ'] == '1']
jri_cost = jri_cost.rename(columns={'発注現法仕入値': '従来拠点着荷コスト'})
jri_cost = jri_cost.loc[::, ['番号', '従来拠点着荷コスト']]
data = pd.merge(data, jri_cost, on='番号', how='left')
# M単毀損行を削除 nullの場合は見積りデータなので残す
data = data[((data['発注現法仕入値'] <= data['従来拠点着荷コスト']) | data['従来拠点着荷コスト'].isnull())]
data.drop(['従来拠点着荷コスト'], axis=1, inplace=True)

# 受注日時順に並べ替え
data.reset_index(inplace=True,drop=True)
data = data.sort_values(['JST変換受注日・JST変換見積回答日', 'JST変換受注時間・JST変換見積回答時間', '番号'])

os.chdir("/data/rbs/mps/割振り処理期間データ抽出/output")
#アウトプット

data.to_csv("check_input.tsv",sep="\t",index=False)

print('finish!')
