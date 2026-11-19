# Emotional Rationalism: integrated architecture (candidate v0.2)

**Date:** 2026-11-19  
**Status:** Proposed framework integration, not an empirical result. This supplements—not silently replaces—the finite-state v0.1 model in [model.md](model.md).  
**Scope:** Human social-affective dynamics first. Extend to other populations only after specifying observation and state semantics.

## 0. Research objective and commitments (F0)

Investigate how affective states and trajectories are distributed, selected for consideration, evaluated, and changed as social context, interpretation, history, and interactions evolve. In particular, investigate *changes in feeling*, not just verbal judgments, action choice, or optimization scores. Whether any specific latent computational state corresponds to felt experience must be independently established.

Preserve **five distinct questions**:

1. **Description:** Given an individual and context, which affective trajectories are likely? This is an empirical/statistical question and can faithfully capture biases.
2. **Inference:** What does an individual believe, perceive, or appraise, and with what accuracy or uncertainty?
3. **Evaluation:** Which features of a response fit the available evidence, values, roles, and legitimate expectations **under explicitly specified criteria**? This is observer- and criterion-relative; no unique universal 'right emotion' is assumed.
4. **Reachability:** Which responses can an individual actually attain, at what horizon and probability, under feasible information and actions?
5. **Intervention/agency:** What decisions, communications, and regulatory attempts are available, and what do they change? Selection of a mathematical profile is not induction of a felt state.

Distinguish **definition / assumption / mathematical consequence / testable prediction / empirical finding / speculative application** in every project artifact. Descriptive typicality does not imply rationality, ethical propriety, or desirable behavior. Nor does a rationally assessed response guarantee control over affect.

## 1. Foundational status registry

- **F0 — methodological constraints:** separations above; explicit perspective and uncertainty; honest provenance; falsifiable comparisons; no fixed taxonomy or universal optimum asserted.
- **F1 — mathematical scaffolding:** indexed agents, latent states, a shared world, differing observations, stochastic transitions, time/history, measurement, interactions, and the possibility of multiple simultaneous emotions. A finite state space is a computational convenience, not a metaphysical claim.
- **F2 — candidate mechanisms:** appraisal and belief-updating maps; bodily/attentional/memory covariates; interpersonal/relational state; action and regulation policies; emotion-to-cognition feedback; person-specific persistence and accessibility. Include only when needed for the specific study.
- **F3 — empirical structural hypotheses:** low effective dimension; separable interpretation and affect-transition operators; differing appraisal/affect timescales; stability across information regimes; person-to-person parameter sharing; independent pathways for different emotional components.
- **F4 — contingent scope expansion:** configurable population-specific observation/state/transition models for animals, human cultures, AI behavior, or unfamiliar agents. Similar external function does not prove similar phenomenology.
- **F5 — applications:** counterfactual emotional perspectives, interaction support, or suggested plausible states for multiple participants. Not a measure of objective emotional correctness; avoid presenting it as mind-reading.

The ordering is about dependence, not prestige. An F3 proposition may graduate if supported; F2 mechanisms should remain replaceable.

## 2. Minimal multi-agent stochastic process (F1)

Let agents be indexed by i, with a shared evolving world state w_t, an agent-specific latent non-affective state \xi_{i,t}, and an affect state e_{i,t}. A state can be represented by a vector, a structured set, or a probability distribution, according to measurement needs. The coordinates of a vector are **not fundamental** and may not be identifiable; subject- and relation-directed affect should retain their targets/roles.

Use the general factorization below as a *research scaffold*, not a claim that this causal graph has been established:

\[
a_{i,t}\sim\pi_i(\cdot\mid e_{i,t},\xi_{i,t},o_{i,\le t}),\qquad
w_{t+1}\sim K(\cdot\mid w_t,a_{1:n,t}),
\]
\[
o_{i,t+1}\sim O_i(\cdot\mid w_{t+1},a_{1:n,t}),\qquad
\xi_{i,t+1}\sim B_i(\cdot\mid \xi_{i,t},e_{i,t},o_{i,t+1},a_{i,t}),
\]
\[
e_{i,t+1}\sim T_i(\cdot\mid e_{i,t},\xi_{i,t+1},w^{\rm accessible}_{i,t+1},a_{i,t}),\qquad
y_{i,t+1}\sim H_i(\cdot\mid e_{i,t+1},\xi_{i,t+1}).
\]

Here y denotes measured self-reports, observed behavior, expression, or physiology, and H is an explicit noisy observation model. The term w^{accessible} means only what is represented to the agent by the assumed information condition; actual hidden facts must not leak into a limited-information model. In observational human studies, the stated factorization and edges are candidate mechanisms, not automatically identified causal relations.

