# coding: utf-8
# UNION_DL_DATA ver1.0 新規作成
# UNION_DL_DATA ver1.1 カラム名を限定
# UNION_DL_DATA ver2.0 inputデータ構造を出力
# UNION_DL_DATA ver2.1 output項目追加、エクセルで出力
# UNION_DL_DATA ver2.3 ダブルコーテーション対策
# UNION_DL_DATA ver2.4 MCコード”NA”が消えないようにする
# UNION_DL_DATA ver2.5 重量を残す
# UNION_DL_DATA ver2.6 ALLで取り込んだファイルを現法毎に分ける
# UNION_DL_DATA ver2.6.1 現法別に分ける際フォルダがなかったら作成する
# UNION_DL_DATA ver2.6.2 1048576Rec以下ならばExcel保存、以外は.tsvで保存

# モジュールのインポート
import os, tkinter.filedialog, tkinter.messagebox
import csv
import pandas as pd
import tkinter as tk
import tkinter.ttk as ttk
import sqlite3

# csv.field_size_limit(1000000000)

#font="utf-8"
font='shift_jisx0213'

# スクリプトのあるディレクトリの絶対パスを取得
# __name__ → Python のプログラムがどこから呼ばれて実行されているかを格納
script_pass = os.path.dirname(os.path.abspath(__name__))

pg_name =()
Inner7_M = ()

def inner7():
    # SELECTボタンが押されたときの動き
    def getitemcode(item_name):
        global pg_name
        pg_name = item_name
        root.destroy()

    global Inner7_M
    # スクリプトのあるディレクトリの絶対パスを取得
    inner7pass = os.path.dirname(os.path.abspath(__name__))

    # inner7マスタを読み込む
    os.chdir(inner7pass)
    Inner7_M = pd.read_csv('inner7.txt', encoding='shift_jisx0213', dtype='object', index_col=None)
    pg = Inner7_M.drop_duplicates(subset=['製造GR'], keep='first', inplace=False)  # 重複削除
    pg = pg.loc[::, ['製造GR']]
    pg = pg.T
    l_pg = pg.values.tolist()
    list_pg = l_pg[0]

    # 抽出したい製造グループを指定する
    # GUIの作成
    # ルートフレームの作成
    root = tk.Tk()
    # 画面を常に手前に表示
    root.attributes("-topmost", True)
    label1 = tk.Label(root,text="【製造GRを選択】",font=("",16),height=2)
    label1.pack(fill="x")

    # コンボボックスの作成(rootに配置,リストの値を編集不可(readonly)に設定)
    combo = ttk.Combobox(root, state='readonly')
    # リストの値を設定
    combo["values"] = list_pg
    # デフォルトの値を食費(index=0)に設定
    combo.current(0)
    # コンボボックスの配置
    combo.pack()

    # ボタンの作成（コールバックコマンドには、コンボボックスの値を取得する処理を定義）
    button = tk.Button(text="select",command=lambda:getitemcode(combo.get()))
    # ボタンの配置
    button.pack()

    root.mainloop()

def check_wq(list_f):
    for i in range(0,len(list_f)):
        f_name = os.path.basename(list_f[i])
        f_pass = os.path.dirname(list_f[i])
        os.chdir(f_pass)
        with open(f_name, 'r', encoding=font) as f:
            file = f.read()
            if '"' in file:
                print(f_name + 'にダブルコーテーションが含まれるため置き換えて新規に保存します')
                file = file.replace('"', '')
                f_name = 'new_' + f_name
                st = open(f_name, 'w', encoding=font)
                st.write(file)
                st.close()
                list_f[i] = f_pass + '/' + f_name

inner7()

# inner7マスタを指定のグループだけにする
Inner7_M = Inner7_M.loc[::,['製造GR', 'インナー7']]
Inner7_M.drop_duplicates(keep='first', inplace=True)#重複削除
Inner7_M = Inner7_M[Inner7_M['製造GR'] == pg_name]

# ファイル選択ダイアログの表示
root = tkinter.Tk()
# 画面を常に手前に表示
root.attributes("-topmost", True)

root.withdraw()
fTyp = [("","*")]
iDir = os.path.abspath(os.path.dirname(__file__))

rfile=0
r=0

# ここの1行を変更 askopenfilename → askopenfilenames
file = tkinter.filedialog.askopenfilenames(filetypes = fTyp,initialdir = iDir)

