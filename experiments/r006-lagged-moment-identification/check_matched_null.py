"""EXPLORATORY validation (post-Part-A, pre-Part-B) of the marginal-matched null used as
Part B's guard: firing rates of the corrected and linear within-person T1 when the
null is matched to a synthetic source dataset (N8-like and N3h-like). MIT licence."""
import json
import warnings
from multiprocessing import Pool

import numpy as np

import lagmom as lm
import matched_null as mn
import simulate as sim

SOURCES = {"N8": 8_100_001, "N3h": 8_100_002}


def one(args):
    src, phi, r = args
    warnings.filterwarnings("ignore")
    Y, person = sim.simulate(sim.WORLDS[src], seed=SOURCES[src])
    Z = mn.simulate_matched(Y, person, seed=int(1000 * phi) * 1000 + r, phi=phi)
    res = lm.analyse(Z, person, discrete=True, n_boot=199, seed=r, linear_too=True)
    return src, phi, {k: res[k] for k in ("cor_w_T1", "cor_w_T1_lo", "lin_w_T1", "lin_w_T1_lo")} | {
        "cor_anyneg3": any(res[f"cor_w_T1_{j}_hi3"] < 0 for j in range(3))}


if __name__ == "__main__":
    jobs = [(s, phi, r) for r in range(50) for s in SOURCES for phi in (0.40, 0.55, 0.70)]
    with Pool(2) as p:
        rows = p.map(one, jobs, chunksize=3)
    out = {}
    for s in SOURCES:
        for phi in (0.40, 0.55, 0.70):
            rr = [o for ss, pp, o in rows if ss == s and pp == phi]
            out[f"{s}_phi{phi}"] = dict(
                n=len(rr),
                cor_mean=float(np.mean([o["cor_w_T1"] for o in rr])), cor_sd=float(np.std([o["cor_w_T1"] for o in rr], ddof=1)),
                cor_fire=float(np.mean([o["cor_w_T1_lo"] > 0 for o in rr])),
                lin_mean=float(np.mean([o["lin_w_T1"] for o in rr])), lin_sd=float(np.std([o["lin_w_T1"] for o in rr], ddof=1)),
                lin_fire=float(np.mean([o["lin_w_T1_lo"] > 0 for o in rr])),
                cor_anyneg3=float(np.mean([o["cor_anyneg3"] for o in rr])))
    json.dump(out, open("results/check_matched_null.json", "w"), indent=1)
    for k, v in out.items():
        print(k, {kk: round(vv, 3) for kk, vv in v.items()})
