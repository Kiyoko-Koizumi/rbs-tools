# coding: utf-8
# PRODUCTION_THRESHOLD 新規作成 2019/6/3
#

# モジュールのインポート
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import csv
import xlrd
from typing import List
import glob
import pandas as pd
import datetime as dt
import tkinter as tk
import tkinter.ttk as ttk
import threading
from dateutil.relativedelta import relativedelta
import pandas.tseries.offsets as offsets
from multiprocessing import Pool
import multiprocessing as multi
import numpy as np
import os
import glob


def make_calendar()
    # Excel取り込み
    input_file_name = '*.xlsx'
    input_book = pd.ExcelFile(input_file_name)
    # Excelブック内の各シートの名前をリストで取得
    input_sheet_name = input_book.sheet_names
    #カラム追加のためにシート名取得
    sheet_name =input_book.sheet_names[0]

    #縦連結のために月ごとにDataFrameとしてsheetを読込、
    df1 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[1, 4])
    df1 = df1.rename(columns={'日': '日付','稼動':'稼働日'})
    df2 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[7, 10])
    df2 = df2.rename(columns={'日.1': '日付','稼動.1':'稼働日'})
    df3 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[13,16])
    df3 = df3.rename(columns={'日.2': '日付','稼動.2':'稼働日'})
    df4 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[19,22])
    df4 = df4.rename(columns={'日.3': '日付','稼動.3':'稼働日'})
    df5 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[25,28])
    df5 = df5.rename(columns={'日.4': '日付','稼動.4':'稼働日'})
    df6 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[31,34])
    df6 = df6.rename(columns={'日.5': '日付','稼動.5':'稼働日'})
    df7 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[37,40])
    df7 = df7.rename(columns={'日.6': '日付','稼動.6':'稼働日'})
    df8 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[43,46])
    df8 = df8.rename(columns={'日.7': '日付','稼動.7':'稼働日'})
    df9 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[49,52])
    df9 = df9.rename(columns={'日.8': '日付','稼動.8':'稼働日'})
    df10 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[55,58])
    df10 = df10.rename(columns={'日.9': '日付','稼動.9':'稼働日'})
    df11= input_book.parse(input_sheet_name[0],skiprows=12, usecols=[13,16])
    df11 = df11.rename(columns={'日.2': '日付','稼動.2':'稼働日'})
    df12 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[61,64])
    df12 = df12.rename(columns={'日.10': '日付','稼動.10':'稼働日'})
    df13 = input_book.parse(input_sheet_name[0],skiprows=12, usecols=[67,70])
    df13 = df13.rename(columns={'日.11': '日付','稼動.11':'稼働日'})

    calendar = pd.concat([df1, df2,df3, df4,df5, df6,df7, df8,df9, df10,df11, df12,df13])
    for index, row in calendar.iterrows():
     calendar['Supplier'] = sheet_name

for calendar in  glob.glob(r'C:\Users\Aoi_Fujishita\OneDrive\PPPF\2.BIツール_見える化\週次検証\Calendar\*.xlsx')

#サプライヤーカレンダーCDの読み込み
SP_name = pd.read_csv('SP_name.csv', encoding='utf-8', dtype='object', index_col=None)
calendar = pd.merge(calendar, SP_name, on=['Supplier'], how='left')
calendar =calendar.loc[:,['日付', '稼働日', 'SP_name']]
print(calendar)


# ファイルアウトプット
f_name = 'calendar.tsv'
calendar.to_csv(f_name, sep='\t', encoding='utf-8', index=True)
print('DONE!')