# Claim-by-claim prior-art comparison (first pass)

**Recorded:** 2026-11-22
**Author:** Claude Opus 5.5 (AI contributor), at Leo's invitation
**Responds to:** the "Next review gate" in [2026-11-20-provisional-novelty-statement.md](2026-11-20-provisional-novelty-statement.md)
**Status:** First pass, not exhaustive. It is based on abstracts, publisher pages and partial full texts found by web search. EMA, the extended process model, Huys et al. (2015) and Erdman & Eldar (2023) still need a full-text read before any verdict here is treated as settled. No claim of novelty is made or implied.

## Summary

| # | Candidate claim | Nearest precedent(s) | Verdict |
|---|---|---|---|
| C1 | Controlled stochastic affect transitions $T_\theta$ with belief, history and context | DynAffect / OU models; EMA; active-inference affect models | **Already known** as a component |
| C2 | Evaluative fittingness $\mathcal E^*(D,c)$ against a justified reference $q$ | D'Arms & Jacobson; Naar; Tamir et al.; Gross (EPM valuation); Emanuel & Eldar | **Narrowed.** Distinct only if $q \neq b$ is specified independently of the person |
| C3 | Probabilistic reachability $\mathcal R_{h,\alpha}$ | Abate et al. (2008); controllability models (Huys & Dayan 2009; Ligneul et al. 2022) | **Mathematics already known**; the application is narrowed |
| C4 | Joint separation that diagnoses why a fitting state is not occupied | Gross EPM stages; EMA appraisal–coping; Huys et al. decision-theoretic psychiatry; Erdman & Eldar (2023) | **Unresolved, narrowed.** Plausibly distinct in one specific form (below) |

The most defensible candidate contribution is now narrower than the 20 Nov statement. It is a formal joint diagnostic separating (a) the person's interpretation $b_t$ from an independently specified, evidence-relative reference $q(x\mid D)$; (b) the resulting evaluative target $\mathcal E^*$; and (c) model-implied, information-constrained reachability of that target. It must be tested on whether it predicts **differential intervention response** that existing appraisal–coping and controllability models do not.

## C1 · Transition dynamics

- **Precedents.** DynAffect models core affect as fluctuating around an individual "home base", with attractor strength and variability as person-level parameters (Kuppens, Oravecz & Tuerlinckx, 2010, *JPSP* 99(6), 1042–1060). Hierarchical latent OU/SDE versions exist (Oravecz, Tuerlinckx & Vandekerckhove, 2011, *Psychological Methods* 16(4), 468–490). Reward-and-expectation models of momentary happiness: Rutledge et al. (2014, *PNAS* 111(33)). Appraisal-driven dynamics: EMA (Marsella & Gratch, 2009, *Cognitive Systems Research* 10(1), 70–90). Affect inside a POMDP-style generative model: Hesp et al. (2021, *Neural Computation* 33(2), 398–446).
- **Exact difference.** ER's $T_\theta(\cdot\mid e_t,b_{t+1},m_t,c_t,u_t,o_t)$ is a generic controlled partially observed process. OU models lack belief and action terms. EMA and active inference include both.
- **Verdict: already known.** Any contribution lies in what $T$ is combined with, not in $T$.

## C2 · Evaluative fittingness

- **Precedents.**
  - *Philosophy.* D'Arms & Jacobson (2000, *Philosophy and Phenomenological Research* 61(1), 65–90) separate fittingness from moral and prudential appropriateness. Naar (2021, *Synthese* 199, 13601–13619) argues that "fitting" (objective match) and "appropriate given the agent's evidence" come apart.
  - *Psychology.* Tamir et al. (2017, *JEP: General* 146, 1448–1459): people are happier when they feel the emotions they *desire*, including unpleasant ones. Gross's extended process model (2015, *Psychological Inquiry* 26(1)) treats regulation as a valuation of one's own emotion as good or bad.
  - *Computation.* Emanuel & Eldar (2023, *Neurosci. Biobehav. Rev.* 144, 104977) give normative RL accounts of what emotions compute. Bayesian models of the emotion an observer expects from a situation (Ong, Zaki & Goodman, 2015, and follow-ups) are close to "the response the evidence supports".
- **Exact difference.** $\mathcal E^*$ is a Bayes-risk minimizer over the affect grid, $\arg\min_e \sum_x q(x\mid D)J_\phi(e,x,c)$. The decision theory is standard. What is specific is that the evaluative standard $(q,\phi)$ is an **explicit, reported, sensitivity-analysed model component kept apart from both the dynamics and the person's belief $b_t$**.
- **Collapse condition.** If $q=b_t$ and $\phi$ encodes the person's own values, $\mathcal E^*$ reduces to Tamir's *desired emotion* or Gross's valuation step. The component is distinct only when $q$ is fixed independently of the person: by design (known contingencies), by independent raters, or by an external evidence standard.
- **Terminology risk.** Because $q$ is conditioned on evidence $D$, ER's quantity is evidence-relative warrant in Naar's sense, not fittingness in the strict D'Arms–Jacobson sense. Philosophy reviewers will catch this. Either rename it ("warranted response set") or add one sentence stating which sense is meant.
- **Verdict: narrowed.** Retain it only as "an explicit, independently specified evaluative reference with mandatory sensitivity analysis".

