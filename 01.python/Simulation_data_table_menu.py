# coding: utf-8
# モジュールのインポート
import os
import csv
import pandas as pd
import sys
import glob
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import tkinter as tk
import tkinter.ttk as ttk
from Orders_creation import Orders_creation_change_date

csv.field_size_limit(1000000000)

font = 'utf-8'

script_pass = os.path.dirname(os.path.abspath(__name__))

def select_func():
    # ルートフレームの作成
    root = tk.Tk()
    label1 = tk.Label(root, text="【処理内容を選択】", font=("", 12), height=2)
    label4 = tk.Label(root, text="　　　　　", font=("", 12), height=2)
    label5 = tk.Label(root, text="　　　　　", font=("", 12), height=2)

    # ボタンの作成（コールバックコマンドには、コンボボックスの値を取得する処理を定義）
    button1 = tk.Button(root, text="ダミーオーダー作成　日付変更あり",
                       command=lambda: Orders_creation_change_date.Orders_creation_change_date(), width=30)
    button2 = tk.Button(root, text="ダミーオーダー作成　日付変更なし",
                       command=lambda: func2(), width=30)
    button3 = tk.Button(root, text="受注予測作成",
                       command=lambda: func3(), width=30)
    button4 = tk.Button(root, text="割付数量・加工済数量作成",
                       command=lambda: func4(), width=30)
    button13 = tk.Button(root, text="処理終了",
                       command=lambda: root.destroy())
    # コンボボックスの配置
    label1.grid(row=0, column=0)
    label4.grid(row=0, column=1)
    label5.grid(row=0, column=3)

    # ボタンの配置
    button1.grid(row=1, column=2)
    button2.grid(row=2, column=2)
    button3.grid(row=3, column=2)
    button4.grid(row=4, column=2)
    button13.grid(row=13, column=4)
    root.mainloop()
    return

if __name__ == '__main__':
    select_func()
    print('Finish!')