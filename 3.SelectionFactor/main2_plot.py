# -*- coding: utf-8 -*-
u"""
 集計したデータからプロットを行うプログラム
"""

import os as os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from scipy import stats
from matplotlib.backends.backend_pdf import PdfPages

workdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(workdir) 

# 0-1.共通の設定 -------------------------------

# PDF出力の設定
pdf = PdfPages('selection_factors_plot.pdf')

# 日本語表示用フォント
#Vfontprop_meiryo = fm.FontProperties(fname=u"C:\Windows\Fonts\meiryo.ttc")

# 日本語フォントを扱う場合、埋め込みの設定が必要
# plt.rcParams['pdf.fonttype'] = 42

# 初期化しておく
plt.close('all')

# 保有データ・支払データを読み込む 
dfplot1_x = pd.read_csv("df_fin_x.csv")
dfplot1_t = pd.read_csv("df_fin_t.csv")

# 0-2.データ作成の共通ロジック -------------------------------

# プロットデータ作成の共通ロジック
def create_plot_data(_df, key, _sex, col_y, col_yerr_tpl = None):
    
    df = _df.copy()
    _filter = ((df['sex'] == _sex) & (df[key] != 999)) # 999 は合計
        
    x = df[key][_filter]
    x = map(float, x) # なぜかこうしないと、barplotでalign='center'の場合にエラーになる。    
    y = df[col_y][_filter]
    
    if col_yerr_tpl is None : 
        return x, y
    else : 
        # 信頼区間用のyを計算する場合
        y_err0 = df[col_yerr_tpl[0]][_filter]
        y_err1 = df[col_yerr_tpl[1]][_filter]
        return x, y, (y_err0, y_err1)

# プロットの説明等の表示（選択効果）
def setplot_for_selection_factor(_ax, key):
    if key == 'x_class':
        xlabel = 'age' 
        xlim = [-5,100]
        xticks = np.arange(0, 100, 5)   
    elif key == 'elapsed':
        xlabel = 'elapsed'
        xlim = [0,15+1]
        xticks = xticks = np.arange(1, 16, 1)
    else:
        raise Exception()
    
    _ax.set_xlabel(xlabel)
    _ax.set_xlim(xlim)
    _ax.set_xticks(xticks)
    _ax.set_xticklabels(xticks)
    
    _ax.set_ylabel('selection factor S')    
    _ax.set_ylim([0,2])
    _ax.set_yticks(np.arange(0, 2, 0.1))
    _ax.set_yticklabels(map(lambda v : str(v) + '%', np.arange(0, 200, 10)))
    
    _ax.legend(loc='best')
    _ax.axhline(y=1, linestyle= '-', color='#aaaaaa')

# プロットの説明等の表示（死差益）
def setplot_for_mortality_profit(_ax, key):
    if key == 'x_class':
        xlabel = 'age' 
        xlim = [-5,100]
        xticks = np.arange(0, 100, 5)   
    elif key == 'elapsed':
        xlabel = 'elapsed'
        xlim = [0,15+1 ]
        xticks = xticks = np.arange(1, 16, 1)
    else:
        raise Exception()
    
    _ax.set_xlabel(xlabel)
    _ax.set_xlim(xlim)
    _ax.set_xticks(xticks)
    _ax.set_xticklabels(xticks)
    
    _ax.set_ylabel('mortality profit')    
    _ax.set_ylim([-10000,30000]) # 今回はこの範囲とした。
    
    _ax.legend(loc='best')
    _ax.axhline(y=0, linestyle= '-', color='#aaaaaa')

# 棒グラフの横幅
def width_for_mortality_profit(key):
    if key == 'x_class':
        return 4.0
    elif key == 'elapsed':
        return 0.8
    else:
        raise Exception()
    

# 1. 選択効果 -------------------------------
def create_plot1(_df, key):
    fig, ax = plt.subplots(1,1)
    
    # データの作成
    x_m, y_m= create_plot_data(_df, key, 'm', 'SF_S')    
    x_f, y_f= create_plot_data(_df, key, 'f', 'SF_S')    
    x_t, y_t= create_plot_data(_df, key, 'total', 'SF_S')    

    # プロット
    ax.plot(x_m, y_m,  linestyle='-', color='b', marker='o', label='m')
    ax.plot(x_f, y_f,  linestyle='-', color='r', marker='o', label='f')
    ax.plot(x_t, y_t,  linestyle='-', color='k', marker='o', label='total')

    # 表示項目の作成
    ax.set_title(u'Selection Factor S')
    setplot_for_selection_factor(ax, key)
    
    # 保存・出力
    pdf.savefig()
    #plt.show()
    
