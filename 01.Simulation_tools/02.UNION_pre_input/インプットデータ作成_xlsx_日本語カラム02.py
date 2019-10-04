#0.2 ファイル選択ダイアログの追加と、それに伴うファイル読み込みソースの変更


##pandasを呼び出す
import pandas as pd
import glob
import os
import openpyxl
import tkinter.messagebox
import tkinter.filedialog


#https://qiita.com/chanmaru/items/1b64aa91dcd45ad91540
#ファイル選択ダイアログの表示
root = tkinter.Tk()
root.withdraw()
# xlslのみ表示に限定
fTyp = [('','xlsx')]
iDir = os.path.abspath(os.path.dirname(__file__))
tkinter.messagebox.showinfo('準備処理input','ファイルを選択してください！')
#複数ファイル選択
file_pass = tkinter.filedialog.askopenfilenames(filetypes = fTyp,initialdir = iDir)
list_f=list(file_pass)

l_name=[]
for r in range(0,len(list_f)):
    l=os.path.basename(list_f[r])
    l_name.append(l)
    print(l_name)

f_pass = os.path.dirname(file_pass[0])

# カレントディレクトリを変更
os.chdir(f_pass)

tkinter.messagebox.showinfo('以下のファイルを読み込みました',l_name)


#pass1=os.path.join("C:","Users","Mayumi_Hosoda","OneDrive - 株式会社ミスミグループ本社","OneDrive-PC","python","テストファイル")
#print(pass1)
#A=os.getcwd()
#print(A)

#
#フォルダ内の取得対象ファイルをリスト型変数で取得する
#glob_files=glob.glob(file_pass)
#list=[]
#リスト型で渡されたファイル名をすべてマージする
#for f in glob_files:
#    list.append(pd.read_excel(f,dtype='object'))
list=[]
for f in range(len(l_name)):
    list.append(pd.read_excel(l_name[f],dtype='object'))
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
test=df.fillna({'見積回答SSD':0,'顧客希望納期':0})
df=test.astype({'見積回答SSD':int,'顧客希望納期':int})
omd=df.query('20180601 < 見積回答SSD < 20180631')
sod=df.query('20180601 < 顧客希望納期 < 20180631')
#結合する
date=pd.concat([omd,sod])


#NO列に連番をふる
#https://note.nkmk.me/python-pandas-at-iat-loc-iloc/
output=date.astype({'番号':int})
i=0
for A in output['番号']:
    output.iat[i,0]=i
    i=i+1

#MC_CDの”NA”が消えてしまうので、NAを書き込む
#https://note.nkmk.me/python-pandas-where-mask/
output.loc[output['グローバル番号'].str[:2] == "NA",'ＭＣコード']="NA"

#実績仕入先コードにあるFCNT・FCNXを0FCNに変換する
#http://sinhrks.hatenablog.com/entry/2014/11/15/230705
output.loc[output['実績仕入先コード'].isin(["FCNT","FCNX"]),'実績仕入先コード']="0FCN"
    


#アウトプット
import openpyxl
output.to_excel("input.xlsx",index=False)

print('finish!')
      
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
