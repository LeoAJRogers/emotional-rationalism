"""R-006c-cal: matched-null calibration rerun for the guarded Part B rules. Code licence: MIT.

Claude Opus 5.5, 2026-11-26. Implements exactly the preregistration "R-006c-cal" appended to
research-log/prediction-register.md on 2026-11-26 (worlds C0-C5, a separate C0 reference set,
seeds, B = 199, predictions P1-P6, conditional DETNUM rule). Written and smoke-tested before any
full run; synthetic data only; no 0010 access.

Run (full, about 60 CPU-minutes at ~2.6 s per dataset):
    python calibrate_r006c.py --n 200 --workers 2
Smoke test (pipeline check only, NOT a result; written to results/r006c_cal_smoke_*.json):
    python calibrate_r006c.py --smoke
"""
import argparse
import json
import os
import warnings
from multiprocessing import Pool

import numpy as np

import decide_part_b as dp
import lagmom as lm
import rank3
import real_data as rd
import simulate as sim

B = 199
WORLDS = {
    "C0": sim.world(**sim.N8),
    "C1": sim.world(**sim.N8, f2_phi=0.55, f2_hetero=True),
    "C2": sim.world(**dict(sim.N8, phi_logit_sd=0.0), phi=-0.30),
    "C3": sim.world(**dict(sim.N8, phi_logit_sd=0.0), phi=0.15),
    "C4": sim.world(**sim.N8, persistence="two_timescale"),
    "C5": sim.world(**sim.N8, item_excess=0.25),
}
WORLD_INDEX = {w: i for i, w in enumerate(WORLDS)}
REF_SEED0 = 20261127900
FLAGS = ["B2_status", "B1_heterogeneity_status", "B3_rank2_sign_status", "B4_T2_status", "B5_T20_status",
         "B6_BIP_status", "B7_PAdet_status", "B8_pooled_within_null_range_status", "T1day_status",
         "OFF_precondition_status", "Tdet_selected_OFF_status", "Tdet_raw_threshold_status", "DETNUM_status"]


def seed_of(world, r):
    return 20261127000 + 1000 * WORLD_INDEX[world] + r


def analyse_one(args):
    cfg, seed = args
    warnings.filterwarnings("ignore")
    Y, person = sim.simulate(cfg, seed=seed)
    r = lm.analyse(Y, person, discrete=True, n_boot=B, seed=seed % 100000, linear_too=True)
    r.update(rank3.analyse_rank(Y, person, discrete=True, n_boot=B, seed=seed % 100000))
    return {k: (float(v) if isinstance(v, (int, float, np.floating, np.integer)) else v) for k, v in r.items()}


def mc_rate(x):
    x = np.asarray(x, float)
    p = float(x.mean()) if x.size else float("nan")
    return {"rate": p, "mc_se": float(np.sqrt(p * (1 - p) / x.size)) if x.size else float("nan"), "n": int(x.size)}


def summarise_world(results, verdicts, version_key="primary_version"):
    out = {"n": len(results)}
    for f in FLAGS:
        st = [v.get(f) for v in verdicts]
        out[f] = {s: float(np.mean([x == s for x in st])) for s in ("fires", "no_fire", "invalid")}
    out["Tdet_interpretable"] = mc_rate([v["Tdet_interpretable"] for v in verdicts])
    out["Tdet_interpretable_concordant_fire"] = mc_rate([v["Tdet_interpretable_concordant_fire"] for v in verdicts])
    out["B2_fires"] = mc_rate([v["B2_status"] == "fires" for v in verdicts])
    out["lin_OFF_gate_pass"] = mc_rate([v["OFF_precondition_status"] == "fires" for v in verdicts])
    out["selected_version"] = {t: float(np.mean([v[version_key] == t for v in verdicts])) for t in ("cor", "lin")}
    out["failed_gate_counts"] = {}
    for v in verdicts:
        for g in v["Tdet_failed_gates"]:
            out["failed_gate_counts"][g] = out["failed_gate_counts"].get(g, 0) + 1
    for tag in ("cor", "lin"):
        d = np.array([r[f"{tag}_w_DETNUM"] for r in results], float)
        d = d[np.isfinite(d)]
        lo = np.array([r[f"{tag}_w_DETNUM_lo"] for r in results], float)
        hi = np.array([r[f"{tag}_w_DETNUM_hi"] for r in results], float)
        out[f"{tag}_DETNUM"] = {
            "n_finite": int(d.size),
            "mean": float(d.mean()) if d.size else float("nan"),
            "mean_mc_se": float(d.std(ddof=1) / np.sqrt(d.size)) if d.size > 1 else float("nan"),
            "sd": float(d.std(ddof=1)) if d.size > 1 else float("nan"),
            "q025_q50_q975": [float(np.quantile(d, q)) for q in (0.025, 0.5, 0.975)] if d.size else [],
            "ci_above_0_rate": float(np.mean(lo > 0)),
            "ci_below_0_rate": float(np.mean(hi < 0)),
        }
        for k in ("n_persons_det", "mean_days_det", "jk_fallback_frac_det", "w_T_det_finite_frac"):
            v = np.array([r[f"{tag}_{k}"] for r in results], float)
            out[f"{tag}_{k}_mean"] = float(np.nanmean(v))
    return out


