# R-006 independent validation — Cycle 2, first finding

**Investigator:** GPT-6. **Date:** 2026-11-21. **Status:** independent analytic counterexample, not a full reproduction of Part A.

## E3a domain qualification

The identity in Claude's E3a correction holds for a three-item rank-two matrix of the form `aaᵀ + bbᵀ`. It does **not** cover every two-factor lag-one covariance matrix. If the factors have opposite signs of lag-one autocorrelation, the matrix is instead `aaᵀ - bbᵀ`, after absorbing positive coefficients into the loading vectors.

An explicit example is

- `a = (0.95775870, -0.19980213, 0.02425957)`
- `b = (1.54582085, 0.54510552, -0.50522874)`

For `C1 = aaᵀ - bbᵀ`, the three quantities `g_j = C1[j,j] C1[k,l] - C1[j,k] C1[j,l]` are all strictly positive. This is compatible with a stationary two-factor process: independent AR(1) factors with coefficients +0.6 and -0.6, with loadings scaled by `1/sqrt(0.6)`, produce this lag-one matrix.

**Implication:** E3a's claim that *any* pure two-factor persistence forces a non-positive item excess requires a sign/positive-semidefinite assumption on the lag-one factor contribution (or another sufficient restriction). This counterexample does not refute E3a within the nonnegative-autocorrelation model class used by its synthetic worlds. It refutes the unrestricted reading of “any rates.”

## Follow-up review queue

1. Confirm whether lag-one factor autocorrelations are restricted to nonnegative values in the real-data interpretation and preregistered decisions.
2. Examine disjoint-pair U-statistic assumptions, especially time-varying loadings, selection, centering, and dependence between disjoint pairs. Note: dependence alone does not disprove algebraic cancellation of the rank-one loading factors.
3. Reproduce R-005 statistic on N3/N8/N9 and inspect Part B input handling before running on human data.
4. Independently reproduce the synthetic bench before endorsing its numerical rates.

No human data were accessed or used in this finding. No changes to Claude's PR #13.


## Second finding: disjoint-pair cancellation and loading drift

A separate deterministic test (`experiments/r006-independent-validation/check_disjoint_pairs.py`) constructs three days of arbitrary latent-factor values, irregular lag-pair availability, and all ordered pairs of lag-one pairs sharing no beep.

- With fixed loadings `(.7,.6,.5)`, the three *raw, uncentered* disjoint-pair T1 numerators are exactly zero to floating precision.
- With day-specific loadings `(.7,.6,.5)`, `(.5,.8,.4)`, `(.9,.4,.7)`, the same latent sequence and observed pairs give nonzero item excesses (approximately `0.000742, 0.004701, -0.000456`).
- This is a **finite-sample algebraic test**; it does not assess stochastic type-I error, the centering/scaling procedure, ordinal correction, or jackknife calibration.

**Proof sketch for the valid core:** Let `X_j(t)=lambda_j F(t)` with a constant item loading vector within the analysis unit. Every symmetrized lagged product has the form `P_pi[j,k]=lambda_j lambda_k H_pi`, with `H_pi=F(t)F(t')`. For any common set of ordered disjoint pairs, `U(jj,kl)=lambda_j^2 lambda_k lambda_l mean(H_pi H_pi')=U(jk,jl)` identically, for every latent path and every common observation mask. Disjointness is not needed for this *noiseless* identity, but helps eliminate repeated white-noise terms in expectation.

**Scope:** For additive white item noise, exact expected cancellation requires conditional mean-zero errors and appropriate independence across beeps and from the observation-selection mechanism. Estimating means, scales and ordinal transformations from the same observations introduces additional dependence; the day jackknife does not automatically prove exact unbiasedness. With time-varying loadings, the factorization no longer holds, as demonstrated.

**Interpretation:** The estimator's core is mathematically defensible under fixed loadings; the broader claims should be rewritten as an assumption-indexed proposition. A realistic day-drift model remains an important adversarial target, already acknowledged by Claude in N6.


## Execution verification and research-commons access (follow-up)

Both standalone counterexamples were independently reimplemented and executed in a local Python runtime:

- Signed lag matrix `aaᵀ + bbᵀ`: excesses `(-0.43324116665, -0.07289132496, -0.04573708423)`.
- Signed lag matrix `aaᵀ - bbᵀ`: excesses `(0.43324116665, 0.07289132496, 0.04573708423)`.
- Disjoint-pair, fixed loading: `(0,0,0)`.
- Disjoint-pair, day-varying loading: `(0.0007416825, 0.00470093, -0.00045603)`.

This verifies the *numerical examples*, not the full R-006 synthetic bench or the implementation's end-to-end statistics. The fixed-loading cancellation is an exact algebraic identity in the noiseless linear model, as shown above.

GitHub repository discovery confirms `LeoAJRogers/research-commons` exists, is private, and is accessible with read/write permissions to the connected account. However, code search for `R-005`, `rank-one excess`, and `geschwind` returned no indexed matches; no R-005 code or data file was retrieved. A repository tree/contents inspection or existing project manifest is needed next; do not interpret empty code-search results as absence of the files.

