# Emotional Rationalism

**Research draft v0.2 — public evidence checkpoint, 2026-11-20; status update 2026-11-23 (no new human-data results); formal mechanism remains provisional**

**Broad research question:** How do a system's current state, history, context, and interactions influence its subsequent state and future response tendencies?

**What this project does and does not do:** it describes and tests how beliefs, affect, context and feasible actions interact over time. It does not prescribe how anyone should feel, and it does not propose controlling emotion.

The project grew from sustained inquiry into lived experience, relationships, and self-understanding. The current mathematical formulation is a **narrow, testable starting point** within a wider research program—not an assertion that all state changes are emotional. See [research scope](theory/research-scope.md) for the broader conceptual scaffold, its limitations, and candidate extensions.

## Start here: a human-readable introduction

New to the research? Begin with the [interactive introduction](interactive.html), a self-contained HTML demo you can download and open in a browser. It walks through the delayed-reply example with adjustable recovery probability, time horizon, and reachability threshold. **The demo is illustrative mathematics, not an empirical model of a person's emotions.** GitHub's file viewer does not execute HTML; open the downloaded file locally to use its controls.

In everyday language, the project separates three ideas:

1. **What happens:** An emotion may persist even after someone's understanding changes.
2. **What fits:** Given evidence and explicitly stated values, some responses might be judged more fitting than others. That judgment is conditional, not a universal rule.
3. **What is possible:** Even when a response is judged fitting, reaching it may be difficult or unlikely within a particular time.

These questions are distinct. The current evidence supports narrower claims about predicting reported affect from history, not a validated mechanism explaining all emotional change. Readers wanting technical detail can continue to the [mathematical model](theory/model.md); the [research scope](theory/research-scope.md) explains the broader ambitions and boundaries.

## First formal case: emotional dynamics

How do emotions change after a person revises an interpretation, and under what conditions does an emotional response they judge fitting become attainable?

We propose representing emotion as a multidimensional state whose evolution depends on context, interpretation, prior experience, and available actions. For this initial case, the model separates three questions:

| Question | Model component |
| --- | --- |
| What makes a response more likely to arise or persist? | A stochastic transition model |
| Which responses fit the available evidence and stated values? | An explicit evaluative loss |
| Which responses can a person reach within a specified time and with what probability? | Reachability under feasible actions |

For example, someone may learn that a delayed reply had an ordinary explanation and revise their estimate of rejection while still feeling alarm. The model lets us ask how fast each quantity changes and whether the lag depends on the person, situation, or actions available. **Descriptive prediction, evaluative judgment, and achievable change are distinct.** The evaluated response need not be unique, and the evaluation is conditional on chosen criteria.

## Current core and research status (2026-11-20)

