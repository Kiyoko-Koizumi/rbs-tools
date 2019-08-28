#商品マスタoverlist処理

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
file_pass = '20190807_作成Master'
# 分析コードを指定　例'03722108'
cls_cd = '03722108'
a_pass = '//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Vietnam_Master_関連資料/01.Master作成データ/' + file_pass + '/' + cls_cd + '/' + cls_cd

# XXXをxheaderに格納


# 単価マスタのファイルパスを取得
f_pass = glob.glob(a_pass + '_Over_*_Product.xlsx')

#p_pass = pd.read_excel(a_pass + '_Over_CHN_Product.xlsx', sheet_names='product', dtype=object)

'''
if len(f_pass)>0:   # 単価マスタのエラーファイルがあれば以下の処理を実施
    # Excelファイルから情報を取得し一つのファイルにまとめる
    for s in range(0, len(f_pass)):
        f_temp = pd.read_excel(f_pass[s], sheet_name='Product', dtype=object)
        if s == 0:
            p_pass = f_temp
            # XXXをxheaderに格納
            #header = UnitPrice.columns
            #xheader = UnitPrice[UnitPrice['Product Code'].str.contains('XXXX')]
        else:
            p_pass = p_pass.append(f_temp, sort=False)


x_header = p_pass[p_pass['Over_List'].str.contains('XXXX')]
x_header = x_header.drop_duplicates()
'''


'''
p_pass = p_pass.drop(['Slide Qty 1','Slide Sales Pc/Unit 1','Slide Purchase Pc/Unit 1','Slide Production LT 1','Slide Days TS 1','Slide Qty 2','Slide Sales Pc/Unit 2',
                      'Slide Purchase Pc/Unit 2','Slide Production LT 2','Slide Days TS 2','Slide Qty 3','Slide Sales Pc/Unit 3','Slide Purchase Pc/Unit 3','Slide Production LT 3',
                      'Slide Days TS 3','Slide Qty 4','Slide Sales Pc/Unit 4','Slide Purchase Pc/Unit 4','Slide Production LT 4','Slide Days TS 4','Slide Qty 5','Slide Sales Pc/Unit 5',
                      'Slide Purchase Pc/Unit 5','Slide Production LT 5','Slide Days TS 5','Slide Qty 6','Slide Sales Pc/Unit 6','Slide Purchase Pc/Unit 6','Slide Production LT 6','Slide Days TS 6',
                      'Slide Qty 7','Slide Sales Pc/Unit 7','Slide Purchase Pc/Unit 7','Slide Production LT 7','Slide Days TS 7','Slide Qty 8','Slide Sales Pc/Unit 8','Slide Purchase Pc/Unit 8','Slide Production LT 8',
                      'Slide Days TS 8','Slide Qty 9','Slide Sales Pc/Unit 9','Slide Purchase Pc/Unit 9','Slide Production LT 9','Slide Days TS 9','Slide Qty 10','Slide Sales Pc/Unit 10','Slide Purchase Pc/Unit 10',
                      'Slide Production LT 10','Slide Days TS 10'],axis=1)
'''



#productmst= glob.glob(a_pass + '_Over_USA_Product.xlsx',sheet_name= 'product')
#productmst.to_csv('C:/Users/Chanwook_Heo/Documents/04.マスタ作成/overlist/product.txt', sep='\t', encoding='utf_16', index=False)

if len(f_pass)>0:   # 単価マスタのエラーファイルがあれば以下の処理を実施
    # Excelファイルから情報を取得し一つのファイルにまとめる
    for s in range(0, len(f_pass)):
        f_temp = pd.read_excel(f_pass[s], sheet_name='Over_List', dtype=object)
        f_temp.loc[:,'Subsidiary Code'] = f_pass[s][-16:-13]
        if s == 0:
            UnitPrice = f_temp
            #XXXをxheaderに格納
            header = UnitPrice.columns
            x_header = UnitPrice[UnitPrice['Product Code'].str.contains('XXXX')]
        else:
            UnitPrice = UnitPrice.append(f_temp, sort=False)

 # XXXを除く
    UnitPrice = UnitPrice[~UnitPrice['Product Code'].str.contains('XXXX')]
    UnitPrice.reset_index(drop=True, inplace=True)

