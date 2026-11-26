"""R-006 Part A synthetic bench (preregistered in research-log/prediction-register.md).

Run: python bench.py [--reps 200] [--workers 2] [--boot 499]
Writes results/bench_raw.jsonl (one line per world x replicate) and
results/bench_summary.json (fire rates, means, SDs per world and statistic).
Code licence: MIT.
"""
import argparse
import json
import os
import time
import warnings
from multiprocessing import Pool

import numpy as np

import lagmom as lm
import simulate as sim

WALD_CRIT = 5.991
OUT = "results"


def fires(res):
    """Decision indicators for one replicate (DESIGN.md section 5)."""
    f = {}
    for key, val in res.items():
        if key.endswith("_lo"):
            base = key[:-3]
            f[base + "_pos"] = bool(res[key] > 0)
            f[base + "_neg"] = bool(res[base + "_hi"] < 0)
        elif key.endswith("_W"):
            f[key + "_fire"] = bool(val > WALD_CRIT)
    return f


def run_one(args):
    wname, widx, rep, n_boot = args
    warnings.filterwarnings("ignore")
    cfg = sim.WORLDS[wname]
    seed = 100000 * (widx + 1) + rep
    Y, person = sim.simulate(cfg, seed=seed)
    res = lm.analyse(Y, person, discrete=cfg["ordinal"], n_boot=n_boot, seed=rep)
    res = {k: (float(v) if isinstance(v, (float, np.floating)) else v) for k, v in res.items()}
    return dict(world=wname, rep=rep, seed=seed, res=res, fire=fires(res))


def summarise(rows):
    out = {}
    worlds = sorted({r["world"] for r in rows}, key=list(sim.WORLDS).index)
    for w in worlds:
        rr = [r for r in rows if r["world"] == w]
        s = {"n_reps": len(rr)}
        keys = [k for k in rr[0]["res"] if not (k.endswith("_lo") or k.endswith("_hi"))]
        for k in keys:
            v = np.array([r["res"][k] for r in rr], float)
            s[k + "_mean"] = float(np.nanmean(v))
            s[k + "_sd"] = float(np.nanstd(v, ddof=1))
        for k in rr[0]["fire"]:
            s[k + "_rate"] = float(np.mean([r["fire"][k] for r in rr]))
        out[w] = s
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--boot", type=int, default=499)
    ap.add_argument("--worlds", default="all")
    a = ap.parse_args()
    names = list(sim.WORLDS) if a.worlds == "all" else a.worlds.split(",")
    jobs = [(w, list(sim.WORLDS).index(w), r, a.boot) for w in names for r in range(a.reps)]
    # interleave ordinal and Gaussian worlds for even load
    jobs.sort(key=lambda j: (j[2], j[1]))
    os.makedirs(OUT, exist_ok=True)
    raw_path = os.path.join(OUT, "bench_raw.jsonl")
    t0 = time.time()
    rows = []
    with Pool(a.workers) as pool, open(raw_path, "w") as fh:
        for i, row in enumerate(pool.imap_unordered(run_one, jobs, chunksize=2)):
            rows.append(row)
            fh.write(json.dumps(row) + "\n")
            if (i + 1) % 200 == 0:
                fh.flush()
                print(f"{i + 1}/{len(jobs)} done, {time.time() - t0:.0f}s", flush=True)
    summ = summarise(rows)
    summ["_meta"] = dict(reps=a.reps, boot=a.boot, seconds=time.time() - t0,
                         worlds=names, wald_crit=WALD_CRIT)
    with open(os.path.join(OUT, "bench_summary.json"), "w") as fh:
        json.dump(summ, fh, indent=1)
    print(f"finished in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
