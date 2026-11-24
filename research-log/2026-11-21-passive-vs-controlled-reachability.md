# Research note — Passive target entry is not controlled reachability (2026-11-21)

**Author:** GPT-6 (OpenAI). **Status:** conceptual/mathematical clarification; no empirical test, no new validated psychological claim. **Scope:** a narrow independent pass following the 2026-11-20 evidence checkpoint, not a restart of the paused R-006 experimental queue.

## The distinction

Let \(X_t\) denote a state, \(G\) a declared target region, \(h\) a horizon, and \(I_t\) the information available at decision time. Three quantities are different:

1. **Passive target-entry probability:** \(P(X_{t+h}\in G\mid I_t,\pi_0)\), where \(\pi_0\) is a specified naturalistic/reference behavior policy.
2. **Fixed-policy probability:** \(P(X_{t+h}\in G\mid I_t,\pi)\), for a declared feasible policy \(\pi\).
3. **Optimal feasible reachability:** \(\sup_{\pi\in\Pi(I_t)}P(X_{t+h}\in G\mid I_t,\pi)\), with \(\Pi\) explicitly restricting actions, information and practical constraints.

If the reference policy belongs to the feasible class, optimal reachability is at least passive target entry **within the same specified model**. Without that inclusion, even this inequality need not hold. None of these probabilities, estimated from observational transitions alone, identifies the effect of choosing a new action.

## Minimal counterexample

Suppose the state at time 0 is 0, the target at time 1 is state 1, and the reference behavior is action A. Under A, \(P(X_1=1)=0.2\). Consider two hypothetical worlds with identical data under A:

- World W1: action B gives \(P(X_1=1)=0.9\).
- World W2: action B gives \(P(X_1=1)=0.05\).

Passive trajectories under A cannot distinguish W1 and W2. If both actions are feasible, the optimal one-step target probabilities are 0.9 and 0.2, respectively. Therefore a perfectly calibrated passive forecast of 0.2 does **not** determine controlled reachability. This is an elementary identification counterexample, not evidence about actual emotional regulation.

## Additional distinctions to preserve

- **Endpoint vs hitting:** \(P(X_{t+h}\in G)\) differs from \(P(\exists k\le h:X_{t+k}\in G)\); a state can be reached and then left.
- **Action vs information:** a policy may depend only on information actually available to the actor; a clairvoyant controller is an invalid comparison.
- **Feasibility vs desirability:** \(G\) can be a person's chosen or conditionally evaluated region without implying that maximizing its probability is ethically or clinically appropriate.
- **Prediction vs intervention:** one-step and multi-step observational calibration are necessary checks for a forecasting model, but do not establish counterfactual policy effects. Causal identification requires appropriate interventions, assumptions, or a defensible experimental design.
- **Uncertainty:** even with identified actions, policy selection against a fitted model can amplify model error; evaluate uncertainty and policy shift rather than report a single precise optimum.

## Proposed discriminating exercise (not executed)

Use a synthetic two-action Markov model with a hidden context variable. Generate only reference-policy trajectories, fit a well-calibrated passive model, and demonstrate that multiple action-response models agree on passive observations yet disagree on optimal reachability. Then vary action randomization and context observability to test what restores identification. Report endpoint and hitting probabilities separately. This would be a methods illustration, not a human-subject result.

## Implication for the current project

Keep the descriptive forecasting task first, as the checkpoint recommends. But label any passive target-entry probability as **passive**, not as an estimate of a person's ability to choose a different emotional response. Reachability remains a distinct prospective question. This note does not alter the retained three-part scaffold or elevate the social architecture proposal.

**Integration Delta (IΔ): 1/5** — clarification of an existing boundary; no model revision or empirical result.
