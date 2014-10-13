# coding=SJIS

u"""
 Input用クラス
"""

class Assumption(object):
    def __init__(self, filename):
        f = open(filename)
        lines = [line.rstrip().split(",") for line in f.readlines()]
        f.close()
        
        self.Values = {}
        for line in lines:
            self.Values[line[0]] = line[1:]
    def get_float_list(self, name):
        return map(float, self.Values[name])
    def get_float_value(self, name):
        return float(self.Values[name][0])

