* 概要
  プライシング用のプロジェクションツールです。
  Python 2.7で記述しています。

* 使い方
  main.pyを実行すると、計算が実行され、レポート(ResultReport.csv, DumpReport.csv)が出力されます。

* モデル
　終身保険・定期保険・養老保険をモデル化しています。
　終身保険は、日本アクチュアリー会教科書 保険１ 第１０章商品別収益検証 付録１表６　保険年度単位のキャッシュフロー
　を再現しようとしたモデルです。（細かいところは異なります）
 終身保険はWLModel.py, WLRate.pyでモデル・レートのクラスを作成していて、
 他の保険種類も同様に作成することができます。

* 速度
　30セルの計算が1秒程度（CPU: Core i7-4500U）なので、プライシングには十分な速度と思われます。