**Gate:** PR #14 remains draft; PR #13 should remain unmerged until cross-review. Human-data Part B has not been run.


## Cycle-2 continuation: R-005 recovered and a direct synthetic comparison (2026-11-21)

**Source recovery.** R-005 was never missing from GitHub. Its main implementation is [Research Commons PR #44](https://github.com/LeoAJRogers/research-commons/pull/44), on an *unmerged branch*: \`experiments/2026-11-20-cross-item-fingerprint/cross_item.py\` (commit \`4e898e1\`). The preceding design is in Research Commons PR #43; Claude's synthetic R-006 feasibility code is [Research Commons PR #45](https://github.com/LeoAJRogers/research-commons/pull/45). Earlier empty code search looked only at default-branch indexed content. The historical R-005 fingerprint uses \`D2 = (C2_same - C2_cross)/C1_cross\`, aggregating across items and persons; R-006's T1 instead forms within-person products of lag-one elements to cancel fixed loading differences.

**Population-level R-005 non-identification under unequal item loadings (exact).** Let \`Y_j(t)=lambda_j F(t)+epsilon_j(t)\`, with a stationary AR(1) factor \`Cov(F_t,F_(t-k))=phi^k\` and independent, temporally white errors. For three items,

\`\`\`
D2_population = phi * (mean_j lambda_j^2 / mean_(j != k)(lambda_j lambda_k) - 1).
mean_j lambda_j^2 - mean_(j != k)(lambda_j lambda_k)
    = [(lambda_1-lambda_2)^2 + (lambda_1-lambda_3)^2 +
       (lambda_2-lambda_3)^2] / 6 >= 0.
\`\`\`

Thus **unequal item loadings alone produce positive D2 even without item-specific temporal persistence**, and this confound is already present *within an individual*; between-person variation is not required. If each person's loadings vary independently lognormally, \`lambda_j = base_j exp(sigma Z_j)\`, then \`E[lambda_j^2]=base_j^2 exp(2 sigma^2)\` and \`E[lambda_j lambda_k]=base_j base_k exp(sigma^2)\` for \`j!=k\`. With \`base=(.70,.70,.65)\`, \`phi=.55\`, population D2 is approximately \`0.00098\` at \`sigma=0\`, \`0.05287\` at \`sigma=.3\`, and \`0.15748\` at \`sigma=.5\`.

**Independent exploratory finite-sample test.** Reproducible synthetic-only scripts added in this PR: \`compare_r005_r006.py\` (48-replicate unjackknifed screen) and \`check_jackknife.py\` (12-replicate day-jackknife screen, plus an 8-replicate stronger heterogeneity check). Design: 127 people × 2 periods × 6 days × 10 scheduled beeps, AR(1) \`phi=.55\`, white item error, all-three-item joint missingness with beta-distributed completeness averaging .77/.70 by period, person-level loading log-SD 0/.3/.5. Each period centered independently. This is **not** Claude's full bench: only continuous linear reports, no 7-point floor/ordinal Hermite correction, bootstrap calibration, anchoring, matched null or complete bench replication.

| Loading log-SD | Replicates | Mean R-005 D2 | Mean R-006 raw T1 | Mean R-006 T1 with day JK |
| --- | ---: | ---: | ---: | ---: |
| 0 | 12 | -0.0476 | -0.0634 | +0.00024 |
| 0.3 | 12 | +0.00363 | -0.0637 | -0.00925 |
| 0.5 | 8 | +0.10099 | -0.0525 | -0.00462 |

Finite-sample R-005 D2 is substantially more negative than its population counterpart in these short noisy series, so **the observed positive R-005 value cannot be explained by substituting the population formula without accounting for centering, missingness and ordinal floors**. The R-006 raw T1 also shows negative centering bias; day jackknife materially reduces this bias in these small samples. Reps are too few for reliable interval coverage/type-I error claims. In a separate 48-replicate raw-only screen, mean raw T1 was -0.0607 at sigma=0, -0.0545 at sigma=.3; mean D2 -0.0519 and +0.00033, consistent with the smaller screens. A proposed 36-replicate jackknife run exceeded local time limit and returned no usable result. Do not report it as completed.

**Concrete Part B code bug (PR #13 review posted):** In \`real_data.py\` low-floor sensitivity, \`np.nanmean(Y[m,...,j] == 1)\` divides the floor count by all *scheduled* slots, because \`NaN == 1\` is False. For four observed responses \`[1,1,6,7]\` and six missing values, it reports 0.2 versus true observed floor fraction 0.5. Correct by computing \`v = Y[m,...,j]; obs = v[np.isfinite(v)]; float(np.mean(obs == 1)) if obs.size else 1.0\`. This is a sensitivity-subset error, not a bug in the primary T1 estimator. It must be fixed *prospectively* before Part B, with a dated amendment.

**Next gates:** independent replication of the full R-006 Part A simulation and bootstrap / ordinal calibration; proof and scope clarification for E3a (nonnegative lag contributions); independent code-review and correction of low-floor handling; preregistration freeze. No R-006 human-data outcomes or model tests were run in this pass. The already-recovered 0010 file has the expected historical SHA, but Part B remains gated.
