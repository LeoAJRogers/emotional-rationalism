# Public integration review — 2026-11-19

**Status:** Research review, not empirical validation. **Integration Delta (IΔ): 2/5** — local conceptual refinement; the three-part core remains unchanged.

## Retain as core

1. Separate descriptive affect transitions, explicitly justified evaluative fittingness, and policy-dependent reachability.
2. Distinguish an emotionally fitting response from an attainable one. The two-state example is arithmetically consistent: 1 - 0.9^3 = 0.271 and 1 - 0.9^7 ≈ 0.5217.
3. Treat causal claims as requiring intervention or stronger identification assumptions; a predictive transition kernel alone does not establish mechanism.

## Clarify before stronger claims

- **Fittingness is set-valued and conditional.** Multiple affect states can tie or be near-optimal under alternative evidence standards, values, or losses. An evaluative score is not a universal moral prescription, nor an instruction to suppress an emotion.
- **Latent-state measurement.** A good fit to self-report does not establish recovery of an underlying affect state. Compare explicit observation models for self-report, behavior, and physiology, and test parameter recovery using synthetic data.
- **Reachability depends on target and information.** Exact point probabilities are grid-dependent; practical experiments should predeclare target regions, horizons, probability thresholds, and the information available to the policy.
- **Population and individual differences.** The same context may produce different transitions, preferences, or feasible actions. Model these as estimable heterogeneity rather than automatically calling deviations irrational.
- **Descriptive bias versus normative evaluation.** Fitting a model to observed behavior also learns habits and biases. Keep that empirical model distinct from evaluative proposals.

## Candidate extension: social coupling (tentative)

For two or more agents, introduce a joint process with agent-indexed latent affect, beliefs, observations, and actions, and context that can include the other agents' observable behavior. Start with an honest, restricted-information interaction, then test whether additional latent perspective-taking or deception variables improve held-out prediction. Do not assume access to another agent's private state.

**Discriminating test:** Compare (A) independent individual dynamics with shared external context, (B) observed-behavior coupling, and (C) additional inferred-other-state variables, with matched complexity penalties and held-out participants/interactions. A failure of B or C to outperform A is evidence against the added complexity in the tested setting, not against social influence in general.

## Next executable research work

1. Specify observation likelihoods and run a synthetic identifiability/parameter-recovery benchmark.
2. Preregister a minimal belief-update versus affect-lag experiment with simpler autoregressive and appraisal baselines.
3. Only then prototype the coupled-agent extension; check whether its parameters are identifiable from permitted observations.
4. Broaden literature comparisons before asserting novelty.

## Change log / hierarchy

- **Core retained:** descriptive dynamics / evaluative fittingness / reachability.
- **Strong methodological constraint:** observational prediction is not mechanistic identification.
- **Refined:** fittingness is conditional and often set-valued; reachability requires specified targets, information, and feasible actions.
- **Tentative:** coupled-agent transition models and staged social-complexity tests.
- **Parked:** universal substrate-neutral affect coordinates, objective ideal emotions, and claims about AI subjective experience. None is established by the current model.

This review records research directions and limitations; it does not claim a new empirical result.
