"""Apply the preregistered R-006 Part B decision rules (register addendum) mechanically to
results/real_0010_partB.json. Written before any 0010 item data were accessed. MIT licence.
Amended by R-006b (2026-11-24, still before any 0010 data access): heterogeneous rank-2 reading,
linear OFF precondition, and the secondary persistent-rank statistic T_det.
Amended by R-006c (2026-11-26, still before any 0010 data access), after GPT-6.2's review of
R-006b on ER PR #13:
  - finiteness and support guards: a non-finite estimate, interval, threshold or matched-null
    summary makes the affected statistic "not interpretable", never a null;
  - T_det is interpreted only if the linear OFF precondition holds AND the selected version's own
    OFF interval is above 0 AND its support guards pass; otherwise it is reported as withheld;
  - the raw determinant numerator (DETNUM) is a registered sensitivity check: a firing T_det
    whose raw numerator interval is not above 0 is reported as discordant, not interpreted;
  - readings are worded as evidence against the declared restricted null under the model and
    measurement assumptions, not as identification of a mechanism; T1day is diagnostic only;
  - when the OFF precondition fails, the unconditioned reading is kept only as a diagnostic field.
Run: python decide_part_b.py -> results/real_0010_partB_verdicts.json
"""
import json
import math

WALD = 5.991
MIN_PP_DET = 40           # R-006c: minimum usable person-periods for T_det (as the low-floor subset rule)
MIN_FINITE_FRAC = 0.95    # R-006c: minimum share of finite bootstrap draws for T_det


def finite(*xs):
    """True if every value is a finite real number (missing keys count as not finite)."""
    try:
        return all(x is not None and math.isfinite(float(x)) for x in xs)
    except (TypeError, ValueError):
        return False


