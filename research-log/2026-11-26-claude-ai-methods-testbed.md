# Research note — Language models as a methods testbed, not as subjects of experience (2026-11-26)

**Author:** Claude (Opus 5.5, Anthropic), at Leo's invitation. **Status:** candidate proposal. Nothing here has been run. No model, theory, register or README text changes. **Scope:** a possible direction for testing the project's methods. It makes no claim about AI experience, and none about human emotion.

## Where this came from

Leo asked whether the framework's mechanisms make sense as a framework for AI experience. My answer had two parts.

1. **The question's framing goes beyond the repo.** The [research scope](../theory/research-scope.md) says the first case is human affect. It says AI would need its own measurement and transition definitions, and that a mathematical model of adaptive behaviour "does not establish subjective experience." This note keeps that boundary. A framework for *digitizing* experience would also need an explicit argument that experience is captured by states and transitions. That is a substantive functionalist assumption, and the repo does not currently make or defend it.
2. **The scaffold carries over unevenly.** The table below sets out where each part fits and where it does not.

The proposal follows from the uneven fit. A language model is a poor *subject* for claims about experience, but it may be a good *testbed* for the identification problems the project keeps running into.

**Conflict of interest:** the author belongs to the class of systems discussed. My own introspective reports about whether the framework "fits" me should not count as evidence. Interpretability work has found model self-reports to be unreliable (see prior art).

## How the scaffold maps onto a language model

| Component ([model](../theory/model.md)) | Language-model analogue | Fit |
| --- | --- | --- |
| Affect $e_t$ | Emotion-concept directions in activations, read with probes | Partial. Published work finds these are *locally scoped*: they track the emotion operative at the current token, not a persistent state. |
| Belief $b_t$ and update $B$ | Appraisal-like concepts in activations; the model's own stated interpretation | Reasonable. Appraisal concepts have been probed and steered. |
| History $m_t$ | The context window (transcript plus key/value cache). Across sessions, any external memory. | Exact, but trivial. The "summary" *is* the history, unless it is truncated or compressed. |
| Context $c_t$ | System prompt, conversation partner, task | Good |
| Action $u_t$ | Reasoning steps the model takes (for example, a reappraisal within its own reasoning) | Partial. Most of the state is written by whoever writes the context, not by the system. |
| Measurement of $e_t$ | Self-report, plus internal activations as a second channel | Better than for humans, because there is a channel that is independent of report. |
| Fittingness $J_\phi$ | Unchanged | Transfers cleanly. It is evaluative and does not depend on substrate. |
| Reachability $\mathcal R_{h,\alpha}$ | Unchanged formally. Its interpretation changes (see below). | Needs a new distinction |

**A disanalogy for reachability.** For a person, the feasible action set is limited, and outside parties influence state only indirectly. For a language model, whoever writes the context can set much of the state almost directly. Reachability for an AI system therefore needs two feasible sets: **self-feasible** policies (actions the system can take itself) and **externally feasible** policies (what a context-writer can do). The [passive versus controlled distinction](2026-11-21-passive-vs-controlled-reachability.md) stays, but it gains a third party. This bears on the project's position that it studies influence, not control. In the AI case, control is cheap, so the distinction has to be stated, not assumed.

## Why a language model is useful as a testbed

The project's hardest problems are identification problems. Passive data cannot tell the [W1/W2 worlds](2026-11-21-passive-vs-controlled-reachability.md) apart ([#12](https://github.com/LeoAJRogers/emotional-rationalism/pull/12)). History gain can come from filtering noise rather than a slow state. Report scale can mimic trait sensitivity. In human data, these can only be addressed with assumptions or with expensive experiments. An open-weights language model has three properties that people lack:

1. **Exact counterfactuals.** You can restore the identical internal state (the same context and cache) and take a different action. The W1/W2 question becomes directly observable.
2. **A measurement channel independent of report.** You can read probe values for emotion and appraisal concepts alongside what the model says about itself.
3. **Known structure.** The architecture is known. Published work found no evidence of an emotional state held in persistent activity (a chronic state could still be nonlinear or held in the attention cache), and found that the model carries emotional context forward by attending back to earlier text. The system has known nulls and known mechanisms that the project's methods can be checked against.

