from utility import *


def xx(self, line, n=None):
    if n is None:
        n = 32
    a1, b1, c1 = self.abc
    a2, b2, c2 = line.abc
    det = a1 * b2 - a2 * b1
    x = round((b2 * c1 - b1 * c2) / det, n)
    y = round((a1 * c2 - a2 * c1) / det, n)
    sx1, sy1 = map(lambda xc: round(xc, n), list(self.p1))
    sx2, sy2 = map(lambda xc: round(xc, n), list(self.p2))
    sx1, sx2 = map(lambda xc: round(xc, n), list(minmax(sx1, sx2)))
    sy1, sy2 = map(lambda xc: round(xc, n), list(minmax(sy1, sy2)))
    lx1, ly1 = map(lambda xc: round(xc, n), list(line.p1))
    lx2, ly2 = map(lambda xc: round(xc, n), list(line.p2))
    lx1, lx2 = map(lambda xc: round(xc, n), list(minmax(lx1, lx2)))
    ly1, ly2 = map(lambda xc: round(xc, n), list(minmax(ly1, ly2)))
    pa = self.collide_point(x, y)
    pb = line.collide_point(x, y)
    pc = sx1 <= x <= sx2
    pd = sy1 <= y <= sy2
    pe = lx1 <= x <= lx2
    pf = ly1 <= y <= ly2
    pt = all([pa, pb, pc, pd, pe, pf])
    return self, line, a1, b1, c1, a2, b2, c2, det, x, y, sx1, sy1, sx2, sy2, lx1, ly1, lx2, ly2, pa, pb, pc, pd, pe, pf, pt


l1 = Line(445.1505, 6.3226, 446.71901, -0.73557)
top = Line(0, 0, 750, 0)
ls, ll, a1, b1, c1, a2, b2, c2, det, x, y, sx1, sy1, sx2, sy2, lx1, ly1, lx2, ly2, pa, pb, pc, pd, pe, pf, pt = xx(l1, top, 0)
print(dict_print({
    "self": ls, "line": ll, "a1": a1, "b1": b1, "c1": c1, "a2": a2, "b2": b2, "c2": c2, "det": det, "x": x, "y": y, "sx1": sx1, "sy1": sy1,
    "sx2": sx2, "sy2": sy2, "lx1": lx1, "ly1": ly1, "lx2": lx2, "ly2": ly2, "pa": pa, "pb": pb, "pc": pc, "pd": pd,
    "pe": pe, "pf": pf, "pt": pt
}, "Values"))
