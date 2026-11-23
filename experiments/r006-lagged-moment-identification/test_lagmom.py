"""Unit tests for lagmom.py. Run: python test_lagmom.py (exits non-zero on failure)."""
import itertools
import sys
from math import factorial

import numpy as np
from scipy.stats import multivariate_normal, norm

import lagmom as lm

FAIL = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  {detail}" if detail else ""))
    if not ok:
        FAIL.append(name)


def brute_ustat(Xs, mask, k, e, k2, f, variant, pairs):
    """Explicit double loop over lag-k and lag-k2 pairs of one person-period."""
    D, B, J = Xs.shape
    j, l = pairs[e]
    j2, l2 = pairs[f]

    def prod(t, tp, a, b):
        if t == tp:
            return Xs[t[0], t[1], a] * Xs[tp[0], tp[1], b]
        return 0.5 * (Xs[t[0], t[1], a] * Xs[tp[0], tp[1], b] + Xs[t[0], t[1], b] * Xs[tp[0], tp[1], a])

    def plist(kk):
        out = []
        for d in range(D):
            for b in range(kk, B):
                if mask[d, b] and mask[d, b - kk]:
                    out.append(((d, b), (d, b - kk)))
        return out

    A, Bl = plist(k), plist(k2)
    num, cnt = 0.0, 0
    for p in A:
        for q in Bl:
            if set(p) & set(q):
                continue
            if variant == "day" and p[0][0] != q[0][0]:
                continue
            if variant == "cross" and p[0][0] == q[0][0]:
                continue
            num += prod(p[0], p[1], j, l) * prod(q[0], q[1], j2, l2)
            cnt += 1
    return num / cnt


def test_ustat():
    rng = np.random.default_rng(1)
    M, D, B, J = 3, 3, 6, 3
    Y = rng.standard_normal((M, D, B, J))
    miss = rng.random((M, D, B)) < 0.25
    Y[miss] = np.nan
    LM = lm.LagMoments(Y, (0, 1, 2), discrete=False, lags=(0, 1, 2, 3),
                       min_beeps=1, min_pairs=1, min_days=1)
    pairs = LM.pairs
    worst = 0.0
    for v in (0, 2):                                   # full data and leave-out-day-1
        for m in range(M):
            # reconstruct the centred, scaled data used by version v
            mask = LM.mask[v, m]
            X = np.where(np.isnan(Y[m]), 0.0, Y[m])
            n = mask.sum()
            mean = (X * mask[..., None]).sum((0, 1)) / n
            Xc = (X - mean) * mask[..., None]
            s = np.sqrt(((Xc ** 2).sum((0, 1)) / n).mean())
            Xs = Xc / s
            for (k, k2) in [(1, 1), (1, 2), (0, 1), (2, 2), (3, 1)]:
                for e, f in [(0, 4), (1, 2), (5, 3), (2, 2)]:
                    for variant in ("all", "day", "cross"):
                        u = LM.ustat(k, e, k2, f, variant)[v, m]
                        bu = brute_ustat(Xs, mask, k, e, k2, f, variant, pairs)
                        if np.isfinite(u) or np.isfinite(bu):
                            worst = max(worst, abs(u - bu))
    check("U-statistic vectorized == brute force", worst < 1e-10, f"max abs diff {worst:.2e}")


def test_hermite():
    """Cov(g1(Z1), g2(Z2)) for step functions equals sum a1n a2n r^n / n!."""
    t1 = np.array([-0.3, 0.4, 1.1, 1.7])
    t2 = np.array([0.8, 1.5, 2.2])
    worst = 0.0
    for r in (-0.4, 0.15, 0.5, 0.8):
        # exact covariance of the integer scores: sum over threshold pairs
        cov = 0.0
        for a in t1:
            for b in t2:
                p11 = multivariate_normal(mean=[0, 0], cov=[[1, r], [r, 1]]).cdf([-a, -b])
                cov += p11 - norm.cdf(-a) * norm.cdf(-b)
        h1 = lm.hermite_coeffs(t1).sum(0)
        h2 = lm.hermite_coeffs(t2).sum(0)
        series = sum(h1[n - 1] * h2[n - 1] * r ** n / factorial(n) for n in range(1, lm.K_HERMITE + 1))
        worst = max(worst, abs(series - cov))
    check("Hermite covariance series == bivariate normal", worst < 2e-6, f"max abs diff {worst:.2e}")
    b = np.array([[0.3, 0.05, -0.02, 0.01]])
    C = b[0, 0] * 0.4 + b[0, 1] * 0.4 ** 2 + b[0, 2] * 0.4 ** 3 + b[0, 3] * 0.4 ** 4
    r = lm.solve_latent_r(b, np.array([C]))
    check("Newton inverse recovers r", abs(r[0] - 0.4) < 1e-10, f"r = {r[0]:.12f}")


