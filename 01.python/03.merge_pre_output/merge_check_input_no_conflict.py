# coding: utf-8
# UNION_prep_output0.5 2018/12/17
#0.3 エラーファイル複数カラム対応
#0.4 従来生産拠点のないREC抜き出す、処理件数をoutput
#0.5 設備管理単位コードを付与
#0.6 BMJP除去
#0.7 ランデットコスト、RBS_製造原価の計算式を修正,単価に*数量、エラー落ちした復活RECのインナーコード先頭2文字に'E'を入れる
#0.8 納区、UFでエラー落ちした復活RECはインナーコードの変更を行わない
#0.9 エラーファイル修正されたので、エラーファイルのヘッダー付与を削除
#    準備処理時エラーで落ちたRECにUF種別やJST時間、エラーコード,をACE参照スキーマに付与
#0.10 Global_Noをキーとして利用しない（Global_Noが意図せず重複してしまうこともあるため）、日本時間昇順に並べ替え
#0.11 ACE仕入先　FCNTをFCNXへ
#0.12 見積もりUF RECに従来生産拠点をつけない、中口になってしまい、スキーマと生産拠点が合わないREC除く、結果の出力内容を変更、従来生産拠点の1はstrで記述
#0.13 インタフェース定義更新に伴いコスト計算式を変更,管理単位コードの付与方式を変更
#0.14 実績仕入先コードはシミュレーション対象RECで負荷に積む際に使用しており、発注現法でなく受注現法でなくてはならないため修正
#0.15 ホワイトリストカウント、logの表記を修正
#0.16 MCコード”NA”が消えてしまうので、書き込む
#0.16 カレンダコード5AAAA→5BBBBへ書き換え、取り込みのファイル名を修正
#2.0  UNION_pre_outputへ変更　AWS内で実行する形式に書き換え　引数として作業ディレクトリを取得,read_table使用しない
#3.0  M単毀損対応　従来生産拠点より着荷コストが上回る選択肢を削除


# モジュールのインポート
import os
import csv
import pandas as pd
import sys

# from tqdm import tqdm
csv.field_size_limit(1000000000)

font = 'utf-8'
# font='shift_jisx0213'

args =sys.argv

# ファイル名で記述
f_name = ['input.tsv', 'input_RBS_OUTPUT.tsv_Default', 'input_RBS_OUTPUT_ERROR.tsv_Default', 'input_RBS_OUTPUT.tsv_MPA', 'input_RBS_OUTPUT_ERROR.tsv_MPA', 'input_RBS_OUTPUT.tsv_AMI', 'input_RBS_OUTPUT_ERROR.tsv_AMI', 'input_RBS_OUTPUT.tsv_CHN',
          'input_RBS_OUTPUT_ERROR.tsv_CHN', 'input_RBS_OUTPUT.tsv_SPCM', 'input_RBS_OUTPUT_ERROR.tsv_SPCM', 'input_RBS_OUTPUT.tsv_AMI_MCOST', 'input_RBS_OUTPUT_ERROR.tsv_AMI_MCOST', 'input_RBS_OUTPUT.tsv_CHN_MCOST', 'input_RBS_OUTPUT_ERROR.tsv_CHN_MCOST',
          'input_RBS_OUTPUT.tsv_SPCM_MCOST', 'input_RBS_OUTPUT_ERROR.tsv_SPCM_MCOST']
file_list = []

# inputファイルの取得
f_pass_i = args[1] + '/input'

os.chdir(f_pass_i)
file = pd.read_csv(f_name[0], sep='\t', dtype='object', index_col=None)
var_list = ['ランデットコスト', '発注現法仕入値', '発注現法実績売値', 'RBS_製造原価', 'RBS_発注先現法仕入単価', 'RBS_マージン単価', 'RBS_販管費', 'RBS_輸出運賃', 'RBS_仕入先売単価', 'RBS_輸入運賃', 'RBS_関税', 'RBS_輸入諸掛']
file[var_list] = file[var_list].astype(float)
file = file.astype({'数量': int})
file = file.fillna({'RBS_マージン単価': 0, 'RBS_販管費': 0, 'RBS_輸出運賃': 0, 'RBS_輸入運賃': 0, 'RBS_関税': 0, 'RBS_輸入諸掛': 0})
file_list.append(file)

