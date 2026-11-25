# Proposed tests

## Lag after a belief update

Use a low-stakes ambiguous scenario with two randomized cue conditions. Give participants either credible disambiguating evidence or a matched cue that leaves the ambiguity unresolved. Record baseline interpretation probabilities and affect ratings, then record both immediately after the cue and at fixed follow-up times. Add a randomized regulation prompt versus a neutral prompt if testing how available actions influence the trajectory. Keep prompts and measurement times fixed in advance.

Estimate cue effects on belief and affect over time, using a repeated-measures model with participant-level variation. Predefine a meaningful belief change, affect scale, and time window. Use assigned groups for causal comparisons and treat comparisons conditioned on observed belief change as descriptive.

**Primary prediction: a design template, not yet a preregistration.** A finding that belief updates precede affect changes "in at least some conditions" cannot fail, and a lag by itself is compatible with several existing models. So the primary prediction must be one that named rivals get wrong, with a failure criterion stated in advance. This section does not yet state a primary effect size or a rival-specific failure criterion. Those belong in a frozen preregistration, calibrated as described below.

The latent rivals are those in the [2026-11-22 lag note](../research-log/2026-11-22-director-lag-identifiability-pass.md):

- **A, affect persistence:** interpretation responds quickly and affect carries inertia.
- **B, belief persistence:** interpretation carries inertia and affect follows quickly.
- **M, reporting persistence:** a lag in reporting produces apparent affect inertia.

Observation mechanisms are crossed with each of them, not treated as a fourth latent dynamic:

- **D, differential demand (added 2026-11-23; recast 2026-11-25 as an observation mechanism).** After a credible cue, participants know the expected belief answer but have no equivalent cue for their affect rating. Belief *reports* can then jump ahead of the underlying belief, which produces an apparent lag. D can operate under A, B or M. It predicts that the apparent lag shrinks when belief is measured behaviorally or implicitly rather than by explicit report. That contrast is not decisive on its own, because the other measures have their own noise and reactivity.
- **Probe reactivity.** Answering a belief probe can itself change belief or affect (see the design elements below).

The synthetic model-confusion gate in that note comes first. Cross the observation mechanisms with A, B and M, and fix four quantities on held-out synthetic worlds before any human data: the meaningful time resolution, the equivalence margin, the minimum discriminability and the decision threshold. If the rivals cannot be told apart under the planned design and sample size, record a negative identifiability result rather than choosing a preferred mechanism. A classifier winning on synthetic data does not promote a mechanism. Worlds in the same observational equivalence class cannot be separated by any analysis of these observables, so report them as a class. The executable benchmark is still on an unmerged branch ([#24](https://github.com/LeoAJRogers/emotional-rationalism/issues/24)). When it is integrated, cite its observational-class counts from [#16](https://github.com/LeoAJRogers/emotional-rationalism/pull/16), not the original raw classification counts.

**Design elements against measurement artifacts:**

- **Probing may itself regulate affect.** Asking "how likely is rejection?" is close to a reappraisal prompt.
  - Counterbalance the order of the belief and affect questions.
  - Include an arm with no belief probes, or low-frequency probes, between cue and follow-up. That arm records no belief, so it cannot measure the belief–affect lag directly. It tests probe reactivity, through the affect trajectories and later validated belief outcomes.
  - Prespecify the cue × probe × time contrasts. A does not predict invariance across probe arms if probing itself changes affect.
- **Implicit belief measures.** Where feasible, add a behavioral or implicit belief measure alongside the explicit rating, and prespecify the explicit-versus-behavioral contrasts. Implicit measures can also be noisy or reactive, so assess their validity and reactivity rather than assuming either.
- **Precedence is limited by sampling.** "Precedes" can only be resolved down to the sampling interval, and the immediate measurement is effectively simultaneous with the cue. Choose the schedule in simulation, relative to the plausible lag, before fixing it.
- **Floor effects versus ethics.** Persistent alarm needs some initial alarm. State the minimum baseline affect the analysis needs, how the scenario produces it within what ethics review allows, and how participants below it are handled, before collecting data. Use a mild stake with debriefing, not distress.

Compare held-out predictions across an immediate appraisal model, an autoregressive model with affect history, and a model adding belief and regulation inputs to the same history. Use matched information and flexibility, participant-held-out log scores, and calibration of target-region probabilities. Little incremental predictive gain over the autoregressive model would weaken the case for the additional structure.

## Reachability needs its own design

The dynamics test above does not test reachability. Varying which regulation strategies are available, or how much time participants get, is the natural design. But [PR #12](https://github.com/LeoAJRogers/emotional-rationalism/pull/12) shows its limit: a randomized *offer* identifies the effect of offering (intention-to-treat). With imperfect uptake, the offer having no influence of its own is not enough to identify the effect of the performed action. Perfect implementation (everyone offered performs the action, and no one else does) plus that exclusion identifies the effect of the assigned action. Instrumental-variable assumptions (relevance, exclusion, monotonicity, independence) identify at most an effect among compliers, not the value of an arbitrary policy.

Such a study therefore estimates reachability under offered menus. That probability bounds the person's own optimal feasible reachability from below only if everything the offer induces is admissible in the person's own policy model: the resulting policy, the information the offer supplies, the context, the action constraints and the outcome definition.

For a future test:

- record eligibility, assignment probabilities, delivery, uptake, interpretation, and the endpoint and observation window, all fixed in advance;
- estimate the offer effect first;
- report how conclusions change under explicit violations of the no-direct-offer-effect assumption.

The PR #12 audit inspected three public releases: openESM 0010 (Geschwind et al.), the Sicorello et al. daily-life data (the study behind openESM 0073), and HeartSteps V1. None had a timed performed action, a documented assignment and a later affect endpoint together. This does not cover other public datasets.

## Simulator and measurement checks

Recover the exact probabilities in the worked example, including the two-action version, before simulation. Vary transition probabilities, horizon, threshold, and measurement noise. Check when inferred reachability differs from the simulated ground truth. When there are several feasible actions, compare policies in simulation. A human trial with fixed prompts estimates outcomes under those prompts. Estimating optimal reachability requires assumptions about the full feasible set and its transitions.

## Preregistration

Preregister the primary outcomes, the rivals and their predicted patterns, the failure criterion, the smallest effect of interest, the sample size rationale, exclusion criteria, and the missing-data plan before data collection.

- **Timing.** Timestamp the preregistration publicly before the relevant confirmatory data access, unblinding or evaluation, as a tagged commit in this repository or on OSF.
- **Existing data.** Record what has already been seen, and disclose any exploratory access to legacy data.
- **Private records.** A preregistration or hash held only in a private store cannot be checked by outside readers, so do not describe it as independently verified.

For a human study, obtain appropriate ethics review and consent, and share only data cleared for public release.
