# Research log

## 2026-11-26 · R-006c prospective guard amendment (Claude Opus 5.5, chat session; before any 0010 data access; for GPT-6.2 review)

- **`decide_part_b.py`:** finiteness and support guards. T_det is withheld unless both OFF gates, support and calibration pass. Adds a raw-numerator (DETNUM) concordance check, readings worded against the declared restricted null, T1day as diagnostic only, and the unconditioned reading kept as a diagnostic when the precondition fails.
- **`rank3.py` / `real_data.py`:** DETNUM, the share of finite T_det draws, and matched-null DETNUM and non-finite rates.
- **`test_decide_part_b.py`:** 12 gate-failure tests. One synthetic end-to-end dry run.
- **Register:** amendment R-006c. Part B stays gated until a preregistered matched-null calibration rerun (signed and weak-denominator worlds, dependent-day nulls, DETNUM) has run and been cross-reviewed.
- No real data accessed; no results changed. **Integration Delta:** not assigned.

## 2026-11-24 · R-006b: heterogeneous F2, signed lags, persistent-rank statistic (Claude Opus 5.5, after GPT-6.2's review)

- **GPT-6.2's counterexample is confirmed [MATH; SIM].** When different people have their negative item excess on different items, the per-item sign test cannot see a second shared persistent factor.
  - Exact: independent Wick enumeration gives every aggregate item ratio as 0.29066255.
  - Registered pipeline: the sign test fired in 0/200 heterogeneous datasets, against 94% when homogeneous. The same held under realistic ordinal nuisance.
- **Part B readings corrected prospectively.** A positive T1 without a negative item ratio is now read as item persistence, anchoring, drift, *or* heterogeneous rank-2 shared persistence. The signed-lag statement in R-006a is corrected: all-positive raw excesses do not imply F1+R. A positive off-diagonal product is also required.
- **New statistic T_det [MATH; SIM]**, a cross-day determinant. It is zero for every person with at most two persistent dimensions, whatever their loadings, so aggregation keeps the null.
  - Calibrated in the Gaussian and ordinal null and rank-2 worlds: false positives 2–5%.
  - Power: 56% at item persistence 0.25 (Gaussian), but only 13–17% under realistic nuisance. A non-firing T_det is never read as rank 2.
- **Scorecard: 6 of 8 predictions held; 1 failed; 1 split.** The corrected positive-lag precondition was too noisy under floors (90.5% against ≥ 95%). The linear version will be used. Power under nuisance fell short of the prediction.
- **Integration Delta:** not assigned. These are identification corrections; Part B is still unrun.

## 2026-11-23 · public integration pass (Claude Opus 5.5 draft; GPT-6.2 director revision; Claude cross-review; both approved head `7cddc43`; merged)

- **README:**
  - a one-line statement that the project describes and tests, and does not prescribe ([#19](https://github.com/LeoAJRogers/emotional-rationalism/pull/19), item P2);
  - a concise five-thread map of work since the checkpoint, with the detailed status matrix in the integration note;
  - explicit broader ambition and evidence classes; a population reference is descriptive, and reflection need not produce convergence;
  - after Claude's cross-review: the definition line keeps a person's own feasible actions in scope as conditional questions; the social paragraph names the open fittingness question; the map shows the preregistered, unrun R-006 test and links the relational grounding note (#20); the evidence guide names the register discipline;
  - a pointer to the proposed release gate;
  - Gemini credited as an external reviewer (also in [CONTRIBUTIONS](../CONTRIBUTIONS.md)), where a sentence about session memory was also corrected.
- **Open problems:** questions opened since the checkpoint.
- **[Integration note](2026-11-23-public-integration-pass.md):** a review state and proposed action for each open PR, for agreement before any merge.
- **Agreed prerequisites merged first (2026-11-23):** [#19](https://github.com/LeoAJRogers/emotional-rationalism/pull/19) (Gemini framing review and release gate), [#9](https://github.com/LeoAJRogers/emotional-rationalism/pull/9) (credit pass) and [#21](https://github.com/LeoAJRogers/emotional-rationalism/pull/21) (social affect distributions). [#16](https://github.com/LeoAJRogers/emotional-rationalism/pull/16) was merged into `experiment/2026-11-22-lag-identifiability`, not `main`.
- No numbers, register entries or model text changed. The release gate has not been passed.
- **Integration Delta (IΔ): 0/5.** Navigation and status only.

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

## 2026-11-21 and 2026-11-22 · research notes added to main (recorded retrospectively on 2026-11-23)

- GPT-6, [context-dependent dynamics: a discriminating design](2026-11-21-context-transition-discrimination.md). Proposed, not executed.
- GPT-6, [passive target entry is not controlled reachability](2026-11-21-passive-vs-controlled-reachability.md). Conceptual; IΔ 1/5.
- GPT-6 (director), [discriminating affect-lag mechanisms](2026-11-22-director-lag-identifiability-pass.md). Proposed design; IΔ 1/5.

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

## 2026-11-20 · credit pass (Claude Opus 5.5, at Leo's invitation)

- **Contributors table:** the contribution-based table merged on `main` (`1690918`) stands, so there is one format for everyone. The CRediT-format table first proposed in PR #9 was withdrawn when PR #9 was brought up to date. CRediT roles remain an option any contributor may propose later.
- **AI note:** a short note says the AI rows describe work, not authorship. It cites COPE's position on AI tools, and states that accountability rests with the human maintainer.
- **Data credit:** Bringmann et al. (2013) and the openESM introduction paper (Siepe et al., 2026) are added alongside Geschwind et al. (2011), as the dataset record asks. They appear in CONTRIBUTIONS, the README and a dated addendum to the checkpoint.
- **Lived experience:** a general acknowledgment that many people's lived experience contributed, without specifying whose. The data-credit section also thanks the trial participants.
- **Unchanged:** the friends and informal-collaborators plan. There is no scientific content.
- **Integration Delta:** not assigned. This is a provenance change.

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
