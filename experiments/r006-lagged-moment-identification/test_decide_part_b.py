"""Unit tests for decide_part_b.decide on constructed result dictionaries (R-006c, 2026-11-26).

No data are used: every input below is a hand-built dictionary of statistics. MIT licence.
Run: python -m pytest test_decide_part_b.py   (or: python test_decide_part_b.py)
"""
import copy
import math

import decide_part_b as dp

NAN = float("nan")


def base():
    """A calibrated, finite configuration in which T1 fires within-person, OFF is positive in both
    versions, and T_det does not fire."""
    main, null = {}, {}
    for t in ("cor", "lin"):
        main.update({f"{t}_w_T1": 0.30, f"{t}_w_T1_lo": 0.10, f"{t}_w_T1_hi": 0.5, f"{t}_p_T1": 0.35,
                     f"{t}_w_T1day": 0.02, f"{t}_w_T1day_lo": -0.01, f"{t}_w_T1day_hi": 0.05,
                     f"{t}_w_T2_W": 1.0, f"{t}_w_T20_W": 1.0,
                     f"{t}_w_BIP": 0.0, f"{t}_w_BIP_lo": -0.1, f"{t}_w_BIP_hi": 0.1,
                     f"{t}_w_PA_det": 0.0, f"{t}_w_PA_det_lo": -0.1, f"{t}_w_PA_det_hi": 0.1,
                     f"{t}_w_T_det": 0.05, f"{t}_w_T_det_lo": -0.2, f"{t}_w_T_det_hi": 0.3,
                     f"{t}_w_OFF": 0.002, f"{t}_w_OFF_lo": 0.0005, f"{t}_w_OFF_hi": 0.004,
                     f"{t}_w_DETNUM": 0.0001, f"{t}_w_DETNUM_lo": -0.0001, f"{t}_w_DETNUM_hi": 0.0003,
                     f"{t}_w_T_det_finite_frac": 1.0, f"{t}_n_pp_det": 120, f"{t}_n_persons_det": 100,
                     f"{t}_mean_days_det": 5.5, f"{t}_jk_fallback_frac_det": 0.02})
        for j in range(3):
            main.update({f"{t}_w_T1_{j}": 0.3, f"{t}_w_T1_{j}_hi3": 0.5})
        null.update({f"{t}_w_T1_sd": 0.05, f"{t}_w_T1_q975": 0.08, f"{t}_T1_ci_fire_rate": 0.03,
                     f"{t}_anyneg3_rate": 0.02, f"{t}_w_T2_W_q95": 6.5, f"{t}_w_T20_W_q95": 6.5,
                     f"{t}_w_PA_det_q975": 0.1, f"{t}_p_T1_q025": -0.1, f"{t}_p_T1_q975": 0.1,
                     f"{t}_w_T_det_q975": 0.3, f"{t}_Tdet_ci_fire_rate": 0.04, f"{t}_Tdet_nonfinite_rate": 0.0})
        for j in range(3):
            null[f"{t}_w_T1_{j}_q025"] = -0.1
    return {"main": main, "matched_null": {"0.4": dict(null), "0.55": dict(null), "0.7": dict(null)}}


def run(mod=None):
    o = base()
    if mod:
        mod(o)
    return dp.decide(o)


def set_main(**kw):
    def f(o):
        o["main"].update(kw)
    return f


def set_null(**kw):
    def f(o):
        for d in o["matched_null"].values():
            d.update(kw)
    return f


def test_base_reads_as_restricted_null_evidence_and_tdet_uninformative():
    V = run()
    assert V["primary_version"] == "cor" and V["B2_within_T1_fires"] and V["Tdet_interpretable"]
    assert V["calibration_problems"] == []
    assert not V["Tdet_fires"]
    assert "evidence against the declared F1 null" in V["reading"]
    assert "uninformative" in V["reading"]
    assert "diagnostic_unconditioned_reading" not in V


def test_tdet_fires_concordant():
    V = run(set_main(cor_w_T_det=0.6, cor_w_T_det_lo=0.1, cor_w_T_det_hi=0.9, cor_w_DETNUM_lo=0.00002))
    assert V["Tdet_fires"] and V["DETNUM_status"] == "fires" and V["Tdet_raw_threshold_status"] == "fires"
    assert "concordant raw numerator" in V["reading"]


def test_tdet_fires_discordant_raw_numerator_is_not_interpreted():
    V = run(set_main(cor_w_T_det=0.6, cor_w_T_det_lo=0.1, cor_w_T_det_hi=0.9, cor_w_DETNUM_lo=-0.00001))
    assert V["Tdet_raw_threshold_status"] == "fires" and not V["Tdet_fires"] and V["DETNUM_status"] == "no_fire"
    assert "discordant, not interpreted" in V["reading"]


