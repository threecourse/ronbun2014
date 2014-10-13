# coding=SJIS

from Rate.BaseRate import BaseRate
from Utility.memoize import memoized
from Utility.Util import Util, Settings
from Utility.CommutationTable import CommutationTable

class TermRate(BaseRate):
    u"""
    定期保険のレートを表すクラス - 終身保険と同じ
    """    

    @memoized
    def CT(s, kiso):
        if (kiso == 0):
            CIR = s.asm.get_float_value("CIR_P")
        else:
            CIR = s.asm.get_float_value("CIR_V")
        return CommutationTable(CIR, s.qx())

    # 予定発生率
    @memoized   
    def qx(s):
        if (s.sex == "M") : 
            return s.asm.get_float_list("qx_m_SLT1996")
        else:
            return s.asm.get_float_list("qx_f_SLT1996")

    # 予定事業費
    @memoized
    def Gamma(s):
        return 0.0
    
    @memoized
    def Alpha(s):
        return 0.015

    @memoized
    def Beta(s):
        return 0.1

    @memoized
    def ZillAlpha(s):
        return s.Alpha()

    # レート
    @memoized
    def GrossP_Rate(s):
        return s.BaseP_Rate() *12

    @memoized
    def BaseP_Rate(s):
        # monthly rate
        kiso = 0
        numer = ( (s.CT(kiso).Mx(s.x) - s.CT(kiso).Mx(s.x + s.n)) / s.CT(kiso).Dx(s.x) 
                 + s.Alpha() 
                 + s.CT(kiso).Annuity_xn(s.x, s.n) * s.Gamma()
                )
        denom = (1 - s.Beta()) * s.CT(kiso).Annuity_xn_k(s.x, s.m,12) * 12
        return numer / denom

    @memoized
    def CV_Rate(s, t):
        kiso = 0;
        if (t < 10) : return max(s.NetV_Rate(t, kiso) - s.ZillAlpha() * (10.0 - t) / 10.0, 0.0)
        return s.NetV_Rate(t, kiso);

    @memoized
    def NetP_Rate(s, kiso):
        numer = ((s.CT(kiso).Mx(s.x) - s.CT(kiso).Mx(s.x + s.n)) / s.CT(kiso).Dx(s.x) 
                + s.CT(kiso).Annuity_xn(s.x, s.n) * s.Gamma()
                )
        denom = s.CT(kiso).Annuity_xn(s.x, s.m);
        return numer / denom;

    @memoized
    def NetV_Rate(s, t, kiso):
        if (t > s.n) : return 0.0
        if (s.CT(kiso).Dx(s.x + t) <= 0.0) : return 0.0
        return ( (s.CT(kiso).Mx(s.x + t) - s.CT(kiso).Mx(s.x + s.n)) / s.CT(kiso).Dx(s.x + t) 
                 + s.CT(kiso).Annuity_xn(s.x + t, s.n - t) * s.Gamma() 
                 - s.CT(kiso).Annuity_xn(s.x + t, s.m - t) * s.NetP_Rate(kiso)
                )
    @memoized
    def ZillV_Rate(s, t, kiso, z):
        zm = min(s.m, z);
        if (t < zm): 
            return (  s.NetV_Rate(t, kiso) 
                     - s.ZillAlpha() * s.CT(kiso).Annuity_xn(s.x + t, zm - t) 
                         / s.CT(kiso).Annuity_xn(s.x, zm)
                    )
        return s.NetV_Rate(t, kiso);

