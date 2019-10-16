# Product Master 出力　Product.txt　Product_Slide.txt
import pandas as pd
import numpy as np
import datetime
import subprocess
import openpyxl
import os, tkinter, tkinter.filedialog, tkinter.messagebox

def SPC_P08_Summary():

    r_path = 'C:/temp/■Python_SPC_Master/'  # ★作業用ローカルフォルダ
    path = '//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/temp_data/'  # ★共通ファイル保存先
    print(datetime.datetime.now())

    p = (pd.read_csv(path + 'Product.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    s = (pd.read_csv(path + 'Product_Slide.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
    t = (pd.read_csv(path + 'SPC_Target.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))

    dft = pd.DataFrame(pd.pivot_table(t, values='分析コード', index=['Subsidiary Code'], aggfunc='count'))

    df = pd.DataFrame(dft)
    df = df.rename(columns={'分析コード': '対象REC数'})

    for i in range(0, 8):  # 集計のためfloatに変更
        s['err_' + str(i)] = s['err_' + str(i)].astype(float)
    s = s.replace(np.nan, 0)
    s['err_sum'] = s['err_0'] + s['err_1'] + s['err_2'] + s['err_3'] + s['err_4'] + s['err_5'] + s['err_6'] + s['err_7'] + s['err_8']

    dfs = pd.DataFrame(pd.pivot_table(s, values=['err_0', 'err_1', 'err_2', 'err_3', 'err_4', 'err_5', 'err_6', 'err_7', 'err_8'],
                                      index=['Subsidiary Code'], aggfunc='sum'))
    df = pd.merge(df, dfs, on='Subsidiary Code', how='left')

    s = s.query('err_sum == 0')
    dfs = pd.DataFrame(pd.pivot_table(s, values='err_sum', index=['Subsidiary Code'], aggfunc='count'))
    df = pd.merge(df, dfs, on='Subsidiary Code', how='left')
    h = ['対象REC数', 'err_sum', 'err_0', 'err_1', 'err_2', 'err_3', 'err_4', 'err_5', 'err_6', 'err_7', 'err_8']
    df = df.reindex(columns=h)
    df = df.rename(columns={'err_sum': '作成REC数（err除く）', 'err_0': 'err_0:Over_List', 'err_1': 'err_1:スライド1の売値=0 And 仕入>0 or 売値>0 And 仕入=0'
                            , 'err_2': 'err_2:売り値=0 And 仕入>0　単価チェック区分=0', 'err_3': 'err_3:重量式未設定'
                            , 'err_4': 'err_4:[Slide(n)_Sales]＜[Slide(n+1)_Sales]'
                            , 'err_5': 'err_5:[Slide(n)_Purchase]＜[Slide(n+1)_Purchase]', 'err_6': 'err_6:[Slide(n)_CatalogDays]＞[Slide(n+1)_CatalogDays]'
                            , 'err_7': 'err_7:中口数量に製作日数・カタログ納期が入っていない', 'err_8': 'err_8:Message Codeが駿河見積は空白だがZettaはコードが入っている'})

    writer = pd.ExcelWriter(path + 'Product_Summary.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Summary', na_rep='', index=True)
    workbook = writer.book
    worksheet = writer.sheets['Summary']
    # フォーマットの設定　ヘッダが勝手に太字＆罫線になるので設定変更
    fmt = workbook.add_format({'bold': False, 'border': 0, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
    # カラム名のフォーマット
    [worksheet.write(0, col_num, col_value, fmt) for col_num, col_value in enumerate(df.columns.values, 1)]
    # インデックス名のフォーマット
    [worksheet.write(idx_num, 0, idx_value, fmt) for idx_num, idx_value in enumerate(df.index.values, 1)]
    [worksheet.write(0,0,'Subsidiary Code',fmt)]
    writer.save()

    print('SPC_P08_Summary')
    print(datetime.datetime.now())
    # 加藤さんからぱくった！
    # ファイル選択ダイアログの表示
    #root = tkinter.Tk()
    #root.withdraw()
    #tkinter.messagebox.showinfo('Summary確認', '「Product_Summary.xlsx」を確認してください！')

    # ファイルが開かないのであきらめた。。。
    #excel = r'C:/Program Files/Microsoft Office\root/Office16/excel.exe'
    #file_path = r'//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/temp_data/Product_Summary.xlsx'
    #subprocess.Popen([excel, file_path], shell=True)
    #wb = openpyxl.load_workbook(file_path)
    #sheet = wb['Summary']
    #wb.close()
if __name__ == '__main__':
    SPC_P08_Summary()