def decide(o):
    m, nl = o["main"], o["matched_null"]
    phis = sorted(nl)
    g = lambda d, k: d.get(k, float("nan"))
    mx = lambda k: max(g(nl[p], k) for p in phis)                   # most conservative over phi
    mn_ = lambda k: min(g(nl[p], k) for p in phis)
    ratio = mx("cor_w_T1_sd") / mx("lin_w_T1_sd") if finite(mx("cor_w_T1_sd"), mx("lin_w_T1_sd")) \
        and mx("lin_w_T1_sd") > 0 else float("nan")
    p = "cor" if finite(ratio) and ratio <= 1.5 else "lin"
    thr = mx(f"{p}_w_T1_q975")
    V = dict(primary_version=p, sd_ratio_cor_over_lin=ratio, primary_threshold=thr)
    V["primary_finite"] = finite(m.get(f"{p}_w_T1"), m.get(f"{p}_w_T1_lo"), thr,
                                 mx(f"{p}_T1_ci_fire_rate"))
    V["B1_heterogeneity"] = (g(m, f"{p}_p_T1") - g(m, f"{p}_w_T1")) >= 0.10
    V["B2_within_T1_fires"] = V["primary_finite"] and (m[f"{p}_w_T1_lo"] > 0) and (m[f"{p}_w_T1"] > thr)
    V["sign_test_items_below_null"] = [bool(g(m, f"{p}_w_T1_{j}_hi3") < 0 and g(m, f"{p}_w_T1_{j}") < mn_(f"{p}_w_T1_{j}_q025"))
                                       for j in range(3)]
    V["sign_test_uncalibrated"] = not (mx(f"{p}_anyneg3_rate") <= 0.10)       # NaN counts as uncalibrated
    V["B3_rank2_sign"] = any(V["sign_test_items_below_null"]) and not V["sign_test_uncalibrated"]
    V["B4_T2_fires"] = (g(m, f"{p}_w_T2_W") > WALD) and (g(m, f"{p}_w_T2_W") > mx(f"{p}_w_T2_W_q95"))
    V["B5_T20_fires"] = (g(m, f"{p}_w_T20_W") > WALD) and (g(m, f"{p}_w_T20_W") > mx(f"{p}_w_T20_W_q95"))
    V["B6_BIP_fires"] = g(m, f"{p}_w_BIP_lo") > 0
    V["B7_PAdet_fires"] = (g(m, f"{p}_w_PA_det_lo") > 0) and (g(m, f"{p}_w_PA_det") > mx(f"{p}_w_PA_det_q975"))
    V["B8_pooled_within_null_range"] = mn_(f"{p}_p_T1_q025") <= g(m, f"{p}_p_T1") <= mx(f"{p}_p_T1_q975")
    V["T1day_fires"] = g(m, f"{p}_w_T1day_lo") > 0
    # R-006b precondition (linear OFF), kept as registered
    V["OFF_precondition_met"] = g(m, "lin_w_OFF_lo") > 0
    # R-006c: T_det guards. The selected version's own denominator must be positive, and support adequate.
    V["Tdet_selected_OFF_positive"] = g(m, f"{p}_w_OFF_lo") > 0
    V["Tdet_support_ok"] = (finite(m.get(f"{p}_w_T_det"), m.get(f"{p}_w_T_det_lo"), mx(f"{p}_w_T_det_q975"),
                                   mx(f"{p}_Tdet_ci_fire_rate"))
                            and g(m, f"{p}_w_T_det_finite_frac") >= MIN_FINITE_FRAC
                            and g(m, f"{p}_n_pp_det") >= MIN_PP_DET
                            and not (mx(f"{p}_Tdet_nonfinite_rate") > 1 - MIN_FINITE_FRAC))
    V["Tdet_uncalibrated"] = not (mx(f"{p}_Tdet_ci_fire_rate") <= 0.10)
    V["Tdet_interpretable"] = (V["OFF_precondition_met"] and V["Tdet_selected_OFF_positive"]
                               and V["Tdet_support_ok"] and not V["Tdet_uncalibrated"])
    V["Tdet_fires"] = (V["Tdet_interpretable"] and (m[f"{p}_w_T_det_lo"] > 0)
                       and (m[f"{p}_w_T_det"] > mx(f"{p}_w_T_det_q975")))
    V["DETNUM_concordant"] = finite(m.get(f"{p}_w_DETNUM_lo")) and m[f"{p}_w_DETNUM_lo"] > 0
    V["primary_matched_null_ci_fire_rate_max"] = mx(f"{p}_T1_ci_fire_rate")
    V["primary_uncalibrated"] = not (V["primary_matched_null_ci_fire_rate_max"] <= 0.10)
    V["estimates"] = {k: m.get(f"{p}_{k}") for k in (
        "w_T1", "w_T1_lo", "w_T1_hi", "w_T1_0", "w_T1_1", "w_T1_2", "p_T1", "w_T1day", "w_T2_W",
        "w_T20_W", "w_PA_det", "w_BIP", "w_T3", "w_T_det", "w_T_det_lo", "w_OFF", "w_OFF_lo",
        "w_DETNUM", "w_DETNUM_lo", "w_T_det_finite_frac", "n_pp_det")}
    V["estimates"]["lin_w_OFF_lo"] = m.get("lin_w_OFF_lo")

    # preregistered reading
    if not V["primary_finite"]:
        reading = ("not interpretable: a primary estimate, interval, threshold or matched-null summary is "
                   "non-finite (reported as a failure, not as a null)")
    elif V["primary_uncalibrated"]:
        reading = "primary statistic uncalibrated on the real marginals (matched-null firing > 10%): not interpreted"
    elif V["sign_test_uncalibrated"] and any(V["sign_test_items_below_null"]):
        reading = "an item shows negative excess, but the sign test is uncalibrated on the real marginals: not interpreted"
    elif V["B3_rank2_sign"]:
        reading = ("evidence against the declared restricted null (homogeneous F1+R) in the direction of rank-2 "
                   "shared persistence, under the model and measurement assumptions; not unique proof of F2; "
                   "T1 sign not read as item persistence")
    elif V["B2_within_T1_fires"]:
        reading = ("evidence against the declared F1 null under the model and measurement assumptions; not "
                   "separable among item-specific persistence, response anchoring, between-day loading drift and "
                   "heterogeneous rank-2 shared persistence (second factor at the shared rate)")
        if V["T1day_fires"]:
            reading += ("; T1day also fires (diagnostic only: no calibrated bound against drift rivals has "
                        "been established, so drift is not excluded)")
    else:
        reading = ("no detectable within-person item-specific or second-dimension persistence at this design's "
                   "power (Part A, corrected, N8-like: 0.98 at T1 = 0.25; 0.29 at T1 = 0.10); not evidence of "
                   "absence")
    if V["B2_within_T1_fires"] and V["primary_finite"] and not V["primary_uncalibrated"]:
        if not V["Tdet_interpretable"]:
            why = [r for r, bad in (("linear OFF precondition not met", not V["OFF_precondition_met"]),
                                    (f"selected-version ({p}) OFF interval not above 0", not V["Tdet_selected_OFF_positive"]),
                                    ("finiteness or support guard failed", not V["Tdet_support_ok"]),
                                    ("uncalibrated on the real marginals", V["Tdet_uncalibrated"])) if bad]
            reading += "; T_det withheld (" + "; ".join(why) + "): not interpreted"
        elif V["Tdet_fires"] and not V["DETNUM_concordant"]:
            reading += ("; T_det fires but the raw determinant numerator interval is not above 0: discordant, "
                        "not interpreted")
        elif V["Tdet_fires"]:
            reading += ("; T_det fires with a concordant raw numerator: evidence against the declared rank <= 2 "
                        "null under the model and measurement assumptions, so heterogeneous rank-2 F2 is not "
                        "supported as the sole source of T1 (anchoring and drift remain)")
        else:
            reading += ("; T_det does not fire: uninformative at its observed low power (13-17% at T1 = 0.25+ "
                        "under realistic nuisance, R-006b-H); rank 2 is not established")
    if not V["OFF_precondition_met"] and V["primary_finite"] and not V["primary_uncalibrated"]:
        V["diagnostic_unconditioned_reading"] = reading
        reading = ("positive-shared-lag precondition not met (linear OFF interval not above 0): T1, the sign "
                   "test and T_det are not read as evidence on F1+R versus F2. The unconditioned reading is "
                   "recorded only as a diagnostic.")
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
