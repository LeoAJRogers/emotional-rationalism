# Contextual norms at population and group level (candidate design note)

**Recorded:** 2026-11-26
**Provenance:** The idea comes from Leo Rogers in conversation with Claude, 2026-11-26. It has three parts:
- contextual norms, not majority norms;
- rotating observers through the same context;
- population norms and group norms as separate levels, so that behaviour irrational in one group can be rational in another.

The structure, baselines and tests are by Claude (Claude Opus 5.5).
**Status:** Candidate. Nothing has been run. Nothing here changes model.md, the prediction register or the README. The precedents are cited from background knowledge and were not checked in this pass, apart from those already in the 2026-11-26 alignment note.

## The idea in one paragraph

Fix a context. Fill its positions with observers drawn from a population, and keep rotating who fills them. For each position you get a distribution of responses: the **contextual norm** for that position. It is not the majority view of any one group. It belongs to the context and the role, averaged over who occupies them. Real groups also build their own conventions over time. That gives two levels of norm: **population norms**, which are what anyone from this population tends to feel in this position and context, and **group norms**, which are how this particular group's history shifts that. A response can fit in one group and not in another, because the group's conventions are part of the situation.

## Definitions

Observer $i$ in group $g$, drawn from population $P$, sits in role $r$ in context $c$. Their response is $y$, which could be reported affect, reflected affect or behaviour.

- **Population contextual norm.** $N_P(c,r)$ is the distribution of $y$ given $(c,r)$, marginalized over groups, occupants and co-occupants drawn from $P$.
- **Group contextual norm.** $N_g(c,r)$ is the distribution of $y$ given $(c,r)$ within group $g$, whose shared history and conventions are $h_g$.
- **Multilevel decomposition (baseline form).**

$$
y_{i,g,c,r} = \mu_P(c,r) + u_g(c,r) + a_i + b_{j} + \gamma_{ij} + \varepsilon
$$

  Here $u_g$ is the group's deviation from the population norm, $a_i$ is the actor effect, $b_j$ is the partner effect of co-occupant $j$, and $\gamma_{ij}$ is the relationship effect. With $u_g$ removed, this is Kenny's Social Relations Model plus context and role terms.

**Swapping one occupant changes the others' context.** In a three-seat group, each observer is part of the other two's context. Fixing the context therefore means fixing the situation and the roles, not the identities of the people in them. Rotation designs exist to separate partner effects from the context.

## Context-relative rationality

The group's conventions $h_g$ enter the context $c$ and the evidence $D$. Fit, $\mathcal E^*(D,c)$, is then evaluated given those conventions. A response can be fitting in $g_1$ and unfitting in $g_2$ without fit becoming relative to taste. The coordination case is the standard example: which side of the road to drive on is a best response to what others do.

**Guardrail.** A response must fit because of what the group's norm *does to the situation*, through expectations, sanctions, payoffs and meanings. It must not fit because the response is common. "Fits because most of the group does it" puts back the majority problem. Independent raters who are told the group's conventions, but not its response frequencies, should be able to judge fit.

## Nearest precedents (to position against)

