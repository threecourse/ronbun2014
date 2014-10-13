# coding=SJIS

u"""
インスタンスメソッドのメモ化用モジュール

インスタンスメソッドに利用できるメモリリークの起こらないMemoize実装
（インスタンスメソッドにのみ使用可能）
通常のMemoizeの実装では、複数インスタンスを生成した際にメモリリークが起ってしまうことに注意。

以下を参考。元の実装はやや遅いため、修正している。
http://code.activestate.com/recipes/577452-a-memoize-decorator-for-instance-methods/
"""

import collections
import functools

def initialize_memoize(self):
    u"""
    クラスをメモ化対応にするメソッド
    メモ化されるインスタンスメソッドを持つクラスのコンストラクタでこれを行うことが必要
    """

    self.cache = {}

class memoized(object):
    u"インスタンスメソッドのメモ化を行うデコレータ"

    def __init__(self, func):
        self.func = func
    def __get__(self, obj, objtype=None):
        return functools.partial(self, obj)
    def __call__(self, obj, *args):
        key = (self.func, args)
        if key in obj.cache:
            return obj.cache[key]
        else:
            obj.cache[key] = self.func(obj, *args)
            return obj.cache[key]