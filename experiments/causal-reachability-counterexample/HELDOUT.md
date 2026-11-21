# Held-out intervention prediction failure

**Executed locally** on 2026-11-20 with Python 3, standard library, fixed seed 20261120. Code: `heldout_intervention.py`. Synthetic only.

For each model, generate 100,000 natural observations (H~Bern(.5), U=H, Y=U for action-causal or Y=H for readiness-causal). Fit a simple empirical conditional estimate P(Y=1 | U=1) from the natural observations. Generate an independent 100,000-observation intervention evaluation set with U assigned to 1 and new H draws. Evaluate the fixed observational estimate against the actual intervention outcome frequency.

Local output:

```text
model,observational_prediction,assigned_outcome,absolute_error
action,1.00000,1.00000,0.00000
readiness,1.00000,0.49817,0.50183
PASS
```

The observational predictor is perfectly calibrated on its naturally observed U=1 stratum in both models. Under assigned action 1, it remains calibrated for the action-causal model but overpredicts the readiness-causal model by approximately 50 percentage points. This is an **out-of-distribution intervention evaluation**, not conventional held-out observational validation: a randomly held-out natural test set would not reveal the error.

The example is deliberately deterministic and does not assess real-world model performance. Its value is establishing a failure mode and motivating separate validation criteria: observational predictive accuracy, action support/overlap, interventional calibration, and policy-specific reachability. Do not equate observational conditional probabilities with do-intervention probabilities absent causal assumptions.

**Next challenge:** compare models trained on mixed natural and randomized-action data; test calibration under changed intervention policies and feedback, with finite-sample uncertainty. A practical ethical dataset may require natural experiments, randomized encouragement, or sensitivity analysis rather than assigned emotional interventions.