# outputファイルの取得
f_pass_o = args[1] + '/output'
os.chdir(f_pass_o)
# ファイル名固定
for f in range(1, len(f_name)):
    file = pd.read_csv(f_name[f], sep='\t',  dtype='object', index_col=None)
    var_list = ['ランデットコスト', '発注現法仕入値', '発注現法実績売値', 'RBS_製造原価', 'RBS_発注先現法仕入単価', 'RBS_マージン単価', 'RBS_販管費', 'RBS_輸出運賃', 'RBS_仕入先売単価', 'RBS_輸入運賃', 'RBS_関税', 'RBS_輸入諸掛']
    file[var_list] = file[var_list].astype(float)
    file = file.astype({'数量': int})
    file = file.fillna({'RBS_マージン単価': 0, 'RBS_販管費': 0, 'RBS_輸出運賃': 0, 'RBS_輸入運賃': 0, 'RBS_関税': 0, 'RBS_輸入諸掛': 0})
    file_list.append(file)

#データを保持
prep_input = file_list[0]
default = file_list[1]
default_e = file_list[2]
MPA = file_list[3]
MPA_e = file_list[4]
AMI_C = file_list[11]
AMI_P = file_list[5]
FCN_C = file_list[13]
FCN_P = file_list[7]
SPC_C = file_list[15]
SPC_P = file_list[9]
AMI_C_e = file_list[12]
AMI_P_e = file_list[6]
FCN_C_e = file_list[14]
FCN_P_e = file_list[8]
SPC_C_e = file_list[16]
SPC_P_e = file_list[10]

# エラーファイルを結合,重複削除
error_list = default_e
error_list = error_list.append(MPA_e, sort=False)
error_list = error_list.append(AMI_C_e, sort=False)
error_list = error_list.append(FCN_C_e, sort=False)
error_list = error_list.append(SPC_C_e, sort=False)
error_list = error_list.append(AMI_P_e, sort=False)
error_list = error_list.append(FCN_P_e, sort=False)
error_list = error_list.append(SPC_P_e, sort=False)

# 正常処理のファイルのエラーRECに対し処理
E_delete = [default, MPA, AMI_P, FCN_P, SPC_P, AMI_C, FCN_C, SPC_C]
for s in range (0, len(E_delete)):
    EE = E_delete[s]
    # エラーRECをエラーファイルに結合
    error_list = error_list.append(EE[EE['ACE参照スキーマ'].isnull()], sort=False)
    error_list = error_list.append(EE[EE['ACE仕入先コード'] == 'BMJP'], sort=False)
    # エラーREC（ACE参照スキーマがNull,仕入先がBMJP）を削除
    EE = EE.dropna(subset=['ACE参照スキーマ'])
    EE = EE[EE['ACE仕入先コード'] != 'BMJP']
    E_delete[s] = EE
# error_list重複削除
error_list.drop_duplicates(keep='first', inplace=True)

default = E_delete[0]
MPA = E_delete[1]
AMI_P = E_delete[2]
FCN_P = E_delete[3]
SPC_P = E_delete[4]
AMI_C = E_delete[5]
FCN_C = E_delete[6]
SPC_C = E_delete[7]