# 選択ファイルリスト作成
list_f = list(file)
tkinter.messagebox.showinfo('UNIONプログラム',list_f)

check_wq(list_f)

# 1つ目のファイルを開く
f_name=os.path.basename(list_f[0])
f_pass=os.path.dirname(list_f[0])
os.chdir(f_pass)

print(f_name)
# 必要な列のみ読み込む
# df = pd.read_csv(f_name, sep='\t', encoding=font, dtype=object, engine='python', error_bad_lines=False, usecols=['SUBSIDIARY_CD', 'SUPPSUB_CD','GLOBAL_NO', 'SO_DATE', 'SO_TIME', 'STOCK_DIV', 'CUST_CD', 'SHIP_TO_CD', 'MC_CD', 'INNER_CD', 'PRODUCT_CD', 'SUPPLIER_CD', 'SO_QTY', 'DELI_DIV','SSD', 'VSD', 'CUST_CATEGORY_CD', 'SUPPLIER_CATEGORY_CD', 'SUPPSUB_SUPPLIER_CD', 'SHIPMENT_FIX_DATE','MC_PLANT_DIV'])
# すべての列を読み込む
df = pd.read_csv(f_name, sep='\t', encoding=font, dtype=object, engine='python', error_bad_lines=False)

'''
#SUBSIDIARY_CD	GLOBAL_NO	SO_DATE	SO_VOUCHER_NO	SO_LINE_NO	REC_STATUS	MC_CD	CUST_CD	NTV_CUST_NAME1	SHIP_TO_CD	ECAL_CUST_CD
MEDIA_CD	CUST_SHIPMODE	QT_VOUCHER_NO	SHIPMENT_FIX_DATE	CCY_EXCHANGE_DATE	CUST_COUNTRY_CD	SHIP_TO_COUNTRY_CD
NTV_CUST_DEPT	NTV_CUST_ATTENTION	NTV_DELI_DEPT	NTV_DELI_ATTENTION	DELI_ATTENTION_CD	VOUCHER_DIV	REASON_CD
ORIGINAL_GLOBAL_NO	ORIGINAL_SO_VOUCHER_NO	ORIGINAL_DELI_NOTE_NO	ORIGINAL_SO_DATE	ORIGINAL_SO_VSD	HEADER_REF
CUST_REF	CUST_SUB_REF	PRODUCT_CD	PRODUCT_NAME	INNER_CD	HS_CD	CLASSIFY_CD	STOCK_DIV	COMPONENT_FLG	SO_QTY
UNIT_OF_MEASURE	DELI_DIV	SUPPLIER_CD	NTV1_COMPANY_NAME	WEIGHT_PER_PIECE	OTHER_AREA_SHIP_DIV	ALLOCATION_DIV
GLOBAL_NO_PO	ALLOCATION_QTY	QT_PREPARATION_DIV	MOVE_TICKET_DIV	SEND_FLG	SO_TIME	MSM_PIC	PACKING_RANK	DELI_NOTE_NO
DELI_NOTE_LINE_NO	INVOICE_NO	CARRIER_INVOICE_NO	INPUT_DIV	CARRIER_INVOICE_QTY	SPECIFY_VOUCHER_DIV	Y_PART_NO_DIV
PRODUCT_ASSORT	PRODUCT_ATTRIBUTION	CUST_SUPPLIER_CD	BILL_TO_CD	TAX_MENTION_DIV	TAX_IN_EX_DIV	CUST_LOCAL_TOWN_CD
PROD_MST_PRODUCT_ASSORT	VOUCHER_DIV_SIGN	STORK_CHARGE_EXCLUDE_FLG	QTY_SLIDE_DIV	TR_SEQ	HEAVY_FLG	EXPENSIVE_FLG	BRAND_CD
SPECIAL_DIV	WH_INPACK_SPECIFY_FLG	PRODUCT_CONTROL_DEP_CODE	WEIGHT	WEIGHT_UNIT	PACK_QTY	MC_PLANT_DIV
SUPPSUB_SPECIFY_PLANT_CD	SUPPSUB_MC_PLANT_DIV	LOGICAL_PLANT	INPACK_CHARGE_DIV	GTI_CATALOG_APPLY_FLG	GTI_CRITERIA_FLG
GTI_ORDER_CLOSING_TIME	S_CCY_RATE_PROD_CUST	S_CCY_RATE_SUPP_SUB	S_CCY_RATE_SUB_CUST	P_CCY_RATE_PROD_SUPP	P_CCY_RATE_FREIGHT_SUPPSUB
P_CCY_RATE_FREIGHT_SUPP	P_CCY_RATE_PROD_SUPPSUB	P_CCY_RATE_SUPPSUB_SUPP	P_CCY_RATE_SUPP_CUST	S_CCY_RATE_CUST_SUB_T_CD	SUPPLIER_RATE_TYPE_CD
DEEMED_STOCK_FLG	SUPPSUB_CD	SUPPSUB_SUPPLIER_CD	SUBSIDIARY_CCY_CD	CUSTSUB_SUBSIDIARY_CD	CUSTSUB_CUST_CD	CUSTSUB_SHIP_TO_CD
STORK_CHARGE_APPLY_DIV	S_U_P_STORKE_CALC_DIV	P_U_P_STORKE_CALC_DIV	BEF_SPL_DSCT_S_U_PRICE	EXCLUDE_TAX_S_U_PRICE	INCLUDE_TAX_S_U_PRICE
REGULAR_S_U_PRICE	REFERENCE_S_U_PRICE	PURCHASE_UNIT_PRICE	SUPPLIER_INV_UNIT_PRICE	CUST_CCY_P_U_PRICE	SUPPSUB_P_U_PRICE
REFERENCE_P_U_PRICE	REFERENCE_SALES_AMOUNT	BEF_DSCT_SLIDE_U_PRICE	LABELED_SLIDE_S_U_P	ADD_PROC_SLIDE_U_P	STORK_SLIDE_U_P	LABELED_NOSLIDE_U_P
ADD_PROC_NOSLIDE_U_P	STORK_NOSLIDE_U_P	S_UNIT_PRICE_CCY_CD	P_UNIT_PRICE_CCY_CD	SUPPSUB_P_U_PRICE_CCY_CD	S_CCY_RATE_CUST_SUB
P_CCY_RATE_SUPP_SUB	C_CCY_RATE_COGS	EXCLUDE_TAX_SALES_AMOUNT	SALE_UNIT_PRICE_TOTAL	BEF_DSCT_SALES_AMOUNT	DSCT_TOTAL_AMOUNT
FREIGHT_AMOUNT	INSURANCE_AMOUNT	MISC_AMOUNT	UNBILLED_AR_AMOUNT	SALES_AMOUNT1_KEY_CURRENCY	SALES_AMOUNT2_KEY_CURRENCY
SALES_COST_UNIT_PRICE	COGS_AMOUNT_KEY_CURRENCY	IMPORT_FREIGHT	IMPORT_DUTY	IMPORT_CHARGE	FACE_UNIT_PRICE	EXCLUDE_MANAGE_COST_P_U_P
REC_CHARGE	MARGIN_RATE	MARGIN_PRICE	EXPORT_FREIGHT	WEIGHT_UNIT_COST	STOCK_COST	COMPONENT_COST	INTERNATIONAL_COST
LOGISTIC_COST	INFO_COST	RESERVE_COST1	RESERVE_COST2	RESERVE_COST3	RESERVE_COST4	SUPP_SUB_IMPORT_DUTY	SUPP_SUB_IMPORT_CHARGE
SUPP_SUB_IMPORT_FREIGHT	TAX_AMOUNT	TAX_RATE	TAX_CD	CUST_TAX_FREE_FLG	PRODUCT_TAX_FREE_FLG	PROD_CUST_DSCT_DIV
PROD_CUST_DSCT_RATE	PROD_CUST_DSCT_AMOUNT	PROD_SEGMENT_DSCT_DIV	PROD_SEGMENT_DSCT_RATE	PROD_SEGMENT_DSCT_AMOUNT
MEDIA_DSCT_DIV	MEDIA_DSCT_RATE	MEDIA_DSCT_AMOUNT	SPL_DSCT_DIV	SPL_DSCT_RATE	SPL_DSCT_AMOUNT	OTHER_DSCT_AMOUNT
ACTUAL_SHIP_DAYS	SPECIFY_PRODUCTION_DAYS	SPECIFY_SHIP_DAYS	CATALOG_DAYS	STORK_T_DAYS	STORK_A_DAYS	STORK_B_DAYS
STORK_C_DAYS	REFILL_PO_DAYS	EARLY_DAYS	EARLY_CATALOG_DAYS	PRODUCTION_DAYS	SSD	VRD	VSD	CRD	SPECIFY_SSD
SPECIFY_VRD	SPECIFY_VSD	SPECIFY_CRD	SUPPSUB_SPECIFY_PROD_DAYS	SUPPSUB_SPECIFY_SHIP_DAYS	SUPPSUB_SSD	SUPPSUB_VRD
SUPPSUB_VSD	SUPPSUB_CRD	SHORTEST_SSD	SHORTEST_VRD	SHORTEST_VSD	SHORTEST_CRD	TRANSPORT_MEANS	DIRECT_SHIP_FLG	HAZARD_FLG
STOCK_PRIORITY_FLG	DATE_CALC_PATTERN	INCOTERMS	CUST_CATEGORY_CD	SUPPLIER_CATEGORY_CD	COUNTRY_OF_ORIGIN	OTHER_SYS_VOUCHER_NO
PAYMENT_TERMS	SETTLEMENT_METHOD	PAYMENT_MEANS	FRT_RECALC_FLG	CREDIT_RESERVE_NO	HISTORY_DIV	SUPPLIER_INV_AMOUNT	PURCHASE_AMOUNT
ARRIVAL_SUPP_INV_AMOUNT	ARRIVAL_PO_AMOUNT	CUST_TAX_AREA_CD	CUST_FRT_AREA_CD	CUST_SHIP_AREA_CD	M_CUST_TAX_FREE_FLG	SHIP_TAX_AREA_CD
SHIP_FRT_AREA_CD	SHIP_CUST_SHIP_AREA_CD	SHIP_TAX_FREE_FLG	SHIPMENT_TIMING_DIV	COMET_NO	DELI_NOTE_AMOUNT_PRICE	DELI_NOTE_AMOUNT_DUTY
FREIGHT_AMOUNT_PRICE	MISC_AMOUNT_PRICE	PREMIUM_AMOUNT_PRICE	TAXABLE_AMOUNT	BOX_NO	TOTAL_WEIGHT	TOTAL_QTY	SHIPMENT_FIX_DATE_YMD_FMT
ENG_HEADER_REF	NTV_CUST_SUB_REF	PROCESS_RECEIVE_DATE	PROCESS_RECEIVE_TIME	UPD_COUNT	DEL_FLG	REG_USR	REG_SYS_TIME	REG_SUBSIDIARY_TIME
REG_LOCAL_TIME	REG_PG	UPD_USR	UPD_SYS_TIME	UPD_SUBSIDIARY_TIME	UPD_LOCAL_TIME	UPD_PG	UPD_PWC
'''

