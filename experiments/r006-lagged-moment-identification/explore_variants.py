"""EXPLORATORY (written and run after the preregistered Part A bench): estimator variants
in the realistic ordinal worlds, to inform the choice of Part B's primary estimator
before any real data are accessed. Not part of the Part A predictions.

Variant compared with the preregistered estimator: day jackknife off (jk=False).
Run: python explore_variants.py [--reps 100] -> results/explore_variants.json. MIT licence.
"""
import argparse
import json
import time
import warnings
from multiprocessing import Pool

import numpy as np

import lagmom as lm
import simulate as sim
from bench import fires

WORLDS = ["N8", "N9", "N3h", "W1s+N8", "W1w+N8", "W2s+N8", "W2e+N8"]


def run_one(args):
    wname, rep, jk = args
    warnings.filterwarnings("ignore")
    cfg = sim.WORLDS[wname]
    seed = 100000 * (list(sim.WORLDS).index(wname) + 1) + rep     # same datasets as the bench
    Y, person = sim.simulate(cfg, seed=seed)
    res = lm.analyse(Y, person, discrete=True, n_boot=499, seed=rep, jk=jk, linear_too=False)
    return wname, rep, jk, res, fires(res)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=100)
    a = ap.parse_args()
    jobs = [(w, r, False) for r in range(a.reps) for w in WORLDS]
    t0 = time.time()
    out = {}
    with Pool(2) as pool:
        rows = pool.map(run_one, jobs, chunksize=4)
    for w in WORLDS:
        rr = [x for x in rows if x[0] == w]
        s = {}
        for k in ("cor_w_T1", "cor_w_T1_0", "cor_w_T1_1", "cor_w_T1_2", "cor_w_T2_W", "cor_p_T1"):
            v = np.array([x[3][k] for x in rr])
            s[k + "_mean"], s[k + "_sd"] = float(np.mean(v)), float(np.std(v, ddof=1))
        for k in ("cor_w_T1_pos", "cor_w_T1_1_neg", "cor_w_T2_W_fire", "cor_p_T1_pos"):
            s[k + "_rate"] = float(np.mean([x[4][k] for x in rr]))
        s["n_reps"] = len(rr)
        out[w] = s
    out["_meta"] = dict(variant="jk=False", reps=a.reps, seconds=time.time() - t0,
                        note="exploratory; datasets identical to the bench's first reps for each world")
    with open("results/explore_variants.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