The shared world transition K makes interaction reciprocal: one person's actions can change another's observations and subsequent state. The latent state \xi_i may be expanded to beliefs about others, goals/values, memory, physiology, baseline, relationships, attention, and regulation capacity **only when operationalized**. The affect transition T_i may depend on cognition, and cognitive dynamics B_i may depend on prior affect: this bidirectionality is a candidate mechanism, not an established universal.

A joint model of all agents plus the shared world is appropriate when reciprocity matters. A single-agent special case remains valid for simpler experiments.

## 3. The interpretation/transition separation is a hypothesis (F2/F3)

A useful restricted model decomposes perceived social context from the transition operator:

\[
\hat c_{i,t} = G_i(o_{i,\le t},b_{i,t},m_{i,t};\psi_i),
\qquad
e_{i,t+1}\sim T_i(\cdot\mid e_{i,t},\hat c_{i,t},u_{i,t};\theta_i).
\]

This permits a controlled test of whether many apparently different responses result from different interpretations while a simpler T is shared. Do **not** assume this is the true decomposition: affect may change perception; uncertainty itself can be affectively salient; physiological factors or unmodeled histories can drive both; G and T may not be separately identifiable from reports alone.

At the start of a staged simulation, full information can force the relevant reconstruction by G to be accurate. It must not force identical values, relationships, affective baselines, or emotional responses across people. Full-information social conflicts can persist.

## 4. Three quantities retained from v0.1

**A. Descriptive dynamics.** Fit p_\theta(e_{t+1}\mid state, observations, context) and compare its calibration and held-out predictive adequacy to simpler baselines. An estimator trained on behavior will often learn patterned human biases and normative defects. Treat this as faithful *description*, not automatically as the best response.

**B. Fittingness/evaluation.** Keep an explicit evidential reference q(x\mid D) and declared criteria \phi, but frame any output as an *evaluated set or distribution*, not a universal prescription. For example:
\[
\bar J_{\phi,q}(e)=\mathbb E_{x\sim q}[J_\phi(e,x,c)],\qquad
\mathcal F_{\phi,q,\epsilon}=\{e:\bar J_{\phi,q}(e)\le \inf_z\bar J_{\phi,q}(z)+\epsilon\}.
\]
This generalizes the v0.1 minimizer set. Report the reference, weighting, allowed disagreement, sensitivity to q and \phi, and which aspects are being evaluated (factual appraisal, proportionality, ethics, present obligations, etc.). One emotion can be understandable given evidence available at the time while misrepresenting a newly known fact. A person may validly choose a boundary without forcing the corresponding feeling.

**C. Reachability.** Retain the finite-horizon probability concept from v0.1. For a **prespecified** target region A, define
\[
p_h^*(A\mid s)=\sup_{\pi\in\Pi_h}
P^\pi(e_{t+h}\in A\mid s).
\]
For a declared family of target regions \mathscr A, define
\[
\mathcal R^{\mathscr A}_{h,\alpha}(s)=
\{A\in\mathscr A:p_h^*(A\mid s)\ge\alpha\}.
\]
Restrict \mathscr A to meaningful prespecified candidates (otherwise the entire state space is trivially attainable). For fittingness, directly evaluate p_h^*(\mathcal F\mid s) if \mathcal F is a measurable region. Policies must use only accessible information and feasible actions. \mathcal F\cap\mathcal R may be empty at a given horizon. An unreachable evaluated response does not by itself imply deficient reasoning, and a reachable response is not necessarily justified.

**Keep a fourth separate object:** a *mathematical selector* S mapping a context/standpoint and stated constraints to a set or distribution of hypothetical emotional trajectories. It selects possibilities *for analysis*; it is not an emotion induction technique. A proposal to reweight trajectories based on a revised appraisal distribution is exploratory. If several appraisals change, test joint constraint satisfaction and order dependence rather than sequentially overwriting previous updates. Do not silently identify S with the descriptive p_\theta or with evaluated \mathcal F.

## 5. Social perspective and recursive representation (F2)

Track, when the study warrants it:

- what actually happened in the modeled world;
- what agent i observes;
- what agent i believes and appraises;
- what agent i believes agent j knows, wants, or feels;
- the agent's actual affect and its reported/observable indicators;
- explicit role, relationship, legitimate expectations, and action constraints.

Different perspectives are not merely errors around a privileged observer: agents can reasonably value the same facts differently, even with accurate beliefs. Recursive theory of mind has computational cost; start with first-order beliefs and only increase depth if predictions require it. We should test role- and relationship-preserving substitutions, not assume two arbitrarily substituted observers have identical dynamics.

## 6. Specific integrations from earlier discussions

