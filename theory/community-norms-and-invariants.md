# Community norms, affective norms, and candidate universals

**Date:** 2026-11-19  
**Status:** Scope refinement and falsifiable model proposal, not an empirical discovery.  
**Related:** [Population-first objective](population-first-objective.md) · [Integration architecture](integration-architecture.md) · [Identification roadmap](../experiments/progressive-identification.md)

## Central research target

Model conditional *distributions of affective (altered-state) transitions* in an individual embedded within a community, shaped by events, perceivable cues, relationships, individual baseline, and population-level regularities. **Do not infer private thoughts as the primary outcome**. Psychological inference is one optional mechanism, not the purpose of the model. Do not treat people as perfectly rational or competent evaluators of evidence.

Affect may have evolved mechanisms with cross-population commonalities while its social triggers, social meaning, magnitude, and regulation differ markedly by community. Shared processes and socially learned norms can coexist; test both. Individuals can belong to multiple overlapping communities and deviate from every group's central tendency.

## Two different meanings of emotional norm

1. **Descriptive norms:** what is typically experienced, reported, or expressed in response to a kind of event, conditional on role and context. Distinguish *experience* from public expression and observers' beliefs about typical experiences.
2. **Injunctive norms:** what participants expect, approve, demand, or sanction others for experiencing or expressing, conditional on role and context. These may differ from the descriptive distribution and may themselves be perceived inaccurately.

Neither is identical to **researcher evaluation** of what an emotion should be under chosen evidence and ethical criteria. Descriptive prevalence is not moral correctness. Injunctive expectations are not necessarily fair, adaptive, or psychologically realizable. Do not let "emotional norm" become a synonym for either "universal emotion" or "optimal emotion."

Social norms may regulate events encountered, attention, interpretation, regulation, action selection, display, and self-reported states. Observed public displays may therefore misrepresent the distribution of internal states. For nonhuman groups, operationalize recurring interaction patterns and sanctions/cues without imposing human concepts of articulated moral duty.

## Minimal population-conditioned state model

For agent i in population/community g, use affect-relevant state z_{i,t} (not assumed fully observed), accessible cues o_{i,t}, social event context c_t, relevant relation and role r_{i,t}, and population environment N_{g,t}. A simple conditional transition *family* is

\[
z_{i,t+1}\sim T_{\theta_{\rm shared},\theta_g,\theta_i}\left(
\cdot\mid z_{i,t},c_t,o_{i,t},r_{i,t},N_{g,t},a_{-i,t}
\right),\quad
y_{i,t+1}\sim H_{g,i}(\cdot\mid z_{i,t+1}).
\]

Here N is a **measured or estimated set of population conditions**, not a magical scalar of social approval. In a more explicit instantiation, N consists of (a) conditional frequency of behaviors or expressions, (b) conditional beliefs about what is approved or sanctioned, (c) learned cue-to-social-meaning maps, and (d) relevant ecology/resource/relationship structures. They are not automatically independent, observed, or causally identifiable.

The common parameters \theta_shared and population-specific parameters \theta_g represent a nested hypothesis. A fully independent model for each population must be retained as a comparator. Because group variation is also individual variation, individual random effects \theta_i and overlapping affiliations must be admitted where warranted.

**Dynamic social environment:** Population norms may evolve from interactions, and those norms shape subsequent affect. In a later extension, estimate a reciprocal community update N_{g,t+1}\sim U(N_{g,t}, \{a_{i,t}, y_{i,t}\}_{i\in g}, \text{environment}), with observation and sampling bias modeled explicitly. **Do not assume** observed expressions are direct emotional ground truth.

## Endogenous norms and population feedback

**Norms are not merely static environmental parameters.** A possible social system begins with individual affective response rules and behavioral tendencies; repeated interactions produce recurring distributions of encounters, expressive behavior, affiliations, avoidance, cooperation or sanctions. Such patterns can feed back into future individual emotional transitions. This is a testable *micro-to-macro-to-micro* feedback loop, not a demonstrated mechanism or evidence that emotion is always the principal driver of social structure.

