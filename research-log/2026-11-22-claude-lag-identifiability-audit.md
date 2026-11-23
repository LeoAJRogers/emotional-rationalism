# Independent methods audit: lag identifiability (2026-11-22)

**Author:** Claude Opus 5.5, working independently of the director passes (no other review seen). **Status:** synthetic re-analysis, exact counterexamples and a design proposal. No human data and no empirical claim. **Reviewed:** branch `experiment/2026-11-22-lag-identifiability` at `2d75bd9`. `unknown_loading.py` and the Pass III script were not available, so Pass IV is re-scored from its published matrices and re-implemented from its description. **Reproduce:** `python -I experiments/lag-identifiability/lag_audit.py` (NumPy only, about 80 s).

Tags: **[MATH]** algebraic identity, checked numerically; **[ARITH]** arithmetic on published numbers; **[SIM]** Monte Carlo under the stated synthetic assumptions. Nothing here is **[EMPIRICAL]**.

## Summary

1. **The equivalence is broader than stated.** With the report loading free, A is nested in M, so an "affect" call is never evidence against report lag, in any row. If the proxy may also respond to the cue or belief directly, A and M have identical observable sets for every parameter value.
2. **Pass IV's counts mix identification with defaults.** On the published matrices, identified calls are 38, 36, 32 and 19 out of 60, against the published 56, 54, 50 and 42 correct.
3. **"Correlated errors" covers two different threats.** Cue-locked shared errors create exact equivalences. Cue-independent ones leave estimates unbiased but degrade selection and calibration.
4. **The cheapest discriminator is a manipulation of the report's anchor, not another channel.**

## 1. Structural equivalence

- [MATH] E1–E3 as stated in the docs hold exactly in the benchmark skeleton (max difference ≤ 1.1e-16).
- [MATH] **General form (E7).** With linear time-invariant stages, report-only data identify only the product of the stage filters. Stage placement is never identified, even with unequal lags: a .6 affect lag followed by a .9 report lag equals the swap (3e-16). A nonlinearity between stages breaks this. With a bounded report the difference is up to .24 (E7b). A cue-amplitude manipulation could therefore carry information, but only once the nonlinearity's location is declared.
- [MATH] **Nesting.** With the loading free on [0, 1], M at loading 1 reproduces A exactly. In-sample, M fit A-truth at least as well as A in 100% of sequences. An affect call can only come from a tie-break or a parsimony effect of held-out selection. [SIM] Among A-truth sequences, 56% were exact ties broken by list order, 20% had A better on the selection split, and 21% had M better.
- [MATH] **Mirror (E4).** Suppose the proxy carries a direct cue/belief component α, for example orienting or appraisal-driven physiology. Then A with α is identical to M with loading 1−α, for every α. Once both contaminations are allowed, the proxy carries no A-vs-M information. Pass IV's positive rows depend on assuming the proxy may read the report but not the cue/belief. More generally, whichever model has the free loading absorbs the other. A proxy separates the two in both directions only if its cue/belief and report loadings, and its own kinetics, are fixed by independent calibration.
- [MATH] **Proxy kinetics (E6).** Take M-truth with a report-free proxy whose own lag equals the report lag. It is exactly A.
- [MATH] **Process noise will not rescue the 100% row (E3b).** At loading 1, M's affect-level noise w reaches the observables only through the report filter. So M equals A with innovation (1−k)w + u, pathwise, which means equal in distribution with innovation variance (1−k)²σ_w² + σ_u². The planned process-noise pass should be expected to leave that row unidentified.
- **Notation.** The director pass gives A and B a one-step input delay (z_{t+1} uses g(b_t)) that M lacks (y_{t+1} uses z_{t+1}). Implemented literally, this dead time would spuriously separate M from A in report-only data. `benchmark.py` aligns the timing correctly; the note's equations should be aligned too.

## 2. Leakage, ties and selection

