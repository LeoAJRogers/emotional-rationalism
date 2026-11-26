"""Exact observational-equivalence checks for the R-006 identification map (DESIGN.md
section 3 and its correction note). Code licence: MIT.

Each check computes both sides of an equivalence by *different* routes and reports the
maximum absolute difference of the implied within-day lag-k covariance matrices
(k = 0..5), or of simulated observations.
Run: python equivalences.py  -> prints results, writes results/equivalences.json
"""
import json
import os

import numpy as np

LAGS = range(6)
LAM3 = np.array([0.70, 0.70, 0.65])
THETA3 = 1 - LAM3 ** 2
PHI = 0.55


def ar_acov(phi, k):
    return phi ** k


def gh_expect(fun, n=80):
    """E[fun(Z)] for Z ~ N(0,1) by Gauss-Hermite quadrature."""
    x, w = np.polynomial.hermite_e.hermegauss(n)
    return float(np.sum(w * fun(x)) / np.sqrt(2 * np.pi))


def e1_loading_heterogeneity(sigma=0.3):
    """Pooled F1 with person-specific loadings lam_j*exp(sigma z_j) vs F1+R with rho=phi."""
    m1 = gh_expect(lambda z: np.exp(sigma * z))
    m2 = gh_expect(lambda z: np.exp(2 * sigma * z))
    worst = 0.0
    for k in LAGS:
        # side A: average of person-level phi^k lam_i lam_i' (+ Theta at lag 0), by quadrature
        EL = np.outer(LAM3, LAM3) * m1 * m1
        np.fill_diagonal(EL, LAM3 ** 2 * m2)
        A = ar_acov(PHI, k) * EL + (np.diag(THETA3) if k == 0 else 0)
        # side B: F1+R with loadings lam*E[e^{sigma z}], residual var lam^2 Var(e^{sigma z}), rho = phi
        lt = LAM3 * np.exp(sigma ** 2 / 2)
        s = LAM3 ** 2 * (np.exp(2 * sigma ** 2) - np.exp(sigma ** 2))
        Bm = ar_acov(PHI, k) * np.outer(lt, lt) + np.diag(s) * PHI ** k + (np.diag(THETA3) if k == 0 else 0)
        worst = max(worst, np.abs(A - Bm).max())
    implied_excess = (np.exp(2 * sigma ** 2) - np.exp(sigma ** 2)) / np.exp(sigma ** 2)
    return worst, implied_excess


def e2_inertia_mixture(phi_a=0.30, phi_b=0.80):
    """Two-point mixture of person inertias vs one factor with two timescales.

    Side A averages person-level AR autocovariances. Side B builds the two-component
    state-space model and propagates its lag-k covariance by matrix powers."""
    worst = 0.0
    lam = LAM3
    for k in LAGS:
        A = np.outer(lam, lam) * (0.5 * phi_a ** k + 0.5 * phi_b ** k) + (np.diag(THETA3) if k == 0 else 0)
        F = np.diag([phi_a, phi_b])                 # state (eta_a, eta_b), unit variances
        G = np.eye(2)                               # stationary covariance
        Ck = np.linalg.matrix_power(F, k) @ G       # Cov(x_{t+k}, x_t)
        H = np.outer(lam, [np.sqrt(0.5), np.sqrt(0.5)])
        Bm = H @ Ck @ H.T + (np.diag(THETA3) if k == 0 else 0)
        worst = max(worst, np.abs(A - Bm).max())
    return worst


def excesses(M):
    g = []
    for j in range(3):
        k, l = [x for x in range(3) if x != j]
        g.append(M[j, j] * M[k, l] - M[j, k] * M[j, l])
    return np.array(g)


def e3a_sign_theorem(n=20000, seed=7):
    """For any rank-2 persistent matrix a a' + b b', prod_j excess_j = -(x y z)^2 <= 0."""
    rng = np.random.default_rng(seed)
    worst, n_all_pos = 0.0, 0
    for _ in range(n):
        a, b = rng.standard_normal(3), rng.standard_normal(3)
        M = np.outer(a, a) + np.outer(b, b)
        g = excesses(M)
        x = a[0] * b[1] - a[1] * b[0]
        y = a[0] * b[2] - a[2] * b[0]
        z = a[1] * b[2] - a[2] * b[1]
        worst = max(worst, abs(np.prod(g) + (x * y * z) ** 2))
        n_all_pos += np.all(g > 1e-12)
    return worst, int(n_all_pos), n


def e3_degenerate():
    """Two items with proportional loadings on both factors: equal-rate F2 equals F1+R with a
    residual on the third item only (exact, all lags)."""
    a = LAM3
    c = 0.4
    b = np.array([c * a[0], c * a[1], -0.25])      # W, F proportional; S distinct
    M = np.outer(a, a) + np.outer(b, b)
    # one-factor decomposition of the persistent matrix
    lam2 = np.array([M[0, 1] * M[0, 2] / M[1, 2], M[0, 1] * M[1, 2] / M[0, 2], M[0, 2] * M[1, 2] / M[0, 1]])
    s = np.diag(M) - lam2
    lam = np.sign(a) * np.sqrt(lam2)
    worst = 0.0
    theta = 1 - np.diag(M)
    for k in LAGS:
        A = PHI ** k * M + (np.diag(theta) if k == 0 else 0)
        Bm = PHI ** k * (np.outer(lam, lam) + np.diag(s)) + (np.diag(theta) if k == 0 else 0)
        worst = max(worst, np.abs(A - Bm).max())
    return worst, s


