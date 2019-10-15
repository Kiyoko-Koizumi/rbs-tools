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
import fill_in_overlist_of_Unitprice
import rbs_master

csv.field_size_limit(1000000000)

font = 'utf-8'

def select_func():
    def func1():
        print("未実装、工事中です")

    # ルートフレームの作成
    root = tk.Tk()
    size = 9
    font = u'メイリオ'
    mes = "・商品別仕入先マスタ" + "\n" +"・RBSオーダー振替設定マスタ" + "\n" + "・RBS商品別仕入先マスタ"
    # root.option_add('*font', u'メイリオ')
    label1 = tk.Label(root, text="【処理内容を選択】", font=(font, size))
    label2 = tk.Label(root, text="マスタ作成", font=(font, size))
    label3 = tk.Label(root, text="R.B.Sマスタ作成", font=(font, size))
    label4 = tk.Label(root, text="　　　　　", font=(font, size))
    label5 = tk.Label(root, text="　　　　　", font=(font, size))
    label6 = tk.Label(root, text="　　　　　", font=(font, size))
    label7 = tk.Label(root, text=mes, font=(font, size), justify='left')

    # ボタンの作成（コールバックコマンドには、コンボボックスの値を取得する処理を定義）
    button1 = tk.Button(root, text="Product_master to ECAL",
                        command=lambda: func1(), width=30)
    button1 = tk.Button(root, text="Product_master to ECAL",
                       command=lambda: func1(), width=30)
    button2 = tk.Button(root, text="Product_master to FCN",
                       command=lambda: func1(), width=30)
    button3 = tk.Button(root, text="Product_master to SPC",
                       command=lambda: func1(), width=30)
    button4 = tk.Button(root, text="Unit_price_master to SPC",
                       command=lambda: SPC_U01_Master.SPC_U01_Master(), width=30)
    button5 = tk.Button(root, text="Check_master to SPC",
                       command=lambda: func1(), width=30)
    button14 = tk.Button(root, text="Over_list",
                       command=lambda: func1(), width=15)
    button15 = tk.Button(root, text="Error_list",
                       command=lambda: func1(), width=15)
    button6 = tk.Button(root, text="SPC 仕入値変更",
                       command=lambda: func1(), width=30)
    button10 = tk.Button(root, text="MCOST商品別仕入先数量スライドマスタ",
                       command=lambda: func1(), width=30)
    button11 = tk.Button(root, text="MCOST単価数量スライドマスタ",
                       command=lambda: func1(), width=30)
    button12 = tk.Button(root, text="MCOST商品チェック詳細マスタ",
                       command=lambda: func1(), width=30)
    button14 = tk.Button(root, text="商品、商品別仕入先マスタより抽出",
                       command=lambda: rbs_master.rbs_master(), width=30)
    button13 = tk.Button(root, text="処理終了",
                       command=lambda: sys.exit())
    # コンボボックスの配置
    label1.grid(row=0, column=0)
    label2.grid(row=1, column=0)
    label3.grid(row=8, column=0)
    label4.grid(row=0, column=1)
    label5.grid(row=0, column=3)
    label6.grid(row=7, column=3)
    # ボタンの配置
    button1.grid(row=1, column=2)
    button2.grid(row=2, column=2)
    button3.grid(row=3, column=2)
    button4.grid(row=4, column=2)
    button5.grid(row=5, column=2)
    button14.grid(row=3, column=4)
    button15.grid(row=4, column=4)
    button6.grid(row=6, column=2)
    button14.grid(row=8, column=2)
    label7.grid(row=9, column=2)
    button10.grid(row=12, column=2)
    button11.grid(row=13, column=2)
    button12.grid(row=14, column=2)
    button13.grid(row=15, column=5)
    root.mainloop()
    return

if __name__ == '__main__':
    select_func()
    print('Finish!')