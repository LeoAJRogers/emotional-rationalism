# Extended adversarial pass: encouragement, adherence, and direct effects

2026-11-20, GPT-6. Synthetic methodological exercise, not human emotional evidence.

## Design
Latent readiness H is a fair binary draw. Under natural selection, assignment Z=H and action A=H. Under randomized encouragement, Z is an independent fair draw. Actual A=Z with probability 0.7, otherwise A=H. Action-causal outcome Y=A; readiness-causal outcome Y=H. In a third model, with probability 0.3 the outcome is replaced by Z, representing a direct assignment pathway, not a validated psychological theory. N=100,000 per condition; seed 31. Run `python experiments/causal-reachability-counterexample/adversarial.py`.

## Executed local results

```
model,assigned,adherence,direct,ITT,observed_contrast,first_stage
action,False,1,0,1.0000,1.0000,1.0000
readiness,False,1,0,1.0000,1.0000,1.0000
action,True,0.7,0,0.6989,1.0000,0.6989
readiness,True,0.7,0,0.0007,0.3017,0.6989
readiness,True,0.7,0.3,0.2985,0.4231,0.6989
PASS
```

ITT is E[Y|Z=1]-E[Y|Z=0]; observed contrast is E[Y|A=1]-E[Y|A=0]; first stage is E[A|Z=1]-E[A|Z=0].

**Debugging provenance:** An initial assertion mistakenly expected action-causal ITT of 0.3–0.4, confusing nonadherence with adherence. The first local run failed; assertion corrected to 0.68–0.72, and rerun passed.

## Adversarial findings
Natural observational associations cannot distinguish the baseline models. Random assignment with imperfect adherence produces ITT near 0.7 in the action-causal model, but near zero in the readiness-causal model. Nevertheless, the naive action contrast remains ~0.30 in the readiness-causal model, reflecting selection by readiness. Direct assignment effects generate ITT ~0.30 even though actual action has no causal effect; interpreting ITT/first-stage (~0.43) as an action effect would violate the exclusion restriction.

Assignment, action, interpretation/context, readiness, and outcome must be distinguished when assessing reachability. Random assignment can identify an effect of an assignment protocol under suitable assumptions; it does not automatically identify the effect of the performed action. This does **not** establish a human-emotion mechanism, the prevalence of meaning effects, or general causal identification. No human datasets were accessed in this pass.

## Next tests
Model explicit interpretation mediators, time-varying readiness and feedback, measurement noise, and nonadherence; assess empirical datasets for recorded assignment, choice, interpretation and timing. Avoid intervention-sensitive reachability claims without adequate design and assumptions.
