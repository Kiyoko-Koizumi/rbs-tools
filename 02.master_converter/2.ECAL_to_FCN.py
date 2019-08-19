#商品マスタ　ECALtoFCN

import pandas as pd
import xlrd
import os
import numpy as np

path = '//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_FCN_Master'




#D/Lしたmstの格納場所の参照
pmst= pd.read_csv(path + '/ZETTA_DL_MST_TEXT/2.ECAL_to_FCN/PRODUCT_MST.txt', sep='\t', encoding='utf_16', dtype=object,engine='python', error_bad_lines=False)

# XXXをxheaderに格納
xheader =pmst [pmst['Subsidiary Code'] == 'XXX']

# XXXを除く
pmst = pmst[pmst['Subsidiary Code'] != 'XXX']



#参照先の対象インナー
reference = pd.read_excel(path + '/REFERENCE_EXECL/2.reference_ECAL_to_FCN.xlsx',dtype={'Inner Code':object})
#GTI
gti = pd.read_excel(path + '/IROIRO/GTI.xlsx',dtype={'Inner Code':object})
#最後の列にGTIのTを追加
gti= gti.drop(['CLASSIFY_CD','TYPE','PRODUCT_CD','PRODUCT_NM','MAKER_CD'],axis=1)
gti.loc[:,'G-TI'] = "T"


#中国仕入先全部_CHN_Supplier_CD  CHN_Supplier
chnsup = pd.read_excel(path + '/IROIRO/CHN_Supplier_CD.xlsx',dtype={'Inner Code':object})
chnsup = chnsup.drop(['Classify_Code','Classify_Name','Type','Product_Code'],axis=1)

#仕入先とGTIのmerge
chnsup = pd.merge(chnsup,gti,on=['Inner Code'],how='left')
chnsup.loc[:,'GTICODE']=(chnsup['CHN_Supplier'].str[1:] ) + (chnsup['G-TI'])

#GTI対象はインナーにTを追加
chnsup = pd.merge(chnsup,gti, on=['Inner Code'], how='left')

#LTタイム　CHN_production_LT
lt = pd.read_excel(path + '/IROIRO/CHN_production_LT.xlsx',dtype={'Inner Code':object})
lt = lt.drop(['CLASSIFY_CD','CLASSIFY_NM','PRODUCT_CD','SUPPLIER_CD','TI_FLG'],axis=1)
#IO supply Means
io = pd.read_excel(path + '/IROIRO/IO_Supply_Means.xlsx',dtype={'Inner Code':object})
#urethane
Urethane = pd.read_excel(path + '/IROIRO/Urethane.xlsx',dtype={'Inner Code':object})

#輸出禁止品除外（対象現法が台湾のみ適用）
TIW = pd.read_excel(path + '/IROIRO/TIW.xlsx',dtype={'Inner Code':object})
TIW=TIW.drop(['No','CLASSIFY_CD','CLASSIFY_NM','Type','Model','TIW_DATE','TIW_SUPPLIER','CHN_DATE','CHN_SUPPLIER'],axis=1)
#台湾輸出禁止品にフラグ1を挿入
TIW.loc[:, 'TIW_FLG'] = '1'


#元のマスタと対象インナー抽出
output1 = pd.merge(pmst,    reference, on =['Inner Code'],      how='inner')
#output1と輸出禁止品
output2 = pd.merge(output1, TIW,       on =['Inner Code'],      how='left')
output3 = pd.merge(output2, chnsup,    on =['Inner Code'],      how='left')
output4 = pd.merge(output3, lt,        on =['Inner Code'],      how='left')
output5 = pd.merge(output4, io,        on =['Subsidiary Code'], how='left')
output5.loc[:, 'catalogdays'] = output5.loc[:,'Production_LT'] + output5.loc[:,'Days']


#TIW_FLGを台湾現法以外はNULLに変更
output5.loc[output5['Subsidiary Code']!= 'TIW', 'TIW_FLG'] = '0'

