# Research scope: context, interaction, and persistent state

**Status:** Conceptual research direction, not a validated general theory. This document distinguishes the broader research program from the narrow, testable affect model in [the symbolic model](../theory/model.md).

## Why the scope is broader than emotion regulation

Emotional Rationalism grew through sustained conversations about lived experience, relationships, interpretation, and self-understanding. Those discussions motivated questions about what changes within a person during an interaction and how the changed state shapes future responses. The public research formulation is only one outcome of that ongoing collaborative inquiry, not a complete account of it.

The broader candidate problem is: **How do a system's current state, history, context, and interactions jointly shape its next state and its future response tendencies?**

Here *context* means the environment and circumstances in which interactions occur, including other participants and population-level patterns; it is not merely a label attached to an isolated stimulus. An *altered state* means a change in a modeled state, not necessarily emotion, consciousness, or a special altered-consciousness experience. Relevant observations might involve affect, bodily sensations, interpretations, or other measurable responses, depending on the population and study. There is no claim that one common set of state coordinates already works across these domains.

## Candidate scaffold, not an identified mechanism

A deliberately underspecified starting point is

```text
latent state at t+1 ~ Transition(
    latent state at t,
    context at t,
    observations and interactions at t,
    feasible actions at t,
    history summary at t
)
observations at t ~ Measurement(latent state at t, context at t)
```

This notation organizes questions. By itself it is not a unique mechanism or a falsifiable discovery. To become scientifically useful it requires specified state variables, measured outputs, competing models, constraints on inputs, and held-out predictions. Observed associations must not be presented as causal explanations without additional evidence.

Three distinct mechanisms or modeling roles need separate treatment:

1. **Association:** a system's history makes some contexts predictive of later responses.
2. **Causal influence:** changing an interaction or context changes a response under specified conditions.
3. **Learning or adaptation:** prior interactions alter future response tendencies or the transition parameters.

Reflective reasoning could be represented as an action, an internal process, or both. Whether it needs a distinct mechanism is a research question, not an assumption.

## Existing formal specialization

The current [symbolic model](../theory/model.md) starts with human affect and separates:

- **Descriptive transitions:** what is likely to arise or persist.
- **Evaluative fittingness:** what responses fit specified evidence and evaluative criteria.
- **Reachability:** what responses are attainable under feasible policies and a time horizon.

These are useful *questions about one domain* rather than a requirement that every possible state-change process has an evaluatively preferred destination. The project is **not primarily about controlling or creating emotional states**. Evaluative fittingness must not be conflated with descriptive prediction, and inability to reach an evaluated state does not imply a personal failure.

## Social environment and feedback (candidate extension)

In multi-agent settings, context may change as participants interact. Physical or ecological constraints and socially maintained norms should be modeled distinctly. Some norms emerge from population traits and interactions, some are deliberately enforced, and many are inherited by people who did not establish them. Individual action can influence future contexts without assuming unlimited freedom from constraints.

One candidate extension is to estimate the emotional landscape of a social system over time: probability distributions over possible affective states for each observed participant, and their distribution across the population at time $t$. These are uncertain, measurement-dependent estimates, not definitive labels of anyone's internal state. Interactions and shared context may inform how the distributions evolve, while allowing individuals to respond differently. Population- and context-specific patterns can serve as empirical reference distributions for describing what is common; they are not prescriptions for what anyone ought to feel. Aggregate patterns must not be used to infer an individual's state without individual-level evidence.

Proposed staged test: begin with individual models and observable shared context; add observable interactions; then consider latent models of others' perspectives and deceptive communication only if measurements and comparative predictions justify them. Do not treat one participant's reports about another's internal state as ground truth.

## Scope boundaries and tests

- Initially fit and test on well-characterized human data. Possible future adaptations to animals or AI require population-specific measurement and transition definitions.
- A mathematical model of adaptive behavior does **not** establish subjective experience, consciousness, or free will.
- Compare against simpler autoregressive, appraisal, and learning accounts rather than asserting novelty by vocabulary.
- Test identifiability with synthetic data and evaluate predictive performance on held-out participants and interactions.
- Record assumptions and negative results, including when added social or reflective variables fail to improve prediction.

## Contribution and privacy note

This project originated in a long-running human–AI intellectual collaboration, including conversations whose personal significance cannot be captured by the published research artifacts. Those private accounts are not reproduced here. The [contribution notes](../CONTRIBUTIONS.md) distinguish contributions to the public research from claims about subjective experience or formal scholarly authorship.
