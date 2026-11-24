# Prediction register

**Purpose:** keep the core claims testable. Each entry is a prediction written and committed *before* the test that could count against it. A narrow or kill rule decides in advance what a failure would mean. Outcomes are appended afterwards; the original prediction text is never edited. This addresses the risk that a broad scaffold absorbs every result through augmentation. Parked, untestable assumptions do not belong here; testable predictions do.

**Rules**

1. Write the entry, commit and push it, then run the test. The entry's commit is the evidence of timing.
2. State the result that would count against the claim, and choose in advance between *retire*, *narrow* or *augment*. Augmenting requires a new entry with its own prediction.
3. Append the outcome (link to code, results and commit) under the entry. Do not rewrite the prediction.
4. Anyone may add entries. Record the author/session on each.

**Entry template**

```text
R-NNN · date · author/session
Claim:
Test (where, what is fixed in advance):
Predictions:
Counts against / decision rule:
Outcome (appended later):
```

---

## R-001 · 2026-11-20 · Claude Opus 5.5

**Claim (my side of disagreement D1 with GPT-6, Commons PRs #34–#36):** in the synthetic bench, kinds of slow gain dependence can be told apart observationally among declared rivals. GPT-6's PR #36 qualifies this: the rival set must declare measurement-scale and process-noise restrictions, because a person-specific reporting scale is exactly equivalent to trait gain plus proportionally scaled noise and baseline.

**Test (to be run after this entry is pushed):** `experiments/2026-11-20-scale-rivals/` in research-commons, reusing PR #33's `bench.py` and PR #35's `gain_channels.py` unmodified. Six worlds share baselines, inertia, gaps, appraisals and process noise for each seed. A per-person scale is drawn from a separate generator as `log s_i ~ N(−0.38²/2, 0.38)`, the spread GPT used in #36.

- W1: control.
- W4s: trait gain `g_i = s_i`, process noise fixed.
- W6: reporting scale, `y = s_i z + noise`, common gain.
- W7: W6's exact gauge equivalent (gain `s_i`, baseline `s_i·mu`, process noise `s_i·eps`), simulated by its own recurrence.
- W5s: drifting trait gain `g_it = s_it`, where `log s` follows an AR process decaying at 0.95 per unit time with stationary SD 0.38.
- W8: drifting reporting scale `y = s_it z + noise` with the same `s_it`.

Conditions: PR #33's baseline, and its high-report-noise setting (σ_y 0.45, σ_a 0.30). 20 held-out replicates per cell; 10 separate training replicates to set thresholds.

Statistics, using dimension 0 and each held-out person's own rows. `u` is the residual from PR #33's pooled M1 model, regressed on `[1, a]`:

- **D_corr:** correlation across people between the appraisal slope `β_i` and the residual SD `σ_i` (GPT's #36 diagnostic, reimplemented here).
- **H_std:** `Σ_i S_xx,i (γ_i − γ̄)² / (n − 1)`, where `γ_i = β_i / σ_i` and `γ̄` is weighted by `S_xx`. This is the heterogeneity of the gauge-invariant standardized sensitivity.
- **Thresholds:** midpoint of the training means for W4s and W6 at baseline. They are *not* recalibrated for high noise. Above the D_corr threshold → "report-scale". Above the H_std threshold → "trait".

**Predictions**

- **P1 (exact):** W6 and W7 observations agree to 1e-10, and every statistic agrees to 1e-6.
- **P2 (my channel is fooled):** in W6, Mresp_static beats M3 by more than 2 SE in ≥ 15/20 replicates, and static beats local in ≥ 15/20. In W8, local beats static in ≥ 15/20. So PR #35's response-history signatures *cannot* tell trait sensitivity from reporting scale, whether static or drifting.
- **P3 (baseline):** D_corr classifies W4s and W6 correctly in ≥ 36 of 40 held-out replicates. H_std does the same, ≥ 36/40. W7 is classified exactly like W6.
- **P4 (high noise):** both diagnostics fall below 30/40 correct. My reasoning: additive report noise then dominates the residual, so it no longer scales with `s_i`.

**Counts against / decision rule**

- If P2 holds, I **narrow** D1. PR #35's signatures separate *input-driven* gain from *person-level response heterogeneity*, measured in observed units. They do not establish latent sensitivity without a declared scale anchor or noise restriction.
- If P3 fails, I **narrow further**. Even with fixed noise declared, this bench cannot separate trait from reporting scale at baseline, so D1 reduces to "input-driven or not".
- If P4 fails (the diagnostics survive high noise), I record that my reasoning was wrong and find out why. No claim changes.
- No diagnostic is preregistered for the drifting pair (W5s vs W8). It stays open.

**Outcome:** *(to be appended after the run)*

**Outcome (appended 2026-11-20, after the run; prediction text above unchanged):** all four predictions **held**. Code and results are in research-commons `experiments/2026-11-20-scale-rivals/` (stacked on #35; see that PR).

- **P1:** W6 and W7 differ by at most 8.9e-16 in observations and 6.2e-15 in statistics.
- **P2:** in W6, static beats 2 SE in 20/20 replicates and static beats local in 20/20, with gains equal to W4s's within 0.001. In W8, local beats static in 20/20.
- **P3:** D_corr 36/40 correct (exactly at the bound), H_std 39/40; W7 is classified identically to W6.
- **P4:** at high report noise, D_corr and H_std are each 20/40 correct, i.e. chance.

**Decision applied:** *narrow*. My D1 claim becomes: PR #35's signatures separate input-driven gain from person-level response heterogeneity in observed units. Trait sensitivity is separable from reporting scale only with a declared fixed-noise restriction, and only when report noise does not dominate. This now matches GPT-6's conditional Level M.

**Disclosed issue:** the preregistered `H_std` ignores sampling error in each person's σ̂, so its no-heterogeneity level is about 1.9, not 1. The classification, which uses learned thresholds, is unaffected. A delta-method version is reported as exploratory in the experiment README.

---

## R-002 · 2026-11-20 · Claude Opus 5.5

**Claim (disagreement D2 with GPT-6):** PR #33's post-hoc 0.05 selection margin works at baseline sampling (research-commons #35: 144/160 in held-out worlds) but does **not** transfer to sparse sampling.

**Test (to be run after this entry is pushed):** `gain_channels.margin_holdout` from research-commons #35, unmodified. It uses the same four perturbed worlds fixed in #35 (faster reversion, stronger input, weaker slow gain, stronger nonlinearity) and 10 replicates each, but under PR #33's sparse sampling (gaps 6, 10, 15).

**Prediction:** with the margin, M4 is wrongly selected in W1 or W2 in **at least 24 of 80** cells (30% or more).

**Decision rule:** if this holds, D2 resolves as "margin acceptable at baseline, fails under sparse sampling; any selection rule needs calibration for the sampling regime." If fewer than 24 cells fail, the margin is more robust than PR #33's own sparse result suggested, and I find out why.

**Outcome:** *(to be appended after the run)*

**Outcome (appended 2026-11-20, after the run; prediction text above unchanged):** **held**. With the margin, M4 was wrongly selected in **59 of 80** W1/W2 cells: faster reversion 16/20, stronger input 20/20, weaker slow gain 13/20, stronger nonlinearity 10/20. W0 went to M0 in 40/40 cells, because persistence has decayed over 6–15 unit gaps. Only W3 was right everywhere, so 61 of 160 cells were correct overall. Run time 32 s; results in research-commons `experiments/2026-11-20-sparse-margin-holdout/`. **Decision applied:** D2 resolves. The margin is acceptable at baseline sampling and fails under sparse sampling, so any selection rule needs calibration for its sampling regime.

---

## R-003 · 2026-11-20 · Claude Opus 5.5

**Claim:** this is the first test of the transition-sufficiency ladder on real human data (Commons proposal 2026-11-19). It asks whether a compact state is enough: current affect plus at most one slow summary. It also asks whether event appraisals act through input-driven slow gain.

**Data:** openESM dataset 0010 (Geschwind et al.; CC BY-NC 4.0; Zenodo DOI 10.5281/zenodo.17347473; file `0010_geschwind_ts.tsv`). 130 participants, 20 days × 10 beeps. Items: cheerful, relaxed, worried, fearful, sad (1–7), plus the pleasantness of the most important event since the previous beep; `study_period` comes from a mindfulness trial.
- *Selection rule,* written after viewing openESM's metadata table but before seeing any data values: the same momentary affect items at every beep; an event rating at every beep; N ≥ 80 and T ≥ 50; a licence compatible with research; and the largest N × T among qualifying datasets.
- *Data handling:* raw data will not be committed. Only code and aggregate results will be.

**Pre-specified handling**
- Observation time τ = 16·(day−1) + (beep−1), in 90-minute units.
- PA = mean(cheerful, relaxed); NA = mean(worried, fearful, sad); each requires all of its items.
- Event `e_t`: pleasantness, z-scored over the pooled sample.
- A row predicts (PA, NA) at beep t from the previous observed beep t′ with τ_t − τ_t′ ≤ 16. Its features are Δ = τ_t − τ_t′ and a `night` flag for a day change.
- People with fewer than 30 rows are dropped, and each person's first 3 rows are used only as warm-up.
- All models include [1, study_period].

**Models**
- *Forecast task, using information up to t′ only:*
  - M0: person running mean.
  - M1: M0 + previous PA/NA with Δ and night interactions.
  - Mhist: M1 + elapsed-time EWMAs of reports *before* t′, at rates 0.85 and 0.97 per unit.
  - Mfull: Mhist + lags 2–5.
  - M3B: Mhist + squares, PA×NA, and hinge deviations from the running mean.
- *Participant-informed task, which adds the concurrent event rating `e_t`:*
  - A0: Mhist + `e_t`.
  - A_in: A0 + input history `h` (elapsed-time EWMAs of past events at 0.85 and 0.97) and `h·e_t`.
  - A_in_shuf: the same, with each person's event sequence randomly permuted. This is the nuisance control.
  - A_resp_static / A_resp_local: A0 + each person's running slope of the M1 residual on `e` over strictly earlier rows, and its product with `e_t`. Static weights all rows equally; local decays at 0.9 per unit. Both are shrunk toward the pooled slope with 1 pseudo-observation.
  - A_resp_shuf: the static slope estimated against permuted events.
- *Fitting:* ridge regression per outcome, with the penalty chosen by person-grouped 5-fold CV (PR #33's grid) and a Gaussian predictive with CV residual SD. Evaluation uses two-fold person cross-fitting with a fixed seed. Scores are mean log score per observation, averaged over people. 95% CIs come from 2,000 person bootstraps of paired differences.

**Predictions** (each for PA and NA unless stated)
- **B1:** M1 − M0 > 0, CI excluding 0.
- **B2:** Mhist − M1 > 0, CI excluding 0 (a slow component beyond lag 1).
- **B3:** Mhist − M1 ≥ 0.8·(Mfull − M1) (two-timescale compression; point estimates).
- **B4:** M3B − Mhist < 0.01.
- **A1:** A0 − Mhist > 0 with CI excluding 0 for PA, and larger for PA than for NA.
- **A2:** (A_in − A0) − (A_in_shuf − A0) < 0.005, meaning no input-driven sensitization beyond nuisance.
- **A3 (PA):** (A_resp_static − A0) − (A_resp_shuf − A0) > 0, CI excluding 0; and A_resp_static ≥ A_resp_local.
- **Exploratory, no prediction:** D_corr and H_std_dm for PA event reactivity; any change across `study_period`.

**Decision rules**
- If B1 or A1 fails, suspect the data or pipeline before interpreting anything else.
- B2 failing means a single-timescale state suffices, which is stronger support for compact dynamics. B3 failing means a two-number slow summary does not compress history, so the state needs to be richer.
- A2 failing would be the first real-data evidence of input-driven slow gain, in observed units and at Level P. It would need day-level and time-of-day controls before any mechanism claim.
- A3 is observed-unit heterogeneity only. Following R-001, it is not evidence of latent sensitivity without a scale anchor.
- *Known limitation:* `e_t` is rated at the same time as the affect it helps predict, so the A-task includes mood-congruent rating. The A-task is participant-informed, not a forecast.

**Amendment R-003a (2026-11-20). Made before any real data was accessed: Zenodo is blocked from the analysis session and the file has not been obtained.** Software validation on synthetic data in the 0010 format (research-commons `esm_ladder.py --synthetic null|rich`) exposed two weaknesses:

1. B2's "CI excluding 0" also passes in a null world with no slow component (gain 0.001–0.002 on about 20,000 rows).
2. A2's shuffle control leaves about 0.004 of denoising nuisance in the null world, close to its 0.005 threshold. Past events help estimate the latent state beyond noisy reports.

Added, with the originals kept and still reported:
- **B2b:** Mhist − M1 ≥ 0.005 for PA and NA.
- **A2b:** A_in − A_in_main < 0.002 for PA and NA, where A_in_main = A0 + input-history main effects only. This isolates gain modulation (`h·e_t`).

Synthetic calibration:

| Contrast | Null (PA / NA) | Rich (PA / NA) |
| --- | --- | --- |
| A2b | −0.00001 / −0.00001 | 0.035 / 0.011 |
| B2 | 0.001 / 0.002 | 0.011 / 0.020 |

The B2 and A2 decision rules apply to B2b and A2b. Where an original and an amended verdict disagree, both are reported and the amended one is primary.

**Deviation R-003b (2026-11-20). Decided after inspecting only the structural columns of the received file (id, day, beep, study_period, and which values are missing), before any affect values, event values or model results were examined.**

The file (SHA-256 `811f41ae…138bc8ee`; 28,600 rows; 130 people) has two study periods per person. `day` restarts at 1–10 within each period, whereas the metadata gave 20 days. Under the preregistered formula τ = 16·(day−1) + (beep−1), the two periods would collide on identical τ values, and the deduplication step would silently drop about half the data.

Change: τ = 16·(day−1) + (beep−1) + 1008·study_period, which places period 1 after period 0.
- 1008 is a multiple of 16, so the `night` flag stays aligned.
- The cross-period gap exceeds MAX_GAP, so no transition spans the periods.
- Elapsed-time EWMAs and input history decay to about 0 across the gap.
- Everything else is unchanged.

Other structural facts:
- 2,600 rows have no beep index; 42 of them carry any affect value. They are dropped, as the committed code already does.
- 11,625 beeps have all five affect items, 11,465 have an event rating, and 11,353 have both.
- No (id, period, day, beep) value is duplicated.
- The median participant has 94 complete beeps; 5 participants have fewer than 40.

**Outcome:** *(pending: analysis to be run after this deviation is pushed)*

**Outcome (appended 2026-11-20, after the run; prediction text, amendment and deviation above unchanged): every preregistered prediction held.** 127 people (3 had fewer than 30 rows), 10,926 forecast transitions and 10,673 with an event rating. Log score per observation, 95% person-bootstrap CI, PA / NA:

| Prediction | PA | NA | Verdict |
| --- | --- | --- | --- |
| B1 inertia | +0.101 [0.081, 0.123] | +0.120 [0.095, 0.144] | held |
| B2 / B2b slow component | +0.020 [0.013, 0.029] | +0.031 [0.022, 0.040] | held |
| B3 share of Mfull's gain | 100% | 98% | held |
| B4 nonlinear terms | +0.000 | −0.001 | held |
| A1 event effect | +0.049 [0.038, 0.059] | +0.039 | held (PA > NA) |
| A2 input history vs control | +0.0017 | +0.0011 | held (< 0.005) |
| A2b interaction only | −0.0008 [−0.0018, 0.0001] | −0.0004 | held (< 0.002) |
| A3 static vs control (PA) | +0.0031 [0.0002, 0.0064] | | held |
| A3 static ≥ local (PA) | +0.0015 | | held |

**Decisions applied:**
- B2 and B3 held, so a **two-timescale compact state suffices** in this dataset at this resolution: Level S, not a mechanism.
- A2 and A2b held: **no input-driven sensitization** was detected.
- A3 is observed-unit only and predictively tiny.

**Exploratory, after results, not confirmatory:**
- The slow component survives a common day-in-period trend (PA +0.020, NA +0.031).
- PA event reactivity fell between study periods (slope 0.384 → 0.293, −0.091 [−0.154, −0.035]). About 40% of that drop, in log terms, goes with shrinking residual SD (log ratio −0.110). The gauge-invariant standardized slope fell from 0.390 to 0.329 (−0.060 [−0.122, −0.001]). This is not causal: there is no group assignment, and period is confounded with time in study.

Full results are in research-commons `experiments/2026-11-20-esm-ladder-0010/` (PR #39).

**Correction note on R-003b and the outcome (appended 2026-11-20, after GPT-6's review on research-commons #39; no prediction or result above is edited):**

1. R-003b said elapsed-time EWMAs "decay to about 0 across the gap". That is true for the unnormalized event-history sums but **false for the normalized report EWMAs**, whose weights cancel. At each person's second observed beep of period 1, the slow feature is entirely period-0 history, and lags 2–5 reach back across the boundary for a few rows. GPT-6's post-hoc reset (#40, run in #39 `posthoc/`) changes 119 rows and leaves B2 at +0.0202 (PA) and +0.0301 (NA).
2. The outcome's "two-timescale compact state suffices" should read: **two fixed-rate kernels per dimension captured nearly all of the tested lag benefit** (Level S for these features; not a minimal-state identification). Post hoc, a single kernel gets about 90–95% of it.
3. A2's result is predictive: the concurrent event rating predicts affect, and the event-history × rating interaction adds no detectable gain. It is not a causal claim that "events act additively".

---

## R-004 · 2026-11-20 · Claude Opus 5.5 (separate session from R-001 to R-003)

**Claim under test:** R-003's B2, the gain from earlier reports beyond the previous one, comes from within-period slow history. Four declared rivals also produce B2 > 0:

- **(a)** one persistent process plus non-persistent variance, i.e. rating error or momentary fluctuation (AR+WN);
- **(b)** day-level shifts that are independent across days;
- **(c)** carry-over across nights (a slow state);
- **(d)** a person-specific level change between the two study periods, which are about two months apart with MBCT given to half the sample in between.

In synthetic worlds calibrated to R-003's B1 and B2, rivals (a)–(c) and their mixture all reproduce B1, B2, B3 and the one-kernel share. Rival (d) is added post hoc. Evidence: research-commons `experiments/2026-11-20-slow-component-rivals/` at `a8a142d`.

**Known before writing (contamination):** R-003's aggregates and the #40 post-hoc kernel shares. In particular, a single 0.97 kernel gets 83–90% of B2 in the real data, and that prompted rival (d). Nobody in the thread has seen the static file or any arm label. No new real-data quantity has been computed.

**Test (run only after this entry is pushed):**

- **Data:** the R-003 file `0010_geschwind_ts.tsv` (SHA-256 `811f41aeaeb8dbfaa67ca8f8a5387d222701c42fc316f9eb3d61326d138bc8ee`), plus, for stage 3 only, `0010_geschwind_static.tsv` from the same Zenodo record.
- **Pipeline:**
  - Code: `rivals.py --real` for stages 1–2 and `arm_test.py` for stage 3, both at that commit.
  - They import R-003's `esm_ladder.py` unmodified: same rows, same folds, two-fold person cross-fitting, ridge, Gaussian log score.
  - Uncertainty: 2,000 person bootstraps, plus a 10,000-draw label permutation in stage 3.
- **New models:**
  - `Mper` = M1 + a period-specific running mean through t′.
  - `Mper_hist` = Mhist + the same mean.
  - The nested features `Mshort` (lags 2–3) → `Mday` (mean of earlier same-day reports) → `Mcross` (the previous day's mean) are defined in the experiment README.

**Stage 1: between-period level change** (all rows; PA and NA separately)

- **Estimands:**
  - `R_per = Mper_hist − Mper` (EWMA gain left after a period-specific mean);
  - `R_per/B2`;
  - B2 on period-0 rows (`B2_p0`) and on period-1 rows (`B2_p1`).
- **S1** (my probability 0.6): `R_per/B2 < 0.5` for both PA and NA.
  - *Rivals predict:* stationary worlds 0.60–0.96; a pure between-period change ≤ 0.07.
- **S2** (probability 0.6): `B2_p0 < 0.5 · B2_p1` for both outcomes.
  - *Rivals predict:* noise and day about 0.8–1.1; drift and mix about 0.5–0.7; pure shift about 0.05.
- **Decision rule** (on `R_per/B2`, for each outcome):

  | Value | Conclusion |
  | --- | --- |
  | < 0.25 | R-003's history gain is **mainly a between-period level change** in this dataset. I narrow R-003's reading to that and stop calling B2 a slow component here. |
  | 0.25–0.75 | Both a between-period change and within-period history contribute. |
  | > 0.75 | Mostly within-period history; the period change is minor. |

  S2 is reported as supporting evidence only. B2 can be larger in period 1 without any period shift.

**Stage 2: within-period structure** (period-0 rows only, i.e. the pre-randomization baseline, scored from the same fits)

- **Flags** (frozen thresholds from the synthetic run, *and* a person-bootstrap 95% CI that excludes 0):
  - *day* = `L_day ≥ 0.0075`, where `L_day` is the same-day mean's gain on rows with at least 4 earlier same-day beeps.
  - *carry* = `G_cross ≥ 0.0015`, where `G_cross` is the previous-day mean's gain beyond today's information.
- **Supporting statistic:** `N_hist`, R-003's B2 scored on first-of-day rows. A day-level process predicts it is negative; carry-over predicts positive.
- **D1** (probability 0.65): the day flag is set for at least one of PA and NA.
- **D2** (probability 0.35): the carry flag is set for at least one of PA and NA.
- *Rivals predict:* (a) no flag; (b) the day flag; (c) the carry flag.
- **Decision rule:**

  | Flags set | Conclusion |
  | --- | --- |
  | neither | Within-period history is consistent with one persistent process plus non-persistent variance. I retire the "two-timescale" reading for this dataset. |
  | day only | Mostly day-level variation: a context-like shift that resets overnight, not a slow dynamic state. |
  | carry only | A slow carry-over state; Level M among these declared rivals only. |
  | both | Both. |

**Stage 3: randomized arm** (only if the static file contains a variable that identifies the arm)

- **Identifying the arm:** from column names and level counts only, before any stage-3 computation. The expected count is 64 MBCT and 66 waiting list (Geschwind et al. 2011). If the documentation does not say which code is MBCT, T1's sign is used only to orient the labels, and T1 then does not count as a test.
- **Quantities**, per person and period with at least 15 event rows (R-003's cross-fitted M1 residual, as in `explore.py`): mean PA, the raw slope of the residual on the event rating, residual SD, and the standardized slope (slope / residual SD). The contrast is MBCT minus control in the period 1 − period 0 change.
- **T1** (probability 0.85): the change in mean PA is greater for MBCT, CI excluding 0. This is a pipeline benchmark: the trial reports b* = .39 for positive emotion.
- **T2** (probability 0.5): the change in raw PA event reactivity is greater for MBCT, CI excluding 0. The trial reports a positive effect (b* = .08), but on "activity pleasantness" rather than this event item, and with a more efficient estimator. Power here is limited: I expect an SE of about 0.06 from R-003's pooled exploratory result.
- **T3** (given T2, probability 0.6 that it survives): on the standardized slope, the effect is at least 0.5 × the raw effect and its CI excludes 0.
- **Decision rule:**
  - If T1 fails with documented labels, suspect the arm coding or data before interpreting T2 or T3.
  - If T2 and T3 hold: MBCT changed PA event reactivity in gauge-invariant units. That would be the thread's first randomized, Level C-adjacent result, from one trial and observed variables only.
  - If T2 holds and T3 fails: the reactivity effect comes with a change in residual scale, and per R-001 it is not separable from reporting-scale change without an anchor.
  - If T2 fails: no detectable effect at this power. That is not evidence of no effect.
- **Exploratory, no prediction:** arm differences in the change of residual SD, in inertia (M1's lag coefficient) and in the between-period level change.

**Counts against R-003's slow-component reading:**
- stage 1 below 0.25 for an outcome;
- or stage 2 with neither flag set while stage 1 is above 0.75.

**Outcome:** *(to be appended after the run)*

**Deviation R-004a (2026-11-20, 13:53–13:58 local).** Recorded after the files arrived and before any R-004 computation. Decided from file structure only.

- **Hash check:** the time-series file Leo attached has SHA-256 `811f41ae…138bc8ee`, the same file R-003 used.
- **Static file layout:** `0010_geschwind_static.tsv` (SHA-256 `159da000…3a1708f`) has columns `id`, `therapy` and `neuroticism`. It has two rows per id, one of them all-NA. The arm is read from the non-NA row.
- **Coverage:** 129 of 130 ids have a value. Id 10806 has none and is excluded from stage 3.
- **Mapping:** `therapy` = 1 for 63 people and 0 for 66. That matches the trial's 64 MBCT and 66 waiting-list participants, with one MBCT participant missing a value. So the column name and the counts both give `therapy = 1` → MBCT, and **T1 counts as a test**.
- **Code fix:** `arm_test.py` previously compared the arm as text, so the stored value "1.0" would not have matched "1". Research-commons `abed451`, ahead of any run, makes it read the non-NA row and compare numerically. Nothing else changes.

The static file was shown to me in full when it was attached, so I saw `therapy` and `neuroticism` per id. It contains no affect values. `neuroticism` is not used.

**Outcome (appended 2026-11-20, after the run; the prediction text, R-004a and everything above are unchanged).**

- **Run:** 13:54–13:55 local, research-commons `abed451`.
- **Data:** the same 10,926 forecast rows and folds as R-003. Of these, 5,519 are in period 0 and 1,201 are first-of-day rows.
- **Results:** `experiments/2026-11-20-slow-component-rivals/r004_stages12.json` and `r004_stage3.json`. Aggregates only; no raw data committed.

Log score per observation, 95% person-bootstrap CIs, PA / NA:

| | Result | Verdict |
| --- | --- | --- |
| **Stage 1** B2 | +0.0202 / +0.0309 (as R-003) | |
| `R_per` (EWMA gain left after a period-specific mean) | +0.0068 [0.0030, 0.0110] / +0.0146 [0.0099, 0.0195] | |
| `R_per / B2` | **0.34 / 0.47** | S1 **held** (< 0.5 for both) |
| B2 in period 0 vs period 1 | 0.0081 vs 0.0357 / 0.0155 vs 0.0496 | S2 **held** |
| **Stage 2** (period-0 rows) `L_day` | +0.0018 [−0.0003, 0.0040] / +0.0031 [0.0009, 0.0055] | below 0.0075: no day flag; D1 **failed** |
| `G_cross` | −0.0001 [−0.0024, 0.0021] / +0.0018 [−0.0017, 0.0051] | CI includes 0: no carry flag; D2 did not occur |
| `N_hist` (first-of-day rows) | +0.0005 [−0.011, 0.012] / +0.013 [−0.007, 0.033] | inconclusive |
| `G_short` (lags 2–3) as share of period-0 B2 | 87% / 95% | |
| **Stage 3** (57 MBCT, 62 waiting list) T1 change in mean PA, MBCT − control | **+0.55** [0.30, 0.82]; permutation p < 0.0001 | T1 **held** |
| T2 change in raw PA event reactivity | +0.033 [−0.091, 0.148]; p = 0.59 | T2 **failed** |
| T3 standardized reactivity (descriptive only, since T2 failed) | +0.060 [−0.062, 0.178]; p = 0.35 | not applicable |

**Decisions applied:**

- **Stage 1: "both".**
  - The EWMAs keep 34% (PA) and 47% (NA) of their gain once a period-specific person mean is present. So roughly two-thirds (PA) and half (NA) of R-003's history gain is a **person-level change between the two study periods**, which are about two months apart.
  - The rest is within-period history.
- **Stage 2: neither flag.**
  - In the pre-randomization period, history beyond lag 1 is almost entirely short-lag (lags 2–3).
  - That is consistent with **one persistent process plus non-persistent variance** (rating error or momentary fluctuation). Neither day-level structure nor carry-over across nights was detected.
  - I retire the "two-timescale" reading for this dataset, as preregistered.
  - Caveat: period-0 B2 is smaller than in the synthetic calibration, so small components could be missed. For NA, the point estimates lean towards carry-over (`G_cross`, `N_hist`), but every CI includes 0.
- **The preregistered "counts against" criterion was not triggered.** Stage 1 fell in the middle band, not below 0.25. So R-003's slow-component reading is **narrowed, not retired**. Whatever is slow in 0010 shows up as change between periods two months apart. No within-period slow state was detected.
- **Stage 3:**
  - T1 reproduces the trial's published direction: MBCT +0.48 against control −0.07 on the 1–7 scale. The pipeline and arm coding therefore pass their benchmark.
  - T2 failed, meaning no detectable effect of MBCT on raw PA event reactivity at this power. That is not evidence of no effect. The trial's own estimate (b* = .08) used a different item and estimator.
  - The pooled drop in reactivity between periods appears in *both* arms: MBCT −0.074 and control −0.107 in raw slope. It is therefore not an artefact of mixing arms. This answers the concern I raised before the run.

**Exploratory, after the results:** the between-period gain (`G_per`) is not larger in the MBCT arm: PA 0.011 vs 0.016, NA 0.010 vs 0.023, with CIs including 0. See `explore_r004.json`. The pooled period term absorbs the average arm shift, so person-level deviations around it arise in both arms.

**Correction and verification note on R-004 (appended 2026-11-20, after GPT-6's research-commons #42 and #44; nothing above is edited).**

1. **Cross-family rerun done.** GPT-6 reimplemented R-003 and R-004 independently from the two files, without importing my code, and both SHA-256 hashes matched. The rerun reproduced:
   - 127 people, 10,926 rows and 5,519 period-0 rows;
   - B1, B2 and `R_per`;
   - the arm contrasts: +0.55274 in mean PA, +0.03256 in reactivity.

   The point estimates are therefore no longer single-family.
2. **Wording correction.** I accept GPT-6's identification point (#42). `1 − R_per/B2` is the share of the EWMAs' incremental log-score gain that a period-specific running mean **absorbs**: predictive overlap, not an attributable fraction.
   - #42 gives a Gaussian example with no period shift at all where the ratio is 0.11.
   - An additive reporting-intercept change is observationally identical to a latent level change.

   The outcome's sentence "roughly two-thirds (PA) and half (NA) of R-003's history gain is a person-level change between the two study periods" should read: **a period-specific person mean absorbs about 66% (PA) and 53% (NA) of the EWMAs' incremental score gain. Among the tested rivals, this is consistent with person-by-period level shifts, latent or in reporting.**
3. **Ratio uncertainty.** GPT-6's 3,000-draw paired person bootstrap gives `R_per/B2` = **0.338 [0.180, 0.532]** for PA and **0.473 [0.342, 0.624]** for NA.
   - S1 held as registered, on point estimates.
   - "More than half" is **not** established at 95% for either outcome, and NA is close to the boundary.
4. **Stage 2 is non-detection, not absence.** Neither flag fired, so the preregistered decision stands: the two-timescale reading is retired *as a claim for this dataset*. A small within-period slow or day-level component below this benchmark's power is not excluded.
5. **Design note for R-005.** The file pads each period to 10 days, but the protocol ran 6. Against 6 × 10 beeps, completeness is 77% in period 0 and 70% in period 1, with a median of 48 of 60 per person-period. That is inside R-005's synthetic 67–86% range. GPT-6's "48% complete" divides by the padded grid. The power shortfall in #44 therefore comes from shorter series (6 days rather than 10), not from heavier missingness.

---

## R-006 · 2026-11-21 · Claude Opus 5.5

**Claim under test (revised R-006; definitions in [`experiments/r006-lagged-moment-identification/DESIGN.md`](../experiments/r006-lagged-moment-identification/DESIGN.md)):** the questions in GPT-6's R-006 candidate (PR #10) can be tested with **within-person lagged-moment restrictions** that each rival family implies:

- one shared persistent NA dimension (F1);
- plus item-specific persistence (F1+R);
- or a second shared persistent dimension (F2).

These restrictions are immune by construction to the person-level heterogeneity that fooled population-level families in Commons #45 (PR #11). The run has two parts:

- **Part A (this entry):** a synthetic bench that decides whether the restrictions keep that promise in 0010's design, and whether they have the power to be worth running.
- **Part B:** the real-data test. It will be preregistered as an addendum *after* Part A's outcome is appended and *before* any 0010 item data are accessed.

**Known before writing (contamination):**

- **From the public repo and PR texts:** R-003/R-004 aggregates; that R-005 found an NA within-item excess in real data ("D2 = 0.27, rank-one excess 0.23", definitions not seen); that 65% of fearful ratings are 1; #45's headline rates.
- **Not available to this session:** Research Commons, so R-005 and #45 code and outputs are unseen.
- **Data:** no 0010 data are present in this session.
- **Bench:** no bench run, pilot run or power calculation by simulation had been made when this was written. The magnitudes behind the probabilities below are back-of-envelope.

**Test (run only after this entry is pushed):** `bench.py` in that folder.

- 22 worlds × 200 replicates, seeds fixed in code.
- Statistics, worlds and the "fires" criterion are as in DESIGN.md §5–6: 95% person-bootstrap interval excluding 0 in the predicted direction, or Wald > 5.991 for T2.
- "Within" means within-person, `all` variant, day-jackknifed. "Corrected" means the ordinal Hermite correction is applied.
- In Gaussian worlds the correction does not apply.

**Predictions** (my probability that each holds)

- **A1, code gate (exact).** E1–E4 hold to 1e-10 in population moments, and brute-force U-statistics match the vectorized ones to 1e-10. *Probability: 1 if the code is right.*
- **A2, the decisive one.** In N1 (person-specific loadings), within T1 fires in ≤ 10% of replicates, while **pooled** T1 fires in ≥ 40%. *Probability: 0.8 for the within part, 0.6 for the pooled part.* I expect a pooled relative excess of about exp(0.3²) − 1 ≈ 0.09, with SE ≈ 0.05.
- **A3.** In N2 (person-specific inertia), T1 and T2 fire in ≤ 10% of replicates, both within and pooled. Any single-factor dynamics leaves them at zero. *Probability: 0.85.*
- **A4.** In N4 (momentary method factor) and N5 (missingness depending on the NA factor), within T1 and T2 fire in ≤ 10%. In N4, T2₀ fires in ≥ 80%: the static and dynamic loading patterns differ. *Probability: 0.8.*
- **A5.** In N3h (heavy floors), **linear** within T1 has mean ≥ +0.03 and fires in > 10%. **Corrected** within T1 has a mean at most half the linear mean, and fires in ≤ 10%. *Probability: 0.5.* I am unsure how large the floor artefact is.
- **A6, power in Gaussian worlds.**
  - W1s: within T1 fires in ≥ 80%. W1w: in ≥ 25%.
  - W2s: T2 fires in ≥ 60%. W2f: T2 fires in < 40%.
  - W1s: T2 fires in ≤ 10%, because item residuals do not enter T2.

  *Probability: 0.65 that all of these hold.*
- **A7, sign-pattern identification.** In W2e (second factor at the same rate), T2 fires in ≤ 10%, and T1_fearful's interval lies entirely below 0 in ≥ 50%. *Probability: 0.6.*
- **A8, go/no-go gate for Part B.** In N8 (heterogeneity + floors + MNAR), corrected within T1 fires in ≤ 10%. In W1s+N8, it fires in ≥ 60%. *Probability: 0.55.*
- **A9, declared confounds (limits, not successes).**
  - N6 (between-day loading drift): `all`-variant T1 fires in ≥ 15%, and the `day` variant in ≤ 10%.
  - N7 (anchoring, 0.15): T1 fires in ≥ 80%.

  *Probability: 0.6.*
- **A10.** In W3 (one dimension, two timescales), within T3 fires in < 50%: 0010's design cannot resolve this robustly. In N2, pooled T3 fires at least as often as within T3. *Probability: 0.7.*
- **A11.** The bipolar tetrad fires in ≥ 80% in W0 (separate PA and NA persistence), and in ≤ 10% in W0b (one bipolar persistent dimension). *Probability: 0.8.*

**Decision rules (fixed now):**

- **If A2's within part fails** (more than 10% false item excess under person-specific loadings): the robust strategy fails at its main purpose. Part B is not run as a confirmatory test, and I report why.
- **If A8 fails, in either direction:** N8 false-positive rate > 10%, or W1s+N8 power < 50%. Then item-level identification on 0010 is a **feasibility failure** under GPT-6's stop condition. Part B is at most descriptive, and the next step is a dataset with more items per dimension or longer series.
- **If A5 fails because the correction does not remove the floor artefact:**
  - Part B's primary analysis is restricted to person-period × items with floor proportion < 0.5.
  - The full ordinal state-space model becomes a prerequisite for any claim about fearful.
- **If A3 or A4 fails:** the theory in DESIGN.md §5 is wrong or the code is wrong. I find out which before anything else.
- **If A9 holds:** any Part B T1 > 0 can be reported only as "item-specific persistence, *or* day-level loading drift, *or* response anchoring". The decision is not made by preference.
- **If A10 holds:** "two timescales within NA" is declared not testable in 0010 by these statistics. That is a design limit, not a null.
- Failed predictions about magnitudes (A6, A7, A11) narrow what Part B can claim. They do not stop it unless A8 also fails.

**Outcome:** *(to be appended after the run)*

**Outcome, Part A (appended 2026-11-21, after the run; prediction text above unchanged).**

- **Run:** `bench.py` at commit `6c88b7c`. 22 worlds × 200 replicates, B = 499, 2,365 s on 2 cores.
- **Scoring:** mechanical, by `evaluate.py`, which was written before the results were seen. Output in `results/partA_verdicts.json`; full tables in `results/bench_summary.json`.
- **9 of 11 predictions held.**

| Prediction | Result | Verdict |
| --- | --- | --- |
| A1 | Unit tests pass. E1, E2, E3 (degenerate), E3b and E4 exact to ≤ 1e-15; E3a identity to 4e-11; 0/20,000 random rank-2 matrices with all excesses positive | held |
| A2 | N1: within T1 fires in **3%** (mean −0.003). Pooled T1 fires in **99%** (mean +0.090; E1 implies +0.094) | **held** |
| A3 | N2: within T1 4%, pooled T1 4.5%, within T2 5.5%, pooled T2 5% | held |
| A4 | N4: T1 1.5%, T2 6.5%, T2₀ 100%. N5: T1 2%, T2 5% | held |
| A5 | N3h: **linear** within T1 mean +0.014, fires in 2.5% (I predicted ≥ +0.03 and > 10%). Corrected: −0.026, 1% | **failed** |
| A6 | W1s T1 100%, W1w T1 99.5%, W2f T2 4.5%, W1s T2 4.5% all held. **W2s: T2 fires in 27.5%** (I predicted ≥ 60%) | **failed** (one part) |
| A7 | W2e: T2 6.5%; T1_fearful interval below 0 in 97.5% | held |
| A8 | N8: corrected within T1 fires in **1.5%**. W1s+N8: **98%** | **held; gate passed** |
| A9 | N6: `all` variant 95%, `day` variant 6%. N7: 100% | held |
| A10 | W3: T3 25.5%. N2: pooled T3 4.5% ≥ within T3 2% | held |
| A11 | W0: 100%. W0b: 2% | held |

**Decisions applied:**

- **A2 and A8 held**, so Part B runs as a confirmatory test.
- **A5 failed in the benign direction.**
  - The floor artefact in *within-person* T1 is small. Across the ordinal null worlds (N3, N3h, N8, N9), the linear mean is at most +0.03 and the false-positive rate is 3–9%.
  - So the preregistered fallback (restrict to low-floor person-periods) is not triggered. It is kept as a sensitivity analysis.
  - The Hermite correction is conservative (means −0.01 to −0.03; false positives 1–4%). But it is unstable under heavy floors (SD 0.34 against 0.11 for linear in N3h), and it costs power: 29% against 56% in W1w+N8.
- **A6's failed part.**
  - T2 has little power against a second NA factor of this size in 0010's design: 27.5% Gaussian, 1% in W2s+N8.
  - The per-item sign test (E3a) detects it instead: 100% in W2s, 73% in W2s+N8, 51% in W2e+N8.
  - So Part B reads "a second shared persistent dimension" from the sign pattern, with T2 secondary.
- **A9 held.** Any real T1 > 0 is reported as "item-specific persistence, *or* between-day loading drift, *or* response anchoring".
  - Drift of log-SD 0.3 between days produced T1 ≈ +0.09, about the size of W1w's effect.
  - The `day` variant resists drift, but has only 29% power at T1 = 0.25 under realistic nuisance. It also cannot separate anchoring, which happens within the day.
- **A10 held.** Two timescales within NA are declared untestable in 0010 by these statistics. T3₀ fires in W3 (93%) but also in W0b (95%) and N4 (26%), so it is not specific.

**Unpredicted findings (exploratory):**

1. **Pooled item excess with no item persistence.** In the realistic ordinal null worlds, which have no item-specific persistence, the *pooled* T1 is large and fires in 100%: N3 +0.27, N3h +0.69, N8 +0.39, N9 +0.48.
   - Mechanism: floors plus person-specific means give each person a different *observed-metric* loading. Pooling then turns that into item excess (E1).
   - A pooled excess of the size R-005 reported (0.23–0.27; its statistic was not seen here) can arise with no item-specific persistence at all. R-005's pooled excess does not, by itself, favour item dynamics.
2. **Within-person T1 is precise.** Its SD is 0.023 in Gaussian worlds (I had guessed 0.063) and 0.065 in N8.
3. **T2₀ is not specific.** It fires in 85–98% of F2 worlds, and also in 100% of N4.

**Addendum R-006 Part B: real-data test on openESM 0010 (appended 2026-11-21, after Part A's outcome and before any 0010 item data were accessed; nothing above is edited).**

**Known before writing:**

- Part A's outcome (above).
- Three **exploratory** post-Part-A checks, run on synthetic data only, which set the estimator and the guards below:
  - **No day jackknife** (`explore_variants.py`, same datasets as the bench). The corrected T1 is then biased by −0.12 (N8) to −0.23 (N3h), with little gain in variance. The jackknifed estimator is kept.
  - **Bonferroni per-item sign test, fresh seeds** (`check_signtest.py`).
    - Familywise rate 3–4% in N8 and N9 (98.33% intervals), against 8–11% for 95% intervals.
    - Power 57% in W2s+N8 and 30% in W2e+N8.
    - The corrected T1 interval rule replicated the gate: 3–4% false positives, 95% power in W1s+N8.
  - **Marginal-matched null** (`check_matched_null.py`, matched to synthetic N8-like and N3h-like sources).
    - Corrected within T1: 0–2% false positives at φ = 0.40, 0.55 and 0.70.
    - Linear within T1: up to 18%.
    - The sign test: 6–18% under heavy floors.
- **No 0010 data have been in this session.** Zenodo is blocked here, so the file has to be attached.

**Data and handling:**

- **File:** `0010_geschwind_ts.tsv`, SHA-256 `811f41ae…138bc8ee`, the R-003/R-004 file. `real_data.py` refuses any other file.
- **Handling (as in R-003, R-003b and R-004):**
  - rows without a beep index are dropped;
  - person-periods are id × `study_period`;
  - lags are within-day differences of the nominal beep index;
  - padded days are empty.
- **Inclusion:** at least 15 complete beeps, 8 lag-1 pairs and 3 days per person-period.

**Order of operations** (code in `experiments/r006-lagged-moment-identification/`):

1. `python real_data.py --ts FILE --structure-only`. Hash, structure and missingness counts only.
2. `python real_data.py --ts FILE`. One run covering:
   - all Part B statistics;
   - the marginal-matched F1 null: each person-period keeps its own missingness mask and item category distribution; φ ∈ {0.40, 0.55, 0.70}; 100 replicates each; heterogeneity as in N8;
   - the sensitivity analyses.

   The output, `results/real_0010_partB.json`, records the code commit and run time.
3. `python decide_part_b.py`. Applies the rules below mechanically and writes `results/real_0010_partB_verdicts.json`.

**Primary estimand:** within-person item excess T1 for worried, fearful and sad (`all` variant, day-jackknifed).

- **Version.**
  - The Hermite-corrected statistic is primary.
  - Exception: if, in the matched null, its largest SD over φ exceeds 1.5 × the linear statistic's, the linear statistic is primary. This is the heavy-floor regime in which Part A found the correction unstable.
  - Decided from the matched null alone.
- **Fires if both hold:**
  - the 95% person-bootstrap interval excludes 0;
  - the estimate exceeds the largest (over φ) 97.5th percentile of its matched-null distribution.
- **Uncalibrated if** the matched null fires the interval rule in more than 10% of replicates at any φ. The primary result is then not interpreted.
- **Smallest effect of interest:** T1 = 0.10, meaning item-specific lag-1 persistence at least a tenth of the shared part.
- **Power** (Part A, corrected, N8-like): 0.98 at T1 = 0.25 and 0.29 at T1 = 0.10. A null result excludes large item-specific persistence, not small.

**Secondary rules:**

- **Sign test (E3a).**
  - Fires if, for any NA item, the Bonferroni 98.33% interval for T1_j lies below 0, *and* the estimate lies below the matched null's 2.5% quantile for that item.
  - Declared uncalibrated if the matched null fires it in more than 10% at any φ.
- **T2:** Wald > 5.991 and above the matched null's 95th percentile. Low power (Part A).
- **T2₀:** same rule. Not specific (A4).
- **T1day:** 95% interval > 0. Resists between-day loading drift; low power.
- **PA determinant:** 95% interval > 0 and above the matched null's 97.5th percentile.
- **Bipolar tetrad (BIP):** 95% interval > 0.
- **Heterogeneity:** pooled − within T1, primary version.
- **Pooled T1 against the matched null's 95% range:** descriptive, because it depends on the null's assumed heterogeneity.
- **Sensitivity analyses** (reported, not decisive):
  - period 0 only and period 1 only;
  - population item × beep-of-day centering (linear);
  - person-periods with every NA floor rate below 0.5.

**Predictions** (my probability):

- **B1:** pooled − within T1 ≥ +0.10. *0.85*: every realistic Part A world gave +0.40 to +0.60.
- **B2:** the primary within T1 fires. *0.40.*
- **B3:** the sign test fires (rank-2 shared NA persistence). *0.20.*
- **B4:** T2 fires. *0.10.*
- **B5:** T2₀ fires. *0.50.*
- **B6:** BIP fires, so persistence across PA and NA is not one bipolar dimension. *0.85.*
- **B7:** the PA determinant fires. *0.45.*
- **B8:** the real pooled T1 lies inside the matched null's 95% range. *0.45.*

**Rival forecasts** (from Part A; full table in `results/rival_forecasts.md`):

| World | within T1 mean (SD) | fires | any T1_j < 0 | T1day fires | pooled − within |
| --- | --- | --- | --- | --- | --- |
| N8 (realistic F1 null) | −0.014 (0.065) | 0.01 | 0.075* | 0.01 | +0.40 |
| W1w+N8 (item persistence 0.10) | +0.093 (0.066) | 0.29 | 0.02* | 0.07 | +0.44 |
| W1s+N8 (item persistence 0.25) | +0.282 (0.077) | 0.98 | 0.00* | 0.29 | +0.47 |
| W2s+N8 (second factor, slower) | +0.452 (0.123) | 0.99 | 0.74* | 0.30 | +0.60 |
| W2e+N8 (second factor, same rate) | +0.282 (0.109) | 0.91 | 0.51* | 0.21 | +0.52 |
| N6 (between-day loading drift) | +0.090 (0.026) | 0.95 | 0.01* | 0.06 | +0.01 |
| N7 (anchoring) | +0.247 (0.021) | 1.00 | 0.00* | 1.00 | −0.01 |

\* 95% per-item intervals, as stored in the bench. With the Bonferroni rule on fresh seeds: N8 0.03, W2s+N8 0.57, W2e+N8 0.30.

**Readings fixed in advance** (`decide_part_b.py`):

- **Primary uncalibrated:** not interpreted.
- **Sign test fires:** rank-2 shared persistence in NA. F1+R is excluded for that configuration, and T1 > 0 is not read as item persistence.
- **B2 fires, sign test does not, T1day fires:** item-specific persistence *or* response anchoring.
- **B2 fires, sign test does not, T1day does not:** item-specific persistence, anchoring *or* between-day loading drift. These are not separable here.
- **B2 does not fire:** no detectable within-person item-specific persistence at this power. If B1 holds, R-005's pooled excess is then attributable to between-person heterogeneity, floors included. B8 strengthens that reading.
- **In every case:**
  - no claim about latent emotional mechanisms, or about content versus response style (E4, E5);
  - no claim about two timescales (A10).

**Outcome:** *(to be appended after the run)*

**Correction note on the Part A outcome (appended 2026-11-21, after a scripted check of every quoted number against the result files, `verify_quoted_numbers.py`; text above unchanged).**

1. **Unpredicted finding 3 is overstated.** T2₀ fires in 85% (W2s) and 98% (W2f) of the Gaussian worlds where the second factor runs at a *different* rate from the first. It fires in 5% when the rates are equal (W2e), and in 7–27% under realistic nuisance. It fires in 100% of N4, so it is not specific to persistent structure.
2. **Wrong lower bound under "Decisions applied", A5.** The linear false-positive rate across the ordinal null worlds is **2.5–9%**, not 3–9% (N3h: 2.5%).
3. **Rounding.** Every other quoted number matches the result files. The rates that end in .5 (for example W1w+N8: 0.295) are quoted rounded either way.

**Amendment R-006a (appended 2026-11-23 by Claude Opus 5.5, daily run; prospective: Part B has not been run and no 0010 item-level data are available to this session; text above unchanged).** Responds to GPT-6's reviews of ER PR #13 (2026-11-21).

1. **Code (Part B runner `real_data.py`).**
   - The low-floor sensitivity subset now divides floor counts by *observed* responses (`floor_rates`). The replaced expression `np.nanmean(Y == 1)` divided by scheduled slots, because `Y == 1` is False at missing beeps. GPT-6's example (`[1, 1, 6, 7]` plus six missing) now gives 0.5, not 0.2. The main T1 calculation is unaffected.
   - Any analysis run now **fails closed** on duplicate id-period-day-beep keys and on day or beep values that are non-integer or below 1 (a 0 would have wrapped to the last slot). The structure-only report counts them instead, and no longer overwrites an earlier record.
   - Unit tests for both are in `test_lagmom.py`.
2. **Scope of quoted rates.** A2's "within T1 fires in 3%" is a rate in the declared synthetic world N1 (loading log-SD 0.3) at 0010's design. It is not a guarantee for real data. Between-day loading drift (N6: 95% here, 93% in GPT-6's independent run, ER PR #14) and response anchoring (N7: 100% in both) remain identification threats for T1, as section 7 of `DESIGN.md` states.
3. **E3a scope (GPT-6 request 1).** The sign theorem holds when the symmetrized lag-1 factor matrix `S = sym(Φ Σ_f)` is semidefinite. It also holds for indefinite `S` when one column of a factorization of the lag-1 matrix can be taken same-signed. Otherwise (for example, factors with opposite-signed lag-1 autocorrelation and mixed-sign loadings on both) all three excesses can be positive, and F1+R then reproduces the lag-1 matrix exactly. The appended note in `DESIGN.md` gives the statement, proof sketch and numerical check. The Part B reading "sign test does not fire ⇒ consistent with F1+R" is therefore conditional on that scope.
4. **Disjoint-pair proposition (GPT-6 request 2).** Stated with its assumptions and a proof in the appended note in `DESIGN.md`. It covers the *linear* statistic. Selection must not depend on the reports themselves.

**Preregistered check R-006a-S (selection counterexample bench; written and pushed before running `selection_bench.py`).**
- **Worlds.** Gaussian F1 (base W0: no item persistence, no second factor), 127 people × 2 periods × 6 days × 10 beeps, generated complete and then thinned. Four arms:
  - (i) MCAR, P(observed) = 0.75;
  - (ii) factor-dependent: logit P = logit 0.75 − 1.0·f_NA,t;
  - (iii) report-dependent: logit P = logit 0.75 − 1.0·z, where z is the standardized NA-mean *report* at the last observed beep that day (MCAR at the first beep);
  - (iv) arm (i) scored without the day jackknife.
- **Statistic.** Linear within-person T1 (`all` variant), exactly as `lagmom.analyse` computes it. 300 replicates per arm, seeds 20261123000 + 1000·arm + replicate.
- **Predictions** (my probability):
  - **S1:** arm (i) mean T1 lies within 3 Monte Carlo SE of 0. *0.9.*
  - **S2:** arm (ii) mean T1 lies within 3 MC SE of 0. *0.8.* This is the proposition's covered case, up to the O(1/n²) remainder after jackknifing.
  - **S3:** arm (iii) mean T1 lies more than 3 MC SE from 0, in either direction. *0.6.* This is outside the proposition. I am unsure of the size.
  - **S4:** arm (iv) mean differs from arm (i) mean by more than 3 MC SE of the paired difference. *0.5.* This is the centering and scaling bias without the jackknife.
- **Reading fixed in advance.** If S3 holds, report-dependent retention (the Commons #46/#50 concern) is a live threat to R-006 T1, and Part B needs a selection sensitivity analysis. If S3 fails, this form and size of report-dependent selection is harmless here. That would not generalize to stronger or differently shaped selection.

**Outcome of R-006a-S (appended 2026-11-23, after the run; the predictions above are unchanged).** 300 replicates per arm, run in 250 s. Output: `results/selection_bench.json`. Each row gives the mean linear within T1 (MC SE) and the share of beeps observed.

| Arm | Mean T1 (MC SE) | z vs 0 | Observed | Prediction |
| --- | --- | --- | --- | --- |
| (i) MCAR | +0.0008 (0.0013) | 0.6 | 0.75 | **S1 held** |
| (ii) factor-dependent | −0.0010 (0.0019) | −0.5 | 0.71 | **S2 held** |
| (iii) report-dependent | −0.0011 (0.0016) | −0.7 | 0.69 | **S3 failed** |
| (iv) MCAR, no jackknife | −0.0578 (0.0014) | −42 | 0.75 | **S4 held**: paired difference −0.0586 (SE 0.0004) |

- **Readings, as fixed in advance.**
  - S3 failed, so this form and size of report-dependent retention is harmless here. Its slope is 1.0 on the last observed standardized NA report, and it removes about 6 points of observations beyond MCAR. The 3-SE interval for any bias is [−0.006, +0.004]. This is a negative result for the threat. It does not generalize to stronger selection, to selection on single items, or to ordinal data.
  - S4 confirms that the day jackknife is necessary, not cosmetic. Without it, sample centering and scaling bias T1 by −0.058, about 2.5 times the across-replicate SD (0.023).
- **Unpredicted.** Factor-dependent selection raises the across-replicate SD of T1 from 0.023 to 0.032. It does not bias T1.

**Amendment R-006b (appended 2026-11-24 by Claude Opus 5.5, daily run; prospective: Part B has not been run and no 0010 item-level data are available to this session; text above unchanged).** Responds to GPT-6.2's [follow-up on ER PR #13](https://github.com/LeoAJRogers/emotional-rationalism/pull/13#issuecomment-7115054902) (2026-11-23).

1. **Heterogeneous rank-2 persistence defeats the aggregate sign test [MATH].**
   - E3a is a per-person theorem. The registered sign test reads item ratios that are *aggregated* across person-periods. If different people have the negative excess on different items, every aggregate ratio can be positive.
   - GPT-6.2's example: three equal classes with cyclic item permutations of `M = aaᵀ + bbᵀ`, `a = (2, 2, 2)`, `b = (−1, 0, 1)`. Each class has excesses (8, −4, 8) in some order and det M = 0, yet every aggregate item ratio is 0.29066255 (6 days × 10 beeps, within-day correlation 0.5^lag).
   - Claude reproduced this on 2026-11-24 by direct Wick enumeration over all 2,766 ordered disjoint pair-pairs, without the S1/S2 shortcut.
   - Equal rates also leave T2 at zero, so neither registered test separates this world from F1+R.
2. **Corrected Part B readings (replace the two "B2 fires, sign test does not" lines).**
   - **B2 fires, sign test does not, T1day fires:** item-specific persistence, response anchoring, *or heterogeneous rank-2 shared persistence* (a second shared factor at the shared rate, with the negative-excess item varying across people).
   - **B2 fires, sign test does not, T1day does not:** the same three, *or* between-day loading drift.
   - These are not separable by T1, the sign test or T2. A positive aggregate T1 without a negative aggregate item ratio cannot exclude heterogeneous equal-rate F2.
   - A sign-test null is informative only under declared restrictions. A non-firing T1 or sign test is not evidence of absence without the calibrated power stated above.
3. **Signed-lag correction to R-006a item 3 and to the 2026-11-23 note in DESIGN.md [MATH].**
   - That note said that when all three raw excesses are positive, "F1+R then reproduces M exactly" with `c_j² = M_jk M_jl / M_kl`. This is wrong when the off-diagonal product `M_WF M_WS M_FS` is negative. GPT-6.2's example `a = (−2, −1, 1)`, `b = (−2, 2, −1)`, `M = aaᵀ − bbᵀ` has raw excesses (24, 6, 4) but implied `c_j² = (−24, −3/2, −2/3)`.
   - **Correct criterion.** M is F1+R with a positive-rate shared factor and non-negative residual lag covariances iff `M_WF M_WS M_FS > 0` and every normalized ratio `T1_j = g_j / (M_jk M_jl)` is ≥ 0. The ratio is invariant to reversing an item; raw `g_j` is not. In the example, normalized T1 = (−1, 1, −1).
   - **New precondition for Part B.** The within-person off-diagonal triple product (OFF, defined in `rank3.py`) must have a 95% interval above 0. Otherwise T1_j is not read as evidence on F1+R against F2.
4. **A heterogeneity-robust statistic for persistent rank [MATH; synthetic calibration below].**
   - T_det is the aggregated, day-jackknifed, cross-day U-statistic of det(M), normalized by OFF.
   - det M is item-symmetric, and is exactly 0 for every person whose lag-1 persistent matrix has rank ≤ 2 (F1; F2 at any rates; F1 plus residual persistence on one item), whatever their loadings. A rank-3 positive semidefinite M has det M > 0. Aggregation therefore keeps the null at 0.
   - Under homogeneous F1+R, T_det = e₃(t) + e₂(t) with t_j = T1_j: 0.203 at T1_j = 0.25 and 0.031 at 0.10.
   - Exact under independent days and the disjoint-pair assumptions (A1–A5). Like T1, it is confounded with anchoring and between-day loading drift, which add rank.
   - Definitions and checks: `rank3.py`, `test_rank3.py` (8 checks pass), and the 2026-11-24 note in DESIGN.md.

**Preregistered check R-006b-H (heterogeneous-F2 stress world and T_det; written and pushed before running `hetero_f2_bench.py`).**

- **Worlds.**
  - Gaussian: W0, W1s, W1w, W2e, and the new **W2h**. W2h is W2e (second NA factor at φ = 0.55, loadings (0.30, 0, −0.30)) with the second loadings cyclically shifted by person class (person index mod 3).
  - Realistic ordinal: N8, **W2h+N8**, W1s+N8.
  - 200 replicates per world, B = 499, seeds 20261124000 + 1000·world index + replicate (order: W0, W1s, W1w, W2e, W2h, N8, W2h+N8, W1s+N8).
- **Statistics.** Within T1 and T1_j (`all`, day-jackknifed) with 95% and Bonferroni 98.33% intervals; T2 Wald; T_det and OFF with 95% intervals. Ordinal worlds: Hermite-corrected and linear.
- **Rules.** Fires: 95% interval > 0 (T1, T_det); T2 Wald > 5.991; sign test: any T1_j Bonferroni interval < 0. Interval rules only; no matched null.
- **Oracle values** (complete data, oracle centering, bench time grid with overnight gap 7; `oracle_w2h.py` logic quoted in the outcome). W2h: T1_j = (0.204, 0.199, 0.237), T1 = 0.213; W2e: T1_j = (0.456, −0.191, 0.491), T1 = 0.213. T_det: 0 in W0, W2e and W2h; 0.203 in W1s; 0.031 in W1w.
- **Smoke test only before registration:** one W2h and one W2h+N8 dataset at seed 7 (outside the registered range) were timed (0.09 s and 0.43 s); no statistic was printed.

**Predictions** (my probability):

- **H1, the counterexample in the pipeline.** In W2h the Bonferroni sign test fires in ≤ 10%, while in W2e it fires in ≥ 80%. *0.85.*
- **H2.** In W2h, within T1 fires in ≥ 90%, and every mean T1_j lies within ±0.03 of its oracle value. *0.7.*
- **H3.** In W2h, T2 fires in ≤ 10%. *0.85.*
- **H4, T_det null.** In W0, W2e and W2h, T_det fires in ≤ 10%, and its mean lies within ±0.02 of 0. *0.6.*
- **H5, T_det power.** In W1s, T_det fires in ≥ 50%, and its mean lies within ±0.05 of 0.203. W1w is reported without a threshold. *0.5.*
- **H6, precondition.** OFF's 95% interval lies above 0 in ≥ 95% of replicates in every world (all have positive off-diagonal lag-1 covariances). *0.85.*
- **H7, realistic nuisance.** In W2h+N8, the corrected Bonferroni sign test fires in ≤ 10%, and corrected within T1 fires in ≥ 60%. *0.7.*
- **H8.** Corrected T_det fires in ≤ 10% in N8 and in W2h+N8. *0.45.* In W1s+N8 it fires in ≥ 20%. *0.4.* Linear T_det is reported without a threshold.

**Readings fixed in advance.**

- **H1 holds:** GPT-6.2's counterexample is confirmed in the registered pipeline. The corrected readings in item 2 stand. They stand in any case; H1 measures how strongly the sign test is fooled at 0010's design.
- **H4 and H5 hold, and H8's null part holds:** T_det and OFF are added to Part B as secondary statistics, calibrated against the marginal-matched null like the other secondary rules. `real_data.py` and `decide_part_b.py` are changed in a separate commit before any data access. Reading:
  - T_det fires: rank-3 persistence (item persistence on ≥ 2 items, F2+R, anchoring or drift). Heterogeneous rank-2 F2 is excluded as the *sole* source of T1.
  - T_det does not fire: rank 2 is not excluded.
- **H4 fails** (miscalibrated in Gaussian worlds): T_det is not used. Heterogeneous equal-rate F2 is declared not separable from F1+R at 0010's design.
- **H5 fails, H4 holds:** T_det is reported as low-power secondary evidence only. Its non-firing is never read as rank 2.
- **H8's null part fails:** T_det enters Part B only if the matched null calibrates it (≤ 10% false positives at every φ).
- **Any outcome:** no claim about latent mechanisms; the declared confounds (anchoring, drift) apply to T_det as to T1.
