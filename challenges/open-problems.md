# Open problems and related research

- **Measurement.** Self-report, expression, and physiology can diverge. Test whether the proposed affect coordinates are stable across repeated trials and comparable across participants.
- **Identifiability.** Several combinations of belief update, affect persistence, and measurement noise can produce the same observed lag. Use repeated measurements and independently varied cues and prompts to test which parameters can be recovered.
- **Fittingness.** Different evidential standards or values can yield different minimizers. Document disagreement and test sensitivity to the choice of loss before treating the optimum as a target.
- **Feasible actions.** Regulatory choices are partly unobserved and context dependent. A restricted action set can underestimate attainable responses. A model that grants participants unavailable information can overestimate them.
- **Competing explanations.** Delayed ratings may follow measurement artifacts, demand effects, baseline affect persistence, or changing context. Look for predictions that distinguish the proposed model from these alternatives and from existing appraisal and regulation accounts.

## Questions sharpened by the 2026-11-20 checkpoint

- **Predictive summaries versus hidden state.** An EWMA or extra lag can improve forecast scores because it denoises the last report, tracks a day effect or reflects a person-by-period change. Build explicit observation/noise and nonstationary rivals before calling such a feature a latent timescale. Compare held-out likelihood and calibration, and test whether purported dimensions are identifiable.
- **Reporting gauge and person-period shifts.** Multiplicative report-scale and latent-sensitivity parameters can be observationally equivalent under noise rescaling. Add external scale anchors or sufficiently restrictive, declared measurement models. A period-specific baseline's shared score gain does not identify its biological, psychological or reporting origin.
- **Short series, missingness and model selection.** Recalibrate error rates when sampling gaps and observation masks change. The R-002 sparse-sampling margin failed; R-005's cross-item explorations do not settle factor count under the observed missingness and short sampling windows.
- **Proposed item-level test (R-006, not yet preregistered here).** Compare ordinal dynamic one-factor, two-factor and one-factor-plus-serial-item-residual models using matched held-out scores, item thresholds, person-level clustering, and missingness-aware synthetic recovery; test nuisance rival families not reused during threshold selection.
- **Replicate the history decomposition.** Check period-specific shifts, day structure and measurement error on another sample. Report paired-person interval estimates rather than interpreting a fraction of predictive score as a fraction of causal explanation.
- **Reachability requires multi-step calibration.** Before extrapolating one-step dynamics to h-step probability of a target region, validate multi-step predictive distributions under fixed information, intervention and time horizons. Passive target entry and optimal action-policy reachability are different estimands.
- **Evidence severity.** A preregistered prediction that every known rival also predicts may test an implementation without discriminating mechanisms. Future prediction entries should describe rival forecasts, failure criteria, prior expectations and what a held outcome actually rules out.

See the [public integration checkpoint](../research-log/2026-11-20-public-integration-checkpoint.md) for quantitative results and the status hierarchy. These are unassigned future questions, not claims of new empirical findings.

## Starting literature

- Klaus R. Scherer (2009), *The dynamic architecture of emotion: Evidence for the component process model*. A comparator for sequential appraisal and coordinated emotion components. [Paper](https://doi.org/10.1080/02699930902928969)
- James J. Gross (1998), *Antecedent- and response-focused emotion regulation: Divergent consequences for experience, expression, and physiology*. An experiment comparing reappraisal and suppression across response measures. [Paper record](https://pubmed.ncbi.nlm.nih.gov/9457784/)
- Anil K. Seth (2013), *Interoceptive inference, emotion, and the embodied self*. A theoretical comparator for the role of inference about bodily signals. [Paper record](https://pubmed.ncbi.nlm.nih.gov/24126130/)
- Noémi K. Schuurman, Jan H. Houtveen & Ellen L. Hamaker (2015), *Incorporating measurement error in n = 1 psychological autoregressive modeling*. Established AR+white-noise and ARMA rivals. [Paper](https://doi.org/10.3389/fpsyg.2015.01038)
- Noémi K. Schuurman & Ellen L. Hamaker (2019), *Measurement error and person-specific reliability in multilevel autoregressive modeling*. Observation-model comparator. [Paper record](https://pubmed.ncbi.nlm.nih.gov/30188157/)
- Nicole Geschwind et al. (2011), *Mindfulness training increases momentary positive emotions and reward experience in adults vulnerable to depression*. Original randomized trial underlying the openESM contact; its reward responsiveness endpoint differs from our event slope. [Paper record](https://pubmed.ncbi.nlm.nih.gov/21767001/)
