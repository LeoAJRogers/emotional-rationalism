"""Rival forecasts for R-006 Part B, read off the Part A bench (results/bench_summary.json).
For each world: mean (SD) of the statistics Part B reports, and their firing rates.
Run: python rival_table.py -> results/rival_forecasts.md and .json. MIT licence.
"""
import json

ROWS = [
    ("N8", "F1 + heterogeneity + floors + MNAR (realistic null)"),
    ("N9", "same, loading log-SD 0.5 (held out)"),
    ("W1w+N8", "item persistence, T1_j = 0.10, realistic nuisance"),
    ("W1s+N8", "item persistence, T1_j = 0.25, realistic nuisance"),
    ("W2s+N8", "second NA factor, slower, realistic nuisance"),
    ("W2e+N8", "second NA factor, same rate, realistic nuisance"),
    ("N6", "between-day loading drift (Gaussian)"),
    ("N7", "response anchoring 0.15 (Gaussian)"),
    ("N4", "momentary method factor (Gaussian)"),
    ("W3", "one NA dimension, two timescales (Gaussian)"),
]


def pick(s, w, base):
    """Corrected statistic if the world is ordinal, linear otherwise."""
    for tag in ("cor", "lin"):
        if f"{tag}_{base}_mean" in s[w]:
            return tag
    raise KeyError(base)


def main():
    with open("results/bench_summary.json") as fh:
        s = json.load(fh)
    out, lines = {}, []
    hdr = ("| World | Description | within T1 | fires | T1_fearful < 0 | T2 fires | T2₀ fires | "
           "pooled T1 | pooled − within | T1day fires |")
    lines += [hdr, "|" + " --- |" * 10]
    for w, desc in ROWS:
        tag = pick(s, w, "w_T1")
        g = s[w]
        rec = dict(
            within_T1=(g[f"{tag}_w_T1_mean"], g[f"{tag}_w_T1_sd"]),
            within_T1_fire=g[f"{tag}_w_T1_pos_rate"],
            T1_fearful_neg=g[f"{tag}_w_T1_1_neg_rate"],
            T2_fire=g[f"{tag}_w_T2_W_fire_rate"],
            T20_fire=g[f"{tag}_w_T20_W_fire_rate"],
            pooled_T1=(g[f"{tag}_p_T1_mean"], g[f"{tag}_p_T1_sd"]),
            pooled_minus_within=g[f"{tag}_p_T1_mean"] - g[f"{tag}_w_T1_mean"],
            T1day_fire=g[f"{tag}_w_T1day_pos_rate"],
            stat_version=tag,
        )
        out[w] = rec
        lines.append(
            f"| {w} | {desc} | {rec['within_T1'][0]:+.3f} ({rec['within_T1'][1]:.3f}) | "
            f"{rec['within_T1_fire']:.2f} | {rec['T1_fearful_neg']:.2f} | {rec['T2_fire']:.2f} | "
            f"{rec['T20_fire']:.2f} | {rec['pooled_T1'][0]:+.3f} ({rec['pooled_T1'][1]:.3f}) | "
            f"{rec['pooled_minus_within']:+.3f} | {rec['T1day_fire']:.2f} |")
    with open("results/rival_forecasts.json", "w") as fh:
        json.dump(out, fh, indent=1)
    with open("results/rival_forecasts.md", "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
