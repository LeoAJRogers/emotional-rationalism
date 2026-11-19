# Progressive social-system identification: experiment roadmap

**Date:** 2026-11-19  
**Status:** Proposed program. No human or simulator results reported here.  
**Companion:** [Integrated architecture](../theory/integration-architecture.md) and [v0.1 protocol](protocol.md).

## Research question

What minimum *observable and identifiable* state, parameter, and transition complexity is necessary to predict population-conditioned social-affective change? Which dynamic features, if any, transfer between different social systems? Only secondarily: can changes under uncertainty, interpretive errors, and deception be explained with contextual observation mechanisms without changing the affect transition kernel? **Private thought inference is not an objective.**

This is a **hypothesis**, not a premise. If it fails, identify the smallest counterexample and augment the model.

## Distinguish dimensions before designing experiments

- **Affect representation dimension:** predictive degrees of freedom of the affect process (not necessarily number of ordinary emotion labels).
- **Social-context dimension:** features and relationships needed to represent relevant events and roles.
- **Belief/inference dimension:** variables required to express uncertainty, error, and beliefs about others.
- **Parameter dimension:** how many transition or observation parameters are separately recoverable under the experimental design.
- **Measurement dimension:** number and reliability of outcome channels; adding self-report scales does not automatically add latent psychological dimensions.

Latent coordinate systems can be nonunique up to transformations. State recovery and parameter recovery require interventions, constraints, or identifiable measurement models; low observed rank alone cannot establish a unique underlying psychology.

## Stage 0A — diverse simulated social populations (primary comparative baseline)

**Design:** Compare at least two deliberately different social ecologies/communities: e.g. frequent affiliation/coordination versus solitary/territorial encounters. Assign different cue relevance, relationship structure, persistence and response strengths. Give each population its own observation function and state semantics where necessary; no claims about actual species.

**Fit:** pooled universal transition parameters versus a shared dynamical architecture with population-specific parameters versus fully separate population models. Compare held-out trajectories, uncertainty calibration, effective complexity, and what remains invariant under context-preserving transformations.

**Failure condition:** if a common kernel loses predictive adequacy across populations, keep the divergent models and document the failed generalization rather than forcing human-style social categories.

See [population-first objective](../theory/population-first-objective.md) and the [learnable transition program](../theory/learnable-state-dynamics.md). The primary output remains trajectories, not reconstructed thought contents.

## Stage 0A.1 — distinguish changing exposures from changing response laws

**Design:** Simulate two agents across repeated contexts, first with a fixed transition kernel but changing exposures, relationships, or strategies; then with known changes to individual response parameters under stable controlled contexts.

**Question:** Can estimation avoid confusing changed marginal emotion frequencies with a genuinely changed response law? Can it recover parameter learning when present, and test models that treat regulation as bounded influence rather than exact emotional selection?

**Failure:** inferred plasticity under a fixed kernel due only to exposure drift, inability to detect known changes, or apparent recovery caused by observing simulator-only latent states without a feasible observation model. See [learning core note](../theory/learnable-state-dynamics.md).

## Stage 0A.2 — can affective dynamics generate social regularities?

**Design:** Compare four otherwise matched multi-agent simulated configurations: (A) endogenous affect-to-action coupling, without imposed norms; (B) no affect-to-action coupling, without imposed norms; (C) affect coupling with fixed externally supplied norms; (D) affect coupling with dynamic norm feedback. Hold ecology, social network, access to cues, and opportunities to interact controlled. Distinguish measurable individual state, behavior, expression, population frequencies, and genuine expectations/sanctions.

**Primary test:** Does the affectful minimal model generate persistent population patterns not explained by the affect-ablated behavioral baseline? Do group regularities later alter individual state-transition distributions? Which patterns require externally injected norm information, rather than emerging?

**Failure criteria:** comparable patterns without affect; norm statistics estimated circularly from the target affect; behavior automatically labeled 'injunctive norm' without expectations/sanctions; apparent learning due only to exposure drift; failure on held-out interactions or populations. See [test plan](../theory/affect-social-structure-feedback.md). No simulation result has yet been claimed for this four-way test.

## Stage 0B — full-information social dynamics in simulation

**Design:** Two to three synthetic agents with known values, relationship weights, histories, initial affect, and contrasting interests. Remove concealment and observational ambiguity without requiring identical goals or responses. Include genuine conflict under perfect mutual knowledge.

**Fit:** A minimal state-transition model versus richer versions with redundant appraisal inputs; attempt to recover known parameters and held-out trajectories. Evaluate by recovery error, predictive log score and calibration, rollout error, and state sufficiency.

**Failure conditions:** distinct parameter sets fit equally; target dynamics cannot be recovered under the proposed measurements; conflict vanishes merely because beliefs are accurate; or a compressed model predicts only its training trajectories.

**Agents need not infer correctly.** Explicitly include a branch in which an individual's beliefs are systematically wrong and test whether the *other* agent's actions and affect change through reciprocal coupling. Modeling and evaluating these errors is our scientific activity; it is not a cognitive prerequisite for the simulated agents. A poorly calibrated observer-side evaluation should never be allowed to stop the simulation.

**Caveat:** The synthetic model defines ground truth. Recovering it validates the procedure under those assumptions, not a claim about human emotion.

