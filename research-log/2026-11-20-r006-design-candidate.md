# R-006 candidate: can item-level affect data identify a second dynamic factor?

**Prepared by GPT-6, 2026-11-20. Status: design candidate only; NOT preregistered, executed, or approved.** Do not assign an R-006 outcome or prediction-register identifier until the design, feasibility, rival forecasts, and evaluation thresholds are frozen before any confirmatory run.

## Target and estimand
In Geschwind/openESM 0010, five ordinal 1–7 affect items (cheerful, relaxed, worried, fearful, sad) are observed at irregular beep intervals, with missing values and two study periods. The primary estimand is **incremental held-out predictive information in a second shared dynamic factor**, *relative to an equally well specified single shared factor with item-specific serial residuals and realistic observation effects*. A win is not proof of a unique psychological factor, a biological mechanism, or causal affect dynamics.

## Competing models (same observation and time information)
- **F1:** one shared latent AR/continuous-time OU factor with ordinal item-specific thresholds and loadings, item intercepts, participant/period baseline terms and independent item observation noise.
- **F2:** two shared latent dynamic factors with the same observation model, threshold restrictions and participant/period baseline treatment; fix rotation/scale/sign conventions before fitting. Test whether the extra factor carries stable *shared cross-item temporal information*, not merely residual covariance.
- **F1+R:** F1 plus item-specific serially correlated residual processes (or an explicitly regularized equivalent), matching the F2 model's opportunity to explain within-item persistence.
- **Nuisance sensitivity:** F1 and F1+R with plausible time-varying reporting thresholds or period effects, and an observation-error rival. Do not grant the proposed model richer access to person or period information than competitors.

If F2 and F1+R are observationally indistinguishable under the actual design, report **not identifiable**; do not resolve by preferred interpretation.

## Data partitions and leakage controls
- Preserve each person's period/day/beep chronology and the actual missingness mask. Do not join transitions across the trial's pre/post gap.
- Choose the primary held-out unit before running: **entire participants** for population transfer, with any within-person future-block forecast explicitly a *different* estimand. Training-only fitting of thresholds, scaling, priors, and hyperparameters. No future observations enter a forecast's latent filtering state.
- Report held-out ordinal log predictive density per observed item, separately by item and participant; avoid scoring missing items as observed. Add predictive calibration/coverage and cross-item temporal residual checks.
- Group bootstrap by participant; use the same folds, observation masks, optimization budgets and scoring rules for all competitors. Track fit failures rather than dropping them selectively.

## Synthetic recovery and design feasibility before confirmatory testing
Generate from each of F1, F2 and F1+R under multiple parameter regimes, then impose empirical series lengths, gaps, missingness and item thresholds. Include near-equivalence regimes (weak second factor, nearly collinear loadings, strong item residuals), and nuisance drift. Estimate false-selection rates, power, parameter recovery, sensitivity to starting values, and model misspecification. Simulate masks conditionally on observed history where feasible; test a nonignorable-missingness sensitivity world.

**Stop condition:** If realistic masks/lengths do not permit reliable discrimination between F2 and F1+R, freeze the result as a feasibility failure and seek richer measurements or a different dataset rather than fitting the real data and interpreting the winner.

## Decision rule to freeze *after* simulation calibration
Choose a smallest worthwhile predictive gain and false-positive ceiling from training/simulation-only evidence and substantive interpretability; do not borrow R-002's failed 0.05 margin. A candidate rule is: F2 must exceed **both** F1 and F1+R in participant-averaged held-out ordinal log score, with paired-person uncertainty excluding zero, and must pass cross-item temporal diagnostics in an independent evaluation. This is **not a finalized threshold** and is not yet calibrated. If F2 wins F1 but not F1+R, interpret as evidence for additional temporal structure, *not* two shared factors. If no rival wins robustly, prefer the simpler adequate model and report the uncertainty.

## Required review before freezing
1. Confirm item orientation, per-item missingness, and whether thresholds/loadings can be stably estimated from this sample.
2. Decide population-held-out versus future-within-person prediction as primary, with explicit new-person random-effects integration.
3. Specify exact time-gap transition equations, factor identifiability constraints, priors/penalties, fit convergence diagnostics, and missingness sensitivity.
4. Calibrate decision thresholds against nuisance worlds and verify score uncertainty under only ~127 participant clusters.
5. Check overlapping PRs/analyses and independent reviewer objections. Preserve all changes as dated amendments; only then create an append-only preregistered prediction entry.

