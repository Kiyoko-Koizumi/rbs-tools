# coding: utf-8
# Alignment 新規作成 2019/10/03
#

# モジュールのインポート
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import csv
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
from multiprocessing import Pool
import multiprocessing as multi
import numpy as np
import glob
import datetime

#結果を取り込むdfを用意
Output = pd.DataFrame()

#内製用のシート取込
files=glob.glob('C:/Users/Aoi_Fujishita/能力調整確認シート/*能力確認B_*.xlsx')#//172.24.81.161/share/F加工企業体/生産計画/共用/FBR資料/能力調整確認シート/*能力確認B_*.xlsx'
for file in files:
    input_file_name = (file)
    #生産能力(実力値)
    original_cap = pd.read_excel(input_file_name ,index_col=[3,4,5] ,
                                 skiprows=[0,1,3,4,6,7,8,9,10,11,12,13,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,31,33,34,35,36,37,38,39,
                                           40,42,43,44,45,46,47,48,49,51,52,53,54,55,56,57,58,60,61,62,63,64,65,66,67,69,70,71,72,73,74,75,76,78,79,
                                           80,81,82,83,84,85,87,88,89,90,91,92,93,94,96,97,98,99,100,101,102,103,105,106,107,108,109,110,111] ,dtype=object)
    #生産能力(投資済)
    original_cap_inv = pd.read_excel(input_file_name ,index_col=[3,4,5] ,
                                 skiprows=[0,1,3,4,5,7,8,9,10,11,12,13,14,16,17,18,19,20,21,22,23,25,26,27,28,29,30,31,32,34,35,36,37,38,39
                                         ,40,41,43,44,45,46,47,48,49,50,52,53,54,55,56,57,58,59,61,62,63,64,65,66,67,68,70,71,72,73,74,75,76,77,79,
                                          80,81,82,83,84,85,86,88,89,90,91,92,93,94,95,97,98,99,100,101,102,103,104,106,107,108,109,110,111] ,dtype=object)
    # 調整後生産能力(実力値)
    adjusted_cap = pd.read_excel(input_file_name ,index_col=[3,4,5] ,
                                 skiprows=[0,1,3,4,5,6,7,8,10,11,12,13,14,15,16,17,19,20,21,22,23,24,25,26,28,29,30,31,32,33,34,35,37,38,39,
                                           40,41,42,43,44,46,47,48,49,50,51,52,53,55,56,57,58,59,60,61,62,64,65,66,67,68,69,70,71,73,74,75,76,77,78,79,
                                           80,82,83,84,85,86,87,88,89,91,92,93,94,95,96,97,98,100,101,102,103,104,105,106,107,109,110,111] ,dtype=object)
    # 調整後生産能力(投資済)
    adjusted_cap_inv = pd.read_excel(input_file_name, index_col=[3, 4, 5],
                                 skiprows=[0,1,
                                           3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,20,21,22,23,24,25,26,27,29,30,31,32,33,34,35,36,38,39,
                                           40,41,42,43,44,45,47,48,49,50,51,52,53,54,56,57,58,59,60,61,62,63,65,66,67,68,69,70,71,72,74,75,76,77,78,79,
                                           80,81,83,84,85,86,87,88,89,90,92,93,94,95,96,97,98,99,101,102,103,104,105,106,107,108,110,111] ,dtype=object)
    #それぞれ不要なカラムを削除
    original_cap.drop(original_cap.columns[[0, 1, 2]], axis=1, inplace = True)
    original_cap_inv.drop(original_cap_inv.columns[[0, 1, 2]], axis=1, inplace=True)
    adjusted_cap.drop(adjusted_cap.columns[[0, 1, 2]], axis=1, inplace=True)
    adjusted_cap_inv.drop(adjusted_cap_inv.columns[[0, 1, 2]], axis=1, inplace=True)

    ds_original_cap = original_cap.stack(dropna=False)
    ds_original_cap_inv = original_cap_inv.stack(dropna=False)
    ds_adjusted_cap = adjusted_cap.stack(dropna=False)
    ds_adjusted_cap_inv = adjusted_cap_inv.stack(dropna=False)

    # まずは生産能力(実力値)
    # 調整前後の比較のためにindexを揃え、カラム名を変える
    cap1 = ds_original_cap.reset_index(level = 2)
    cap1 = cap1.rename(columns={'level_2': '数値名1' , 0: '値1'})

    cap2 = ds_adjusted_cap.reset_index(level = 2)
    cap2 = cap2.rename(columns={'level_2': '数値名2', 0: '値2'})
    #調整前後で一つのデータフレームにする(indexをキーとする)
    CAP = cap2.join(cap1)
    CAP.fillna(0, inplace=True)
    #調整があればその差分を値とする
    CAP['値'] = np.where(CAP['値2'] != 0, CAP['値2']-CAP['値1'],  0)

    #値が０であれば消す=0でないデータを取り出す
    CAP = CAP[CAP['値'] != 0]

    #更新後-...という名前を生産能力(実力値)に変える
    CAP['数値名'] = '生産能力(実力値)'
    #フラグを付ける
    CAP['フラグ'] = 1

    #indexをカラムに戻す
    CAP = CAP.reset_index()
    CAP = CAP.rename(columns={'level_2': '日付 の年、月'}).astype(str)
    CAP['日付 の年、月'] = pd.to_datetime(CAP['日付 の年、月'] + '01', format='%Y/%m/%d')
    CAP['日付 の年、月'] = [x.strftime('%Y{0}%m{1}').format(*'年月') for x in CAP['日付 の年、月']]

    #内製外製を判断する
    CAP['内製'] = '内製'

    #順番を整える
    CAP = CAP.loc[:,['日付 の年、月','製造GR','内製','管理Gr','数値名','値','フラグ']]
    Add_CAP = CAP.copy()
    Add_CAP['数値名'] = '生産能力（実力値）不足分'
    Add_CAP['値'] = (-1)*Add_CAP['値'].astype(int)
    Add_CAP['フラグ'] = ''


    # 続いて生産能力(投資済)
    # 調整前後の比較のためにindexを揃え、カラム名を変える
    cap_inv1 = ds_original_cap_inv.reset_index(level = 2)
    cap_inv1 = cap_inv1.rename(columns={'level_2': '数値名1' , 0: '値1'})

    cap_inv2 = ds_adjusted_cap_inv.reset_index(level = 2)
    cap_inv2 = cap_inv2.rename(columns={'level_2': '数値名2', 0: '値2'})
    # 調整前後で一つのデータフレームにする(indexをキーとする)
    CAP_inv = cap_inv2.join(cap_inv1)
    CAP_inv.fillna(0 ,inplace=True)
    # 調整があればその差分を値とする
    CAP_inv['値'] = np.where(CAP_inv['値2'] != 0, CAP_inv['値2']-CAP_inv['値1'],  0)

    #値が0であれば消す=0でないデータを取り出す
    CAP_inv = CAP_inv[CAP_inv['値'] != 0]

    #更新後-...という名前を生産能力(投資済)に変える
    CAP_inv['数値名'] = '生産能力(投資済)'
    #フラグを付ける
    CAP_inv['フラグ'] = 1

    #indexをカラムに戻す
    CAP_inv = CAP_inv.reset_index()
    CAP_inv = CAP_inv.rename(columns={'level_2': '日付 の年、月'}).astype(str)
    CAP_inv['日付 の年、月'] = pd.to_datetime(CAP_inv['日付 の年、月'] + '01', format='%Y/%m/%d')
    CAP_inv['日付 の年、月'] = [x.strftime('%Y{0}%m{1}').format(*'年月') for x in CAP_inv['日付 の年、月']]

    # 内製外製を判断する
    CAP_inv['内製'] = '内製'

    # 順番を整える
    CAP_inv = CAP_inv.loc[:, ['日付 の年、月', '製造GR', '内製', '管理Gr', '数値名', '値', 'フラグ']]

    Add_CAP_inv = CAP_inv.copy()
    Add_CAP_inv['数値名'] = '生産能力（投資済）不足分'
    Add_CAP_inv['値'] = (-1)*Add_CAP_inv['値'].astype(int)
    Add_CAP_inv['フラグ'] = ''

    #順番を整える
    Add_CAP_inv = Add_CAP_inv.loc[:,['日付 の年、月', '製造GR', '内製', '管理Gr', '数値名', '値', 'フラグ']]
    Output = Output.append([CAP,Add_CAP,CAP_inv,Add_CAP_inv])

