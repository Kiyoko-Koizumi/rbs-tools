# ZettaとSPCそれぞれ参照項目の設定
import pandas as pd
import numpy as np
import Header
import datetime

def SPC_P06_ProductMerge():

    r_path = 'C:/temp/■Python_SPC_Master/'  # ★作業用ローカルフォルダ
    path='//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/temp_data/'  # ★共通ファイル保存先
    print(datetime.datetime.now())

    z_p = (pd.read_csv(path + 'Zetta_Product.txt', sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    s_p = (pd.read_csv(path + 'SPC_Product.txt', sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))

    df = pd.DataFrame(pd.merge(z_p, s_p, on='Product Code', suffixes=['_z', '_s'], how='left'))
    # df.to_csv(path + '20190819_Product.txt', sep='\t', encoding='utf_16', index=False)  # Zetta_Product.txt　ALL出力

    # カラム名末尾「_z」=Zetta　「_s」=Spc
    df['Production LT_s'] = df['Production LT_s'].astype(int)   # 製作日数　数値型
    df['DaysTS'] = df['DaysTS'].astype(int) # 輸送日数　数値型
    dfs = pd.DataFrame()
    dfs['Process Mode'] = '2'  # 処理区分   なぜか？空白
    dfs['Master ID'] = '01'  # 登録区分　なぜか？空白
    dfs['Subsidiary Code'] = df['Subsidiary Code_z']  # 現法コード
    dfs['Inner Code'] = df['Inner Code_z']  # インナーコード
    dfs['Product Code'] = df['Product Code']  # 商品コード
    dfs['Stock / MTO'] = df['Stock / MTO_z']  # 在庫／受注生産品
    dfs['Product Component'] = df['Product Component_z']  # 部材
    dfs['Production LT'] = df['Production LT_s']  # 製作日数
    dfs['Min Qty of Big Order'] = df['Min Qty of Big Order_s']  # 大口下限数量
    dfs['Max Qty of Big Order'] = df['Max Qty of Big Order_s']  # 大口上限数量
    dfs['Supplier Code of BO'] = ''  # 大口メーカーコード
    dfs['Unit Price Check'] = df['Unit Price Check_s']  # 単価チェック区分
    dfs['Express T Calc Type for Sales'] = '0'  # ストークT適用フラグ
    dfs['Express T Sales Pc/Unit'] = '0'  # ストークT売単価
    dfs['Express T Purchase Pc/Unit'] = '0'  # ストークT仕入単価
    dfs['Express A Calc Type for Sales'] = df['Express A Calc Type for Sales_s']  # ストークA適用フラグ
    dfs['Express A Sales Pc/Unit'] = df['Express A Sales Pc/Unit_z']  # ストークA売単価
    dfs['Express A Calc Type for Purchase'] = df['Express A Calc Type for Purchase_s']  # ストークA仕入計算方法
    dfs['Express A Purchase Pc/Unit'] = df['Express A Purchase Pc/Unit_s']  # ストークA仕入単価
    dfs['Express A Production LT'] = df['Express A Production LT_s']  # ストークA製作日数
    dfs['Special Express A Calc Type for Sales'] = df['Special Express A Calc Type for Sales_s']  # ストークA早割適用フラグ
    dfs['Special Express A Sales Pc/Unit'] = df['Special Express A Sales Pc/Unit_z']  # ストークA早割売単価
    dfs['Plant Express A Purchase Calc'] = df['Plant Express A Purchase Calc_s']  # ストークA同梱仕入計算方法
    dfs['Plant Express A Purchase Pc/Unit'] = df['Plant Express A Purchase Pc/Unit_s']  # ストークA同梱仕入単価
    dfs['Express B Calc Type for Sales'] = df['Express B Calc Type for Sales_s']  # ストークB適用フラグ
    dfs['Express B Sales Pc/Unit'] = df['Express B Sales Pc/Unit_z']  # ストークB売単価
    dfs['Express B Purchase Pc/Unit'] = df['Express B Purchase Pc/Unit_s']  # ストークB仕入単価
    dfs['Express B Production LT'] = df['Express B Production LT_s']  # ストークB製作日数
    dfs['Express C Calc Type for Sales'] = df['Express C Calc Type for Sales_s']  # ストークC適用フラグ
    dfs['Express C Sales Pc/Unit'] = df['Express C Sales Pc/Unit_z']  # ストークC売単価
    dfs['Express C Purchase Pc/Unit'] = df['Express C Purchase Pc/Unit_s']  # ストークC仕入単価
    dfs['Express C Production LT'] = df['Express C Production LT_s']  # ストークC製作日数
    dfs['Weight'] = df['Weight_z']  # 商品重量
    dfs['Weight Calc Mode'] = df['Weight Calc Mode_y']  # 重量式区分
    dfs['Weight Coefficient'] = df['Weight Coefficient_s']  # 重量係数
    dfs['Weight Calc'] = df['Weight Calc_y']  # 重量式
    dfs['Classify Code'] = df['Classify Code_z']  # 分析コード
    dfs['Launch Date'] = df['Launch Date_z']  # 発売年月日
    dfs['Prod Mst for Alt Supplier'] = df['Prod Mst for Alt Supplier_z']  # Qランク
    dfs['Supplier Code'] = 'SPCM'  # 仕入先コード
    dfs['Spec Condition Code'] = df['Spec Condition Code_s']  # 規格条件
    dfs['Ordering Message Code'] = df['Ordering Message Code_s']  # 受注メッセージコード
    dfs['Product Special Flg'] = df['Product Special Flg_s']  # 商品種別
    dfs['Country Of Origin'] = '110'  # 原産国
    dfs['Discontinued on Date'] = df['Discontinued on Date_z']  # 商品廃止年月日
    dfs['Production Days Calc Opt'] = df['Production Days Calc Opt_z']  # 納期計算式区分
    dfs['SO Suspension'] = df['SO Suspension_z']  # 受注停止区分
    dfs['Abolishment MSG'] = df['Abolishment MSG_z']  # 廃止品MSG
    dfs['Product Group Code'] = df['Product Group Code_z']  # 商品グループコード
    dfs['BU Code'] = df['BU Code_z']  # 所管部署
    dfs['Qty / Order'] = df['Qty / Order_z']  # 注文単位数量
    dfs['Each Time QT'] = df['Each Time QT_z']  # 都度見積区分
    dfs['Product Delivery'] = df['Product Delivery_z']  # 商品納入先
    dfs['Packing List Delivery'] = df['Packing List Delivery_z']  # 納品書納入先区分
    dfs['PO Format Div'] = df['PO Format Div_z']  # 発注フォーマット区分
    dfs['SO Cancel Charge Rate'] = df['SO Cancel Charge Rate_z']  # 当日掛率
    dfs['1st Day After SO Cancel Charge Rate'] = df['1st Day After SO Cancel Charge Rate_z']  # 翌日掛率
    dfs['3rd Days After SO Cancel Charge Rate'] = df['3rd Days After SO Cancel Charge Rate_z']  # 3日目以降掛率
    dfs['Production LT for STOCK'] = df['Production LT for STOCK_z']  # 発注納期
    dfs['Developed on Date'] = df['Developed on Date_z']  # 開発年月日
    dfs['CSS Div'] = df['CSS Div_z']  # CSS伝送フラグ
    dfs['Pressure Div'] = df['Pressure Div_z']  # 文字情報区分
    dfs['Pressure Length'] = df['Pressure Length_z']  # 刻印桁数
    dfs['Tax Free Div'] = df['Tax Free Div_z']  # 非課税フラグ
    dfs['Dsct Rt :Sales'] = df['Dsct Rt :Sales_z']  # 早割売掛率
    dfs['Dsct Rt :Purchase'] = df['Dsct Rt :Purchase_z']  # 早割仕入掛率
    dfs['Product LT of ExpZ'] = df['Product LT of ExpZ_z']  # 早割納期
    dfs['Supplier Code of ExpZ'] = df['Supplier Code of ExpZ_z']  # 早割仕入先コード
    dfs['Direct Ship (ref Check Mst)'] = df['Direct Ship (ref Check Mst)_z']  # メーカー直送区分
    dfs['Production Days Count'] = '4'  # 土祝カウント方法
    dfs['Reorder level Logic'] = df['Reorder level Logic_z']  # 発注点
    dfs['MTO Calc'] = df['MTO Calc_z']  # 製作品扱除外フラグ
    dfs['Period'] = df['Period_z']  # 対象期間
    dfs['Safety'] = df['Safety_z']  # 安全在庫係数
    dfs['Heavy Product'] = df['Heavy Product_z']  # 大重量
    dfs['Expensive Product Div'] = df['Expensive Product Div_z']  # 高額商品フラグ
    dfs['Heavy Threshold'] = df['Heavy Threshold_z']  # 大重量閾値
    dfs['Expensive Threshold'] = df['Expensive Threshold_z']  # 高額商品閾値
    dfs['Cutoff Time for Direct'] = df['Cutoff Time for Direct_z']  # 直送切替時刻
    dfs['Cutoff Time for 1day MTO'] = df['GTI_Order_Close']  # 当日受注締時刻
    dfs['Limited MBO Product'] = df['Limited MBO Product_z']  # 有償支給フラグ
    dfs['Minimum Charge'] = df['Minimum Charge_z']  # バラチャージ計算方式区分
    dfs['Max Qty 1'] = df['Max Qty 1_z']  # バラチャージ上限1
    dfs['Amount 1'] = df['Amount 1_z']  # バラチャージ料金1
    dfs['Max Qty 2'] = df['Max Qty 2_z']  # バラチャージ上限2
    dfs['Amount 2'] = df['Amount 2_z']  # バラチャージ料金2
    dfs['Qty / Pack'] = df['Qty / Pack_z']  # パック数
    dfs['Brand Code'] = df['Brand Code_z']  # ブランドコード
    dfs['Qty / Purchase'] = df['Qty / Purchase_z']  # 発注入り数
    dfs['PO Product Code'] = df['PO Product Code_z']  # 発注用商品コード
    dfs['Currency(Sales) Code'] = df['Currency(Sales) Code_z']  # 売単価通貨コード
    dfs['Currency(Purchase) Code'] = 'USD'  # 仕入単価通貨コード
    dfs['Purchase Mode'] = 'B'  # 調達パターン
    dfs['HS Code'] = df['HS Code_z']  # HSコード
    dfs['Product Name'] = df['Product Name_z']  # 商品名(英語)
    dfs['Native Product Name'] = df['Native Product Name_z']  # 商品名(現地語)
    dfs['IO Supply Means'] = ''  # IO調達方法管理コード
    dfs['IO Supply Means (URG)'] = ''  # IO調達方法（緊急）
    dfs['Days to Ship on Catalog'] = df['Production LT_s'] + df['DaysTS']  # カタログ納期　製作日数+輸送日数
    dfs['Express T Production LT'] = '0'  # ストークT納期
    dfs['Express T Days TS'] = '0'  # ストークTカタログ納期
    dfs['Express A Days TS'] = df['Express A Days TS_z']  # ストークAカタログ納期
    dfs['Express B Days TS'] = df['Express B Days TS_z']  # ストークBカタログ納期
    dfs['Express C Days TS'] = df['Express C Days TS_z']  # ストークCカタログ納期
    dfs['Print Weight Unit'] = df['Print Weight Unit_z']  # 商品重量単位
    dfs['Days to Ship of ExpZ'] = df['Days to Ship of ExpZ_z']  # 早割カタログ納期
    dfs['Currency(Purchase of BO)'] = df['Currency(Purchase of BO)_z']  # 大口仕入通貨コード
    dfs['Purchase Mode of BO'] = ''  # 大口調達パターン　大口仕入先設定がNullなので大口調達パターンもNull
    dfs['Shipment Stop Div'] = df['Shipment Stop Div_z']  # 出荷停止区分
    dfs['Express A Direct Ship Flg'] = df['Express A Direct Ship Flg_z']  # ストークA直送フラグ
    dfs['Express B Direct Ship Flg'] = df['Express B Direct Ship Flg_z']  # ストークB直送フラグ
    dfs['Express C Direct Ship Flg'] = df['Express C Direct Ship Flg_z']  # ストークC直送フラグ
    dfs['Express T Direct Ship Flg'] = df['Express T Direct Ship Flg_z']  # ストークT直送フラグ
    dfs['Apply TI to Plant 1'] = df['Apply TI to Plant 1_z']  # 置場1同梱適用区分
    dfs['Cutoff Time for TI to Plant 1'] = df['Cutoff Time for TI to Plant 1_z']  # 置場1同梱締時刻
    dfs['Apply TI to Plant 2'] = df['Apply TI to Plant 2_z']  # 置場2同梱適用区分
    dfs['Cutoff Time for TI to Plant 2'] = df['Cutoff Time for TI to Plant 2_z']  # 置場2同梱締時刻
    dfs['Apply TI to Plant 3'] = df['Apply TI to Plant 3_z']  # 置場3同梱適用区分
    dfs['Cutoff Time for TI to Plant 3'] = df['Cutoff Time for TI to Plant 3_z']  # 置場3同梱締時刻
    dfs['Apply TI to Plant 4'] = df['Apply TI to Plant 4_z']  # 置場4同梱適用区分
    dfs['Cutoff Time for TI to Plant 4'] = df['Cutoff Time for TI to Plant 4_z']  # 置場4同梱締時刻
    dfs['Apply TI to Plant 5'] = df['Apply TI to Plant 5_z']  # 置場5同梱適用区分
    dfs['Cutoff Time for TI to Plant 5'] = df['Cutoff Time for TI to Plant 5_z']  # 置場5同梱締時刻
    dfs['Apply TI to Plant 6'] = df['Apply TI to Plant 6_z']  # 置場6同梱適用区分
    dfs['Cutoff Time for TI to Plant 6'] = df['Cutoff Time for TI to Plant 6_z']  # 置場6同梱締時刻
    dfs['Apply TI to Plant 7'] = df['Apply TI to Plant 7_z']  # 置場7同梱適用区分
    dfs['Cutoff Time for TI to Plant 7'] = df['Cutoff Time for TI to Plant 7_z']  # 置場7同梱締時刻
    dfs['Apply TI to Plant 8'] = df['Apply TI to Plant 8_z']  # 置場8同梱適用区分
    dfs['Cutoff Time for TI to Plant 8'] = df['Cutoff Time for TI to Plant 8_z']  # 置場8同梱締時刻
    dfs['Apply TI to Plant 9'] = df['Apply TI to Plant 9_z']  # 置場9同梱適用区分
    dfs['Cutoff Time for TI to Plant 9'] = df['Cutoff Time for TI to Plant 9_z']  # 置場9同梱締時刻
    dfs['Distribution Flg'] = df['Distribution Flg_z']  # 在庫優先フラグ
    dfs['PO as STOCK'] = df['PO as STOCK_z']  # 事前補充発注フラグ
    dfs['Remarks'] = df['Remarks_z']  # 注釈
    dfs['Hazardous Product'] = df['Hazardous Product_z']  # 危険品フラグ
    dfs['GTI Apply'] = '0'  # GTI対象フラグ
    dfs['Message Mst to Imp Sub'] = df['Message Mst to Imp Sub_s']
    dfs['Print Qty Unit'] = df['Print Qty Unit_z']  # 数量単位
    dfs['QC Product'] = df['QC Product_z']  # QCフラグ
    dfs['Partial Delivery Threshold'] = '0'  # 分納閾値
    dfs['Express L Calc Type for Sales'] = '0'  # 長納期大口割適用フラグ
    dfs['Express L Message Code'] = ''  # 長納期大口割メッセージコード
    dfs['Express L Supplier Code'] = ''  # 長納期大口割仕入先コード
    dfs['TI対象_z'] = df['TI対象_z']    # TI対象flg
    dfs['Weight_y'] = df['Weight_y']    # 【提出用】ベトナム重量ロジック★最終アップリスト_CC
    dfs['Weight Calc Mode_y'] = df['Weight Calc Mode_y']    # 【提出用】ベトナム重量ロジック★最終アップリスト_CC
    dfs['Weight Calc_y'] = df['Weight Calc_y']  # 【提出用】ベトナム重量ロジック★最終アップリスト_CC
    dfs['位置'] = df['位置']    # 【提出用】ベトナム重量ロジック★最終アップリスト_CC
    dfs['Weight2'] = df['Weight2']  # 【提出用】ベトナム重量ロジック★最終アップリスト_CC
    dfs['DaysTS'] = df['DaysTS']    # 輸送日数

    # 在庫品の場合、直送切替時刻・当日受注締時刻=Null
    dfs.loc[dfs['Stock / MTO'] == '0', 'Cutoff Time for Direct'] = ''
    dfs.loc[dfs['Stock / MTO'] == '0', 'Cutoff Time for 1day MTO'] = ''

    # 受注メッセージコードがNullの時、現法間受注メッセージフラグもNull err_8追加
    dfs.loc[dfs['Ordering Message Code'].isnull(), 'Message Mst to Imp Sub'] = ''
    dfs['err_8'] = ''
    dfs['err_8_C'] = ''
    dfs.loc[(dfs['Ordering Message Code'].isnull()) & (df['Ordering Message Code_z'].notnull()), 'err_8'] = '1'
    dfs.loc[(dfs['Ordering Message Code'].isnull()) & (df['Ordering Message Code_z'].notnull()), 'err_8_C'] = df['Ordering Message Code_z']


    # 商品重量
    dfs.loc[(dfs['Stock / MTO'] == '0') & (dfs['位置'] == 'x'), 'Weight'] = dfs['Weight2']
    dfs.loc[(dfs['位置'] != 'x') & (dfs['Weight_y'] > '0'), 'Weight'] = dfs['Weight_y']

    # USA処理　商品納入先・納品書納入先区分
    dfs.loc[dfs['Subsidiary Code'] == 'USA', 'Product Delivery'] = 'C'
    dfs.loc[dfs['Subsidiary Code'] == 'USA', 'Packing List Delivery'] = 'C'

    # TI処理
    ti = pd.DataFrame()
    ti = ti.append(dfs.query('TI対象_z == "1"'))
    ti['Production LT'] = ti['Production LT'].astype(int)
    ti['DaysTS'] = ti['DaysTS'].astype(int)

    ti['Production LT'] = 1  # 製作日数
    ti['Days to Ship on Catalog'] = 1 + ti['DaysTS']  # カタログ納期
    ti['Express A Calc Type for Sales'] = '0'  # ストークA適用フラグ
    ti['Express A Sales Pc/Unit'] = 0  # ストークA売単価
    ti['Express A Calc Type for Purchase'] = '0'  # ストークA仕入計算方法
    ti['Express A Purchase Pc/Unit'] = 0  # ストークA仕入単価
    ti['Express A Production LT'] = 0  # ストークA製作日数
    ti['Special Express A Calc Type for Sales'] = '0'  # ストークA早割適用フラグ
    ti['Special Express A Sales Pc/Unit'] = 0  # ストークA早割売単価
    ti['Plant Express A Purchase Calc'] = '0'  # ストークA同梱仕入計算方法
    ti['Plant Express A Purchase Pc/Unit'] = 0  # ストークA同梱仕入単価
    ti['Express B Calc Type for Sales'] = '0'  # ストークB適用フラグ
    ti['Express B Sales Pc/Unit'] = 0  # ストークB売単価
    ti['Express B Purchase Pc/Unit'] = 0  # ストークB仕入単価
    ti['Express B Production LT'] = 0  # ストークB製作日数
    ti['Express C Calc Type for Sales'] = '0'  # ストークC適用フラグ
    ti['Express C Sales Pc/Unit'] = 0  # ストークC売単価
    ti['Express C Purchase Pc/Unit'] = 0  # ストークC仕入単価
    ti['Express C Production LT'] = 0  # ストークC製作日数

    # USA TI処理
    ti.loc[ti['Subsidiary Code'] == 'USA', 'Production LT'] = 2 + ti['DaysTS']
    ti.loc[(ti['Stock / MTO'] == '0') & (ti['Production LT for STOCK'] == '1'), 'Production LT for STOCK'] = 2

    # 非TI処理
    tin = pd.DataFrame()
    tin = tin.append(dfs.query('TI対象_z != "1"'))
    tin['Production LT'] = tin['Production LT'].astype(int)
    tin['DaysTS'] = tin['DaysTS'].astype(int)

    # ストークA売単価=0
    tin.loc[tin['Express A Sales Pc/Unit'] == '0', 'Express A Calc Type for Sales'] = '0'   # ストークA適用フラグ
    tin.loc[tin['Express A Sales Pc/Unit'] == '0', 'Express A Calc Type for Purchase'] = '0'  # ストークA仕入計算方法
    tin.loc[tin['Express A Sales Pc/Unit'] == '0', 'Express A Purchase Pc/Unit'] = 0    # ストークA仕入単価
    tin.loc[tin['Express A Sales Pc/Unit'] == '0', 'Express A Production LT'] = 0   # ストークA製作日数

    # ストークA早割売単価=0
    tin.loc[tin['Special Express A Sales Pc/Unit'] == '0', 'Special Express A Calc Type for Sales'] = '0'   # ストークA早割適用フラグ
    tin.loc[tin['Special Express A Sales Pc/Unit'] == '0', 'Plant Express A Purchase Calc'] = '0'  # ストークA同梱仕入計算方法
    tin.loc[tin['Special Express A Sales Pc/Unit'] == '0', 'Plant Express A Purchase Pc/Unit'] = 0    # ストークA同梱仕入単価

    # ストークB売単価=0
    tin.loc[tin['Express B Sales Pc/Unit'] == '0', 'Express B Calc Type for Sales'] = '0'   # ストークB適用フラグ
    tin.loc[tin['Express B Sales Pc/Unit'] == '0', 'Express B Purchase Calc'] = '0'  # ストークB同梱仕入計算方法
    tin.loc[tin['Express B Sales Pc/Unit'] == '0', 'Express B Purchase Pc/Unit'] = 0    # ストークB同梱仕入単価

    # ストークC売単価=0
    tin.loc[tin['Express C Sales Pc/Unit'] == '0', 'Express C Calc Type for Sales'] = '0'   # ストークC適用フラグ
    tin.loc[tin['Express C Sales Pc/Unit'] == '0', 'Express C Purchase Calc'] = '0'  # ストークC同梱仕入計算方法
    tin.loc[tin['Express C Sales Pc/Unit'] == '0', 'Express C Purchase Pc/Unit'] = 0    # ストークC同梱仕入単価

    # USA　非TI処理
    tin.loc[tin['Subsidiary Code'] == 'USA', 'Production LT'] = 1 + tin['Production LT']    # 製作日数=製作日数+1
    tin.loc[tin['Subsidiary Code'] == 'USA', 'Days to Ship on Catalog'] = tin['Production LT'] + tin['DaysTS']     # カタログ納期=製作日数+輸出日数
    tin.loc[(tin['Subsidiary Code'] == 'USA') & (tin['Stock / MTO'] == '0') & (tin['Production LT for STOCK'] == '1'), 'Production LT for STOCK'] = 1 + tin['Production LT']    # 発注納期=製作日数+1

    ti = ti.append(tin, sort=False)
    ti['Process Mode'] = '2'  # 処理区分   なぜか？空白
    ti['Master ID'] = '01'  # 登録区分　なぜか？空白
    print(len(ti))

    # err_8とerr_8_CをProduct_Slide.txtに追加
    dfs = ti[['Subsidiary Code', 'Product Code', 'err_8', 'err_8_C']]
    p_zetta = (pd.read_csv(path + 'Product_Slide.txt', sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    p_err = pd.merge(p_zetta, dfs, on=('Subsidiary Code', 'Product Code'), how='left')
    p_err.to_csv(path + 'Product_Slide.txt', sep='\t', encoding='utf_16', index=False)  # 出力

    ti.drop(columns=['TI対象_z', 'Weight_y', 'Weight Calc Mode_y', 'Weight Calc_y', '位置', 'Weight2', 'DaysTS', 'err_8', 'err_8_C'], inplace=True)    #不要な列を削除
    ti.to_csv(path + 'Product.txt', sep='\t', encoding='utf_16', index=False)  # Zetta_Product.txt　ALL出力

    print('SPC_P06_ProductMerge')
    print(datetime.datetime.now())

if __name__ == '__main__':
    SPC_P06_ProductMerge()