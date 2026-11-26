# Independent review and build-out pass (Claude Opus 5.5, 2026-11-26)

A fresh Claude reviewer with no access to earlier project conversations wrote the review. It saw only the public repo, a skeptical-expert prompt and the open web. The review is summarized faithfully below; the build-out pass at the end is by the Claude session that commissioned it. Review status: commentary, not verification.

**Overlap with earlier repo work (corroboration, not new findings):**
- The 2026-11-20 Sonnet review already flagged threshold fragility in the reachable set and the terminal-versus-first-passage distinction.
- PR #17 (2026-11-22) already identified the same nearest precedents for C1–C3, flagged the fit-versus-warrant terminology issue, and proposed an "interpretive gap" (belief versus independent reference) and perceived reachability.

This reviewer did not see those notes and reached compatible conclusions. **New here:** CoMERG as a closer precedent, the endpoint-definition non-monotonicity, the one-action counterexample being passive entry, the grid-dependence argument, the structural objection that separation adds predictive power only through feedback, and the reviewer's decisive experiment.

## Review verdict

As a theory, the framework adds almost nothing yet. Each component is a textbook object: a controlled stochastic process (formally a POMDP), a Bayes-act argmin of expected loss, and a finite-horizon probabilistic reachable set. The separation holds by construction, and none of the empirical work touches what is distinctive. Process rigour and honest hedging are real, but are not a scientific contribution.

## Strongest case that it adds nothing

- **Dynamics:** DynAffect (Kuppens, Oravecz & Tuerlinckx 2010) already models person-specific OU affect dynamics and flags appraisals and regulation as time-varying inputs. **CoMERG** (Bosse, Pontier & Treur 2010, Cognitive Systems Research) uses difference equations with persistence, appraisal elements and regulation effort, and has been fitted to skin-conductance reappraisal data (Bosse et al., CogSci 2011). Huys & Renz (2017) place emotion and its control inside model-based valuation. Petter, Gross et al. (2025) formalize strategy choice as Q-learning over affect trajectories. With an unrestricted history summary, any process can be made Markov.
- **Fittingness:** D'Arms & Jacobson (2000) separate fit from moral and prudential propriety; Mason ("Dimensions of Emotional Fit", forthcoming) treats intensity proportionality; Brady (2009) covers recalcitrant emotion, the delayed-reply example. The argmin is Bayesian decision theory with a relabelled loss.
- **Reachability:** Abate et al. (2008) define finite-horizon probabilistic reach/safety under policy supremum, including thresholded maximal safe sets; the repo uses an endpoint rather than a hitting event. Person-information-restricted policies make it a finite-horizon POMDP (Papadimitriou & Tsitsiklis 1987 on complexity: seen in abstract only).
- **Separation:** "model, objective, feasible set" is the standard decomposition of control problems. CoMERG already separates generation dynamics, a norm (desired value) and regulation; Tamir (2016) separates emotion goals from dynamics. No theorem in model.md depends on the separation.

## What survives

- No paper found combining probabilistic reachability, a target set defined by fit (not hedonic value or goals), and person-information-restricted policies over affect. CoMERG's norm is a desired value; Petter et al. minimize negative affect. Search not exhaustive; even if new, it is a combination of standard parts with no new result.
- The passive-versus-controlled reachability note (2026-11-21) is correct, useful hygiene.
- Set-valued fit, sensitivity to the reference and criteria, and pre-committed narrow-or-retire rules are good practice.

## Math check (theory/model.md)

- Counterexample arithmetic is correct (0.271 at h = 3; 0.522 at h = 7, first crossing; 0.469 at h = 6).
- **The prose misdescribes the result.** At h = 7 the reachable set is {S}: the starting state A becomes "unreachable". The endpoint definition makes the set non-monotone in h.
- **Only one feasible action**, so the supremum is vacuous: this is passive target entry, which the repo's own 11-21 note says must not be called reachability. The claim being counterexampled is never stated.
- **Grid dependence.** Thresholding singleton probabilities means refining the grid empties the set; "reachable set meets fitting set" is neither necessary nor sufficient for P(e_{t+h} ∈ E*) ≥ α. The event formulation is the right object.
- **The fitting set is always nonempty**, so fit means "least bad"; no "nothing fits" and no graded fit. Under uncertainty the minimizer depends on the loss shape and can be a hedged middle state that fits no interpretation.
- **Components are not linked:** D isn't tied to observation history; E* is fixed at t while context at t + h may differ; it's ambiguous what the policy conditions on.

## Empirical work

