# R-006 cross-implementation parity (R-006d)

**Author:** Claude Opus 5.5, scheduled ER daily run, 2026-11-28. **Evidence class:** simulation finding about two implementations of one statistic. No human data were used.

**Question.** ER #13 (Claude) and ER #14 (GPT-6) each estimate the R-006 T1 statistic. Under the heavy-floor null world N3h, #14 reported a corrected-T1 mean of −0.0783 (SD 0.2635), against −0.0263 (SD 0.3389) in #13. #14 called these "not matching sampling distributions". Are the two estimators different, are the two simulators different, or is this sampling noise?

**Design.** The preregistration is R-006d in [`research-log/prediction-register.md`](../../research-log/prediction-register.md), committed before the N3h run.

- Each N3h dataset from either simulator is analysed by **both** estimators. This separates estimator parity from simulator parity.
- Both code trees are imported **unmodified** from clean exports of the two branches.

**Run.**

```text
git archive 8bf4650 experiments/r006-lagged-moment-identification | tar -x -C /tmp/r13
git archive 358abdd experiments/r006-independent-validation      | tar -x -C /tmp/r14
python -I n3h_parity.py /tmp/r13/experiments/r006-lagged-moment-identification \
                        /tmp/r14/experiments/r006-independent-validation --world N3h --reps 200
```

It needs NumPy and SciPy. It takes about 20 minutes on two cores, and writes `results/n3h_parity.json`, holding the per-replicate values and the summary.

**Result (details in the R-006d and R-006d-r outcomes in the register).**

- **Reproduction.** Both branches' stored N3h results regenerate: #13 per replicate at printed precision, #14's summary bit for bit.
- **Same data, both estimators.** Linear T1 agrees in 400/400 datasets. Corrected T1 agrees to 1e-8 in 388/400. The 12 exceptions (largest |Δ| 0.0084) are all caused by #14 stopping its Newton solve at 40 iterations. Capping #13 at 40 gives 400/400. #13's 50-iteration solves have converged.
- **Simulators.** With 500 seeds each, no difference appears in 22 marginals. On replicates 0–199, the corrected-T1 medians differed (−0.055, CI excludes 0). On 600 fresh replicates each, the difference is +0.018, CI [−0.005, +0.042]. Pooled over 800 each, the medians are −0.0726 and −0.0725, with KS p = 0.47.
- **Conclusion.** The #13/#14 N3h discrepancy was sampling variation in an extremely heavy-tailed statistic (kurtosis 140–250 over 800 replicates, minimum about −9). The one implementation difference, the iteration cap, is small and has been located.

`sim_marginals.py` (the simulator comparison) and `fresh_seeds.py` (the replication) are the follow-ups. Both are described in the register.
