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

**Result.** See the R-006d outcome in the register, and `results/`.
