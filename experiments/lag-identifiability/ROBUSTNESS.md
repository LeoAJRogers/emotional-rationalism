# Director Pass III — proxy contamination sensitivity (2026-11-22)

**Status:** exploratory synthetic experiment executed locally; no human data. This note records the second benchmark's results. The runnable second-rung script remains a local artifact pending repository transfer.

Three known linear lag mechanisms (belief, affect, report); true lag coefficient 0.78, 240 observations per sequence, randomized piecewise-constant cues. 20 seeded sequences per true mechanism, hence 60 classifications per condition. Gaussian observation noise SD 0.12 or 0.4, with shared report/proxy noise. The simulated affect proxy is a known mixture of latent affect and reported affect. Its mixture weight is supplied to the candidate fitting models: **a favorable assumption, not real-world construct validation**. Fit coefficient on first 60%, select rival on next 20%, reserve final 20% for evaluating the selected predictor. Sampling stride 1 or 4.

At observation-noise SD 0.4 and stride 1:

| Channels | Correct / 60 |
|---|---:|
| Report only | 20 |
| Report + belief | 39 |
| Report + belief + idealized proxy (0% report mixture) | 58 |
| Report + belief + proxy (75% report mixture) | 47 |
| Report + belief + proxy (100% report mixture) | 39 |

At stride 4, the same sequence was 20, 39, 58, 47, 40. Report-only classification is determined by tie ordering under exact structural equivalence; 20/60 is **not** a chance-level empirical finding. The tiny 39-to-40 difference is not meaningful at this sample size.

**Interpretation:** an additional measurement channel only resolves ambiguity when it carries information beyond the existing report. If it is entirely another report measurement, affect and reporting persistence remain structurally ambiguous. This does not validate physiology as an affect measure.

**Limitations:** no process disturbances, ordinal outcomes, heterogeneous participants, informative missingness, unknown proxy loading, or model misspecification. The fitting model is given the true proxy mixture. The model-selection split is not a final confirmatory set. A follow-up must challenge the unknown loading assumption and recover parameters under process noise before any prospective human study.

**Integration Delta:** 1/5. No change to the formal scaffold. Keep this a bounded synthetic design result.
