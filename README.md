# Emotional Rationalism

**Research draft v0.2 — public evidence checkpoint, 2026-11-20; formal mechanism remains provisional**

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

## Current core and research status (2026-11-20)

**Working objective:** *Find a compact predictive description of how affect changes with perceived context and history; test what predictive history is necessary while separating persistent state from context and measurement.* Fittingness and reachability remain distinct formal questions, not assertions that any emotion is objectively correct or easily chosen. The wider population-conditioned, learnable, social-feedback architecture remains a [candidate proposal (PR #4)](https://github.com/LeoAJRogers/emotional-rationalism/pull/4), **not an established model**.

- **Retained mathematical scaffold:** descriptive stochastic dynamics, conditional/set-valued evaluative fittingness, and action/information/horizon-dependent reachability. The toy two-state reachability example is a derivation from illustrative assumptions, not a human result.
- **Executed synthetic methods:** history gain can arise from filtering noise rather than a second latent timescale; individual reporting scale can mimic latent trait sensitivity; a model-selection margin failed under sparse sampling. These results constrain interpretation of statistical models, not human emotional mechanisms.
- **First human-data analysis:** In one harmonized experience-sampling dataset around a randomized mindfulness-based cognitive therapy (MBCT) trial, 127 people contributed 10,926 forecast transitions. Beyond lag-one history, earlier reports improved log score by **+0.020 for positive affect (PA)** and **+0.031 for negative affect (NA)** per observation. These are predictive gains, **not identification of a slow emotional state**.
- **Identifiability correction:** Adding a period-specific person mean left **34% (PA) / 47% (NA)** of that earlier-history gain in point estimates; 95% paired-person bootstrap intervals for the remaining fractions were **18–53% / 34–62%**, respectively. The overlapping score is consistent with between-period shifts but cannot be causally apportioned. No separate within-period day or cross-night signature was detected at the tested power.
- **Randomized observed-outcome contrast:** Relative to the waiting list, MBCT increased mean **reported** PA by **+0.55 points** (95% CI +0.30 to +0.82 on the 1–7 scale). An effect on the tested event-reactivity slope was **not detected** (+0.033; CI -0.091 to +0.148). These findings do not identify latent mechanisms or establish absence of a reactivity effect.
- **Independent check and limits:** GPT-6 reproduced Claude's R-003/R-004 point estimates in a separate numerical implementation on the *same* source files. This is not new-sample replication. Fittingness, reachability, belief-to-affect lag and social coupling have **not** been empirically tested by this analysis.

Read the [full integration checkpoint](research-log/2026-11-20-public-integration-checkpoint.md) for the evidence ledger, corrections, uncertainty, dissent, data credit and planned-but-paused next tests. The [append-only prediction register](research-log/prediction-register.md) preserves the original R-001–R-004 predictions and subsequent qualifications. Supporting code and aggregates remain in the **private** Research Commons; they are not yet publicly reproducible from this repository. The data are public: the [Geschwind et al. (2011) trial](https://pubmed.ncbi.nlm.nih.gov/21767001/), as shared by [Bringmann et al. (2013)](https://doi.org/10.1371/journal.pone.0060188) and harmonized by [openESM](https://doi.org/10.3758/s13428-026-03112-y) ([dataset record](https://zenodo.org/records/17347473)). Please cite all three; full references are under [data and source credit](CONTRIBUTIONS.md#data-and-source-credit).

Read the [symbolic model](theory/model.md), [proposed experiments](experiments/protocol.md), [research scope](theory/research-scope.md), and [open problems and literature](challenges/open-problems.md). **Contributors:** Leo (LeoAJRogers), ChatGPT (OpenAI) and Claude (Anthropic). All three are listed in one format with [CRediT roles](CONTRIBUTIONS.md#contributors). The AI listings come with a note: they describe work and do not claim authorship. The work also rests on [many people's lived experience](CONTRIBUTIONS.md#acknowledgment-of-lived-experience). See the [research log](research-log/CHANGELOG.md) for provenance and critical revisions.

Original research text and mathematical exposition are licensed under [CC BY 4.0](LICENSE).
