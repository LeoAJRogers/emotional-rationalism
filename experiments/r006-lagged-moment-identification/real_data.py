"""R-006 Part B runner for openESM 0010 (Geschwind et al.). Code licence: MIT.

Usage:
  python real_data.py --ts PATH/0010_geschwind_ts.tsv --structure-only
  python real_data.py --ts PATH/0010_geschwind_ts.tsv            # full Part B (after prereg)

Writes aggregates only (results/real_0010_*.json); no participant-level values.
Data handling follows R-003/R-003b/R-004: rows without a beep index are dropped; the
two study periods are separate person-periods; day restarts within period; lags are
within-day beep differences (nominal time; openESM 0010 has no raw timestamps).
"""
import argparse
import csv
import hashlib
import json
import os
import sys
import warnings

import numpy as np

import lagmom as lm
import rank3

SHA256_TS = "811f41aeaeb8dbfaa67ca8f8a5387d222701c42fc316f9eb3d61326d138bc8ee"
ITEM_WORDS = ("cheerful", "relaxed", "worried", "fearful", "sad")
KEY_COLS = ("id", "day", "beep", "study_period")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def find_columns(header):
    low = [c.lower() for c in header]
    cols = {}
    for k in KEY_COLS:
        if k not in low:
            raise SystemExit(f"required column '{k}' not found; header = {header}")
        cols[k] = low.index(k)
    for w in ITEM_WORDS:
        hits = [i for i, c in enumerate(low) if w in c]
        if w == "sad":                       # avoid matching e.g. 'sadness_event' if present
            exact = [i for i in hits if low[i] in ("sad", "sad_state", "feel_sad")]
            hits = exact or hits
        if len(hits) != 1:
            raise SystemExit(f"item '{w}': expected exactly one matching column, got "
                             f"{[header[i] for i in hits]}; resolve by hand before running")
        cols[w] = hits[0]
    return cols


def to_float(x):
    x = x.strip()
    if x in ("", "NA", "NaN", "nan", "."):
        return np.nan
    return float(x)


def key_problems(rec):
    """Count key defects that would silently corrupt the array (amendment R-006a, 2026-11-23).

    Day and beep must be integer-valued and >= 1; otherwise int() truncates and a 0 index
    wraps to the last slot. Counts only: no participant-level values are returned.
    """
    out = {}
    for k in ("day", "beep"):
        v = rec[k]
        out[f"{k}_non_integer"] = int(np.sum(np.abs(v - np.round(v)) > 1e-9))
        out[f"{k}_below_1"] = int(np.sum(v < 1))
    return out


def load(path, strict=True):
    """Read the 0010 TSV into Y[person-period, day, beep, item].

    strict=True (any analysis run) fails closed on duplicate id-period-day-beep keys and on
    invalid day/beep values. strict=False (structure-only report) records their counts instead.
    """
    with open(path, newline="") as fh:
        rd = csv.reader(fh, delimiter="\t")
        header = next(rd)
        rows = list(rd)
    cols = find_columns(header)
    rec = {k: np.array([to_float(r[i]) for r in rows]) for k, i in cols.items()}
    info = dict(n_rows=len(rows), columns={k: header[i] for k, i in cols.items()})
    nobeep = np.isnan(rec["beep"])
    info["rows_without_beep"] = int(nobeep.sum())
    info["rows_without_beep_with_any_item"] = int((nobeep & ~np.all(
        np.isnan(np.column_stack([rec[w] for w in ITEM_WORDS])), axis=1)).sum())
    keep = ~nobeep & ~np.isnan(rec["day"]) & ~np.isnan(rec["study_period"]) & ~np.isnan(rec["id"])
    rec = {k: v[keep] for k, v in rec.items()}
    bad = key_problems(rec)
    info.update(bad)
    if strict and any(bad.values()):
        raise SystemExit(f"invalid day/beep values {bad}; refusing to run (fail closed)")
    ok = (np.abs(rec["day"] - np.round(rec["day"])) <= 1e-9) & (rec["day"] >= 1) \
        & (np.abs(rec["beep"] - np.round(rec["beep"])) <= 1e-9) & (rec["beep"] >= 1)
    rec = {k: v[ok] for k, v in rec.items()}               # only reached when strict=False
    ids = np.unique(rec["id"])
    periods = np.unique(rec["study_period"])
    days = np.unique(rec["day"]).astype(int)
    beeps = np.unique(rec["beep"]).astype(int)
    info.update(n_ids=int(len(ids)), periods=periods.tolist(), day_range=[int(days.min()), int(days.max())],
                beep_range=[int(beeps.min()), int(beeps.max())])
    D, B = int(days.max()), int(beeps.max())
    pp = [(i, p) for i in ids for p in periods]
    index = {k: m for m, k in enumerate(pp)}
    Y = np.full((len(pp), D, B, 5), np.nan)
    seen = np.zeros((len(pp), D, B), bool)
    dup = 0
    for r in range(len(rec["id"])):
        m = index[(rec["id"][r], rec["study_period"][r])]
        d, b = int(rec["day"][r]) - 1, int(rec["beep"][r]) - 1
        if seen[m, d, b]:
            dup += 1
            continue                                       # never overwrite an earlier record
        seen[m, d, b] = True
        Y[m, d, b] = [rec[w][r] for w in ITEM_WORDS]
    info["duplicate_id_period_day_beep"] = dup
    if strict and dup:
        raise SystemExit(f"{dup} duplicate id-period-day-beep keys; refusing to run (fail closed)")
    person = np.array([np.searchsorted(ids, i) for (i, _) in pp])
    complete5 = ~np.isnan(Y).any(-1)
    completeNA = ~np.isnan(Y[..., 2:]).any(-1)
    info["beeps_all_five_items"] = int(complete5.sum())
    info["beeps_all_NA_items"] = int(completeNA.sum())
    info["values_outside_1_7"] = int(np.nansum((Y < 1) | (Y > 7)))
    info["non_integer_values"] = int(np.nansum(np.abs(Y - np.round(Y)) > 1e-9))
    info["non_finite_values"] = int(np.sum(np.isinf(Y)))
    # R-006b (GPT-6.2 on ER #13): the Hermite correction assumes integer categories 1..7, so any
    # analysis run fails closed on out-of-range, non-integer or infinite item values.
    if strict and (info["values_outside_1_7"] or info["non_integer_values"] or info["non_finite_values"]):
        raise SystemExit("item values outside the documented integer range 1..7; refusing to run (fail closed)")
    return Y, person, info