- **No data leakage was found in `benchmark.py`.** The confusion matrices are scored against known labels, with no tuned thresholds. Scoring classification on the selection split is therefore not leakage; the docs' caveat applies only to predictive scores of the selected model. The real optimism is oracle alignment: the generator is in the candidate set, the true lag is on `benchmark.py`'s grid, and Pass IV's generating loadings (0, .5, .75, 1) are on its grid. That includes the boundary value 1, which makes ties exact. The cue and initial state are also known, and fitting uses the same noise model as generation.
- **Ties.** `np.argmin` gives every exact tie to the first-listed kind (affect). The README flags this for report-only, but the patched benchmark shows the belief + report cell is half ties too. At stride 1 it has 30 unique correct calls and 60 exact ties; at stride 4, 59 ties and 1 unique wrong. ROBUSTNESS's 39/60 rows presumably also contain 20 tie-breaks, because A and M coincide on belief and report.
- [ARITH] **Pass IV re-scored by observational class.** "Identified" means the call is the truth and no other candidate reproduces it. "Unidentified" means the call lies inside an exact equivalence class. "Wrong" means it lies outside.

  | report fraction | published correct | identified | unidentified | wrong |
  |---|---:|---:|---:|---:|
  | 0 | 56 | 38 | 20 | 2 |
  | .5 | 54 | 36 | 20 | 4 |
  | .75 | 50 | 32 | 20 | 8 |
  | 1 | 42 | 19 | 39 | 2 |

  [SIM] In the re-implementation (300 sequences per mechanism), identified calls were 64%, 63%, 58% and 32%. The order-rule "correct" rates were 90%, 89%, 84% and 64%.
- **Pass III and Pass IV are not on one scale.** With the loading supplied and below 1, A is refutable; with it free, A is not. At 0%, the change from 58 to 56 "correct" hides a fall from about 58 to 38 identified calls.
- **Common random numbers.** Pass IV's A and B rows are identical in all four conditions. Differences in "correct/60" therefore come from 20 report-true sequences.
- [SIM] **Uninformative selection windows.** Every wrong call at loading 0 had at most one cue switch in the 48-point selection window, against 35% of all windows. `benchmark.py`'s two unique misses fall in test windows with no switches, where the three held-out scores lie within 2e-5 of each other (MSE about .011–.016). A cue schedule that guarantees switches in each evaluation window would fix this, as would blocked cross-validation over the whole sequence.
- **Stride thins the data; it is not a manipulation.** Every recursion, including the report lag, runs at unobserved steps, so stride only removes observations. That is why strides 1 and 4 agree. A report lag anchored on actual answers would make prompt timing informative (Section 4).
- **Reproducibility.** On NumPy 2.5.3, `benchmark.py` gives 89/90 at stride 1 with all channels, where the README says 90/90. The extra miss is one belief→report call in a zero-switch window. The patch prints the NumPy version.

## 3. Correlated-error rivals

**(a) Cue-locked shared error: the identification threat.**

- [MATH] Consider a proxy that never reads the report but shares a lagged method component with it, such as a slowly updating response set, demand, or matched kinetics. Its skeleton is the same as report loading λ: a share c behaves exactly like λ = c. Pass IV's "report fraction" is really the proxy's share of the report's cue-locked error. Showing that the proxy cannot read the report, for instance by recording it before the rating, does not rule out λ > 0.
- [SIM] **Mirror direction.** A-truth with cue reactivity α = .25 is called "report lag" in 75% of sequences at noise SD .4, and in 95% at SD .12. Less noise makes it worse, so this is bias, not lack of power. When A is given the same freedom (α free), A and M had identical validation scores in 100% of sequences.

**(b) Cue-independent shared error.** Report and proxy share an AR(1) component: φ = .9, 80% of variance shared, marginal SD .4.

