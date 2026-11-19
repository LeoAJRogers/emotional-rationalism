# Population-first scope correction: affective dynamics, not mind reading

**Date:** 2026-11-19  
**Status:** Foundational scope clarification to the candidate v0.2 integration, not an empirical finding.  
**Provenance:** User clarified that the central target is the emergence of altered/affective states from context and the dynamics of an agent's community, rather than predicting anyone's thoughts. GPT formalized this as the population-level prediction target and comparative program.

## Revised central question

**Can we identify a compact set of dynamical principles that describe how affective states change with context, perception, and social interaction, while accounting for differences between individuals, communities, and populations?**

Here "altered state" means a change in an affective/emotional or emotion-related functional state relative to baseline, **not necessarily a drug-induced altered state**. The state might be latent and measured imperfectly through behavior, physiology, experience reports (where meaningful), and dynamics; cross-species functional state resemblance does not prove equivalent subjective experience.

**Primary goal: calibrated conditional distributions of state/trajectory changes** under context, socially structured interaction, and available observations. This may be expressed as

\[
p_{\Theta_g}\!\left(z_{i,t:t+h}\mid {\cal C}_{t:t+h},\,{\cal R}_{g,t},\,o_{i,\le t},\,z_{i,t},\,{\cal H}_{i,t}\right)
\]

where:
- \(g\) indexes a population/community/ecology, not necessarily a species;
- \(z\) is an operationally specified affect-relevant latent state, or a measured proxy if the latent variable is not identified;
- \({\cal C}\) is environmental and event context;
- \({\cal R}_g\) is the community's social structure, patterns of coordination, relationships, norms and distributions of social actions;
- \(o_i\) represents cues accessible to an individual; no direct access to their private thoughts is presupposed;
- \({\cal H}_i\) collects relevant individual history, baseline, and role where evidence allows.
- \(\Theta_g\) is a population-configured parameter family, ideally with recoverable shared components and residual population-specific differences.

The prediction is a **distribution over state transitions, not a claimed correct reading of a particular mind**. Population-average predictions may be less precise for individuals; uncertainty must be displayed.

## Foundational design decisions

1. **Social dynamics exist with imperfect agents and imperfect observers.** Perceptual mistakes, inaccurate evidence assessment, poor reasoning, low self-awareness and ineffective emotion regulation can all be ordinary causes of the process, not exclusions. The researcher's own evaluation can likewise be wrong.
2. **Latent beliefs are optional mechanisms, not the prediction objective.** Include belief/appraisal variables only when they improve held-out conditional transition predictions, support an identifiable intervention, or represent a needed mechanistic distinction. Do not silently turn a model of affective change into theory-of-mind reconstruction.
3. **Context is *relational*.** The same physical cue may carry different social significance depending on community ecology, relationship, role, prior interactions, and perceptual access. The mapping from observed cues to social meaning need not be shared across populations.
4. **A general kernel is a design aim; universal emotional content is not an axiom.** Candidate common principles (persistence, graded intensity, generalization, reciprocity, competition, affiliation, uncertainty sensitivity, feedback) are hypotheses. Similar descriptions can arise by convergent mechanisms; homologous mechanisms may serve divergent social roles.
5. **Population differences must be testable and representable.** Try parameter sharing, hierarchical population effects, transferable transition structures, and fully population-specific alternatives. Never force equivalent affect labels across species.
6. **Normative/evidence-based evaluation, rationality, and reachability are *optional analytic lenses*** built around the descriptive model. They do not govern whether the social system can evolve or whether an agent's state changes, and they are not prerequisites for predictive success.
7. **Measurement constrains claims.** Human self-report and physiology can give different glimpses; animal data often provide behavioral and physiological proxies. Where the latent emotional state is unidentifiable, predict those operational outcomes and say so rather than asserting direct access to experience.

## Comparative starting points, not universal truths

Ask whether some *properties of the dynamics* recur across populations:
- **Persistence:** state effects can continue after a trigger disappears.
- **Scalability and nonlinear switching:** intensity varies and can generate changes in policy/behavior.
- **Generalization:** state changes caused in one context alter response in another.
- **Reciprocal influence:** one agent's response modifies the subsequent cue landscape for others.
- **Population tuning:** socially relevant events and their state consequences depend on ecology and the social organization.
- **Relationship dependence:** the same behavior can mean different things from a friend, competitor, relative, or stranger.

Do not assume every feature is shared by every organism, or that a similar feature implies the same emotion or neural implementation.

## First comparative identification experiment

Keep the existing two-agent synthetic test as a **restricted implementation/methodology check**, not as the definition of the scientific target. Its explicit inferred-intent feature is one intentionally testable mechanistic choice.

Add a second, population-centered synthetic benchmark:

- **Population A:** affiliative, frequent reciprocal interactions; separation/exclusion cues have a large effect.
- **Population B:** more solitary/territorial, different baselines, different social-affordance weights and signal access.
- **Population C (stress test):** invented incompatible mapping of social cues to relevance, such that the same naive labels or response weights cannot transfer.
- **Training:** compare pooled universal parameters, hierarchical/shared-core plus population-specific parameters, and independently fitted population models.
- **Tests:** held-out episodes, interactions, and within-population agents, then an unseen population with explicitly supplied configuration/calibration observations.
- **Critical criterion:** generality means fewer *transferable structural assumptions or parameters* with comparable held-out predictions, not that the same social cue produces identical emotional changes in everyone.
- **Negative result:** if no common kernel performs satisfactorily, preserve the population-specific models and identify the failed invariance.

Separately test fully informed versus inaccurate-observer conditions **within each population**, rather than allowing human-style cognitive appraisal to become the default mechanism.

## Relationship to existing v0.1 work

The finite-state dynamics/evaluation/reachability framework and its toy result are preserved. However, the primary scientific deliverable is now the **population-conditioned descriptive state transition model**. Evaluation and reachability remain interesting downstream analytic research programs, not mandatory modules in every application.

## Prior research relevant to this direction

- Anderson, D. J. & Adolphs, R. (2014). *A Framework for Studying Emotions across Species*. Cell 157, 187–200. [Open manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC4098837/). Provides cross-species functional criteria such as scalability, persistence, generalization, and valence. These are proposed useful comparative primitives, not demonstrated universal laws.
- [Beyond the dichotomy between field and lab — the importance of studying cognition in context](https://www.sciencedirect.com/science/article/pii/S235215462200078X) (2022). Discusses ecological and social contextual effects on animal cognition.
- [Reciprocal processes of sensory perception and social bonding: an integrated social-sensory framework](https://pmc.ncbi.nlm.nih.gov/articles/PMC9744507/) (2022). Highlights that sensory systems and social behavior differ across species.
- [Animal emotion: Descriptive and prescriptive definitions and their implications for a comparative perspective](https://pmc.ncbi.nlm.nih.gov/articles/PMC6041721/) (2018). Notes the distinction between operational criteria for emotion and wider claims about subjective welfare/experience.

**Research caution:** Human concepts of social norm, moral responsibility, deception, or verbal appraisal are not automatically suitable variables in every population. First compare properties that can be operationalized with that population's own sensory and social repertoire.
