# Executed norm-conditioned synthetic identification check

**Date:** November 19, 2026  
**Status:** Executed in local Python/NumPy, deterministic seeds, hand-designed dynamics. **No psychological or cross-species empirical findings.**  
**Code:** [norms_identification.py](norms_identification.py). Reproduce using \`python norms_identification.py\`.

## Question

If social events acquire different affective significance under different community norms, does a compact shared dynamical rule transfer better when conditioned on independently known descriptive and injunctive norm variables? Can a deliberately incompatible third population expose the limits of that rule?

## Design

- Three **invented** populations: 'affiliative' and 'territorial' are assigned the *same* affective transition coefficients but opposite signs of descriptive and injunctive norm coordinates; 'different' shares the affiliative coordinates but has different response coefficients.
- Two mutually affecting agents in each eight-step episode, one scalar latent affect-relevant state per agent. This is not a full account of real emotions; no private thought, appraisal, norm judgment, or moral evaluation is modeled.
- Generated state law: \`z_next = rho * z + gamma * partner_z + beta_desc * cue * descriptive_norm + beta_inj * cue * injunctive_norm + process_noise\`. Coefficients are explicit invented simulation parameters. Norm coordinates vary independently across episodes around each population's center.
- Fit least squares on 16,000 latent transitions from the first two populations; evaluate 2,560 held-out transitions from each population. Use a separate 125-episode calibration sample for the third population model.
- **Raw pooled comparator:** same \`z, partner_z, cue\` without norm interactions. **Norm-conditioned shared model:** replace raw \`cue\` by \`cue * descriptive\` and \`cue * injunctive\`. **Calibrated population-specific model:** fit new dynamics using observed local norm and state variables.

## Actual output of executed code

| Held-out population | Pooled raw-context RMSE | Shared norm-conditioned RMSE | Locally calibrated RMSE |
|---|---:|---:|---:|
| Affiliative | 0.21289 | 0.02475 | Not tested |
| Territorial | 0.20980 | 0.02601 | Not tested |
| Different dynamics | 0.05109 | 0.23866 | 0.02543 |

The shared coefficients recovered from the norm-conditioned model were \`[intercept 0.00017, persistence 0.59892, partner feedback 0.17955, descriptive effect 0.09962, injunctive effect 0.16016]\`; true values were \`[0, 0.6, 0.18, 0.1, 0.16]\`.

For the third population, the fitted local parameters were \`[0.00023, 0.24379, 0.48558, -0.09831, 0.06884]\`; invented truth was \`[0, 0.25, 0.48, -0.10, 0.07]\`.

### Interpretation

A single affect transition law can **mechanically** transfer between communities when independently specified local norm coordinates explain the event's significance. If the transition dynamics differ, imposing the shared law can be worse than a simple pooled raw-context predictor, as in the deliberately incompatible third population.

These outcomes are expected from the model we deliberately constructed. They **do not** establish that norms cause real human feelings, that four parameters are biologically universal, or that injunctive norms are accurately measurable across species. Nor do they establish causal direction: norms were exogenous known numbers in the simulator.

## Limits and next experimental changes

1. Distinguish *public expression* from latent affect: injunctive norms may change what people show without changing what they feel; add a separate emission model.
2. Avoid norm/experience circularity: recover norms from independent data, not by using the emotional outcomes being predicted.
3. Test time-varying norms and individual identification/attachment to communities; communities can contain multiple subcultures.
4. Separate social relevance from intrinsic stimulus valence; change only a norm cue while holding event content constant.
5. Include an evolutionary/phylogenetic comparative hypothesis without presupposing that the same subjective emotions exist.
6. Use a hierarchical partial-pooling model and compare it to fully independent population fits; evaluate held-out populations only under explicit calibration.
7. Predefine model-selection scores and uncertainty intervals for future larger samples. Here standard errors and confidence intervals were not computed.

**Note on chronology:** Earlier exploratory synthetic figures in the conversation should not be treated as audited research results unless independently reproduced. This note reports the specific code and numbers actually executed for the population-norm check.
