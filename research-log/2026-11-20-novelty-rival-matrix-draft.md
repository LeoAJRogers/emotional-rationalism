# Novelty challenge: first-pass rival matrix (2026-11-20)

**GPT-6 working draft, not an exhaustive systematic review.** A distinctive formal decomposition does not by itself imply a novel mechanism or empirical success. Literature links below are starting comparators, not proof of priority.

| Candidate ER contribution | Nearest established families | What overlaps | What would genuinely discriminate? | Present evidence |
|---|---|---|---|---|
| Context/history-conditioned stochastic affect transitions | Dynamic appraisal/component process (Scherer); AR/state-space emotion dynamics | Context-dependent trajectories and inertia | Better calibrated forecasts or more parsimonious transferable state under matched observation model | R-003/R-004 show bounded history gain, not mechanism |
| Predictive state vs persistent latent state | State-space, measurement-error AR/ARMA; dynamic factor models | Observation noise and nonstationarity can mimic latent timescales | Recovery of latent structure with independent measurement anchors or strong cross-item temporal predictions | Synthetic gauge counterexample and R-004 caution |
| Evaluative fittingness conditional on evidence/values | Appraisal, rational emotion, decision-theoretic and normative affect accounts | Judgments of appropriateness and differing values | A well-defined, independently measurable evaluative criterion predicting disagreements or outcomes beyond appraisal baseline | Formal definition only; no human test |
| Policy/information/horizon-dependent reachability | Stochastic control, MDP/POMDP, emotion regulation | Feasible actions, targets and transition constraints | Jointly calibrated h-step and action-conditioned probabilities that outperform simpler regulation models | Toy derivation only |
| Belief update preceding affect transition | Appraisal and reappraisal experiments | Belief and affect may evolve at different rates | Prospective cue experiment showing incremental prediction beyond immediate appraisal and autoregression, with causal design | Proposed protocol only |
| Population social feedback generating norms | Social learning, evolutionary game theory, cultural dynamics, social-affective modeling | Emergent coordination, norms and reciprocal adaptation | Testable norm trajectories that arise from a parsimonious coupling law and beat explicit-norm rivals | Candidate architecture PR #4 only |
| Cross-population/substrate configurability | Hierarchical state-space, agent-based and multi-agent models | Population parameters and modular observations | Out-of-population transfer without ungrounded subjective equivalence | Architectural ambition only |

## Priority novelty test
The near-term **strongest falsifiable contribution** is not 'emotion has dynamics'. It is whether a carefully measured compact state representation predicts held-out affect trajectories **better than a robust measurement-error/nonstationarity rival**, and whether the distinctive evaluation/reachability layers yield separately testable predictions in a future intervention design.

## Benchmark contract
- Fix information availability and forecast horizon *before* comparing models.
- Include an autoregressive report baseline, a measurement-error/nonstationarity state-space rival, an appraisal/context rival, and only then an ER extension with a defensible extra parameter.
- Compare proper scoring rules, calibration, stability under missingness, participant transfer and complexity.
- Ablate one mechanism at a time. A better score without measurement identification supports prediction, not ontology or causal explanation.
- Publish negative outcomes and rival forecasts. Do not retrofit a model family to make a result seem uniquely predicted.

## Specific literature to audit in a later dedicated review
- Scherer (2009), dynamic architecture of emotion, DOI 10.1080/02699930902928969.
- Gross (1998), antecedent- vs response-focused emotion regulation, PMID 9457784.
- Schuurman, Houtveen & Hamaker (2015), measurement error in n=1 psychological autoregression, DOI 10.3389/fpsyg.2015.01038.
- Schuurman & Hamaker (2019), person-specific reliability and measurement error in multilevel autoregression, PMID 30188157.
- Partially observed stochastic control and appraisal/decision-theoretic emotion models: select exact strongest comparators before claiming priority.

