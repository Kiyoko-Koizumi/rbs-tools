#商品マスタ　FCNtoECAL

import csv
import glob
import pandas as pd
import xlrd

font = 'shift_jisx0213'
csv.field_size_limit(1000000000)

#path = '//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_FCN_Master'
path = 'C:/Users/Chanwook_Heo/Documents/04.マスタ作成/検証/1.reference_FCN_to_ECAL'
inner_list = glob.glob(path + '/2.INNER_LIST/INNER_LIST_*.xlsx')
master_list = glob.glob(path + '/1.moto/PRODUCT_*.txt')

inner_matome= pd.DataFrame()
for s in range(0,len(inner_list)):
    a_temp = pd.read_excel(inner_list[s],dtype={'Inner Code':object})
    #a_temp = a_temp.drop(['PRODUCT_CD', 'STOCK_DIV', 'CLASSIFY_CD', 'SUPPLIER_CD'], axis=1)
    inner_matome = inner_matome.append(a_temp, ignore_index=True)




master_matome = pd.DataFrame()
for x in range(0,len(master_list)):
    b_temp = pd.read_csv(master_list[x],sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False)
    master_matome = master_matome.append(b_temp,ignore_index=True)

x_header = master_matome[master_matome['Product Code'].str.contains('XXXX')]
x_header = x_header.drop_duplicates()


#輸出禁止品除外（対象現法が台湾のみ適用）
TIW = pd.read_excel(path + '/3.IROIRO/TIW.xlsx',dtype={'Inner Code':object})
TIW=TIW.drop(['No','CLASSIFY_CD','CLASSIFY_NM','Type','Model','TIW_DATE','TIW_SUPPLIER','CHN_DATE','CHN_SUPPLIER'],axis=1)
#台湾輸出禁止品にフラグ1を挿入
TIW.loc[:, 'TIW_FLG'] = '1'

#pmst[pmst['Inner Code'] == df['Inner Code']]
output1 = pd.merge(master_matome, inner_matome , on=['Subsidiary Code','Inner Code'], how= 'inner')
output2 = pd.merge(output1,TIW,on =['Inner Code'], how= 'left')


