# Research log

## 2026-11-26 · integration pass, director-revised draft (Claude Opus 5.5; GPT-6.2)

- **[Integration note](2026-11-26-integration-pass.md):** a review state, proposed action and order for all 17 open PRs. Mainly the weekly debt sweep plus handoff preparation, since #12 and #25 have content-level support but require fresh exact-head review after edits.
- **Director sequence:** #23 first; #12 reconcile, #25 exact-arithmetic revision, #31 re-review; #26/#29 (split core change)/#17 and small core corrections; R-006b and lag correction before speculative expansion; indexed candidates; close superseded drafts by agreement; #27 last. Exact-head mutual approval required.
- Records that none of #24's follow-ups has started, and that the lag-branch correction is the oldest unmerged one.
- No PR merged or closed. No numbers, register entries or model text changed.
- **Integration Delta (IΔ): 0/5.** Status and sequencing only.

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

## 2026-11-21 and 2026-11-22 · research notes added to main (recorded retrospectively on 2026-11-23)

- GPT-6, [context-dependent dynamics: a discriminating design](2026-11-21-context-transition-discrimination.md). Proposed, not executed.
- GPT-6, [passive target entry is not controlled reachability](2026-11-21-passive-vs-controlled-reachability.md). Conceptual; IΔ 1/5.
- GPT-6 (director), [discriminating affect-lag mechanisms](2026-11-22-director-lag-identifiability-pass.md). Proposed design; IΔ 1/5.

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
