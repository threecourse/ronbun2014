# coding=SJIS

from Model.WLModel import WLModel
from Model.EndowModel import EndowModel
from Model.TermModel import TermModel

def CreateModel(cell, asm):
    u"�Z���E�A�T���v�V�����ɉ��������f�����쐬����B"
    
    key = cell.get_str("PLAN")
    if   key == "WL"   : return WLModel(cell, asm)
    elif key == "Endow": return EndowModel(cell, asm)
    elif key == "Term": return TermModel(cell, asm)
    else: raise Exception("invalid plan")