create_plot1(dfplot1_x, 'x_class')
create_plot1(dfplot1_t, 'elapsed')


# 2.選択効果＋信頼区間エラーバー ------------------------------

# エラーバー作成のため、信頼区間上限・下限の選択効果の列を付加する
def confidence_interval_SF(n, p, sf):
    u"""
    選択効果の両側95%の信頼区間を求める。
    ・二項分布の標準偏差の1.96倍によって計算
    ・n = 保有件数、p = 実績S支払率として計算
    """
    
    std = stats.binom.std(n,p)
    lower_p = max(p - 1.96 * std / n , 0)
    upper_p =     p + 1.96 * std / n
    lowerSF = sf * lower_p / p
    upperSF = sf * upper_p / p
    return lowerSF, upperSF

def confidence_interval_SF_lower(n, p, sf):
    l, u = confidence_interval_SF(n, p, sf)
    return l
    
def confidence_interval_SF_upper(n, p, sf):
    l, u = confidence_interval_SF(n, p, sf)
    return u

def add_confidence_interval_SF(_df):
    df = _df.copy()
    col_n = df['inforce_N']
    col_p = df['pay_S'] / df['inforce_S']
    col_SF = df['SF_S']
    col_CI_lower = map(confidence_interval_SF_lower, col_n, col_p, col_SF)
    col_CI_upper = map(confidence_interval_SF_upper, col_n, col_p, col_SF)
    df['CIlower_SF_S'] = col_CI_lower
    df['CIupper_SF_S'] = col_CI_upper
    
    # プロット用
    df['err_CIlower_SF_S'] = df['SF_S'] - df['CIlower_SF_S']
    df['err_CIupper_SF_S'] = df['CIupper_SF_S'] - df['SF_S']
    return df

dfplot2_x = add_confidence_interval_SF(dfplot1_x)
dfplot2_t = add_confidence_interval_SF(dfplot1_t)


def create_plot2_each(_df, key, _sex, _color):
    fig, ax = plt.subplots(1,1)

    # データの作成
    x, y, _y_err = create_plot_data(_df, key, _sex, 'SF_S',
                            ('err_CIlower_SF_S','err_CIupper_SF_S'))

    # プロット
    ax.errorbar(x, y, yerr=_y_err, 
                linestyle='-', color=_color, marker='o', label=_sex)
    
    # 表示項目の作成
    ax.set_title(u'Selection Factor S - 95% Confidence Interval')
    setplot_for_selection_factor(ax, key)
    
    pdf.savefig()
    #plt.show()
    
def create_plot2(_df, key):
    create_plot2_each(_df, key, 'm', 'b')
    create_plot2_each(_df, key, 'f', 'r')

create_plot2(dfplot2_x, 'x_class')
create_plot2(dfplot2_t, 'elapsed')


# 3.死差益＋信頼区間エラーバー　------------------------------

# 死差益（粗発生率を基準としたもの）を作成する
def add_mortality_profits(_df):
    df = _df.copy()
    df['m_profits'] = df['expected_S'] * (1 - df['SF_S'])
    
    # 選択効果の信頼区間下限が、死差益の信頼区間上限になる。
    df['CIlower_m_profits']  =df['expected_S'] * (1 - df['CIupper_SF_S'])
    df['CIupper_m_profits']  =df['expected_S'] * (1 - df['CIlower_SF_S'])
    
    # プロット用
    df['err_CIlower_m_profits']  = df['m_profits'] - df['CIlower_m_profits']
    df['err_CIupper_m_profits']  = df['CIupper_m_profits'] - df['m_profits']
    
    return df
    
dfplot3_x = add_mortality_profits(dfplot2_x)
dfplot3_t = add_mortality_profits(dfplot2_t)


def create_plot3_each(_df, key, _sex, _color):
    fig, ax = plt.subplots(1,1)

    # データの作成
    x, y, _y_err = create_plot_data(_df, key, _sex, 'm_profits',
                        ('err_CIlower_m_profits','err_CIupper_m_profits'))
    _width = width_for_mortality_profit(key)

    # プロット
    ax.bar(x, y, width = _width, align='center',
           yerr=_y_err, color=_color, label=_sex,
           error_kw=dict(ecolor='k'))
    
    # 表示項目の作成
    ax.set_title(u'Mortality Profit - 95% Confidence Interval')
    setplot_for_mortality_profit(ax, key)
    
    pdf.savefig()
    #plt.show()
    
def create_plot3(_df, key):
    create_plot3_each(_df, key, 'm', 'b')
    create_plot3_each(_df, key, 'f', 'r')

create_plot3(dfplot3_x, 'x_class')
create_plot3(dfplot3_t, 'elapsed')

pdf.close()