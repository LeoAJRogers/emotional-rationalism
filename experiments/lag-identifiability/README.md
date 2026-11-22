# Lag mechanism benchmark — initial synthetic smoke test (2026-11-22)

Run `python benchmark.py` (NumPy required). Three rival linear mechanisms apply the same one-pole lag to the cue, respectively in belief, latent affect, or reporting. Their report-only trajectories are exactly identical under matched coefficients and initial conditions. Thus the report-only model-selection tie is resolved by code ordering, not evidence.

Seed 20261122, 30 replicates per generating mechanism, 240 time points, Gaussian measurement noise SD .12, 65% fitting / 35% model-selection holdout:

| Sampling stride | Report only | Report + belief | Report + belief + idealized latent-affect proxy |
|---|---:|---:|---:|
| 1 | 30/90 | 60/90 | 90/90 |
| 4 | 30/90 | 60/90 | 90/90 |

The idealized latent-affect proxy is a simulated measurement of a known hidden variable, **not** a real validated human measure. This is a favorable implementation smoke test, not human evidence or a realistic power study. No process noise, ordinal responses, correlated measurement errors, nonignorable missingness, variable coefficients, or cue reactivity are included. The held-out segment is used to choose a rival, so is not an untouched confirmatory test set.

**Next:** add realistic nuisance rivals and a separate untouched test set before drawing any practical design recommendation. The code is a narrower runnable version of the November 22 director proposal; no theory promotion is warranted.
