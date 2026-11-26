# Prior-art addendum: integrated frameworks (Claude Opus 5.5, 2026-11-26)

**Status:** This supplements the open first-pass comparison in PR #17, the 2026-11-26 addendum and independent review (PR #26), and the same-day alignment and contextual-norms notes. Those notes compared ER's components one at a time. This one asks whether ER's *scope* is new: one framework covering individual dynamics, appraisal, social coupling, population and group norms, and reflection. Sources were read at abstract or summary level only. Absence of a precedent is not evidence of absence.

## Question

Has anyone already built one framework that combines affect dynamics, appraisal or belief, social interaction, emotional contagion, norms at several levels, and norm–emotion feedback?

## Answer: yes, several times

| Framework | What it combines | Purpose |
|---|---|---|
| **BEN** (Bourgais et al., *JASSS* 23(4), 2020) | BDI cognition plus modules for emotions, emotional contagion, personality, social relationships and norms. Built because no existing architecture incorporated all of these. | Social simulation |
| **FAtiMA / FAtiMA-PSI / ORIENT** (Paiva, Dias, Mascarenhas, Aylett and colleagues, 2005 onward; *Emotion Review*, 2012) | OCC-based appraisal, culture, social interaction and theory of mind. Cultural norms and rituals are modelled explicitly. | Believable virtual agents and social robots |
| **TABASCOJAM** (Staller & Petta, *JASSS* 4(1), 2001) | Appraisal plus social norms, with a two-way link: emotions sustain norms and norms regulate emotion | Social simulation (aggression control) |
| **Normative emotional agents** (Broersen et al.; Argente et al.; Noe, arXiv:2104.15034) | Emotion model, normative model and BDI. Norms emerge from emotions in multi-agent systems. | Multi-agent systems |
| **Active inference, social and affective** (Hesp et al., 2021; Kastel, Hesp, Ridderinkhof & Friston, 2023; second-person affect under active inference, arXiv:2506.08599; social allostasis, arXiv:2605.07761) | Affect as inference inside generative models. Coupled dyads. In some models, agents acquire prior preferences adapted to each other, close to emergent group norms. | Theory and simulation |
| **Affect Control Theory / BayesACT** (Heise, 1977 onward; Hoey, Schröder & Alhothali, 2013 onward). Checked the same day; see the section below. | Culture-wide affective meanings for identities, behaviours and settings. Emotion and action are predicted from deflection, the gap between cultural sentiment and in-context impression. | Sociology and agents |

