# coding: utf-8
# python test

# ライブラリを呼び出し
import glob
import pandas as pd
import numpy as np
import datetime

def SPC_P01_Target_Inner():

    r_path = 'C:/temp/■Python_SPC_Master/'  # ★作業用ローカルフォルダ
    path = '//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/'  # ★共通ファイル保存先
    print(datetime.datetime.now())

    # フォルダからExcelファイル名抽出　フルパス
    files = glob.glob(path + 'SPC_Global_inner/*.xlsx')
    lists = []
    for file in files:
        #　フルパスからファイル名のみ抽出
        lists.append(file.replace(path + 'SPC_Global_inner', ''))
    n = len(lists)

    # ファイルを開く　excel=立上ファイル
    for l in range(0, n):
        excel = pd.read_excel(path + 'SPC_Global_inner/' + lists[l], dtype=object)
        print(lists[l])

    # 立上データ出力
    SUBSIDIARY_CD=['CHN', 'KOR', 'TIW', 'SGP', 'MYS', 'THA', 'USA', 'GRM', 'VNM', 'JKT', 'IND', 'MJP']   # 現法増えた際はこちらも追加
    df3 = pd.DataFrame([], columns=['分析コード', 'Product Code', '立上日', '仕入先', 'Subsidiary Code'])
    df4 = pd.DataFrame([], columns=['分析コード', 'Product Code', '立上日', '仕入先', 'Subsidiary Code', '新TI対象'])

    for SUBSIDIARY_CD in SUBSIDIARY_CD:
        data = (excel[['分析コード', '型式', SUBSIDIARY_CD+'立上日', SUBSIDIARY_CD+'仕入先']])
        df = pd.DataFrame(data)
        df2 = df.rename(columns={'型式': 'Product Code', SUBSIDIARY_CD+'立上日': '立上日', SUBSIDIARY_CD+'仕入先': '仕入先'})  # 列見出し変更（統一）
        df2['Subsidiary Code'] = SUBSIDIARY_CD  #「現法コード」列追加
        df2 = df2.query('立上日 == "20190617"')    # 日付指定をどうするか？
        if len(df2)>0:
            df3 = df3.append(df2)
    print(len(df3))
    if len(df3)>0:
        # 立上データにTIフラグを追加する
        fcn_inner = pd.read_excel(path+'temp_master/FCNインナーリスト.xlsx', dtype=object)     # TI対象ファイル
        df4 = pd.merge(df3, fcn_inner, how='left', left_on='Product Code', right_on='型式')
        df4.drop(columns=['型式'], inplace=True)  # 不要な列を削除

        # 　「temp_data」フォルダに作成
        df4.to_csv(path + 'temp_data/SPC_Target.txt', sep='\t', encoding='utf_16', index=False)
        print('Finish!')
    else:
        print('Not Found')
    print('SPC_P01_Target_Inner')
    print(datetime.datetime.now())
if __name__ == '__main__':
    SPC_P01_Target_Inner()