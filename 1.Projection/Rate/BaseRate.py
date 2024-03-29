# coding=SJIS

from Utility.memoize import memoized, initialize_memoize
from Utility.Util import Util, Settings
from Utility.CommutationTable import CommutationTable

class BaseRate(object):
    u"""
    [gΜξκNX

    ±ΜNXπp³΅ΔAeΫ―νήΜ[gNXπμ¬·ιB
    """

    def __init__(s, asm, x, n, m, sex):
        initialize_memoize(s)

        s.asm = asm
        s.x = x
        s.n = n
        s.m = m
        s.sex = sex
    
    def CT(s, kiso):
        u"ξ"
        raise NotImplementedError

    # [g
    def GrossP_Rate(s):
        u"cΖΫ―Ώ¦"
        raise NotImplementedError

    def BaseP_Rate(s):
        u"ξΫ―Ώ¦"
        raise NotImplementedError

    def CV_Rate(s, t):
        u"πρΤίΰ¦"
        raise NotImplementedError

    def NetP_Rate(s, kiso):
        u"Ϋ―Ώ¦"
        raise NotImplementedError

    def NetV_Rate(s, t, kiso):
        u"NetV¦"
        raise NotImplementedError

    def ZillV_Rate(s, t, kiso, z):
        u"`V¦"
        raise NotImplementedError
    
    # |[g
    def DumpReport(s):
        rep = []
        rep += s.CT(0).DumpReport()
        rep += s.CT(1).DumpReport()
        rep.append(Util.record_single("GrossP_Rate", s.GrossP_Rate()))
        rep.append(Util.record_single("BaseP_Rate", s.BaseP_Rate()))
        rep.append(Util.record_single("NetP_Rate_P", s.NetP_Rate(0)))
        rep.append(Util.record_single("NetP_Rate_V", s.NetP_Rate(1)))
        rep.append(Util.record("CV_Rate", s.CV_Rate))
        rep.append(Util.record("NetV_Rate_P", lambda t: s.NetV_Rate(t, 0)))
        rep.append(Util.record("NetV_Rate_V", lambda t: s.NetV_Rate(t, 1)))
        rep.append(Util.record("ZillV_Rate", lambda t: s.ZillV_Rate(t, 1, 99)))
        return rep