def test_jackknife_linear():
    """For a statistic that is exactly linear in day totals, the jackknife leaves it unchanged."""
    rng = np.random.default_rng(3)
    M, D, B, J = 4, 5, 8, 3
    Y = rng.standard_normal((M, D, B, J))
    LM = lm.LagMoments(Y, (0, 1, 2), discrete=False, lags=(1,), min_beeps=1, min_pairs=1, min_days=1)
    est = np.tile(np.arange(M, dtype=float), (D + 1, 1))   # identical across versions
    jk = LM.jackknife(est)
    check("jackknife of a constant estimate is the constant", np.allclose(jk, np.arange(M)))


def test_real_loader():
    """real_data.load() on a fake TSV in the documented 0010 layout reproduces the array."""
    import csv
    import os
    import tempfile

    import real_data
    import simulate as sim
    Y, person = sim.simulate(sim.WORLDS["N3"], seed=4, n_persons=6)
    rows = []
    for m in range(Y.shape[0]):
        pid, per = 1000 + person[m], m % 2
        for d in range(10):                                  # padded to 10 days like 0010
            for b in range(10):
                vals = Y[m, d, b] if d < 6 else np.full(5, np.nan)
                rows.append([pid, d + 1, b + 1, per] + ["NA" if np.isnan(x) else str(int(x)) for x in vals])
        rows.append([pid, 1, "NA", per, "3", "NA", "NA", "NA", "NA"])   # row without beep index
    path = os.path.join(tempfile.mkdtemp(), "fake.tsv")
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["id", "day", "beep", "study_period", "cheerful", "relaxed", "worried", "fearful", "sad"])
        w.writerows(rows)
    Y2, person2, info = real_data.load(path)
    same = np.array_equal(np.isnan(Y2[:, :6]), np.isnan(Y)) and np.allclose(np.nan_to_num(Y2[:, :6]), np.nan_to_num(Y))
    check("real-data loader reproduces array; padded days empty", same and np.isnan(Y2[:, 6:]).all()
          and info["rows_without_beep"] == Y.shape[0] and np.array_equal(person2, person), str(info["day_range"]))


def _fake_tsv(rows):
    import csv
    import os
    import tempfile
    path = os.path.join(tempfile.mkdtemp(), "fake.tsv")
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["id", "day", "beep", "study_period", "cheerful", "relaxed", "worried", "fearful", "sad"])
        w.writerows(rows)
    return path


def test_real_loader_fail_closed():
    """Amendment R-006a (2026-11-23), GPT-6 requests on ER #13: duplicate keys and invalid
    day/beep values stop any analysis run; the structure-only report counts them instead."""
    import real_data
    base = [[1, d, b, 0, "4", "4", "2", "1", "3"] for d in (1, 2) for b in (1, 2, 3)]
    def raises(rows):
        try:
            real_data.load(_fake_tsv(rows), strict=True)
        except SystemExit:
            return True
        return False
    dup = base + [[1, 1, 2, 0, "7", "7", "7", "7", "7"]]
    check("strict loader fails closed on a duplicate id-period-day-beep key", raises(dup))
    Y, _, info = real_data.load(_fake_tsv(dup), strict=False)
    check("structure-only loader counts the duplicate and keeps the first record",
          info["duplicate_id_period_day_beep"] == 1 and Y[0, 0, 1, 0] == 4.0, str(Y[0, 0, 1, 0]))
    check("strict loader fails closed on day 0 (would wrap to the last day)",
          raises(base + [[1, 0, 1, 0, "4", "4", "2", "1", "3"]]))
    check("strict loader fails closed on a non-integer beep",
          raises(base + [[1, 1, 2.5, 0, "4", "4", "2", "1", "3"]]))
    check("strict loader accepts clean keys", not raises(base))


def test_floor_rate_denominator():
    """GPT-6's example on ER #13: observed [1, 1, 6, 7] plus six missing beeps -> 0.5, not 0.2."""
    import real_data
    Y = np.full((1, 1, 10, 5), np.nan)
    Y[0, 0, :4, 2] = [1, 1, 6, 7]
    Y[0, 0, :, 3] = 1.0                                  # fully observed, all floor -> 1.0
    r = real_data.floor_rates(Y)
    old = np.nanmean(Y[0, ..., 2] == 1)                  # the replaced expression, for the record
    check("floor rate uses observed responses as denominator", np.isclose(r[0, 0], 0.5)
          and np.isclose(r[0, 1], 1.0) and r[0, 2] == 1.0 and np.isclose(old, 0.2),
          f"new {r[0, 0]:.2f}, old {old:.2f}; item with no responses -> {r[0, 2]:.1f}")


if __name__ == "__main__":
    test_ustat()
    test_hermite()
    test_jackknife_linear()
    test_real_loader()
    test_real_loader_fail_closed()
    test_floor_rate_denominator()
    print("FAILURES:", FAIL if FAIL else "none")
    sys.exit(1 if FAIL else 0)