def floor_rates(Y, items=(2, 3, 4)):
    """Per person-period floor (category 1) rate among OBSERVED responses of each item.

    Amendment R-006a (2026-11-23): the earlier inline expression np.nanmean(Y == 1) divided by
    scheduled slots, because Y == 1 is False (not NaN) at missing beeps (found by GPT-6, ER #13).
    A person-period with no observed response for an item gets rate 1.0 (excluded downstream).
    """
    out = np.ones((Y.shape[0], len(items)))
    for m in range(Y.shape[0]):
        for c, j in enumerate(items):
            v = Y[m, ..., j]
            obs = v[np.isfinite(v)]
            if obs.size:
                out[m, c] = float(np.mean(obs == 1))
    return out


def marginals(Y):
    """Pooled category frequencies per item and quantiles of person-period floor rates."""
    out = {}
    for j, w in enumerate(ITEM_WORDS):
        v = Y[..., j]
        vals = v[~np.isnan(v)].astype(int)
        out[w + "_category_counts_1to7"] = np.bincount(vals, minlength=8)[1:].tolist()
        fl, ce = [], []
        for m in range(Y.shape[0]):
            x = v[m][~np.isnan(v[m])]
            if len(x) >= 15:
                fl.append(np.mean(x == 1))
                ce.append(np.mean(x == 7))
        out[w + "_pooled_floor_rate"] = float(np.mean(vals == 1))
        out[w + "_pp_floor_rate_quantiles_10_50_90"] = np.quantile(fl, [0.1, 0.5, 0.9]).round(3).tolist()
        out[w + "_pp_ceiling_rate_quantiles_10_50_90"] = np.quantile(ce, [0.1, 0.5, 0.9]).round(3).tolist()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ts", required=True)
    ap.add_argument("--structure-only", action="store_true")
    ap.add_argument("--boot", type=int, default=1999)
    ap.add_argument("--null-reps", type=int, default=100)
    a = ap.parse_args()
    h = sha256(a.ts)
    if h != SHA256_TS:
        raise SystemExit(f"SHA-256 mismatch: {h} (expected {SHA256_TS}); refusing to run")
    Y, person, info = load(a.ts, strict=not a.structure_only)
    info["sha256"] = h
    os.makedirs("results", exist_ok=True)
    with open("results/real_0010_structure.json", "w") as fh:
        json.dump(info, fh, indent=1)
    print(json.dumps(info, indent=1))
    if a.structure_only:
        return
    run_part_b(Y, person, info, a.boot, a.null_reps)


def git_head():
    try:
        import subprocess
        return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception:                                    # noqa: BLE001
        return "unknown"


def beep_centered_linear(Y):
    """Sensitivity: remove population item x beep-of-day means (linear statistics only)."""
    Z = Y.copy()
    for j in range(Y.shape[-1]):
        for b in range(Y.shape[2]):
            v = Z[:, :, b, j]
            Z[:, :, b, j] = v - np.nanmean(v)
    return Z