#外製用のシート取込
files1 = glob.glob('C:/Users/Aoi_Fujishita/能力調整確認シート/*能力確認A_*.xlsx') #//172.24.81.161/share/F加工企業体/生産計画/共用/FBR資料/能力調整確認シート/*能力確認A_*.xlsx
for file1 in files1:
    input_file_name1 = (file1)
    input_book = pd.ExcelFile(input_file_name1)
    # Excelブック内の各シートの名前をリストで取得
    input_sheet_name = input_book.sheet_names
    # 管理Gr生成のためにシート名取得
    sheet_name = input_book.sheet_names[0]
    # 生産能力(実力値)
    original_cap1 = pd.read_excel(input_file_name1 ,index_col=[3,4] ,
                                 skiprows=[0,1,3,5,6,7,8,9,11,12,13,14,15,17,18,19,20,21,23,24,25,26,27,29,30,31,32,33,35,36,37,38,39,41,42,43,44,45] ,dtype=object)
    #生産能力(投資済)
    original_cap_inv1 = pd.read_excel(input_file_name1 ,index_col=[3,4] ,
                                 skiprows=[0,1,3,4,6,7,8,9,10,12,13,14,15,16,18,19,20,21,22,24,25,26,27,28,30,31,32,33,34,36,37,38,39,40,42,43,44,45] ,dtype=object)
    # 調整後生産能力(実力値)
    adjusted_cap1 = pd.read_excel(input_file_name1, index_col=[3, 4],
                                 skiprows=[0,1,3,4,5,7,8,9,10,11,13,14,15,16,17,19,20,21,22,23,25,26,27,28,29,31,32,33,34,35,37,38,39,40,41,43,44,45] ,dtype=object)
    # 調整後生産能力(投資済)
    adjusted_cap_inv1 = pd.read_excel(input_file_name1, index_col=[3, 4],
                                 skiprows=[0,1,3,4,5,6,8,9,10,11,12,14,15,16,17,18,20,21,22,23,24,26,27,28,29,30,32,33,34,35,36,38,39,40,41,42,44,45] ,dtype=object)

    # それぞれ不要なカラムを削除
    original_cap1.drop(original_cap1.columns[[0, 1, 2]], axis=1, inplace=True)
    original_cap_inv1.drop(original_cap_inv1.columns[[0, 1, 2]], axis=1, inplace=True)
    adjusted_cap1.drop(adjusted_cap1.columns[[0, 1, 2]], axis=1, inplace=True)
    adjusted_cap_inv1.drop(adjusted_cap_inv1.columns[[0, 1, 2]], axis=1, inplace=True)

    ds_original_cap1 = original_cap1.stack(dropna=False)
    ds_original_cap_inv1 = original_cap_inv1.stack(dropna=False)
    ds_adjusted_cap1 = adjusted_cap1.stack(dropna=False)
    ds_adjusted_cap_inv1 = adjusted_cap_inv1.stack(dropna=False)
    # まずは生産能力(実力値)
    # 調整前後の比較のためにindexを揃え、カラム名を変える
    cap3 = ds_original_cap1.reset_index(level = 1)
    cap3 = cap3.rename(columns={'level_1': '数値名1' , 0: '値1'})

    cap4 = ds_adjusted_cap1.reset_index(level = 1)
    cap4 = cap4.rename(columns={'level_1': '数値名2', 0: '値2'})
    #調整前後で一つのデータフレームにする(indexをキーとする)
    CAP1 = cap4.join(cap3)
    CAP1.fillna(0, inplace=True)
    # 調整があればその差分を値とする
    CAP1['値'] = np.where(CAP1['値2'] != 0 ,CAP1['値2']-CAP1['値1'], 0 )

    #値が０であれば消す=0でないデータを取り出す
    CAP1 = CAP1[CAP1['値'] != 0]

    #更新後-...という名前を生産能力(実力値)に変える
    CAP1['数値名'] = '生産能力(実力値)'
    #フラグを付ける
    CAP1['フラグ'] = 1

    #indexをカラムに戻す
    CAP1 = CAP1.reset_index()
    CAP1 = CAP1.rename(columns={'level_1': '日付 の年、月'}).astype(str)

    CAP1['日付 の年、月'] = pd.to_datetime(CAP1['日付 の年、月'] + '01', format='%Y/%m/%d')
    CAP1['日付 の年、月'] = [x.strftime('%Y{0}%m{1}').format(*'年月') for x in CAP1['日付 の年、月']]


    #シート名から管理Gr生成
    CAP1['Supplier'] = sheet_name
    # FBR帳票用サプライヤー名ファイルの読み込み //172.24.81.161/share/F加工企業体/生産計画/共用/FBR資料/稼働日カレンダー
    SP_name = pd.read_csv('C:/Users/Aoi_Fujishita/能力調整確認シート/SP_name.csv', encoding='utf-8',
                          dtype='object', index_col=None)
    # calendarのカラムを管理Grに揃える
    CAP1 = pd.merge(CAP1, SP_name, on=['Supplier'], how='left')

    # 内製外製を判断する
    CAP1['内製'] = '外製'

    # 順番を整える
    CAP1 = CAP1.loc[:, ['日付 の年、月', '製造GR', '内製', '管理Gr', '数値名', '値', 'フラグ']]

    Add_CAP1 = CAP1.copy()
    Add_CAP1['数値名'] = '生産能力（実力値）不足分'
    Add_CAP1['値'] =  (-1)*Add_CAP1['値'].astype(int)
    Add_CAP1['フラグ'] = ''

    # 順番を整える
    Add_CAP1 = Add_CAP1.loc[:, ['日付 の年、月', '製造GR', '内製', '管理Gr', '数値名', '値', 'フラグ']]


    # 続いて生産能力(投資済)
    # 調整前後の比較のためにindexを揃え、カラム名を変える
    cap_inv3 = ds_original_cap_inv1.reset_index(level=1)
    cap_inv3 = cap_inv3.rename(columns={'level_1': '数値名1', 0: '値1'})

    cap_inv4 = ds_adjusted_cap_inv1.reset_index(level=1)
    cap_inv4 = cap_inv4.rename(columns={'level_1': '数値名2', 0: '値2'})
    # 調整前後で一つのデータフレームにする(indexをキーとする)
    CAP_inv1 = cap_inv4.join(cap_inv3)
    CAP_inv1.fillna(0, inplace=True)
    # 調整があればその差分を値とする
    CAP_inv1['値'] = np.where(CAP_inv1['値2'] !=0, CAP_inv1['値2']-CAP_inv1['値1'], 0 )

    # 値が0であれば消す=0でないデータを取り出す
    CAP_inv1 = CAP_inv1[CAP_inv1['値'] != 0]

    # 更新後-...という名前を生産能力(投資済)に変える
    CAP_inv1['数値名'] = '生産能力(投資済)'
    # フラグを付ける
    CAP_inv1['フラグ'] = 1

    # indexをカラムに戻す
    CAP_inv1 = CAP_inv1.reset_index()
    CAP_inv1 = CAP_inv1.rename(columns={'level_1': '日付 の年、月'}).astype(str)

    CAP_inv1['日付 の年、月'] = pd.to_datetime(CAP_inv1['日付 の年、月'] + '01', format='%Y/%m/%d')
    CAP_inv1['日付 の年、月'] = [x.strftime('%Y{0}%m{1}').format(*'年月') for x in CAP_inv1['日付 の年、月']]

    # シート名から管理Gr生成
    CAP_inv1['Supplier'] = sheet_name
    # calendarのカラムを管理Grに揃える
    CAP_inv1 = pd.merge(CAP_inv1, SP_name, on=['Supplier'], how='left')
    # 内製外製を判断する
    CAP_inv1['内製'] = '外製'
    # 順番を整える
    CAP_inv1 = CAP_inv1.loc[:, ['日付 の年、月', '製造GR', '内製', '管理Gr', '数値名', '値', 'フラグ']]

    Add_CAP_inv1 = CAP_inv1.copy()
    Add_CAP_inv1['数値名'] = '生産能力（投資済）不足分'
    Add_CAP_inv1['値'] =  (-1)*Add_CAP_inv1['値'].astype(int)
    Add_CAP_inv1['フラグ'] = ''

    # 順番を整える
    Add_CAP1 = Add_CAP1.loc[:, ['日付 の年、月', '製造GR', '内製', '管理Gr', '数値名', '値', 'フラグ']]

    Output = Output.append([CAP1, Add_CAP1, CAP_inv1, Add_CAP_inv1])
