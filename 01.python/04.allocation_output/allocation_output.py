# coding: utf-8
# Dispatch_output 2019/1/24
# 0.1 ヘッダーの名称を変更、シミュレーション対象のデータを補完
# 0.2 日付をYYYYMMDDからYYYY/MM/DDに変換
# 0.3 Tableauに空欄が影響する列があるため、空欄を埋める
# 0.31 AWS用にallocation_outputへ変更
# 0.32 管理単位コード書き換え
# MASTER_SUPPLIER_CDを追加 git用に名称更新
# 現法仕入差額を計算
# 1レコードの中にbefore/after拠点を記載
# データ削減のため不必要な列を削除


import csv
# モジュールのインポート
import os
import pandas as pd
import sys

# from tqdm import tqdm
csv.field_size_limit(1000000000)

font = 'utf-8'
# font='shift_jisx0213'

# 引数を取得
args =sys.argv

# 読み込み
f_pass = args[1] + '/output'
os.chdir(f_pass)
Output = pd.read_csv('check_input_RBS_OUTPUT_RBS_OUTPUT.tsv', sep='\t', dtype=str)

# シミュレーション対象RECに割付仕入先フラブを立てる
Output.loc[((Output['従来生産拠点フラグ'] == '1') &
               ((Output['適用ロジック'] == 'a1') |
                (Output['適用ロジック'] == 'a2') |
                (Output['適用ロジック'] == 'a3') |
                (Output['適用ロジック'] == 'a4') |
                (Output['適用ロジック'] == 'a5') |
                (Output['適用ロジック'] == 'a6') |
                (Output['適用ロジック'] == 'z1'))), '割付仕入先フラグ'] = '1'
# シミュレーション対象RECに従来情報をコピー　RBS_受注現法コード、RBS_受注現法インナーコード、RBS_受注現法仕入先コード、RBS_管理単位コード、割振りSSD
Output.loc[(Output['割付仕入先フラグ'] == '1') & (Output['RBS_受注現法コード'].isnull()), 'RBS_受注現法コード'] = Output['実績現法コード']
Output.loc[(Output['割付仕入先フラグ'] == '1') & (Output['RBS_受注現法インナーコード'].isnull()), 'RBS_受注現法インナーコード'] = Output['インナーコード']
Output.loc[(Output['割付仕入先フラグ'] == '1') & (Output['RBS_受注現法仕入先コード'].isnull()), 'RBS_受注現法仕入先コード'] = Output['実績仕入先コード']
Output.loc[(Output['割付仕入先フラグ'] == '1') & (Output['RBS_管理単位コード'].isnull()), 'RBS_管理単位コード'] = Output['実績管理単位コード']
Output.loc[(Output['割付仕入先フラグ'] == '1') & (Output['割振りSSD'].isnull()), '割振りSSD'] = Output['受注実績SSD']

