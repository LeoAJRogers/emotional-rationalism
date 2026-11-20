# Two-step causal feedback extension

**Executed locally:** 2026-11-20, Python 3, standard library. Source: `dynamic.py`. 100,000 independent two-step trials per condition, fixed seed. Synthetic only.

## Model

At t=0 latent readiness H0 ~ Bernoulli(.5). Under natural action selection U0=H0. Under 10% exploration, U0 is replaced with a fair independent coin with probability .1. Under assignment, U0 is fixed at 0 or 1.

Action-causal model: Y0=U0. Readiness-causal model: Y0=H0. **Both models share the same feedback rule**: H1=Y0 with probability .8; otherwise H1 is an independent fair coin. At t=1, U1=H1 and Y1=U1 in action-causal model or H1 in readiness-causal model. Thus the t=1 outcome is always H1; the models differ in how U0 changes Y0 and thereby H1.

This is a deliberately minimal feedback system, not an emotional model. Outcomes are binary and do not represent affect valence, fittingness, agency, or clinical change.

## Actual local output

```text
model,policy,P(Y0=1),P(Y1=1),P(U0!=Y0)
action,natural,0.49845,0.49825,0.0
action,explore10,0.49871,0.49872,0.0
action,do0,0.0,0.1004,0.0
action,do1,1.0,0.89903,0.0
readiness,natural,0.49845,0.49825,0.0
readiness,explore10,0.49845,0.49825,0.05006
readiness,do0,0.49845,0.49825,0.49845
readiness,do1,0.49845,0.49825,0.50155
PASS
```

With natural action selection, both structural models generate the same **coupled synthetic sample**; this is verified by an assertion on the reported aggregate probabilities, not a formal proof of full distributional equivalence. The equations themselves establish equivalence under U0=H0, including both outcomes and feedback, given shared exogenous draws.

Under do(U0=1), the theoretical probability P(Y1=1) is .9 in the action-causal model and .5 in the readiness-causal model. Thus a one-step causal ambiguity propagates into future reachability. A target probability threshold of .75 at t=1 is met in the former and not the latter.

Under 10% exploration, the models diverge in P(U0 != Y0): 0 versus approximately .05, enabling discrimination **within this restricted model family**.

## Interpretive limits

This does not show that human emotional dynamics have these binary mechanisms, nor that randomization is necessary or sufficient for causal identification generally. It assumes known timing, no interference, perfect outcome measurement, stable structural rules, and an intervention with perfect adherence. A realistic model must account for partial observation, anticipation, policy selection, action adherence, delayed feedback, competing causal structures, and ethical intervention constraints. Crucially, it is not a claim that a person's emotional state is directly selectable by will.

## Next falsification target

Test whether a model trained only on natural trajectories can predict held-out intervention trajectories under partial observability. Compare observational likelihood, interventional calibration, and target reachability separately. Avoid treating model-family discrimination as general identification.
