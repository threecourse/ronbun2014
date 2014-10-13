# coding=SJIS

u"""
ユーティリティモジュール
"""
import string 

class Settings(object):
    u"設定項目を保持するクラス"
    Max_t = 100

class Util(object):
    u"ユーティリティクラス"

    @classmethod
    def record(cls, header, source, format  = "%12.6f"):
        u"ヘッダおよび関数（tを引数にとるもの）の計算結果を文字列にする"
        return header + "," + string.join([format % source(t) for t in range(0, Settings.Max_t + 1)], ",")

    @classmethod
    def record_single(cls, header, value, format = "%12.6f"):
        u"ヘッダおよび値を文字列にする"
        return header + "," + format % value

    @classmethod
    def at(cls, seq, idx_plus_1):
        u"""
        配列から値を取得する。ここで、添字が配列の範囲を超えている場合は最後の要素の値を取得する。
        第１保険年度⇒idx=0とするため、引数は添字＋１とする。
        """
        idx = idx_plus_1 - 1
        if idx < 0 :
            return 0.0
        if idx < len(seq):
            return seq[idx]
        else:
            return seq[-1]