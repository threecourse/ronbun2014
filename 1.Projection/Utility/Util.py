# coding=SJIS

u"""
���[�e�B���e�B���W���[��
"""
import string 

class Settings(object):
    u"�ݒ荀�ڂ�ێ�����N���X"
    Max_t = 100

class Util(object):
    u"���[�e�B���e�B�N���X"

    @classmethod
    def record(cls, header, source, format  = "%12.6f"):
        u"�w�b�_����ъ֐��it�������ɂƂ���́j�̌v�Z���ʂ𕶎���ɂ���"
        return header + "," + string.join([format % source(t) for t in range(0, Settings.Max_t + 1)], ",")

    @classmethod
    def record_single(cls, header, value, format = "%12.6f"):
        u"�w�b�_����ђl�𕶎���ɂ���"
        return header + "," + format % value

    @classmethod
    def at(cls, seq, idx_plus_1):
        u"""
        �z�񂩂�l���擾����B�����ŁA�Y�����z��͈̔͂𒴂��Ă���ꍇ�͍Ō�̗v�f�̒l���擾����B
        ��P�ی��N�x��idx=0�Ƃ��邽�߁A�����͓Y���{�P�Ƃ���B
        """
        idx = idx_plus_1 - 1
        if idx < 0 :
            return 0.0
        if idx < len(seq):
            return seq[idx]
        else:
            return seq[-1]