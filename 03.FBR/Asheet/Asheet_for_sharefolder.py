# coding: utf-8
# 2019/7/25 Forcust集計用
# FA共有フォルダアドレス仕様へ変更

# ライブラリを呼び出し
import pandas as pd
import datetime as dt

# ファイルを取り込む
FC_A = pd.read_excel('//172.24.81.161/share/F加工企業体/生産計画/共用/FBR資料/A表作成ツール/input/FC_A表テンプレ.xlsx', sheet_name='FC_A表',
                     dtype=object)
FC_FCNSPC = pd.read_excel('//172.24.81.161/share/F加工企業体/生産計画/共用/FBR資料/A表作成ツール/input/FC_A表テンプレ.xlsx',
                          sheet_name='FC_FCNSPC元', dtype=object)
FC_SPCD = pd.read_excel('//172.24.81.161/share/F加工企業体/生産計画/共用/FBR資料/A表作成ツール/input/FC_A表テンプレ.xlsx', sheet_name='FC_SPCD',
                        dtype=object)
FC_MJP = pd.read_excel('//172.24.81.161/share/F加工企業体/生産計画/共用/FBR資料/A表作成ツール/input/FC_A表テンプレ.xlsx', sheet_name='FC_MJP元',
                       dtype=object, header=2, index_col=0)
FC_CHNKOR = pd.read_excel('//172.24.81.161/share/F加工企業体/生産計画/共用/FBR資料/A表作成ツール/input/FC_A表テンプレ.xlsx',
                          sheet_name='FC_KOR元', dtype=object)
CORR = pd.read_excel('//172.24.81.161/share/F加工企業体/生産計画/共用/FBR資料/A表作成ツール/input/FC_A表テンプレ.xlsx', sheet_name='補正値',
                     dtype=object)
FC_ratio = pd.read_excel('//172.24.81.161/share/F加工企業体/生産計画/共用/FBR資料/A表作成ツール/input/FC_比率マスタ.xlsx', dtype=object)
inter_ratio = pd.read_excel('//172.24.81.161/share/F加工企業体/生産計画/共用/FBR資料/A表作成ツール/input/国内比率.xlsx', dtype=object)
cls_cd = pd.read_excel('//172.24.81.161/share/F加工企業体/生産計画/共用/FBR資料/A表作成ツール/input/分析コード一覧.xlsx', dtype=object)

# 年月以外をindex化、カラムの名前を統一
FC_A.rename(columns={'項目': 'FCフラグ', '仕入先': '調達Gr'}, inplace=True)
FC_A.set_index(['調達Gr', '現法', 'FCフラグ'], inplace=True)
FC_FCNSPC.rename(columns={'BE': '管理Gr', '現法コード': '現法', 'グループコード': '製造GR', 'メーカコード': '仕入先'}, inplace=True)
FC_FCNSPC.set_index(['管理Gr', '現法', '分析コード', '商品名', '製造GR', '仕入先'], inplace=True)
FC_SPCD.rename(columns={'向地': '現法', 'サプライヤ': '管理Gr'}, inplace=True)
# FC_SPCD['SUPPLIER_CD'] = 'SPCD' # 私市さんフォームになり不要
FC_SPCD.loc[FC_SPCD['管理Gr'] == 'SPCD', '管理Gr'] = 'SPC'
FC_SPCD.set_index(['SUPPLIER_CD', '管理Gr', 'キー', '現法', 'CLASSIFY_CD', '名称'], inplace=True)
FC_MJP.rename(columns={'現法': 'SUBSIDIARY_CD', '分析CD': 'CLASSIFY_CD'}, inplace=True)
FC_MJP.set_index(['担当チーム', 'Gr', 'CLASSIFY_CD', '分析名称', 'SUBSIDIARY_CD'], inplace=True)
FC_CHNKOR.rename(columns={'製造Gr': '製造GR'}, inplace=True)
FC_CHNKOR.set_index(['現法', '製造GR', '管理Gr'], inplace=True)
CORR.rename(columns={'設定月': 'A表設定月', 'Gr': '製造GR'}, inplace=True)
CORR.set_index(['A表設定月', '製造GR', '元仕入先', '振り先', '理由'], inplace=True)
FC_ratio.rename(columns={'輸出ベース': '現法'}, inplace=True)

