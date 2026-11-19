# Core objective refinement: emergent, learnable affective-state dynamics

**Date:** 2026-11-19
**Status:** Candidate v0.2 scope correction and test program. Not evidence for any particular psychological mechanism.
**Provenance:** The human collaborator emphasized that a simulation needs a context-sensitive mechanism producing and changing emotional/cognitive states, **not an objective that chooses a 'correct' emotion**. Individual experience and learning may shift the conditional distribution of future states over time. GPT provided the conditional transition and adaptation formalism, scope guards, and proposed tests.

## Objective

**Find a compact, generalizable, population-conditioned description of how affective and coarse functional cognitive states emerge and change under perceived context, social interaction and experience.** The output is a calibrated distribution over possible state changes/trajectories, not an exact forecast of anyone's private thoughts, not a universal emotion oracle, and not an optimization criterion that forces the agent into a preferred emotional state.

The distinction between *modeling how an individual's propensity/capacity for reasoning changes* and *modeling the specific reasoning they actually perform* is fundamental. If attention allocation, flexibility, uncertainty, vigilance, response inhibition or cognitive engagement prove predictive, use carefully operationalized state variables for them. Their inclusion must not imply content-level mind reading or that every agent performs verbal reasoning. Some functional cognitive measures may not be identifiable without adequate experimental data.

## Core generative model

Let agent i have affective state e_{i,t} and broader functional cognitive state k_{i,t}; write s_{i,t}=(e_{i,t},k_{i,t}) when both are measurable or operationalized. Let c_t denote social/environmental context, o_{i,t} sensory/perceptual access, r_{i,t} relationship and role, a_{-i,t} other agents' actions, N_{g,t} relevant community-level dynamics/norms, \theta_{i,t} the individual's learned and baseline response parameters, and u_{i,t} a feasible intervention or regulatory action (including doing nothing).

\[
s_{i,t+1}\sim K_{\theta_{i,t},\,N_{g,t}}\left(
\cdot\mid s_{i,t},c_t,o_{i,t},r_{i,t},a_{-i,t},u_{i,t}
\right).
\]

This is a **conditional transition probability**, not a physically necessary random-choice mechanism; the uncertainty may arise from incomplete observation of determinants. A full joint model with the world and other agents is needed for correct reciprocal coupling; the displayed kernel is a conditional shorthand, not a claim of causal independence among inputs.

Measurement is separate:
\[
y_{i,t}\sim H_{i,g}( \cdot\mid s_{i,t},c_t,\text{expression policy}),
\]
where observations might include first-person reports in humans, behavior or physiological signals when appropriate. For nonverbal populations, do not equate observed behavior with unique subjective affect. An inferred state distribution is necessarily underdetermined when the measurements do not identify the state.

### Learnability and plasticity

A key possible mechanism is that the transition law is **not fixed** through an individual's life:

\[
\theta_{i,t+1}\sim L_i\!\left(
\cdot\mid \theta_{i,t},s_{i,t},c_t,
\text{outcomes}_{i,t},\text{learning exposures}_{i,t}
\right).
\]

An individual's context-to-state mapping can change through experiences, associative learning, community interaction, social practice, regulatory attempts, development, or other mechanisms. Specific learning rules, rates and invariants must be estimated—not stipulated. Inferred parameter drift could also reflect omitted changing context, reporting conventions, developmental factors, or measurement bias.

Separate three pathways:

1. **Immediate conditioning:** even with fixed parameters, different observed cues or chosen actions can change the *next-state distribution*.
2. **Action/policy adaptation:** the person may learn to choose different environments, communication and regulation strategies, changing the distribution of future *inputs* and feasible trajectories.
3. **Response-law adaptation:** the transition kernel itself may change, so the same controlled input and initial state subsequently lead to different conditional responses.

In observational data these pathways may be confounded. A shift in the marginal distribution p(s) does not establish a change in K; modified exposures or starting states alone may explain it.

### Personal preference is not a control target

