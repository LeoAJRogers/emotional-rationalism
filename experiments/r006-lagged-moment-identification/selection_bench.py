"""R-006a-S: does report-dependent retention bias within-person T1 under F1? Code licence: MIT.

Preregistered in research-log/prediction-register.md (amendment R-006a) before this was run.
Claude Opus 5.5, 2026-11-23. Gaussian F1 world W0, generated (almost) complete, then thinned:
  (i) MCAR 0.75; (ii) factor-dependent; (iii) report-dependent (last observed NA report that day);
  (iv) arm (i) scored without the day jackknife.
Statistic: linear within-person T1 ('all' variant) exactly as lagmom.analyse computes it.
Run: python selection_bench.py [--reps 300]   -> results/selection_bench.json
"""
import argparse
import json
import os
import time

import numpy as np
from scipy.special import expit, logit

import lagmom as lm
import simulate as sim

PI, SLOPE = 0.75, 1.0
NA = list(sim.NA_ITEMS)


def complete_world(seed):
    """W0 with (almost) every beep observed; returns Y, person, latent NA factor (MP,D,B)."""
    keep = sim.COMPLETENESS, sim.CONCENTRATION
    sim.COMPLETENESS, sim.CONCENTRATION = (1 - 1e-7, 1 - 1e-7), 1e7
    try:
        Y, person, lat = sim.simulate(sim.WORLDS["W0"], seed=seed, return_latent=True)
    finally:
        sim.COMPLETENESS, sim.CONCENTRATION = keep
    return Y, person, lat["fNA"]


def thin(Y, fNA, arm, rng):
    MP, D, B, _ = Y.shape
    base = ~np.isnan(Y).any(-1)
    if arm in ("mcar", "mcar_nojk"):
        keep = rng.random((MP, D, B)) < PI
    elif arm == "factor":
        keep = rng.random((MP, D, B)) < expit(logit(PI) - SLOPE * fNA)
    elif arm == "report":
        rep = np.nanmean(Y[..., NA], -1)                     # NA-mean report at each beep
        z = (rep - np.nanmean(rep)) / np.nanstd(rep)        # one constant scale per dataset
        keep = np.zeros((MP, D, B), bool)
        last = np.full((MP, D), np.nan)                     # last observed report that day
        for b in range(B):
            lp = np.where(np.isnan(last), logit(PI), logit(PI) - SLOPE * np.nan_to_num(last))
            keep[:, :, b] = rng.random((MP, D)) < expit(lp)
            ok = keep[:, :, b] & base[:, :, b]
            last = np.where(ok, z[:, :, b], last)
    else:
        raise ValueError(arm)
    Z = Y.copy()
    Z[~keep] = np.nan
    return Z


def t1(Z, person, jk):
    r = lm.analyse(Z, person, discrete=False, n_boot=2, seed=0, variants=("all",),
                   pooled=False, jk=jk)
    return r["lin_w_T1"], r["lin_n_pp"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=300)
    a = ap.parse_args()
    arms = ["mcar", "factor", "report", "mcar_nojk"]
    vals = {k: [] for k in arms}
    obs_rate = {k: [] for k in arms}
    t0 = time.time()
    for r in range(a.reps):
        Y, person, fNA = complete_world(seed=20261123000 + r)
        for i, arm in enumerate(arms[:3]):
            rng = np.random.default_rng(20261123000 + 1000 * (i + 1) + r)
            Z = thin(Y, fNA, arm, rng)
            v, _ = t1(Z, person, jk=True)
            vals[arm].append(v)
            obs_rate[arm].append(float(np.mean(~np.isnan(Z).any(-1))))
            if arm == "mcar":                               # arm (iv): same thinned data, no jackknife
                v2, _ = t1(Z, person, jk=False)
                vals["mcar_nojk"].append(v2)
                obs_rate["mcar_nojk"].append(obs_rate["mcar"][-1])
    out = {"reps": a.reps, "seconds": round(time.time() - t0, 1), "pi": PI, "slope": SLOPE, "arms": {}}
    for arm in arms:
        v = np.array(vals[arm])
        out["arms"][arm] = dict(mean=float(v.mean()), sd=float(v.std(ddof=1)),
                                mc_se=float(v.std(ddof=1) / np.sqrt(len(v))),
                                z_vs_0=float(v.mean() / (v.std(ddof=1) / np.sqrt(len(v)))),
                                obs_rate=float(np.mean(obs_rate[arm])))
    d = np.array(vals["mcar_nojk"]) - np.array(vals["mcar"])
    out["paired_nojk_minus_jk"] = dict(mean=float(d.mean()), mc_se=float(d.std(ddof=1) / np.sqrt(len(d))),
                                       z=float(d.mean() / (d.std(ddof=1) / np.sqrt(len(d)))))
    A = out["arms"]
    out["verdicts"] = {
        "S1_mcar_within_3se": abs(A["mcar"]["z_vs_0"]) <= 3,
        "S2_factor_within_3se": abs(A["factor"]["z_vs_0"]) <= 3,
        "S3_report_beyond_3se": abs(A["report"]["z_vs_0"]) > 3,
        "S4_nojk_differs_beyond_3se": abs(out["paired_nojk_minus_jk"]["z"]) > 3,
    }
    os.makedirs("results", exist_ok=True)
    with open("results/selection_bench.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