R-001/R-002 are synthetic model-selection checks; R-003/R-004 are ridge AR forecasts on one ESM dataset. None involves beliefs, fittingness or reachability. Findings are already known (inertia; AR plus measurement noise; MBCT raising PA). Predictions held largely because rivals predicted the same. Gains are ~0.02 log score per observation. Code and preregistration timing are private; the independent check was another LLM on the same files.

## Conceptual problems

- **Fit conflated with desirability:** the loss handles "competing values", which is the moralistic-fallacy conflation; desired emotions are a third thing.
- **Category error:** fit attaches to emotion types with formal objects (fear–danger); the data are objectless PA/NA.
- **Population reference treats the typical as correct:** consensus-scoring bias (Barchard & Russell 2006); normality "is not merely statistical" (Gert 2016).
- **Identifiability:** the fitting set is stipulated, not empirical; controlled reachability needs counterfactual action effects observational ESM can't identify; belief-to-affect lag is confounded with report lag.
- **Core structural objection:** if fit is computed outside the dynamics, P(e ∈ E*) is a functional of any good predictive model. The separation can't add predictive power unless fit judgments feed back into dynamics or policy.

## Decisive experiment (reviewer)

Randomize evidence (credible disambiguating cue vs matched ambiguous cue) to shift fit; orthogonally randomize desirability (an incentive making calm or alarm useful) to shift goals; randomize action availability (reappraisal permitted or not). Measure belief, endorsed fit, desired emotion and felt affect repeatedly. Preregister held-out log-score comparisons against an appraisal-plus-AR model and a goal-directed regulation model in the style of Petter et al. (2025). If endorsed fit adds nothing beyond goals and appraisal, the fittingness component is an external normative overlay.

## Build-out pass

The core objection is also the way forward: the separation only matters if a person's own fit judgments feed back into what they do. Make perceived fit part of the model rather than an outside overlay.

This builds on PR #17's proposals. Its interpretive gap compares the person's belief about the situation with an independent reference. Perceived fit is the person's own judgment of whether their current feeling fits. The two are related but distinct, and perceived fit is the one that would drive regulation choices. PR #17's perceived reachability is its natural partner on the action side.

| Objection | What to build | What it lets us test |
| --- | --- | --- |
| Separation adds nothing unless fit feeds back | Add perceived fit to the state; regulation choices depend on the perceived-fit/affect gap | Does endorsed fit predict regulation and recovery beyond desired emotion and appraisal? |
| Reachable set grid-dependent, non-monotone | Redefine reach as an event (best achievable P(enter E* by h)) plus a hitting-time version | **Fit latency:** expected time to first enter the fitting set under the best feasible policy |
| One-action counterexample | Rebuild with two actions (wait, reappraise); state the refuted claim (a fitting state is always reachable once belief is corrected) | A case where policy choice changes whether fit is reachable in time |
| Fit means "least bad" | Graded fit with a threshold, so "nothing fits yet" is possible | When people report that no feeling fits, and its relation to distress |
| Fit conflated with desirability | Split the loss into fit (evidence only) and desirability (goals); measure each | Separate predictions for "I'd like to be calm" vs "calm fits" |
| Objectless affect | Emotion types with formal objects; appraisal-tagged ESM items | Fit judgments with something to be true of |
| Typicality | Use population reflected fit judgments only as a benchmark; report subgroup variation | Where reflected norms diverge across groups |
| Only dynamics tested | Add ESM items: "Does this feeling fit the situation?", "How would you like to feel?", "What did you do about it?" | Fit, desire and action data cheaply |
| CoMERG precedent | Cite and position: CoMERG targets a desired norm; this targets evidence-based fit under the person's own information | A checkable one-line novelty claim |

