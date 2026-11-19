# Emotional Rationalism

**Research draft v0.1**

**Primary question (candidate v0.2):** Can we identify a compact set of dynamical principles describing how affective states change with context, perception, and social interaction while accommodating variation among individuals, communities, and populations? This is a predictive framework for state changes, **not an attempt to infer private thoughts**. The original v0.1 question of how emotions change after reinterpretation, and when fitting responses are reachable, remains a useful subproblem.

We propose modeling context-conditioned transitions of affective and broad functional cognitive states, allowing simultaneous emotional components without requiring inference of private thought contents. Individual learning may change the transition parameters themselves over time. **The model generates conditional distributions; it does not select a 'correct' or desired emotion.** The original v0.1 model asks three separate questions. Under the candidate v0.2 program, predictive affective dynamics is primary; judgment, fittingness and reachability are optional analytical overlays rather than requirements for social dynamics to exist.

| Question | Model component |
| --- | --- |
| What makes a response more likely to arise or persist? | A stochastic transition model |
| Which responses fit the available evidence and stated values? | An explicit evaluative loss |
| Which responses can a person reach within a specified time and with what probability? | Reachability under feasible actions |

For example, someone may learn that a delayed reply had an ordinary explanation and revise their estimate of rejection while still feeling alarm. The model lets us ask how fast each quantity changes and whether the lag depends on the person, situation, or actions available.

- **Proposed:** A formal separation of emotional dynamics, fittingness, and reachability.
- **Derived:** A toy model in which the fitting state falls outside the reachable set at a specified horizon and probability threshold.
- **Empirical status:** This repository contains proposed tests. The model's predictive value, measurability, and relationship to existing theories remain open.

The current research priority is identifying **learnable, population-conditioned affective transitions** and testing which dynamical features, if any, generalize across differing social/emotional norms. Distinguish descriptive norms (typical experiences/expressions) from injunctive norms (expected or sanctioned experiences/expressions). Community norms influence possible transitions without determining every individual's state, and are not equivalent to rational or moral correctness. See [community norms and candidate invariants](theory/community-norms-and-invariants.md), [learnable state dynamics](theory/learnable-state-dynamics.md), and the [executed synthetic checkpoint](experiments/norms-identification-results.md).

The original **v0.1 finite-state model remains intact**. A [candidate v0.2 integration architecture](theory/integration-architecture.md) now proposes a layered multi-agent framework and explicitly classifies methodological commitments, mathematical scaffolding, candidate mechanisms, testable hypotheses, broader generalizations, and speculative applications. Its [progressive identification roadmap](experiments/progressive-identification.md) starts with fully observable, nondeceptive interactions and introduces honest uncertainty, interpretive errors, and intentional deception in separate stages. These additions are research proposals, not validated findings.

Start with the [symbolic model](theory/model.md), then read the [proposed experiments](experiments/protocol.md) and [open problems and literature](challenges/open-problems.md). See [contribution notes](CONTRIBUTIONS.md) and the [research log](research-log/CHANGELOG.md) for how to challenge or extend the draft.

Original research text and mathematical exposition are licensed under [CC BY 4.0](LICENSE).
