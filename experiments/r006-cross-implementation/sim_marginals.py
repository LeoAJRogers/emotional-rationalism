"""R-006d follow-up: do the #13 and #14 N3h simulators differ in distribution? (Claude, 2026-11-28)

The R-006d decision rule says that if the estimators agree on the same data (P3) but the
T1 distributions differ (P4), the simulators' floor rates, completeness and lag-1
autocorrelations are compared. The rule was fixed before the run; the statistics below
were chosen after it, so this is exploratory. Synthetic data only.

Usage: python -I sim_marginals.py DIR13 DIR14 [--world N3h] [--reps 500]
"""
import argparse
import json
import sys

import numpy as np

G_ORDER = ['W0', 'N3', 'N3h', 'N8', 'W1s+N8', 'W1w+N8', 'N6', 'N7']


def stats(Y):
    """Per-dataset summaries of a (254, 6, 10, 3) ordinal NA array with NaN = missing."""
    out = {}
    obs = np.isfinite(Y).all(-1)                                   # (M,D,B)
    out['complete_p0'] = obs[0::2].mean()
    out['complete_p1'] = obs[1::2].mean()
    for j in range(3):
        y = Y[..., j]
        yo = y[obs]
        for c in (1, 2, 3):
            out[f'item{j}_cat{c}'] = np.mean(yo == c)
        # person-period floor rates and their spread
        n = obs.sum((1, 2))
        fr = np.where(obs, y == 1, False).sum((1, 2)) / np.maximum(n, 1)
        out[f'item{j}_floor_sd_pp'] = fr[n > 0].std()
        out[f'item{j}_floor_ge95_pp'] = np.mean(fr[n >= 15] >= 0.95)
        # within person-period centring, then pooled lag-1 (within day) autocorrelation
        mu = np.where(obs, y, 0).sum((1, 2)) / np.maximum(n, 1)
        yc = np.where(obs, y - mu[:, None, None], np.nan)
        a, b = yc[:, :, 1:], yc[:, :, :-1]
        ok = np.isfinite(a) & np.isfinite(b)
        out[f'item{j}_lag1_ac'] = np.sum(a[ok] * b[ok]) / np.sqrt(np.sum(a[ok] ** 2) * np.sum(b[ok] ** 2))
    # lag-0 and lag-1 cross-item correlations (items 0,1), centred within person-period
    n = obs.sum((1, 2))
    mu = np.where(obs[..., None], Y, 0).sum((1, 2)) / np.maximum(n, 1)[:, None]
    Yc = np.where(obs[..., None], Y - mu[:, None, None, :], np.nan)
    x0, x1 = Yc[..., 0][obs], Yc[..., 1][obs]
    out['cross01_lag0'] = np.sum(x0 * x1) / np.sqrt(np.sum(x0 ** 2) * np.sum(x1 ** 2))
    a, b = Yc[:, :, 1:, 0], Yc[:, :, :-1, 1]
    ok = np.isfinite(a) & np.isfinite(b)
    out['cross01_lag1'] = np.sum(a[ok] * b[ok]) / np.sqrt(np.sum(a[ok] ** 2) * np.sum(b[ok] ** 2))
    return {k: float(v) for k, v in out.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dir13')
    ap.add_argument('dir14')
    ap.add_argument('--world', default='N3h')
    ap.add_argument('--reps', type=int, default=500)
    ap.add_argument('--out', default='results/n3h_sim_marginals.json')
    a = ap.parse_args()
    sys.path.insert(0, a.dir14)
    sys.path.insert(0, a.dir13)
    import calibrate_t1_independent as G
    import lagmom as LM
    import simulate as SIM
    wc = list(SIM.WORLDS).index(a.world)
    wg = G_ORDER.index(a.world)
    rows = {'C': [], 'G': []}
    for rep in range(a.reps):
        Y5, _ = SIM.simulate(SIM.WORLDS[a.world], seed=100000 * (wc + 1) + rep)
        rows['C'].append(stats(Y5[..., list(LM.NA_IDX)]))
        rows['G'].append(stats(G.sim(np.random.default_rng(100000 * (wg + 1) + rep), a.world)))
    keys = list(rows['C'][0])
    table = {}
    for k in keys:
        c = np.array([r[k] for r in rows['C']])
        g = np.array([r[k] for r in rows['G']])
        z = (g.mean() - c.mean()) / np.sqrt(g.var(ddof=1) / g.size + c.var(ddof=1) / c.size)
        table[k] = dict(C_mean=float(c.mean()), G_mean=float(g.mean()), welch_z=float(z))
    flagged = [k for k, v in table.items() if abs(v['welch_z']) > 3.5]
    res = dict(world=a.world, reps=a.reps, flag_rule='|z| > 3.5 (about 0.05 / 25 two-sided)',
               flagged=flagged, table=table)
    with open(a.out, 'w') as fh:
        json.dump(res, fh, indent=1)
    for k, v in table.items():
        print(f"{k:22s} C {v['C_mean']:+.5f}  G {v['G_mean']:+.5f}  z {v['welch_z']:+.2f}")
    print('flagged:', flagged)


if __name__ == '__main__':
    main()
