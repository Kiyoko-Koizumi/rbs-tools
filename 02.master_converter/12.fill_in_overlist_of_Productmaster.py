# coding: utf-8
# 新規作成　単価マスタのオーバーリスト処理　2019/08/15

# モジュールのインポート
import os
import csv
import pandas as pd
import sys
import glob

csv.field_size_limit(1000000000)

font = 'utf-8'
# font='shift_jisx0213'
# 変数を宣言
UnitPrice = ()

# 実行する01.Master作成データ以下のファイル名を指定 例'20190807_作成Master/'
file_pass = '20190809_作成Master'
# 分析コードを指定　例'03722108'
cls_cd = '03622711'
a_pass = '//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Vietnam_Master_関連資料/01.Master作成データ/' + file_pass + '/' + cls_cd + '/' + cls_cd

# 単価マスタのファイルパスを取得
f_pass = glob.glob(a_pass + '_*_UnitPrice.xlsx')

if len(f_pass)>0:   # 単価マスタのエラーファイルがあれば以下の処理を実施
    # Excelファイルから情報を取得し一つのファイルにまとめる
    for s in range(0, len(f_pass)):
        f_temp = pd.read_excel(f_pass[s], sheet_name='UnitPrice①', dtype=object)
        if s == 0:
            UnitPrice = f_temp
            # XXXをxheaderに格納
            header = UnitPrice.columns
            xheader = UnitPrice[UnitPrice['Subsidiary Code'] == 'XXX']
        else:
            UnitPrice = UnitPrice.append(f_temp, sort=False)

    # XXXを除く
    UnitPrice = UnitPrice[UnitPrice['Subsidiary Code'] != 'XXX']
    UnitPrice.reset_index(drop=True, inplace=True)

    # 各Err_Flgの数をカウント
    Err_Flg1 = str(len(UnitPrice[UnitPrice['Err_Flg1'].notnull()]))
    Err_Flg2 = str(len(UnitPrice[UnitPrice['Err_Flg2'].notnull()]))
    Err_Flg3 = str(len(UnitPrice[UnitPrice['Err_Flg3'].notnull()]))
    Err_Flg4 = str(len(UnitPrice[UnitPrice['Err_Flg4'].notnull()]))

    # ErrFlgのみのデータをErrFlg数量のファイル名でアウトプット
    ErrFlg = UnitPrice[(UnitPrice['Err_Flg1'].notnull() | UnitPrice['Err_Flg2'].notnull() | UnitPrice['Err_Flg3'].notnull() | UnitPrice['Err_Flg4'].notnull())].copy()
    ErrFlg = xheader.append(ErrFlg, sort=False)
    ErrFlg_name = a_pass + '_ErrFlg_UnitPrice_' + Err_Flg1 + '_' + Err_Flg2 + '_' + Err_Flg3 + '_' + Err_Flg4 + '.xlsx'
    ErrFlg.to_excel(ErrFlg_name, sheet_name='UnitPrice①', index=False)

    # OverList処理の対応
    if len(UnitPrice[UnitPrice['Err_Flg1'].notnull()]) > 0:# ErrFlgがあった場合のみ実行
        for i in range(1, 20):  # 2~20までで仕入値がないカラムは1つ前のスライドから転記
            j = i + 1
            i_ssp = 'Slide Sales Pc/Unit ' + str(i)# 例　i_ssp=Slide Sales Pc/Unit 1
            i_spp = 'Slide Purchase Pc/Unit ' + str(i)# 例　i_spp=Slide Purchase Pc/Unit 1
            i_splt = 'Slide Production LT ' + str(i)
            i_sdts = 'Slide Days TS ' + str(i)
            j_ssp = 'Slide Sales Pc/Unit ' + str(j)# 例　i_ssp=Slide Sales Pc/Unit 2
            j_spp = 'Slide Purchase Pc/Unit ' + str(j)# 例　i_spp=Slide Purchase Pc/Unit 2
            j_splt = 'Slide Production LT ' + str(j)
            j_sdts = 'Slide Days TS ' + str(j)
            sura = 'スラ' + str(i) + str(j)

            # 判定列（例スラ12）を新規作成しデフォルトで1を入れる
            UnitPrice.loc[:, sura] = '1'
            # ssp,spp,splt,sdtsすべてが一致していたら1→0に変更する
            UnitPrice.loc[((UnitPrice[i_ssp] == UnitPrice[j_ssp]) & (UnitPrice[i_spp] == UnitPrice[j_spp]) & (UnitPrice[i_splt] == UnitPrice[j_splt]) & (UnitPrice[i_sdts] == UnitPrice[j_sdts])), sura] = '0'

        for i in reversed(range(1, 20)):  # 2~20までで仕入値がないカラムは1つ前のスライドから転記
            j = i + 1
            sura = 'スラ' + str(i) + str(j)
            UnitPrice.loc[(UnitPrice[sura] == '0')]



    # 修正が終わったファイルを出力
    if (len(UnitPrice[UnitPrice['Err_Flg1'].notnull()]) + len(UnitPrice[UnitPrice['Err_Flg4'].notnull()])) > 0:# ErrFlgがあった場合のみ実行
        ErrFlg = UnitPrice[(UnitPrice['Err_Flg1'].notnull() | UnitPrice['Err_Flg2'].notnull() | UnitPrice['Err_Flg3'].notnull() | UnitPrice['Err_Flg4'].notnull())].copy()
        ErrFlg = xheader.append(ErrFlg, sort=False)
        ErrFlg_name = a_pass + '_filled_UnitPrice_' + Err_Flg1 + '_' + Err_Flg2 + '_' + Err_Flg3 + '_' + Err_Flg4 + '.xlsx'
        ErrFlg.to_excel(ErrFlg_name, sheet_name='UnitPrice①', index=False)

    # 現法毎にファイル出力
    sub_name = ['CHN', 'GRM', 'HKG', 'IND', 'JKT', 'KOR', 'MEX', 'MJP', 'MYS', 'SGP', 'THA', 'TIW', 'USA', 'VNM']
    for v in sub_name:
        sub_up = UnitPrice[UnitPrice['Subsidiary Code'] == v].copy()
        if len(sub_up) > 0:
            sub_up = xheader.append(sub_up, sort=False)
            # 不要なカラムを削除
            sub_up.drop(['Err_Flg1', 'Err_Flg2', 'Err_Flg3', 'Err_Flg4'], axis=1, inplace=True)
            sub_up_name = a_pass + '_' + v + '_UnitPrice_filled.txt'
            sub_up.to_csv(sub_up_name, sep='\t', encoding='utf_16', quotechar='"', line_terminator='\n', index=False)
else:
    print('単価マスタのエラーファイルはありません！')

print('finish!')