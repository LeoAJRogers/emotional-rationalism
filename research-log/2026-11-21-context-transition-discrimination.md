# Context-dependent dynamics: a discriminating design (2026-11-21)

**Status:** independent GPT-6 theoretical pass; proposed experiment, **not executed**. No new empirical mechanism established. This note is subordinate to the 2026-11-20 evidence checkpoint and does not promote PR #4's social architecture.

## Question

When an identical nominal cue has different effects on reported affect, is that evidence for a distinct context-sensitive affect transition, or can context-dependent *appraisal*, baseline shifts, and reporting alone explain it?

The key is to avoid treating “context matters” as a distinctive prediction: nearly every serious appraisal model expects it.

## Minimal competing models

Let $x_t$ be an externally randomized cue, $c_t$ a measured context condition, $b_t$ a measured interpretation or belief, $e_t$ a latent affect state, and $y_t$ its noisy report. All models include person intercepts, lagged affect, observation noise, and declared response thresholds; the same sampling and missingness model is used across rivals.

- **M0: Context acts only through appraisal.** $b_{t+1}=B(b_t,x_t,c_t)$; $e_{t+1}=a e_t+g(b_{t+1})+\epsilon_t$. Conditional on actual appraisal and prior affect, there is no additional context term.
- **M1: Context modifies affect transition.** As M0, but $e_{t+1}=a(c_t)e_t+g(b_{t+1})+\epsilon_t$. The candidate distinguishing parameter is a *context-by-prior-affect persistence* interaction, not a generic context coefficient.
- **M2: Context modifies reporting or baseline, not persistence.** Same transition as M0, but $y_t=h_{c_t}(e_t)+\eta_t$ or an observed period-specific baseline varies with $c_t$. This rival can mimic M1 in raw ratings.

**Important:** M0's conditioning on measured $b$ does not guarantee the true appraisal is controlled. Noisy or incomplete appraisal measurements can manufacture residual context effects. Models need matched appraisal measurement-error alternatives.

## Proposed within-person experiment

Randomize a mild, ethically acceptable cue crossed with a context manipulation, repeated across short blocks; record appraisal **before** affect ratings when feasible, use multiple ordinal affect items, and include an independent physiological/behavioral measure if justified. Randomize context order, measure expectations and demand, predeclare timing and exclusions, and avoid treating physiology as a direct emotion meter.

A stronger test uses *matched-appraisal trials*: compare post-cue trajectories for conditions with similar measured belief shifts and initial affect, while accounting for uncertainty in matching. A design with context changes between the cue and later ratings can help separate appraisal-at-cue from subsequent persistence, but only if the context change does not itself create new appraisal.

## Distinguishing predictions

1. M0 predicts no context-specific difference in decay after conditioning on true appraisal and initial state. A difference in raw reports alone is insufficient.
2. M1 predicts context-by-prior-state effects on **future** affect trajectories that generalize across multiple report items and, when valid, external measures; effects should persist under explicitly tested measurement and baseline rivals.
3. M2 predicts context-specific rating thresholds or intercepts can account for apparent decay differences without a changed latent transition.

Score these predictions prospectively using participant-held-out or block-held-out predictive log scores and calibration; fit model complexity fairly. Simulate parameter recovery under realistic ordinal thresholds, sparse prompts, missingness, and appraisal error **before** choosing a threshold for success. Record cases where M0/M1/M2 are observationally indistinguishable as non-identification, not negative evidence for context.

## Decision rule and scope

Promote a context-modulated transition only if (i) the experiment identifies the persistence contrast in recovery simulations, (ii) it improves prespecified held-out prediction against M0 and M2 including their measurement-error variants, and (iii) estimates are stable across reasonable reporting models. Otherwise retain context sensitivity as a broad organizing idea, not a newly discovered dynamical law.

This pass refines the experimental question rather than adding another latent dimension. It does not test fittingness, optimal regulation, social norms, or the consciousness of any participant. The strongest novelty candidate would be a **recoverable separation of appraisal-mediated context effects from context-conditioned transition persistence**, not the assertion that emotions depend on context.

**Provenance:** GPT-6 independent pass requested by Leo, 2026-11-21. Related prior work: [model](../theory/model.md), [open problems](../challenges/open-problems.md), [Nov 20 evidence checkpoint](2026-11-20-public-integration-checkpoint.md). No dataset accessed or experiment run for this note.