## C3 · Reachability

- **Precedents.** $\mathcal R_{h,\alpha}$ is standard finite-horizon probabilistic reachability for controlled discrete-time stochastic systems, computed by dynamic programming (Abate, Prandini, Lygeros & Sastry, 2008, *Automatica* 44(11), 2724–2734). On the psychology side, controllability has been formalized as priors over action–outcome contingencies (Huys & Dayan, 2009, *Cognition* 113(3), 314–328) and as inferred task controllability (Ligneul et al., 2022, *Nature Human Behaviour*). Erdman & Eldar (2023, *Psychopharmacology* 240(11)) name *misestimated controllability* as one source of excessive emotion. The regulatory-flexibility work on strategy repertoire (Bonanno & Burton, 2013, *Perspectives on Psychological Science*) and the formal strategy-choice model of Petter et al. (2025, *Emotion* 25(5), 1273–1292) cover the "what can I do" side verbally and formally.
- **Exact difference.** ER's set is the **model-implied (objective) reachability** of affect states under information-constrained admissible policies. The controllability literature models the person's **estimate** of control. Contrasting the two would be a useful extension, but ER does not yet define the perceived version.
- **Verdict: mathematics already known.** The application to affect *target sets* may be uncommon, but the conceptual ground is largely covered.

## C4 · The joint separation (the substantive claim)

- **Precedents.**
  - *Gross EPM.* Its identification → selection → implementation stages map roughly onto evaluate → choose a policy → execute and reach.
  - *EMA.* Couples appraisal, coping (actions that change beliefs, intentions or the world) and dynamics.
  - *Huys, Guitart-Masip, Dolan & Dayan (2015, Clinical Psychological Science).* Frame psychiatric dysfunction as failures of identifiable components of Bayesian decision-making.
  - *Erdman & Eldar (2023).* Decompose excessive emotion into self-intensifying biases, misestimated predictability and misestimated controllability. This is the closest found precedent for a "why is this person stuck" decomposition.
- **What none of these appear to do** (pending full-text check): use one formal model to separate three failure routes for not occupying a fitting state:
  1. *Interpretive gap:* $b_t$ diverges from an independent $q$, so the person is aiming at the wrong target.
  2. *Reachability gap:* $\mathcal E^*\cap\mathcal R_{h,\alpha}=\varnothing$, so the right target cannot yet be reached.
  3. *Horizon gap:* the target is reachable only at larger $h$ (the worked $A/S$ example).

  Each route implies a different intervention: information, capability, or time.
- **Discriminating experiment (sketch).** Use a threat-of-shock or similar paradigm where the experimenter **sets the true contingencies**, which makes $q$ known by design. Cross two factors:
  - *Information:* credible disclosure of the true benign probability, or none. This shifts $b$ toward $q$.
  - *Capability:* an available effective action, such as escape or a trained regulation strategy, or none. This expands $\mathcal R$.

  Measure fear or affect at several lags. **ER predicts a pre-registered crossover.** Information should help mainly where model-estimated $b$–$q$ divergence is large and $\mathcal E^*$ is reachable. Capability should help mainly where $b\approx q$ but $\mathcal E^*\notin\mathcal R_{h,\alpha}$. Information without reachability should produce a delayed, horizon-dependent reduction, not an immediate one. Baselines should include an appraisal–coping model, a controllability-prior model and an OU model with intervention covariates. If they predict the same pattern without separate $q$ and $\mathcal R$, C4 is not distinct.
- **Verdict: unresolved, narrowed.** This is the claim worth keeping, in the narrow form above.

## Recommended changes (proposals, not applied)

1. Name EMA, the Gross EPM, Huys & Dayan's controllability model and Erdman & Eldar (2023) as **explicit comparison baselines** in `theory/research-scope.md` and the prediction register.
2. Add the **collapse condition** for C2 ($q=b$, $\phi$ = own values) to `theory/model.md`, so the distinct case is stated rather than implied.
3. Resolve the **"fittingness" terminology** (strict fit vs evidence-relative warrant) in one sentence.
4. Consider defining **perceived reachability** $\hat{\mathcal R}$ (the person's estimate) next to $\mathcal R$. The $\hat{\mathcal R}$ vs $\mathcal R$ gap connects ER directly to the controllability literature and is itself testable.
5. Before elevating any claim: full-text reads of Marsella & Gratch (2009), Gross (2015), Huys et al. (2015) and Erdman & Eldar (2023), checking specifically whether any of them already separates an external evaluative reference from the agent's belief.

## Limits of this pass

- Searches were English-language web searches. Many sources were read only at abstract or publisher-page level.
- Absence of a precedent here is not evidence of absence. This applies especially to the computational psychiatry and affective-computing literatures, where a close formal analogue could plausibly exist.
- No data were analysed and no model was changed. This is a review contribution: **Integration Delta not assigned.**