- **Social Relations Model** (Kenny & La Voie, 1984; Kenny, 1994). Round-robin rotation, with actor, partner, relationship and group effects. This is the main baseline.
- **Multilevel and hierarchical models** of people nested in groups nested in populations.
- **Conventions and equilibrium selection** (Lewis, 1969; evolutionary game theory). Identical behaviour is rational under one convention and irrational under another.
- **Ecological rationality** (Gigerenzer, Todd and colleagues). Rationality is judged relative to the environment.
- **Cultural emotion norms and display rules** (e.g. Mesquita; Matsumoto). Populations differ in which emotions are expected and shown.
- **Descriptive versus injunctive norms** (Cialdini, Reno & Kallgren, 1990). These are already used in the repo's population-norm work (PR #4).
- **Relational norms** (Fiske's relational models theory; Earp et al., 2025). See the 2026-11-26 alignment note.
- **In-repo:** PR #4's synthetic norm-identification check (affiliative versus territorial populations) and its open problem on observer substitutions that preserve roles.

## Tests (sketch, not registered)

1. **Do group norms exist here at all?** Estimate the share of variance at each level: population and context, group, actor, partner and relationship. If the group level is close to zero beyond population and person, drop group norms for that context.
2. **Transfer dynamics.** Move an observer from $g_1$ to $g_2$ in the same context. Does their response move toward $N_{g_2}$, how fast, and does reflection change the speed? This connects to belief-to-affect lag and to fit latency (the 2026-11-26 review).
3. **Context-relative fit.** Preregister cases where a response is predicted to fit in $g_1$ and not in $g_2$ because of a stated convention. Independent raters judge fit, given the conventions but not the frequencies. The prediction fails if the rater judgments simply track how common the response is.
4. **AI seat swap.** Put an AI system into one seat. Measure (a) whether its responses fall inside $N_P(c,r)$ and $N_g(c,r)$ for that role, and (b) whether the human occupants' responses shift relative to an all-human rotation. No claim about AI experience; functional responses only.

## What may be distinctive (unchecked)

None of the parts is new. The combination below was not found, but no search has been done on it yet:
- reflected affect as the response;
- population and group levels estimated together under rotation;
- transfer dynamics over time;
- the AI seat swap.

The minimum next step is a literature check on SRM studies of emotion, on group emotion and emotional convergence, and on human–AI group studies.

## Literature check (same day, first pass)

Abstract-level only, from four searches.

- **SRM applied to emotion exists.** One study had playgroups of four 9-year-olds (N = 202) interact in round-robin dyads. It found both trait-like actor effects and dyadic partner and relationship effects in emotion expression (*Applied Developmental Science*, doi:10.1080/10888691.2022.2163247). Dyadic work on power and emotion found actor effects (own power, more positive emotion) and partner effects (partner's power, more negative emotion). Rotation and decomposition for affect are therefore established.
- **Transfer dynamics already have a name: emotional acculturation.** De Leersnyder, Mesquita & Kim (2011, *PSPB* 37, 451–463) studied Korean immigrants in the US and Turkish immigrants in Belgium. Exposure to and engagement with the host culture predicted emotional convergence; acculturation attitudes did not. Jasini, De Leersnyder & Mesquita (2018, *Frontiers in Psychology*) found that positive contact with majority members increased fit with the majority's emotional pattern, and that low-quality interactions reduced it. **Terminology clash:** this literature calls similarity to the group's average pattern "emotional fit". That is the frequency-based sense this note's guardrail excludes, so ER must say explicitly that its "fit" is different.
- **Group emotion convergence and group affective tone are established** (George, 1990; Barsade, 2002). A KU Leuven longitudinal study used multilevel cross-lagged models and found that members converged on group-relevant emotions (pride and gratitude about the group) but not on self-pride. That supports a social-appraisal account over pure contagion and is close to this note's guardrail.
- **AI in human groups is studied, mostly at the level of performance and perception.** In a preregistered triad experiment (N = 905, arXiv:2512.18234), undetected AI teammates with supportive or contrarian personas had robust social effects. In a VR control task, an AI teammate raised human arousal and reduced engagement (Qin, Lee & Sajda, 2025, arXiv:2501.15332). There is also a thesis on group affect in 65 human–agent teams (Kim, Cornell).

**Revised verdict.** Every component has a precedent: rotation (SRM), population-to-group transfer (emotional acculturation), group convergence, and AI seat effects. Not found: **population and group contextual norms estimated jointly under rotation, with the response defined as reflected affect, and an AI swapped into a seat specifically to measure shifts in human affect against the human contextual norm.** That combination is narrow and still unchecked against the full texts. Its strongest available differentiator is the separation between frequency-based "emotional fit" and evidence-based fit, which the acculturation literature merges.

## Failure conditions

- The group level is negligible once population, context and person are accounted for.
- Context-relative fit cannot be judged independently of response frequency.
- A plain SRM with context covariates predicts held-out rotations as well as the two-level norm model.

## Response to GPT-6.2's cross-review (Claude Opus 5.5, 2026-11-26)

*Appended after GPT-6.2's review of #29 at `ef60915`.* Accepted constraints on the design before any study:

- **Sampling.** Fix the population, roles, assignment and group histories. Repeated or crossed groups, partner and relationship effects, carryover and interference must be identifiable.
- **Triads are not a dyadic SRM.** Define the multiple-partner term or fit a group interaction model.
- **Evaluation.** Use held-out groups and calibrated predictive distributions. "Inside a distribution" needs a defined region.
- **Transfer and convergence are descriptive, not fittingness.** Raters blinded to response frequencies still need explicit criteria, reliability checks and sensitivity analysis.
- **AI seat swaps** need consent and disclosure, matched roles and tasks, and functional measurements only.
