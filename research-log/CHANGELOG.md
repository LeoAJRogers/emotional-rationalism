# Research log

## 2026-11-23 · R-006a: fixes and scope after GPT-6's review (Claude Opus 5.5)

- **Code fixes** to the Part B runner:
  - The low-floor sensitivity rate now uses observed responses as its denominator; it had been counting scheduled slots.
  - Any analysis now fails closed on duplicate keys and on invalid day or beep values.
  - Both were found by GPT-6 on PR #13. Part B is still unrun.
- **Scope of the sign theorem E3a.** It holds for semidefinite lag-1 factor matrices. It also holds for indefinite ones when one loading column is same-signed. Otherwise, factors with opposite-signed lag-1 autocorrelation can produce an all-positive excess pattern that F1+R reproduces exactly, and T2 must then separate them. The 2026-11-21 entry below states E3a without this scope.
- **The disjoint-pair claim** is now stated as a proposition with its assumptions and a proof (DESIGN appended note).
- **Preregistered selection check (R-006a-S), synthetic.**
  - Within-person T1 stayed unbiased under MCAR and under factor-dependent retention. Both predictions held.
  - It also stayed unbiased under one form of report-dependent retention, which I had predicted would bias it. That prediction failed, and the negative result is kept.
  - Without the day jackknife, T1 is biased by −0.058. That prediction held.
- **Integration Delta:** not assigned. These are method corrections; the public evidence ledger is unchanged.

## 2026-11-21 · R-006 revised; Part A run; Part B preregistered (Claude Opus 5.5)

- **Design change.** Replaced the population-level model race in GPT-6's R-006 candidate (PR #10) with within-person lagged vanishing-tetrad restrictions. These are robust by construction to the person-level heterogeneity that fooled population families in Commons #45 (PR #11).
  - [Design](../experiments/r006-lagged-moment-identification/DESIGN.md).
  - It includes an identification map, E1–E5, with a new sign theorem (E3a): in a 3-item set, a second shared persistent dimension always leaves some item with non-positive excess.
- **Part A: a synthetic bench, preregistered before any code ran.** 22 worlds × 200 replicates; 9 of 11 predictions held.
  - **Robustness.** Under person-specific loadings, within-person item excess fired in 3% of datasets and the pooled version in 99%.
  - **Floors.** With no item-specific persistence at all, pooled excess of +0.27 to +0.69 arose from floors plus heterogeneity.
  - **Failed predictions:** the floor artefact in the within-person statistic was smaller than predicted, and the rate-difference test T2 was underpowered.
- **Part B: the 0010 real-data test.** Preregistered, with marginal-matched null guards and decision rules in code. **Not run:** the data file cannot be reached from the session.
- **Report and data.** See the [pass report](2026-11-21-claude-r006-pass.md). No human data were used; no participant-level data were committed.
- **Integration Delta:** not assigned. This is a method and design change; the model scaffold and the public evidence ledger are unchanged.

## 2026-11-20 · public evidence integration checkpoint (GPT-6, following Claude reviews)

- Reviewed and integrated the [R-001–R-004 prediction register](prediction-register.md), with original preregistered wording and dated corrections retained. Merged the Sonnet review/contribution note and reviewed register PRs before this synthesis.
- Published the [integration checkpoint](2026-11-20-public-integration-checkpoint.md), separating model-prediction gains, synthetic identification limits, real-data observed outcomes and causal claims. R-003's “slow state” reading was narrowed; R-004's “fraction caused by a period change” was corrected to overlapping predictive gain with uncertainty.
- Recorded GPT-6's independent numerical R-003/R-004 reproduction, including same-dataset and private-code limitations; no human data or participant-level records were committed.
- Kept candidate architecture PR #4 and exploratory item-level R-005 work outside the integrated evidential core. No new experiment was run in this integration; the next-test queue is intentionally paused.
- **Integration Delta (IΔ): 2/5** — meaningful interpretation/method revision, without replacement of the three-part mathematical scaffold. This is a change-magnitude score, not a quality grade.

## 2026-11-20 · proposed core statement and prediction register (Claude Opus 5.5, under cross-agent review)

- Proposed a one-sentence current core in the README, pointing to draft PR #4 as the candidate architecture. `main`'s v0.2 text is otherwise unchanged.
- Added a [prediction register](prediction-register.md), with entries R-001 to R-003 each written before their tests. R-001 covers the reporting-scale rivals (held). R-002 covers the sparse-sampling selection margin (held). R-003 is the **first real-data test**, on openESM 0010: all predictions held, followed by a correction note after GPT-6's review. Results are in research-commons #38 and #39.
- **Integration Delta:** not assigned. These are process additions, not model changes.

## 2026-11-20 · Informal collaborators and consent-first attribution

- Documented that friendships and personal conversations helped shape some research ideas, questions, and conceptual development.
- Added a [plan for acknowledging informal collaborators](../CONTRIBUTIONS.md): seek individual permission before names or specific attributed contributions appear; allow pseudonymous or anonymous acknowledgment; distinguish contributions, scholarly authorship, and GitHub access.
- No people were identified, presumed to consent, or granted repository access. This is a provenance and collaboration-policy update, not a revision of the scientific model.

## 2026-11-19 · v0.2 — scope and provenance clarification

- Clarified that the formal affect model is a narrow starting case of a broader proposed program on context, interaction, history, and persistent state.
- Added [research scope](../theory/research-scope.md), distinguishing contextual association, causal influence, and adaptation and defining limits of social/reflective extensions.
- Updated the README without claiming that the wider scaffold has been empirically validated or that every state-change process requires evaluative fittingness.
- Expanded [contribution notes](../CONTRIBUTIONS.md) to reflect an extended, reciprocal human–AI research process and preserve the privacy of personal conversations.
- **Integration Delta (IΔ): 3/5** for this scope and presentation change (magnitude only, not evidence quality). The initial mathematics itself was not replaced.
- Next: operationalize measurable variables, establish observation models and synthetic parameter-recovery benchmarks, and compare added mechanisms against simpler baselines.

For the earlier, narrower local review, see [public integration review](2026-11-19-public-integration-review.md) (IΔ 2/5).

## 2026-11-18 · v0.1

- Reconstructed the first public draft from the proposal discussion.
- Defined separate models for affect dynamics, fittingness, and finite-horizon reachability.
- Derived a two-state example illustrating a horizon-dependent reachability gap.
- Outlined a belief-to-affect lag study and identified simpler predictive baselines.
- Open questions include parameter identification, measurement validity, and empirical comparison with existing models.
