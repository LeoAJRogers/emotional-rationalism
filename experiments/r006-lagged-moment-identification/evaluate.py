"""Score R-006 Part A predictions mechanically from results/bench_summary.json and
results/equivalences.json. Written before the bench results were seen.
Run: python evaluate.py -> results/partA_verdicts.json and a printed table. MIT licence.
"""
import json
import subprocess
import sys


def load():
    with open("results/bench_summary.json") as fh:
        s = json.load(fh)
    with open("results/equivalences.json") as fh:
        e = json.load(fh)
    return s, e


def rate(s, world, key):
    return s[world][key + "_rate"]


def mean(s, world, key):
    return s[world][key + "_mean"]


def main():
    s, e = load()
    tests = subprocess.run([sys.executable, "test_lagmom.py"], capture_output=True, text=True)
    V = {}

    def rec(pid, held, **numbers):
        V[pid] = dict(held=bool(held), **{k: round(v, 4) if isinstance(v, float) else v
                                          for k, v in numbers.items()})

    rec("A1", tests.returncode == 0 and e["E1_max_abs_diff"] < 1e-10 and e["E2_max_abs_diff"] < 1e-10
        and e["E3a_sign_identity_max_abs_diff"] < 1e-10
        and e["E3a_random_rank2_all_excess_positive"].startswith("0/")
        and e["E3_degenerate_max_abs_diff"] < 1e-10 and e["E3b_max_abs_diff"] < 1e-10
        and e["E4_max_abs_obs_diff"] < 1e-10, unit_tests_exit=tests.returncode)

    w_in, p_n1 = rate(s, "N1", "lin_w_T1_pos"), rate(s, "N1", "lin_p_T1_pos")
    rec("A2", w_in <= 0.10 and p_n1 >= 0.40, within_part=w_in <= 0.10, pooled_part=p_n1 >= 0.40,
        N1_within_T1_rate=w_in, N1_pooled_T1_rate=p_n1,
        N1_within_T1_mean=mean(s, "N1", "lin_w_T1"), N1_pooled_T1_mean=mean(s, "N1", "lin_p_T1"))

    a3 = {k: rate(s, "N2", k) for k in ("lin_w_T1_pos", "lin_p_T1_pos", "lin_w_T2_W_fire", "lin_p_T2_W_fire")}
    rec("A3", all(v <= 0.10 for v in a3.values()), **{"N2_" + k: v for k, v in a3.items()})

    a4 = {f"{w}_{k}": rate(s, w, k) for w in ("N4", "N5") for k in ("lin_w_T1_pos", "lin_w_T2_W_fire")}
    t20 = rate(s, "N4", "lin_w_T20_W_fire")
    rec("A4", all(v <= 0.10 for v in a4.values()) and t20 >= 0.80, N4_T20_rate=t20, **a4)

    lin_m, cor_m = mean(s, "N3h", "lin_w_T1"), mean(s, "N3h", "cor_w_T1")
    lin_r, cor_r = rate(s, "N3h", "lin_w_T1_pos"), rate(s, "N3h", "cor_w_T1_pos")
    rec("A5", lin_m >= 0.03 and lin_r > 0.10 and cor_m <= 0.5 * lin_m and cor_r <= 0.10,
        N3h_lin_mean=lin_m, N3h_lin_rate=lin_r, N3h_cor_mean=cor_m, N3h_cor_rate=cor_r)

    a6 = dict(W1s_T1=rate(s, "W1s", "lin_w_T1_pos"), W1w_T1=rate(s, "W1w", "lin_w_T1_pos"),
              W2s_T2=rate(s, "W2s", "lin_w_T2_W_fire"), W2f_T2=rate(s, "W2f", "lin_w_T2_W_fire"),
              W1s_T2=rate(s, "W1s", "lin_w_T2_W_fire"))
    parts6 = dict(W1s_T1=a6["W1s_T1"] >= 0.80, W1w_T1=a6["W1w_T1"] >= 0.25, W2s_T2=a6["W2s_T2"] >= 0.60,
                  W2f_T2=a6["W2f_T2"] < 0.40, W1s_T2=a6["W1s_T2"] <= 0.10)
    rec("A6", all(parts6.values()), **{k + "_rate": v for k, v in a6.items()},
        **{k + "_held": v for k, v in parts6.items()})

    t2e, neg = rate(s, "W2e", "lin_w_T2_W_fire"), rate(s, "W2e", "lin_w_T1_1_neg")
    rec("A7", t2e <= 0.10 and neg >= 0.50, W2e_T2_rate=t2e, W2e_T1fearful_neg_rate=neg)

    fp, pw = rate(s, "N8", "cor_w_T1_pos"), rate(s, "W1s+N8", "cor_w_T1_pos")
    rec("A8", fp <= 0.10 and pw >= 0.60, N8_cor_T1_rate=fp, W1sN8_cor_T1_rate=pw,
        gate_feasibility_failure=bool(fp > 0.10 or pw < 0.50))

    n6a, n6d, n7 = rate(s, "N6", "lin_w_T1_pos"), rate(s, "N6", "lin_w_T1day_pos"), rate(s, "N7", "lin_w_T1_pos")
    rec("A9", n6a >= 0.15 and n6d <= 0.10 and n7 >= 0.80, N6_all_rate=n6a, N6_day_rate=n6d, N7_rate=n7)

    w3, n2p, n2w = rate(s, "W3", "lin_w_T3_pos"), rate(s, "N2", "lin_p_T3_pos"), rate(s, "N2", "lin_w_T3_pos")
    rec("A10", w3 < 0.50 and n2p >= n2w, W3_T3_rate=w3, N2_pooled_T3_rate=n2p, N2_within_T3_rate=n2w)

    b0, b0b = rate(s, "W0", "lin_w_BIP_pos"), rate(s, "W0b", "lin_w_BIP_pos")
    rec("A11", b0 >= 0.80 and b0b <= 0.10, W0_rate=b0, W0b_rate=b0b)

    with open("results/partA_verdicts.json", "w") as fh:
        json.dump(V, fh, indent=1)
    for k, v in V.items():
        print(k, "HELD" if v["held"] else "FAILED", {kk: vv for kk, vv in v.items() if kk != "held"})


if __name__ == "__main__":
    main()
