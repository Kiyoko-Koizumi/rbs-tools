#0.2 ファイル選択ダイアログの追加と、それに伴うファイル読み込みソースの変更
# git向けにファイル名変更
# J_LS19_101専用

##pandasを呼び出す
import pandas as pd
import os
import csv

csv.field_size_limit(1000000000)

# ファイル名で記述
f_name = ['input.tsv', 'input_RBS_OUTPUT.tsv_Default', 'input_RBS_OUTPUT_ERROR.tsv_Default', 'input_RBS_OUTPUT.tsv_MPA', 'input_RBS_OUTPUT_ERROR.tsv_MPA', 'input_RBS_OUTPUT.tsv_AMI', 'input_RBS_OUTPUT_ERROR.tsv_AMI', 'input_RBS_OUTPUT.tsv_CHN',
          'input_RBS_OUTPUT_ERROR.tsv_CHN', 'input_RBS_OUTPUT.tsv_SPCM', 'input_RBS_OUTPUT_ERROR.tsv_SPCM', 'input_RBS_OUTPUT.tsv_AMI_MCOST', 'input_RBS_OUTPUT_ERROR.tsv_AMI_MCOST', 'input_RBS_OUTPUT.tsv_CHN_MCOST', 'input_RBS_OUTPUT_ERROR.tsv_CHN_MCOST',
          'input_RBS_OUTPUT.tsv_SPCM_MCOST', 'input_RBS_OUTPUT_ERROR.tsv_SPCM_MCOST']

os.chdir("/data/rbs/mps/01.割振り準備処理/J_LS19_101/output/")
for i in range(1,17):
    file = pd.read_csv(f_name[i], sep='\t', dtype='object', index_col=None)
    file = file.astype({'顧客希望納期':int})
    DEC= file.query( '20191201 <= 顧客希望納期 <= 20191231')
    JAN = file.query('20200101 <= 顧客希望納期 <= 20200131')
    #MC_CDの”NA”が消えてしまうので、NAを書き込む
    DEC.loc[DEC['グローバル番号'].str[:2] == "NA",'ＭＣコード']="NA"
    JAN.loc[JAN['グローバル番号'].str[:2] == "NA",'ＭＣコード']="NA"
    #アウトプット
    os.chdir("/data/rbs/mps/01.割振り準備処理/J_LS19_011/output/")
    DEC.to_csv(f_name[i],sep="\t",index=False)
    os.chdir("/data/rbs/mps/01.割振り準備処理/J_LS19_012/output/")
    JAN.to_csv(f_name[i],sep="\t",index=False)

print('finish!')
