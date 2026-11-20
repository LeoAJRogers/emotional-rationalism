# Claude review — 2026-11-20

**Status:** AI-generated research review (Claude Sonnet 5.5), read from the repo at commit `ca29a13`. Not empirical validation. Claims below are unverified by a human; literature pointers are from model memory and must be checked before citing. Arithmetic in the worked example (1 − 0.9³ = 0.271; 1 − 0.9⁷ ≈ 0.522) was checked and is correct.

## Retain
- The descriptive / evaluative / reachability separation, with fittingness set-valued and conditional.
- The protocol's competing baselines and its explicit weakening criterion (little gain over autoregression weakens the added structure).

## Issues to consider

1. **No affect-to-belief feedback.** `B(b_t, o_t, c_t, u_t)` has no `e_t` input. Mood-congruent interpretation could produce lags without a slow affect transition. Add the dependence or state its absence as a limitation.
2. **Threshold fragility.** Reachability flips at an arbitrary α. Report the curve of max-over-policies Pr(e_{t+h} ∈ E*) against h as a continuous measure of the reachability gap.
3. **Fixed terminal time ignores overshoot.** Also report "reaches E* at any step within h".
4. **Policy information.** `b_t` is a belief over interpretations, but the person may not observe `e_t` or `c_t`. Specify the observation space; this is a partially observed control problem.
5. **Circularity risk in J_φ.** Fix J_φ in advance or elicit it from independent raters. Do not estimate it from the trajectories it evaluates, or fittingness becomes descriptive.
6. **The worked example is an illustration, not a test.** The gap is built in by the choice of J and the 0.1 transition probability.

## Experiment suggestions

- **Primary discriminating contrast.** A belief-resolved × regulation-prompt interaction on recovery rate. If belief updates change what regulation can do, a prompt should shorten recovery by different amounts after a resolved cue than after an unresolved one. An autoregressive baseline with only a prompt main effect predicts the same shortening in both.
- **Floor effects.** A low-stakes scenario may produce too little affect to show a lag. Consider a mild, ethically cleared stake with debriefing.
- **Immediate cue effects** can mimic a belief-mediated lag. Dose-response across cue credibility may help separate them.
- **Simulate before fixing the measurement schedule.** Detectability depends on sampling density relative to the lag.

## Literature to check (from memory, unverified)
- Probabilistic reachability for controlled stochastic systems (Abate and colleagues, ~2008).
- Kuppens et al. on affective inertia (natural AR baseline).
- Marsella and Gratch, EMA (computational appraisal).
- Joffily and Coricelli (2013), valence and active inference.
- D'Arms and Jacobson, *The Moralistic Fallacy* (fittingness versus other kinds of appropriateness).

## Note on the log itself
Integration Delta scores are self-assigned and unanchored; treat them as notes, not evidence.

## Correction to an earlier informal take
Before reading the subfolders, Claude said it saw no falsifiable predictions. The protocol does contain them.
