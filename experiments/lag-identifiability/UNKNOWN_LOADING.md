# Director Pass IV — unknown proxy loading (2026-11-22)

**Executed synthetic sensitivity analysis; no human data.** Previous model fitting was supplied the true mixing fraction of an auxiliary affect proxy. This pass estimates each candidate's mixture fraction on training observations, then selects a rival on separate validation observations.

20 seeded sequences per true mechanism, 240 points each, noise SD 0.4, lag coefficient 0.78. Training 60%, selection 20%; no untouched final confirmatory test. Candidate coefficient grid 0.1–0.9 (33 points); candidate mixture grid 0–1 (41 points).

| True report fraction in proxy | Correct / 60 | Confusion (rows true affect, belief, report; columns predicted same order) |
|---|---:|---|
| 0% | 56 | [[18,0,2],[1,19,0],[0,1,19]] |
| 50% | 54 | [[18,0,2],[1,19,0],[2,1,17]] |
| 75% | 50 | [[18,0,2],[1,19,0],[6,1,13]] |
| 100% | 42 | [[18,0,2],[1,19,0],[14,1,5]] |

**Structural finding:** affect-lag and report-lag models with matched lag coefficients yield identical reported trajectories and belief channels. Affect-lag latent affect equals the report, so the proxy equals the report for every mixture fraction. Report-lag with 100% report mixture also yields the same proxy. Therefore the joint observables are *exactly* identical at that boundary. The classifier's apparent preference for affect is not identification. The classification percentage at 100% mixture is not a reliable mechanism identification rate.

**Limits:** synthetic idealized linear models, no process noise, ordinal responses, missingness, unknown nonlinear observation map, or person heterogeneity. The fit uses an in-sample search over loading and coefficient; validation selection is not an untouched confirmatory test. Earlier fixed-loading results are not directly comparable to these runs as a controlled effect estimate.

**Decision:** require measurement-channel validation and independent anchors before causal or latent-mechanism interpretation. Next challenge: correlated observation errors, unknown nonlinear response maps, and an independent model audit.

**Delegation proposal:** independent reviewer to check equivalence proof, search/tie handling and leakage, and propose a correlated-error rival. No other agent's review has yet been performed.

**Integration Delta: 2/5.** Local change to measurement assumptions, not the core framework.