Separate **descriptive regularities** (what often happens) from **injunctive norms** (what is expected or sanctioned), and distinguish public expression from latent affect. Emergence of regular behavior does not itself prove the existence of shared expectations. The reference [affect-social-structure feedback](affect-social-structure-feedback.md) defines contrasting synthetic configurations with affect coupling removed, externally imposed norms, and genuinely updating norms. This comparison protects us from baking the desired emergence into the simulator.

## What could be universal? (Test, do not presume)

Candidate common *formal mechanisms* (not universal valence meanings):
- state persistence after a trigger;
- intensity or activation dependence on stimulus/relevance;
- generalization to related contexts;
- differential sensitivity to familiarity, affiliation or threat where operationally meaningful;
- interaction feedback (one agent's actions change another's social environment);
- social learning or calibration toward local recurring patterns.

Even these features need not exist in identical form or in every population. Similar outward behavior is not enough to claim homologous emotions or subjective experience.

## Identification and non-identification

Do not infer norm effects solely from observing that populations with different feelings have different norms: this is circular and confounded by ecology, selection, individual differences, and differences between expressed and felt states. Prefer independently measured norms, within-population changes in norms, natural experiments, randomized social-context cues where ethical, repeated social ties, and longitudinal observations. Avoid inferring causal influence from mere cross-cultural correlations.

Compare:
- M0: universal transition with raw event cue and individual baseline, no norm information;
- M1: common transition family with an independently measured population-conditioned cue/meaning map;
- M2: M1 plus population-specific response strengths/dynamics;
- M3: population-specific mechanisms without a shared transition kernel.

Test held-out individuals, events, time periods, relationships, subgroups, and populations. Evaluate predictions at multiple levels: population distributions, trajectory statistics, and individual forecast calibration. Complexity penalties and recovery tests are necessary; held-out fit alone cannot determine whether parameters are causally meaningful.

**Discriminating experiment:** Hold the observable event fixed while independently varying information about the social norm, identity/affiliation, and perceived approval/sanction, with social meaning and sensory features controlled where possible. Test whether changes in *experienced affect* (not just expression or stated appraisal) follow the norm condition and how effects vary with baseline and population. Uncertainty, demand characteristics, and social desirability remain alternative explanations.

**Negative results:** If norms add no incremental predictive value once ecology, personal history, and context are measured, simplify. If response mechanisms differ among populations even after contextual mappings, allow true population-specific dynamics. Both outcomes are informative.

## Prior work / scope boundaries

- Vishkin (2023), [*Emotion Norms Are Unique*](https://pmc.ncbi.nlm.nih.gov/articles/PMC10514023/), distinguishes descriptive and injunctive emotion norms and discusses experiential and expressive dimensions.
- Mesquita, Boiger & De Leersnyder (2018), [*The cultural construction of emotions*](https://pubmed.ncbi.nlm.nih.gov/29506799/), reviews cultural variation in emotional practices and relational dynamics.
- De Leersnyder, Boiger & Mesquita (2013), [*Cultural regulation of emotion*](https://pmc.ncbi.nlm.nih.gov/articles/PMC3569661/), discusses individual, relational, and structural pathways affecting elicitation.
- Anderson & Adolphs (2014), [*A Framework for Studying Emotions Across Phylogeny*](https://pmc.ncbi.nlm.nih.gov/articles/PMC4098837/), proposes operational cross-species features such as persistence and scalability.
- [*Norms for experiencing emotions in different cultures*](https://pubmed.ncbi.nlm.nih.gov/11708563/), reports both shared and culture-specific patterns; not a demonstration that emotional contents are universal.

## First executed synthetic checkpoint

The [executed norm-conditioned synthetic experiment](../experiments/norms-identification-results.md) shows a fixed transition kernel recovering its known coefficients across two deliberately norm-divergent populations, while failing on a third population with genuinely different invented dynamics. This is an implementation/methodology result only, not empirical evidence of universal human or animal emotional norms. Source: [norms_identification.py](../experiments/norms_identification.py).

## Research priority

Next synthetic benchmark must **factorially manipulate contextual cue meaning, descriptive/injunctive group norms, and affective transition parameters**. Ask which mechanisms survive context mapping, and how much empirical evidence is required to identify a common kernel. Prefer this test to further elaboration of private belief reconstruction. Existing first simulator remains a narrow engineering check, not the main substantive theory.