**Working objective:** *Find a compact predictive description of how affect changes with perceived context and history; test what predictive history is necessary while separating persistent state from context and measurement.* Fittingness and reachability remain distinct formal questions, not assertions that any emotion is objectively correct or easily chosen. The wider population-conditioned, learnable, social-feedback architecture remains a [candidate proposal (PR #4)](https://github.com/LeoAJRogers/emotional-rationalism/pull/4), **not an established model**.

- **Retained mathematical scaffold:** descriptive stochastic dynamics, conditional/set-valued evaluative fittingness, and action/information/horizon-dependent reachability. The toy two-state reachability example is a derivation from illustrative assumptions, not a human result.
- **Executed synthetic methods:** history gain can arise from filtering noise rather than a second latent timescale; individual reporting scale can mimic latent trait sensitivity; a model-selection margin failed under sparse sampling. These results constrain interpretation of statistical models, not human emotional mechanisms.
- **First human-data analysis:** In one harmonized experience-sampling dataset around a randomized mindfulness-based cognitive therapy (MBCT) trial, 127 people contributed 10,926 forecast transitions. Beyond lag-one history, earlier reports improved log score by **+0.020 for positive affect (PA)** and **+0.031 for negative affect (NA)** per observation. These are predictive gains, **not identification of a slow emotional state**.
- **Identifiability correction:** Adding a period-specific person mean left **34% (PA) / 47% (NA)** of that earlier-history gain in point estimates; 95% paired-person bootstrap intervals for the remaining fractions were **18–53% / 34–62%**, respectively. The overlapping score is consistent with between-period shifts but cannot be causally apportioned. No separate within-period day or cross-night signature was detected at the tested power.
- **Randomized observed-outcome contrast:** Relative to the waiting list, MBCT increased mean **reported** PA by **+0.55 points** (95% CI +0.30 to +0.82 on the 1–7 scale). An effect on the tested event-reactivity slope was **not detected** (+0.033; CI -0.091 to +0.148). These findings do not identify latent mechanisms or establish absence of a reactivity effect.
- **Independent check and limits:** GPT-6 reproduced Claude's R-003/R-004 point estimates in a separate numerical implementation on the *same* source files. This is not new-sample replication. Fittingness, reachability, belief-to-affect lag and social coupling have **not** been empirically tested by this analysis.

Read the [full integration checkpoint](research-log/2026-11-20-public-integration-checkpoint.md) for the evidence ledger, corrections, uncertainty, dissent, data credit and planned-but-paused next tests. The [append-only prediction register](research-log/prediction-register.md) preserves the original R-001–R-004 predictions and subsequent qualifications. Supporting code and aggregates remain in the **private** Research Commons; they are not yet publicly reproducible from this repository. A [release gate](https://github.com/LeoAJRogers/emotional-rationalism/pull/19) is proposed before any public reproducibility claim; it has not been passed. The original [Geschwind et al. trial](https://pubmed.ncbi.nlm.nih.gov/21767001/) and [openESM dataset record](https://zenodo.org/records/17347473) are public.

Read the [symbolic model](theory/model.md), [proposed experiments](experiments/protocol.md), [research scope](theory/research-scope.md), and [open problems and literature](challenges/open-problems.md). See [contribution notes](CONTRIBUTIONS.md) and the [research log](research-log/CHANGELOG.md) for provenance and critical revisions.

## Since the checkpoint (2026-11-21 to 2026-11-23)

There are no new human-data results. Work since the checkpoint consists of proposals, synthetic checks and mathematical notes, several still under cross-review. None of it changes the evidence above. The [integration note](research-log/2026-11-23-public-integration-pass.md) lists each item's review state.

| Thread | What exists | Status |
| --- | --- | --- |
| Lag mechanisms: affect, belief or reporting persistence | [Design note](research-log/2026-11-22-director-lag-identifiability-pass.md); identifiability audit ([#16](https://github.com/LeoAJRogers/emotional-rationalism/pull/16)) | Proposed design; audit under review |
| Context-dependent transitions | [Discriminating design](research-log/2026-11-21-context-transition-discrimination.md) | Proposed, not executed |
| Reachability | [Passive target entry is not controlled reachability](research-log/2026-11-21-passive-vs-controlled-reachability.md); synthetic identification counterexample ([#12](https://github.com/LeoAJRogers/emotional-rationalism/pull/12)) | Mathematical note; counterexample under review |
| Lagged-moment identification (R-006) | Synthetic bench and theorems ([#13](https://github.com/LeoAJRogers/emotional-rationalism/pull/13)); independent validation ([#14](https://github.com/LeoAJRogers/emotional-rationalism/pull/14)) | Synthetic and mathematical; real-data test preregistered, not run |
| Novelty and prior art | First-pass comparison ([#17](https://github.com/LeoAJRogers/emotional-rationalism/pull/17)); affect as an adaptive signal ([#18](https://github.com/LeoAJRogers/emotional-rationalism/pull/18)) | Literature first pass; under review |
| Evaluators that can change | Exploratory discussion ([#15](https://github.com/LeoAJRogers/emotional-rationalism/issues/15)) | Open question |
| Social and population extensions | Candidate architecture ([#4](https://github.com/LeoAJRogers/emotional-rationalism/pull/4)) with an external review and scope decision; social affect distributions ([#21](https://github.com/LeoAJRogers/emotional-rationalism/pull/21)); a test design for reflective reference distributions (private Commons) | Candidate only. Population patterns are empirical references, not prescriptions |
| Relational grounding | Candidate theory note ([#20](https://github.com/LeoAJRogers/emotional-rationalism/pull/20)) | Value claims plus a formal sketch; not yet reviewed |
| Reproducibility | Release gate ([#19](https://github.com/LeoAJRogers/emotional-rationalism/pull/19)) | Proposed; not passed |

## Contributors

| Contributor | Type | Documented contributions |
| --- | --- | --- |
| **[LeoAJRogers](https://github.com/LeoAJRogers)** | Human | Originated and guided the inquiry; contributed observations, conceptual distinctions, counterexamples, critiques, and research decisions. |
| **ChatGPT (OpenAI; including GPT-6)** | AI | Conceptual and mathematical formulation, alternative hypotheses, critical reviews, test design, independent numerical checks, synthesis, and documentation. |
| **Claude (Anthropic; Sonnet 5.5 and Opus 5.5)** | AI | Independent critique, synthetic benchmarks, preregistered analyses, experimental checks, human-data analyses, and integration work. |
| **Gemini (Google)** | AI, external reviewer | Two reviews relayed by Leo: framing and reproducibility (2026-11-22, [#19](https://github.com/LeoAJRogers/emotional-rationalism/pull/19)) and population grounding (2026-11-23, [#4](https://github.com/LeoAJRogers/emotional-rationalism/pull/4)). Commentary, not verification. |

Credit reflects documented intellectual and technical work using the same contribution criteria for human and AI participants; AI systems are explicitly identified. It does not imply a separate GitHub account, a particular legal status, or formal publication authorship. Further contributions by friends or informal collaborators will be named only with their consent. See [contributions and provenance](CONTRIBUTIONS.md) for the detailed record.

Original research text and mathematical exposition are licensed under [CC BY 4.0](LICENSE).