def e3b_f2r_vs_f1r():
    """Equal-rate F2 + item residuals can equal F1+R exactly (non-identification)."""
    a = LAM3
    b = np.array([0.25, -0.05, 0.10])
    d = np.array([0.10, 0.12, 0.08])                 # item residual variances (rho = phi)
    M = np.outer(a, a) + np.outer(b, b) + np.diag(d)
    g = excesses(M)
    lam2 = np.array([M[0, 1] * M[0, 2] / M[1, 2], M[0, 1] * M[1, 2] / M[0, 2], M[0, 2] * M[1, 2] / M[0, 1]])
    s = np.diag(M) - lam2
    lam = np.sqrt(lam2)
    worst = 0.0
    for k in LAGS:
        A = PHI ** k * M
        Bm = PHI ** k * (np.outer(lam, lam) + np.diag(s))
        worst = max(worst, np.abs(A - Bm).max())
    return worst, g, s


def e4_rotation(seed=11, n=200, T=60):
    """Separate PA/NA persistence (Phi = phi I) vs bipolar valence + acquiescence, simulated
    with the same random numbers through each model's own recursion."""
    rng = np.random.default_rng(seed)
    lam = np.array([0.70, 0.60, 0.70, 0.70, 0.65])
    Lam = np.zeros((5, 2))
    Lam[:2, 0] = lam[:2]
    Lam[2:, 1] = lam[2:]
    G = np.array([[1, -0.45], [-0.45, 1]])
    L = np.linalg.cholesky(G)
    R = np.array([[1, -1], [1, 1]]) / np.sqrt(2)     # (V, A) = R (PA, NA)
    Lam2 = Lam @ R.T                                  # = Lam R^{-1} for orthogonal R
    g = np.ones(T - 1)
    g[9::10] = 7
    z0 = rng.standard_normal((n, 2))
    zs = rng.standard_normal((T - 1, n, 2))
    eps = rng.standard_normal((n, T, 5)) * np.sqrt(1 - lam ** 2)
    x = np.empty((n, T, 2))
    x2 = np.empty((n, T, 2))
    x[:, 0] = z0 @ L.T
    x2[:, 0] = z0 @ (R @ L).T
    for t in range(T - 1):
        c = PHI ** g[t]
        x[:, t + 1] = c * x[:, t] + np.sqrt(1 - c ** 2) * (zs[t] @ L.T)
        x2[:, t + 1] = c * x2[:, t] + np.sqrt(1 - c ** 2) * (zs[t] @ (R @ L).T)
    y = x @ Lam.T + eps
    y2 = x2 @ Lam2.T + eps
    covVA = (R @ G @ R.T)
    return float(np.abs(y - y2).max()), Lam2, covVA


def main():
    out = {}
    w, ex = e1_loading_heterogeneity()
    out["E1_max_abs_diff"] = w
    out["E1_implied_relative_excess_at_logSD_0.3"] = ex
    out["E2_max_abs_diff"] = e2_inertia_mixture()
    w, npos, n = e3a_sign_theorem()
    out["E3a_sign_identity_max_abs_diff"] = w
    out["E3a_random_rank2_all_excess_positive"] = f"{npos}/{n}"
    w, s_deg = e3_degenerate()
    out["E3_degenerate_max_abs_diff"] = w
    out["E3_degenerate_residual_variances"] = s_deg.round(12).tolist()
    w, g, s = e3b_f2r_vs_f1r()
    out["E3b_max_abs_diff"] = w
    out["E3b_excesses"] = g.tolist()
    out["E3b_F1R_residual_variances"] = s.tolist()
    w, Lam2, covVA = e4_rotation()
    out["E4_max_abs_obs_diff"] = w
    out["E4_rotated_loadings_(V,A)"] = Lam2.round(4).tolist()
    out["E4_cov(V,A)"] = covVA.round(4).tolist()
    for k, v in out.items():
        print(f"{k}: {v}")
    os.makedirs("results", exist_ok=True)
    with open("results/equivalences.json", "w") as fh:
        json.dump(out, fh, indent=2)
    ok = (out["E1_max_abs_diff"] < 1e-10 and out["E2_max_abs_diff"] < 1e-10
          and out["E3a_sign_identity_max_abs_diff"] < 1e-10 and npos == 0
          and out["E3_degenerate_max_abs_diff"] < 1e-10 and min(s_deg) >= -1e-12 and min(s) >= 0
          and out["E3b_max_abs_diff"] < 1e-10 and out["E4_max_abs_obs_diff"] < 1e-10)
    print("ALL EXACT CHECKS PASS" if ok else "SOME CHECK FAILED")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