# 表形式のデータシートをリスト形式へ
FC_A = FC_A.stack()
FC_A = FC_A.reset_index()
FC_FCNSPC = FC_FCNSPC.stack()
FC_FCNSPC = FC_FCNSPC.reset_index()
FC_SPCD = FC_SPCD.stack()
FC_SPCD = FC_SPCD.reset_index()
FC_MJP = FC_MJP.stack()
FC_MJP = FC_MJP.reset_index()
FC_CHNKOR = FC_CHNKOR.stack()
FC_CHNKOR = FC_CHNKOR.reset_index()
CORR = CORR.stack()
CORR = CORR.reset_index()

# カラムの名前を統一
FC_A.rename(columns={'level_3': '月', 0: '数量の合計'}, inplace=True)
FC_FCNSPC.rename(columns={'level_6': '月', 0: '数量の合計'}, inplace=True)
FC_SPCD.rename(columns={'level_6': '月', 0: '数量の合計'}, inplace=True)
FC_MJP.rename(columns={'level_5': '月', 0: '数量の合計'}, inplace=True)
FC_CHNKOR.rename(columns={'level_3': '月', 0: '数量の合計'}, inplace=True)
CORR.rename(columns={'level_5': '月', 0: '数量の合計', '理由': '現法'}, inplace=True)# 理由カラムを現法へ
CORR['現法'].replace({'在庫品振替': '補正値(在庫品振替)','DLO移管': '補正値(DLO移管)','DPP移管': '補正値(DPP移管)',
                    'ECAL戻し': '補正値(ECAL戻し)','R.B.S': '補正値(R.B.S)','TENEO移管': '補正値(TENEO移管)',
                    'メーカー握り': '補正値(メーカー握り)','売上対策_先納期': '補正値(売上対策_先納期)','売上対策_在庫発注': '補正値(売上対策_在庫発注)','調整': 'CHN'}, inplace=True)
#CORR.loc[:, '現法'] = '補正値'
# 補正値をin/outデータを±で行を複製する
CORR = CORR.astype({'数量の合計': float})
CORR_out = CORR[CORR['元仕入先'].notnull()].copy()
CORR_out.loc[:, '管理Gr'] = CORR_out['元仕入先']
CORR_out['数量の合計'] = CORR_out['数量の合計'] * -1
CORR_in = CORR[CORR['振り先'].notnull()].copy()
CORR_in.loc[:, '管理Gr'] = CORR_in['振り先']
CORR = CORR_in.append(CORR_out, sort=False)
# データ修正
# 4つの分析コードはJ2へ
FC_FCNSPC.loc[((FC_FCNSPC['分析コード'] == '03633520') | (FC_FCNSPC['分析コード'] == '03633521') | (
            FC_FCNSPC['分析コード'] == '03723524') | (FC_FCNSPC['分析コード'] == '03733521')), '管理Gr'] = 'J2' + FC_FCNSPC['管理Gr']
FC_FCNSPC.loc[((FC_FCNSPC['分析コード'] == '03633520') | (FC_FCNSPC['分析コード'] == '03633521') | (
            FC_FCNSPC['分析コード'] == '03723524') | (FC_FCNSPC['分析コード'] == '03733521')), '製造GR'] = 'J2'
# vグループはSPCNewへ
FC_FCNSPC.loc[((FC_FCNSPC['製造GR'] == 'V') & (FC_FCNSPC['仕入先'] == 'SPCM')), '管理Gr'] = 'SPCNew'
FC_FCNSPC = pd.merge(FC_FCNSPC, cls_cd, left_on=['分析コード', '製造GR'], right_on=['CLASSIFY_CD', '製造GR'], how='inner')
FC_SPCD.loc[:, '製造GR'] = 'V'
FC_SPCD.loc[FC_SPCD['CLASSIFY_CD'] == '03722115', '管理Gr'] = 'SPC_V'

# FA_数量計画_ECAL現地調達分_各国まとめにFC_比率マスタ、FC_MJPに国内比率を乗算
# FC_AとFC_ratioをmerge
FC_ratio = FC_ratio[FC_ratio['備考'].isnull()]
FC_ratio.drop(['備考', '元の割合', '備考2'], axis=1, inplace=True)
FC_A = pd.merge(FC_A, FC_ratio, on=['調達Gr', '現法'], how='inner')
FC_A = FC_A.astype({'数量の合計': float, '割合': float})
FC_A.loc[:, '数量の合計'] = FC_A['数量の合計'] * FC_A['割合']
# FC_MJPとinter_ratioをmerge
FC_MJP = pd.merge(FC_MJP, inter_ratio, on=['CLASSIFY_CD', 'SUBSIDIARY_CD'], how='inner')
FC_MJP = FC_MJP.astype({'比率': float, '数量の合計': float})
FC_MJP.loc[:, '数量の合計'] = FC_MJP['数量の合計'] * FC_MJP['比率']
FC_MJP.rename(columns={'SUBSIDIARY_CD': '現法'}, inplace=True)


