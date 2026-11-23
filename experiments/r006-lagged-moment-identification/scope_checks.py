"""E3a scope checks for amendment R-006a (GPT-6 request 1 on ER PR #13). Claude, 2026-11-23. Seeded NumPy. Code licence: MIT.
Item excess g_j(M) = M_jj M_kl - M_jk M_jl for a symmetric 3x3 lag-1 matrix M."""
import numpy as np
rng = np.random.default_rng(61123)
def excess(M):
    g = []
    for j, (k, l) in zip(range(3), [(1, 2), (0, 2), (0, 1)]):
        g.append(M[j, j] * M[k, l] - M[j, k] * M[j, l])
    return np.array(g)
def minors(a, b):
    x = lambda i, j: a[i] * b[j] - a[j] * b[i]
    return x(0, 1), x(0, 2), x(1, 2)
N = 20000; allpos = {"+": 0, "-": 0}; err = 0.0
for _ in range(N):
    a, b = rng.normal(size=3), rng.normal(size=3)
    xWF, xWS, xFS = minors(a, b)
    for s in ["+", "-"]:
        M = np.outer(a, a) + (1 if s == "+" else -1) * np.outer(b, b)
        g = excess(M)
        pred = np.array([xWF * xWS, -xWF * xFS, xWS * xFS]) * (1 if s == "+" else -1)
        err = max(err, np.abs(g - pred).max())
        allpos[s] += bool(np.all(g > 0))
print(f"identity g_j = (+/-) x_jk x_jl holds to {err:.1e}")
print(f"all three excesses > 0: PSD a a'+b b': {allpos['+']}/{N}; indefinite a a'-b b': {allpos['-']}/{N}")
# Concrete two-factor model with a NEGATIVE-rate second factor: lag-1 = phi_f*l l' + phi_g*m m'
lam = np.array([0.70, 0.70, 0.65]); mu = np.array([0.30, 0.0, -0.30])
for phig in [0.55, -0.40]:
    C1 = 0.55 * np.outer(lam, lam) + phig * np.outer(mu, mu)
    C2 = 0.55**2 * np.outer(lam, lam) + phig**2 * np.outer(mu, mu)
    g = excess(C1)
    # exact F1+R representation of C1: c_j^2 = M_jk M_jl / M_kl, d_j = g_j / M_kl
    Mkl = np.array([C1[1, 2], C1[0, 2], C1[0, 1]])
    d = g / Mkl
    c = np.sqrt(np.array([C1[0,1]*C1[0,2]/C1[1,2], C1[0,1]*C1[1,2]/C1[0,2], C1[0,2]*C1[1,2]/C1[0,1]]))
    rec = np.outer(c, c) + np.diag(d)
    # T2-style decay minor between lags 1 and 2 for pairs (WF, WS): C1[a]C2[b] - C1[b]C2[a]
    minor = C1[0, 1] * C2[0, 2] - C1[0, 2] * C2[0, 1]
    print(f"phi_g={phig:+.2f}: excesses={np.round(g, 4)}, F1+R residual var d={np.round(d, 4)}, "
          f"F1+R reproduces lag-1 to {np.abs(rec - C1).max():.1e}, lag1-vs-lag2 minor={minor:+.4f}")

# Half-plane criterion for the indefinite case: all three excesses > 0  <=>  rows (a_i, b_i)
# do not lie in a common open half-plane through the origin.
def in_halfplane(a, b):
    ang = np.sort(np.arctan2(b, a)); gaps = np.diff(np.r_[ang, ang[0] + 2 * np.pi])
    return gaps.max() > np.pi
agree = 0; pos_constrained = 0
for _ in range(N):
    a, b = rng.normal(size=3), rng.normal(size=3)
    allp = bool(np.all(excess(np.outer(a, a) - np.outer(b, b)) > 0))
    agree += (allp == (not in_halfplane(a, b)))
    ap = np.abs(a)                                   # same-signed column (e.g. a common NA factor)
    pos_constrained += bool(np.all(excess(np.outer(ap, ap) - np.outer(b, b)) > 0))
print(f"indefinite: all-positive <=> rows not in a half-plane, agreement {agree}/{N}")
print(f"indefinite with a same-signed column: all-positive in {pos_constrained}/{N}")
