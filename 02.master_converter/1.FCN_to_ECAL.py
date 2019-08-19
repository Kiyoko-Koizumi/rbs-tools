#商品マスタ　FCNtoECAL



import pandas as pd

import xlrd


path = '//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_FCN_Master'

#格納場所指定 & textをcsvに変換 \tタブ　sep=','csv
pmst = pd.read_csv(path + '/ZETTA_DL_MST_TEXT/1.FCN_to_ECAL/PRODUCT_MST.txt', sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False)

# XXXをxheaderに格納
xheader = pmst[pmst['Subsidiary Code'] == 'XXX']
# XXXを除く
pmst = pmst[pmst['Subsidiary Code'] != 'XXX']

#参照先の対象インナー
df = pd.read_excel(path + '/REFERENCE_EXECL/1.reference_FCN_to_ECAL.xlsx',dtype={'Inner Code':object})

#輸出禁止品除外（対象現法が台湾のみ適用）
TIW = pd.read_excel(path + '/IROIRO/TIW.xlsx',dtype={'Inner Code':object})
TIW=TIW.drop(['No','CLASSIFY_CD','CLASSIFY_NM','Type','Model','TIW_DATE','TIW_SUPPLIER','CHN_DATE','CHN_SUPPLIER'],axis=1)
#台湾輸出禁止品にフラグ1を挿入
TIW.loc[:, 'TIW_FLG'] = '1'

#pmst[pmst['Inner Code'] == df['Inner Code']]
output1 = pd.merge(pmst, df, on=['Inner Code'], how= 'inner')
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
output2['Apply TI to Plant 1']=""
#58	Apply TI to Plant 2→0変更
output2['Apply TI to Plant 2']=""
#59	Apply TI to Plant 3→0変更
output2['Apply TI to Plant 3']=""
#60	Apply TI to Plant 4→0変更
output2['Apply TI to Plant 4']=""
#61	Apply TI to Plant 5→0変更
output2['Apply TI to Plant 5']=""
#62	Apply TI to Plant 6→0変更
output2['Apply TI to Plant 6']=""
#63	Apply TI to Plant 7→0変更
output2['Apply TI to Plant 7']=""
#64	Apply TI to Plant 8→0変更
output2['Apply TI to Plant 8']=""
#65	Apply TI to Plant 9→0変更
output2['Apply TI to Plant 9']=""
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
#102	Express T Calc Type for Sales→""
output2['Express T Calc Type for Sales']=""
#103	Express T Sales Pc/Unit→""
output2['Express T Sales Pc/Unit']=""
#104	Express A Calc Type for Sales→""
output2['Express A Calc Type for Sales']=""
#105	Express A Sales Pc/Unit→""
output2['Express A Sales Pc/Unit']=""
#106	Special Express A Calc Type for Sales→""
output2['Special Express A Calc Type for Sales']=""
#107	Special Express A Sales Pc/Unit→""
output2['Special Express A Sales Pc/Unit']=""
#108	Express B Calc Type for Sales→""
output2['Express B Calc Type for Sales']=""
#109	Express B Sales Pc/Unit→""
output2['Express B Sales Pc/Unit']=""
#110	Express C Calc Type for Sales→""
output2['Express C Calc Type for Sales']=""
#111	Express C Sales Pc/Unit→""
output2['Express C Sales Pc/Unit']=""
#112	Express T Days TS→""
output2['Express T Days TS']=""
#113	Express A Days TS→""
output2['Express A Days TS']=""
#114	Express B Days TS→""
output2['Express B Days TS']=""
#115	Express C Days TS→""
output2['Express C Days TS']=""
#116	Express A Direct Ship Flg→""
output2['Express A Direct Ship Flg']=""
#117	Express B Direct Ship Flg→""
output2['Express B Direct Ship Flg']=""
#118	Express C Direct Ship Flg→""
output2['Express C Direct Ship Flg']=""
#119	Express T Direct Ship Flg→""
output2['Express T Direct Ship Flg']=""
#114　Prod Mst for Alt Supplier→0変更
output2['Prod Mst for Alt Supplier']=0






# XXX行を戻す
output2 = xheader.append(output2, sort=False)


output2.to_csv(path + '/OUTPUT/output(FCN_to_ECAL).txt', sep='\t', encoding='utf_16', index=False)






print('finsh')