#輸出禁止フラグ1を削除
output5 = output5[output4['TIW_FLG'] != '1']

#1_Process Mode→2変更
output5.loc[:, 'Process Mode'] = '2'

#4_Production LT→0変更
output5.loc[:, 'Production LT']='0'
#5_Slide Purchase Pc/Unit 1→0変更
output5.loc[:, 'Slide Purchase Pc/Unit 1']='0'
#6_Slide Production LT 1→0変更
output5.loc[:, 'Slide Production LT 1']='0'
#7_Slide Days TS 1→0変更
output5.loc[:, 'Slide Days TS 1']='0'
#8_Slide Purchase Pc/Unit 2→0変更
output5.loc[:, 'Slide Purchase Pc/Unit 2']='0'
#9_Slide Production LT 2→0変更
output5.loc[:, 'Slide Production LT 2']='0'
#10_Slide Days TS 2→0変更
output5.loc[:, 'Slide Days TS 2']='0'
#11_Slide Purchase Pc/Unit 3→0変更
output5.loc[:, 'Slide Purchase Pc/Unit 3']='0'
#12_Slide Production LT 3→0変更
output5.loc[:, 'Slide Production LT 3']='0'
#13_Slide Days TS 3→0変更
output5.loc[:, 'Slide Days TS 3']='0'
#14_Slide Purchase Pc/Unit 4→0変更
output5.loc[:, 'Slide Purchase Pc/Unit 4']='0'
#15_Slide Production LT 4→0変更
output5.loc[:, 'Slide Production LT 4']='0'
#16_Slide Days TS 4→0変更
output5.loc[:, 'Slide Days TS 4']='0'
#17_Slide Purchase Pc/Unit 5→0変更
output5.loc[:, 'Slide Purchase Pc/Unit 5']='0'
#18_Slide Production LT 5→0変更
output5.loc[:, 'Slide Production LT 5']='0'
#19_Slide Days TS 5→0変更
output5.loc[:, 'Slide Days TS 5']='0'
#20_Slide Purchase Pc/Unit 6→0変更
output5.loc[:, 'Slide Purchase Pc/Unit 6']='0'
#21_Slide Production LT 6→0変更
output5.loc[:, 'Slide Production LT 6']='0'
#22_Slide Days TS 6→0変更
output5.loc[:, 'Slide Days TS 6']='0'
#23_Slide Purchase Pc/Unit 7→0変更
output5.loc[:, 'Slide Purchase Pc/Unit 7']='0'
#24_Slide Production LT 7→0変更
output5.loc[:, 'Slide Production LT 7']='0'
#25_Slide Days TS 7→0変更
output5.loc[:, 'Slide Days TS 7']='0'
#26_Slide Purchase Pc/Unit 8→0変更
output5.loc[:, 'Slide Purchase Pc/Unit 8']='0'
#27_Slide Production LT 8→0変更
output5.loc[:, 'Slide Production LT 8']='0'
#28_Slide Days TS 8→0変更
output5.loc[:, 'Slide Days TS 8']='0'
#29_Slide Purchase Pc/Unit 9→0変更
output5.loc[:, 'Slide Purchase Pc/Unit 9']='0'
#30_Slide Production LT 9→0変更
output5.loc[:, 'Slide Production LT 9']='0'
#31_Slide Days TS 9→0変更
output5.loc[:, 'Slide Days TS 9']='0'
#32_Slide Purchase Pc/Unit 10→0変更
output5.loc[:, 'Slide Purchase Pc/Unit 10']='0'
#33_Slide Production LT 10→0変更
output5.loc[:, 'Slide Production LT 10']='0'
#34_Slide Days TS 10→0変更
output5.loc[:, 'Slide Days TS 10']='0'
#35_Express T Purchase Pc/Unit→0変更
output5.loc[:, 'Express T Purchase Pc/Unit']='0'
#36_Express A Calc Type for Sales→0変更
output5.loc[:, 'Express A Calc Type for Sales']='0'
#37_Express A Sales Pc/Unit→0変更
output5.loc[:, 'Express A Sales Pc/Unit']='0'
#38_Express A Calc Type for Purchase→0変更
output5.loc[:, 'Express A Calc Type for Purchase']='0'
#39_Express A Purchase Pc/Unit→0変更
output5.loc[:, 'Express A Purchase Pc/Unit']='0'
#40_Express A Production LT→0変更
output5.loc[:, 'Express A Production LT']='0'
#41_Express B Purchase Pc/Unit→0変更
output5.loc[:, 'Express B Purchase Pc/Unit']='0'
#42_Express B Production LT→0変更
output5.loc[:, 'Express B Production LT']='0'
#43_Express C Purchase Pc/Unit→0変更
output5.loc[:, 'Express C Purchase Pc/Unit']='0'
#44_Express C Production LT→0変更
output5.loc[:, 'Express C Production LT']='0'
#45_Weight→0変更
output5.loc[:, 'Weight']='0'
#46_Weight Calc Mode→変更
output5.loc[:, 'Weight Calc Mode']=''
#47_Weight Coefficient→0変更
output5.loc[:, 'Weight Coefficient']='0'
#48_Weight Calc→変更
output5.loc[:, 'Weight Calc']=''
#49_Supplier Code→中国マスタを参照して　0FCN 0AIO 0TYO の後ろ三文字とTI品ならT　非TI品ならXをつける
output5.loc[output5["GTICODE"].notnull(), 'Supplier Code']=output5["GTICODE"]

