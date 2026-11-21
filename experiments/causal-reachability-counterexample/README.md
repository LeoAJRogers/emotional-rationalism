# Observational equivalence versus causal reachability

**Status:** synthetic counterexample, executed locally with Python 3 on 2026-11-20. Not a human-data analysis. Source: `simulate.py`.

Run from repository root:

```sh
python experiments/causal-reachability-counterexample/simulate.py
```

No external packages or datasets required. A fixed random seed generates 10,000 observations in each model. Both models produce identical observed (action, outcome) rows: action and outcome agree perfectly. The hidden-variable structural model differs from the causal-action structural model only under intervention.

Observed local output:

```text
action: observational rows identical; do(0)=0.0000; do(1)=1.0000; effect=1.0000; target reachable at alpha=.75: True
readiness: observational rows identical; do(0)=0.5053; do(1)=0.5053; effect=0.0000; target reachable at alpha=.75: False
```

The exact theoretical intervention probabilities are (0,1) in the action-causal model and (0.5,0.5) in the hidden-readiness model. The 0.5053 is finite-sample Monte Carlo variation. Because both models are seeded identically, equality of observational rows is an explicit assertion. This verifies a deliberately constructed counterexample, **not** the identification of causal effects from observational data. No external replication or empirical intervention was performed.

The companion conceptual note is [the reachability identification note](../../research-log/2026-11-20-reachability-identification-note.md). Next useful adversarial extension: add noisy readiness proxies and evaluate observational versus interventional generalization; preregister the comparison before inspecting results.

The [extended validation report](VALIDATION.md) records a reproduction of all six original scripts, an exact two-step test of assignment versus performed action, and an aggregate audit of three public human datasets.