## Stage 1 — partial information without deception (inside each population)

**Design:** Randomly hide or delay facts while requiring truthful communications. Distinguish unknown intent from known conflict; model uncertain appraisals and confidence. Cross two manipulations: hold world state fixed while changing evidence available, and hold reported beliefs approximately fixed while changing observed cues.

**Compare:**
- end-to-end transition T(e, observations);
- decomposed interpretation G followed by T(e, G);
- model with separate uncertainty-sensitive affect inputs;
- model with affect-to-attention/belief feedback.

**Decisive result:** If a fixed T plus G consistently predicts held-out regimes with fewer identifiable parameters, evidence favors factorization. If uncertainty remains affectively predictive after conditioning on inferred context, a purely factual G is insufficient.

## Stage 2 — systematic interpretation error (optional mechanism)

**Design:** Add stable priors, overconfidence, attribution bias, and incorrect beliefs. Keep errors distinct from deception. Test whether changing only the inference layer recovers the observed transitions.

**Failure conditions:** parameter instability when priors change; long-lag affect not captured by persistence; or multiple nonidentifiable combinations of G, T, and the observation model.

## Stage 3 — information management and deception

**Design:** Add omission, selective truthful disclosure, misleading cues, and explicit false claims as distinct signaling policies. Agents can choose signals; receiving agents update trust and beliefs. Introduce first-order and then second-order mental-state estimates only as needed.

**Question:** Does deception change emotion through inferred intent/trust and information, or does it require an additional direct response to perceived dishonesty? Direct response may still be captured by T if deception itself is represented as a relevant context feature.

**Warning:** Information hiding is not identical to deception, nor is misunderstanding. Equal revealed data need not imply equal emotion if an agent learns that it was intentionally manipulated.

## Stage 4 — population-appropriate empirical evidence and transfer

**Design:** For initial humans, use the established low-stakes intent × present-obligation fictional scenarios from the earlier November 18 research note as inspiration; do not treat synthetic actors as observed people. A [related Observatory inquiry](https://github.com/LeoAJRogers/the-observatory/commit/fa5ff93c6ab74d5b6a7b8d4c7e4d4578622bc5ab) concerns judgment calibration. Independently randomize verified intent, present responsibility, and (in a separate factor if feasible) whether/how information was withheld. Balance cue order. Pre-register and secure consent/ethics review as appropriate.

**Separate measures:** affect toward a target (anger, warmth, sympathy, guilt as appropriate); task urgency/salience; explicit appraisal of motive and harm; confidence; delayed spontaneous response on re-exposure; chosen actions and memory. Self-report is evidence of reported experience, not transparent access to a latent state.

**Competing predictions:** 
- deliberateness can increase anger while completion of obligations decreases urgency; a single scalar 'distress' model may fail;
- updated judgments can precede affect change;
- emotion may influence subsequent attention or interpretation;
- full-information conditions should not force consensus in felt responses;
- models must predict held-out individuals and scenarios, not merely fit mean ratings.

Compare immediate-appraisal, autoregressive-affect, belief-plus-regulation, decomposed G/T, and bidirectional baselines. Use sensitivity analyses for reference distributions, model misspecification, missing data, and measurement errors.

## Addition/deletion decision rule

At each stage, report a model ledger:

| Item | Required record |
| --- | --- |
| New mechanism | What residual prediction or causal distinction forced it? |
| Simpler comparator | What failed without it? |
| Identifiability | Under which measurements/interventions is it recoverable? |
| Quantitative gain | Cross-validated score, calibration, effect size and uncertainty |
| Generalization | Held-out individual, context, relation, and information regime |
| Alternatives | Demand, reporting, baseline persistence, physiology, confounding |
| Decision | Retain provisionally / simplify / reject / unresolved |

A more complex model should not be accepted solely because it fits more training data. Do not conclude that a null result proves the absence of an emotional process if the measurement is insensitive.

## Minimal first implementation checkpoint

Start with a reproducible finite-state two-agent simulator with:

1. persistent, simultaneous anger and warmth (or similarly nonexclusive features);
2. separately measured present-task urgency;
3. explicit true intention, desired outcome, and relationship role;
4. a full-information switch that changes observation fidelity **without changing underlying interests or baseline dynamics**;
5. a partial-information and biased-inference switch;
6. ablations for G, feedback, and emotional persistence;
7. a seeded train/test design and recoverability checks.

Implement no deceptive agent until Stage 0–2 are debugged. Avoid reifying synthetic weights as psychological findings.

## Open identification problems

1. Do the affect and belief transition operators admit a uniquely recoverable decomposition?
2. Can apparent emotion inertia be explained by observation lag, appraisal lag, rating artifacts, or external context drift?
3. If trajectory-selection analysis is ever attempted, how can it remain an explicitly optional researcher-side counterfactual exercise rather than an assumed agent mechanism or framework objective?
4. Which dimensions are portable across individuals without erasing roles, targets, and subjective report semantics?
5. What experimentally discriminates felt change from judgment updating, demand compliance, and action policy change?
6. When does uncertainty itself act as a relevant affective cause, invalidating an overly simple G/T split?

**Outcome status:** Entire roadmap is proposed. It does not report verified empirical evidence.
