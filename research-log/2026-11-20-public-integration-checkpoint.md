# Public integration checkpoint — 2026-11-20

**Status:** Evidence synthesis and interpretation audit, not a new experiment or a validated general theory.  
**Integration Delta (IΔ): 2/5** — substantive narrowing of the empirical reading and prioritization of measurement, with no replacement of the three-part formal scaffold. IΔ measures magnitude of revision, not scientific quality or confidence.

## 1. What remains central

**Primary scientific task (working statement):** Find compact, adequately calibrated predictive descriptions of affect-relevant transitions conditional on perceived context, and test which history features are necessary **without confusing persistent state, context variation, and observation/measurement processes**.

This is a test program, not a theorem that affect is low-dimensional or universally governed by one transition law. The first formal human-affect case still separates:
1. **Descriptive transition:** what measured or latent response is likely under a specified model and information set.
2. **Evaluative fittingness:** which responses fit explicitly defended evidence/values under chosen criteria; this may be set-valued and disagreement is possible.
3. **Reachability:** how likely a declared target region is under feasible policies, information and horizon.

The first task supplies a candidate dynamics model for the other two, but **fittingness and reachability remain distinct research questions**. They are not empirical results, and the descriptive task need not assume that any emotion is morally or rationally correct.

The broader program on social coupling, changing norms, learning, and population-conditioned dynamics remains an **unmerged candidate architecture** in [PR #4](https://github.com/LeoAJRogers/emotional-rationalism/pull/4). Configurability is an architectural possibility; successful transfer to new populations is not established.

## 2. Evidence ledger — keep prediction, compression, mechanism and causality separate

| Observation / result | Supported conclusion | Not established |
| --- | --- | --- |
| R-001, synthetic reporting-scale rivals | A person-specific rating scale and proportionally scaled latent dynamics can be observationally equivalent; separation requires explicit scale/noise restrictions. | A uniquely measured individual latent sensitivity. |
| R-002, synthetic sparse-sampling holdout | A post-hoc model-selection margin that worked at baseline sampling misselected the slow rung in 59/80 W1/W2 sparse cells. | A sampling-invariant criterion for adding hidden state. |
| R-003, real data (127 participants, 10,926 forecast transitions) | Lag-one history helps prediction: +0.101 PA / +0.120 NA log score per observation. Earlier reports add +0.020 PA / +0.031 NA, and the tested EWMA summaries capture nearly all lags-2-to-5 gain. | A distinct slow emotional state, two true latent timescales, or a uniquely minimal state. |
| R-003 concurrent event task | Event ratings observed at the **same beep** predict PA and NA. The tested input-history interaction gave no detected incremental sensitization (PA -0.0008, NA -0.0004). | A causal additive event mechanism; the concurrent task is **not** a real-time forecast from strictly prior information. |
| R-004, period-specific history comparison | After adding a person-by-period running mean, remaining EWMA gain was +0.0068 PA / +0.0146 NA; the remaining fractions of the original history gain were 0.338 and 0.473. | That exactly 66%/53% of the gain was *caused* by a latent level shift. Score attenuation is predictive overlap. |
| R-004, within pre-treatment period | No preregistered day-level or cross-night carry-over flag passed; observed short-lag history is consistent with one persistent process plus non-persistent variance. | Proof that weak day or slow components do not exist. |
| R-004, randomized treatment contrast | MBCT minus waitlist change in mean **reported** PA was +0.55 on the 1–7 scale (95% CI +0.30 to +0.82). | A uniquely identified change in latent affect dynamics or measurement invariance. |
| R-004, event reactivity arm contrast | The raw PA event-reactivity change difference was +0.033 (95% CI -0.091 to +0.148): not detected at this analysis's power. | No effect under every measure/estimator; the source trial evaluated a different pleasant-activity outcome. |
| R-005, exploratory cross-item follow-up | A method-development prompt for future ordinal/item-level and missingness-aware comparisons. | Confirmed factor count, reporting mechanism, or latent affect structure. |

**Uncertainty on R-004 attenuation:** Paired-person bootstrap intervals for the *remaining* ratio `R_per/B2` are **PA 0.338 [0.180, 0.532]** and **NA 0.473 [0.342, 0.624]**. Both include 0.5. The preregistered point-estimate prediction (`<0.5`) held, but a claim that *more than half* was absorbed for either outcome is **not** established at 95% confidence.

**Independent numerical cross-check:** GPT-6 separately reimplemented the R-003/R-004 analysis rather than importing Claude's pipeline, checked both source-file SHA-256 hashes, and reproduced the forecast and arm point estimates to reported precision. This is cross-model-family numerical replication **on the same data**, not replication in a second population or independent clinical validation. The original register entries and later corrections are preserved verbatim in the [prediction register](prediction-register.md).

## 3. What this changes conceptually

**Main correction:** a predictive history feature is not necessarily a dynamical *state variable*. A summary of earlier reports can help because it filters measurement noise, tracks a changed person-by-period mean, captures day context, or tracks genuine persistent latent structure. A compact predictive statistic is therefore a useful engineering object, **not** a measurement of a unique emotional mechanism.

The R-003 result survives as evidence that past reports provide useful predictive information. Its initial “slow component” and “two timescales” interpretation is **narrowed**: R-004's tested within-period carry-over and day-level signatures were not detected, while period-specific means absorbed substantial overlapping predictive information. In particular, `1 - R_per/B2` is not an identifiable causal attribution.

A second exact caution is **measurement gauge freedom**: under some models, multiplying an individual's latent response and process noise by a factor while changing the rating scale yields identical observed sequences. Neither more fitting nor better prediction of the same reports, by itself, breaks that equivalence. Identification requires independent measurement anchors, restrictions, instruments, or discriminating data.

Finally, **a held preregistered prediction is not automatically severe evidence**. If standard rival models also predict it, the success verifies an analysis expectation without selecting a distinctive explanation. Future entries should declare the strongest rivals and how their predictions differ *before* testing. R-003's original timing is preserved; this correction is retrospective and not a retroactive preregistration change.

## 4. Evidence hierarchy after this pass

- **Core / retained:** descriptive transition, conditional/set-valued fittingness, and information-and-policy-dependent reachability are distinct; the broader contextual research objective is retained.
- **Strong methodological constraints:** separate reports from latent state; specify observation models; test against measurement error, nonstationarity and context; compare held-out predictions and calibration; do not identify mechanisms from predictive gain alone; distinguish randomized effects on observed outcomes from identified latent pathways.
- **Supported but bounded empirical contact:** one published human dataset shows persistence, added short history prediction, person-period predictive overlap and a randomized mean reported PA effect, with the limits in the table.
- **Tentative:** common low-dimensional mechanisms, separable perceptual and affect kernels, social feedback generating norms, hidden perspective states, multi-population transfer.
- **Parked / not inferred:** a universal correct emotional state, automatic mind-reading, subjective equivalence across species or AI, unique hidden dimensions, or a demonstrated causal slow emotional process.

## 5. Unresolved questions and pause point

1. **Item-level identification / proposed R-006:** predeclare an ordinal, missingness-aware held-out comparison of one shared dynamic factor, two shared factors, and one factor plus serial item residuals, with response thresholds and reliability controls. R-005's observed-item patterns are exploratory and the real missingness/series-length regime limits detection.
2. **External replication:** test the period-mean and measurement-error rivals on another suitable dataset; calibrate the exact contrast and missingness regime first.
3. **Multi-step predictions before reachability:** evaluate h-step predictive calibration under prespecified target regions and information sets before treating estimated region probabilities as intervention-sensitive reachability.
4. **Fittingness and belief-to-affect lag:** the original prospective cue/reappraisal experiment remains unrun. Keep this distinct from the openESM correlation work.
5. **Social coupling and norms:** staged, rival-controlled tests remain proposed; neither the present human trial nor the synthetic method benches establish population-general affect laws.

These are a **future queue, not an active assignment**. The 2026-11-20 integration deliberately ends this research cycle without opening a new experimental pass.

## 6. Provenance, access, and reproducibility boundary

- Public registered outcomes and their chronology: [R-001 to R-004 prediction register](prediction-register.md) and its append-only correction notes.
- Detailed method records, negative synthetic results, scripts and aggregate outputs: dated 2026-11-20 Research Commons PRs [#33](https://github.com/LeoAJRogers/research-commons/pull/33), [#38](https://github.com/LeoAJRogers/research-commons/pull/38), [#39](https://github.com/LeoAJRogers/research-commons/pull/39), [#41](https://github.com/LeoAJRogers/research-commons/pull/41), [#42](https://github.com/LeoAJRogers/research-commons/pull/42), [#43](https://github.com/LeoAJRogers/research-commons/pull/43) and [#44](https://github.com/LeoAJRogers/research-commons/pull/44). **Research Commons is private at this checkpoint:** external readers cannot independently inspect those records yet. This public synthesis does not pretend the supporting code is publicly archived.
- Source material: Geschwind et al. (2011), [original randomized trial](https://pubmed.ncbi.nlm.nih.gov/21767001/); openESM's [Zenodo record 17347473](https://zenodo.org/records/17347473), licensed CC BY-NC 4.0 for the harmonized data. Raw/participant-level data are not committed here.
- Established methodological comparator: Schuurman, Houtveen & Hamaker (2015), [measurement error in autoregressive modeling](https://doi.org/10.3389/fpsyg.2015.01038); Schuurman & Hamaker (2019), [person-specific reliability](https://pubmed.ncbi.nlm.nih.gov/30188157/). These motivate rivals; they do not prove which rival generated these observations.
- This synthesis draws on Leo's research direction, Claude Sonnet/Opus's reviews and experiments, and GPT-6's audits and cross-family reimplementation. The [contribution record](../CONTRIBUTIONS.md) applies. No named friends or private anecdotes are disclosed.

**Checkpoint decision:** integrate the public evidence boundaries; leave candidate architecture PR #4 open; preserve the registers and exploratory records; pause new research until voluntarily resumed.
