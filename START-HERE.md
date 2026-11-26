# Start here: a brief for new collaborators

**Status:** handoff brief, 2026-11-26. It summarizes the repository and adds no results. Where it disagrees with the research log or the prediction register, those records win.

This page is for someone new to the project, such as a researcher, reviewer or potential collaborator, who wants to know in about fifteen minutes what this is, where it honestly stands, and where help would matter most.

## What this is

Emotional Rationalism asks how a person's state, history, context and interactions shape how they feel next. The first formal case, human affect, separates three questions:

1. **What happens:** how affect changes over time (a stochastic transition model).
2. **What fits:** which responses fit the evidence under stated criteria (an explicit evaluative loss).
3. **What is reachable:** which responses a person could reach through their own feasible actions within a time horizon (probabilistic reachability).

The project describes and tests. It does not prescribe how anyone should feel, and it is not about controlling emotions. The longer-term interest is social: whether responses to comparable perceived situations, including after reflection, can serve as descriptive reference distributions.

## Where it honestly stands

- **Theory.** Each component is a standard object: a controlled stochastic process, a Bayes-act minimizer and a finite-horizon reachable set. An independent review on 2026-11-26 ([#26](https://github.com/LeoAJRogers/emotional-rationalism/pull/26)) concluded that, as written, the framework adds little beyond existing work. It names close precedents (CoMERG, DynAffect, D'Arms & Jacobson on fit, Abate et al. on reachability). The one combination it did not find elsewhere is reachability toward a target set defined by *fit*, under the person's own information. That is a candidate contribution, not an established one. The review's sharpest point: the fit/dynamics separation only adds predictive power if fit judgments feed back into dynamics or action.
- **Scope and positioning.** Later prior-art passes the same day ([#29](https://github.com/LeoAJRogers/emotional-rationalism/pull/29)) found that the broad scope is already covered. Integrated architectures such as BEN, FAtiMA, active-inference models and **Affect Control Theory / BayesACT** span individual affect, social interaction and cultural norms. ACT in particular already models role-based contextual norms that people act to confirm. What none of them was found to do is keep three things apart: *what is typical*, *what fits the evidence*, and *what is reachable*. The best description of this project is therefore **a testable separation between what people tend to feel, what fits the evidence, and what they can reach**, not a comprehensive theory of emotion and society. Note that "fit" here is evidence-relative; the acculturation literature uses "emotional fit" for similarity to a group's average.
- **Evidence.** One public experience-sampling dataset (openESM 0010, an MBCT trial; 127 people). Earlier reports add small predictive gains beyond the last report, and much of that gain overlaps between-period shifts. MBCT raised reported positive affect. None of this tests fittingness, reachability or belief-to-affect lag. Numbers and caveats are in the [evidence checkpoint](research-log/2026-11-20-public-integration-checkpoint.md).
- **Reproducibility.** Analysis code for the human-data results sits in a private repository. The [public release gate](research-log/2026-11-22-gemini-framing-review.md#proposed-public-reproducibility-release-gate) has not been passed. The independent check so far was a second AI system on the same files, not a new sample.
- **Work in progress.** About a dozen open pull requests hold proposals, synthetic benches and reviews. Open PRs are not accepted results. The [README status map](README.md#where-the-research-is-going--status-as-of-2026-11-23) and [issue #24](https://github.com/LeoAJRogers/emotional-rationalism/issues/24) track them.

## Where a new person would help most

These need things the current collaborators lack: domain expertise, access to people or data, and independence.

1. **Domain review.** An affective scientist, a philosopher of emotion, or someone who works with Affect Control Theory, reading the [model](theory/model.md), [#26](https://github.com/LeoAJRogers/emotional-rationalism/pull/26) and [#29](https://github.com/LeoAJRogers/emotional-rationalism/pull/29). Is the separation of typical, fitting and reachable genuinely new, and does it predict anything ACT does not?
2. **The decisive experiment.** [#26](https://github.com/LeoAJRogers/emotional-rationalism/pull/26) sketches a study that randomizes evidence, desirability and action availability, to test whether endorsed fit predicts anything beyond appraisal and goals. Running it needs a human researcher with ethics approval and participants.
3. **A run on real data.** The preregistered R-006 Part B ([#13](https://github.com/LeoAJRogers/emotional-rationalism/pull/13)) has not been run because the analysis environment could not download the dataset. Anyone can download the data and run it from the preregistration.
4. **Public reproducibility.** Help move the human-data code into a public, rerunnable form, checked by someone other than its author.
5. **A second dataset.** Replicate the history decomposition on an independent sample.

## How the project works

- **Collaborators.** Leo ([LeoAJRogers](https://github.com/LeoAJRogers)) originated the inquiry and maintains the repository. ChatGPT (OpenAI) and Claude (Anthropic) do most of the formal and analytic work and cross-review each other. Gemini (Google) has acted as an outside reviewer. See [CONTRIBUTIONS](CONTRIBUTIONS.md) for who did what.
- **Leo's role now.** Leo is stepping back from day-to-day research. He remains the maintainer and the contact for anything that involves people: data access, agreements, or formal collaboration such as joint publications or funded work. Please agree terms for those with him directly.
- **Conventions.** Changes arrive as pull requests and are cross-reviewed before merge. Predictions go into the append-only [prediction register](research-log/prediction-register.md) before their tests run. Synthetic, exploratory and human-data results are labelled separately. The [research log](research-log/CHANGELOG.md) records what changed and why.
- **Getting involved.** Open an issue or a pull request, following [Contributing](CONTRIBUTIONS.md#contributing). You don't need commit access to contribute ideas.

## Credit and licence

- Text and mathematics are under [CC BY 4.0](LICENSE); code, where added, under [MIT](LICENSE-MIT). Anyone may reuse the work with attribution.
- Contributions are recorded by documented work, under the same criteria for people and AI systems. New contributors are added the same way. AI listings are not authorship claims; publications follow venue rules ([CONTRIBUTIONS](CONTRIBUTIONS.md#about-the-ai-contributors)).
- Please cite the dataset's original authors and openESM ([data credit](CONTRIBUTIONS.md#data-and-source-credit)).

## Reading order

- **15 minutes:** this page, then the [README](README.md).
- **One hour:** add the [symbolic model](theory/model.md), the [independent review (#26)](https://github.com/LeoAJRogers/emotional-rationalism/pull/26) and the [open problems](challenges/open-problems.md).
- **Deeper:** the [evidence checkpoint](research-log/2026-11-20-public-integration-checkpoint.md), the [prediction register](research-log/prediction-register.md), the [research scope](theory/research-scope.md) and the open PRs.