sura_list = []

for i in range(1, 20):  # 2~20までで仕入値がないカラムは1つ前のスライドから転記
    j = i + 1
    i_ssp = 'Slide Sales Pc/Unit ' + str(i)  # 例　i_ssp=Slide Sales Pc/Unit 1
    i_spp = 'Slide Purchase Pc/Unit ' + str(i)  # 例　i_spp=Slide Purchase Pc/Unit 1
    i_splt = 'Slide Production LT ' + str(i)
    i_sdts = 'Slide Days TS ' + str(i)
    j_ssp = 'Slide Sales Pc/Unit ' + str(j)  # 例　i_ssp=Slide Sales Pc/Unit 2
    j_spp = 'Slide Purchase Pc/Unit ' + str(j)  # 例　i_spp=Slide Purchase Pc/Unit 2
    j_splt = 'Slide Production LT ' + str(j)
    j_sdts = 'Slide Days TS ' + str(j)
    sura = 'スラ' + str(i) + '/' + str(j)
    sura_list.append(sura)

    # 判定列（例スラ12）を新規作成しデフォルトで1を入れる
    UnitPrice.loc[:, sura] = 1

    # ssp,spp,splt,sdtsすべてが一致していたら1→0に変更する
    UnitPrice.loc[((UnitPrice[i_ssp] == UnitPrice[j_ssp]) & (UnitPrice[i_spp] == UnitPrice[j_spp]) & (
                UnitPrice[i_splt] == UnitPrice[j_splt]) & (UnitPrice[i_sdts] == UnitPrice[j_sdts])), sura] = 0

    UnitPrice.loc[((UnitPrice[j_ssp].isnull()|UnitPrice[j_spp].isnull()| UnitPrice[j_splt].isnull() | UnitPrice[j_sdts].isnull())), sura] = ''

#カラムスラ1/2～19/20まで合計
UnitPrice.loc[:, 'SUM'] = UnitPrice.loc[:, sura_list].sum(axis=1)

UnitPrice = UnitPrice[UnitPrice['SUM'] < 10]
slide_over = UnitPrice[UnitPrice['SUM'] > 9]
slide_over.to_csv('//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Vietnam_Master_関連資料/01.Master作成データ/20190807_作成Master/03722108/overlist.txt',sep='\t', encoding='utf_16', index=False)

for ii in range(2, 20):
    jj=ii + 1
    sura = 'スラ' + str(ii) + '/' + str(jj)

    for x in range(ii, 20):
        y = x + 1
        x_spa = 'Slide Qty ' + str(x)
        x_ssp = 'Slide Sales Pc/Unit ' + str(x)  # 例　i_ssp=Slide Sales Pc/Unit 1
        x_spp = 'Slide Purchase Pc/Unit ' + str(x)  # 例　i_spp=Slide Purchase Pc/Unit 1
        x_splt = 'Slide Production LT ' + str(x)
        x_sdts = 'Slide Days TS ' + str(x)
        y_spa = 'Slide Qty ' + str(y)
        y_ssp = 'Slide Sales Pc/Unit ' + str(y)  # 例　i_ssp=Slide Sales Pc/Unit 2
        y_spp = 'Slide Purchase Pc/Unit ' + str(y)  # 例　i_spp=Slide Purchase Pc/Unit 2
        y_splt = 'Slide Production LT ' + str(y)
        y_sdts = 'Slide Days TS ' + str(y)
        UnitPrice.loc[UnitPrice[sura] == 0, x_spa] = UnitPrice[y_spa]
        UnitPrice.loc[UnitPrice[sura] == 0, x_ssp] = UnitPrice[y_ssp]
        UnitPrice.loc[UnitPrice[sura] == 0, x_spp] = UnitPrice[y_spp]
        UnitPrice.loc[UnitPrice[sura] == 0, x_splt] = UnitPrice[y_splt]
        UnitPrice.loc[UnitPrice[sura] == 0, x_sdts] = UnitPrice[y_sdts]