# 仕入値スキーマのRBS_仕入先売単価+RBS_輸入運賃+RBS_関税+RBS_輸入諸掛＝発注現法仕入値
MPA['発注現法仕入値'] = MPA['RBS_仕入先売単価'] + MPA['RBS_輸入運賃'] + MPA['RBS_関税'] + MPA['RBS_輸入諸掛']
# 各費目に数量をかける
MPA=MPA.assign(発注現法仕入値=lambda MPA:MPA.発注現法仕入値 * MPA.数量,
               ランデットコスト=lambda MPA:MPA.ランデットコスト * MPA.数量,
               発注現法実績売値=lambda MPA:MPA.発注現法実績売値 * MPA.数量,
               RBS_製造原価=lambda MPA:MPA.RBS_製造原価 * MPA.数量,
               RBS_発注先現法仕入単価=lambda MPA: MPA.RBS_発注先現法仕入単価 * MPA.数量,
               RBS_マージン単価=lambda MPA:MPA.RBS_マージン単価 * MPA.数量,
               RBS_販管費=lambda MPA:MPA.RBS_販管費 * MPA.数量,
               RBS_輸出運賃=lambda MPA:MPA.RBS_輸出運賃 * MPA.数量,
               RBS_仕入先売単価=lambda MPA:MPA.RBS_仕入先売単価 * MPA.数量,
               RBS_輸入運賃=lambda MPA:MPA.RBS_輸入運賃 * MPA.数量,
               RBS_関税=lambda MPA:MPA.RBS_関税 * MPA.数量,
               RBS_輸入諸掛=lambda MPA:MPA.RBS_輸入諸掛 * MPA.数量)
MPA = MPA.round({'発注現法仕入値': 3, 'ランデットコスト': 3, '発注現法実績売値': 3, 'RBS_製造原価': 3, 'RBS_マージン単価': 3, 'RBS_販管費': 3, 'RBS_輸出運賃': 3, 'RBS_仕入先売単価': 3, 'RBS_輸入運賃': 3, 'RBS_関税': 3, 'RBS_輸入諸掛': 3})

P_tbl = [AMI_P, FCN_P, SPC_P]
C_tbl = [AMI_C, FCN_C, SPC_C]

# 内製分だけ繰り返す
for s in range(0, len(P_tbl)):
    P = P_tbl[s]
    C = C_tbl[s]

    #RBS_仕入先売単価+RBS_輸入運賃+RBS_関税+RBS_輸入諸掛＝発注現法仕入値
    P['発注現法仕入値'] = P['RBS_仕入先売単価'] + P['RBS_輸入運賃'] + P['RBS_関税'] + P['RBS_輸入諸掛']

    # 製造原価スキーマのRBS_製造原価のみ保持、名前の変更
    C = C.loc[::, ['番号', 'RBS_製造原価']]
    C = C.rename(columns={'RBS_製造原価': 'RBS_製造原価_C'})

    # 仕入値と製造原価スキーマ２つのテーブルをマージ、値の入れかえ
    # P,Cのテーブルを結合
    P = pd.merge(P, C, on='番号', how='left')
    # 製造原価スキーマの製造原価を用いてランデットコストを再算出
    P['ランデットコスト'] =P['ランデットコスト'] + P['RBS_製造原価_C'] - P['RBS_製造原価']
    # 仕入値スキーマに製造原価に製造原価スキーマの製造原価を転記
    P['RBS_製造原価'] = P['RBS_製造原価_C']

    # 単価をREC金額に変更
    P = P.assign(発注現法仕入値=lambda P: P.発注現法仕入値 * P.数量,
                 ランデットコスト=lambda P: P.ランデットコスト * P.数量,
                 発注現法実績売値=lambda P: P.発注現法実績売値 * P.数量,
                 RBS_製造原価=lambda P: P.RBS_製造原価 * P.数量,
                 RBS_発注先現法仕入単価=lambda P: P.RBS_発注先現法仕入単価 * P.数量,
                 RBS_マージン単価=lambda P: P.RBS_マージン単価 * P.数量,
                 RBS_販管費=lambda P: P.RBS_販管費 * P.数量,
                 RBS_輸出運賃=lambda P: P.RBS_輸出運賃 * P.数量,
                 RBS_仕入先売単価=lambda P: P.RBS_仕入先売単価 * P.数量,
                 RBS_輸入運賃=lambda P: P.RBS_輸入運賃 * P.数量,
                 RBS_関税=lambda P: P.RBS_関税 * P.数量,
                 RBS_輸入諸掛=lambda P: P.RBS_輸入諸掛 * P.数量)
    P.drop(['RBS_製造原価_C'], axis=1, inplace=True)
    P = P.round({'発注現法仕入値': 3, 'ランデットコスト': 3, '発注現法実績売値': 3, 'RBS_製造原価': 3, 'RBS_マージン単価': 3, 'RBS_販管費': 3, 'RBS_輸出運賃': 3, 'RBS_仕入先売単価': 3, 'RBS_輸入運賃': 3, 'RBS_関税': 3, 'RBS_輸入諸掛': 3})

    P_tbl[s] = P
    C_tbl[s] = C

    P_sample=P

