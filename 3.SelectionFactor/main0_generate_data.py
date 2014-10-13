# -*- coding: utf-8 -*-
u"""
 保有データ・支払データを生成するプログラム
"""

import os as os
import pandas as pd
import numpy as np
import Input
import random

workdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(workdir) 

# 前提を読み込む -------------------------------

asm = Input.Assumption("Assumption.csv")

print "Assumption:"
for k in asm.Values.keys():
    val = asm.Values[k]
    print " - %s : items %s" % (k, len(val))

selection_factor = asm.get_float_list("SelectionFactor")
popn_f = asm.get_float_list("popn_f")
popn_m = asm.get_float_list("popn_m")
qx_f = asm.get_float_list("qx_f_SLT1996")
qx_m = asm.get_float_list("qx_m_SLT1996")

# 保有データを生成する -------------------------------

# 乱数の初期化
random.seed(12345)

def write_inforce_header(f):
    header = "{0},{1},{2},{3}\n".format("x", "sex", "elapsed", "S")
    f.write(header)
    
def write_inforce_data(f, popn, sex):
    x_range = range(10, 95) # age 10-94
    
    elapsed_ary = range(1,15+1) # elapsed 1-15
    S_ary = [100,200,500,1000] # S 100,200,500,1000
    
    for x in x_range:
        popx = int(popn[x])
        for i in range(0, popx):
            elapsed = elapsed_ary[random.randint(0,14)]
            S = S_ary[random.randint(0,3)]
            
            line = "{0},{1},{2},{3}\n".format(x, sex, elapsed, S)
            f.write(line)
            
f = open('inforce.csv', 'w')
write_inforce_header(f)
write_inforce_data(f, popn_f, "f")
write_inforce_data(f, popn_m, "m")
f.close()


# 支払データを生成する -------------------------------

# 乱数の初期化
random.seed(34567)

# 保有データを読み込む
data_inforce = pd.read_csv("inforce.csv")

# 死亡率を求める関数
def get_mort_rate(x, sex):
    if sex == 'm' : return qx_m[min(x, len(qx_m) - 1)]            
    if sex == 'f' : return qx_f[min(x, len(qx_f) - 1)]            
    raise Exception('invalid sex')

# 選択効果を求める関数
def get_selection_factor(elapsed):
    # 配列selection_factorは1から始まるので、idxを調整
    return selection_factor[min(elapsed - 1, len(selection_factor) - 1)]

def write_pay_header(f):
    header = "{0},{1},{2},{3}\n".format("x", "sex", "elapsed", "S")
    f.write(header)

def write_pay_data(f, data_inforce):
    for index, row in data_inforce.iterrows():
        x = row['x']
        sex = row['sex']
        elapsed = row['elapsed']
        S = row['S']
        qx = get_mort_rate(x, sex) * get_selection_factor(elapsed) 
        rand = random.random() 
        if rand < qx: # 乱数が死亡率より小さいとき、死亡が発生したとなる
            line = "{0},{1},{2},{3}\n".format(x, sex, elapsed, S)
            f.write(line)
            
f = open('pay.csv', 'w') 
write_pay_header(f)
write_pay_data(f, data_inforce)
f.close() # close file

data_pay = pd.read_csv("pay.csv")