# ヘッダー名変更
Output = Output.rename(columns={"番号":"NO",
"現法コード":"SUBSIDIARY_CD",
"グローバル番号":"GLOBAL_NO",
"受注日・見積回答日":"SO_DATE",
"受注時間・見積回答時間":"SO_TIME",
"JST変換受注日・JST変換見積回答日":"SO_DATE_JST",
"JST変換受注時間・JST変換見積回答時間":"SO_TIME_JST",
"見積有効日":"QT_DEADLINE_DATE",
"見積有効時間":"QT_DEADLINE_TIME",
"JST変換見積有効日":"QT_DEADLINE_DATE_JST",
"JST変換見積有効時間":"QT_DEADLINE_TIME_JST",
"アンフィット種別":"UF_SYUBETU",
"得意先コード":"CUST_CD",
"直送先コード":"SHIP_TO_CD",
"ＭＣコード":"MC_CD",
"インナーコード":"INNER_CD",
"商品コード":"PRODUCT_CD",
"実績現法コード":"RESULTS_SUBSIDIARY_CD",
"実績仕入先コード":"RESULTS_SUPPLIER_CD",
"実績管理単位コード":"RESULTS_MANAGEMENT_UNIT_CD",
"ACE仕入先コード":"ACE_SUPPLIER_CD",
"ACE仕入先カテゴリコード":"ACE_CATEGORY_CD",
"受注実績SSD":"SO_SSD",
"見積回答SSD":"QT_SSD",
"数量":"QTY",
"納入区分":"DELI_DIV",
"顧客希望納期":"SHIPPING_FIXED_DATE",
"ACE参照スキーマ":"ACE_REF_SCHEMA",
"RBS_受注現法コード":"RBS_SUBSIDIARY_CD",
"RBS_受注現法インナーコード":"RBS_INNER_CD",
"RBS_受注現法仕入先コード":"RBS_SUPPLIER_CD",
"仕入先稼動カレンダコード":"SUPPLIER_CALENDAR_CD",
"仕入先出荷時カレンダコード":"SUPPLIER_SHIPPING_CALENDAR_CD",
"置場コード1":"MC_PLANT_CD_SUB1",
"置場コード2":"MC_PLANT_CD_SUB2",
"輸送手段1":"TRANSPORT_METHOD_SUB1",
"輸送手段2":"TRANSPORT_METHOD_SUB2",
"RBS_管理単位コード":"RBS_MANAGEMENT_UNIT_CD",
"ランデットコスト":"RBS_LANDED_COST",
"発注現法仕入値":"RBS_PURCHASE_PRICE",
"発注現法実績売値":"RBS_EXCLUDE_TAX_S_U_PRICE",
"RBS_製造原価":"RBS_MANUFACTURING_COST",
"RBS_発注先現法仕入単価":"RBS_SUPPSUB_P_U_PRICE",
"RBS_マージン単価":"RBS_MARGIN_PRICE",
"RBS_マージン率":"RBS_MARGIN_RATE",
"RBS_販管費":"RBS_REC_CHARGE",
"RBS_輸出運賃":"RBS_EXPORT_FREIGHT",
"RBS_仕入先売単価":"RBS_SUPPLIER_INV_UNIT_PRICE",
"RBS_輸入運賃":"RBS_IMPORT_FREIGHT",
"RBS_関税":"RBS_IMPORT_DUTY",
"RBS_輸入諸掛":"RBS_IMPORT_CHARGE",
"売単価通貨コード":"S_UNIT_PRICE_CCY_CD",
"仕入単価通貨コード":"P_UNIT_PRICE_CCY_CD",
"発注先現法仕入通貨コード":"SUPPSUB_P_U_PRICE_CCY_CD",
"RBS_製造LT":"RBS_SSLT",
"RBS_輸送LT":"RBS_TPLT",
"従来生産拠点フラグ":"MASTER_SUPPLIER_FLAG",
"納期考慮なし最安仕入先フラグ":"NO_DELIDATE_SUPPLIER_FLAG",
"納期考慮あり最安仕入先フラグ":"DELIDATE_SUPPLIER_FLAG",
"割付仕入先フラグ":"FIXED_SUPPLIER_FLAG",
"逆計算受注日":"SO_DATE_REVERSE",
"割振りSSD":"FIXED_SSD",
"コストダウン額":"COSTDOWN",
"発注現法仕入差額":"PURCHASE_PRICE_GAP",
"適用ロジック":"APPLY_LOGIC"})

# 日付をYYYYMMDDからYYYY/MM/DDに変換
Output.loc[Output['SO_DATE'].notnull(), 'SO_DATE'] = Output['SO_DATE'].str[0:4] + '/' + Output['SO_DATE'].str[4:6] + '/' + Output['SO_DATE'].str[6:8]
Output.loc[Output['SO_SSD'].notnull(), 'SO_SSD'] = Output['SO_SSD'].str[0:4] + '/' + Output['SO_SSD'].str[4:6] + '/' + Output['SO_SSD'].str[6:8]
Output.loc[Output['QT_SSD'].notnull(), 'QT_SSD'] = Output['QT_SSD'].str[0:4] + '/' + Output['QT_SSD'].str[4:6] + '/' + Output['QT_SSD'].str[6:8]
Output.loc[Output['SHIPPING_FIXED_DATE'].notnull(), 'SHIPPING_FIXED_DATE'] = Output['SHIPPING_FIXED_DATE'].str[0:4] + '/' + Output['SHIPPING_FIXED_DATE'].str[4:6] + '/' + Output['SHIPPING_FIXED_DATE'].str[6:8]
Output.loc[Output['FIXED_SSD'].notnull(), 'FIXED_SSD'] = Output['FIXED_SSD'].str[0:4] + '/' + Output['FIXED_SSD'].str[4:6] + '/' + Output['FIXED_SSD'].str[6:8]

# ヘッダーを取得
Output_df = Output.copy()
Output_df['Alteration'] = ''
header = Output_df.columns

# 管理単位コードを設備毎に書き換え
os.chdir('/data/rbs/mps/allocation_output')
MNG_Unit = pd.read_csv('MNG_UNIT_20170101_20181231.csv', encoding=font, dtype='object', index_col=None)
MNG_header = MNG_Unit.columns.values

Output = pd.merge(Output,MNG_Unit,left_on='PRODUCT_CD', right_on='PRODUCT_CD',how='left')