#Output['フラグ'].astype(int)


#その他のシート取込
files2 = glob.glob('C:/Users/Aoi_Fujishita/能力調整確認シート/その他調整.xlsx')#//172.24.81.161/share/F加工企業体/生産計画/共用/FBR資料/能力調整確認シート/その他調整.xlsx
for file2 in files2:
    input_file_name2 = (file2)
    #需要予測数
    others_fc = pd.read_excel(input_file_name2 ,index_col = [0,1,2] ,skiprows=[0,2,4,5,6,7,8,10,11,12,13,14,16,17,18,19,20,22,23,24,25,26,28,29,30,31,32,34,35,36,37,38,
                                                                               40,41,42,43,44,46,47,48,49,50,52,53,54,55,56,58,59,60,61,62,64,65,66,67,68,70,71,72,73] ,dtype=str )
    #生産能力(実力値)
    others_cap =pd.read_excel(input_file_name2 ,index_col = [0,1,2] ,skiprows=[0,2,3,5,6,7,8,9,11,12,13,14,15,17,18,19,20,21,23,24,25,26,27,29,30,31,32,33,35,36,37,38,39,
                                                                               41,42,43,44,45,47,48,49,50,51,53,54,55,56,57,59,60,61,62,63,65,66,67,68,69,71,72,73] ,dtype=str)
    #生産能力(投資済)
    others_cap_inv = pd.read_excel(input_file_name2 ,index_col = [0,1,2] ,skiprows=[0,2,3,4,6,7,8,9,10,12,13,14,15,16,18,19,20,21,22,24,25,26,27,28,30,31,32,33,34,36,37,38,39,
                                                                               40,42,43,44,45,46,48,49,50,51,52,54,55,56,57,58,60,61,62,63,64,66,67,68,69,70,72,73] ,dtype=str)
    ds_others_fc = others_fc.stack(dropna=False)
    ds_others_cap = others_cap.stack(dropna=False)
    ds_others_cap_inv = others_cap_inv.stack(dropna=False)


    #数値調整のためにindexをそろえカラムを整える
    df_others_fc = ds_others_fc.reset_index(level=2)
    df_others_fc.rename(columns={'level_2': '数値名1' , 0: '値1'} , inplace=True)
    df_others_cap = ds_others_cap.reset_index(level=2)
    df_others_cap.rename(columns={'level_2': '数値名2' , 0: '値2'}, inplace=True)
    df_others_cap_inv = ds_others_cap_inv.reset_index(level=2)
    df_others_cap_inv.rename(columns={'level_2': '数値名3' , 0: '値3'}, inplace=True)


    #まずは生産能力(実力値)
    df_for_cap = df_others_fc.join(df_others_cap)
    df_for_cap.fillna(0.0, inplace=True)
    df_for_cap['値'] = np.where(df_for_cap['値1'] != df_for_cap['値2'], df_for_cap['値1'].astype(float)-df_for_cap['値2'].astype(float), 0.0)
    # 値が０であれば消す=0でないデータを取り出す
    df_for_cap = df_for_cap[df_for_cap['値'] != 0.0]

    #数値名2を数値名とする
    df_for_cap.rename(columns={'数値名2': '数値名'}, inplace=True)
    df_for_cap['数値名']= '生産能力(実力値)'


    # indexをカラムに戻す
    df_for_cap = df_for_cap.reset_index()
    df_for_cap = df_for_cap.rename(columns={'level_2': '日付 の年、月'}).astype(str)
    df_for_cap['日付 の年、月'] = pd.to_datetime(df_for_cap['日付 の年、月'] + '01', format='%Y/%m/%d')
    df_for_cap['日付 の年、月'] = [x.strftime('%Y{0}%m{1}').format(*'年月') for x in df_for_cap['日付 の年、月']]

    df_for_cap['フラグ'] = ''

    # 内製外製を判断する
    df_for_cap['内製'] = '外製'

    # 順番を整える
    df_for_cap = df_for_cap.loc[:, ['日付 の年、月', '製造GR', '内製', '管理Gr', '数値名', '値', 'フラグ']]

    Add_df_for_cap = df_for_cap.copy()
    Add_df_for_cap['数値名'] = '生産能力（実力値）不足分'
    Add_df_for_cap['値'] = (-1)*Add_df_for_cap['値'].astype(float)


    #続いて生産能力(投資済)
    df_for_cap_inv = df_others_fc.join(df_others_cap_inv)
    df_for_cap_inv.fillna(0, inplace=True)
    df_for_cap_inv['値'] = np.where(df_for_cap_inv['値1'] != df_for_cap_inv['値3'], df_for_cap_inv['値1'].astype(float)-df_for_cap_inv['値3'].astype(float), 0)
    # 値が０であれば消す=0でないデータを取り出す
    df_for_cap_inv = df_for_cap_inv[df_for_cap_inv['値'] != 0]

    # 数値名2を数値名とする
    df_for_cap_inv.rename(columns={'数値名3': '数値名'}, inplace=True)
    df_for_cap_inv['数値名'] = '生産能力(投資済)'

    # indexをカラムに戻す
    df_for_cap_inv = df_for_cap_inv.reset_index()
    df_for_cap_inv = df_for_cap_inv.rename(columns={'level_2': '日付 の年、月'}).astype(str)
    df_for_cap_inv['日付 の年、月'] = pd.to_datetime(df_for_cap_inv['日付 の年、月'] + '01', format='%Y/%m/%d')
    df_for_cap_inv['日付 の年、月'] = [x.strftime('%Y{0}%m{1}').format(*'年月') for x in df_for_cap_inv['日付 の年、月']]


    df_for_cap_inv['フラグ'] = ''
    # 内製外製を判断する
    df_for_cap_inv['内製'] = '外製'

    # 順番を整える
    df_for_cap_inv = df_for_cap_inv.loc[:, ['日付 の年、月', '製造GR', '内製', '管理Gr', '数値名', '値', 'フラグ']]

    Add_df_for_cap_inv = df_for_cap_inv.copy()
    Add_df_for_cap_inv['数値名'] = '生産能力（投資済）不足分'
    Add_df_for_cap_inv['値'] = (-1)*Add_df_for_cap_inv['値'].astype(float)
    Output = Output.append([df_for_cap, Add_df_for_cap, df_for_cap_inv,Add_df_for_cap_inv])


# ファイルアウトプット
f_name = 'Output.tsv'  #'//172.24.81.161/share/F加工企業体/生産計画/共用/FBR資料/能力調整確認シート/output/生産能力値用シート貼り付け用' + dt.datetime.today().strftime("%Y%m%d") + '.tsv'
Output.to_csv(f_name, sep='\t', encoding='utf-8', index=False)
print('処理が完了しました')