# ファイルを繰り返し開き結合する
for r in range(1,len(list_f)):
    f_name=os.path.basename(list_f[r])
    print(f_name)
    # df_add = pd.read_csv(f_name, sep='\t', encoding=font, dtype=object, engine='python', error_bad_lines=False, usecols=['SUBSIDIARY_CD', 'SUPPSUB_CD','GLOBAL_NO', 'SO_DATE', 'SO_TIME', 'STOCK_DIV', 'CUST_CD', 'SHIP_TO_CD', 'MC_CD', 'INNER_CD', 'PRODUCT_CD', 'SUPPLIER_CD', 'SO_QTY', 'DELI_DIV','SSD', 'VSD', 'CUST_CATEGORY_CD', 'SUPPLIER_CATEGORY_CD', 'SUPPSUB_SUPPLIER_CD', 'SHIPMENT_FIX_DATE','MC_PLANT_DIV'])
    df_add = pd.read_csv(f_name, sep='\t', encoding=font, dtype=object, engine='python', error_bad_lines=False)
    #ファイルを追加する
    df=df.append(df_add)

# 現法毎に分けて保存する
sub_name = ['CHN', 'GRM', 'HKG', 'IND', 'JKT', 'KOR', 'MEX', 'MJP', 'MYS', 'SGP', 'THA', 'TIW', 'USA', 'VNM']
# save_pass = script_pass + '/by_Subsidiary_cd'
save_pass = f_pass + '/by_Subsidiary_cd'
if not os.path.exists(save_pass):
    os.mkdir(save_pass)
