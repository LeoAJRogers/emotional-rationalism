# Reachability is not identified by observational transition prediction

**2026-11-20 — GPT-6 independent conceptual/methodological pass.** Status: mathematical counterexample and proposed test, **not** a human-data finding or an executed experiment. This note supplements, rather than revises, the public integration checkpoint.

## Claim and boundary

A model can perfectly predict the joint observational distribution of reported state and self-selected action yet fail to identify the effect of *choosing* that action. Thus observational predictive calibration, even at multiple horizons, is necessary for some uses but insufficient for intervention-sensitive reachability. The gap is causal identification, not merely sample size or model expressiveness.

## Minimal counterexample

Let \(U\in\{0,1\}\) be a person's action and \(Y\in\{0,1\}\) be a favorable next-step state. Consider a population in which observed \(P(U=1)=1/2\), and \(Y=U\) always. Two structural models fit the **entire observed joint distribution** exactly:

- **Model A (action has an effect):** \(U\sim\mathrm{Bernoulli}(1/2)\); \(Y:=U\). Under intervention, \(P(Y=1\mid do(U=1))=1\) and \(P(Y=1\mid do(U=0))=0\).
- **Model B (selection by unobserved readiness):** \(H\sim\mathrm{Bernoulli}(1/2)\); \(U:=H\); \(Y:=H\). Under intervention, \(P(Y=1\mid do(U=1))=P(Y=1\mid do(U=0))=1/2\).

Both give \(P(Y=1\mid U=1)=1\) and \(P(Y=1\mid U=0)=0\). Their observational likelihoods are identical, yet the action's effect is either 1 or 0. The example is deliberately deterministic for clarity; adding measurement noise does not in general restore identification.

**Reachability consequence:** For a target \(Y=1\) and threshold \(\alpha=0.75\), action 1 reaches the threshold under Model A, but no intervention on \(U\) reaches it under Model B. If the individual's latent readiness \(H\) were known, the corresponding conditional quantities would need to be specified separately. This is a population-level counterexample, not a claim about an individual person's capacity.

## A further target-definition trap

The model's fitting set \(\mathcal E^*(D,c)\) may itself change after an action changes evidence, interpretation or context. A probability of entering the **fixed pre-action target** and a probability of entering a **future re-evaluated target** are different estimands. The existing symbolic model correctly specifies a fixed target; experiments should state when they use that convention rather than quietly substituting a moving target.

## Proposed test ladder (not run)

1. **Observational benchmark:** forecast next reported state under naturally chosen actions; calibrate conditional and multi-step predictions. Label this prediction, not control.
2. **Selection stress test:** simulate the two structural models above and test whether an estimator trained on observational sequences spuriously reports intervention effects. Include a noisy proxy for readiness and vary proxy quality.
3. **Prospective intervention:** where ethical and feasible, randomize an encouragement or low-risk action with measured adherence, pre-action covariates and a preregistered target. An encouragement instrument identifies only under additional exclusion/monotonicity/relevance assumptions; it does not automatically identify universal action effects.
4. **Reachability validation:** compare predicted target-region probabilities under assigned policies with observed outcomes, including adherence, adverse responses, missingness and uncertainty. Separate intention-to-treat from per-protocol or causal policy claims.
5. **Transport check:** repeat across contexts and participants before claiming stable action effects or a general controllability law.

## Implications for the project

- Preserve the three-part scaffold: the issue does **not** invalidate descriptive transitions or conditional fittingness.
- Distinguish \(P(Y\mid U=u,\mathcal H_t)\) from \(P(Y\mid do(U=u),\mathcal H_t)\). A controlled Markov kernel used for reachability needs interventional justification or an explicitly assumed causal interpretation.
- Do not treat randomized MBCT effects on **reported mean positive affect** as validation of arbitrary moment-to-moment reappraisal policies.
- Maintain two labels for reachability results: **model-implied under stated causal assumptions** and **intervention-validated**. Neither implies subjective emotions are freely selectable.
- Before building a policy optimizer, define the target, feasible action set, decision-time information, horizon, safety constraints and estimand.

**Provenance:** GPT-6 authored this pass after reading the 2026-11-20 public checkpoint and current symbolic model. The counterexample uses standard causal-inference logic, not a claim of novel causal theory. No datasets were accessed and no tests executed for this note. It is a proposal for critical review, not a merged empirical result.

**Related work (2026-11-23):** the [November 21 passive-versus-controlled note](2026-11-21-passive-vs-controlled-reachability.md) gives the concise two-action conceptual distinction; the [executed counterexamples and aggregate dataset audit](../experiments/causal-reachability-counterexample/README.md) extend the identification argument. They do not identify actual human policy effects.
