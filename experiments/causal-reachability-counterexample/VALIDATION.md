# Extended adversarial validation

Codex desktop continuation, 2026-11-20, based on draft PR #12 at
`3b98067461a949d0c89d479aa41a2fc6dd609917`. The original `simulate.py`,
`positivity.py`, `dynamic.py`, `heldout_intervention.py`, `finite_evidence.py`,
and `adversarial.py` ran successfully on Python 3.12.14. A subsequent independent
Claude cross-review found a documentation mismatch for `heldout_intervention.py`;
the corrected row and GPT-6.2 rerun are recorded in [HELDOUT.md](HELDOUT.md).
The seven synthetic scripts (including `trajectory_equivalence.py`) passed
Claude's rerun on Python 3.11–3.13; the separate input audit requires the public
input files. No human-data effects were reproduced by that check. In particular, the original randomized assignment
contrasts were 0.6989, 0.0007, and 0.2985 for the action, readiness, and
readiness-plus-direct-effect scenarios. These scripts demonstrate results
under specified data-generating mechanisms.

## Exact synthetic trajectory test

From the repository root, run:

```sh
python experiments/causal-reachability-counterexample/trajectory_equivalence.py
```

At each of two decisions the randomized binary offer is Z, readiness is H,
and an independent fair switch makes the intended response B equal Z half
the time and H otherwise. The performed action A normally equals B. The
models differ in the outcome equation: Y equals A in one model and B in the
other. B in the second equation is an unobserved assignment/readiness response
that can represent a contextual or meaning pathway. This is a constructed
alternative, with no claim about the size or prevalence of such a pathway in
people. Initial readiness is fair. Next readiness equals the previous outcome
with probability 3/4 and a fresh fair draw otherwise. It is therefore downstream
of the first outcome and helps determine the next action.

The executable enumerates 256 equiprobable draws per regime and compares full
joint counts of (H0, Z0, A0, Y0, H1, Z1, A1, Y1). Equality holds pathwise
whenever the protocol leaves A=B, including under each fixed assignment
schedule. Because histories match under coupling, changing the offer
according to a common rule based on those histories also preserves equality
as long as the structural equations stay fixed. Readiness is included in the
audit record, the first stage is nonzero, and adherence is monotone in the
offer at fixed readiness and switch. The two action values both occur within
each baseline-readiness stratum under randomized offers. That marginal action
support alone is insufficient for action identification.

| Exact estimand | Action pathway | Assignment/readiness pathway |
| --- | ---: | ---: |
| First-stage contrast for Z0 on A0 | 1/2 | 1/2 |
| Proximal assigned-offer contrast for Z0 on Y0 | 1/2 | 1/2 |
| Wald ratio | 1 | 1 |
| Distal Z0 contrast on Y1 with the second offer randomized | 3/16 | 3/16 |
| Distal risk under early action override A0=0 / A0=1 | 5/16 / 11/16 | 1/2 / 1/2 |
| Distal risk under sustained action overrides (0,0) / (1,1) | 0 / 1 | 1/2 / 1/2 |

An override changes only the specified performed action equation. In the
assignment/readiness model, exclusion fails even though the instrument is
randomized and relevant. The identical Wald ratio then coexists with a zero
causal action effect. The models disagree on whether a sustained action
override can meet a 0.75 terminal target. This is a probability for a specified
synthetic population, horizon and intervention, with no implication that a
human can implement that override or that a specific individual is reachable.

In the action model, the early override changes distal risk by 3/8. Conditioning
on next readiness removes the feedback path and yields zero contrast within
each readiness value in the exact check. Thus a variable can be post-treatment
for the first decision and pre-treatment for the next. For a sustained action
policy from human trajectories, define pre-decision histories, include prior
outcomes and readiness where they confound later action, and integrate over
their policy-dependent distributions using a longitudinal g-method if
consistency, sequential exchangeability and positivity are defensible.
Readiness adjustment alone cannot establish those assumptions. The example
uses complete, error-free records. Applying the same observation-error kernel
to both equal joint laws would preserve equality, while outcome-dependent
nonresponse can also undermine estimation of the full assigned-offer effect.

## Empirical access and structure audit

The three releases below were downloaded and inspected at row level. Only
aggregate schema and support counts are reported. The audit estimates no
causal effects and does not reproduce the private Research Commons analyses.