AMI_P = P_tbl[0]
FCN_P = P_tbl[1]
SPC_P = P_tbl[2]

# ４つのファイルを結合
check_input = MPA
check_input = check_input.append(AMI_P, sort=False)
check_input = check_input.append(FCN_P, sort=False)
check_input = check_input.append(SPC_P, sort=False)

# スキーマと生産拠点が一致していないRECはエラーファイルへ
# 一致していないRECは別だし
SUP_NG = check_input[~(((check_input['ACE参照スキーマ']=='MPA') & (check_input['RBS_受注現法仕入先コード']=='7017')) |
                      ((check_input['ACE参照スキーマ']=='AMI') & (check_input['RBS_受注現法仕入先コード']=='3764')) |
                      ((check_input['ACE参照スキーマ']=='CHN') & (check_input['RBS_受注現法仕入先コード']=='0FCN')) |
                      ((check_input['ACE参照スキーマ']=='SPCM') & (check_input['RBS_受注現法仕入先コード']=='SPCM')))]
# 一致してるファイルのみ、SUP_NGを生成してからcheck_inputを上書き
check_input = check_input[(((check_input['ACE参照スキーマ']=='MPA') & (check_input['RBS_受注現法仕入先コード']=='7017')) |
                      ((check_input['ACE参照スキーマ']=='AMI') & (check_input['RBS_受注現法仕入先コード']=='3764')) |
                      ((check_input['ACE参照スキーマ']=='CHN') & (check_input['RBS_受注現法仕入先コード']=='0FCN')) |
                      ((check_input['ACE参照スキーマ']=='SPCM') & (check_input['RBS_受注現法仕入先コード']=='SPCM')))]

# 結合ファイルとdefaultファイルを比較し従来拠点にフラグを付ける
make_flg = check_input.append(default, sort=False)
df_make_flg = make_flg.duplicated(subset=['番号', 'RBS_受注現法仕入先コード'], keep=False)
make_flg.loc[df_make_flg, '従来生産拠点フラグ'] = '1'

make_flg = make_flg[make_flg['ACE参照スキーマ'] != 'Default']

check_input = make_flg

# 正常処理したRECの件数
n_True=check_input['従来生産拠点フラグ'] == '1'
num_True=n_True.sum()

#従来生産拠点がないREC件数の取得
n_jri_e = make_flg.loc[::,['番号', '従来生産拠点フラグ']]#番号と従来生産拠点フラグのみ
n_jri_e = n_jri_e.sort_values(['番号', '従来生産拠点フラグ'])
n_jri_e.drop_duplicates(subset=['番号'], keep='first', inplace=True)#重複削除
n_jri_e = n_jri_e[n_jri_e['従来生産拠点フラグ'].isnull()]#従来生産拠点がnullのみ残す
num_jri_e=len(n_jri_e)#件数数える

#従来生産拠点フラグがないものをcheck_inputから削除
check_input = pd.merge(check_input,n_jri_e,on='番号', how='left', indicator = True)
check_input = check_input[check_input['_merge'] == 'left_only']
check_input.drop(['_merge', '従来生産拠点フラグ_y'], axis=1, inplace=True)
check_input = check_input.rename(columns={'従来生産拠点フラグ_x': '従来生産拠点フラグ'})

