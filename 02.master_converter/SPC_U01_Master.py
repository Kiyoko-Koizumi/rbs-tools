# Unit Price SPC・Zetta　対象Master抽出
import glob
import pandas as pd
import Header_U
import numpy as np
import datetime

def SPC_U01_Master():
    path = '//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/'
    print(datetime.datetime.now())

    # ProductMasterのnon_err_ProductデータとSlide_Noデータ
    slide_no = pd.DataFrame(pd.read_csv(path + 'temp_data/SZ_Slide.txt', sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    non_err = pd.DataFrame(pd.read_csv(path + 'temp_data/non_err_Product.txt', sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    slide_no['new_slide_no'] = slide_no['new_slide_no'].astype(int)
    u_check = pd.DataFrame(pd.merge(slide_no, non_err, on=('Subsidiary Code', 'Product Code')))
    z_new_no = u_check[['Subsidiary Code', 'Product Code', 'new_slide_no', 'slide_no']]
    s_new_no = u_check[['Subsidiary Code', 'Product Code', 'new_slide_no', 'spc_slide_no']]
    non_err = non_err[['Subsidiary Code', 'Product Code']]
    u_check.drop_duplicates(subset=['Subsidiary Code', 'Product Code'], keep='first', inplace=True)  # 重複データ削除　先頭行残す

    # ★Step1　フォルダからtxtファイル名抽出　フルパス　SPCデータ抽出
    files = glob.glob(path + 'SPC_Master/UNIT_PRICE/*.txt')
    lists = []
    for file in files:
        # フルパスからファイル名のみ抽出
        lists.append(file.replace(path + 'SPC_Master/UNIT_PRICE', ''))
    n = len(lists)

    h_order=({'Subsidiary Code': 0, 'Product Code': 1, 'spc_slide_no': 2, 'Min.Val.1': 3, 'Min.Val.2': 4, 'Min.Val.3': 5,
              'Min.Val.4': 6, 'Min.Val.5': 7, 'purchase': 8, 'data': 9})  # スライドHeader並び順
    spc_slide = pd.DataFrame(columns=h_order)   # スライド出力用
    spc_data1 = pd.DataFrame([], columns=Header_U.Header())    # ALLデータ出力用

    for l in range(0, n):
        spc = (pd.read_csv(path + 'SPC_Master/UNIT_PRICE/' + lists[l], sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
        spc_data = pd.merge(spc, non_err, on=['Product Code'])  # non_errデータの型式が一致する現法データ
        spc_data1 = spc_data1.append(spc_data)

        for i in range(1, 11):
            i = str(i)
            spc_data2 = (spc_data[['Subsidiary Code_y', 'Product Code', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5',
                                   'Slide Purchase Unit Price ' + i]])
            # Subsidiary Code_yはSZ_Slideデータの現法コード
            spc_data3 = (spc_data2.rename(columns={'Subsidiary Code_y':'Subsidiary Code', 'Slide Purchase Unit Price ' + i: 'purchase'}))
            spc_data3['spc_slide_no'] = i
            spc_data3['data'] = 'spc'
            spc_slide = spc_slide.append(spc_data3, sort=False)  # sort=Falseでアラートが消える

    # 「temp_data」フォルダに作成
    spc_slide['purchase'] = spc_slide['purchase'].astype(float)
    spc_slide['Min.Val.1'] = spc_slide['Min.Val.1'].astype(float)
    # spc_slide = (spc_slide.query('purchase > 0'))  # 仕入単価>0で抽出　Accessは条件つけていない
    spc_slide = spc_slide.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1'])
    spc_slide = pd.merge(s_new_no, spc_slide, how='left')   # new_slide_no 追加
    spc_slide.to_csv(path + 'temp_data/SPC_U_Slide.txt', sep='\t', encoding='utf_16', index=False)    # SPC_U_Slide.txt スライドデータのみ出力

    spc_data1 = spc_data1.rename(columns={'Subsidiary Code_x': 'Subsidiary Code'})
    spc_data1.drop(columns=['Subsidiary Code_y'], inplace=True)    # 不要な列を削除
    # spc_data1.drop_duplicates(subset=['Product Code', 'Min.Val.1'], keep='first', inplace=True)  # 重複データ削除　先頭行残す   Accessは削除していない
    spc_data1['Process Mode'] = '4'
    spc_data1['Master ID'] = '02'
    spc_data1.to_csv(path + 'temp_data/SPC_U_Product.txt', sep='\t', encoding='utf_16', index=False)  # SPC_U_Product.txt　ALL出力

    # ★Step2　フォルダからtxtファイル名抽出　フルパス  Zettaデータ抽出
    files = glob.glob(path + 'Zetta_Unit/*.txt')
    lists = []
    for file in files:
        # 　フルパスからファイル名のみ抽出
        lists.append(file.replace(path + 'Zetta_Unit', ''))
    n = len(lists)

    h_order=({'Subsidiary Code': 0, 'Product Code': 1, 'slide_no': 2, 'Min.Val.1': 3, 'Min.Val.2': 4, 'Min.Val.3': 5,
              'Min.Val.4': 6, 'Min.Val.5': 7, 'sales': 8, 'data': 9})  # スライドHeader並び順
    z_slide = pd.DataFrame(columns=h_order)   # スライド出力用
    z_data1 = pd.DataFrame([], columns=Header_U.Header())    # ALLデータ出力用

    for l in range(0, n):
        z = (pd.read_csv(path + 'Zetta_Unit/' + lists[l], sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
        z_data = pd.merge(z, non_err, on=['Subsidiary Code', 'Product Code'])  # non_errデータの現法コードと型式が一致する現法データ
        z_data1 = z_data1.append(z_data)

        for i in range(1, 11):
            i = str(i)
            z_data2 = (z_data[['Subsidiary Code', 'Product Code', 'Min.Val.1', 'Min.Val.2', 'Min.Val.3', 'Min.Val.4', 'Min.Val.5',
                                   'Slide Sales Unit Price ' + i]])

            z_data3 = (z_data2.rename(columns={'Slide Sales Unit Price ' + i: 'sales'}))
            z_data3['slide_no'] = i
            z_data3['data'] = 'zetta'
            z_slide = z_slide.append(z_data3, sort=False)  # sort=Falseでアラートが消える

    h_product = pd.DataFrame(z[z['Subsidiary Code'] == 'XXX'])  # ヘッダ抽出
    h_product.to_csv(path + 'temp_data/h_U_Product.txt', sep='\t', encoding='utf_16', index=False)  # h_U_Product.txt　ヘッダ出力

    # 「temp_data」フォルダに作成
    z_slide['sales'] = z_slide['sales'].astype(float)
    z_slide['Min.Val.1'] = z_slide['Min.Val.1'].astype(float)
    # z_slide = (z_slide.query('sales > 0'))  # 売単価>0で抽出　Accessは条件つけていない
    z_slide = z_slide.sort_values(by=['Subsidiary Code', 'Product Code', 'Min.Val.1'])
    z_slide = pd.merge(z_new_no, z_slide, how='left')   # new_slide_no 追加
    z_slide.to_csv(path + 'temp_data/Zetta_U_Slide.txt', sep='\t', encoding='utf_16', index=False)    # Zetta_U_Slide.txt スライドデータのみ出力

    z_data1['Process Mode'] = '4'
    z_data1['Master ID'] = '02'
    # z_data1.drop_duplicates(subset=['Subsidiary Code', 'Product Code', 'Min.Val.1'], keep='first', inplace=True)  # 重複データ削除　先頭行残す　Accessは削除していない
    z_data1.to_csv(path + 'temp_data/Zetta_U_Product.txt', sep='\t', encoding='utf_16', index=False)  # Zetta_U_Product.txt　ALL出力

    print('Fin')
    print(datetime.datetime.now())
if __name__ == '__main__':
    SPC_U01_Master()