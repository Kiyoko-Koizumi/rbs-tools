
##pandasを呼び出す
import pandas as pd

#
#import os
#pass1=os.path.join("C:","Users","Mayumi_Hosoda","OneDrive - 株式会社ミスミグループ本社","OneDrive-PC","python","テストファイル")
#print(pass1)
#A=os.getcwd()
#print(A)

#フォルダ内の取得対象ファイルをリスト型変数で取得する
import glob
glob_files=glob.glob("*.xlsx")
list=[]


#リスト型で渡されたファイル名をすべてマージする
for f in glob_files:
    list.append(pd.read_excel(f,dtype='object'))
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
test=df.fillna({'QT_SSD':0,'SHIPPING_FIXED_DATE':0})
df=test.astype({'QT_SSD':int,'SHIPPING_FIXED_DATE':int})
omd=df.query('20180320 < QT_SSD < 20180510')
sod=df.query('20180320 < SHIPPING_FIXED_DATE < 20180510 ')
#結合する
date=pd.concat([omd,sod])


#NO列に連番をふる
#https://note.nkmk.me/python-pandas-at-iat-loc-iloc/
output=date.astype({'NO':int})
i=0
for A in output['NO']:
    output.iat[i,0]=i
    i=i+1

    
#MC_CDの”NA”が消えてしまうので、NAを書き込む
#https://note.nkmk.me/python-pandas-where-mask/
output.loc[output['GLOBAL_NO'].str[:2] == "NA",'MC_CD']="NA"

#実績仕入先コードにあるFCNT・FCNXを0FCNに変換する
#http://sinhrks.hatenablog.com/entry/2014/11/15/230705
output.loc[output['RESULTS_SUPPLIER_CD'].isin(["FCNT","FCNX"]),'RESULTS_SUPPLIER_CD']="0FCN"
    


#アウトプット
import openpyxl
output.to_excel("input.xlsx",index=False)


#文字コードをutf-8にする
#import codecs
#def main():
#    shiftjis_tsv_path="対象インプットデータ.tsv"
#    utf8_tsv_path ="対象インプットデータuft8.tsv"

#fin = codecs.open("対象インプットデータ.tsv", "r", "shift_jis")
#fout_utf = codecs.open("対象インプットデータuft8.tsv", "w", "utf-8")
#for row in fin:
#        fout_utf.write(row)
#fin.close()
#fout_utf.close()

#http://blog.pyq.jp/entry/Python_kaiketsu_180207
#if __name__ == '__main__':
#    main()
