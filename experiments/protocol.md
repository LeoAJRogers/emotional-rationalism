# Proposed tests

## Lag after a belief update

Use a low-stakes ambiguous scenario with two randomized cue conditions. Give participants either credible disambiguating evidence or a matched cue that leaves the ambiguity unresolved. Record baseline interpretation probabilities and affect ratings, then record both immediately after the cue and at fixed follow-up times. Add a randomized regulation prompt versus a neutral prompt if testing how available actions influence the trajectory. Keep prompts and measurement times fixed in advance.

Estimate cue effects on belief and affect over time, using a repeated-measures model with participant-level variation. Predefine a meaningful belief change, affect scale, and time window. Use assigned groups for causal comparisons and treat comparisons conditioned on observed belief change as descriptive.

**Primary prediction.** A finding that belief updates precede affect changes "in at least some conditions" cannot fail, and a lag by itself is compatible with several existing models. So the primary prediction must be one that named rivals get wrong, with a failure criterion stated in advance. The rivals are those in the [2026-11-22 lag note](../research-log/2026-11-22-director-lag-identifiability-pass.md), plus one more:

- **A, affect persistence:** interpretation responds quickly and affect carries inertia.
- **B, belief persistence:** interpretation carries inertia and affect follows quickly.
- **M, reporting persistence:** a lag in reporting produces apparent affect inertia.
- **D, differential demand (added 2026-11-23):** after a credible cue, participants know the expected belief answer but have no equivalent cue for their affect rating. Belief *reports* then jump while underlying belief and affect move together, which produces an apparent lag with no affect inertia. D predicts that the lag shrinks when belief is measured implicitly or behaviorally, or not probed at all. A predicts it does not.

The synthetic model-confusion gate in that note comes first. If the rivals cannot be told apart under the planned design and sample size, record a negative identifiability result rather than choosing a preferred mechanism.

**Design elements against measurement artifacts:**

- **Probing may itself regulate affect.** Asking "how likely is rejection?" is close to a reappraisal prompt. Counterbalance the order of the belief and affect questions, and include an arm with no belief probes, or low-frequency probes, between cue and follow-up.
- **Implicit belief measures.** Where feasible, add a behavioral or implicit belief measure alongside the explicit rating. Assess its validity and reactivity rather than assuming either.
- **Precedence is limited by sampling.** "Precedes" can only be resolved down to the sampling interval, and the immediate measurement is effectively simultaneous with the cue. Choose the schedule in simulation, relative to the plausible lag, before fixing it.
- **Floor effects versus ethics.** Persistent alarm needs some initial alarm. State the minimum baseline affect the analysis needs, how the scenario produces it within what ethics review allows, and how participants below it are handled, before collecting data. Use a mild stake with debriefing, not distress.

Compare held-out predictions across an immediate appraisal model, an autoregressive model with affect history, and a model adding belief and regulation inputs to the same history. Use matched information and flexibility, participant-held-out log scores, and calibration of target-region probabilities. Little incremental predictive gain over the autoregressive model would weaken the case for the additional structure.

## Reachability needs its own design

The dynamics test above does not test reachability. Varying which regulation strategies are available, or how much time participants get, is the natural design. But [PR #12](https://github.com/LeoAJRogers/emotional-rationalism/pull/12) shows its limit: a randomized *offer* identifies the effect of offering. It identifies the effect of the performed action only if the offer has no influence of its own. Such a study therefore estimates reachability under offered menus. That is a lower bound on the person's own feasible-policy reachability only if being offered is something the person could do for themselves.

For a future test:

- record eligibility, assignment probabilities, delivery, uptake, interpretation, and the endpoint and observation window, all fixed in advance;
- estimate the offer effect first;
- report how conclusions change under explicit violations of the no-direct-offer-effect assumption.

The PR #12 audit found no public release with a timed performed action, a documented assignment and a later affect endpoint together.

## Simulator and measurement checks

Recover the exact probabilities in the worked example, including the two-action version, before simulation. Vary transition probabilities, horizon, threshold, and measurement noise. Check when inferred reachability differs from the simulated ground truth. When there are several feasible actions, compare policies in simulation. A human trial with fixed prompts estimates outcomes under those prompts. Estimating optimal reachability requires assumptions about the full feasible set and its transitions.

## Preregistration

Preregister the primary outcomes, the rivals and their predicted patterns, the failure criterion, the smallest effect of interest, the sample size rationale, exclusion criteria, and the missing-data plan before data collection. Timestamp the preregistration publicly before data access, as a tagged commit in this repository or on OSF. A preregistration held only in a private store cannot be checked as preregistered by outside readers. For a human study, obtain appropriate ethics review and consent, and share only data cleared for public release.