os.chdir(save_pass)
for s in range(14):
    subsidiary = sub_name[s]
    df_sub = df[df['SUBSIDIARY_CD'] == sub_name[s]].copy()
    f_name = sub_name[s] + '.tsv'
    df_sub.to_csv(f_name, sep='\t', encoding=font, quotechar='"', line_terminator='\n', index=False)

# 列を限定する
df = df[['SUBSIDIARY_CD', 'SUPPSUB_CD','GLOBAL_NO', 'SO_DATE', 'SO_TIME', 'STOCK_DIV', 'CUST_CD', 'SHIP_TO_CD', 'MC_CD', 'INNER_CD', 'PRODUCT_CD', 'SUPPLIER_CD', 'SO_QTY', 'DELI_DIV','SSD', 'VSD', 'CUST_CATEGORY_CD', 'SUPPLIER_CATEGORY_CD', 'SUPPSUB_SUPPLIER_CD', 'SHIPMENT_FIX_DATE','MC_PLANT_DIV', 'WEIGHT', 'WEIGHT_UNIT']]

# recを A調達(Sub1,Sub2),B調達 に分ける
Sub1 = df[(((df['CUST_CATEGORY_CD'] == '03') | (df['CUST_CATEGORY_CD'] == '04') | (df['CUST_CATEGORY_CD'] == '05') | (df['CUST_CATEGORY_CD'] == '06')) & ((df['SUPPLIER_CATEGORY_CD'] == '01') | (df['SUPPLIER_CATEGORY_CD'] == '02')))]
Sub2 = df[(((df['SUPPLIER_CATEGORY_CD'] == '03') | (df['SUPPLIER_CATEGORY_CD'] == '04') | (df['SUPPLIER_CATEGORY_CD'] == '05') | (df['SUPPLIER_CATEGORY_CD'] == '06')) & ((df['CUST_CATEGORY_CD'] == '01') | (df['CUST_CATEGORY_CD'] == '02'))) ]
Bcho = df[(((df['CUST_CATEGORY_CD'] == '03') | (df['CUST_CATEGORY_CD'] == '04') | (df['CUST_CATEGORY_CD'] == '05') | (df['CUST_CATEGORY_CD'] == '06')) & ((df['SUPPLIER_CATEGORY_CD'] == '03') | (df['SUPPLIER_CATEGORY_CD'] == '04') | (df['SUPPLIER_CATEGORY_CD'] == '05') | (df['SUPPLIER_CATEGORY_CD'] == '06')))]