'''
UnitPrice= UnitPrice.drop(['Production LT','Min Qty of Big Order',	'Max Qty of Big Order','Alt Dsct Rt:S 1' ,
                           'Alt Dsct Rt:P 1' ,	'Alt Dsct Rt:S 2' ,	'Alt Dsct Rt:P 2' ,	'Alt Dsct Rt:S 3' ,
                           'Alt Dsct Rt:P 3' ,	'Alt Dsct Rt:S 4' ,	'Alt Dsct Rt:P 4' ,	'Alt Dsct Rt:S 5' ,
                           'Alt Dsct Rt:P 5' ,	'Alt Dsct Rt:S 6' ,	'Alt Dsct Rt:P 6' ,	'Alt Dsct Rt:S 7' ,
                           'Alt Dsct Rt:P 7' ,	'Alt Dsct Rt:S 8' ,	'Alt Dsct Rt:P 8' ,	'Alt Dsct Rt:S 9' ,
                           'Alt Dsct Rt:P 9' ,	'Alt Dsct Rt:S 10' ,'Alt Dsct Rt:P 10' ],axis=1)
'''

#output = pd.merge(p_pass,UnitPrice, on = ['Product Code', 'Subsidiary Code'],how='inner')



    #output= output(t_header)
    #output= output.loc[:, t_header]


    # 現法毎にファイル出力
sub_name = ['CHN', 'GRM', 'HKG', 'IND', 'JKT', 'KOR', 'MEX', 'MJP', 'MYS', 'SGP', 'THA', 'TIW', 'USA', 'VNM']
for v in sub_name:
    sub_up = UnitPrice[UnitPrice['Subsidiary Code'] == v].copy()
    if len(sub_up) > 0:
        sub_up1 = sub_up.iloc[:1048574, :].copy()
        sub_up1 = x_header.append(sub_up1, sort=False)
        sub_up1.drop(['Subsidiary Code','スラ1/2' ,'スラ2/3' ,'スラ3/4' ,'スラ4/5' ,'スラ5/6' ,'スラ6/7' ,'スラ7/8' ,'スラ8/9' ,'スラ9/10' ,'スラ10/11'
                        ,'スラ11/12' ,'スラ12/13' ,'スラ13/14' ,'スラ14/15' ,'スラ15/16' ,'スラ16/17' ,'スラ17/18' ,'スラ18/19' ,'スラ19/20' ,
                          'SUM'], axis=1, inplace=True)
        sub_up_name = a_pass + '_' + v + '_Productmst_filled.xlsx'
        sub_up1.to_excel(sub_up_name,index=False)
        # sub_up_name = a_pass + '_' + v + '_Productmst_filled.txt'
        # sub_up1.to_csvl(sub_up_name, sep='\t', encoding='utf_16', quotechar='"', line_terminator='\n', index=False)

        if len(sub_up) > 1048574:
            sub_up2 = sub_up.iloc[1048574:, :].copy()
            sub_up2 = x_header.append(sub_up2, sort=False)
            sub_up2.drop(['Subsidiary Code', 'スラ1/2', 'スラ2/3', 'スラ3/4', 'スラ4/5', 'スラ5/6', 'スラ6/7', 'スラ7/8', 'スラ8/9', 'スラ9/10', 'スラ10/11'
                             , 'スラ11/12', 'スラ12/13', 'スラ13/14', 'スラ14/15', 'スラ15/16', 'スラ16/17', 'スラ17/18', 'スラ18/19',
                          'スラ19/20','SUM'], axis=1, inplace=True)
            sub_up_name = a_pass + '_' + v + '_Productmst_filled2.xlsx'
            sub_up2.to_excel(sub_up_name,index=False)
            # sub_up_name = a_pass + '_' + v + '_Productmst_filled.txt'
            # sub_up2.to_csvl(sub_up_name, sep='\t', encoding='utf_16', quotechar='"', line_terminator='\n',index=False)




else:
    print('単価マスタのエラーファイルはありません！')

print('finish')

#suraの値が0の場合は後ろの値を埋める