output5.loc[output5['Subsidiary Code']!= 'TIW', 'TIW_FLG'] = '0'
#50_Spec Condition Code→変更
output5.loc[:, 'Spec Condition Code']=''
#51_Alt Dsct Rt:P 1→0変更
output5.loc[:, 'Alt Dsct Rt:P 1']='0'
#52_Alt Dsct Rt:P 2→0変更
output5.loc[:, 'Alt Dsct Rt:P 2']='0'
#53_Alt Dsct Rt:P 3→0変更
output5.loc[:, 'Alt Dsct Rt:P 3']='0'
#54_Alt Dsct Rt:P 4→0変更
output5.loc[:, 'Alt Dsct Rt:P 4']='0'
#55_Alt Dsct Rt:P 5→0変更
output5.loc[:, 'Alt Dsct Rt:P 5']='0'
#56_Alt Dsct Rt:P 6→0変更
output5.loc[:, 'Alt Dsct Rt:P 6']='0'
#57_Alt Dsct Rt:P 7→0変更
output5.loc[:, 'Alt Dsct Rt:P 7']='0'
#58_Alt Dsct Rt:P 8→0変更
output5.loc[:, 'Alt Dsct Rt:P 8']='0'
#59_Alt Dsct Rt:P 9→0変更
output5.loc[:, 'Alt Dsct Rt:P 9']='0'
#60_Alt Dsct Rt:P 10→0変更
output5.loc[:, 'Alt Dsct Rt:P 10']='0'
#61_Country Of Origin→105変更
output5.loc[:, 'Country Of Origin']='105'
#62_Production Days Count→変更
output5.loc[:, 'Production Days Count']='4'
#63_Cutoff Time for Direct→変更
output5.loc[:, 'Cutoff Time for Direct']=''
#64_Cutoff Time for 1day MTO→変更
output5.loc[:, 'Cutoff Time for 1day MTO']=''
#65_Currency(Purchase) Code→変更
output5.loc[:, 'Currency(Purchase) Code']=''
#66_Purchase Mode→A変更
output5.loc[:, 'Purchase Mode']='A'
#67_IO Supply Means→変更
output5.loc[:, 'IO Supply Means']=''
#68_IO Supply Means (URG)→変更
output5.loc[:, 'IO Supply Means (URG)']=''
#69_Days to Ship on Catalog→IIf(IsNull(.loc[:, CHN_Lnk_Product_ALL]..loc[:, PRODUCT_CD]),.loc[:, tmpProduct]..loc[:, CATALOG_DAYS],IIf(.loc[:, tmpProduct]..loc[:, SUBSIDIARY_CD] In (""KOR"",""THA"",""SGP"",""MYS"",""VNM"",""TIW""),.loc[:, CHN_Lnk_Product_ALL]..loc[:, CATALOG_DAYS]+2,IIf(.loc[:, tmpProduct]..loc[:, SUBSIDIARY_CD] In (""GRM"",""USA""),.loc[:, CHN_Lnk_Product_ALL]..loc[:, CATALOG_DAYS]+3,.loc[:, tmpProduct]..loc[:, CATALOG_DAYS])))現法が増えた時の対応が必要
#output5.loc[:,['Days to Ship on Catalog']=output4(['Subsidiary Code'] ==["KOR","THA","SGP","MYS","VNM","TIW"],['Production_LT']+2)
#「IO_Supply_Means.xlsx」にDays_Tsを追加して対応する変更"


