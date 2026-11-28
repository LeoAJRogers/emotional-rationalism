"""R-006d-r: fresh-seed replication of the E2 median comparison (Claude, 2026-11-28).

Registered after the R-006d run and before this one (see the register). Corrected T1
with #13's estimator, lag 1 only (bit-identical to lags 0-3 for T1, checked on two
N3h datasets), on new replicates of each simulator, seeded by each branch's own rule.
Synthetic data only.

Usage: python -I fresh_seeds.py DIR13 DIR14 [--world N3h] [--start 200] [--reps 600]
"""
import argparse
import json
import sys
from multiprocessing import Pool

import numpy as np
from scipy import stats as sps

G_ORDER = ['W0', 'N3', 'N3h', 'N8', 'W1s+N8', 'W1w+N8', 'N6', 'N7']
LM = SIM = G = None


def load(dir13, dir14):
    global LM, SIM, G
    sys.path.insert(0, dir14)
    sys.path.insert(0, dir13)
    import calibrate_t1_independent
    import lagmom
    import simulate
    LM, SIM, G = lagmom, simulate, calibrate_t1_independent


def t1(Y3):
    person = np.repeat(np.arange(127), 2)
    lmo = LM.LagMoments(Y3, (0, 1, 2), True, lags=(1,), correct=True, jk=True)
    st = [s for s in LM.t1_stats('all') if s.name == 'T1']
    est, _ = LM.compute_within(lmo, st, person, 127, np.ones((1, 127)), {})
    return float(est['T1'])


def one(args):
    world, rep = args
    Y5, _ = SIM.simulate(SIM.WORLDS[world], seed=100000 * (list(SIM.WORLDS).index(world) + 1) + rep)
    Yg = G.sim(np.random.default_rng(100000 * (G_ORDER.index(world) + 1) + rep), world)
    return rep, t1(Y5[..., list(LM.NA_IDX)]), t1(Yg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dir13')
    ap.add_argument('dir14')
    ap.add_argument('--world', default='N3h')
    ap.add_argument('--start', type=int, default=200)
    ap.add_argument('--reps', type=int, default=600)
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--out', default='results/n3h_fresh_seeds.json')
    a = ap.parse_args()
    import warnings
    warnings.filterwarnings('ignore')
    jobs = [(a.world, r) for r in range(a.start, a.start + a.reps)]
    with Pool(a.workers, initializer=load, initargs=(a.dir13, a.dir14)) as pool:
        rows = list(pool.imap(one, jobs, chunksize=4))
    c = np.array([r[1] for r in rows])
    g = np.array([r[2] for r in rows])
    rng = np.random.default_rng(20261128)
    ic = rng.integers(0, c.size, (10000, c.size))
    ig = rng.integers(0, g.size, (10000, g.size))
    d = np.median(g[ig], axis=1) - np.median(c[ic], axis=1)
    td = sps.trim_mean(g[ig], 0.1, axis=1) - sps.trim_mean(c[ic], 0.1, axis=1)
    ks = sps.ks_2samp(g, c)
    res = dict(world=a.world, start=a.start, reps=a.reps,
               C=dict(mean=float(c.mean()), sd=float(c.std(ddof=1)), median=float(np.median(c)),
                      trim10=float(sps.trim_mean(c, 0.1))),
               G=dict(mean=float(g.mean()), sd=float(g.std(ddof=1)), median=float(np.median(g)),
                      trim10=float(sps.trim_mean(g, 0.1))),
               median_diff_G_minus_C=[float(np.median(g) - np.median(c)),
                                      [float(np.quantile(d, .025)), float(np.quantile(d, .975))]],
               trim10_diff_G_minus_C=[float(sps.trim_mean(g, 0.1) - sps.trim_mean(c, 0.1)),
                                      [float(np.quantile(td, .025)), float(np.quantile(td, .975))]],
               ks_D=float(ks.statistic), ks_p=float(ks.pvalue),
               rows=[list(r) for r in rows])
    with open(a.out, 'w') as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != 'rows'}, indent=1))


if __name__ == '__main__':
    main()