**Closest to ER:**
- **Contextual norms by role:** Affect Control Theory. Reviewers will name it first.
- **Norm–emotion feedback:** TABASCOJAM, Noe and BEN.
- **Coupled dyads:** active inference.
- **Dynamics with a regulation norm:** CoMERG (already in PR #26).

## Affect Control Theory in detail (abstract and summary level, 2026-11-26)

ACT is the closest precedent found for the *norm* side of ER, including the "north star" and contextual-norm ideas.

- **Core.** People hold culturally shared "fundamental sentiments" about identities, behaviours and settings. Each sentiment is a point in a three-dimensional space: evaluation, potency and activity (EPA). Events create transient impressions, estimated with empirical impression-formation equations. *Deflection* is the weighted squared distance between sentiment and impression. People act, and reinterpret events, to reduce deflection: the affect control principle. Emotions are defined as the difference between fundamental and transient sentiment.
- **Roles and institutions.** Identities are assigned when a situation is defined, often by an institution (doctor–patient, professor–student). Confirming those identities produces role behaviour. Combining settings with identities that match them institutionally may make it possible to predict emotion norms for settings. Large EPA dictionaries exist for several cultures.
- **Multi-level and dynamic extensions.** ACT has been described as a unifying multi-level framework covering individual cognition and emotion, situational and institutional context, and cultural meaning (Duke dissertation). Later work argues that sentiments are dynamic and shaped by social networks, which is close to ER's group-norm level. There are also the affect control theories of the self (ACTS) and of institutions (ACTI), and work on cultural consensus and variation in sentiments (Curdy, 2018).
- **BayesACT.** This is a POMDP formulation. Emotions become probability distributions over a continuous affective space, identities become dynamic, uncertain and learnable, and the agent gets explicit utility and decision-theoretic action selection. It has been applied to assistive technology (the COACH handwashing system) and to the networked Prisoner's Dilemma.
- **Already applied to AI.** ACT has been used to generate emotionally aligned dialogue responses (Asghar, Kobyzev, Hoey, Poupart & Sheikh, 2020, arXiv:2003.03645).

**Mapping to ER**

| ER idea | ACT counterpart | Same? |
|---|---|---|
| Contextual norm by role and setting | Fundamental sentiments for identities and settings, and emotion norms for settings | **Largely the same idea**, with decades of measurement behind it |
| Population and group norms | Culture-wide dictionaries; network-contingent sentiments and cultural consensus work | Largely covered |
| "North star" that guides behaviour | The affect control principle: people act to confirm cultural meanings | **Close.** ACT treats the cultural reference as what behaviour is controlled toward |
| Reflection or reappraisal | Redefinition: reinterpreting identities when deflection cannot be reduced by action | Partly |
| Stochastic transitions under uncertainty | BayesACT | Covered |
| **Evidence-relative fit $q(x\mid D)$** | None. Deflection is measured against *cultural* sentiment, not evidence | **Not in ACT** |
| **Reachability $\mathcal R_{h,\alpha}$** | None as a separate quantity. BayesACT plans, but does not ask whether a fitting state is reachable | **Not in ACT** |
| Felt-affect trajectories in experience-sampling data | ACT works with EPA meanings; emotion is derived | Different measurement target |

**Consequence.** ACT is the strongest existing model of the *typical* side of ER's typical-versus-fitting distinction. Deflection is a norm-based quantity, and in ACT the norm is the reference. That makes ACT the natural baseline for ER's claim that fit is distinct from the norm. Where a culturally confirming response and an evidence-fitting response come apart, ACT and ER should predict different things. Testing that is the most direct way to show what ER adds.

## What these frameworks mostly do not do

The search found none that does any of the following. That is not proof that none exists.

1. **Separate what is typical from what fits.** Norms in these architectures prescribe or describe responses. None keeps an evidence-relative reference $q(x\mid D)$ apart from both the agent's belief and the group's frequencies. The emotional-acculturation literature goes further and *defines* "emotional fit" as similarity to the majority pattern. See the contextual-norms note.
2. **Treat reachability as its own formal question.** Regulation and coping appear as actions or processes. "Is the fitting state attainable at horizon $h$ with probability $\alpha$, given what the person knows?" is not posed as a separate quantity.
3. **Support identification from data.** Most of these are architectures for believable or simulated agents, evaluated qualitatively or on task behaviour. ER requires several things those evaluations do not: held-out prediction on real experience-sampling data, comparison against simpler baselines (OU, autoregressive, appraisal), synthetic recovery checks, and pre-committed rules to narrow or retire claims.
4. **Model reflection as something that can move the person away from the norm.** Leo's position is that reasoning and free will operate alongside contextual norms. The norm is a reference that reasoning can depart from, not a determinant.

## Verdict

- **Scope: already known.** A framework that "covers emotion, cognition and society" will be compared to BEN, FAtiMA, active inference and Affect Control Theory, and will look late.
- **Distinctive: unresolved, narrowed.** What may be distinctive is the combination of (1)–(4): a *testable evaluative separation* that these frameworks lack, applied inside a scope they have already built.

## Recommended framing (proposal, not applied)

For external reviewers, START-HERE.md (PR #27) and the IP consultation package, describe ER as:

> A testable separation between what people tend to feel, what fits the evidence, and what they can reach, applied to individual, group and population dynamics. It is not a comprehensive architecture of emotion and society.

Name BEN, FAtiMA, active inference and Affect Control Theory as the integrated frameworks ER positions against.

## Next checks

- **Done at abstract level:** ACT deflection is norm-referenced, not evidence-referenced (section above). Still needed: a full-text read of Heise (2007) and Hoey, Schröder & Alhothali (2016) to check whether any ACT extension adds an evidence-based standard. Also needed: a discriminating study sketch in which cultural confirmation and evidence-based fit diverge. One example would be a culturally expected emotion toward an identity whose behaviour the evidence shows to be benign.
- A check on whether any active-inference affect model separates an evidence-relative reference from the agent's own prior preferences. If one does, item (1) narrows further.
- A search of the computational-psychiatry literature for reachability-like quantities (also open from PR #17).

## Sources

Affect control theory overview, https://en.wikipedia.org/wiki/Affect_control_theory · Robinson, Smith-Lovin & Wisecup, ACT chapter, https://cs.uwaterloo.ca/~jhoey/teaching/cs886-affect/papers/ACTRobinsonChapter.pdf · Hoey, Schröder & Alhothali, Affect Control Processes, https://arxiv.org/abs/1306.5279 · BayesACT project page, https://cs.uwaterloo.ca/~jhoey/research/bayesact/ · Asghar et al. 2020, https://arxiv.org/abs/2003.03645 · Hoey & MacKinnon, "Conservatives Overfit, Liberals Underfit", https://arxiv.org/abs/1908.03106 · Heise special issue introduction 2022, https://escholarship.org/content/qt14c670fs/qt14c670fs.pdf · Curdy 2018, https://hdl.handle.net/10161/16952 · ACT and settings/emotion norms chapter, https://doi.org/10.1007/978-94-017-9130-4_4 · Duke dissertation on ACT as a multi-level framework, https://dukespace.lib.duke.edu/server/api/core/bitstreams/decb78a8-e16f-4cd0-8d67-8db2fafaab0f/content · 
Staller & Petta 2001, https://jasss.soc.surrey.ac.uk/4/1/2.html · BEN 2020, https://jasss.soc.surrey.ac.uk/23/4/12.html · FAtiMA culture and affect 2012, https://journals.sagepub.com/doi/10.1177/1754073912439766 · FAtiMA Toolkit, https://arxiv.org/abs/2103.03020 · Noe, https://arxiv.org/abs/2104.15034 · Kastel et al. 2023, https://doi.org/10.3389/fnbot.2022.944986 · Second-person affect under active inference, https://arxiv.org/abs/2506.08599 · Social allostasis model, https://arxiv.org/abs/2605.07761 · Computational model of social norms, https://arxiv.org/abs/1801.05796