#台湾輸不可分除外
output2.loc[output2['Subsidiary Code']!= 'TIW', 'TIW_FLG'] = '0'
output2 = output2[output2['TIW_FLG'] != '1']
output2 = output2.drop(['TIW_FLG'],axis=1)
#0Process Mode→2変更
output2['Process Mode']="2"
#1	Production LT→0変更
output2['Production LT']="0"
#2	Slide Purchase Pc/Unit 1→0変更
output2['Slide Purchase Pc/Unit 1']="0"
#3	Slide Production LT 1→0変更
output2['Slide Production LT 1']="0"
#4	Slide Purchase Pc/Unit 2→0変更
output2['Slide Purchase Pc/Unit 2']="0"
#5	Slide Production LT 2→0変更
output2['Slide Production LT 2']="0"
#6	Slide Purchase Pc/Unit 3→0変更
output2['Slide Purchase Pc/Unit 3']="0"
#7	Slide Production LT 3→0変更
output2['Slide Production LT 3']="0"
#8	Slide Purchase Pc/Unit 4→0変更
output2['Slide Purchase Pc/Unit 4']="0"
#9	Slide Production LT 4→0変更
output2['Slide Production LT 4']="0"
#10	Slide Purchase Pc/Unit 5→0変更
output2['Slide Purchase Pc/Unit 5']="0"
#11	Slide Production LT 5→0変更
output2['Slide Production LT 5']="0"
#12	Slide Purchase Pc/Unit 6→0変更
output2['Slide Purchase Pc/Unit 6']="0"
#13	Slide Production LT 6→0変更
output2['Slide Production LT 6']="0"
#14	Slide Purchase Pc/Unit 7→0変更
output2['Slide Purchase Pc/Unit 7']="0"
#15	Slide Production LT 7→0変更
output2['Slide Production LT 7']="0"
#16	Slide Purchase Pc/Unit 8→0変更
output2['Slide Purchase Pc/Unit 8']="0"
#17	Slide Production LT 8→0変更
output2['Slide Production LT 8']="0"
#18	Slide Purchase Pc/Unit 9→0変更
output2['Slide Purchase Pc/Unit 9']="0"
#19	Slide Production LT 9→0変更
output2['Slide Production LT 9']="0"
#20	Slide Purchase Pc/Unit 10→0変更
output2['Slide Purchase Pc/Unit 10']="0"
#21	Slide Production LT 10→0変更
output2['Slide Production LT 10']="0"
#22	Express T Purchase Pc/Unit→0変更
output2['Express T Purchase Pc/Unit']="0"
#23	Express A Calc Type for Purchase→0変更
output2['Express A Calc Type for Purchase']="0"
#24	Express A Purchase Pc/Unit→0変更
output2['Express A Purchase Pc/Unit']="0"
#25	Express A Production LT→0変更
output2['Express A Production LT']="0"
#26	Plant Express A Purchase Calc→0変更
output2['Plant Express A Purchase Calc']="0"
#27	Plant Express A Purchase Pc/Unit→0変更
output2['Plant Express A Purchase Pc/Unit']="0"
#28	Express B Purchase Pc/Unit→0変更
output2['Express B Purchase Pc/Unit']="0"
#29	Express B Production LT→0変更
output2['Express B Production LT']="0"
#30	Express C Purchase Pc/Unit→0変更
output2['Express C Purchase Pc/Unit']="0"
#31	Express C Production LT→0変更
output2['Express C Production LT']="0"
#32	Weight→0変更
output2['Weight']="0"
#33	Weight Calc Mode→Null変更
output2['Weight Calc Mode']=""
#34	Weight Coefficient→0変更
output2['Weight Coefficient']="0"
#35	Weight Calc→Null変更
output2['Weight Calc']=""
#36	Supplier Code→ECAL変更
output2['Supplier Code']="ECAL"
#37	Spec Condition Code→Null変更
output2['Spec Condition Code']=""
#38	Alt Dsct Rt:P 1→0変更
output2['Alt Dsct Rt:P 1']="0"
#39	Alt Dsct Rt:P 2→0変更
output2['Alt Dsct Rt:P 2']="0"
#40	Alt Dsct Rt:P 3→0変更
output2['Alt Dsct Rt:P 3']="0"
#41	Alt Dsct Rt:P 4→0変更
output2['Alt Dsct Rt:P 4']="0"
#42	Alt Dsct Rt:P 5→0変更
output2['Alt Dsct Rt:P 5']="0"
#43	Alt Dsct Rt:P 6→0変更
output2['Alt Dsct Rt:P 6']="0"
#44	Alt Dsct Rt:P 7→0変更
output2['Alt Dsct Rt:P 7']="0"
#45	Alt Dsct Rt:P 8→0変更
output2['Alt Dsct Rt:P 8']="0"
#46	Alt Dsct Rt:P 9→0変更
output2['Alt Dsct Rt:P 9']="0"
#47	Alt Dsct Rt:P 10→0変更
output2['Alt Dsct Rt:P 10']="0"
#48	Country Of Origin→192変更
output2['Country Of Origin']="192"
#49	Production Days Count→"4"変更
output2['Production Days Count']="4"
#50	Cutoff Time for Direct→Null変更
output2['Cutoff Time for Direct']=""
#51	Cutoff Time for 1day MTO→Null変更
output2['Cutoff Time for 1day MTO']=""
#52	Currency(Purchase) Code→Null変更
output2['Currency(Purchase) Code']=""
#53	Purchase Mode→A変更
output2['Purchase Mode']="A"
#54	IO Supply Means→Null変更
output2['IO Supply Means']=""
#55	IO Supply Means (URG)→Null変更
output2['IO Supply Means (URG)']=""
#56	Express T Production LT→0変更
output2['Express T Production LT']="0"
#57	Apply TI to Plant 1→0変更
output2['Apply TI to Plant 1']="0"
#58	Apply TI to Plant 2→0変更
output2['Apply TI to Plant 2']="0"
#59	Apply TI to Plant 3→0変更
output2['Apply TI to Plant 3']="0"
#60	Apply TI to Plant 4→0変更
output2['Apply TI to Plant 4']="0"
#61	Apply TI to Plant 5→0変更
output2['Apply TI to Plant 5']="0"
#62	Apply TI to Plant 6→0変更
output2['Apply TI to Plant 6']="0"
#63	Apply TI to Plant 7→0変更
output2['Apply TI to Plant 7']="0"
#64	Apply TI to Plant 8→0変更
output2['Apply TI to Plant 8']="0"
#65	Apply TI to Plant 9→0変更
output2['Apply TI to Plant 9']="0"
#66	Partial Delivery Threshold→0変更
output2['Partial Delivery Threshold']="0"
#67	Express L Calc Type for Sales→0変更
output2['Express L Calc Type for Sales']="0"
#68	Express L Message Code→Null変更
output2['Express L Message Code']=""
#69	Express L Supplier Code→Null変更
output2['Express L Supplier Code']=""
#70	Express L Dsct Rt:S 1→0変更
output2['Express L Dsct Rt:S 1']="0"
#71	Express L Dsct Rt:P 1→0変更
output2['Express L Dsct Rt:P 1']="0"
#72	Express L Slide Days 1→0変更
output2['Express L Slide Days 1']="0"
#73	Express L Dsct Rt:S 2→0変更
output2['Express L Dsct Rt:S 2']="0"
#74	Express L Dsct Rt:P 2→0変更
output2['Express L Dsct Rt:P 2']="0"
#75	Express L Slide Days 2→0変更
output2['Express L Slide Days 2']="0"
#76	Express L Dsct Rt:S 3→0変更
output2['Express L Dsct Rt:S 3']="0"
#77	Express L Dsct Rt:P 3→0変更
output2['Express L Dsct Rt:P 3']="0"
#78	Express L Slide Days 3→0変更
output2['Express L Slide Days 3']="0"
#79	Express L Dsct Rt:S 4→0変更
output2['Express L Dsct Rt:S 4']="0"
#80	Express L Dsct Rt:P 4→0変更
output2['Express L Dsct Rt:P 4']="0"
#81	Express L Slide Days 4→0変更
output2['Express L Slide Days 4']="0"
#82	Express L Dsct Rt:S 5→0変更
output2['Express L Dsct Rt:S 5']="0"
#83	Express L Dsct Rt:P 5→0変更
output2['Express L Dsct Rt:P 5']="0"
#84	Express L Slide Days 5→0変更
output2['Express L Slide Days 5']="0"
#85	Express L Dsct Rt:S 6→0変更
output2['Express L Dsct Rt:S 6']="0"
#86	Express L Dsct Rt:P 6→0変更
output2['Express L Dsct Rt:P 6']="0"
#87	Express L Slide Days 6→0変更
output2['Express L Slide Days 6']="0"
#88	Express L Dsct Rt:S 7→0変更
output2['Express L Dsct Rt:S 7']="0"
#89	Express L Dsct Rt:P 7→0変更
output2['Express L Dsct Rt:P 7']="0"
#90	Express L Slide Days 7→0変更
output2['Express L Slide Days 7']="0"
#91	Express L Dsct Rt:S 8→0変更
output2['Express L Dsct Rt:S 8']="0"
#92	Express L Dsct Rt:P 8→0変更
output2['Express L Dsct Rt:P 8']="0"
#93	Express L Slide Days 8→0変更
output2['Express L Slide Days 8']="0"
#94	Express L Dsct Rt:S 9→0変更
output2['Express L Dsct Rt:S 9']="0"
#95	Express L Dsct Rt:P 9→0変更
output2['Express L Dsct Rt:P 9']="0"
#96	Express L Slide Days 9→0変更
output2['Express L Slide Days 9']="0"
#97	Express L Dsct Rt:S 10→0変更
output2['Express L Dsct Rt:S 10']="0"
#98	Express L Dsct Rt:P 10→0変更
output2['Express L Dsct Rt:P 10']="0"
#99	Express L Slide Days 10→0変更
output2['Express L Slide Days 10']="0"
#100	Cutoff Time for TI to Plant 1→””変更
output2['Cutoff Time for TI to Plant 1']=""
#101	Cutoff Time for TI to Plant 2→変更
output2['Cutoff Time for TI to Plant 2']=""
#102	Express T Calc Type for Sales→"0"
output2['Express T Calc Type for Sales']="0"
#103	Express T Sales Pc/Unit→""
output2['Express T Sales Pc/Unit']="0"
#104	Express A Calc Type for Sales→""
output2['Express A Calc Type for Sales']="0"
#105	Express A Sales Pc/Unit→""
output2['Express A Sales Pc/Unit']="0"
#106	Special Express A Calc Type for Sales→""
output2['Special Express A Calc Type for Sales']="0"
#107	Special Express A Sales Pc/Unit→""
output2['Special Express A Sales Pc/Unit']="0"
#108	Express B Calc Type for Sales→""
output2['Express B Calc Type for Sales']="0"
#109	Express B Sales Pc/Unit→""
output2['Express B Sales Pc/Unit']="0"
#110	Express C Calc Type for Sales→""
output2['Express C Calc Type for Sales']="0"
#111	Express C Sales Pc/Unit→""
output2['Express C Sales Pc/Unit']="0"
#112	Express T Days TS→""
output2['Express T Days TS']="0"
#113	Express A Days TS→""
output2['Express A Days TS']="0"
#114	Express B Days TS→""
output2['Express B Days TS']="0"
#115	Express C Days TS→""
output2['Express C Days TS']="0"
#116	Express A Direct Ship Flg→""
output2['Express A Direct Ship Flg']="0"
#117	Express B Direct Ship Flg→""
output2['Express B Direct Ship Flg']="0"
#118	Express C Direct Ship Flg→""
output2['Express C Direct Ship Flg']="0"
#119	Express T Direct Ship Flg→""
output2['Express T Direct Ship Flg']="0"
#114　Prod Mst for Alt Supplier→0変更
output2['Prod Mst for Alt Supplier']=0

