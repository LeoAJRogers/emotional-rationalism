# R-006 Cycle 2 — independent T1-only calibration

**Investigator:** GPT-6. **Date:** 2026-11-21. **Status:** completed *targeted independent synthetic replication*, **not** full replication of Claude's 22-world R-006 Part A and not human-data Part B. This follows the initial signed-lag and disjoint-pair counterexamples in this branch. No real human-data item responses were opened or analyzed.

## Sources and reproducibility

- Source under audit: Claude Opus 5.5, ER PR #13, revision `2f6ebbf2d64c0c263a8440629200276a93b0c2c8`; original `lagmom.py`, `simulate.py`, `bench.py` and `results/bench_summary.json`.
- Independent code: `calibrate_t1_independent.py` (NumPy/SciPy), separate from the original `lagmom.py` and `simulate.py`. Algorithm independently implements lag-one disjoint-pair U-statistic, per-period centering/scalar scaling, 6-day leave-one-day-out jackknife, 20-term Hermite ordinal correction, and person-level multinomial bootstrap. `test_calibrate_t1_independent.py` verifies disjoint-pair algebra against explicit nested-loop enumeration and checks finite severe-floor results; both local tests passed.
- 127 people × 2 periods (254 person-periods), 6 days × 10 nominal prompts, shared NA factor AR(1), item-white error, Beta-distributed per-period compliance; combined nuisance worlds also vary person loadings/inertia and MNAR response. Six targeted NA worlds: W0, N3, N3h, N8, W1s+N8 (strong item excess .25), W1w+N8 (weak item excess .10).
- 200 new replicates per world (1,200 simulations total); 199 person-bootstrap draws per replicate (less than Claude's 499). Seeds: `100000*(world_index+1)+rep`, with world order `[W0,N3,N3h,N8,W1s+N8,W1w+N8]` and `rep = 0..199`. The T1 positivity decision is the *lower two-sided 95% bootstrap percentile bound > 0*; this is equivalent to a one-sided nominal 2.5% criterion. Results are aggregated without retaining individual synthetic outputs; the script regenerates them deterministically.
- Run from the script directory: `python calibrate_t1_independent.py --reps 100 --start 0 --worlds N8 --boot 199 --output N8_part1.json` and repeat `--start 100`. For other worlds, substitute the name. The output folder must already exist if using a path.

## Primary result: independent T1 detection

| World | Independent T1 fires | Independent T1 mean (SD) | Claude #13 fires |
| --- | ---: | ---: | ---: |
| W0 continuous F1 null | 4/200 (2.0%) | −0.0042 (0.0236) | 1.5% |
| N3 ordinal floors | 3/200 (1.5%) | −0.0176 (0.0568) | 1.5% |
| N3h 75%-floor nuisance | 2/200 (1.0%) | −0.0783 (0.2635) | 1.0% |
| N8 combined heterogeneity, floor, MNAR | 5/200 (2.5%) | −0.0102 (0.0608) | 1.5% |
| W1s+N8 strong item persistence | 193/200 (96.5%) | +0.2721 (0.0852) | 98.0% |
| W1w+N8 weak item persistence | 58/200 (29.0%) | +0.0891 (0.0711) | 29.5% |

All independently generated detection rates are broadly consistent with Claude's original runs. The rates are *sampling estimates*, not exact probabilities: for the N8 null, 5/200 has a Wilson 95% binomial interval approximately 1.1–5.7%; for the weak effect, 58/200 has interval 23.2–35.6%. Detailed values and all rates are in `results/t1_targeted_calibration_summary.json`.

## Important divergences and limitations

- **High-floor mean discrepancy:** N3h's corrected T1 mean was −0.0783 (SD 0.2635) independently, versus −0.0263 (SD 0.3389) in Claude's summary. Even with the same broad detection rate, these *are not matching sampling distributions*. Could be random-seed/simulator details, finite sample, or a subtle code difference. Must audit before treating full numerical equivalence as established.
- **Ordinal correction tradeoff:** In these independent worlds the *uncorrected* linear T1 fired for 12/200 N3, 8/200 N3h and 12/200 N8 null datasets, versus 3/200, 2/200 and 5/200 corrected. But the corrected severe-floor estimate is negatively biased and highly dispersed in this run. Conservative false-positive behavior can coexist with weak sensitivity, and the correction assumptions still need adversarial testing beyond latent-Gaussian ordinal worlds.
- **Weak-effect limitation:** under W1w+N8 the primary corrected T1 detected 29%, so *a negative Part B result would not exclude a weak item-specific persistence effect*. Power is condition-specific.
- **Uncovered scope:** This independently tests T1 only, not T2 lag-rate minors, T3 curvature, PA determinant, bipolar tetrad, sign-test familywise control, E3a under signed lag contributions, or R-006's full 22-world preregistration. Other nuisance classes (between-day loading drift N6, response anchoring N7, non-Gaussian ordinal settings, floor-dependent drift) remain possible confounds.
- **Simulation matching:** The generator matches the NA marginal model and 0010-like schedule/completeness assumptions but does not simulate the full correlated PA/NA system. It uses new RNG streams, a 40-iteration Newton inverse rather than Claude's 50, and 199 rather than 499 bootstrap resamples. This is an *independent implementation check*, not exact seeded code duplication. Higher-order details and null coverage should be reconciled in cross-review.
- **Code gate remains:** the observed-denominator low-floor sensitivity bug in `real_data.py` and duplicate-key fail-closed concerns were separately reported on PR #13. These must be repaired prospectively before Part B. Geschwind file integrity and participant-period keys were verified by HAAR H-001, but no human-data models were run here.

## Director's disposition

The T1 core has survived an independent targeted replication of the central *false-positive vs strong/weak power pattern*. **Do not promote to validated mechanism identification**: loading stability, reporting anchoring, positive lag-covariance assumptions, and meaningful external anchors remain unverified. Maintain PR #14 as draft and PR #13 unmerged pending Claude cross-review and the remaining test families. Next highest-value pass: deliberately challenge the ordinal correction with non-Gaussian measurement and **calibrate negative/sign tests** rather than rerunning confirming T1 worlds indefinitely.

**No new HAAR assignment.** The five acquired datasets remain untouched pending a preregistration amendment, code review, and a separate Part B decision.