DF_list = [Sub1, Sub2, Bcho]

# それぞれのREC数を確認
df_count = len(df)
Sub1_count = len(Sub1)
Sub2_count = len(Sub2)
Bcho_count = len(Bcho)

# メッセージを作成
OK_mes = '全てSub1,Sub2,B調達に分類できました\n' + 'input:' + str(df_count) +'REC\n' + 'Sub1:' + str(Sub1_count) +'REC\n' + 'Sub2:' + str(Sub2_count) +'REC\n' + 'B調達:' + str(Bcho_count) +'REC\n'
NG_mes = 'Sub1,Sub2,B調達に分類できないRECがありました\n' + 'input:' + str(df_count) +'REC\n' + 'Sub1:' + str(Sub1_count) +'REC\n' + 'Sub2:' + str(Sub2_count) +'REC\n' + 'B調達:' + str(Bcho_count) +'REC\n'

# inner7を列を追加しdfを３つ生成
for i in range(0,3):
    df = DF_list[i]
    df['インナー7'] = df['INNER_CD'].str[0:7]
    df =  pd.merge(df,Inner7_M,on='インナー7', how='inner')
    DF_list[i] = df


# Sub1とSub2をGlobal_Noで結合し在庫区分、仕入先、仕入先SSDを転記する、SO_DATE・SSD・VSD・SHIPPING_FIXED_DATEを日付形式に変換
Sub1 = DF_list[0]
Sub2 = DF_list[1].loc[::,['GLOBAL_NO', 'SUPPLIER_CD', 'SSD', 'STOCK_DIV']]
Sub2 = Sub2.rename(columns={'SUPPLIER_CD': 'SUPPLIER_CD2', 'SSD':'SSD2', 'STOCK_DIV':'STOCK_DIV2'})


