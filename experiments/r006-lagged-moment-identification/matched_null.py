"""Marginal-matched F1 null for R-006 Part B. Code licence: MIT.

Given an observed array Y (M, D, B, 5) on the 1..7 scale, simulate datasets in which
every person-period keeps its *observed missingness mask* and, item by item, its
*observed category distribution*, while the latent dynamics are F1 (one shared
persistent factor per block, no item-specific persistence) with person-level
heterogeneity as in bench world N8. Uses no lagged/dynamic information from Y.
"""
import numpy as np
from scipy.special import expit, logit, ndtr

LAM = np.array([0.70, 0.60, 0.70, 0.70, 0.65])


def _gaps(D, B):
    g = np.ones(D * B - 1)
    g[B - 1::B] = 16 - (B - 1)          # nominal overnight gap (7 for B = 10)
    return g


def simulate_matched(Y, person, seed, phi=0.55, load_sd=0.3, phi_logit_sd=0.5, rho_pn=-0.45):
    rng = np.random.default_rng(seed)
    M, D, B, J = Y.shape
    T = D * B
    obs = ~np.isnan(Y)                                          # item-level mask (M,D,B,J)
    n_p = int(person.max()) + 1
    phi_p = expit(logit(phi) + phi_logit_sd * rng.standard_normal(n_p))[person]
    lam = np.clip(LAM * np.exp(load_sd * rng.standard_normal((n_p, J))), 0.05, 0.95)[person]
    g = _gaps(D, B)
    L = np.linalg.cholesky(np.array([[1, rho_pn], [rho_pn, 1]]))
    f = np.empty((M, T, 2))
    f[:, 0] = rng.standard_normal((M, 2)) @ L.T
    for t in range(T - 1):
        c = (phi_p ** g[t])[:, None]
        f[:, t + 1] = c * f[:, t] + np.sqrt(1 - c ** 2) * (rng.standard_normal((M, 2)) @ L.T)
    F = f[..., [0, 0, 1, 1, 1]]                                 # PA, PA, NA, NA, NA
    ystar = lam[:, None, :] * F + np.sqrt(1 - lam[:, None, :] ** 2) * rng.standard_normal((M, T, J))
    u = ndtr(ystar).reshape(M, D, B, J)                         # latent percentile
    out = np.full(Y.shape, np.nan)
    for m in range(M):
        for j in range(J):
            o = obs[m, ..., j]
            if not o.any():
                continue
            vals = Y[m, ..., j][o].astype(int)
            cum = np.cumsum(np.bincount(vals, minlength=8)[1:]) / o.sum()   # P(y <= c), c = 1..7
            cat = 1 + np.searchsorted(cum[:-1], u[m, ..., j], side="right")
            out[m, ..., j] = np.where(o, cat, np.nan)
    return out