# # 確認用　その他のカラム名を区別
# FC_A.loc[((FC_A['調達Gr'] == '現地調達') & (FC_A['管理Gr'] == 'その他')), '管理Gr'] = 'その他_現地調達'
# FC_A.loc[((FC_A['調達Gr'] == 'ECAL') & (FC_A['管理Gr'] == 'その他')), '管理Gr'] = 'その他_ECAL'
# FC_A.loc[((FC_A['調達Gr'] == '現地調達') & (FC_A['管理Gr'] == '無錫森本')), '管理Gr'] = '無錫森本_現地調達'
# FC_A.loc[((FC_A['調達Gr'] == 'ECAL') & (FC_A['管理Gr'] == '無錫森本')), '管理Gr'] = '無錫森本_ECAL'

# データを結合する
FC_A = FC_A.append(FC_FCNSPC, sort=False)
FC_A = FC_A.astype({'月': str})
# FC_A['月'] = '20' + FC_A['月']
FC_A = FC_A.append(FC_MJP, sort=False)
FC_A = FC_A.append(FC_CHNKOR, sort=False)
FC_A = FC_A.append(FC_SPCD, sort=False)

# 数量の合計を集計する
FC_A.reset_index(drop=True, inplace=True)
if ((FC_A['現法'].isnull().values.sum() == 0) &
        (FC_A['製造GR'].isnull().values.sum() == 0) &
        (FC_A['月'].isnull().values.sum() == 0) &
        (FC_A['管理Gr'].isnull().values.sum() == 0)):
    FC_A = FC_A.groupby(['現法', '製造GR', '月', '管理Gr'], as_index=False)[['数量の合計']].sum()

    # 集計後補正値を加える
    FC_A = FC_A.append(CORR, sort=False)

    # 出力する条件を絞る
    FC_A = FC_A[FC_A['管理Gr'] != '対象外']
    FC_A = FC_A[((FC_A['製造GR'] == 'I') | (FC_A['製造GR'] == 'J') | (FC_A['製造GR'] == 'J2') | (FC_A['製造GR'] == 'K') |
                 (FC_A['製造GR'] == 'P') | (FC_A['製造GR'] == 'S') | (FC_A['製造GR'] == 'T') | (FC_A['製造GR'] == 'U') |
                 (FC_A['製造GR'] == 'V') | (FC_A['製造GR'] == 'F') | (FC_A['製造GR'] == 'W') | (FC_A['製造GR'] == 'Z') |
                 (FC_A['製造GR'] == 'B'))]
    FC_A = FC_A.loc[:, ['現法', '製造GR', '月', '管理Gr', '数量の合計']]

    # 並べ替え
    FC_A.sort_values(['現法', '製造GR', '月', '管理Gr'], inplace=True)

    # 内製、外製フラグをつける
    FC_A.loc[:, '内製'] = '外製'  # すべて外製を書き込み
    FC_A.loc[(FC_A['管理Gr'].str.contains('FCN') |
              FC_A['管理Gr'].str.contains('SPC') |
              FC_A['管理Gr'].str.contains('DLO') |
              FC_A['管理Gr'].str.contains('DPP') |
              FC_A['管理Gr'].str.contains('KOR') |
              FC_A['管理Gr'].str.contains('駿河阿見')), '内製'] = '内製'
    # A表設定月を入れる
    today = dt.datetime.today().strftime("%Y%m")
    FC_A.loc[:, 'A表設定月'] = today

    # ファイルをアウトプット
    fname = '//172.24.81.161/share/F加工企業体/生産計画/共用/FBR資料/A表作成ツール/output/A表' + dt.datetime.today().strftime(
        "%Y%m%d") + '.xlsx'
    FC_A.to_excel(fname, sheet_name='A表', index=False)
    print("A表作成が完了しました!")
else:
    print('読み込みに失敗したファイルがあります！担当者にご連絡ください。')