def summarise_stats(res, prefix):
    keys = [k for k in res if k.startswith(prefix)]
    return {k: res[k] for k in keys}


def run_part_b(Y, person, info, n_boot, null_reps):
    import datetime
    import matched_null as mn
    out = dict(code_commit=git_head(), run_utc=datetime.datetime.utcnow().isoformat() + "Z",
               sha256=info["sha256"], n_boot=n_boot)
    out["marginals"] = marginals(Y)
    # 1. primary and secondary statistics (corrected and linear; within and pooled)
    res = lm.analyse(Y, person, discrete=True, n_boot=n_boot, seed=20261121)
    res.update(rank3.analyse_rank(Y, person, discrete=True, n_boot=n_boot, seed=20261124))   # R-006b
    out["main"] = res
    # 2. marginal-matched F1 null (no dynamic information from Y is used)
    keys = []
    for tag in ("cor", "lin"):
        keys += [f"{tag}_w_T1", f"{tag}_w_T1_lo", f"{tag}_w_T2_W", f"{tag}_w_T20_W", f"{tag}_w_PA_det",
                 f"{tag}_w_PA_det_lo", f"{tag}_p_T1", f"{tag}_w_T1day_lo", f"{tag}_w_BIP"]
        keys += [f"{tag}_w_T1_{j}_hi3" for j in range(3)] + [f"{tag}_w_T1_{j}" for j in range(3)]
        keys += [f"{tag}_w_T_det", f"{tag}_w_T_det_lo", f"{tag}_w_OFF_lo"]                  # R-006b
    nulls = {}
    for phi in (0.40, 0.55, 0.70):
        vals = []
        for r in range(null_reps):
            Z = mn.simulate_matched(Y, person, seed=int(1000 * phi) * 1000 + r, phi=phi)
            rr = lm.analyse(Z, person, discrete=True, n_boot=199, seed=r, linear_too=True)
            rr.update(rank3.analyse_rank(Z, person, discrete=True, n_boot=199, seed=r))  # R-006b
            vals.append({k: rr[k] for k in keys})
        nulls[str(phi)] = vals
    mnull = {}
    for phi, vals in nulls.items():
        d = {"n": len(vals)}
        for k in keys:
            v = np.array([x[k] for x in vals], float)
            d[k + "_mean"], d[k + "_sd"] = float(np.mean(v)), float(np.std(v, ddof=1))
            d[k + "_q025"], d[k + "_q95"], d[k + "_q975"] = (float(np.quantile(v, q)) for q in (0.025, 0.95, 0.975))
        for tag in ("cor", "lin"):
            d[f"{tag}_T1_ci_fire_rate"] = float(np.mean([x[f"{tag}_w_T1_lo"] > 0 for x in vals]))
            d[f"{tag}_anyneg3_rate"] = float(np.mean([any(x[f"{tag}_w_T1_{j}_hi3"] < 0 for j in range(3))
                                                      for x in vals]))
            d[f"{tag}_T2_fire_rate"] = float(np.mean([x[f"{tag}_w_T2_W"] > 5.991 for x in vals]))
            d[f"{tag}_Tdet_ci_fire_rate"] = float(np.mean([x[f"{tag}_w_T_det_lo"] > 0 for x in vals]))
            d[f"{tag}_OFF_ci_pos_rate"] = float(np.mean([x[f"{tag}_w_OFF_lo"] > 0 for x in vals]))
        mnull[phi] = d
    out["matched_null"] = mnull
    # 3. sensitivity analyses
    sens = {}
    sens["beep_of_day_centered_linear"] = summarise_stats(
        lm.analyse(beep_centered_linear(Y), person, discrete=False, n_boot=n_boot, seed=1), "lin_w_T")
    for per in (0, 1):
        sel = np.arange(Y.shape[0]) % 2 == per            # person-periods are ordered (id, period)
        sub = np.unique(person[sel], return_inverse=True)[1]
        r = lm.analyse(Y[sel], sub, discrete=True, n_boot=n_boot, seed=2 + per, linear_too=False)
        sens[f"period_{per}_only"] = summarise_stats(r, "cor_w_T")
    floor = floor_rates(Y)                                 # observed-response denominator (R-006a)
    sel = (floor < 0.5).all(1)
    sens["low_floor_subset_n_pp"] = int(sel.sum())
    if sel.sum() >= 40:
        sub = np.unique(person[sel], return_inverse=True)[1]
        r = lm.analyse(Y[sel], sub, discrete=True, n_boot=n_boot, seed=5, linear_too=False)
        sens["low_floor_subset"] = summarise_stats(r, "cor_w_T")
    out["sensitivity"] = sens
    os.makedirs("results", exist_ok=True)
    with open("results/real_0010_partB.json", "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    print(json.dumps({k: out[k] for k in ("code_commit", "run_utc")}, indent=1))


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    main()
