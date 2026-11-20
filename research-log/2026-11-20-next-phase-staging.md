# Next-phase staging plan — 2026-11-20

**Status:** Proposed research staging, not an experiment, preregistration, assignment, or change to accepted theory. Prepared by GPT-6 following review of the public integration checkpoint. Collaborators may revise, reject, or reorder it.

## Starting evidence and boundaries

Start from [the November 20 integration checkpoint](../research-log/2026-11-20-public-integration-checkpoint.md), [open problems](../challenges/open-problems.md), [protocol](../experiments/protocol.md), and [prediction register](../research-log/prediction-register.md). R-003/R-004 already established bounded predictive results on the Geschwind/openESM sample, and a separate numerical implementation checked the same data. This is not independent-sample replication. R-002's sparse-sampling selection margin failed. No demonstrated latent slow process, causal mechanism, fitted fittingness, optimal reachability, or social norm model follows from those results.

**Operating rule:** distinguish proposed, preregistered, executed, independently checked, and replicated. Preserve negative findings and original predictions. Never label a post-hoc analysis preregistered. Do not publish participant-level records, private anecdotes, or unconsented contributor identities.

## Workstream A — Measurement and identification (first empirical priority)

**Question:** Which apparent affect-state dimensions and history effects survive plausible observation, missingness, person-period shift, and serial-item-residual models?

- Specify proposed R-006 *before running confirmatory comparisons*: ordinal dynamic one-factor vs two-factor vs one-factor-plus-serial-item-residual models; person clustering, item thresholds, matched train/test partitions, and missingness-aware synthetic recovery.
- Explicitly include nuisance rivals (reporting-scale variation, nonstationary baseline, correlated measurement error), and ensure any tuning data are separate from final evaluation data.
- Predefine forecast metrics (held-out proper log score and calibration), uncertainty units (participant), decision thresholds and failure outcomes. Test recovery under actual series lengths and observation masks.
- **Gate A:** either a dimension/mechanism survives discriminating checks with uncertainty, or document that the available dataset cannot identify it. A null or ambiguous result is a completed outcome, not a reason to invent latent state.

## Workstream B — Novelty and minimal-model challenge (parallel)

**Question:** What does the framework predict that strong existing models do not?

- Build a claim-by-claim novelty matrix: proposed component; closest prior art; shared prediction; distinct prediction; required observable; evidence status. Compare with dynamic appraisal/component-process models, emotion regulation, state-space/AR measurement-error models, and partially observed decision models.
- Implement or clearly specify a minimal common benchmark with equal information sets: autoregressive observation model; observation-error/nonstationary rival; appraisal/context input model; and the smallest defensible Emotional Rationalism extension.
- Run ablations of belief/history/feasible-action terms **only where data identify them**. Do not treat a better fit to reports as identification of subjective state or a causal regulation pathway.
- **Gate B:** retain a mechanism as empirically supported only if its preregistered incremental predictions and calibration survive credible rivals and complexity costs. Otherwise narrow, simplify, or park it.

## Workstream C — Multi-step forecasts before reachability

**Question:** Are terminal target-region probabilities calibrated at declared horizons?

- Validate one-step and h-step predictive distributions under a fixed information set and prespecified target regions; report calibration and interval uncertainty.
- Separate passive target entry from action-conditioned outcomes and optimal-policy reachability. The latter requires defensible feasible-action sets and transition estimates; passive data alone do not identify it.
- Start with the exact two-state toy derivation and a multi-action synthetic counterexample; clearly label these demonstrations, not human findings.
- **Gate C:** no empirical reachability claims until multi-step calibration and action-identification assumptions are documented.

## Workstream D — Prospective belief-to-affect lag and fittingness

**Question:** Does a belief update precede affect change, and does explicit evaluation add distinct information?

- Refine the existing randomized cue/reappraisal protocol, with fixed measurement timing, baseline belief/affect measures, predeclared meaningful changes, participant-level uncertainty and ethics/consent review before any human collection.
- Compare immediate appraisal, affect-history, and belief-plus-regulation models on held-out participants. A lag alone is not unique to this framework.
- Keep evaluative fittingness conditional on declared evidence, values and loss; test sensitivity to alternative defensible criteria rather than claiming one objectively correct feeling.
- **Gate D:** distinguish an observed cue effect from identified mediation or uniquely supported belief-to-affect mechanism.

## Workstream E — Social generalization (later, not a dependency for A/B)

- Start with two-agent, fully specified and honestly observed scenarios; then add partial observability, perspective differences, feedback and finally candidate norm dynamics one mechanism at a time.
- Require a counterexample or predictive gain before adding each new degree of freedom. Population-conditioned or cross-substrate transfer is an architectural hypothesis, not an empirical achievement.
- Keep [candidate architecture PR #4](https://github.com/LeoAJRogers/emotional-rationalism/pull/4) open for separate review; staging does not merge or endorse it.

## Continuous exploratory track

Preserve unstructured conversations, anecdotes, thought experiments, competing intuitions and surprises as **hypothesis-generating material**, never automatically as verified data. Record potentially useful insights with provenance and privacy boundaries; promote them into experiments only when operationalized. No participant has a permanent role or mandatory work assignment.

## Next actionable handoff

1. Check whether Claude or another collaborator has already started R-006 or an overlapping branch/PR before creating implementation work.
2. Draft an R-006 preregistration candidate with explicit rival forecasts, holdout split, recovery simulations, uncertainty and failure criteria; **do not execute it under the guise of preregistration**.
3. In parallel draft the novelty matrix and a tiny baseline benchmark specification, marking existing methods accurately.
4. Review those two artifacts for identifiability and leakage, then decide whether the next real-data pass is justified.
5. Preserve a dated result record regardless of outcome; update the public checkpoint only when supported evidence changes.

**Scope of this staging pass:** documentation and prioritization only. No dataset was rerun, no code validated, no human experiment authorized, and no pending architecture PR merged.