**Interpretation discipline:** predictive compression, statistical identification, mechanistic interpretation, normative justification and causal intervention success are five separate evidentiary achievements. No one result automatically establishes the next.

---

## Amendments proposed by Claude Opus 5.5 (2026-11-20)

These are appended to GPT-6's draft above, which is left unchanged. The citations below were checked against publisher or index records this session. See the [staging review](2026-11-20-claude-staging-review.md) for the reasoning.

**Nearest established families, named precisely**

| Matrix row | Closest established work | What it means for novelty claims |
| --- | --- | --- |
| Context/history-conditioned transitions; predictive vs persistent state | **DSEM**, which combines multilevel time-series and structural equation models with person-specific parameters and measurement error ([Asparouhov, Hamaker & Muthén, 2018](https://doi.org/10.1080/10705511.2017.1406803)). **DynAffect**, which models individual differences in affective home base, variability and attractor strength with a diffusion (OU) process ([Kuppens, Oravecz & Tuerlinckx, 2010](https://doi.org/10.1037/a0020962)). | R-006's F1/F1+R/F2 comparison sits squarely inside DSEM-class modeling. Its result would be a measurement finding about this dataset, and a prerequisite for ER rather than evidence of ER's novelty. |
| Person-specific persistence | Individual differences in emotional inertia, linked to maladjustment ([Kuppens, Allen & Sheeber, 2010](https://doi.org/10.1177/0956797610372634)). Aggregating AR(1) units with heterogeneous coefficients produces long memory ([Granger, 1980](https://doi.org/10.1016/0304-4076(80)90092-5)). | A pooled model with one inertia can mistake person differences for a slow component. Person-specific inertia is a declared rival, not a nuisance to ignore. |
| Policy/information/horizon-dependent reachability | Finite-horizon probabilistic reachability for controlled discrete-time stochastic systems, solved by dynamic programming ([Abate, Prandini, Lygeros & Sastry, 2008, *Automatica* 44(11)](https://ptolemy.berkeley.edu/projects/chess/pubs/435.html)). | `R_{h,α}` in `theory/model.md` is the standard terminal-time form. Novelty cannot rest on the definition, only on how targets and feasible actions are specified and measured for affect. |
| Measurement: reporting scale, person-period shifts, MBCT contrast | **Response shift**: change in internal standards, values or conceptualization ([Sprangers & Schwartz, 1999](https://doi.org/10.1016/S0277-9536(99)00045-3)). **Anchoring vignettes**, for respondent-specific use of response scales ([King, Murray, Salomon & Tandon, 2004, *APSR* 98(1)](https://www.cambridge.org/core/journals/american-political-science-review/article/enhancing-the-validity-and-crosscultural-comparability-of-measurement-in-survey-research/220C13F13BA152E91A53F794BE3575ED)). | These are the established names, and an established tool, for R-001's gauge freedom and #42's reporting-intercept equivalence. A therapy-induced response shift is the declared rival to "MBCT raised latent PA". |
| Minimal-model challenge (Gate B) | Dynamic measures add little beyond mean levels and variability when predicting well-being ([Dejonckheere et al., 2019](https://doi.org/10.1038/s41562-019-0555-0)). | That estimand is between-person prediction, not within-person forecasting, so it is not a direct test of ER. It is still the right prior: expect complex dynamics to add little until shown otherwise. |

**One candidate row to add**

| Candidate ER contribution | Nearest established families | What overlaps | What would genuinely discriminate? | Present evidence |
| --- | --- | --- | --- | --- |
| Fittingness and reachability targets stated in **gauge-invariant** (identified) coordinates | Anchoring vignettes; response-shift methods; reachability with specified target sets | Scale use can differ by person and change with treatment | Whether a target defined in anchored or person-relative units predicts outcomes that report-unit targets miss, especially under interventions that change reporting | Proposal only (staging review, "anchor dilemma"); no comparator found yet, so search before claiming |
