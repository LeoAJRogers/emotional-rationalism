"""Apply the preregistered R-006 Part B decision rules (register addendum) mechanically to
results/real_0010_partB.json. Written before any 0010 item data were accessed. MIT licence.
Amended by R-006b (2026-11-24, still before any 0010 data access): heterogeneous rank-2 reading,
linear OFF precondition, and the secondary persistent-rank statistic T_det.
Amended by R-006c (2026-11-26, still before any 0010 data access), after GPT-6.2's reviews of
R-006b and of the first R-006c head (ed90ec9) on ER PR #13. Fail-closed throughout:
  - every required matched-null summary is validated separately for each phi BEFORE any max/min
    reduction (Python's max/min can hide a NaN); an empty phi set is invalid;
  - intervals need both endpoints finite and lo <= hi; rates must be finite and in [0, 1];
  - each statistic gets a status: "fires", "no_fire" or "invalid". An invalid statistic is never
    reported as a non-fire, and an infinite statistic can never fire;
  - invalid selection calibration (cor/lin SD ratio) makes the primary reading not interpretable;
    it no longer falls back to "lin" silently;
  - T_det is interpreted only if both OFF gates pass (finite, ordered, lower bound > 0), its support
    guards pass (finite draws, person-periods, persons, days, jackknife fallbacks, matched-null
    non-finite rate <= 0.05 literal) and it is calibrated. A raw threshold crossing is reported
    separately from interpretable, raw-numerator-concordant evidence, with the failed gates named;
  - readings are worded as evidence against the declared restricted null under the model and
    measurement assumptions; T1day is diagnostic only.
Run: python decide_part_b.py -> results/real_0010_partB_verdicts.json
"""
import json
import math

WALD = 5.991
MIN_PP_DET = 40             # usable person-periods for T_det
MIN_PERSONS_DET = 30        # distinct persons among them
MIN_MEAN_DAYS_DET = 4.0     # mean observed days per usable person-period (triple U-statistic needs >= 3)
MAX_JK_FALLBACK_DET = 0.10  # share of usable person-periods whose day jackknife fell back
MIN_FINITE_FRAC = 0.95      # share of finite bootstrap draws for T_det
MAX_NONFINITE_RATE = 0.05   # matched-null share of replicates with non-finite T_det (literal limit)
MAX_FIRE_RATE = 0.10        # calibration limit for matched-null interval firing
SD_RATIO_MAX = 1.5          # corrected/linear matched-null SD ratio for choosing "cor"


def is_num(x):
    """A finite real number (bool and missing values excluded)."""
    if isinstance(x, bool) or x is None:
        return False
    try:
        return math.isfinite(float(x))
    except (TypeError, ValueError):
        return False


class Calib:
    """Matched-null summaries validated per phi before any reduction."""

    def __init__(self, nl):
        self.nl = nl if isinstance(nl, dict) else {}
        self.phis = sorted(self.nl)
        self.problems = []
        if not self.phis:
            self.problems.append("matched-null calibration set is empty")

    def values(self, k):
        if not self.phis:
            return None
        vals = [self.nl[p].get(k) if isinstance(self.nl[p], dict) else None for p in self.phis]
        if not all(is_num(v) for v in vals):
            self.problems.append(f"matched-null {k} missing or non-finite at some phi")
            return None
        return [float(v) for v in vals]

    def max(self, k):
        v = self.values(k)
        return None if v is None else max(v)

    def min(self, k):
        v = self.values(k)
        return None if v is None else min(v)

    def rate_max(self, k):
        v = self.values(k)
        if v is None:
            return None
        if not all(0.0 <= x <= 1.0 for x in v):
            self.problems.append(f"matched-null {k} outside [0, 1] at some phi")
            return None
        return max(v)


def num(m, k):
    v = m.get(k)
    return float(v) if is_num(v) else None


def interval(m, prefix):
    """(est, lo, hi) if all finite and lo <= hi, else None."""
    est, lo, hi = num(m, prefix), num(m, prefix + "_lo"), num(m, prefix + "_hi")
    if est is None or lo is None or hi is None or lo > hi:
        return None
    return est, lo, hi


def status(valid, fires):
    return "invalid" if not valid else ("fires" if fires else "no_fire")


