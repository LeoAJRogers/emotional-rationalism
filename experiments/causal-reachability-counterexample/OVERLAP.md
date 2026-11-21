# Readiness proxy versus intervention overlap — executed synthetic extension

**Date:** 2026-11-20. GPT-6. Synthetic methodological demonstration only; no human participants, no affect data.

Run `python experiments/causal-reachability-counterexample/positivity.py`. Python standard library only. Local run completed with PASS, 100,000 generated observations for each of 12 conditions (2 causal models × 3 proxy accuracies × 2 exploration rates).

Structural definitions: latent readiness H ~ Bernoulli(1/2); observed proxy Z equals H with probability a; naturally chosen action U=H, except with probability epsilon an independent fair-coin action replaces it. Outcome Y=U in the action-causal model, and Y=H in the readiness model. Independent draws of H, proxy noise and exploration are assumed.

| Model | Proxy accuracy | Exploration | P(U != Y), simulated |
| --- | ---: | ---: | ---: |
| action | .5, .9, 1.0 | 0 or .1 | 0 |
| readiness | .5, .9, 1.0 | 0 | 0 |
| readiness | .5, .9, 1.0 | .1 | .04997 |

With epsilon=0, the observed joint distribution of (U,Y,Z) is identical under both models, for any proxy accuracy, even perfect measurement. At proxy accuracy 1, some (U,Z) cells have zero support: knowing H does not tell us what happens under U != H. With epsilon=.1, the randomized action produces discordant (U,Y) observations in the readiness model and none in the action-causal model. The exact expected mismatch probability is epsilon/2 = .05. This distinguishes the **specified** structural models under this intervention protocol, not arbitrary competing causal models.

Important caveats: (1) random exploration is an assumed intervention and would require ethical/safety constraints for real affective behavior; (2) action adherence, interference, temporal feedback, measurement error in Y, and confounding outside this simple construction are not modeled; (3) the result does not imply that randomized intervention is always required for identification, or that observing a noisy proxy is useless; identification may be possible under other justified assumptions/designs; (4) a randomized encouragement is not equivalent to assigned action if adherence is incomplete; (5) these tests demonstrate a designed invariant and are not severe empirical tests of a theory.

**Implication:** separate predictive sufficiency, measurement identification, action overlap, and causal-policy identification as different checks before making intervention-sensitive reachability claims. Do not promote this toy result to a validated human-emotion mechanism.