# インプットファイルと結合し重複しないRECのインプットファイルのみ残す
prep_input_error = prep_input.append(check_input, sort=False)
prep_input_error.drop_duplicates(subset='番号', keep=False, inplace=True)
#インプットから復活させるRECの従来生産拠点フラグに１つける
prep_input_error['従来生産拠点フラグ'] = '1'

# error_listから復活RECにACE_アンフィット区分とACE_エラーメッセージコードを付与
error_list_t = error_list.loc[::, ['番号', 'JST変換受注日・JST変換見積回答日','JST変換受注時間・JST変換見積回答時間','ACE_アンフィット区分', 'ACE_エラーメッセージコード' ]]
error_list_t = error_list_t.rename(columns={'JST変換受注日・JST変換見積回答日' : 'JST変換受注日・JST変換見積回答日_e','JST変換受注時間・JST変換見積回答時間' : 'JST変換受注時間・JST変換見積回答時間_e'})
# 一つのRECに各スキーマで複数のエラーが発生した際は上段にあるエラーを優先する
error_list_t.drop_duplicates(subset='番号', keep='first', inplace=True)
prep_input_error = pd.merge(prep_input_error, error_list_t, on='番号', how='left',indicator = True)
prep_input_error.loc[prep_input_error['_merge'] == 'both','JST変換受注日・JST変換見積回答日'] = prep_input_error['JST変換受注日・JST変換見積回答日_e']
prep_input_error.loc[prep_input_error['_merge'] == 'both','JST変換受注時間・JST変換見積回答時間'] = prep_input_error['JST変換受注時間・JST変換見積回答時間_e']
prep_input_error.loc[prep_input_error['ACE_アンフィット区分'].notnull(),'アンフィット種別'] = prep_input_error['ACE_アンフィット区分']
prep_input_error.loc[prep_input_error['ACE_アンフィット区分'].notnull(),'ACE参照スキーマ'] = prep_input_error['ACE_エラーメッセージコード']
prep_input_error.drop(['JST変換受注日・JST変換見積回答日_e','JST変換受注時間・JST変換見積回答時間_e', 'ACE_アンフィット区分', 'ACE_エラーメッセージコード', '_merge'], axis=1, inplace=True)

#インプットから復活させるRECのインナーコードの先頭2文字をEにする
#納区、UF対象外、エラーコードありは除く
prep_input_error.loc[((prep_input_error['納入区分'] == '00') | (prep_input_error['納入区分'] == '0L')) & (prep_input_error['アンフィット種別'] == '0'),'インナーコード'] = 'EE' + prep_input_error['インナーコード'].str[-9:]
# 見積りUF RECの従来生産拠点フラグを削除
prep_input_error.loc[prep_input_error['見積有効日'].notnull(), '従来生産拠点フラグ'] = ''
#正常処理したRECと復活させるRECの結合
check_input = check_input.append(prep_input_error, sort=False)

# FCNT→FCNXへ
check_input.loc[check_input['ACE仕入先コード']=='FCNT', 'ACE仕入先コード'] = 'FCNX'

# 管理単位コード付与
'''管理単位が設備コード毎の場合は以下を利用
#管理単位CD付与
#管理単位CD一覧読み込み
MNG_Unit = pd.read_csv('MNG_UNIT_20170101_20180930.csv', encoding=font, dtype='object', index_col=None)
MNG_header = MNG_Unit.columns.values

check_input=pd.merge(check_input,MNG_Unit,left_on='商品コード', right_on='PRODUCT_CD',how='left')
#管理単位CD一覧がExcelの際は下記を使う
#check_input.loc[check_input['RBS_受注現法仕入先コード']=='7017','RBS_管理単位コード']=check_input[7017]
#check_input.loc[check_input['RBS_受注現法仕入先コード']=='3764','RBS_管理単位コード']=check_input[3764]
check_input.loc[check_input['RBS_受注現法仕入先コード']=='7017','RBS_管理単位コード']=check_input['7017']
check_input.loc[check_input['RBS_受注現法仕入先コード']=='3764','RBS_管理単位コード']=check_input['3764']
check_input.loc[check_input['RBS_受注現法仕入先コード']=='0FCN','RBS_管理単位コード']=check_input['0FCN']
check_input.loc[check_input['RBS_受注現法仕入先コード']=='SPCM','RBS_管理単位コード']=check_input['SPCM']
check_input.drop(MNG_header, axis=1, inplace=True)
'''

