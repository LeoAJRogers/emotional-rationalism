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
