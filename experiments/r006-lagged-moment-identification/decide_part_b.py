"""Apply the preregistered R-006 Part B decision rules (register addendum) mechanically to
results/real_0010_partB.json. Written before any 0010 item data were accessed. MIT licence.
Run: python decide_part_b.py -> results/real_0010_partB_verdicts.json
"""
import json

WALD = 5.991


def main(path="results/real_0010_partB.json"):
    o = json.load(open(path))
    m, nl = o["main"], o["matched_null"]
    phis = sorted(nl)
    mx = lambda k: max(nl[p][k] for p in phis)                      # most conservative over phi
    mn_ = lambda k: min(nl[p][k] for p in phis)
    ratio = mx("cor_w_T1_sd") / mx("lin_w_T1_sd")
    p = "cor" if ratio <= 1.5 else "lin"
    thr = mx(f"{p}_w_T1_q975")
    V = dict(primary_version=p, sd_ratio_cor_over_lin=ratio, primary_threshold=thr)
    V["B1_heterogeneity"] = (m[f"{p}_p_T1"] - m[f"{p}_w_T1"]) >= 0.10
    V["B2_within_T1_fires"] = (m[f"{p}_w_T1_lo"] > 0) and (m[f"{p}_w_T1"] > thr)
    V["sign_test_items_below_null"] = [bool(m[f"{p}_w_T1_{j}_hi3"] < 0 and m[f"{p}_w_T1_{j}"] < mn_(f"{p}_w_T1_{j}_q025"))
                                       for j in range(3)]
    V["sign_test_uncalibrated"] = mx(f"{p}_anyneg3_rate") > 0.10
    V["B3_rank2_sign"] = any(V["sign_test_items_below_null"]) and not V["sign_test_uncalibrated"]
    V["B4_T2_fires"] = (m[f"{p}_w_T2_W"] > WALD) and (m[f"{p}_w_T2_W"] > mx(f"{p}_w_T2_W_q95"))
    V["B5_T20_fires"] = (m[f"{p}_w_T20_W"] > WALD) and (m[f"{p}_w_T20_W"] > mx(f"{p}_w_T20_W_q95"))
    V["B6_BIP_fires"] = m[f"{p}_w_BIP_lo"] > 0
    V["B7_PAdet_fires"] = (m[f"{p}_w_PA_det_lo"] > 0) and (m[f"{p}_w_PA_det"] > mx(f"{p}_w_PA_det_q975"))
    V["B8_pooled_within_null_range"] = mn_(f"{p}_p_T1_q025") <= m[f"{p}_p_T1"] <= mx(f"{p}_p_T1_q975")
    V["T1day_fires"] = m[f"{p}_w_T1day_lo"] > 0
    V["primary_matched_null_ci_fire_rate_max"] = mx(f"{p}_T1_ci_fire_rate")
    V["primary_uncalibrated"] = V["primary_matched_null_ci_fire_rate_max"] > 0.10
    V["estimates"] = {k: m[f"{p}_{k}"] for k in (
        "w_T1", "w_T1_lo", "w_T1_hi", "w_T1_0", "w_T1_1", "w_T1_2", "p_T1", "w_T1day", "w_T2_W",
        "w_T20_W", "w_PA_det", "w_BIP", "w_T3")}
    # preregistered reading
    if V["primary_uncalibrated"]:
        reading = "primary statistic uncalibrated on the real marginals (matched-null firing > 10%): not interpreted"
    elif V["sign_test_uncalibrated"] and any(V["sign_test_items_below_null"]):
        reading = "an item shows negative excess, but the sign test is uncalibrated on the real marginals: not interpreted"
    elif V["B3_rank2_sign"]:
        reading = "rank-2 shared persistence in NA (F1+R excluded for the configuration); T1 sign not read as item persistence"
    elif V["B2_within_T1_fires"] and V["T1day_fires"]:
        reading = "item-specific persistence OR response anchoring (between-day loading drift excluded at tested power)"
    elif V["B2_within_T1_fires"]:
        reading = "item-specific persistence OR response anchoring OR between-day loading drift (not separable)"
    else:
        reading = ("no detectable within-person item-specific or second-dimension persistence at this "
                   "design's power (Part A, corrected, N8-like: 0.98 at T1 = 0.25; 0.29 at T1 = 0.10)")
    V["reading"] = reading
    json.dump(V, open("results/real_0010_partB_verdicts.json", "w"), indent=1, default=float)
    print(json.dumps(V, indent=1, default=float))


if __name__ == "__main__":
    main()
