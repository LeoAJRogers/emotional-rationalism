# Research log

## 2026-11-26 · open problem: emotional influence in shared spaces (Claude Opus 5.5, from Leo's framing; for cross-agent review)

- **New [problem statement](../challenges/shared-space-influence.md):** Leo's framing of Emotional Rationalism as a general mechanism for emotional influence in shared spaces, constrained into a descriptive part (testable) and a normative part (consent by entering a space, listener responsibility, how much weight a purely informational impact deserves), recorded as candidate evaluative criteria and not as a project position.
- Separates four quantities behind "does it impact me or just what I know": causal outcome contrast, predictive update about outcomes, residual world-information and evaluative importance, with other-regarding stakes as their own category. Names the hard points, the requirements for any cross-observer claim (each a hypothesis), tests, falsifiers and comparators.
- **Refinements the same day, from Leo's framing:** a common space requires free expression and freedom to leave; consent attaches to a stay-or-leave calculation but is not established by entry and exit alone; "rational" means the emotional state fits its context, meaning the situation and the group's social dynamics, not reasoning; populations have local norms plus a shared layer that makes interaction possible; Leo's hypothesis that evolved social dynamics become less xenophobic as intelligence increases (labelled a claim); Leo's views that conflict can always be chosen and that, with freedom to reason, xenophobia might not be permanent, restated as questions about hazard and about whether a xenophobic state set is closed; B3 does not discount concern for others, and expressed concern is a cue, not an obligation; Leo's conjecture that tells are informative only if not fully controllable, recorded as a conjecture and restated for the regime where it holds (costless, unverifiable signals with conflicting incentives), with a conditional AI pilot.
- **Revised after GPT-6.2 cross-review of `3d9df0a`:** information-theoretic terms relabelled (outcome-relevant information and residual world-information, not impact), with event-specific and causal quantities distinguished; the claims that non-fixed policies imply conflict and non-absorption were withdrawn; consent, responsibility and exposure-cost wording narrowed; cross-observer claims restated as hypotheses on operational variables.
- **Second revision after GPT-6.2's re-review of `4b9188a`:** the monotonic controllability-informativeness claim was withdrawn; the summable-hazard arithmetic was corrected (the sum is exactly 1, and survival is positive); possibility of choosing conflict was separated from positive probability; conditioning on history and context was made explicit; other-regarding outcomes get an explicit third partition.
- **Open problems:** a short entry linking to the statement.
- No model text, numbers or register entries changed.
- **Integration Delta:** not assigned. This is an open problem, not a model change.

## 2026-11-25 · core-file corrections after GPT-6.2's cross-review (Claude Opus 5.5, ER daily run; for re-review)

- **Why:** GPT-6.2's [cross-review](https://github.com/LeoAJRogers/emotional-rationalism/pull/23#issuecomment-7115031669) of the 2026-11-23 entry below found four blocking errors.
- **`theory/model.md`:**
  - the two-action example no longer says that no single policy reaches both states. A randomized policy attains $\Pr(A)=\Pr(S)=1/2$ at $h=3$, and the text now separates target-by-target optima from the jointly attainable set;
  - reachability is defined given the person's information, with state-informed results labelled separately and feasible actions knowable;
  - the attainment argument is restricted to finitely many information histories;
  - the offer-versus-action statement now distinguishes intention-to-treat, the effect of the assigned action under perfect implementation, and complier effects under instrumental-variable assumptions;
  - nonblocking points: the exact condition for the modal-interpretation reading of expected loss, fixed versus re-evaluated targets, endpoint versus hitting labels, and partial observation as the conservative default for human studies.
- **`experiments/protocol.md`:**
  - the lag prediction is marked as a design template until a frozen preregistration;
  - differential demand is recast as an observation mechanism crossed with A, B and M, not a fourth latent dynamic;
  - the no-probe arm is described as a test of probe reactivity;
  - the calibration quantities (time resolution, equivalence margin, minimum discriminability, decision threshold) are named, and observational equivalence classes respected;
  - the offer-menu bound is stated with its full admissibility condition;
  - the dataset audit is scoped to the three releases PR #12 inspected;
  - preregistration timing refers to confirmatory access, unblinding or evaluation, and private hashes are not described as verified.
- **README:** the licence sentence now restates the existing notices for project-owned material only. The rule for files that mix code and prose is left for Leo's decision.
- **Open problems:** the three added references are worded as comparators, and the claim that D'Arms and Jacobson introduced the term is withdrawn.
- Every number in the worked example was checked with exact rational arithmetic [MATH]. No register entries, empirical claims or results changed.
- **Integration Delta (IΔ): 1/5.** Corrections only.

## 2026-11-23 · core files brought up to date (Claude Opus 5.5; for cross-review)

- **Why:** an external review relayed by Leo read only the core files and spent most of its effort on points the research log had already settled. `theory/model.md` and `experiments/protocol.md` still read as v0.1.
- **`theory/model.md`:**
  - the worked example now names the proposition it refutes and adds a two-action version (wait or reappraise), which shows different targets needing different policies, and passive versus optimal values;
  - added the person's, researcher's and simulator information sets, with partial observation declared per study (from Sonnet's 2026-11-20 review);
  - $m_t$ must be declared for the Markov claim to have content; exogenous events enter through $o_t$;
  - a correct argument for why the maximum is attained even though $b_t$ is continuous-valued;
  - the expected-loss fittingness form named as a Bayes-act commitment, with alternatives (links #15);
  - the passive and controlled distinction, endpoint versus hitting, and the "model-implied" and "intervention-validated" labels (from the 2026-11-21 note and PR #12).
- **`experiments/protocol.md`:**
  - the "at least some conditions" prediction is replaced by rival-discriminating predictions with a stated failure criterion, using the 2026-11-22 lag note's rivals plus a new differential-demand rival;
  - added a no-probe arm, question-order counterbalancing, sampling-limit and floor-effect requirements, an offer-versus-action section on reachability, and public timestamping of preregistrations.
- **Open problems:** Brady (2009), D'Arms & Jacobson (2003) and Sheppes et al. (2011) added; citations checked against publisher pages.
- **README:** states that LICENSE-MIT covers code, including the HTML and JavaScript demos.
- No numbers, register entries or empirical claims changed.
- **Integration Delta (IΔ): 1/5.** This brings already-agreed clarifications into the core files and adds a few new ones. It does not revise the model.

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
