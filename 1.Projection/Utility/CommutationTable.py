# coding=SJIS

from Utility.memoize import memoized, initialize_memoize
from Utility.Util import Util, Settings

class CommutationTable(object):
    u"""
    ��N���X
    """

    def __init__(s, CIR, _qx):
        initialize_memoize(s)

        s.CIR = CIR
        s._qx = _qx
        s.max_x = len(_qx) - 1

    # �����\�E������
    def qx(s, x):
        return s._qx[x]

    @memoized
    def lx(s, x):
        if(x == 0):
            return 1.0
        return s.lx(x - 1) - s.d_x(x - 1)
    
    @memoized
    def d_x(s, x):
        return s.lx(x) * s.qx(x)

    def v(s):
        return 1.0 / (1.0 + s.CIR)

    # �
    @memoized
    def Dx(s, x):
        return s.lx(x) * (s.v() ** x)
    
    @memoized
    def Cx(s, x):
        return s.d_x(x) * (s.v() ** (x + 0.5))
    
    @memoized
    def Nx(s, x):
        if (x > s.max_x) : return 0.0
        if (x == s.max_x) : return s.Dx(x)
        return s.Dx(x) + s.Nx(x + 1);
    
    @memoized
    def Mx(s, x):
        if (x > s.max_x) : return 0.0
        if (x == s.max_x) : return s.Cx(x)
        return s.Cx(x) + s.Mx(x + 1);
    
    # �N������
    @memoized
    def Annuity_x(s, x):
        u"x�ΊJ�n, �I�g"
        if (s.Dx(x) <= 0) : return 0.0
        return s.Nx(x) / s.Dx(x)
    
    @memoized
    def Annuity_x_k(s, x, n, k):
        u"x�ΊJ�n, �I�g, �Nk��x��"        
        if (s.Dx(x) <= 0 or n < 0) : return 0.0
        return s.Annuity_x(x) - (k - 1.0)/(2.0 * k)

    @memoized
    def Annuity_xn(s, x, n):
        u"x�ΊJ�n, n�N"        
        if (s.Dx(x) <= 0 or n < 0) : return 0.0
        return (s.Nx(x) - s.Nx(x + n)) / s.Dx(x);

    @memoized
    def Annuity_xn_k(s, x, n, k):
        u"x�ΊJ�n, n�N, �Nk��x��"
        if (s.Dx(x) <= 0 or n < 0) : return 0.0
        return s.Annuity_xn(x,n) - (k - 1.0)/(2.0 * k) * (1.0 - s.Dx(x + n) / s.Dx(x))

    # ���|�[�g
    def DumpReport(s):
        rep = []
        rep.append(Util.record("Dx", s.Dx))
        rep.append(Util.record("Cx", s.Cx))
        rep.append(Util.record("Nx", s.Nx))
        rep.append(Util.record("Mx", s.Mx))
        return rep

