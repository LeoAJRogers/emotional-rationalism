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