def test_linear_off_gate_failure_withholds_tdet_and_demotes_unconditioned_reading():
    V = run(set_main(lin_w_OFF_lo=-0.001, cor_w_T_det=0.6, cor_w_T_det_lo=0.1, cor_w_T_det_hi=0.9, cor_w_DETNUM_lo=0.00002))
    assert not V["OFF_precondition_met"] and not V["Tdet_interpretable"] and not V["Tdet_fires"]
    assert V["reading"].startswith("positive-shared-lag precondition not met")
    assert "T_det withheld" in V["diagnostic_unconditioned_reading"]
    assert "raw threshold crossed" in V["diagnostic_unconditioned_reading"]
    assert "concordant" not in V["reading"]


def test_selected_version_off_not_positive_withholds_tdet_even_if_linear_off_positive():
    V = run(set_main(cor_w_OFF_lo=-0.0001, cor_w_T_det=0.6, cor_w_T_det_lo=0.1, cor_w_T_det_hi=0.9))
    assert V["OFF_precondition_met"] and V["Tdet_selected_OFF_status"] == "no_fire"
    assert not V["Tdet_fires"]
    assert "selected-version (cor) OFF interval not above 0" in V["reading"]


def test_nonfinite_tdet_and_low_support_withhold_tdet():
    for mod in (set_main(cor_w_T_det=math.inf), set_main(cor_w_T_det_lo=NAN),
                set_main(cor_w_T_det_finite_frac=0.9), set_main(cor_n_pp_det=10),
                set_main(cor_n_persons_det=12), set_main(cor_mean_days_det=3.0),
                set_main(cor_jk_fallback_frac_det=0.3),
                set_null(cor_w_T_det_q975=NAN), set_null(cor_Tdet_nonfinite_rate=0.2)):
        V = run(mod)
        assert not V["Tdet_interpretable"] and not V["Tdet_fires"]
        assert "T_det withheld" in V["reading"]


def test_missing_r006c_keys_withhold_tdet():
    def drop(o):
        for k in ("cor_w_DETNUM_lo", "cor_w_T_det_finite_frac", "cor_n_pp_det"):
            o["main"].pop(k)
    V = run(drop)
    assert not V["Tdet_support_ok"] and "T_det withheld" in V["reading"]
    assert V["DETNUM_status"] == "invalid"


def test_nonfinite_primary_is_not_interpretable_not_null():
    for mod in (set_main(cor_w_T1=NAN), set_null(cor_w_T1_q975=math.inf), set_null(cor_T1_ci_fire_rate=NAN)):
        V = run(mod)
        assert not V["primary_valid"] and not V["B2_within_T1_fires"] and V["B2_status"] == "invalid"
        assert V["reading"].startswith("not interpretable")
        assert "no detectable" not in V["reading"]


def test_t1day_is_diagnostic_and_never_excludes_drift():
    V = run(set_main(cor_w_T1day_lo=0.05))
    assert V["T1day_fires"]
    assert "drift is not excluded" in V["reading"] and "excluded at tested power" not in V["reading"]


def test_uncalibrated_tdet_withheld():
    V = run(set_null(cor_Tdet_ci_fire_rate=0.2))
    assert V["Tdet_uncalibrated"] and "uncalibrated on the real marginals" in V["reading"]


def test_uncalibrated_primary():
    V = run(set_null(cor_T1_ci_fire_rate=0.2))
    assert V["reading"].startswith("primary statistic uncalibrated")


def test_rank2_sign_wording():
    def neg(o):
        o["main"].update(cor_w_T1_0=-0.3, cor_w_T1_0_hi3=-0.05)
    V = run(neg)
    assert V["B3_rank2_sign"]
    assert "not unique proof of F2" in V["reading"]


# ---------------------------------------------------------------- R-006c revision tests (GPT-6.2, ed90ec9)
def set_phi(phi, **kw):
    def f(o):
        o["matched_null"][phi].update(kw)
    return f


def test_invalid_value_at_first_and_last_phi_is_not_masked():
    for phi in ("0.4", "0.7"):                          # sorted order: first and last
        for k in ("cor_w_T1_q975", "cor_T1_ci_fire_rate"):
            V = run(set_phi(phi, **{k: NAN}))
            assert not V["primary_valid"] and V["reading"].startswith("not interpretable"), (phi, k)
        V = run(set_phi(phi, cor_w_T_det_q975=NAN))
        assert not V["Tdet_interpretable"] and "matched-null T_det threshold invalid" in V["Tdet_failed_gates"]
        def drop(o, phi=phi):
            o["matched_null"][phi].pop("cor_Tdet_ci_fire_rate")
        V = run(drop)
        assert V["Tdet_uncalibrated"] and not V["Tdet_interpretable"]


def test_python_max_nan_masking_is_handled():
    assert max([0.02, NAN]) == 0.02                      # the pitfall GPT-6.2 identified
    V = run(set_phi("0.7", cor_Tdet_nonfinite_rate=NAN))
    assert not V["Tdet_interpretable"]
    assert "matched-null non-finite T_det rate above 0.05 or invalid" in V["Tdet_failed_gates"]