# 従来生産拠点のコードを先に転記
Output.loc[Output['RESULTS_MANAGEMENT_UNIT_CD']=='MAL','RBS_MANAGEMENT_UNIT_CD']=Output['7017']
Output.loc[Output['RESULTS_MANAGEMENT_UNIT_CD']=='AAL','RBS_MANAGEMENT_UNIT_CD']=Output['3764']
Output.loc[Output['RESULTS_MANAGEMENT_UNIT_CD']=='FAL','RBS_MANAGEMENT_UNIT_CD']=Output['0FCN']
Output.loc[Output['RESULTS_MANAGEMENT_UNIT_CD']=='SAL','RBS_MANAGEMENT_UNIT_CD']=Output['SPCM']
# R.B.S RECのみ従来生産拠点のコードに上書き
Output.loc[Output['RBS_SUPPLIER_CD']=='7017','RBS_MANAGEMENT_UNIT_CD']=Output['7017']
Output.loc[Output['RBS_SUPPLIER_CD']=='3764','RBS_MANAGEMENT_UNIT_CD']=Output['3764']
Output.loc[Output['RBS_SUPPLIER_CD']=='0FCN','RBS_MANAGEMENT_UNIT_CD']=Output['0FCN']
Output.loc[Output['RBS_SUPPLIER_CD']=='0NEW','RBS_MANAGEMENT_UNIT_CD']=Output['0FCN']
Output.loc[Output['RBS_SUPPLIER_CD']=='SPCM','RBS_MANAGEMENT_UNIT_CD']=Output['SPCM']
Output.drop(['7017', '3764_ALL', '0FCN_ALL', 'SPCM_ALL', '3764', '0FCN', 'SPCM'], axis=1, inplace=True)

# カラム順を元に戻す
Output = Output.loc[:,header]

# MASTER_SUPPLIER_CD,MASTER_PURCHASE_PRICEを追加
jri_cost = Output[Output['MASTER_SUPPLIER_FLAG'] == '1']
jri_cost = jri_cost.rename(columns={'RBS_SUPPLIER_CD': 'MASTER_SUPPLIER_CD', 'RBS_PURCHASE_PRICE': 'MASTER_PURCHASE_PRICE'})
jri_cost = jri_cost.loc[::, ['NO', 'MASTER_SUPPLIER_CD', 'MASTER_PURCHASE_PRICE']]
Output = pd.merge(Output, jri_cost, on='NO', how='left')
# RBS_SUPPLIER_CDを追加
RBS_supp = Output[Output['FIXED_SUPPLIER_FLAG'] == '1']
RBS_supp = RBS_supp.rename(columns={'RBS_SUPPLIER_CD': 'FIXED_SUPPLIER_CD'})
RBS_supp = RBS_supp.loc[::, ['NO', 'FIXED_SUPPLIER_CD']]
Output = pd.merge(Output, RBS_supp, on='NO', how='left')

# 軽量化のため不要カラムを削除
Output.drop(["SO_DATE_JST",
             "SO_TIME_JST",
             "QT_DEADLINE_DATE",
             "QT_DEADLINE_TIME",
             "QT_DEADLINE_DATE_JST",
             "QT_DEADLINE_TIME_JST",
             "CUST_CD",
             "SHIP_TO_CD",
             "RESULTS_SUBSIDIARY_CD",
             "RESULTS_MANAGEMENT_UNIT_CD",
             "ACE_SUPPLIER_CD",
             "ACE_CATEGORY_CD",
             "SO_SSD",
             "QT_SSD",
             "ACE_REF_SCHEMA",
             "RBS_SUBSIDIARY_CD",
             "RBS_INNER_CD",
             "SUPPLIER_CALENDAR_CD",
             "SUPPLIER_SHIPPING_CALENDAR_CD",
             "MC_PLANT_CD_SUB1",
             "MC_PLANT_CD_SUB2",
             "TRANSPORT_METHOD_SUB1",
             "TRANSPORT_METHOD_SUB2",
             "S_UNIT_PRICE_CCY_CD",
             "P_UNIT_PRICE_CCY_CD",
             "SUPPSUB_P_U_PRICE_CCY_CD",
             "RBS_SSLT",
             "RBS_TPLT",], axis=1, inplace=True)


#空欄を０に
Output=Output.fillna({'QT_SSD':'1899/12/30','SHIPPING_FIXED_DATE':'1899/12/30','SO_DATE_REVERSE':'1899/12/30','FIXED_SSD':'1899/12/30'})
#'RBS_MARGIN_RATE':'0',

# ファイル名変更
f_name = args[2] + '.tsv'

# ファイルアウトプット
os.chdir('/data/rbs/mps/割振り処理結果')
Output.to_csv(f_name, sep='\t', encoding=font, quotechar='"', line_terminator='\n', index=False)

print('Finish!')