1. **Parallel emotions and targets (F1 representation design):** anger, warmth, guilt, concern, etc. can coexist; labels like 'anger at Alex' and 'warmth for Alex' must not be collapsed into a single valence coordinate without a demonstrated sufficient-statistic argument.
2. **Attention/urgency versus emotion (F2 design):** the felt need to replay an event or act today is an outcome distinct from anger or affection, even if coupled to them. Model salience, attention, and action policy separately unless evidence supports merging.
3. **Intent and present obligation (F2):** learning that harm was deliberate can increase blame/anger while learning that a matter is closed decreases task urgency. The two changes may oppose one another rather than reflecting uniform 'distress'.
4. **Appraisal vs transition capacity (F0/F2):** knowing that an interpretation was mistaken may change a verbal assessment long before affect changes. Do not label this lag 'irrationality'; estimate persistence, time horizon, individual control pathways, and measurement artifacts.
5. **Emotion shaping subsequent reasoning (F2/F3):** attention, retrieval, interpretive search, or belief updating can be influenced by prior affect. Test against purely feed-forward alternatives.
6. **Autonomy and agency (F0/F2):** emotional reactions, actions, boundaries, and the legitimacy of others' expectations require different justifications. Regulation capacity and personal autonomy are constraints, not optimization failures.
7. **Trajectories and path dependence (F1/F3):** record state, transition, and trajectory separately; two paths with the same endpoint can differ in duration, recurrence, costs, and effects on relationships. A trajectory functional is a candidate evaluative extension, not a settled objective.
8. **Observer diversity (F4):** use a modular kernel with population-specific operators. Human data first; avoid assuming a human emotional taxonomy maps cleanly to animals or AI.
9. **Counterfactual perspectives (F5):** present a conditional range of possible interpretations and feelings, with calibration and disagreement visible. Never market a modeled suggestion as another person's hidden true experience.

## 7. Demotions, exclusions and corrections

- **Demote 'emotions must have few universal dimensions' to F3.** Test intrinsic/predictive dimension; beware coordinate transformations, weak observability, and dimension/rank confounds.
- **Demote 'separable G and T' to F3.** An elegant architecture is not identified by its notation. Compare with end-to-end and bidirectional alternatives.
- **Do not equate no deception with full information.** Honest people may lack information or make errors. These are separate controlled manipulations.
- **Do not treat any optimal emotional state as objective moral truth.** Evaluation is conditioned on evidence, criteria, standpoint, and the question asked; the emotional state need not be uniquely selected.
- **Do not assume reported judgment change is felt change.** Track repeated spontaneous response as well as explicit appraisal, action, memory, and behavior.
- **Do not collapse concern, warmth, anger, salience, urgency, cognition, and action into one scalar** merely to simplify fitting.
- **Do not reify illustrative linear interpolation, finite affect grids, exact numbers, or simulator policies** as discovered psychology.
- **Do not equate a statistically frequent response with a fitting response.** A learned descriptive model includes population habits, errors, and biases.
- **Do not infer consciousness from modeled AI behavior**, and do not presume philosophical premises are either proven or required for early operational work.
- **Do not remove historical proposals from the record.** Mark superseded, illustrative, or exploratory status and preserve attribution.

## 8. Practical staged identification program

See [progressive-identification.md](../experiments/progressive-identification.md) for the test ladder and failure criteria.

1. Start with synthetic full-information, nondeceptive agents; vary real conflicts, values, and relationships. Fix state representation and measurement; test recovery of known transition parameters and dimensions.
2. Add partial but honest observations and uncertainty; compare a shared T with a separate G against models requiring more state.
3. Add stable interpretation bias and confidence calibration errors; see whether extra latent dynamics are identifiable.
4. Add selective disclosure and intentional deception; test whether signaling, trust, and recursive beliefs explain new variance without new affect dimensions.
5. Only then apply human longitudinal evidence, with human self-reports and behavioral measures. Synthetic success proves recoverability under assumptions, not biological truth.
6. Revisit cross-population generality only after the human base can make distinguishable, calibrated predictions.

## 9. Immediate criteria for success

A proposed extra state/parameter should earn its place by at least one prespecified criterion: improved out-of-sample prediction/calibration, recoverability under controlled interventions, identifiable counterfactual predictions unavailable to the reduced model, or necessary semantic separation for the stated research question. Prefer simpler alternatives, ablations, held-out subjects/contexts, and negative findings. Check invariances only where transformations preserve relevant roles, evidence, and measurement meaning.

**Integration verdict:** Preserve v0.1's dynamics/evaluation/reachability split as a valuable subtheory; place it in a multi-agent partially observable dynamical scaffold; demote dimension and operator-separation claims; keep selection and speculative augmentation explicitly outside the validated core.
