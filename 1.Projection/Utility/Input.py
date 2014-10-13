# coding=SJIS

u"""
インプット用クラスのモジュール
"""

class Assumption(object):
    u"""
    アサンプションクラス
    """

    def __init__(self, filename):
        u"ファイルからアサンプションを作成する"
        f = open(filename)
        lines = [line.rstrip().split(",") for line in f.readlines()]
        f.close()
        
        self.Values = {}
        for line in lines:
            self.Values[line[0]] = line[1:]

    #--- キーにより各型で値や配列を取得する
    def get_float_list(self, name):
        return map(float, self.Values[name])

    def get_float_value(self, name):
        return float(self.Values[name][0])

class Cell(object):
    u"""
    プライシングセルを表すクラス
    """
    
    @classmethod
    def LoadCells(self, filename):
        u"ファイルからセルの配列を作成する"
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

    #--- キーにより各型で値を取得する
    def get_str(self, name):
        return str(self.Values[name])
    def get_float(self, name):
        return float(self.Values[name])
    def get_int(self, name):
        return int(self.Values[name])
    def get_bool(self, name):
        return bool(self.Values[name])
