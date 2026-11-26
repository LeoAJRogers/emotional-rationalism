"""Code licence: MIT. Oracle (ratio-of-expectations) T1_j for the R-006b worlds on the bench grid.
Complete data, oracle centering, fixed scale; Gaussian; Wick enumeration over all ordered
disjoint lag-1 pair-pairs. Time axis tau = 16*day + beep (bench overnight gap 7), phi = 0.55."""
import numpy as np
from itertools import product
phi = 0.55
a = np.array([0.70, 0.70, 0.65]); b0 = np.array([0.30, 0.0, -0.30])
pairs = [((d, bb + 1), (d, bb)) for d in range(6) for bb in range(9)]
tau = lambda s: 16 * s[0] + s[1]
r = lambda s, t: phi ** abs(tau(s) - tau(t))
# precompute, for every ordered disjoint pair-pair, the 3 contraction weights
W1 = W2 = W3 = 0.0
rows = []
for pi, pj in product(pairs, repeat=2):
    if len({*pi, *pj}) < 4:
        continue
    (t, tp), (u, up) = pi, pj
    rows.append((r(t, tp) * r(u, up), r(t, u) * r(tp, up), r(t, up) * r(tp, u)))
R = np.array(rows)  # (n,3)
n = len(R)
def EU(M, e, f):
    """mean over pair-pairs of E[P_pi[e] P_pj[f]] (symmetrized products), Wick."""
    (j, l), (k, m) = e, f
    tot = 0.0
    for (p, q) in ((j, l), (l, j)):
        for (s_, v) in ((k, m), (m, k)):
            # x_p,t x_q,t' x_s,u x_v,u'
            tot += (M[p, q] * M[s_, v] * R[:, 0] + M[p, s_] * M[q, v] * R[:, 1] + M[p, v] * M[q, s_] * R[:, 2]).mean()
    return tot / 4
def T1j(Ms, wts):
    out = []
    for j in range(3):
        k, l = [x for x in range(3) if x != j]
        g = sum(w * (EU(M, (j, j), (k, l)) - EU(M, (j, k), (j, l))) for M, w in zip(Ms, wts))
        q = sum(w * EU(M, (j, k), (j, l)) for M, w in zip(Ms, wts))
        out.append((g, q, g / q))
    return out
print("pair-pairs", n)
classes = [np.outer(a, a) + np.outer(np.roll(b0, c), np.roll(b0, c)) for c in range(3)]
wts = [43, 42, 42]
res = T1j(classes, wts)
print("W2h oracle T1_j:", [round(x[2], 4) for x in res], " overall T1:", round(sum(x[0] for x in res) / sum(x[1] for x in res), 4))
res_e = T1j([classes[0]], [1])
print("W2e oracle T1_j:", [round(x[2], 4) for x in res_e], " overall:", round(sum(x[0] for x in res_e) / sum(x[1] for x in res_e), 4))
for c, M in enumerate(classes):
    g = [M[j, j] * M[k, l] - M[j, k] * M[j, l] for j, (k, l) in zip(range(3), ((1, 2), (0, 2), (0, 1)))]
    print("class", c, "g(M) =", np.round(g, 5), "det =", f"{np.linalg.det(M):.1e}", "offprod>0:", M[0,1]*M[0,2]*M[1,2] > 0)