- [MATH] With the cue randomized independently of every error, the skeleton estimates stay consistent for any error covariance. This is the standard output-error result and needs a persistently exciting cue.
- [SIM] Lag estimates stay unbiased (mean .778 in every condition), but their SD rises from .017 to .039. Wrong calls rise from 3.3% to 5.1% at loading 0, and from 9.6% to 11.6% at .75. Under the iid likelihood, the share of wrong calls with a nominal likelihood ratio above 20 rises from 0% to 20% at loading 0, and from 3.5% to 17% at .75.
- [SIM] Scoring with the contemporaneous error covariance, estimated from training residuals, cuts wrong calls below the iid level (2.3% and 8.0%). The shared component cancels in the proxy-minus-report contrast. But more of the remaining errors look confident (48% and 31%) unless temporal dependence is modelled as well, for example with state-space error terms or a block bootstrap.

## 4. Cheapest discriminating manipulation

Manipulate the report process rather than adding channels. Physiology is the expensive route, and by §1 it separates A from M only under calibration assumptions as strong as the conclusion.

**Proposal (no new instrument).** Each trial starts with a pre-cue rating. The cue (switch or stay) and the starting level (±) are randomized. The first post-cue rating follows a randomized delay with no ratings in between. It uses either the same item (repeat) or a parallel item this person has never answered (fresh), at random.

- Clock-time lags (A, B, and the repo's M) predict the same cue effect on both items.
- A rating anchored on its own last answer predicts a larger effect on the fresh item.
- Test: the difference between items in the scale-free normalized cue effect, 1 − mean(switch)/mean(stay), after sign-aligning by starting level.

[SIM] Rejection rates at .05, from 1,000 simulated studies per cell. Item loadings are N(1, .1²) per trial, with item roles randomized.

| mechanism | 160 trials | 640 trials |
|---|---:|---:|
| A, affect lag | 6.8% | 5.7% |
| A + prompt reactivity .3 | 5.0% | 4.6% |
| A + fresh item read ×1.1, offset +.2 | 5.7% | 4.1% |
| M, anchored on last answer (.78) | 100% | 100% |
| M, anchor fading .78 per step | 98.7% | 100% |
| M, weak anchor (.3), fading | 44.3% | 96.3% |
| repo's clock-time report lag | 4.5% | 4.8% |

Negative results and caveats:

- A naive cue × item regression without the randomized starting level gives 15% (160 trials) and 47% (640 trials) false positives for the fresh-item scale shift; the ratio test removes them.
- The delta-method ratio test is slightly liberal at 160 trials (6.8%). Use a permutation test in a real analysis.
- Delay alone does not separate a fading anchor from affect lag; their repeat-item curves nearly coincide.
- A zero-cost, repeatable variant on the same item: randomize whether the slider starts at the previous answer or at a neutral point. This targets visual anchoring only.
- **Not discriminated, and to be recorded:** a report process that relaxes in clock time without being tied to the answers (the benchmark's M) is equivalent to an affect stage under any report-only design.
- Separating B from A needs the belief probe, and the probe needs the same anchor control, because a belief rating anchored on its last answer mimics belief lag.
- Assumptions: items are parallel up to scale and offset; items are momentary ("right now"); the cue comes immediately after a prompt; item novelty does not interact with the cue beyond scale and offset; trials are independent (no person-level structure was simulated).

## Requests

1. `unknown_loading.py` and the Pass III script, to check:
   - candidate order and tie rule;
   - whether the proxy mixes the *noisy* observed report ("shared report/proxy noise");
   - whether any candidate plugs observed channels into its predictions;
   - the cue generator and seeds;
   - which split produced the confusion matrices.

## Proposed changes

1. Report set-valued outcomes (identified, unidentified, wrong, plus exact ties) instead of argmin accuracy. The included `benchmark.py` patch adds a tie-aware line without changing the existing output.
2. In any proxy follow-up, give A the same proxy freedom as M (cue/belief loading and its own kinetics), or state the asymmetry as an assumption.
3. Make the anchor manipulation the next A-vs-M step, ahead of physiology.
4. Align the timing of the director note's equations.

**Suggested IΔ: 2/5.** This re-reads the Pass III/IV results and changes the next measurement priority, with no change to the formal scaffold.
