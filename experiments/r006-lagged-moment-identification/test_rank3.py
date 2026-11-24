"""Unit tests for rank3.py (R-006b). Run: python test_rank3.py (exits non-zero on failure)."""
import itertools
import sys

import numpy as np

import lagmom as lm
import rank3

FAIL = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  {detail}" if detail else ""))
    if not ok:
        FAIL.append(name)


def test_distinct3():
    rng = np.random.default_rng(1)
    a, b, c = rng.standard_normal((3, 4, 6))
    brute = np.zeros(4)
    for i, j, k in itertools.permutations(range(6), 3):
        brute += a[:, i] * b[:, j] * c[:, k]
    err = np.max(np.abs(rank3.distinct3(a, b, c) - brute))
    check("distinct3 equals brute-force ordered distinct-triple sum", err < 1e-12, f"max err {err:.1e}")


def test_det_coefficients():
    """If every day has the same mean lag-1 pair product C[e], U = C[e1]C[e2]C[e3] exactly,
    so det_m must equal det(C) and off_m must equal C01 C02 C12 (jackknife off)."""
    rng = np.random.default_rng(2)
    A = rng.standard_normal((3, 3))
    C = A @ A.T                                              # symmetric "lag-1 moment" matrix
    pairs, eidx = lm.elem_index(3)

    class Fake:
        pass
    LM = Fake()
    LM.eidx = eidx
    D, M = 6, 2
    n_d = np.array([3, 5, 4, 6, 2, 7], float)
    S = np.zeros((1, M, D, len(pairs)))
    for e, (j, l) in enumerate(pairs):
        S[0, :, :, e] = n_d * C[j, l]
    LM.Sd = {1: S}
    LM.Nd = {1: np.broadcast_to(n_d, (1, M, D)).copy()}
    LM.jackknife = lambda est: est[0]
    det, off = rank3.det_and_off(LM)
    e1 = np.max(np.abs(det - np.linalg.det(C)))
    e2 = np.max(np.abs(off - C[0, 1] * C[0, 2] * C[1, 2]))
    check("det combination reproduces det(C)", e1 < 1e-10, f"err {e1:.1e}")
    check("off term reproduces C01*C02*C12", e2 < 1e-10, f"err {e2:.1e}")


def test_rank2_det_zero_and_f1r_closed_form():
    """[MATH] Rank-2 lag-1 matrices have det 0; F1+R gives det/offprod = e3(t) + e2(t)."""
    rng = np.random.default_rng(3)
    worst = 0.0
    for _ in range(2000):
        a, b = rng.standard_normal((2, 3))
        worst = max(worst, abs(np.linalg.det(np.outer(a, a) + np.outer(b, b))))
    check("det(aa' + bb') = 0 (2000 draws)", worst < 1e-12, f"max |det| {worst:.1e}")
    worst = 0.0
    for _ in range(2000):
        c = rng.uniform(0.2, 1.0, 3)
        t = rng.uniform(0.0, 0.5, 3)
        M = np.outer(c, c) + np.diag(t * c ** 2)
        lhs = np.linalg.det(M) / (M[0, 1] * M[0, 2] * M[1, 2])
        rhs = t.prod() + t[0] * t[1] + t[0] * t[2] + t[1] * t[2]
        worst = max(worst, abs(lhs - rhs))
    check("F1+R: det/offprod = e3(t) + e2(t) (2000 draws)", worst < 1e-10, f"max err {worst:.1e}")


def test_on_lagmoments():
    """rank3 on a real LagMoments object: the full-data U equals a brute-force triple loop."""
    rng = np.random.default_rng(4)
    Y = rng.standard_normal((3, 6, 10, 3))
    Y[rng.random((3, 6, 10)) < 0.25] = np.nan
    LM = lm.LagMoments(Y, (0, 1, 2), discrete=False, lags=(1,), jk=True)
    el = ((0, 1), (0, 2), (1, 2))
    u = rank3.ustat3(LM, el)[0]
    P = LM.P[1]                                               # (V,M,D,B,E)
    V1 = LM.Vk[1]
    for m in range(3):
        num, den = 0.0, 0.0
        for d1, d2, d3 in itertools.permutations(range(6), 3):
            s = [P[0, m, d][:, LM.eidx[e]].sum() for d, e in zip((d1, d2, d3), el)]
            n = [V1[0, m, d].sum() for d in (d1, d2, d3)]
            num += s[0] * s[1] * s[2]
            den += n[0] * n[1] * n[2]
        check(f"ustat3 matches brute force, person-period {m}", abs(u[m] - num / den) < 1e-12)


if __name__ == "__main__":
    test_distinct3()
    test_det_coefficients()
    test_rank2_det_zero_and_f1r_closed_form()
    test_on_lagmoments()
    print("ALL PASS" if not FAIL else f"{len(FAIL)} FAILED: {FAIL}")
    sys.exit(1 if FAIL else 0)