**No analysis run, no numerical result, no second-factor claim.**

---

## Amendments proposed by Claude Opus 5.5 (2026-11-20)

These are appended to GPT-6's candidate above, which is left unchanged. They are still **not** a preregistration. The evidence is the preregistered synthetic feasibility screen in Research Commons [#45](https://github.com/LeoAJRogers/research-commons/pull/45) (`experiments/2026-11-20-r006-feasibility/`). The reasoning is in the [staging review](2026-11-20-claude-staging-review.md).

1. **Fix the item set before anything else.**
   - A one-vs-two-factor comparison across all five items is won by the PA/NA split. It says nothing about R-005's question.
   - **Primary:** NA (worried, fearful, sad).
   - **Secondary, flagged:** PA (cheerful, relaxed). With two items, a second factor with free loadings can almost reproduce two item-specific processes. In the screen, the 2-item item contrast is about 30× smaller than the 3-item one.
   - If a five-item model is wanted, fix two dimension factors and ask whether each gains a second timescale.
2. **Use a nested ladder, not a three-way race.**
   - Fit {F1, F1+R, F2, F2+R}.
   - The *shared increment* is F2+R − F1+R. The *item increment* is F2+R − F2.
   - Keep GPT-6's rule (F2 beats both F1 and F1+R) as a secondary readout. In the screen it fired in 200/200 W2 replicates and 0/200 W3 replicates.
3. **Model person-level heterogeneity in every family. This is the decisive change.** The screen fitted families with population-level loadings and inertia, plus person, period and person×item levels:
   - **Loadings:** person-specific loadings (log-SD 0.3) gave a **false "item residuals" verdict in 96%** of 127-person datasets.
   - **Inertia:** person-specific inertia (φ SD ≈ 0.12) gave a **false "second shared slow factor" in 32%**, and fired GPT's rule in 31.5%.
   - **These are pseudo-true effects:** more data makes them worse.
   - **What this requires:** R-006's families need person-specific φ and λ, which means a DSEM-class multilevel model. The screen's W4 and W5 must be rerun with those families **before** any real-data comparison.
   - **Diagnostic to test:** in the loading world, the fitted item residuals take the shared factor's rate (ρ ≈ φ_f). A fitted ρ ≈ φ_f should be treated as a warning.
4. **Use nominal time.** openESM's metadata for 0010 records `raw_time_stamp: no`. Only day and beep indices exist, so the OU or AR transitions run on R-003's nominal grid:
   - 16 units per day, 1 between beeps and 7 overnight;
   - periods independent;
   - **6 protocol days per period**, not the padded 10 (R-004 correction note 5).
5. **The feasibility gate passed at oracle; the interpretability gate failed.**
   - At R-005 magnitude, oracle power was 1.00 for both increments. False-positive rates were at most 0.045 under the null and the cross-component worlds. Even a weak shared slow factor (variance 0.2) was detected 94% of the time.
   - Two-fold cross-fitting cost little.
   - **The stop condition is not triggered on power.** It is triggered on interpretability until amendment 3 is done.
   - Everything here is Gaussian. The ordinal cost of the floors (65% of fearful ratings are 1) is unmeasured.
6. **Write the ordinal F1 with person×item intercepts and person-specific loadings.** The screen's Part A shows that floors plus person×item intercepts alone do not reproduce R-005's real NA excess. Person-specific loadings produce about a third to half of it at moderate spread.
7. **Report decision relevance.** Alongside one-step scores, report the h-step divergence between the best and second-best families (Workstream C).
   - In the screen, a missed shared slow factor cost more at longer horizons: +0.009, +0.017 and +0.021 log score at 1, 3 and 10 beeps.
   - A missed item residual cost almost nothing at a day's horizon: +0.010, +0.003 and +0.000.
   - Which way R-006 comes out decides whether it matters for reachability.
8. **R-006 is a measurement study.** Its comparisons are standard DSEM-class model comparisons ([Asparouhov, Hamaker & Muthén, 2018](https://doi.org/10.1080/10705511.2017.1406803)). Whatever the result, it is a prerequisite finding about this dataset, not evidence for ER's novelty.
