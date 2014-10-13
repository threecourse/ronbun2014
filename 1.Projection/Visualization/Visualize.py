#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os as os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.cm as cm

# カレントディレクトリの設定
workdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(workdir) 

def main():
    
    # PDF出力の設定
    pdf = PdfPages('resultreport.pdf')

    # 初期化    
    plt.close('all')
    
    # resultreportの読み込み
    df_result = pd.read_csv("..\\files_result\\ResultReport.csv")
    
    # plotの作成
    create_plot(df_result[:11], pdf)
    create_plot(df_result[11:21], pdf)
    create_plot(df_result[21:], pdf)
    
    pdf.close()

def create_plot(_df, _pdf):
    fig, ax = plt.subplots(1,1)
    df = _df.copy()
    
    # plotの図示
    
    # plot用変数
    n = len(df)
    ind = np.arange(n) 
    colors = cm.rainbow(np.linspace(0, 1, 10)) # 色を設定    
    
    bars = []
    btm = np.zeros(len(df))    
    
    # plotの図示 - 各給付の割合の図示
    cols_elements = list(df.columns[5:])

    for i, col in enumerate(cols_elements):
        values = df[col]
        bar = ax.bar(ind, values, color=colors[i], bottom=btm, align='center')
        bars.append(bar)
        btm += values
    
    # plotの図示 - ProfitMarginの図示
    col_pm = 'ProfitMargin'
    values_pm = df[col_pm]
    values_pm_min0 = map(lambda x: max(x, 0), values_pm) 
    bar_pm = ax.bar(ind, values_pm_min0, color='r', bottom=btm, align='center')
    bars.append(bar_pm)
    
    # 表示項目の設定
    ax.set_title(u'Ratio of Benefits and Profit Margin')

    fp = fm.FontProperties(size=10)
    ax.legend(bars + [bar_pm], cols_elements + [col_pm], 
              prop=fp, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.subplots_adjust(right=0.65)
    
    ax.axhline(y=1.0, linestyle= '-', color='#aaaaaa')
    
    ax.set_xlim([-0.7, n - 0.3])
    xticks = np.arange(0, n)
    description = list(df["Descripton"])
    ax.set_xticks(xticks)
    ax.set_xticklabels(description, rotation=30)
    
    ax.set_ylim([0,1.2])
    ax.set_yticks(np.arange(0, 1.2, 0.2))
    ax.set_yticklabels(map(lambda v : str(v) + '%', np.arange(0, 120, 20)))
    
    # 表示・PDFの保存
    _pdf.savefig()
    plt.show()

main()