def decide(o):
    m = o.get("main", {}) if isinstance(o.get("main"), dict) else {}
    C = Calib(o.get("matched_null"))
    V = {}

    # ---- version selection (prospective rule for invalid calibration: fail closed)
    sd_c, sd_l = C.max("cor_w_T1_sd"), C.max("lin_w_T1_sd")
    if sd_c is None or sd_l is None or sd_l <= 0:
        V["selection_valid"], V["sd_ratio_cor_over_lin"], p = False, None, None
    else:
        ratio = sd_c / sd_l
        V["selection_valid"], V["sd_ratio_cor_over_lin"] = True, ratio
        p = "cor" if ratio <= SD_RATIO_MAX else "lin"
    V["primary_version"] = p

    # ---- primary T1
    thr = C.max(f"{p}_w_T1_q975") if p else None
    t1 = interval(m, f"{p}_w_T1") if p else None
    fire_rate = C.rate_max(f"{p}_T1_ci_fire_rate") if p else None
    V["primary_threshold"] = thr
    V["primary_matched_null_ci_fire_rate_max"] = fire_rate
    V["primary_valid"] = V["selection_valid"] and None not in (thr, t1, fire_rate)
    V["primary_uncalibrated"] = V["primary_valid"] and fire_rate > MAX_FIRE_RATE
    V["B2_status"] = status(V["primary_valid"], V["primary_valid"] and t1[1] > 0 and t1[0] > thr)
    V["B2_within_T1_fires"] = V["B2_status"] == "fires"

    # ---- auxiliary statistics: each with an explicit status
    def aux(name, valid, fires):
        V[name + "_status"] = status(valid, valid and fires)

    if p:
        pT1, wT1 = num(m, f"{p}_p_T1"), num(m, f"{p}_w_T1")
        aux("B1_heterogeneity", None not in (pT1, wT1), pT1 is not None and wT1 is not None and pT1 - wT1 >= 0.10)
        items, items_valid = [], True
        for j in range(3):
            e, hi3, q = num(m, f"{p}_w_T1_{j}"), num(m, f"{p}_w_T1_{j}_hi3"), C.min(f"{p}_w_T1_{j}_q025")
            if None in (e, hi3, q):
                items_valid = False
                items.append(None)
            else:
                items.append(hi3 < 0 and e < q)
        V["sign_test_items_below_null"] = items
        sr = C.rate_max(f"{p}_anyneg3_rate")
        V["sign_test_calibration_valid"] = sr is not None
        V["sign_test_uncalibrated"] = sr is None or sr > MAX_FIRE_RATE
        aux("B3_rank2_sign", items_valid and sr is not None, items_valid and any(items) and sr <= MAX_FIRE_RATE)
        for nm, key, q in (("B4_T2", f"{p}_w_T2_W", f"{p}_w_T2_W_q95"), ("B5_T20", f"{p}_w_T20_W", f"{p}_w_T20_W_q95")):
            x, qq = num(m, key), C.max(q)
            aux(nm, None not in (x, qq), x is not None and qq is not None and x > WALD and x > qq)
        bip = interval(m, f"{p}_w_BIP")
        aux("B6_BIP", bip is not None, bip is not None and bip[1] > 0)
        pa, paq = interval(m, f"{p}_w_PA_det"), C.max(f"{p}_w_PA_det_q975")
        aux("B7_PAdet", None not in (pa, paq), pa is not None and paq is not None and pa[1] > 0 and pa[0] > paq)
        lo8, hi8 = C.min(f"{p}_p_T1_q025"), C.max(f"{p}_p_T1_q975")
        aux("B8_pooled_within_null_range", None not in (lo8, hi8, pT1),
            None not in (lo8, hi8, pT1) and lo8 <= pT1 <= hi8)
        day = interval(m, f"{p}_w_T1day")
        aux("T1day", day is not None, day is not None and day[1] > 0)
    V["B3_rank2_sign"] = V.get("B3_rank2_sign_status") == "fires"
    V["T1day_fires"] = V.get("T1day_status") == "fires"

    # ---- OFF gates (finite, ordered, lower bound > 0)
    lin_off = interval(m, "lin_w_OFF")
    V["OFF_precondition_status"] = status(lin_off is not None, lin_off is not None and lin_off[1] > 0)
    V["OFF_precondition_met"] = V["OFF_precondition_status"] == "fires"
    sel_off = interval(m, f"{p}_w_OFF") if p else None
    V["Tdet_selected_OFF_status"] = status(sel_off is not None, sel_off is not None and sel_off[1] > 0)

    # ---- T_det support, calibration and fire
    gates = []
    if V["OFF_precondition_status"] != "fires":
        gates.append("linear OFF precondition " + ("invalid" if V["OFF_precondition_status"] == "invalid" else "not met"))
    if V["Tdet_selected_OFF_status"] != "fires":
        gates.append(f"selected-version ({p}) OFF interval " +
                     ("invalid" if V["Tdet_selected_OFF_status"] == "invalid" else "not above 0"))
    td = interval(m, f"{p}_w_T_det") if p else None
    tq = C.max(f"{p}_w_T_det_q975") if p else None
    sup = {k: (num(m, f"{p}_{k}") if p else None) for k in
           ("w_T_det_finite_frac", "n_pp_det", "n_persons_det", "mean_days_det", "jk_fallback_frac_det")}
    nfr = C.rate_max(f"{p}_Tdet_nonfinite_rate") if p else None
    tfr = C.rate_max(f"{p}_Tdet_ci_fire_rate") if p else None
    checks = [
        ("T_det estimate or interval invalid", td is not None),
        ("matched-null T_det threshold invalid", tq is not None),
        ("finite-draw share below 0.95 or invalid", sup["w_T_det_finite_frac"] is not None
         and 0.0 <= sup["w_T_det_finite_frac"] <= 1.0 and sup["w_T_det_finite_frac"] >= MIN_FINITE_FRAC),
        ("fewer than 40 usable person-periods", sup["n_pp_det"] is not None and sup["n_pp_det"] >= MIN_PP_DET),
        ("fewer than 30 distinct persons", sup["n_persons_det"] is not None and sup["n_persons_det"] >= MIN_PERSONS_DET),
        ("mean observed days below 4", sup["mean_days_det"] is not None and sup["mean_days_det"] >= MIN_MEAN_DAYS_DET),
        ("jackknife fallback share above 0.10 or invalid", sup["jk_fallback_frac_det"] is not None
         and 0.0 <= sup["jk_fallback_frac_det"] <= MAX_JK_FALLBACK_DET),
        ("matched-null non-finite T_det rate above 0.05 or invalid", nfr is not None and nfr <= MAX_NONFINITE_RATE),
    ]
    failed_support = [msg for msg, ok in checks if not ok]
    V["Tdet_support_ok"] = not failed_support
    V["Tdet_uncalibrated"] = tfr is None or tfr > MAX_FIRE_RATE
    if V["Tdet_uncalibrated"]:
        gates.append("T_det uncalibrated on the real marginals" if tfr is not None else "T_det calibration rate invalid")
    gates += failed_support
    V["Tdet_raw_threshold_status"] = status(td is not None and tq is not None,
                                            td is not None and tq is not None and td[1] > 0 and td[0] > tq)
    dn = interval(m, f"{p}_w_DETNUM") if p else None
    V["DETNUM_status"] = status(dn is not None, dn is not None and dn[1] > 0)
    V["Tdet_interpretable"] = not gates
    V["Tdet_failed_gates"] = gates
    V["Tdet_interpretable_concordant_fire"] = (V["Tdet_interpretable"] and V["Tdet_raw_threshold_status"] == "fires"
                                               and V["DETNUM_status"] == "fires")
    V["Tdet_fires"] = V["Tdet_interpretable_concordant_fire"]
    V["calibration_problems"] = sorted(set(C.problems))
    V["estimates"] = {k: m.get(f"{p}_{k}") for k in (
        "w_T1", "w_T1_lo", "w_T1_hi", "w_T1_0", "w_T1_1", "w_T1_2", "p_T1", "w_T1day", "w_T2_W",
        "w_T20_W", "w_PA_det", "w_BIP", "w_T3", "w_T_det", "w_T_det_lo", "w_T_det_hi", "w_OFF", "w_OFF_lo",
        "w_OFF_hi", "w_DETNUM", "w_DETNUM_lo", "w_DETNUM_hi", "w_T_det_finite_frac", "n_pp_det",
        "n_persons_det", "mean_days_det", "jk_fallback_frac_det")} if p else {}
    V["estimates"]["lin_w_OFF_lo"] = m.get("lin_w_OFF_lo")

    # ---- preregistered reading
    if not V["selection_valid"]:
        reading = ("not interpretable: the version-selection calibration (matched-null T1 SDs) is missing, "
                   "non-finite or degenerate at some phi (reported as a failure, not as a null)")
    elif not V["primary_valid"]:
        reading = ("not interpretable: a primary estimate, interval, threshold or matched-null summary is missing, "
                   "non-finite or out of range at some phi (reported as a failure, not as a null)")
    elif V["primary_uncalibrated"]:
        reading = "primary statistic uncalibrated on the real marginals (matched-null firing > 10%): not interpreted"
    elif V["B3_rank2_sign_status"] == "invalid":
        reading = "the sign test's inputs or calibration are missing or non-finite: not interpreted"
    elif V["sign_test_uncalibrated"] and any(x for x in V["sign_test_items_below_null"]):
        reading = "an item shows negative excess, but the sign test is uncalibrated on the real marginals: not interpreted"
    elif V["B3_rank2_sign"]:
        reading = ("evidence against the declared restricted null (homogeneous F1+R) in the direction of rank-2 "
                   "shared persistence, under the model and measurement assumptions; not unique proof of F2; "
                   "T1 sign not read as item persistence")
    elif V["B2_within_T1_fires"]:
        reading = ("evidence against the declared F1 null under the model and measurement assumptions; not "
                   "separable among item-specific persistence, response anchoring, between-day loading drift and "
                   "heterogeneous rank-2 shared persistence (second factor at the shared rate)")
        if V["T1day_status"] == "fires":
            reading += ("; T1day also fires (diagnostic only: no calibrated bound against drift rivals has "
                        "been established, so drift is not excluded)")
        elif V["T1day_status"] == "invalid":
            reading += "; T1day invalid (missing or non-finite): not reported"
    else:
        reading = ("no detectable within-person item-specific or second-dimension persistence at this design's "
                   "power (Part A, corrected, N8-like: 0.98 at T1 = 0.25; 0.29 at T1 = 0.10); not evidence of "
                   "absence")
    primary_ok = V["primary_valid"] and not V["primary_uncalibrated"]
    if V["B2_within_T1_fires"] and primary_ok:
        if not V["Tdet_interpretable"]:
            raw = {"fires": "raw threshold crossed", "no_fire": "raw threshold not crossed",
                   "invalid": "raw statistic invalid"}[V["Tdet_raw_threshold_status"]]
            reading += "; T_det withheld (" + "; ".join(gates) + "; " + raw + "): not interpreted"
        elif V["Tdet_raw_threshold_status"] == "fires" and V["DETNUM_status"] != "fires":
            reading += ("; T_det crosses its threshold but the raw determinant numerator interval is "
                        + ("invalid" if V["DETNUM_status"] == "invalid" else "not above 0")
                        + ": discordant, not interpreted")
        elif V["Tdet_interpretable_concordant_fire"]:
            reading += ("; T_det fires with a concordant raw numerator: evidence against the declared rank <= 2 "
                        "null under the model and measurement assumptions, so heterogeneous rank-2 F2 is not "
                        "supported as the sole source of T1 (anchoring and drift remain)")
        else:
            reading += ("; T_det does not fire: uninformative at its observed low power (13-17% at T1 = 0.25+ "
                        "under realistic nuisance, R-006b-H); rank 2 is not established")
    if V["OFF_precondition_status"] != "fires" and primary_ok:
        V["diagnostic_unconditioned_reading"] = reading
        reading = ("positive-shared-lag precondition " +
                   ("invalid (missing or non-finite linear OFF interval)" if V["OFF_precondition_status"] == "invalid"
                    else "not met (linear OFF interval not above 0)") +
                   ": T1, the sign test and T_det are not read as evidence on F1+R versus F2. The unconditioned "
                   "reading is recorded only as a diagnostic.")
    V["reading"] = reading
    return V


def main(path="results/real_0010_partB.json"):
    with open(path) as fh:
        o = json.load(fh)
    V = decide(o)
    with open("results/real_0010_partB_verdicts.json", "w") as fh:
        json.dump(V, fh, indent=1, default=float)
    print(json.dumps(V, indent=1, default=float))


if __name__ == "__main__":
    main()
