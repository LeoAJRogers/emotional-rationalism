# Proposed tests

## Lag after a belief update

Use a low-stakes ambiguous scenario with two randomized cue conditions. Give participants either credible disambiguating evidence or a matched cue that leaves the ambiguity unresolved. Record baseline interpretation probabilities and affect ratings, then record both immediately after the cue and at fixed follow-up times. Add a randomized regulation prompt versus a neutral prompt if testing how available actions influence the trajectory. Keep prompts and measurement times fixed in advance.

Estimate cue effects on belief and affect over time, using a repeated-measures model with participant-level variation. Predefine a meaningful belief change, affect scale, and time window. The candidate prediction is that belief updates precede affect changes in at least some conditions. Use assigned groups for causal comparisons and treat comparisons conditioned on observed belief change as descriptive.

Compare held-out predictions across an immediate appraisal model, an autoregressive model with affect history, and a model adding belief and regulation inputs to the same history. Use participant-held-out log scores and calibration of target-region probabilities. Little incremental predictive gain over the autoregressive model would weaken the case for the additional structure. A lag by itself is compatible with several existing models.

## Simulator and measurement checks

Recover the exact probabilities in the worked example before simulation. Vary transition probabilities, horizon, threshold, and measurement noise. Check when inferred reachability differs from the simulated ground truth. When there are several feasible actions, compare policies in simulation. A human trial with fixed prompts estimates outcomes under those prompts. Estimating optimal reachability requires assumptions about the full feasible set and its transitions.

Preregister the primary outcomes, smallest effect of interest, sample size rationale, exclusion criteria, and missing-data plan before data collection. For a human study, obtain appropriate ethics review and consent, and share only data cleared for public release.
