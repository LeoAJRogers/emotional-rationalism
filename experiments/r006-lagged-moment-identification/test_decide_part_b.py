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
                     f"{t}_w_T1day_lo": -0.01, f"{t}_w_T2_W": 1.0, f"{t}_w_T20_W": 1.0, f"{t}_w_BIP_lo": -0.1,
                     f"{t}_w_PA_det": 0.0, f"{t}_w_PA_det_lo": -0.1, f"{t}_w_T_det": 0.05,
                     f"{t}_w_T_det_lo": -0.2, f"{t}_w_OFF": 0.002, f"{t}_w_OFF_lo": 0.0005,
                     f"{t}_w_DETNUM": 0.0001, f"{t}_w_DETNUM_lo": -0.0001, f"{t}_w_T_det_finite_frac": 1.0,
                     f"{t}_n_pp_det": 120})
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
    assert not V["Tdet_fires"]
    assert "evidence against the declared F1 null" in V["reading"]
    assert "uninformative" in V["reading"]
    assert "diagnostic_unconditioned_reading" not in V


def test_tdet_fires_concordant():
    V = run(set_main(cor_w_T_det=0.6, cor_w_T_det_lo=0.1, cor_w_DETNUM_lo=0.00002))
    assert V["Tdet_fires"] and V["DETNUM_concordant"]
    assert "concordant raw numerator" in V["reading"]


def test_tdet_fires_discordant_raw_numerator_is_not_interpreted():
    V = run(set_main(cor_w_T_det=0.6, cor_w_T_det_lo=0.1, cor_w_DETNUM_lo=-0.00001))
    assert V["Tdet_fires"] and not V["DETNUM_concordant"]
    assert "discordant, not interpreted" in V["reading"]


def test_linear_off_gate_failure_withholds_tdet_and_demotes_unconditioned_reading():
    V = run(set_main(lin_w_OFF_lo=-0.001, cor_w_T_det=0.6, cor_w_T_det_lo=0.1, cor_w_DETNUM_lo=0.1))
    assert not V["OFF_precondition_met"] and not V["Tdet_interpretable"] and not V["Tdet_fires"]
    assert V["reading"].startswith("positive-shared-lag precondition not met")
    assert "T_det withheld" in V["diagnostic_unconditioned_reading"]
    assert "concordant" not in V["reading"]


def test_selected_version_off_not_positive_withholds_tdet_even_if_linear_off_positive():
    V = run(set_main(cor_w_OFF_lo=-0.0001, cor_w_T_det=0.6, cor_w_T_det_lo=0.1))
    assert V["OFF_precondition_met"] and not V["Tdet_selected_OFF_positive"]
    assert not V["Tdet_fires"]
    assert "selected-version (cor) OFF interval not above 0" in V["reading"]


def test_nonfinite_tdet_and_low_support_withhold_tdet():
    for mod in (set_main(cor_w_T_det=math.inf), set_main(cor_w_T_det_lo=NAN),
                set_main(cor_w_T_det_finite_frac=0.9), set_main(cor_n_pp_det=10),
                set_null(cor_w_T_det_q975=NAN), set_null(cor_Tdet_nonfinite_rate=0.2)):
        V = run(mod)
        assert not V["Tdet_support_ok"] and not V["Tdet_fires"]
        assert "finiteness or support guard failed" in V["reading"]


def test_missing_r006c_keys_withhold_tdet():
    def drop(o):
        for k in ("cor_w_DETNUM_lo", "cor_w_T_det_finite_frac", "cor_n_pp_det"):
            o["main"].pop(k)
    V = run(drop)
    assert not V["Tdet_support_ok"] and "T_det withheld" in V["reading"]


def test_nonfinite_primary_is_not_interpretable_not_null():
    for mod in (set_main(cor_w_T1=NAN), set_null(cor_w_T1_q975=math.inf), set_null(cor_T1_ci_fire_rate=NAN)):
        V = run(mod)
        assert not V["primary_finite"] and not V["B2_within_T1_fires"]
        assert V["reading"].startswith("not interpretable")
        assert "no detectable" not in V["reading"]


def test_t1day_is_diagnostic_and_never_excludes_drift():
    V = run(set_main(cor_w_T1day_lo=0.05))
    assert V["T1day_fires"]
    assert "drift is not excluded" in V["reading"] and "excluded at tested power" not in V["reading"]


def test_uncalibrated_tdet_withheld():
    V = run(set_null(cor_Tdet_ci_fire_rate=0.2))
    assert V["Tdet_uncalibrated"] and "uncalibrated on the real marginals" in V["reading"]


def test_uncalibrated_primary_and_nan_ratio_fallback():
    V = run(set_null(cor_T1_ci_fire_rate=0.2))
    assert V["reading"].startswith("primary statistic uncalibrated")
    V = run(set_null(cor_w_T1_sd=NAN))
    assert V["primary_version"] == "lin"


def test_rank2_sign_wording():
    def neg(o):
        o["main"].update(cor_w_T1_0=-0.3, cor_w_T1_0_hi3=-0.05)
    V = run(neg)
    assert V["B3_rank2_sign"]
    assert "not unique proof of F2" in V["reading"]


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
