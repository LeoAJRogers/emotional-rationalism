"""R-006b-H: heterogeneous equal-rate F2 in the stress set, and the persistent-rank statistic.

Preregistered in research-log/prediction-register.md (amendment R-006b) before this was run.
Claude Opus 5.5, 2026-11-24 (ER daily run). Code licence: MIT.

Worlds (simulate.py): W0, W1s, W1w, W2e, W2h (new: F2 at the shared rate, with the second
factor's loadings (0.30, 0, -0.30) cyclically shifted across three person classes, so a
different NA item carries the negative excess in each class), and the realistic ordinal
N8, W2h+N8 and W1s+N8.
Per replicate: within T1 and T1_j ('all', day-jackknifed) with 95% and Bonferroni 98.33%
person-bootstrap intervals, the T2 Wald statistic, and rank3.T_det and OFF with 95% intervals.
Ordinal worlds: Hermite-corrected ('cor') and linear ('lin'); Gaussian worlds: linear.
Run: python hetero_f2_bench.py [--reps 200] [--boot 499]  -> results/hetero_f2_bench.json
"""
import argparse
import json
import os
import time

import numpy as np

import lagmom as lm
import rank3
import simulate as sim

W = sim.WORLDS
sim.WORLDS["W2h"] = sim.world(f2_phi=0.55, f2_hetero=True)
sim.WORLDS["W2h+N8"] = sim.world(**sim.N8, f2_phi=0.55, f2_hetero=True)
WORLD_LIST = ["W0", "W1s", "W1w", "W2e", "W2h", "N8", "W2h+N8", "W1s+N8"]
SEED0 = 20261124000


def one(Y, person, discrete, n_boot, seed):
    n_persons = int(person.max()) + 1
    counts = lm.boot_counts(n_persons, n_boot, np.random.default_rng(seed))
    out = {}
    modes = [("cor", True), ("lin", False)] if discrete else [("lin", False)]
    for tag, correct in modes:
        LM = lm.LagMoments(Y, lm.NA_IDX, discrete, lags=(1, 2), correct=correct, jk=True)
        cache = {}
        stats = lm.t1_stats("all") + lm.t2_stats(1, 2, "T2")
        est, draws = lm.compute_within(LM, stats, person, n_persons, counts, cache)
        r = {}
        lm._store(r, "w", est, draws, stats)
        e3, d3, n_ok = rank3.t_det(LM, person, n_persons, counts)
        for k in ("T_det", "OFF"):
            lo, hi = lm.ci(d3[k])
            r[f"w_{k}"], r[f"w_{k}_lo"], r[f"w_{k}_hi"] = float(e3[k]), lo, hi
        r["n_pp_det"] = n_ok
        out[tag] = r
    return out


def summarise(rows):
    """rows: list of per-replicate dicts for one mode."""
    g = lambda k: np.array([r[k] for r in rows], float)
    s = {}
    for k in ("w_T1", "w_T1_0", "w_T1_1", "w_T1_2", "w_T_det", "w_OFF"):
        v = g(k)
        s[k + "_mean"] = float(np.mean(v))
        s[k + "_sd"] = float(np.std(v, ddof=1))
        s[k + "_mcse"] = float(np.std(v, ddof=1) / np.sqrt(len(v)))
    s["T1_fires"] = float(np.mean(g("w_T1_lo") > 0))
    s["sign_fires_bonf"] = float(np.mean(np.any(np.column_stack([g(f"w_T1_{j}_hi3") < 0 for j in range(3)]), 1)))
    s["sign_fires_by_item_bonf"] = [float(np.mean(g(f"w_T1_{j}_hi3") < 0)) for j in range(3)]
    s["T2_fires"] = float(np.mean(g("w_T2_W") > 5.991))
    s["Tdet_fires"] = float(np.mean(g("w_T_det_lo") > 0))
    s["Tdet_neg_fires"] = float(np.mean(g("w_T_det_hi") < 0))
    s["OFF_positive"] = float(np.mean(g("w_OFF_lo") > 0))
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--boot", type=int, default=499)
    ap.add_argument("--worlds", nargs="*", default=WORLD_LIST)
    a = ap.parse_args()
    t0 = time.time()
    res = {"reps": a.reps, "boot": a.boot, "seed0": SEED0, "worlds": {}}
    for wi, name in enumerate(WORLD_LIST):
        if name not in a.worlds:
            continue
        cfg = W[name]
        per_mode = {}
        for rep in range(a.reps):
            seed = SEED0 + 1000 * wi + rep
            Y, person = sim.simulate(cfg, seed=seed)
            r = one(Y, person, cfg["ordinal"], a.boot, seed)
            for tag, v in r.items():
                per_mode.setdefault(tag, []).append(v)
        res["worlds"][name] = {tag: summarise(rows) for tag, rows in per_mode.items()}
        res["worlds"][name]["seconds_cum"] = round(time.time() - t0, 1)
        print(name, json.dumps(res["worlds"][name]), flush=True)
    res["seconds"] = round(time.time() - t0, 1)
    os.makedirs("results", exist_ok=True)
    out = "results/hetero_f2_bench.json" if a.worlds == WORLD_LIST else "results/hetero_f2_bench_partial.json"
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