bunseki = output2['Classify Code']
bunseki = bunseki.drop_duplicates()

    # 現法毎にファイル出力
sub_name = ['CHN', 'GRM', 'HKG', 'IND', 'JKT', 'KOR', 'MEX', 'MJP', 'MYS', 'SGP', 'THA', 'TIW', 'USA', 'VNM']
for v in sub_name:
    sub_up0 = output2[output2['Subsidiary Code'] == v].copy()
    classify = bunseki
    for w in classify:
        sub_up = sub_up0[sub_up0['Classify Code'] == w].copy()
        if len(sub_up) > 0:
            sub_up1 = sub_up.iloc[:1048574, :].copy()
            sub_up1 = x_header.append(sub_up1, sort=False)
            sub_up_name =path + '/4.output/FCN_to_ECAL_' + v + w +'_Productmst.txt'
            sub_up1.to_csv(sub_up_name, sep='\t', encoding='utf_16', quotechar='"', line_terminator='\r\n', index=False)
            if len(sub_up) > 1048574:
                sub_up2 = sub_up.iloc[1048574:, :].copy()
                sub_up2 = x_header.append(sub_up2, sort=False)
                sub_up_name =path + '/4.output/FCN_to_ECAL_' + v + w +'_Productmst2.txt'
                sub_up2.to_csv(sub_up_name, sep='\t', encoding='utf_16', quotechar='"', line_terminator='\r\n', index=False)




  #sub_up_name = a_pass + '_' + v + '_Productmst_filled.xlsx'
        #sub_up1.to_excel(sub_up_name, index=False)



# XXX行を戻す
#output2 = x_header.append(output2, sort=False)


#output2.to_csv(path + '/4.output/output(FCN_to_ECAL).txt', sep='\t', encoding='utf_16', index=False)






print('finsh')
