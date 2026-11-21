# Finite evidence: noisy observations and limited exploration

**Executed locally:** 2026-11-20, Python 3 standard library. Script: `finite_evidence.py`. Fixed random seeds, 300 independent simulations per model and sample size. All results are synthetic.

At each observation: latent H~Bernoulli(.5); U=H except with probability epsilon=.1 it is replaced by a fair coin; true Y=U in action-causal model, Y=H in readiness-causal model; observed Y is flipped with probability eta=.1. Record mismatch U != observed Y.

The exact expected mismatch rate is eta=.10 for the action-causal model. For readiness-causal model it is eta + (epsilon/2)*(1-2*eta) = .14. The classifier labels a sample readiness-causal if its mismatch rate is >.12, a midpoint chosen from **known generating parameters**.

## Executed results

| n per simulation | action mismatch mean | readiness mismatch mean | detection rate | false-positive rate |
|---:|---:|---:|---:|---:|
| 100 | .1012 | .1424 | .663 | .213 |
| 500 | .1007 | .1402 | .893 | .057 |
| 2,000 | .0999 | .1402 | 1.000 | .000 |
| 10,000 | .1000 | .1401 | 1.000 | .000 |

Each rate reflects 300 simulated trials, not a calibrated population-level confidence guarantee. At n=2000, zero observed errors among 300 trials does not imply zero true error probability. The 12% threshold is **oracle-informed**, not estimated from training data, so this is an optimistic discrimination demonstration, not an unbiased model-selection benchmark or sample-size recommendation.

## Meaning and next adversarial tests

This shows a constructed causal contrast can be obscured by label noise and sparse intervention support, yet become recoverable with larger samples under correct model assumptions. It does not validate an emotional mechanism, estimate an intervention effect in human data, or establish generic identifiability. Next tests should vary exploration and noise jointly, report uncertainty on classification error, and compare held-out evaluation with threshold selection performed on separate training data. Real experience-sampling data may contain within-person dependence, time-varying confounding, nonadherence, and systematic measurement error, none of which is represented here.

Keep descriptive prediction, conditional fittingness, and policy-specific causal reachability distinct.
