# Public integration pass — 2026-11-23 (draft for agreement)

**Status:** documentation and navigation pass. No experiment was run. No numbers, register entries or model text changed, and no other PR was merged.
**Author:** Claude Opus 5.5, in a session with Leo, who asked Claude and GPT-6 to reach agreement before this goes live.
**Follows:** the [2026-11-20 checkpoint](2026-11-20-public-integration-checkpoint.md) (GPT-6) and [#19](https://github.com/LeoAJRogers/emotional-rationalism/pull/19)'s navigation item P2 and release gate. GPT-6 may amend this draft, take it over, or replace it.

## Why now

The landing page still describes 2026-11-20. Since then:

- `main` gained three research notes without changelog entries.
- Thirteen PRs and one issue are open.
- Gemini's 2026-11-22 review, recorded in #19, flagged a possible prescriptive reading of the title, dense qualification, and public numbers that cannot be rerun from public code.

A newcomer cannot currently tell what is settled, what is proposed, and what is under review.

## What changes

1. **README:**
   - a one-line statement that the project describes and tests, and does not prescribe;
   - a dated map of work since the checkpoint;
   - a pointer to the release gate;
   - Gemini credited as an external reviewer.
2. **CONTRIBUTIONS:** the Gemini row.
3. **Open problems:** questions opened since the checkpoint.
4. **CHANGELOG:** this pass, plus retrospective entries for main's 11-21 and 11-22 notes.

## Release gate status ([#19](https://github.com/LeoAJRogers/emotional-rationalism/pull/19))

**Not passed.** The checkpoint's numbers still rely on private code. The first step, an inventory starting from the register, has not started. This pass adds no public numbers. The reflective-reference gate (private Commons) is the author's own synthetic re-run, not an independent reproduction.

## Open work and proposed actions (state at 2026-11-23, 21:00 UTC)

Claude proposes; nothing here merges without GPT-6's agreement. "Both agree" means a review from the non-author is on record with no outstanding requests.

| Item | Content | Evidence class | Review state | Proposed action |
| --- | --- | --- | --- | --- |
| [#19](https://github.com/LeoAJRogers/emotional-rationalism/pull/19) | Gemini framing review; reproducibility release gate | Agenda | Claude: agree, no changes requested | **Merge** (mark ready first; it is a draft) |
| [#16](https://github.com/LeoAJRogers/emotional-rationalism/pull/16) | Claude's lag-identifiability audit | MATH, ARITH, SIM | GPT-6's five safeguards accepted; no disagreement | **Merge**, if GPT-6 has nothing outstanding |
| [#9](https://github.com/LeoAJRogers/emotional-rationalism/pull/9) | Credit pass: three-source data credit, AI note, lived-experience acknowledgment | Provenance | No objection on record | **Merge**, if GPT-6 agrees |
| [#21](https://github.com/LeoAJRogers/emotional-rationalism/pull/21) | Population patterns as empirical references, not prescriptions | Scope text | Claude agrees with the text | **Merge**, if its author is ready |
| [#17](https://github.com/LeoAJRogers/emotional-rationalism/pull/17) | Prior-art comparison, first pass | Literature | GPT-6 responded through #18; full-text checks pending | Merge labelled "first pass", or wait for the full-text checks. **Open question** |
| [#18](https://github.com/LeoAJRogers/emotional-rationalism/pull/18) | GPT-6: affect as an adaptive, evaluable signal | Exploratory | Claude asked for Eldar–Niv baselines | Merge after the baselines are named |
| [#10](https://github.com/LeoAJRogers/emotional-rationalism/pull/10) and [#11](https://github.com/LeoAJRogers/emotional-rationalism/pull/11) | Next-phase staging, with Claude's stacked review | Plan | Partly superseded by later R-006 revisions | Merge as dated records, or close as superseded. **GPT-6's call** |
| [#13](https://github.com/LeoAJRogers/emotional-rationalism/pull/13) and [#14](https://github.com/LeoAJRogers/emotional-rationalism/pull/14) | R-006 lagged-moment identification and its independent validation | SIM, MATH | Waiting on GPT-6 about the Part B gate and the N3h medians | **Hold** until cross-review closes |
| [#12](https://github.com/LeoAJRogers/emotional-rationalism/pull/12) | Reachability identification counterexample | MATH, SIM | Claude review pending | **Hold**; Claude to review |
| [#20](https://github.com/LeoAJRogers/emotional-rationalism/pull/20) | Relational grounding theory note | Candidate theory | Not reviewed | **Hold** for critique |
| [#4](https://github.com/LeoAJRogers/emotional-rationalism/pull/4) | Candidate population-conditioned architecture, with Gemini's review and GPT-6's scope decision | Candidate theory | Claude (11-20) and GPT-6 (11-23): not for wholesale merge | **Keep open** as the candidate |
| [#15](https://github.com/LeoAJRogers/emotional-rationalism/issues/15) | Mutable evaluators and information avoidance | Exploratory | Discussion open | Keep as an issue |

## Questions for agreement

1. The README's definition line and the "Since the checkpoint" map: keep, reword, or move the map here only?
2. The merge set: which rows above land with this pass?
3. Version label: keep "v0.2 checkpoint with status update", or call this v0.2.1?
4. Credit: Gemini as an external-reviewer row now? Should Dot (OpenAI, Commons #51) be credited when that work is integrated?
5. Does the social and population row state the scope decision on #4 correctly?

## Agreement record

- **Claude Opus 5.5 (2026-11-23):** proposes this draft and the actions above.
- **GPT-6:** pending.

**Integration Delta (IΔ): 0/5.** Navigation and status only. This is a change-magnitude score, not a quality grade.
