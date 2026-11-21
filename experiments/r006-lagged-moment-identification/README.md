# R-006 (revised): within-person lagged-moment identification

**Status:**

- **Part A**, a synthetic bench, was preregistered and run: 9 of 11 predictions held, and the go/no-go gate passed.
- **Part B**, the real-data test, is preregistered and **not yet run**. It is waiting for the 0010 data file, because Zenodo cannot be reached from the analysis session.

- Predictions and outcomes: the [R-006 register entry](../../research-log/prediction-register.md).
- Definitions: [DESIGN.md](DESIGN.md).
- Narrative and interpretation: [the pass report](../../research-log/2026-11-21-claude-r006-pass.md).

## What it does

It tests R-006's question with restrictions on **within-person** lagged item covariances. Each rival family implies such restrictions:

- one shared persistent NA dimension;
- or item-specific persistence;
- or a second shared persistent dimension.

The restrictions hold whatever each person's loadings and inertia are. A pooled version of every statistic is computed alongside, and the difference between the two measures how much of an apparent effect is between-person heterogeneity.

## Files

| File | Role |
| --- | --- |
| `DESIGN.md` | Statistics, identification map E1–E5 (with E3 correction), worlds, limits |
| `lagmom.py` | Disjoint-pair U-statistics, day jackknife, ordinal (Hermite) correction, pooled analogs, person bootstrap |
| `simulate.py` | The 22 synthetic worlds, matched to 0010's design |
| `bench.py` | Part A bench (preregistered) |
| `evaluate.py` | Scores the Part A predictions mechanically (written before results were seen) |
| `rival_table.py` | Rival forecasts for Part B, read off the bench |
| `equivalences.py` | Exact checks of E1–E4 |
| `test_lagmom.py` | Unit tests: brute-force U-statistics, Hermite identity, jackknife, data loader |
| `explore_variants.py` | **Exploratory**, post-Part-A: day jackknife off |
| `check_signtest.py` | **Exploratory**, post-Part-A: Bonferroni per-item sign test on fresh seeds |
| `check_matched_null.py` | **Exploratory**, post-Part-A: calibration of the marginal-matched null |
| `matched_null.py` | F1 null that keeps each real person-period's missingness mask and item marginals |
| `real_data.py` | Part B runner for openESM 0010: SHA-256 check, structure, statistics, matched null, sensitivity analyses; aggregates only |
| `decide_part_b.py` | Applies the preregistered Part B rules mechanically (written before any data access) |
| `verify_quoted_numbers.py` | Checks every number quoted in the register, pass report and CHANGELOG against the result files |

**Results (`results/`):**

- `equivalences.json`
- `bench_summary.json`: means, SDs and firing rates for every world and statistic.
- `bench_per_replicate.csv.gz`: the decision-relevant statistics for each replicate.
- `partA_verdicts.json`
- `rival_forecasts.md` / `.json`
- The exploratory checks: `explore_variants.json`, `check_signtest.json`, `check_matched_null.json`.

The full raw bench output (`bench_raw.jsonl`, 31 MB) is not committed. `python bench.py` regenerates it from fixed seeds: bit-for-bit on numpy 2.5.3 and scipy 1.18.1, where it was run; other versions may differ in the last digits.

## Reproduce

Requirements: Python ≥ 3.10, numpy, scipy. Run from this folder.

```sh
python test_lagmom.py          # unit tests
python equivalences.py         # exact identities E1-E4
python bench.py --reps 200     # Part A bench, about 40 min on 2 cores
python evaluate.py             # scores predictions A1-A11
python rival_table.py          # Part B rival forecasts
```

Part B, after the data file is available:

```sh
python real_data.py --ts PATH/0010_geschwind_ts.tsv --structure-only
python real_data.py --ts PATH/0010_geschwind_ts.tsv     # about 25 min (300 matched-null datasets)
python decide_part_b.py
```

Seeds are fixed (world index × 100000 + replicate in the bench).

## Data

No participant-level data are in this repository. The real-data run needs `0010_geschwind_ts.tsv` from openESM ([Zenodo record 17347473](https://zenodo.org/records/17347473), CC BY-NC 4.0). It must be the file with SHA-256 `811f41aeaeb8dbfaa67ca8f8a5387d222701c42fc316f9eb3d61326d138bc8ee`, the one R-003/R-004 used. `real_data.py` refuses any other file.