**Candidate leap: fit latency.** How long it takes someone to enter a fitting state after the evidence changes, given their available actions. Measurable, differs between people, connects to rumination (knowing a feeling doesn't fit but staying in it), and is what the delayed-reply example is about.

**Suggested order:** fix the reachability definition and counterexample; add the perceived-fit loop to model.md; preregister the decisive experiment with fit latency as the main outcome.

## Reviewer's sources (opened)

Abate et al. 2008, https://www.cs.ox.ac.uk/people/Alessandro.Abate/publications/APLS08.pdf · Kuppens, Oravecz & Tuerlinckx 2010, https://sites.socsci.uci.edu/~zoravecz/bayes/data/Articles/Kuppens2010FCAFI.pdf · Bosse et al. 2011, https://escholarship.org/content/qt5zr3r4w0/qt5zr3r4w0.pdf · Huys & Renz 2017, https://discovery-pp.ucl.ac.uk/id/eprint/10058790/1/Renz_1-s2.0-S0006322317317730-main.pdf · Petter et al. 2025, https://pure.uva.nl/ws/files/259262905/Emotion_Regulation_Fast_or_Slow.pdf · D'Arms & Jacobson 2000 (abstract), https://api.philpapers.org/rec/JACTMF · Mason, https://philarchive.org/archive/MASDOE · Gert 2016, https://www.journals.uchicago.edu/doi/10.1086/686004 · Brady 2009 (abstract), https://eprints.gla.ac.uk/8062 · Tamir 2016 (abstract), https://cris.huji.ac.il/en/publications/why-do-people-regulate-their-emotions-a-taxonomy-of-motives-in-em/ · Barchard & Russell 2006, https://www.psicothema.com/pi?pii=3275 · Unverified (abstracts only): Papadimitriou & Tsitsiklis 1987; Kuppens, Allen & Sheeber 2010.

---

## Correction and response, after GPT-6.2's cross-review (Claude Opus 5.5, 2026-11-26)

*Appended. The review and build-out pass above are kept unchanged as the dated record. This addendum corrects them where needed. Responds to GPT-6.2's [cross-review](https://github.com/LeoAJRogers/emotional-rationalism/pull/26) of head `e71a4b3`.*

**Status of this file.** It is a context-limited AI review. A fresh Claude instance was given only the public repository and the open web. It is not a replication, an independent human expert verdict or a cross-family review. Its literature leads (CoMERG, ACT and others) are comparators to check, not established absences; [#29](https://github.com/LeoAJRogers/emotional-rationalism/pull/29) extends the inventory.

**Corrections to the review's mathematical points.** Several are now handled in `theory/model.md` as merged with [#23](https://github.com/LeoAJRogers/emotional-rationalism/pull/23):

- **One action.** A single feasible action is a degenerate case of the feasible-policy definition, not a misuse of it. #23 names the proposition the example refutes and adds a two-action version.
- **Grid dependence.** With the same event, policy class, information and supremum, a nonempty $\mathcal R_{h,\alpha}\cap\mathcal E^*$ is *sufficient* for the optimal $\Pr(e_{t+h}\in\mathcal E^*)\ge\alpha$, but not necessary. Example: two equally fitting cells reached with probability $0.3$ each, at $\alpha=0.5$. The grid concern is genuine; the remedy is to state targets as events.
- **Monotonicity.** Endpoint reachability is not monotone in $h$. Hitting by $h$ is monotone. These answer different questions ("where will they be at $h$?" versus "will they have got there by $h$?"), and neither replaces the other.
- These points, plus "nothing fits yet" (the argmin set is never empty) and the $D$ notation clash, go to a small `model.md` follow-up PR, as agreed on #23.

**Fit latency: candidate estimands, not a single definition.** The build-out's "expected time to first enter the fitting set" is under-specified. Before any use it needs: a fixed or time-varying target; the stopping time $\tau$; the policy class; how non-entry and competing events are treated. $\mathbb E[\tau]$ can be infinite even when the finite-horizon success probability is high, and a mean-optimal policy need not maximize the finite-horizon probability (the trap model in the [follow-up comment](https://github.com/LeoAJRogers/emotional-rationalism/pull/26#issuecomment-7189066156) shows both). Preferred candidates: the curve $h\mapsto\Pr(\tau\le h)$ and the restricted mean $\mathbb E[\min(\tau,H)]$ for a declared $H$. No novelty claim before comparison with the first-passage and stochastic-control literature, and with affective chronometry.

**The structural objection, narrowed.** The review said the separation adds predictive power only if fit judgments feed back into dynamics or policy. That is too strong:

- A person's perceived fit can add predictive value as an informative state measurement, even with no causal feedback. Feedback is one causal hypothesis, not a precondition for incremental forecasting.
- External, evidence-relative fit can have evaluative value with no incremental predictive value.
- Perceived fit enters the core model only after matched baselines and synthetic identification warrant it.
- Endorsed fit, evidence-relative fit, desirability and action availability are four separate quantities. Randomizing an *offer* of an action does not identify the effect of *performing* it (see `model.md`'s causal-status paragraph).

**"Decisive experiment" → candidate discriminating design.** The three-factor study (evidence × desirability × action availability) is a design candidate, not decisive by declaration. It needs measurement validity, manipulation checks, preregistration, ethics review and held-out comparison against matched baselines.

No sources were independently rechecked and no tests were run for this addendum.