# 管理単位コードをALに設定
# RBS_管理単位コード
check_input.loc[check_input['RBS_受注現法仕入先コード'] == '7017', 'RBS_管理単位コード'] = 'MAL'
check_input.loc[check_input['RBS_受注現法仕入先コード'] == '3764', 'RBS_管理単位コード'] = 'AAL'
check_input.loc[check_input['RBS_受注現法仕入先コード'] == '0FCN', 'RBS_管理単位コード'] = 'FAL'
check_input.loc[check_input['RBS_受注現法仕入先コード'] == 'SPCM', 'RBS_管理単位コード'] = 'SAL'
# 実績管理単位コード
check_input.loc[check_input['実績仕入先コード'] == '7017', '実績管理単位コード'] = 'MAL'
check_input.loc[check_input['実績仕入先コード'] == '3764', '実績管理単位コード'] = 'AAL'
check_input.loc[check_input['実績仕入先コード'] == '0FCN', '実績管理単位コード'] = 'FAL'
check_input.loc[check_input['実績仕入先コード'] == 'SPCM', '実績管理単位コード'] = 'SAL'

# 実績現法コードを受注現法コードへ変更
check_input.loc[check_input['実績仕入先コード'] == '7017', '実績現法コード'] = 'MJP'
check_input.loc[check_input['実績仕入先コード'] == '3764', '実績現法コード'] = 'MJP'
check_input.loc[check_input['実績仕入先コード'] == '0FCN', '実績現法コード'] = 'CHN'
check_input.loc[check_input['実績仕入先コード'] == 'SPCM', '実績現法コード'] = 'VNM'

# カレンダコードの変更
check_input.loc[check_input['仕入先稼動カレンダコード'] == '5AAAA', '仕入先稼動カレンダコード'] = '5BBBB'
check_input.loc[check_input['仕入先出荷時カレンダコード'] == '5AAAA', '仕入先出荷時カレンダコード'] = '5BBBB'

# 受注日時順に並べ替え
check_input = check_input.sort_values(['JST変換受注日・JST変換見積回答日', 'JST変換受注時間・JST変換見積回答時間', '番号'])


#MCコードの”NA”が消えてしまうので、NAを書き込む
#https://note.nkmk.me/python-pandas-where-mask/
check_input.loc[check_input['グローバル番号'].str[:2] == "NA",'ＭＣコード']="NA"


#従来生産拠点のないエラーファイルのみ取り出す
jri_e = pd.merge(error_list, n_jri_e, on='番号', how='inner')

#1つのRECに従来生産拠点フラグが2つ以上ついていないかチェック
MAS_FLG_E = check_input[((check_input.duplicated(subset=['番号','従来生産拠点フラグ'], keep=False)) & (check_input['従来生産拠点フラグ'] == '1'))]
check_input = check_input[~((check_input.duplicated(subset=['番号','従来生産拠点フラグ'], keep=False)) & (check_input['従来生産拠点フラグ'] == '1'))]

# M単毀損評価用に着荷コスト列を追加
check_input['着荷コスト'] = check_input['RBS_仕入先売単価'] + check_input['RBS_輸入運賃'] + check_input['RBS_関税'] + check_input['RBS_輸入諸掛']
jri_cost =check_input[check_input['従来生産拠点フラグ'] == '1']
jri_cost = jri_cost.rename(columns={'着荷コスト': '従来拠点着荷コスト'})
jri_cost = jri_cost.loc[::, ['番号', '従来拠点着荷コスト']]
check_input = pd.merge(check_input, jri_cost, on='番号', how='left')
# M単毀損行を削除
check_input = check_input[((check_input['着荷コスト'] <= check_input['従来拠点着荷コスト']) | check_input['従来拠点着荷コスト'].isnull())]
check_input.drop(['着荷コスト', '従来拠点着荷コスト'], axis=1, inplace=True)

