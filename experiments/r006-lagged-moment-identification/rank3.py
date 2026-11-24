"""R-006b: a within-person persistent-rank statistic for the NA triad. Code licence: MIT.

Claude Opus 5.5, 2026-11-24 (ER daily run). Definitions in DESIGN.md, appended note of 2026-11-24.

The per-item sign test (E3a) asks *which* item has a negative excess. Different people can
have different such items, and aggregation then hides them (GPT-6.2's counterexample on
ER PR #13). The determinant of the within-person lag-1 matrix is item-symmetric: it is
exactly 0 for every person whose lag-1 persistent matrix has rank <= 2 (F1; F2 at any rates;
F1 plus residual persistence on one item), whoever they are. A rank-3 matrix that is
positive semidefinite (F1+R with residuals on >= 2 items, F2+R, ...) has det > 0.

Cross-day triple U-statistic for elements (e1, e2, e3) of the lag-1 pair products:

    U_m(e1, e2, e3) = sum over ordered triples of distinct days (d1, d2, d3) of
                      S_d1[e1] S_d2[e2] S_d3[e3]  /  sum of N_d1 N_d2 N_d3

where S_d[e] is the sum of lag-1 pair products P_pi[e] on day d and N_d the number of
lag-1 pairs. If days are independent given the person's parameters and the lag-1 process
is stationary, E[U_m] is the product of the three lag-1 moments (no Gaussianity needed).

    det_m = U(00,11,22) + 2 U(01,02,12) - U(00,12,12) - U(11,02,02) - U(22,01,01)
    off_m = U(01,02,12)
    T_det = sum_m w_m det~_m / sum_m w_m off~_m      (tilde: day jackknife)

Under homogeneous F1+R, T_det = e3(t) + e2(t), where t_j = T1_j (population).
off_m > 0 is the positive-shared-lag precondition for reading T1_j >= 0 as F1+R.
"""
import numpy as np

import lagmom as lm

DET_TERMS = [(+1.0, ((0, 0), (1, 1), (2, 2))),
             (+2.0, ((0, 1), (0, 2), (1, 2))),
             (-1.0, ((0, 0), (1, 2), (1, 2))),
             (-1.0, ((1, 1), (0, 2), (0, 2))),
             (-1.0, ((2, 2), (0, 1), (0, 1)))]
OFF_TERM = ((0, 1), (0, 2), (1, 2))


def distinct3(a, b, c):
    """sum over ordered triples of distinct indices on the last axis of a_i b_j c_k."""
    A, B, C = a.sum(-1), b.sum(-1), c.sum(-1)
    ab, ac, bc = (a * b).sum(-1), (a * c).sum(-1), (b * c).sum(-1)
    return A * B * C - ab * C - ac * B - bc * A + 2.0 * (a * b * c).sum(-1)


def ustat3(LM, elems):
    """Cross-day triple U-statistic (V, M) for three elements (local item pairs), lag 1."""
    S = LM.Sd[1]                                        # (V,M,D,E)
    N = LM.Nd[1].astype(float)                          # (V,M,D)
    e = [LM.eidx[x] for x in elems]
    num = distinct3(S[..., e[0]], S[..., e[1]], S[..., e[2]])
    den = distinct3(N, N, N)
    with np.errstate(invalid="ignore", divide="ignore"):
        return num / den


def det_and_off(LM, cache=None):
    """Day-jackknifed per person-period det_m and off_m, shape (M,) each."""
    cache = {} if cache is None else cache

    def jk_u(elems):
        key = ("u3",) + tuple(sorted(elems))
        if key not in cache:
            cache[key] = LM.jackknife(ustat3(LM, tuple(sorted(elems))))
        return cache[key]

    det = sum(c * jk_u(el) for c, el in DET_TERMS)
    off = jk_u(OFF_TERM)
    return det, off


def t_det(LM, person, n_persons, counts, cache=None):
    """Point estimate and bootstrap draws for T_det and for the precondition OFF (mean off_m)."""
    det, off = det_and_off(LM, cache)
    w = LM.n_pairs1.astype(float)
    ok = LM.keep & np.isfinite(det) & np.isfinite(off) & (LM.n_days >= 3)
    pn = lm.person_sums(w * np.where(ok, det, 0.0), person, ok, n_persons)
    pd = lm.person_sums(w * np.where(ok, off, 0.0), person, ok, n_persons)
    pw = lm.person_sums(w, person, ok, n_persons)
    est = {"T_det": pn.sum() / pd.sum(), "OFF": pd.sum() / pw.sum()}
    with np.errstate(invalid="ignore", divide="ignore"):
        draws = {"T_det": (counts @ pn) / (counts @ pd), "OFF": (counts @ pd) / (counts @ pw)}
    return est, draws, int(ok.sum())