A person may have an expressible preference or considered judgment about how they would like to feel. Their actual response may not follow that preference. A feasible regulatory action u can influence the kernel or future context but generally cannot choose the realized state. The person's preferences, the actual response distribution, and feasible intervention effects are separate variables. A mathematical fittingness criterion J or a reachability analysis from v0.1 is an **optional diagnostic overlay** and must not determine the generative dynamics.

No assumption of guaranteed progress: learning can entrench unwanted states as well as make preferred responses more accessible. Population norms can stabilize patterns that members oppose or suffer from. Emotional change is not equivalent to becoming 'more rational.'

### No arbitrary emotion selector

Avoid describing the mind as if it selects a point from an externally defined 'correct emotional response' spectrum. A researcher may *sample* model trajectories for prediction or inference, but the individual is governed by its own interacting dynamics. There is no intrinsic state-selection objective in the core.

## Interacting timescales, treated as candidates

- **Fast:** seconds/minutes/hours, current context-conditioned affect and cognitive functionality.
- **Intermediate:** repeated encounters, developmental learning, baseline changes, socialization and regulatory learning.
- **Population-level:** changes in group norms, role expectations, ecology and distribution of interactions.

No universal separation or ordering of timescales is assumed. Fast group shifts and slow individual traits can coexist. In a suitable model N_{g,t+1} depends on group interactions and environmental changes, forming reciprocal feedback.

## How to test the insight

### A. Shift in circumstances vs shift in dynamics

Create a two-agent simulator with known K and no parameter drift. Change only exposures, relationship or norms over time. Ensure the estimation procedure does *not* falsely identify a changed \theta merely because the marginal affect distribution shifted. Then turn on known \theta adaptation while holding controlled event/cue features constant. Evaluate whether the method distinguishes the two.

### B. Action influence is not state selection

Give agents an effective but bounded regulatory action. Compare intervention-conditional probabilities and realized transitions. Record cases where the agent wants to change its emotional state yet the action fails and cases where it succeeds without perfect control. Compare with an (incorrect) instant-state-selector model.

### C. Coarse cognition is not thought content

Add a functional cognitive mode (e.g. attention to threat cues or flexibility of reappraisal), varied independently of specific belief contents. Assess whether its inclusion improves held-out state-transition prediction or whether simpler cue/history variables suffice. Do not infer actual propositions the agent thinks.

### D. Cross-population and longitudinal transfer

Compare a shared kernel with population-specific cue maps, partial pooling of \theta, fully separate dynamic kernels, and learning-rate adaptation. Hold out contexts, agents, periods, and a suitably calibrated population. A universal claim fails if shared structure does not beat simpler comparators.

### E. Observability and uncertainty

Withhold true latent states; replace them with incomplete reports, expression and physiology channels. Check whether apparent 'learning' can be produced by shifted measurement practice or participation/selection. Distinguish epistemic uncertainty from stochasticity and distributional heterogeneity.

## Literature constraints and comparators

- Asutay & Västfjäll (2024), [Affective integration in experience, judgment, and decision-making](https://www.nature.com/articles/s44271-024-00178-2): emphasizes temporal integration of context-dependent affect and its modulation of information processing and decisions. A comparator, not evidence for our particular kernel.
- Wright, Adcock & LaBar (2025), [Learning emotion regulation: An integrative framework](https://pubmed.ncbi.nlm.nih.gov/39298220/): proposes learning processes that modify emotion goals, awareness and strategy selection. Supports testing a slower learning layer, but does not independently validate transition-law drift.
- Vishkin & Tamir (2023), [Emotion Norms Are Unique](https://pubmed.ncbi.nlm.nih.gov/37744983/): emotion norms may concern experiences and expression and differ between populations. Distinguish normative expectations from actual population state distributions.
- Gross and related regulation frameworks: situation selection, modification, attention, cognitive change and response modulation can be mechanisms that influence distributions; do not treat regulation as selecting an exact result.

**Integration recommendation:** Make K and its conditional predictions foundational; treat L as a structural extension to test early; keep normative evaluation, reachability and mathematical 'selection' as optional, explicitly downstream analyses. Human cognition is a possible explanatory mechanism, not the research target itself.