def evaluate(S):
    """Preregistered predictions P1-P6 (R-006c-cal). Failure criteria as registered."""
    P = {}
    c0 = S["C0"]
    P["P1"] = {"concordant_Tdet_fire": c0["Tdet_interpretable_concordant_fire"]["rate"],
               "B2_fire": c0["B2_fires"]["rate"]}
    P["P1"]["held"] = P["P1"]["concordant_Tdet_fire"] <= 0.075 and P["P1"]["B2_fire"] <= 0.075
    c2 = S["C2"]
    P["P2"] = {"lin_OFF_gate_pass": c2["lin_OFF_gate_pass"]["rate"],
               "concordant_Tdet_fire": c2["Tdet_interpretable_concordant_fire"]["rate"]}
    P["P2"]["held"] = P["P2"]["lin_OFF_gate_pass"] <= 0.075 and P["P2"]["concordant_Tdet_fire"] == 0.0
    c3 = S["C3"]
    P["P3"] = {"concordant_Tdet_fire": c3["Tdet_interpretable_concordant_fire"]["rate"],
               "Tdet_withheld_exploratory": 1 - c3["Tdet_interpretable"]["rate"]}
    P["P3"]["held"] = P["P3"]["concordant_Tdet_fire"] <= 0.075
    c4 = S["C4"]
    P["P4"] = {"B2_fire": c4["B2_fires"]["rate"], "concordant_Tdet_fire": c4["Tdet_interpretable_concordant_fire"]["rate"]}
    P["P4"]["day_dependence_material"] = P["P4"]["B2_fire"] > 0.075 or P["P4"]["concordant_Tdet_fire"] > 0.075
    c1 = S["C1"]
    sel = max(c1["selected_version"], key=c1["selected_version"].get)
    dn = c1[f"{sel}_DETNUM"]
    P["P5"] = {"version": sel, "mean": dn["mean"], "mean_mc_se": dn["mean_mc_se"], "ci_below_0_rate": dn["ci_below_0_rate"]}
    P["P5"]["held"] = (dn["mean"] + 1.96 * dn["mean_mc_se"] < 0) and dn["ci_below_0_rate"] >= 0.20
    c5 = S["C5"]
    P["P6"] = {"concordant_Tdet_fire": c5["Tdet_interpretable_concordant_fire"]["rate"]}
    P["P6"]["held"] = P["P6"]["concordant_Tdet_fire"] >= 0.10
    P["conditional_DETNUM_rule_triggered"] = P["P5"]["held"]
    return P


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--smoke", action="store_true", help="2 datasets per world; pipeline check, not a result")
    a = ap.parse_args()
    n = 2 if a.smoke else a.n
    tag = "smoke" if a.smoke else "full"
    os.makedirs("results", exist_ok=True)
    jobs = [("REF", r, (WORLDS["C0"], REF_SEED0 + r)) for r in range(n)]
    jobs += [(w, r, (cfg, seed_of(w, r))) for w, cfg in WORLDS.items() for r in range(n)]
    with Pool(a.workers) as pool:
        res = pool.map(analyse_one, [j[2] for j in jobs])
    by = {}
    for (w, r, _), x in zip(jobs, res):
        by.setdefault(w, []).append(x)
    ref = rd.summarise_null({"ref": [{k: x[k] for k in rd.null_keys()} for x in by["REF"]]})
    S, raw = {}, {}
    for w in WORLDS:
        verdicts = [dp.decide({"main": x, "matched_null": ref}) for x in by[w]]
        S[w] = summarise_world(by[w], verdicts)
        raw[w] = [{"seed": seed_of(w, r), "verdict": {k: v for k, v in V.items() if k != "estimates"}}
                  for r, V in enumerate(verdicts)]
    out = {"prereg": "R-006c-cal (prediction-register.md, 2026-11-26)", "mode": tag, "n_per_world": n,
           "B": B, "code_commit": rd.git_head(), "summary": S,
           "evaluation": None if a.smoke else evaluate(S)}
    with open(f"results/r006c_cal_{tag}_summary.json", "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    with open(f"results/r006c_cal_{tag}_verdicts.json", "w") as fh:
        json.dump(raw, fh, default=float)
    print(json.dumps({"mode": tag, "n": n, "evaluation": out["evaluation"]}, indent=1, default=float))


if __name__ == "__main__":
    main()