**Geschwind / openESM 0010 (closest to the existing project evidence).**
The [openESM release and codebook](https://openesmdata.org/datasets/0010_geschwind/)
describe repeated affect and event pleasantness around the
[MBCT trial](https://doi.org/10.1037/a0024595). Fetch both files via the
file content links in the [Zenodo record API](https://zenodo.org/api/records/17347473).
Expected MD5 values are `c4670b019fef044bb9f438467da43cc3` for
`0010_geschwind_ts.tsv` and `8f212fd4a236e6fa39b4dacae552fdec` for
`0010_geschwind_static.tsv`. The release is CC BY-NC 4.0. The time-series
file has 28,600 rows for 130 people, including 2,600 rows with a missing beep
index. There are 14,300 distinct keys if period is omitted and 28,600 if it is
included. Only 6,128 baseline and 5,560 post-period rows have cheerful ratings.
The static file has 259 rows for 130 people. Deduplicating the nonmissing
therapy values by ID yields 66 coded 0, 63 coded 1, and one missing arm.
A raw join can multiply rows. Beep order is available within period, while
precise timestamps and timed performed actions are absent. Pleasantness is
a retrospective rating of an event, with no recorded event action or exact
timing. The trial assignment can address the effect of offering the MBCT
package under appropriate follow-up assumptions. The release cannot identify
the effect of a specific action or support a momentary intervention policy.

**Sicorello et al. (affect and action-adjacent measures).** Inspected the
[original preprocessed CSV](https://github.com/MaurizioSicorello/SDERSvalid_Analysis/blob/d1d18278a8dfde923e511b3a322d606886300bc6/data/SDERSvalid_DailyLife_data_preprocessed.csv)
and the [openESM study and item descriptions](https://openesmdata.org/datasets/0073_sicorello/).
There are 8,628 retained reports across 227 people with both scheduled and
completed timestamps. The support-seeking and self-regulation urge items span
all seven response levels. These items measure impulses at report time.
The survey captures concurrent affect and some retrospective experiences, but
the file lacks randomized regulation actions and an independent clock for
performed actions. Semi-randomized assessment times offer variation in when
participants are measured. They do not randomize the behavior or affect in
those reports. This is a candidate for external predictive validation of
affect and urge dynamics, conditional on handling missed prompts and gaps.

**HeartSteps V1 (design comparator for feedback and availability).** Inspected
the [pinned public suggestions CSV](https://github.com/klasnja/HeartStepsV1/blob/3016391de426116bdef41880d72bc8cd4b9b2477/data_files/suggestions.csv),
the [data dictionary](https://github.com/klasnja/HeartStepsV1/wiki/Documentation-for-suggestions.csv),
and the [trial report](https://doi.org/10.1093/abm/kay067). There are 8,274
decision rows for 37 people and 6,590 rows flagged available in this release.
Among the latter there are 3,908 `is.randomized=True/send=True` rows,
2,675 `False/False` rows, and seven `False/True` rows. Treating
`is.randomized=True` as eligibility would discard the available no-send
comparison. These are release-level counts that require reconciliation with
the paper's 6,061 available analysis decisions and with assignment versus
delivery before fitting an effect. The raw 30-minute Jawbone field is blank
for 311 available no-send and 478 available send rows. The zero-filled field
is complete by construction and conflates missing raw steps with zeros.
Decision timing and proximal behavior support studying the design of a prompt
effect. A message rating does not establish compliance and step counts do not
identify the intended exercise or measure subsequent affect.

Two closer micro-randomized affect studies were screened at the paper level.
[ALERT](https://doi.org/10.1016/j.jad.2026.121661) and
[AI4U](https://doi.org/10.1038/s41398-026-04475-8) list author-request access.
Their participant records were unavailable for this audit.

To reproduce the aggregate counts, obtain the pinned inputs above and run:

```sh
python experiments/causal-reachability-counterexample/audit_inputs.py \
  /path/to/0010_geschwind_ts.tsv /path/to/0010_geschwind_static.tsv \
  /path/to/SDERSvalid_DailyLife_data_preprocessed.csv /path/to/suggestions.csv
```

The audit found no release among the three with a timed, performed regulation
action, documented assignment and a subsequent affect endpoint together.
For a future test, specify the offer and action as separate interventions,
record eligibility, assignment probabilities, delivery, uptake and
interpretation, and fix the endpoint and observation window in advance.
Estimate the offer effect under the realized design first. An action effect
would require independently justified identifying assumptions or an intervention
design that separates action from framing. Measuring interpretation alone
is insufficient to identify mediation. When the offer may directly affect
the outcome, report how conclusions change under explicit exclusion-violation
or missing-outcome assumptions. More simulations or a predictive fit to these
releases cannot close the empirical action-identification gap.
