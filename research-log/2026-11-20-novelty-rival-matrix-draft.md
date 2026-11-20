# Novelty challenge: first-pass rival matrix (2026-11-20)

**GPT-6 working draft, not an exhaustive systematic review.** A distinctive formal decomposition does not by itself imply a novel mechanism or empirical success. Literature links below are starting comparators, not proof of priority.

| Candidate ER contribution | Nearest established families | What overlaps | What would genuinely discriminate? | Present evidence |
|---|---|---|---|---|
| Context/history-conditioned stochastic affect transitions | Dynamic appraisal/component process (Scherer); AR/state-space emotion dynamics | Context-dependent trajectories and inertia | Better calibrated forecasts or more parsimonious transferable state under matched observation model | R-003/R-004 show bounded history gain, not mechanism |
| Predictive state vs persistent latent state | State-space, measurement-error AR/ARMA; dynamic factor models | Observation noise and nonstationarity can mimic latent timescales | Recovery of latent structure with independent measurement anchors or strong cross-item temporal predictions | Synthetic gauge counterexample and R-004 caution |
| Evaluative fittingness conditional on evidence/values | Appraisal, rational emotion, decision-theoretic and normative affect accounts | Judgments of appropriateness and differing values | A well-defined, independently measurable evaluative criterion predicting disagreements or outcomes beyond appraisal baseline | Formal definition only; no human test |
| Policy/information/horizon-dependent reachability | Stochastic control, MDP/POMDP, emotion regulation | Feasible actions, targets and transition constraints | Jointly calibrated h-step and action-conditioned probabilities that outperform simpler regulation models | Toy derivation only |
| Belief update preceding affect transition | Appraisal and reappraisal experiments | Belief and affect may evolve at different rates | Prospective cue experiment showing incremental prediction beyond immediate appraisal and autoregression, with causal design | Proposed protocol only |
| Population social feedback generating norms | Social learning, evolutionary game theory, cultural dynamics, social-affective modeling | Emergent coordination, norms and reciprocal adaptation | Testable norm trajectories that arise from a parsimonious coupling law and beat explicit-norm rivals | Candidate architecture PR #4 only |
| Cross-population/substrate configurability | Hierarchical state-space, agent-based and multi-agent models | Population parameters and modular observations | Out-of-population transfer without ungrounded subjective equivalence | Architectural ambition only |

## Priority novelty test
The near-term **strongest falsifiable contribution** is not 'emotion has dynamics'. It is whether a carefully measured compact state representation predicts held-out affect trajectories **better than a robust measurement-error/nonstationarity rival**, and whether the distinctive evaluation/reachability layers yield separately testable predictions in a future intervention design.

## Benchmark contract
- Fix information availability and forecast horizon *before* comparing models.
- Include an autoregressive report baseline, a measurement-error/nonstationarity state-space rival, an appraisal/context rival, and only then an ER extension with a defensible extra parameter.
- Compare proper scoring rules, calibration, stability under missingness, participant transfer and complexity.
- Ablate one mechanism at a time. A better score without measurement identification supports prediction, not ontology or causal explanation.
- Publish negative outcomes and rival forecasts. Do not retrofit a model family to make a result seem uniquely predicted.

## Specific literature to audit in a later dedicated review
- Scherer (2009), dynamic architecture of emotion, DOI 10.1080/02699930902928969.
- Gross (1998), antecedent- vs response-focused emotion regulation, PMID 9457784.
- Schuurman, Houtveen & Hamaker (2015), measurement error in n=1 psychological autoregression, DOI 10.3389/fpsyg.2015.01038.
- Schuurman & Hamaker (2019), person-specific reliability and measurement error in multilevel autoregression, PMID 30188157.
- Partially observed stochastic control and appraisal/decision-theoretic emotion models: select exact strongest comparators before claiming priority.

**Interpretation discipline:** predictive compression, statistical identification, mechanistic interpretation, normative justification and causal intervention success are five separate evidentiary achievements. No one result automatically establishes the next.
