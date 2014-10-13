# -*- coding: utf-8 -*-
u"""
 保有データ・支払データを集計するプログラム
"""

import os as os
import pandas as pd
import numpy as np
import Input
import itertools
import functools

workdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(workdir) 

# 前提を読み込む -------------------------------
asm = Input.Assumption("Assumption.csv")
qx_f = asm.get_float_list("qx_f_SLT1996")
qx_m = asm.get_float_list("qx_m_SLT1996")

# Step0 保有データ・支払データを読み込む -------------------------------
df_inforce = pd.read_csv("inforce.csv")
df_pay = pd.read_csv("pay.csv")

# 年齢階級を追加する
df_inforce['x_class'] = (df_inforce['x'] // 5) * 5
df_pay['x_class'] = (df_pay['x'] // 5) * 5

# Step1 予定N・予定Sを付加する ---------------------

# 行を引数にとり、予定発生率を返す関数
def mort_rate(series):
    sex = series['sex']
    x = series['x_class'] + 2
    if sex == 'm' : return qx_m[min(x, len(qx_m) - 1)]            
    if sex == 'f' : return qx_f[min(x, len(qx_f) - 1)]            
    raise Exception('invalid sex')

# 保有データに予定発生率、予定N、予定Sを付加する
df1_inf = df_inforce.copy()
df1_inf['mort_rate'] = df1_inf.apply(mort_rate, axis = 1)
df1_inf['expected_N'] = df1_inf['mort_rate'] * 1.0
df1_inf['expected_S'] = df1_inf['mort_rate'] * df1_inf['S']

# 支払データには特になにもしない
df1_pay = df_pay.copy()


# Step2 （性別・年齢階級）、（性別、経過）でグルーピングし、枠に当てはめる --------------


#  保有データのグルーピングを引数にとり、行を返す関数
def aggregate_inf(group):
     N = len(group)
     S = group['S'].sum()
     expected_N = group['expected_N'].sum()
     expected_S = group['expected_S'].sum()
     return pd.Series([N, S, expected_N, expected_S], 
                       index=['inforce_N', 'inforce_S', 'expected_N', 'expected_S'])

# 支払データのグルーピングを引数にとり、行を返す関数
def aggregate_pay(group):
     N = len(group)
     S = group['S'].sum()
     return pd.Series([N, S], index=['pay_N', 'pay_S'])

# 保有データをグルーピングする関数
def groupby_inf(df, group_cols):
    g = df.groupby(group_cols, as_index =False)
    g = g.apply(aggregate_inf)
    g.reset_index(inplace=True)
    return g

# 支払データをグルーピングする関数
def groupby_pay(df, group_cols):
    g = df.groupby(group_cols, as_index =False)
    g = g.apply(aggregate_pay)
    g.reset_index(inplace=True)
    return g
    

# （性別・年齢階級）でグルーピングしたテーブルの枠 
def template_x():
    keylist_sex = ['f','m','total']
    keylist_x = range(0, 100, 5) + [999]
    keys = list(itertools.product(keylist_sex, keylist_x))
    return pd.DataFrame(keys, columns = ['sex','x_class'])

# （性別、経過）でグルーピングしたテーブルの枠
def template_t():
    keylist_sex = ['f','m','total']
    keylist_t =  range(1,15+1) + [999]
    keys = list(itertools.product(keylist_sex, keylist_t))
    return pd.DataFrame(keys, columns = ['sex','elapsed'])

# 保有データ・支払データを枠に合わせて結合する    
def merge_dfs(df_template, df_inf, df_pay, key_cols):
    df = df_template
    df = pd.merge(df, df_inf, on = key_cols, how='left')
    df = pd.merge(df, df_pay, on = key_cols, how='left')
    df = df.fillna(0)
    return df


# 小計を作成する
def get_subtotal(series, df, key1, key_total1, key2, key_total2):
    value_cols = ['inforce_N', 'inforce_S', 'expected_N', 'expected_S','pay_N', 'pay_S']
    
    if series[key1] == key_total1:
        mask1 = df[key1] != key_total1
    else:
        mask1 = df[key1] == series[key1]

    if series[key2] == key_total2 :
        mask2 = df[key2] != key_total2
    else:
        mask2 = df[key2] == series[key2]
    
    mask = mask1 & mask2                
    series[value_cols] = df[mask][value_cols].sum()
    return series

# 年齢別の場合の小計に値を入力する
def calc_subtotal_x(df):
    func = functools.partial(get_subtotal,
       df=df, key1='sex', key_total1='total', key2='x_class', key_total2=999 )
    return df.apply(func, axis=1)

# 経過別の場合の小計に値を入力する
def calc_subtotal_t(df):
    func = functools.partial(get_subtotal,
       df=df, key1='sex', key_total1='total', key2='elapsed', key_total2=999 )
    return df.apply(func, axis=1)
    

# 年齢別の場合 -----

# 保有データ、支払データをグルーピングする
df2_inf_x = groupby_inf(df1_inf , ['sex','x_class'])
df2_pay_x = groupby_pay(df1_pay , ['sex','x_class'])

# 枠とmergeすることにより、枠に当てはめる
df2_x = merge_dfs(template_x(), df2_inf_x, df2_pay_x, ['sex','x_class'])

# 小計に値を入力する
df2_x = calc_subtotal_x(df2_x)

# 出力する
df2_x.to_csv("df2_x.csv", index = False)


# 経過別の場合 -----
df2_inf_t = groupby_inf(df1_inf , ['sex','elapsed'])
df2_pay_t = groupby_pay(df1_pay , ['sex','elapsed'])

df2_t = merge_dfs(template_t(), df2_inf_t, df2_pay_t, ['sex','elapsed'])
df2_t = calc_subtotal_t(df2_t)
df2_t.to_csv("df2_t.csv", index = False)


# step3 選択効果を追加する ------------------------

df3_x = df2_x.copy()
df3_x['SF_N'] = df3_x['pay_N'] / df3_x['expected_N']
df3_x['SF_S'] = df3_x['pay_S'] / df3_x['expected_S']
df3_x.to_csv("df_fin_x.csv", index = False)

df3_t = df2_t.copy()
df3_t['SF_N'] = df3_t['pay_N'] / df3_t['expected_N']
df3_t['SF_S'] = df3_t['pay_S'] / df3_t['expected_S']
df3_t.to_csv("df_fin_t.csv", index = False)
