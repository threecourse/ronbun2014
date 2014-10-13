# coding=SJIS

u"""
�C���X�^���X���\�b�h�̃������p���W���[��

�C���X�^���X���\�b�h�ɗ��p�ł��郁�������[�N�̋N����Ȃ�Memoize����
�i�C���X�^���X���\�b�h�ɂ̂ݎg�p�\�j
�ʏ��Memoize�̎����ł́A�����C���X�^���X�𐶐������ۂɃ��������[�N���N���Ă��܂����Ƃɒ��ӁB

�ȉ����Q�l�B���̎����͂��x�����߁A�C�����Ă���B
http://code.activestate.com/recipes/577452-a-memoize-decorator-for-instance-methods/
"""

import collections
import functools

def initialize_memoize(self):
    u"""
    �N���X���������Ή��ɂ��郁�\�b�h
    �����������C���X�^���X���\�b�h�����N���X�̃R���X�g���N�^�ł�����s�����Ƃ��K�v
    """

    self.cache = {}

class memoized(object):
    u"�C���X�^���X���\�b�h�̃��������s���f�R���[�^"

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