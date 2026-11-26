"""Check (within quoted rounding; x.x5 values may be quoted either way) that numbers quoted in the R-006 register entry, the pass report and the CHANGELOG
match the committed result files (rounded as quoted). Run: python verify_quoted_numbers.py"""
import gzip
import json
import sys

s = json.load(open("results/bench_summary.json"))
x = json.load(open("results/explore_variants.json"))
st = json.load(open("results/check_signtest.json"))
mn = json.load(open("results/check_matched_null.json"))
eq = json.load(open("results/equivalences.json"))
fails = []


def q(label, value, quoted, tol):
    ok = abs(value - quoted) <= tol
    print(("ok   " if ok else "FAIL ") + f"{label}: file {value:.4f} vs quoted {quoted}")
    if not ok:
        fails.append(label)


r = lambda w, k: s[w][k + "_rate"]
m = lambda w, k: s[w][k + "_mean"]
# Part A table
q("N1 within T1 rate", r("N1", "lin_w_T1_pos"), 0.03, 0.005)
q("N1 pooled T1 rate", r("N1", "lin_p_T1_pos"), 0.99, 0.005)
q("N1 within mean", m("N1", "lin_w_T1"), -0.003, 0.0005)
q("N1 pooled mean", m("N1", "lin_p_T1"), 0.090, 0.0005)
q("E1 implied", eq["E1_implied_relative_excess_at_logSD_0.3"], 0.094, 0.0005)
for k, v in (("lin_w_T1_pos", .04), ("lin_p_T1_pos", .045), ("lin_w_T2_W_fire", .055), ("lin_p_T2_W_fire", .05)):
    q("N2 " + k, r("N2", k), v, 0.0026)
q("N4 T1", r("N4", "lin_w_T1_pos"), 0.015, 0.0026)
q("N4 T2", r("N4", "lin_w_T2_W_fire"), 0.065, 0.0026)
q("N4 T20", r("N4", "lin_w_T20_W_fire"), 1.0, 0.0026)
q("N5 T1", r("N5", "lin_w_T1_pos"), 0.02, 0.0026)
q("N5 T2", r("N5", "lin_w_T2_W_fire"), 0.05, 0.0026)
q("N3h lin mean", m("N3h", "lin_w_T1"), 0.014, 0.0006)
q("N3h lin rate", r("N3h", "lin_w_T1_pos"), 0.025, 0.0026)
q("N3h cor mean", m("N3h", "cor_w_T1"), -0.026, 0.0006)
q("N3h cor rate", r("N3h", "cor_w_T1_pos"), 0.01, 0.0026)
q("W1s T1", r("W1s", "lin_w_T1_pos"), 1.0, 0.0026)
q("W1w T1", r("W1w", "lin_w_T1_pos"), 0.995, 0.0026)
q("W2f T2", r("W2f", "lin_w_T2_W_fire"), 0.045, 0.0026)
q("W1s T2", r("W1s", "lin_w_T2_W_fire"), 0.045, 0.0026)
q("W2s T2", r("W2s", "lin_w_T2_W_fire"), 0.275, 0.0026)
q("W2e T2", r("W2e", "lin_w_T2_W_fire"), 0.065, 0.0026)
q("W2e F<0", r("W2e", "lin_w_T1_1_neg"), 0.975, 0.0026)
q("N8 cor T1", r("N8", "cor_w_T1_pos"), 0.015, 0.0026)
q("W1s+N8 cor T1", r("W1s+N8", "cor_w_T1_pos"), 0.98, 0.0026)
q("N6 all", r("N6", "lin_w_T1_pos"), 0.95, 0.0026)
q("N6 day", r("N6", "lin_w_T1day_pos"), 0.06, 0.0026)
q("N7", r("N7", "lin_w_T1_pos"), 1.0, 0.0026)
q("W3 T3", r("W3", "lin_w_T3_pos"), 0.255, 0.0026)
q("N2 pooled T3", r("N2", "lin_p_T3_pos"), 0.045, 0.0026)
q("N2 within T3", r("N2", "lin_w_T3_pos"), 0.02, 0.0026)
q("W0 BIP", r("W0", "lin_w_BIP_pos"), 1.0, 0.0026)
q("W0b BIP", r("W0b", "lin_w_BIP_pos"), 0.02, 0.0026)
# decisions / unpredicted
for w, v in (("N3", .27), ("N3h", .69), ("N8", .39), ("N9", .48)):
    q(w + " pooled cor", m(w, "cor_p_T1"), v, 0.006)