#70_Express T Days TS→0変更
output5.loc[:, 'Express T Days TS']='0'
#71_Express A Days TS→0変更
output5.loc[:, 'Express A Days TS']='0'
#72_Express B Days TS→0変更
output5.loc[:, 'Express B Days TS']='0'
#73_Express C Days TS→0変更
output5.loc[:, 'Express C Days TS']='0'
#74_Apply TI to Plant 1→変更
output5.loc[:, 'Apply TI to Plant 1']=''
#75_Cutoff Time for TI to Plant 1→変更
output5.loc[:, 'Cutoff Time for TI to Plant 1']=''
#76_Apply TI to Plant 2→変更
output5.loc[:, 'Apply TI to Plant 2']=''
#77_Cutoff Time for TI to Plant 2→変更
output5.loc[:, 'Cutoff Time for TI to Plant 2']=''
#78_Apply TI to Plant 3→変更
output5.loc[:, 'Apply TI to Plant 3']=''
#79_Cutoff Time for TI to Plant 3→変更
output5.loc[:, 'Cutoff Time for TI to Plant 3']=''
#80_Apply TI to Plant 4→変更
output5.loc[:, 'Apply TI to Plant 4']=''
#81_Cutoff Time for TI to Plant 4→変更
output5.loc[:, 'Cutoff Time for TI to Plant 4']=''
#82_Apply TI to Plant 5→変更
output5.loc[:, 'Apply TI to Plant 5']=''
#83_Cutoff Time for TI to Plant 5→変更
output5.loc[:, 'Cutoff Time for TI to Plant 5']=''
#84_Apply TI to Plant 6→変更
output5.loc[:, 'Apply TI to Plant 6']=''
#85_Cutoff Time for TI to Plant 6→変更
output5.loc[:, 'Cutoff Time for TI to Plant 6']=''
#86_Apply TI to Plant 7→変更
output5.loc[:, 'Apply TI to Plant 7']=''
#87_Cutoff Time for TI to Plant 7→変更
output5.loc[:, 'Cutoff Time for TI to Plant 7']=''
#88_Apply TI to Plant 8→変更
output5.loc[:, 'Apply TI to Plant 8']=''
#89_Cutoff Time for TI to Plant 8→変更
output5.loc[:, 'Cutoff Time for TI to Plant 8']=''
#90_Apply TI to Plant 9→変更
output5.loc[:, 'Apply TI to Plant 9']=''
#91_Cutoff Time for TI to Plant 9→変更
output5.loc[:, 'Cutoff Time for TI to Plant 9']=''
#92_Partial Delivery Threshold→0変更
output5.loc[:, 'Partial Delivery Threshold']='0'
#93_Express L Calc Type for Sales→0変更
output5.loc[:, 'Express L Calc Type for Sales']='0'
#94_Express L Message Code→変更
output5.loc[:, 'Express L Message Code']=''
#95_Express L Supplier Code→変更
output5.loc[:, 'Express L Supplier Code']=''
#96_Express L Dsct Rt:S 1→0変更
output5.loc[:, 'Express L Dsct Rt:S 1']='0'
#97_Express L Dsct Rt:P 1→0変更
output5.loc[:, 'Express L Dsct Rt:P 1']='0'
#98_Express L Slide Days 1→0変更
output5.loc[:, 'Express L Slide Days 1']='0'
#99_Express L Dsct Rt:S 2→0変更
output5.loc[:, 'Express L Dsct Rt:S 2']='0'
#100_Express L Dsct Rt:P 2→0変更
output5.loc[:, 'Express L Dsct Rt:P 2']='0'
#101_Express L Slide Days 2→0変更
output5.loc[:, 'Express L Slide Days 2']='0'
#102_Express L Dsct Rt:S 3→0変更
output5.loc[:, 'Express L Dsct Rt:S 3']='0'
#103_Express L Dsct Rt:P 3→0変更
output5.loc[:, 'Express L Dsct Rt:P 3']='0'
#104_Express L Slide Days 3→0変更
output5.loc[:, 'Express L Slide Days 3']='0'
#105_Express L Dsct Rt:S 4→0変更
output5.loc[:, 'Express L Dsct Rt:S 4']='0'
#106_Express L Dsct Rt:P 4→0変更
output5.loc[:, 'Express L Dsct Rt:P 4']='0'
#107_Express L Slide Days 4→0変更
output5.loc[:, 'Express L Slide Days 4']='0'
#108_Express L Dsct Rt:S 5→0変更
output5.loc[:, 'Express L Dsct Rt:S 5']='0'
#109_Express L Dsct Rt:P 5→0変更
output5.loc[:, 'Express L Dsct Rt:P 5']='0'
#110_Express L Slide Days 5→0変更
output5.loc[:, 'Express L Slide Days 5']='0'
#111_Express L Dsct Rt:S 6→0変更
output5.loc[:, 'Express L Dsct Rt:S 6']='0'
#112_Express L Dsct Rt:P 6→0変更
output5.loc[:, 'Express L Dsct Rt:P 6']='0'
#113_Express L Slide Days 6→0変更
output5.loc[:, 'Express L Slide Days 6']='0'
#114_Express L Dsct Rt:S 7→0変更
output5.loc[:, 'Express L Dsct Rt:S 7']='0'
#115_Express L Dsct Rt:P 7→0変更
output5.loc[:, 'Express L Dsct Rt:P 7']='0'
#116_Express L Slide Days 7→0変更
output5.loc[:, 'Express L Slide Days 7']='0'
#117_Express L Dsct Rt:S 8→0変更
output5.loc[:, 'Express L Dsct Rt:S 8']='0'
#118_Express L Dsct Rt:P 8→0変更
output5.loc[:, 'Express L Dsct Rt:P 8']='0'
#119_Express L Slide Days 8→0変更
output5.loc[:, 'Express L Slide Days 8']='0'
#120_Express L Dsct Rt:S 9→0変更
output5.loc[:, 'Express L Dsct Rt:S 9']='0'
#121_Express L Dsct Rt:P 9→0変更
output5.loc[:, 'Express L Dsct Rt:P 9']='0'
#122_Express L Slide Days 9→0変更
output5.loc[:, 'Express L Slide Days 9']='0'
#123_Express L Dsct Rt:S 10→0変更
output5.loc[:, 'Express L Dsct Rt:S 10']='0'
#124_Express L Dsct Rt:P 10→0変更
output5.loc[:, 'Express L Dsct Rt:P 10']='0'
#125_Express L Slide Days 10→0変更
output5.loc[:, 'Express L Slide Days 10']='0'





#不要カラム削除　axi=1
output5=output5.drop(['IO Supply Means_x','TIW_FLG','CHN_Supplier','G-TI_x','GTICODE','G-TI_y','Production_LT','IO Supply Means_y','Days','catalogdays'],axis=1)

# XXX行を戻す
output5 = xheader.append(output5, sort=False)



output5.to_csv(path + '/OUTPUT/output(ECAL_to_FCN_).txt', sep='\t', encoding='utf_16', index=False)




print('finsh')