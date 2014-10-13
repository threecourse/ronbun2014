# coding=SJIS

from Model.BaseModel import BaseModel
from Utility.memoize import memoized
from Rate.TermRate import TermRate

class TermModel(BaseModel):
    u"""
    定期保険のプロジェクションモデルを表すクラス － 終身保険と同じ
    """    

    # レート
    @memoized
    def Rate(s):
        return TermRate(s.asm, s.x, s.n, s.m, s.sex)
    
    # 死亡率・解約率・選択効果などの配列
    @memoized
    def qx_list(s):
        if (s.sex == "M") : 
            return s.asm.get_float_list("qx_m_SLT1996")
        else:
            return s.asm.get_float_list("qx_f_SLT1996")

    @memoized
    def qwx_list(s):
        return s.asm.get_float_list("LapseRate")
    
    @memoized
    def SelectionFactor_list(s):
        return s.asm.get_float_list("SelectionFactor")
    
    # 事業費・コミッション・運用利回りの前提
    @memoized
    def Expense_AcqN(s):
        return s.asm.get_float_value("Expense_AcqN")
        
    @memoized
    def Expense_AcqS(s):
        return s.asm.get_float_value("Expense_AcqS")

    @memoized
    def Expense_AcqP(s):
        return s.asm.get_float_value("Expense_AcqP")

    @memoized
    def Expense_MaintpayingS(s):
        return s.asm.get_float_value("Expense_MaintpayingS")
        
    @memoized
    def Expense_MaintpayingN(s):
        return s.asm.get_float_value("Expense_MaintpayingN")

    @memoized
    def Expense_MaintpaidupS(s):
        return s.asm.get_float_value("Expense_MaintpaidupS")

    @memoized
    def Expense_MaintpaidupN(s):
        return s.asm.get_float_value("Expense_MaintpaidupN")

    @memoized
    def Expense_MaintP(s):
        return s.asm.get_float_value("Expense_MaintP")
    
    @memoized
    def CommRatio(s, t):
        return 0.0
    
    # 保険金額・コミッション率
    @memoized
    def DeathBen(s, t):
        if (t == 0 or t > s.n) : return 0.0
        return 1.0;

    @memoized
    def SurrenderBen(s, t):
        if (t == 0 or t > s.n) : return 0.0
        return s.Rate().CV_Rate(t);
    
    @memoized
    def PartialEndowBen(s, t):
        return 0.0
    
    @memoized
    def EndowBen(s, t):
        return 0.0