q("W0 within SD", s["W0"]["lin_w_T1_sd"], 0.023, 0.0006)
q("N8 within SD", s["N8"]["cor_w_T1_sd"], 0.065, 0.0006)
q("W1w+N8 cor", r("W1w+N8", "cor_w_T1_pos"), 0.29, 0.0051)
q("W1w+N8 lin", r("W1w+N8", "lin_w_T1_pos"), 0.56, 0.0026)
q("N3h cor SD", s["N3h"]["cor_w_T1_sd"], 0.34, 0.0026)
q("N3h lin SD", s["N3h"]["lin_w_T1_sd"], 0.11, 0.0026)
q("W2s F<0", r("W2s", "lin_w_T1_1_neg"), 1.0, 0.0026)
q("W2s+N8 F<0", r("W2s+N8", "cor_w_T1_1_neg"), 0.73, 0.0051)
q("W2e+N8 F<0", r("W2e+N8", "cor_w_T1_1_neg"), 0.51, 0.0051)
q("W1s+N8 T1day", r("W1s+N8", "cor_w_T1day_pos"), 0.29, 0.0051)
q("W3 T30", r("W3", "lin_w_T30_pos"), 0.93, 0.0051)
q("W0b T30", r("W0b", "lin_w_T30_pos"), 0.95, 0.0026)
q("N4 T30", r("N4", "lin_w_T30_pos"), 0.26, 0.0051)
for w, v in (("N8", .40), ("N9", .49), ("W1w+N8", .44), ("W1s+N8", .47), ("W2s+N8", .60), ("W2e+N8", .52)):
    q(w + " pooled-within", m(w, "cor_p_T1") - m(w, "cor_w_T1"), v, 0.006)
# exploratory
q("jk-off N8", x["N8"]["cor_w_T1_mean"], -0.12, 0.006)
q("jk-off N3h", x["N3h"]["cor_w_T1_mean"], -0.23, 0.006)
q("sign Bonf N8", st["N8"]["cor_anyneg3"], 0.03, 0.005)
q("sign Bonf N9", st["N9"]["cor_anyneg3"], 0.04, 0.005)
q("sign Bonf W2s+N8", st["W2s+N8"]["cor_anyneg3"], 0.57, 0.005)
q("sign Bonf W2e+N8", st["W2e+N8"]["cor_anyneg3"], 0.30, 0.005)
q("fresh W1s+N8 T1", st["W1s+N8"]["cor_T1fire"], 0.95, 0.005)
q("matched null cor max", max(v["cor_fire"] for v in mn.values()), 0.02, 0.0001)
q("matched null lin max", max(v["lin_fire"] for v in mn.values()), 0.18, 0.0001)
q("matched null sign max", max(v["cor_anyneg3"] for v in mn.values()), 0.18, 0.0001)
# any-item sign test (95%) from the per-replicate table
rows = [l.strip().split(",") for l in gzip.open("results/bench_per_replicate.csv.gz", "rt")]
hdr = rows[0]
ix = {h: i for i, h in enumerate(hdr)}


def anyneg(world, version):
    rr = [x for x in rows[1:] if x[0] == world and x[3] == version]
    return sum(any(float(x[ix[f"w_T1_{j}_hi"]]) < 0 for j in range(3)) for x in rr) / len(rr)


q("any-item W2s+N8 (95%)", anyneg("W2s+N8", "cor"), 0.74, 0.006)
q("any-item W2e+N8 (95%)", anyneg("W2e+N8", "cor"), 0.51, 0.006)
q("any-item N8 (95%)", anyneg("N8", "cor"), 0.075, 0.001)
print("ALL QUOTED NUMBERS MATCH" if not fails else f"MISMATCHES: {fails}")
sys.exit(1 if fails else 0)
