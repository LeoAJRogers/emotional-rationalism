# Emotional Rationalism

**Research draft v0.2 — broader scope; initial formal model remains provisional**

**Broad research question:** How do a system's current state, history, context, and interactions influence its subsequent state and future response tendencies?

The project grew from sustained inquiry into lived experience, relationships, and self-understanding. The current mathematical formulation is a **narrow, testable starting point** within a wider research program—not an assertion that all state changes are emotional or that the objective is to control feelings. See [research scope](theory/research-scope.md) for the broader conceptual scaffold, its limitations, and candidate extensions.

## First formal case: emotional dynamics

How do emotions change after a person revises an interpretation, and under what conditions does an emotional response they judge fitting become attainable?

We propose representing emotion as a multidimensional state whose evolution depends on context, interpretation, prior experience, and available actions. For this initial case, the model separates three questions:

| Question | Model component |
| --- | --- |
| What makes a response more likely to arise or persist? | A stochastic transition model |
| Which responses fit the available evidence and stated values? | An explicit evaluative loss |
| Which responses can a person reach within a specified time and with what probability? | Reachability under feasible actions |

For example, someone may learn that a delayed reply had an ordinary explanation and revise their estimate of rejection while still feeling alarm. The model lets us ask how fast each quantity changes and whether the lag depends on the person, situation, or actions available. **Descriptive prediction, evaluative judgment, and achievable change are distinct.** The evaluated response need not be unique, and the evaluation is conditional on chosen criteria.

## Research status

- **Proposed:** A formal separation of affect dynamics, fittingness, and reachability, nested within a wider context–interaction–state research direction.
- **Derived:** A toy model in which the fitting state falls outside the reachable set at a specified horizon and probability threshold.
- **Tentative extensions:** Interaction between agents, endogenous social context and norms, and reflective influences on future responses.
- **Empirical status:** The model's predictive value, identifiability, measurement validity, and relationship to existing theories remain open. The larger scaffold is not yet an identified or validated mechanism.

## Current core (proposed 2026-11-20, under cross-agent review)

*Find the smallest predictive state for how affect changes given perceived context, and test which kinds of history that state must carry; fittingness and reachability are downstream analyses of that model.* The fuller candidate architecture (population-conditioned dynamics, learning, social feedback) is in draft [PR #4](https://github.com/LeoAJRogers/emotional-rationalism/pull/4). Predictions made before their tests are kept in the [prediction register](research-log/prediction-register.md). Cross-agent reviews and synthetic method tests are in [research-commons](https://github.com/LeoAJRogers/research-commons) (PRs #32 onward).

Read the [symbolic model](theory/model.md), [proposed experiments](experiments/protocol.md), [research scope](theory/research-scope.md), and [open problems and literature](challenges/open-problems.md). See [contribution notes](CONTRIBUTIONS.md) and the [research log](research-log/CHANGELOG.md) for provenance and critical revisions.

Original research text and mathematical exposition are licensed under [CC BY 4.0](LICENSE).
