# -*- coding: utf-8 -*-
import pandas 
import statsmodels.api as sm
import patsy as patsy
import numpy as np
import matplotlib.pyplot as plt

# ファイルの読み込み ===========================================

# 以下からdiabetes.csv(糖尿病による死者データ）を取得する
# http://www.businessandeconomics.mq.edu.au/our_departments/Applied_Finance_and_Actuarial_Studies/research/books/GLMsforInsuranceData/data_sets

# csvファイルをデータフレームに読み込む
df = pandas.read_csv('diabetes.csv')

# 最終行が不要だったので、それを削除する
df = df[:-1] 
print df


# モデルの作成 ======================================================

# オフセット項の定義
offset_term = df['l_popn']

# モデル行列の作成
y_1, X_1 = patsy.dmatrices(
  'deaths ~ gender + agemidpt', data=df, return_type='dataframe')
y_2, X_2 = patsy.dmatrices(
  'deaths ~ gender + C(age,Treatment("45-54"))',
  data=df, return_type='dataframe')

# GLMモデルの作成 
model1 = sm.GLM(y_1, X_1, family=sm.families.Poisson(link=sm.families.links.log), 
                offset = offset_term )
model2 = sm.GLM(y_2, X_2, family=sm.families.Poisson(link=sm.families.links.log), 
                offset = offset_term )

# 結果の表示（サマリーの表示）===================================

# モデルのフィット
fit1 = model1.fit()
fit2 = model2.fit()

# モデルのサマリーの表示
print fit1.summary()
print fit2.summary()


# 結果の表示（AIC・逸脱度の表示） ===================================

# statsmodels ver0.5.0 では、逸脱度の計算にバグがあるため、ここで定義した。
# ver0.6.0では修正される予定
def poisson_deviance(fit):
    Y = fit.model.endog
    mu = fit.fittedvalues
    return np.where(Y == 0, 0, Y * np.log(Y / mu)).sum() * 2

models = [model1, model2]
modelnames = ['model1', 'model2']

#　AIC・逸脱度を一度データフレームに入れ、表示させた。
params_df = pandas.DataFrame()
params_df['name'] = modelnames
params_df['aic'] = [m.fit().aic for m in models]
params_df['deviance'] = [poisson_deviance(m.fit()) for m in models]

print params_df


# プロット ===================================
from matplotlib.backends.backend_pdf import PdfPages

# PDF出力の設定
pdf = PdfPages('glm_mortality.pdf')
plt.close('all')

# 各モデルの死亡数の推定値を入れたデータフレームを作成する
fitted_df = pandas.DataFrame()
fitted_df[['gender', 'agemidpt', 'popn', 'observed']] = df[['gender', 'agemidpt', 'popn', 'deaths']]
for i in range(0, len(models)):
    fitted_df[modelnames[i]] = models[i].fit().fittedvalues

# 各モデルの死亡数の推定値を死亡率に変換したデータフレームを作成する
mort_df = fitted_df.copy()
obs_and_models_name = ['observed'] + modelnames 

for name in obs_and_models_name:
    mort_df[name] = mort_df[name] * 1.0 /  mort_df['popn'] 

# 男性の死亡率をプロットする
mort_df_M = mort_df[mort_df['gender'] == "Male"]
fig, ax = plt.subplots(1,1)
mort_df_M.plot(ax = ax, x = mort_df_M['agemidpt'], y = obs_and_models_name, 
              marker='o', xticks = mort_df_M['agemidpt'], xlim = [15, 95], 
              title = "Mortality_Male", label = obs_and_models_name)
ax.set_xlabel("")
ax.legend(loc='best')
pdf.savefig()
#plt.savefig("mortM.png")

# 女性の死亡率をプロットする
mort_df_F = mort_df[mort_df['gender'] == "Female"]
fig, ax = plt.subplots(1,1)
mort_df_F.plot(ax = ax, x = mort_df_F['agemidpt'], y = obs_and_models_name, 
              marker='o', xticks = mort_df_F['agemidpt'], xlim = [15, 95], 
              title = "Mortality_Female", label = obs_and_models_name)
ax.set_xlabel("")
ax.legend(loc='best')
pdf.savefig()
#plt.savefig("mortF.png")

pdf.close()