#check_inputの件数をカウント
num_check_input=len(check_input)

# ホワイトリストの件数をカウント
WL = check_input[((check_input.duplicated(subset=['番号','適用ロジック'], keep='first')) & (check_input['適用ロジック'] == 'a4'))]
num_WL = len(WL)

#件数を出力するファイルの件数を取得
num_prep_input = len(prep_input)
num_error=len(prep_input_error[prep_input_error['見積有効日'].isnull()])
num_QT=len(prep_input_error[prep_input_error['見積有効日'].notnull()])
num_sup_ng=len(SUP_NG)
num_MAS_FLG_E = len(MAS_FLG_E)
jri = len(check_input[check_input['従来生産拠点フラグ'] == '1'])

# 空白埋め用の文字を作成
space = '          '

#string型にしてから行数格納のリストを作成
num_prep_input = space[:(10-len(str(num_prep_input)))] + str(num_prep_input)
num_check_input= space[:(10-len(str(num_check_input)))] + str(num_check_input)
num_True= space[:(10-len(str(num_True - num_WL)))] + str(num_True - num_WL)
num_error= space[:(10-len(str(num_error)))] + str(num_error)
num_jri_e= space[:(10-len(str(num_jri_e)))] + str(num_jri_e)
num_sup_ng = space[:(10-len(str(num_sup_ng)))] + str(num_sup_ng)
num_MAS_FLG_E = space[:(10-len(str(num_MAS_FLG_E)))] + str(num_MAS_FLG_E)
num_jri = space[:(10-len(str(jri+num_QT)))] + str(jri+num_QT)
num_WL = space[:(10-len(str(num_WL)))] + str(num_WL)
num_QT= space[:(10-len(str(num_QT)))] + str(num_QT)

# 基本情報を既述
num = ['UNION_pre_output3.0.py', '\n',
       '入力','\n',
       num_prep_input, ':準備処理inputREC数', '\n',
       num_True, ':内訳 RBS対象REC数', '\n',
       num_WL, ':内訳 ホワイトリストREC数', '\n',
       num_error, ':内訳 シミュレーション対象REC数', '\n',
       num_QT, ':内訳 見積りREC数', '\n',
       '\n',
       '結果', '\n',
       num_jri,':従来生産拠点フラグREC数＋見積りREC数', '\n',
       num_check_input, ':check_input.tsv行数', '\n',
       '\n',
       'エラー','\n']

os.chdir('/data/rbs/mps/UNION_pre_output/output')

# エラーRECがあるかで処理を分岐
if num_sup_ng != '0':
    num = num + [num_sup_ng, ':サプライヤコードNG行数→削除','\n']
    SUP_NG.to_csv('Supplier_CD_NG.tsv', sep='\t', encoding=font, quotechar='"', line_terminator='\n', index=False)

if num_jri_e != '0':
    num = num + [num_jri_e, ':従来生産拠点フラグなしREC数→シミュレーション対象RECへ','\n']
    jri_e.to_csv('従来生産拠点なし_error_list.tsv', sep='\t', encoding=font, quotechar='"', line_terminator='\n', index=False)

if num_MAS_FLG_E != '0':
    num = num + [num_MAS_FLG_E, ':従来生産拠点フラグ重複行数→削除','\n']
    MAS_FLG_E.to_csv('従来生産拠点重複.tsv', sep='\t', encoding=font, quotechar='"', line_terminator='\n', index=False)

# ファイルアウトプット
check_input.to_csv('check_input.tsv', sep='\t', encoding=font, quotechar='"', line_terminator='\n', index=False)
error_list.to_csv('error_list.tsv', sep='\t', encoding=font, quotechar='"', line_terminator='\n', index=False)
with open('log.csv', mode='w') as f:
    f.writelines(num)

print(''.join(num))

print('Finish!')