def test_missing_or_all_missing_nonfinite_rate_fails_closed():
    def drop_all(o):
        for d in o["matched_null"].values():
            d.pop("cor_Tdet_nonfinite_rate")
    for mod in (drop_all, set_null(cor_Tdet_nonfinite_rate=NAN), set_null(cor_Tdet_nonfinite_rate=-0.1),
                set_null(cor_Tdet_nonfinite_rate=1.5)):
        V = run(mod)
        assert not V["Tdet_interpretable"] and not V["Tdet_fires"]


def test_nonfinite_rate_exactly_five_percent_passes_and_above_fails():
    V = run(set_null(cor_Tdet_nonfinite_rate=0.05))
    assert V["Tdet_interpretable"]
    V = run(set_null(cor_Tdet_nonfinite_rate=0.0500001))
    assert not V["Tdet_interpretable"]


def test_infinite_off_never_passes_either_gate():
    V = run(set_main(lin_w_OFF_lo=math.inf, lin_w_OFF_hi=math.inf))
    assert V["OFF_precondition_status"] == "invalid" and not V["OFF_precondition_met"]
    assert V["reading"].startswith("positive-shared-lag precondition invalid")
    V = run(set_main(cor_w_OFF_lo=math.inf))
    assert V["Tdet_selected_OFF_status"] == "invalid" and not V["Tdet_interpretable"]


def test_invalid_upper_endpoints_and_misordered_intervals():
    for mod in (set_main(cor_w_T1_hi=NAN), set_main(cor_w_T1_hi=0.05)):      # NaN; hi < lo
        V = run(mod)
        assert V["B2_status"] == "invalid" and V["reading"].startswith("not interpretable")
    V = run(set_main(cor_w_T_det_hi=NAN, cor_w_T_det=0.6, cor_w_T_det_lo=0.1))
    assert V["Tdet_raw_threshold_status"] == "invalid" and not V["Tdet_fires"]
    V = run(set_main(lin_w_OFF_hi=0.0001))                                  # hi < lo
    assert V["OFF_precondition_status"] == "invalid"
    V = run(set_main(cor_w_DETNUM_hi=NAN, cor_w_T_det=0.6, cor_w_T_det_lo=0.1, cor_w_T_det_hi=0.9,
                     cor_w_DETNUM_lo=0.00002))
    assert V["DETNUM_status"] == "invalid" and not V["Tdet_fires"] and "discordant" in V["reading"]


def test_infinite_statistic_cannot_fire():
    V = run(set_main(cor_w_T_det=math.inf, cor_w_T_det_lo=0.1, cor_w_T_det_hi=math.inf, cor_w_DETNUM_lo=0.1))
    assert V["Tdet_raw_threshold_status"] == "invalid" and not V["Tdet_fires"]
    V = run(set_main(cor_w_T2_W=math.inf))
    assert V["B4_T2_status"] == "invalid"
    V = run(set_main(cor_w_T1=math.inf, cor_w_T1_hi=math.inf))
    assert V["B2_status"] == "invalid" and not V["B2_within_T1_fires"]


def test_invalid_sd_ratio_fails_closed_instead_of_selecting_lin():
    for mod in (set_null(cor_w_T1_sd=NAN), set_phi("0.7", lin_w_T1_sd=NAN), set_null(lin_w_T1_sd=0.0)):
        V = run(mod)
        assert not V["selection_valid"] and V["primary_version"] is None
        assert V["reading"].startswith("not interpretable: the version-selection calibration")


def test_empty_calibration_set_is_invalid():
    def empty(o):
        o["matched_null"] = {}
    V = run(empty)
    assert not V["selection_valid"] and "matched-null calibration set is empty" in V["calibration_problems"]
    assert V["reading"].startswith("not interpretable")


def test_auxiliary_flags_report_invalid_not_nonfire():
    V = run(set_main(cor_w_BIP_hi=NAN))
    assert V["B6_BIP_status"] == "invalid"
    V = run(set_null(cor_w_T20_W_q95=NAN))
    assert V["B5_T20_status"] == "invalid"
    V = run(set_main(cor_w_PA_det_lo=NAN))
    assert V["B7_PAdet_status"] == "invalid"
    V = run(set_main(cor_w_T1day_hi=NAN))
    assert V["T1day_status"] == "invalid" and "T1day invalid" in V["reading"]
    V = run(set_phi("0.4", cor_w_T1_1_q025=NAN))
    assert V["B3_rank2_sign_status"] == "invalid"
    assert V["reading"].startswith("the sign test's inputs or calibration are missing")


def test_raw_threshold_fire_reported_separately_when_withheld():
    V = run(set_main(cor_w_T_det=0.6, cor_w_T_det_lo=0.1, cor_w_T_det_hi=0.9, cor_w_DETNUM_lo=0.00002,
                     cor_n_persons_det=5))
    assert V["Tdet_raw_threshold_status"] == "fires" and not V["Tdet_interpretable_concordant_fire"]
    assert "fewer than 30 distinct persons" in V["Tdet_failed_gates"]
    assert "raw threshold crossed" in V["reading"]


if __name__ == "__main__":
    import sys
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print("PASS", t.__name__)
        except AssertionError as e:                       # noqa: PERF203
            failed += 1
            print("FAIL", t.__name__, e)
    print(f"{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
