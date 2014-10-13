# coding=SJIS

from Utility.memoize import memoized, initialize_memoize
from Utility.Util import Util, Settings
import math
import string

class BaseModel(object):
    u"""
    プロジェクションモデルの基底クラス

    このクラスを継承して、各保険種類のモデルを作成する。
    """

    def __init__(s, cell, asm):
       initialize_memoize(s)

       s.cell = cell
       s.asm = asm

       s.PLAN = s.cell.get_str("PLAN")
       s.x = s.cell.get_int("x")
       s.n = s.cell.get_int("n")
       s.m = s.cell.get_int("m")
       s.sex = s.cell.get_str("sex")
       s.S = s.cell.get_float("S")
   
    # レート
    def Rate(s):
        raise NotImplementedError

    # 死亡率・解約率・選択効果などの配列
    def qx_list(s):
        raise NotImplementedError
    def qwx_list(s):
        raise NotImplementedError
    def SelectionFactor_list(s):
        raise NotImplementedError

    # 事業費・コミッション・運用利回りの前提
    def Expense_AcqN(s):
        raise NotImplementedError
    def Expense_AcqS(s):
        raise NotImplementedError
    def Expense_AcqP(s):
        raise NotImplementedError
    def Expense_MaintpayingS(s):
        raise NotImplementedError
    def Expense_MaintpaidupS(s):
        raise NotImplementedError
    def Expense_MaintpayingN(s):
        raise NotImplementedError
    def Expense_MaintpaidupN(s):
        raise NotImplementedError
    def Expense_MaintP(s):
        raise NotImplementedError

    @memoized
    def InvestmentYield(s):
        return s.asm.get_float_list("InvYield")

    # 生命表
    @memoized
    def qx(s,t):
        if (t == 0 | t > s.n) : return 0.0;
        return Util.at(s.qx_list(), s.x + t) * Util.at(s.SelectionFactor_list(), t)

    @memoized
    def qwx(s,t):
        if (t == 0 | t > s.n) : return 0.0
        return Util.at(s.qwx_list(), t) 

    @memoized
    def lxBOY(s, t):
        if (t == 0) : return 0.0;
        if (t == 1) : return 1.0;
        return s.lxEOYaftMat(t - 1);
    
    @memoized
    def lxMOY(s,t):
        return (s.lxBOY(t) + s.lxEOY(t)) / 2.0
    
    @memoized
    def lxPay(s, t):
        if (t <= s.m) : return s.lxBOY(t);  # 年払を想定 
        return 0.0;
    
    @memoized
    def lxEOY(s, t):
        return max(s.lxBOY(t) - s.d_x(t) - s.dwx(t), 0.0);
    
    @memoized
    def lxEOYaftMat(s, t):
        if (t >= s.n) : return 0.0
        return s.lxEOY(t);
    
    @memoized
    def d_x(s, t):
        if (t == 0) : return 0.0   
        return s.lxBOY(t) * s.qx(t) * (1.0 - s.qwx(t) / 2.0);
    
    @memoized
    def dwx(s, t):
        if (t == 0) : return 0.0   
        return s.lxBOY(t) * s.qwx(t) * (1.0 - s.qx(t) / 2.0);    
    
    # 保険金額・コミッション率
    def DeathBen(s,t):
        raise NotImplementedError
    def SurrenderBen(s,t):
        raise NotImplementedError
    def PartialEndowBen(s, t):
        raise NotImplementedError
    def EndowBen(s, t):
        raise NotImplementedError
    def CommRatio(s, t):
        raise NotImplementedError

    # 使用するレート
    @memoized    
    def ReserveRate(s, t):
        return s.Rate().NetV_Rate(t, 1)
    
    @memoized
    def CashValueRate(s, t):
        return s.Rate().CV_Rate(t)
    
    @memoized
    def AZilVRate(s, t):
        return s.Rate().ZillV_Rate(t, 1, 99)
    
    # CF項目
    @memoized
    def PremiumIncome(s, t):
        if (t == 0 or t > s.m) : return 0.0
        return s.lxPay(t) * s.Rate().GrossP_Rate() * s.S
    
    @memoized
    def DeathBenefit(s, t):
        return s.d_x(t) * s.S * s.DeathBen(t)

    @memoized
    def SurrenderBenefit(s, t):
        return s.dwx(t) * s.S * s.SurrenderBen(t)
    
    @memoized
    def PartialEndowBenefit(s, t):
        return s.lxBOY(t) * s.S * s.PartialEndowBen(t)
    
    @memoized
    def EndowBenefit(s, t):
        return s.lxEOY(t) * s.S * s.EndowBen(t)
    
    @memoized
    def InitExpense(s, t):
        if (t == 0 or t > s.n) : return 0.0
        if (t > 1) : 
            expense_acqS = 0.0
            expense_acqN = 0.0
        else:
            expense_acqS = s.Expense_AcqS()
            expense_acqN = s.Expense_AcqN()
        return ( s.lxBOY(t) * s.S * expense_acqS
                + s.lxBOY(t) * expense_acqN
                + s.PremiumIncome(t) * s.Expense_AcqP())
    
    @memoized
    def MaintExpense(s, t):
        if (t == 0 or t > s.n) : return 0.0
        if (t > s.m) :
            expense_maintS = s.Expense_MaintpaidupS()
            expense_maintN = s.Expense_MaintpaidupN()            
        else :
            expense_maintS = s.Expense_MaintpayingS()
            expense_maintN = s.Expense_MaintpayingN()
        return ( s.lxMOY(t) * s.S * expense_maintS 
                + s.lxMOY(t) * expense_maintN 
                + s.PremiumIncome(t) * s.Expense_MaintP())

    @memoized
    def Commission(s, t):
        return s.PremiumIncome(t) * s.CommRatio(t)

    @memoized
    def InvestmentIncome(s, t):
        return s.InvestmentAsset(t) * Util.at(s.InvestmentYield(), t)

    @memoized
    def ReserveIncrease(s, t):
        if (t == 0) : return 0.0
        return s.Reserve(t) - s.Reserve(t - 1)
    
    @memoized
    def ProfitBeforeTax(s, t):
        return ( s.PremiumIncome(t) 
               + s.InvestmentIncome(t) 
               - ( s.DeathBenefit(t) + s.SurrenderBenefit(t) + s.PartialEndowBenefit(t) 
                 + s.EndowBenefit(t) + s.InitExpense(t) + s.MaintExpense(t) + s.Commission(t) ) 
               - s.ReserveIncrease(t)
               )
    

    # ストック項目等
    @memoized
    def Reserve(s, t):
        return s.lxEOYaftMat(t) * s.ReserveRate(t) * s.S

    @memoized    
    def CashValueEndT(s, t):
        return s.lxEOYaftMat(t) * s.CashValueRate(t) * s.S
    
    @memoized
    def AzilVEndT(s, t):
        return s.lxEOYaftMat(t) * s.AZilVRate(t) * s.S
    
    @memoized
    def InvestmentAsset(s, t):
        if (t == 0) : return 0.0;

        # 年払を想定 
        return ( s.Reserve(t - 1) 
               + s.PremiumIncome(t) 
               - (s.InitExpense(t) + s.Commission(t))
               - (s.DeathBenefit(t) + s.SurrenderBenefit(t) + s.PartialEndowBenefit(t) 
               + s.EndowBenefit(t) + s.MaintExpense(t) ) / 2.0
               )

    @memoized
    def PVProfitBeforeTax(s, t):
        return s.PVCalc(t, s.ProfitBeforeTax, s.PVProfitBeforeTax, "End")
    
    @memoized
    def PVPremium(s, t):
        return s.PVCalc(t, s.PremiumIncome, s.PVPremium, "Begin")

    @memoized
    def DiscountFactor(s,t):
        if (t == 0) : return 1.0
        return s.DiscountFactor(t - 1) / (1 + Util.at(s.InvestmentYield(),t));
    
    @memoized
    def ProfitMargin(s):
        return s.PVProfitBeforeTax(0) / s.PVPremium(0)
    
    # ユーティリティ変数
    def PVCalc(s, t, func_cf, func_pv, timing):
        disc = s.DiscountFactor(t + 1) / s.DiscountFactor(t)
        
        if timing == "Begin":
           disc_term = 0.0
        elif timing == "Mid":
           disc_term = 0.5
        elif timing == "End":
           disc_term = 1.0
        else : 
           raise Exception("timing is invalid")

        if (t >= Settings.Max_t) : return 0.0
        return func_cf(t + 1) * math.pow(disc, disc_term) + func_pv(t + 1) * disc        
        
    # 分析用項目
    @memoized
    def PVDeathBenefit(s, t):
        return s.PVCalc(t, s.DeathBenefit, s.PVDeathBenefit, "Mid")

    @memoized
    def PVSurrenderBenefit(s, t):
        return s.PVCalc(t, s.SurrenderBenefit, s.PVSurrenderBenefit, "Mid")

    @memoized
    def PVPartialEndowBenefit(s, t):
        return s.PVCalc(t, s.PartialEndowBenefit, s.PVPartialEndowBenefit, "Mid")

    @memoized
    def PVEndowBenefit(s, t):
        return s.PVCalc(t, s.EndowBenefit, s.PVEndowBenefit, "Mid")

    @memoized
    def PVInitExpense(s, t):
        return s.PVCalc(t, s.InitExpense, s.PVInitExpense, "Begin")

    @memoized
    def PVMaintExpense(s, t):
        return s.PVCalc(t, s.MaintExpense, s.PVMaintExpense, "Mid")

    @memoized
    def PVCommission(s, t):
        return s.PVCalc(t, s.Commission, s.PVCommission, "Begin")

    def PM_DeathBenefit(s) : return s.PVDeathBenefit(0) / s.PVPremium(0)
    def PM_SurrenderBenefit(s) : return s.PVSurrenderBenefit(0) / s.PVPremium(0)
    def PM_PartialEndowBenefit(s) : return s.PVPartialEndowBenefit(0) / s.PVPremium(0)
    def PM_EndowBenefit(s) : return s.PVEndowBenefit(0) / s.PVPremium(0)
    def PM_InitExpense(s) : return s.PVInitExpense(0) / s.PVPremium(0)
    def PM_MaintExpense(s) : return s.PVMaintExpense(0) / s.PVPremium(0)
    def PM_Commission(s): return s.PVCommission(0) / s.PVPremium(0)

    # レポート
    def DumpReport(s):
        u"デバッグ用のレポート"

        rep = []
        rep += s.Rate().DumpReport()
        rep.append(Util.record_single("PLAN", s.PLAN, "%s"))
        rep.append(Util.record_single("x", s.x, "%d"))
        rep.append(Util.record_single("n", s.n, "%d"))
        rep.append(Util.record_single("m", s.m, "%d"))
        rep.append(Util.record_single("sex", s.sex, "%s"))
        rep.append(Util.record_single("S", s.S))
        rep.append(Util.record("t", lambda t: t, "%12d"))
        rep.append(Util.record("lxBOY", s.lxBOY))
        rep.append(Util.record("lxMOY", s.lxMOY))
        rep.append(Util.record("lxPay", s.lxPay))
        rep.append(Util.record("lxEOY", s.lxEOY))
        rep.append(Util.record("lxEOYaftMat", s.lxEOYaftMat))
        rep.append(Util.record("d_x", s.d_x))
        rep.append(Util.record("dwx", s.dwx))
        rep.append(Util.record("PremiumIncome", s.PremiumIncome, "%12d"))
        rep.append(Util.record("DeathBenefit", s.DeathBenefit, "%12d"))
        rep.append(Util.record("SurrenderBenefit", s.SurrenderBenefit, "%12d"))
        rep.append(Util.record("PartialEndowBenefit", s.PartialEndowBenefit, "%12d"))
        rep.append(Util.record("EndowBenefit", s.EndowBenefit, "%12d"))
        rep.append(Util.record("InitExpense", s.InitExpense, "%12d"))
        rep.append(Util.record("MaintExpense", s.MaintExpense, "%12d"))
        rep.append(Util.record("Commission", s.Commission, "%12d"))
        rep.append(Util.record("InvestmentIncome", s.InvestmentIncome, "%12d"))
        rep.append(Util.record("ReserveIncrease", s.ReserveIncrease, "%12d"))
        rep.append(Util.record("ProfitBeforeTax", s.ProfitBeforeTax, "%12d"))
        rep.append(Util.record("Reserve", s.Reserve, "%12d"))
        rep.append(Util.record("PVProfitBeforeTax", s.PVProfitBeforeTax, "%12d"))
        rep.append(Util.record("PVPremium", s.PVPremium, "%12d"))
        rep.append(Util.record("DiscountFactor", s.DiscountFactor))
        rep.append(Util.record_single("ProfitMargin", s.ProfitMargin()))
        #rep.append(Util.record("qx_t",lambda t: Util.at(s.qx_list(), s.x + t)))
        #rep.append(Util.record("SelectionFactor_t",lambda t: Util.at(s.SelectionFactor_list(), t)))
        return rep

    def ResultReportHeader(s):
        u"結果出力用のレポートヘッダ"
        values = [  "ProfitMargin",
                    "PVProfitBeforeTax", "PVPremium",
                    "PM_DeathBenefit",
                    "PM_SurrenderBenefit ",
                    "PM_PartialEndowBenefit ",
                    "PM_EndowBenefit ",
                    "PM_InitExpense ",
                    "PM_MaintExpense ",
                    "PM_Commission " ]
        
        return string.join(values, ",")

    def ResultReportValues(s):
        u"結果出力用のレポートの値"
        
        values = [  s.ProfitMargin(),
                    s.PVProfitBeforeTax(0), s.PVPremium(0),
                    s.PM_DeathBenefit(),
                    s.PM_SurrenderBenefit (),
                    s.PM_PartialEndowBenefit (),
                    s.PM_EndowBenefit (),
                    s.PM_InitExpense (),
                    s.PM_MaintExpense (),
                    s.PM_Commission () ]
        
        return string.join(["%12f" % val for val in values],",")