Sub1 = pd.merge(Sub1,Sub2, on='GLOBAL_NO', how='left')
Sub1.loc[Sub1['SUPPLIER_CD2'].notnull(), 'SUPPLIER_CD'] = Sub1['SUPPLIER_CD2']
Sub1.loc[(Sub1['SUPPLIER_CD2'].isnull() & Sub1['SUPPSUB_SUPPLIER_CD'].notnull()), 'SUPPLIER_CD'] = Sub1['SUPPSUB_SUPPLIER_CD']
Sub1.loc[Sub1['SSD2'].notnull(), 'SSD'] = Sub1['SSD2']
Sub1.loc[Sub1['STOCK_DIV2'].notnull(), 'STOCK_DIV'] = Sub1['STOCK_DIV'] + Sub1['STOCK_DIV2']
Sub1.loc[Sub1['STOCK_DIV2'].isnull(), 'STOCK_DIV'] = Sub1['STOCK_DIV'] + 'Y'
Sub1.drop([ 'SUPPLIER_CD2', 'SSD2', 'STOCK_DIV2'], axis=1, inplace=True)

# 置場区分を左2桁だけ抽出
Sub1['MC_PLANT_DIV']=Sub1['MC_PLANT_DIV'].str[0:2]
DF_list[2]['MC_PLANT_DIV']=DF_list[2]['MC_PLANT_DIV'].str[0:2]

# ファイルをUnionする
Sub1 = Sub1.append(DF_list[2])
Sub1.drop(['CUST_CATEGORY_CD', 'SUPPLIER_CATEGORY_CD', 'インナー7', '製造GR'], axis=1, inplace=True)
Sub1 = Sub1.loc[:,['SUBSIDIARY_CD', 'SUPPSUB_CD','GLOBAL_NO', 'SO_DATE', 'SO_TIME', 'STOCK_DIV', 'CUST_CD', 'SHIP_TO_CD', 'MC_CD', 'INNER_CD', 'PRODUCT_CD', 'SUPPLIER_CD', 'SO_QTY', 'DELI_DIV','SSD', 'VSD', 'SHIPMENT_FIX_DATE','MC_PLANT_DIV']]
Sub1.loc[:, 'SO_DATE'] = pd.to_datetime(Sub1['SO_DATE'])
Sub1.loc[:, 'SSD'] = pd.to_datetime(Sub1['SSD'])
Sub1.loc[:, 'VSD'] = pd.to_datetime(Sub1['VSD'])
Sub1.loc[:, 'SHIPMENT_FIX_DATE'] = pd.to_datetime(Sub1['SHIPMENT_FIX_DATE'])

# 'NO'列を追加
# https://note.nkmk.me/python-pandas-reset-index/
Sub1.reset_index(inplace=True,drop=True)
Sub1.reset_index(inplace=True)
Sub1=Sub1.rename(columns={'index':'NO'})

# Sub1['NO']=0
# Sub1=Sub1.astype({'NO':int})
# i=0
# for A in Sub1.iterrows():
#     Sub1.loc[i,'NO']=i
#     i=i+1


#MC_CDの”NA”が消えてしまうので、NAを書き込む
#https://note.nkmk.me/python-pandas-where-mask/
Sub1.loc[Sub1['GLOBAL_NO'].str[:2] == "NA",'MC_CD']="NA"

if len(Sub1)<1048576:
    #エクセルで出力
    os.chdir(f_pass)
    import openpyxl
    name=pg_name + "_output.xlsx"
    Sub1.to_excel(name,index=False)
    Output_count = str(len(Sub1)) + '件抽出できました'
    tkinter.messagebox.showinfo('結果',Output_count)
else:
    # tsv出力
    os.chdir(f_pass)
    # name = pg_name + "_output.txt"
    name = pg_name + "_output.tsv"
    Sub1.to_csv(name,sep="\t",encoding=font,quotechar='"',line_terminator="\n",index=False)
    Output_count = str(len(Sub1)) + '件抽出できました'
    tkinter.messagebox.showinfo('結果',Output_count)

# メッセージを出力
if df_count == (Sub1_count + Sub2_count + Bcho_count):
    tkinter.messagebox.showinfo('読み取り結果', OK_mes)
else:
    tkinter.messagebox.showerror('読み取り結果', NG_mes)


print("Finish!")

