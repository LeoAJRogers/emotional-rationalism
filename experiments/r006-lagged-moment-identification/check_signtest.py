"""EXPLORATORY calibration check (post-Part-A, pre-Part-B) of the Bonferroni per-item sign
test, on FRESH seeds (not the bench's datasets). MIT licence."""
import json
import warnings
from multiprocessing import Pool

import numpy as np

import lagmom as lm
import simulate as sim

WORLDS = ["N8", "N9", "W1s+N8", "W2s+N8", "W2e+N8"]


def one(args):
    w, r = args
    warnings.filterwarnings("ignore")
    Y, person = sim.simulate(sim.WORLDS[w], seed=7_000_000 + 1000 * WORLDS.index(w) + r)
    res = lm.analyse(Y, person, discrete=True, n_boot=499, seed=r, linear_too=True)
    out = {}
    for tag in ("cor", "lin"):
        out[tag + "_anyneg3"] = any(res[f"{tag}_w_T1_{j}_hi3"] < 0 for j in range(3))
        out[tag + "_anyneg95"] = any(res[f"{tag}_w_T1_{j}_hi"] < 0 for j in range(3))
        out[tag + "_T1fire"] = res[f"{tag}_w_T1_lo"] > 0
        out[tag + "_T1"] = res[f"{tag}_w_T1"]
    return w, out


if __name__ == "__main__":
    jobs = [(w, r) for r in range(100) for w in WORLDS]
    with Pool(2) as p:
        rows = p.map(one, jobs, chunksize=4)
    summ = {}
    for w in WORLDS:
        rr = [o for ww, o in rows if ww == w]
        summ[w] = {k: float(np.mean([o[k] for o in rr])) for k in rr[0]}
        summ[w]["n"] = len(rr)
    summ["_meta"] = "exploratory; fresh seeds 7,000,000+; Bonferroni 98.33% per-item intervals"
    json.dump(summ, open("results/check_signtest.json", "w"), indent=1)
    print(json.dumps(summ, indent=1))
