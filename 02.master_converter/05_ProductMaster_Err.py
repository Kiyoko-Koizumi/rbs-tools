# New Slideデータ作成
import pandas as pd
import numpy as np
path='//172.24.81.185/share1/share1c/加工品SBU/加工SBU共有/派遣/■Python_SPC_Master/temp_data/'

# over_slide・sales(n)<sales(n+1)・purchase(n)<purchase(n+1)・slide1=(sales=0 and purchase>0) or (sales>0 and purchase=0)
new_slide = (pd.read_csv(path + 'New_Slide.txt',sep='\t', encoding='utf_16', dtype=object, engine='python', error_bad_lines=False))
new_slide['new_slide_no'] = new_slide['new_slide_no'].astype(int)
df = (new_slide.query('new_slide_no > 10'))  # Over_Slide_Check
df['err_1']=1   # Over_slide
h_order=({'Subsidiary Code':0,'Product Code':1,'err_1':2})
df.drop_duplicates(subset=['Product Code', 'Subsidiary Code'],keep='first',inplace=True)
df = df.loc[:, h_order]


n = len(new_slide)
for i in range(0, n):

print(df)