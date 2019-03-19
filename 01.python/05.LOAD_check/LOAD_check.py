# coding: utf-8
# Orders prediction 新規作成 2019/2/15

# モジュールのインポート
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import csv
import pandas as pd
import datetime as dt
import workdays
import numpy as np

# from tqdm import tqdm
csv.field_size_limit(1000000000)

font = 'utf-8'
# font='shift_jisx0213'

# スクリプトのあるディレクトリの絶対パスを取得
script_pass = os.path.dirname(os.path.abspath(__name__))

# ファイル選択ダイアログの表示
root = tkinter.Tk()
root.withdraw()
fTyp = [("","*")]
iDir = os.path.abspath(os.path.dirname(__file__))

rfile=0
r=0

# 受注実績データの取得
# ここの1行を変更 askopenfilename → askopenfilenames
file = tkinter.filedialog.askopenfilenames(filetypes = fTyp,initialdir = iDir)

# 選択ファイルリスト作成
list_f = list(file)
# tkinter.messagebox.showinfo('UNIONプログラム',list_f)

# 1つ目のファイルを開く
f_name=os.path.basename(list_f[0])
f_pass=os.path.dirname(list_f[0])
os.chdir(f_pass)

# 必要な列のみ読み込む
load = pd.read_table(f_name, encoding=font, dtype=object, engine='python', error_bad_lines=False, usecols=['JST変換受注日・JST変換見積回答日', '仕入先コード', '生産予定日', '負荷評価判定結果'])
load.drop_duplicates(subset=['JST変換受注日・JST変換見積回答日', '仕入先コード', '生産予定日'], keep='first', inplace=True)


# ファイルを繰り返し開き結合する
for r in range(1,len(list_f)):
    f_name=os.path.basename(list_f[r])
    print(f_name)
    load_add = pd.read_table(f_name, encoding=font, dtype=object, engine='python', error_bad_lines=False, usecols=['JST変換受注日・JST変換見積回答日', '仕入先コード', '生産予定日', '負荷評価判定結果'])
    load_add.drop_duplicates(subset=['JST変換受注日・JST変換見積回答日', '仕入先コード', '生産予定日'], keep='first', inplace=True)
    #ファイルを追加する
    load=load.append(load_add)

# 負荷評価判定結果を末尾一桁にしSは4とする
load['負荷評価判定結果'] = load['負荷評価判定結果'].str[-1:]
load.loc[load['負荷評価判定結果'] == 'S', '負荷評価判定結果'] = '4'

# 生産予定日をN+係数にする
# JST変換受注日・JST変換見積回答日、生産予定日をdate形式へ変更
load = load.astype({'JST変換受注日・JST変換見積回答日': str, '生産予定日': str})
load['JST変換受注日・JST変換見積回答日'] = load['JST変換受注日・JST変換見積回答日'].str[0:4] + '-' + load['JST変換受注日・JST変換見積回答日'].str[4:6] + '-' + load['JST変換受注日・JST変換見積回答日'].str[6:8]
load['生産予定日'] = load['生産予定日'].str[0:4] + '-' + load['生産予定日'].str[4:6] + '-' + load['生産予定日'].str[6:8]

load['JST変換受注日・JST変換見積回答日'] = pd.to_datetime(load['JST変換受注日・JST変換見積回答日'])
load['生産予定日'] = pd.to_datetime(load['生産予定日'])

# 受注日と生産予定日の差分からN+係数を作成
load['生産予定日'] = [(x - y).days for x,y in zip(load['生産予定日'], load['JST変換受注日・JST変換見積回答日'])]

# 仕入先、受注日、生産予定日をindex化し生産予定日をheaderにする
load = load.set_index(['仕入先コード', 'JST変換受注日・JST変換見積回答日', '生産予定日'])
load = load.unstack()

# ファイルアウトプット
load.to_csv('LOAD_check.tsv', sep='\t', encoding=font, quotechar='"', line_terminator='\n', index=True)

print('Finish!')
