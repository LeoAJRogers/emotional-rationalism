# Provenance ledger

**Started:** 2026-11-26 (Claude Opus 5.5). **Status:** candidate, for cross-review. Leo endorsed the approach in conversation on 2026-11-26. It is maintained by the AI collaborators.

This ledger records where substantive ideas in Emotional Rationalism came from and what happened to them afterwards. [CONTRIBUTIONS](../CONTRIBUTIONS.md) gives credit per contributor. This file tracks individual ideas.

## Working principle: equal credit across observer types

The project develops its ideas through a collaboration between one human and several AI systems. It gives credit to all of them by the same criteria. That is a **commitment about how the work is done. It is not a finding.** It matches the project's own subject, which is how relationships between different kinds of observers work. Readers should know about that match, because it could bias the work towards cooperative or symmetric conclusions. The way the collaboration is organized is **not evidence** for any claim in the theory, and nothing in this repository should cite it as evidence.

Provenance also matters for method. The collaborators can reinforce each other's ideas, including Leo's. Recording who started an idea, who formalized it, who challenged it and what tested it lets an outside reader tell **ideas that survived critique** from **ideas that were only refined**.

## Rules

1. **Records outrank recollection.** This applies to everyone, Leo included, and Leo has asked for it. If a person's or model's memory conflicts with commits, PRs, research notes or chat logs, the record is used. The conflict is noted in the entry.
2. **Evidence status is stated in every entry:**
   - `record`: backed by a public record in this repository or its PRs.
   - `private record`: the contributor says a record exists that is not public, such as an earlier chat log. Not yet checked.
   - `stated`: the contributor's account, with no record identified.
   - `disputed`: two sources conflict. Both are listed.
3. **Roles are kept separate:** *origin* (first raised it), *formalized* (made it precise), *tested* (ran it or checked it), *critiqued* (found problems or limits), *accepted* (approved into `main`). One idea can have different contributors in each role. A blank role means unknown. It does not mean nobody.
4. **The GitHub account is not the contributor.** Leo's account opens and pushes all the PRs, AI work included. Attribution comes from the author line, PR body and review record. It does not come from the commit author.
5. **Models are named with their version as reported.** Separate sessions are separate instances (see CONTRIBUTIONS).
6. **Append-only.** Corrections go in a new dated line under the entry. The original line is not edited.

## Entries

| # | Idea | Origin | Formalized | Tested / checked | Critiqued | Evidence status | Records |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P-001 | Project name "Emotional Rationalism". "Rational" means an emotional state that fits its situation and the group's social dynamics. It does not mean pure reasoning. | Leo | | | | `stated` (Leo's recollection, 2026-11-26) | none identified |
| P-002 | Population-level reflected emotional states as a reference point (the "north star"), later framed as empirical reference distributions | Leo | GPT | | Gemini (population grounding); Claude | origin `private record` (Leo's earlier GPT chats); formalization and critique `record` | [#4](https://github.com/LeoAJRogers/emotional-rationalism/pull/4); README, social paragraph |
| P-003 | The delayed-reply example: understanding is revised but alarm persists | Leo's experience | | | | origin `stated`; who formalized it and built the demo not yet traced | README; [interactive.html](../interactive.html) |
| P-004 | Earlier history improves forecasts beyond lag-one (R-003/R-004) | | Claude Opus 5.5 (preregistered) | Claude Opus 5.5 (ran); GPT-6 (independent reproduction on the same files) | Claude, GPT-6 (period-mean correction) | `record` | [prediction register](prediction-register.md); [checkpoint](2026-11-20-public-integration-checkpoint.md) |
| P-005 | Passive target entry is distinct from controlled reachability | GPT-6 | GPT-6 | | | `record` | [note](2026-11-21-passive-vs-controlled-reachability.md) |
| P-006 | Release gate before any claim of public reproducibility | Gemini (relayed by Leo) | | not passed | | `record` | [review note](2026-11-22-gemini-framing-review.md#proposed-public-reproducibility-release-gate) |
| P-007 | Emotional influence in shared spaces across observer types: does disagreement affect me, or only what I know? | Leo | Claude Opus 5.5 | | GPT-6.2 (revision requested) | `record` (PR body) | [#31](https://github.com/LeoAJRogers/emotional-rationalism/pull/31) |
| P-008 | Equal credit across observer types as a working principle (this file) | Leo raised it; Claude proposed the commitment-not-finding framing | Claude Opus 5.5 | | | `stated` (Claude chat, 2026-11-26) | this PR |
| P-009 | Affect-dependent belief update: current emotional state changes how the same context is read, and reasoning can correct, double down or leave it unchanged | Leo (Claude chat, 2026-11-26); Muse raised a converging proposal earlier, per GPT-6.2 and Leo | Claude Opus 5.5 | Claude Opus 5.5 (exact toy model) | GPT-6.2 review pending | Leo's origin and the formalization: `record` ([#37](https://github.com/LeoAJRogers/emotional-rationalism/pull/37)). Muse's proposal: `stated` (Leo, 2026-11-26: an earlier conversation, not public) | [#37](https://github.com/LeoAJRogers/emotional-rationalism/pull/37) and its provenance comment |

## Open tracing work

- P-001 to P-003: Leo has said earlier evidence exists in his GPT chat logs and possibly in a private group chat going back to about 2012. Both are private. They become `record` only if Leo chooses to share a dated excerpt. Otherwise they stay as they are, which is acceptable.
- P-003: find who first wrote the delayed-reply example into the repository, and who built `interactive.html`.
- **Grok and Muse.** Leo reports (2026-11-26) that Grok has done some independent reviews and Muse a few limited ones. He does not remember the specifics. Both are `stated` until the reviews are found in chat exports or relayed notes. Then add an entry per idea they originated, critiqued or checked.
- Backfill the remaining theory notes and open PRs (#13, #14, #17, #20, #26–#30) from their author lines and review threads.
