# coding=SJIS

u"""
�C���v�b�g�p�N���X�̃��W���[��
"""

class Assumption(object):
    u"""
    �A�T���v�V�����N���X
    """

    def __init__(self, filename):
        u"�t�@�C������A�T���v�V�������쐬����"
        f = open(filename)
        lines = [line.rstrip().split(",") for line in f.readlines()]
        f.close()
        
        self.Values = {}
        for line in lines:
            self.Values[line[0]] = line[1:]

    #--- �L�[�ɂ��e�^�Œl��z����擾����
    def get_float_list(self, name):
        return map(float, self.Values[name])

    def get_float_value(self, name):
        return float(self.Values[name][0])

class Cell(object):
    u"""
    �v���C�V���O�Z����\���N���X
    """
    
    @classmethod
    def LoadCells(self, filename):
        u"�t�@�C������Z���̔z����쐬����"
        f = open(filename)
        lines = [line.rstrip().split(",") for line in f.readlines()]
        f.close()

        Cells = []        
        header = lines[0]
        for line in lines[1:]:
            dict = {}
            for i in range(0, len(header)):
               dict[header[i]] = line[i]
            Cells.append(Cell(dict))
        return Cells

    def __init__(self, dict):
        self.Values = dict

    #--- �L�[�ɂ��e�^�Œl���擾����
    def get_str(self, name):
        return str(self.Values[name])
    def get_float(self, name):
        return float(self.Values[name])
    def get_int(self, name):
        return int(self.Values[name])
    def get_bool(self, name):
        return bool(self.Values[name])