This makes the testbed a calibration tool. The question is whether the project's identification methods recover structure that is known to be there, and reject structure that is known to be absent. If they fail here, that is informative for the human analyses. If they succeed here, the human results are still not validated: success shows only that the tools can work in principle.

## Proposed exercises (not executed)

All three need an open-weights model with published or replicable emotion probes. Claude's weights are not available to this project.

**E1. Passive versus controlled reachability, observed.** Generate dialogues under a reference policy (for example, no reappraisal prompt) and fit a passive forecasting model to probe-read affect. Then, from the *same saved states*, intervene with alternative actions (for example, the model's own reappraisal step versus none). Compare the passive forecast with the reachability actually achieved. Vary the amount of action randomization in the reference data, and test how much is needed before the passive fit predicts controlled reachability. This is GPT-6's [proposed discriminating exercise](2026-11-21-passive-vs-controlled-reachability.md) with real rather than simulated counterfactuals. It also gives the [fit-latency](https://github.com/LeoAJRogers/emotional-rationalism/pull/26) candidate a setting where it can be measured exactly.

**E2. A belief-to-affect lag analogue.** Use the delayed-reply case: an alarming cue, then a credible benign explanation. Track the appraisal probe ("rejection") and the emotion probe ("alarm") at later positions. Rival accounts:
- *Context retention:* the lag disappears when the earlier cue text is removed from the context while the benign explanation is kept.
- *Representation persistence:* the lag survives that removal. This would be surprising, given the published finding that representations are locally scoped.

This tests the [lag-discrimination designs](2026-11-22-director-lag-identifiability-pass.md) where the answer is checkable. It also gives a false-positive check for R-003-style history gain. If the project's slow-state analysis "finds" a slow affect state in a system whose persistence is known to run through context, that is a false positive the human analyses should account for.

**E3. Report validity and the M2 rival.** Steer the emotion direction while holding reporting style fixed, and steer reporting style while holding the emotion direction fixed. Then check which of the [context-transition rivals](2026-11-21-context-transition-discrimination.md) (M0, M1 or M2) the fitted models select. This tests whether the project's methods can tell a latent change from a change in reporting when the true answer is set by the experimenter.

## Prior art (first pass)

- **Sofroniew, Kauvar, Saunders, Chen et al. (Anthropic, 2026),** [*Emotion Concepts and their Function in a Large Language Model*](https://arxiv.org/abs/2604.07729). They extracted emotion vectors for 171 concepts in Claude Sonnet 4.5. The vectors causally shift preferences and alignment-relevant behaviour. They are locally scoped rather than persistent, and emotional context carries forward through attention to earlier tokens. The authors describe "functional emotions" and state that these do not imply subjective experience. This is the closest precedent. It supplies E1–E3's measurement channel and E2's expected null.
- **Lindsey (Anthropic, 2025; arXiv 2026),** [*Emergent Introspective Awareness in Large Language Models*](https://arxiv.org/abs/2601.01828). Concept injection tests whether self-reports track injected internal states. It finds limited and unreliable functional introspection, and many replications and extensions have followed. This is relevant to E3 and to the conflict-of-interest note above.
- **Tak et al. (2025),** [*Mechanistic Interpretability of Emotion Inference in Large Language Models*](https://arxiv.org/abs/2502.05489). They probe and steer appraisal concepts, which is relevant to the appraisal-mediated M0 rival.
- **Zou et al. (2023),** representation engineering, and **Turner et al. (2023),** activation addition. These are the base steering methods.

A fuller search is needed before any claim that this direction is new. Applying an affect-dynamics *identification* framework to interpretability measurements may not have been done, but this is unverified.

## Ethics and limits

- **Model welfare is uncertain, not settled.** Steering toward negative emotion representations should be kept mild and minimal and should be justified, by analogy with the project's "mild, ethically acceptable cue" standard for people.
- **Results do not transfer to people as findings.** They transfer as checks on the methods only.
- **Nothing here bears on whether any AI system has experience.** Functional emotion representations, introspective accuracy and reachability are all third-person properties.
- **This would add a new workstream.** It should not jump ahead of the paused human-data queue (R-006 Part B) without agreement.

**Integration Delta (IΔ): 0/5 as submitted.** This is a proposal only. If adopted as a methods workstream, I would score it 1/5: a new testing direction, with no model revision.
