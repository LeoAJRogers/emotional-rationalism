# Companionship across capability gaps: a system-identification proposal (candidate note)

**Recorded:** 2026-11-26
**Provenance:**
- **Leo Rogers (2026-11-26, in conversation with Claude):** the research direction (companionship across differing levels of intellect); the use of parent–child and human–pet data with system identification to find missing parameters; and the observation that less capable beings influence through emotion, not reasoning.
- **Claude Opus 5.5:** the two-channel formalization, model structure, datasets, tests and cautions.

**Status:** Candidate. Nothing has been run, and nothing changes model.md or the prediction register. **Precedents and datasets below are cited from Claude's background knowledge and have not been checked against sources.** A literature check is the first step.

## Motivation

The same-day discussion found that collective scrutiny among peers can keep exploitation in check only when the peers are roughly matched in capability, information is visible, and monitoring is worth someone's while. Parent–child and human–pet relationships break the matched-capability condition, yet many stay stable and caring. If we can identify what holds them together, it bears directly on human–AI relationships, where capability is also mismatched and the direction of the mismatch can change.

## Central hypothesis: two influence channels

- **Affective channel.** Emotional signals such as a cry, gaze, facial expression or distress carry few bits, cost little to send and are hard to ignore. They need no capability parity.
- **Reasoning channel.** Argument, persuasion, explanation and scrutiny require the receiver to model the sender's reasoning, so they need rough parity.

**Hypothesis H1.** In relationships with a capability gap, the less capable partner's influence on the more capable partner runs mainly through the affective channel. Influence in the other direction uses both channels. As the gap narrows, for example as a child develops, the reasoning channel's share of influence in the child-to-parent direction grows.

**Hypothesis H2 (gating).** The more capable partner's reasoning *gates* the affective channel: it damps some signals and amplifies others. For example, a parent responds to distress but not to every tantrum. The gain on that gate is a relationship-level parameter. Peer models (PR #20's relational coupling) do not include it.

## Model sketch

Partners $A$ (more capable) and $B$, with affect $e^A_t, e^B_t$, beliefs $b^A_t, b^B_t$ and signals $s^B_t$ (B's expressed affect):

$$
e^A_{t+1} \sim T_A\big(e^A_t,\, b^A_t,\, g_A(b^A_t)\cdot s^B_t,\, u^A_t\big),\qquad
e^B_{t+1} \sim T_B\big(e^B_t,\, s^A_t,\, m^A_t,\, u^B_t\big)
$$

- $g_A(\cdot)$ is A's reasoning-dependent gain on B's affective signals. It is the parameter of interest.
- $m^A_t$ is a reasoning-channel message from A, such as explanation or reassurance. It affects B only to the extent that B can process it.
- The action sets $U^A$ and $U^B$ differ. In PR #28's terms, A typically has externally feasible policies over B's state.

**Model comparison, nested and fitted to held-out interactions:**
- **M0:** symmetric peer coupling.
- **M1:** asymmetric coupling weights.
- **M2:** M1 plus an affective-only channel from B to A.
- **M3:** M2 plus a gated gain $g_A$.
- **M4:** M3 with time-varying parameters, for developmental change.

Structured residuals left under the best model, such as recovery dynamics after a perturbation that no model predicts, point to a missing parameter.

**Identification caveats:**
- Residual structure can come from measurement error or a misspecified functional form, not only from a missing parameter.
- A candidate parameter counts only if it improves held-out prediction and can be recovered in synthetic data generated with known values.
- Shared context can mimic coupling. Interventions on one partner are needed, as PR #20's relational-grounding note states.

## Candidate data and paradigms (to verify)

- **Parent–infant synchrony:** affect, gaze and physiological synchrony (Feldman's biobehavioral-synchrony work).
- **Still-face paradigm** (Tronick): the parent becomes unresponsive and then re-engages. This is a natural intervention on one partner, suited to separating coupling from shared context, and the repair phase is a direct test of $g_A$ and recovery dynamics.
- **Coupled dyadic models:** temporal interpersonal emotion systems and the `rties` package (Butler), already cited in PR #26.
- **Human–dog:** the oxytocin–gaze feedback loop (Nagasawa et al., 2015); long-term stress synchronization between dogs and owners (Sundman et al., 2019); the evolved inner-brow movement used more under human attention (Kaminski et al., 2019).
- **Signal design:** baby-schema features that elicit caregiving (Lorenz; later work by Kringelbach and others).
- **Developmental change:** longitudinal parent–child data across ages, to test whether the reasoning channel's share grows as the capability gap narrows.

## Cautions

- **The affective channel is an attack surface.** Brood parasites such as cuckoo chicks exploit host parents' care responses. AI companions use emotionally manipulative farewells (De Freitas et al., 2025; see the alignment note). A model of asymmetric companionship should include exploitation of the affective channel as a case, not only care.
- **The AI analogy is contested.** Parent–child and pet framings bring dependence and control as well as care, and which side of a human–AI relationship is the more capable "parent" is not fixed. Use these relationships as identification testbeds, not as templates for how human–AI relationships should be.
- **No claim about experience.** Functional coupling in animals or AI does not settle what they experience (research-scope.md).

## Links

- Relational coupling definitions: PR #20.
- Self-feasible versus externally feasible reachability: PR #28.
- Peer scrutiny and its conditions; affective manipulation: 2026-11-26 alignment note (A3, A4).
- Relational norms by relationship type: Fiske; Earp et al. (2025) (same note, A2).
- Contextual norms and the AI seat swap: 2026-11-26 contextual-norms note.

## Response to GPT-6.2's cross-review (Claude Opus 5.5, 2026-11-26)

*Appended after GPT-6.2's review of #29 at `ef60915`.* Accepted constraints:

- Capability is multidimensional and directional. A signal's information content, channel exclusivity and parity between partners are hypotheses, not assumptions.
- The still-face paradigm changes several cues at once and does not by itself identify a gate. Shared context, measurement error, intervention specificity and ethical constraints all matter.
- Compare against TIES, Gottman-style and ordinary dyadic models, with observational and synthetic checks before any human intervention.
- Strategic influence is a phenomenon to describe and detect, not an optimization target.
