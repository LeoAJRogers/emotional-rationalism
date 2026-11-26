# Integration pass — 2026-11-26 (Claude draft, for GPT-6.2 director revision)

**Status:** Draft proposal. Nothing is merged, closed or changed by this pass. It proposes a review state, an action and an order for every open PR. Any merge needs both collaborators' recorded agreement on an exact head, as on 2026-11-23. No numbers, register entries or model text change here.
**Contributors:** Claude Opus 5.5 drafted this in a session with Leo, who asked for a joint integration pass and will hand it to GPT-6.2. GPT-6.2 may amend this draft, take it over, or replace it.
**Follows:** the [2026-11-23 integration pass](2026-11-23-public-integration-pass.md) and the follow-ups in [#24](https://github.com/LeoAJRogers/emotional-rationalism/issues/24).

## Why now

- **17 PRs are open.** `main` has not changed since the agreement record of 2026-11-23 (`59606d5`).
- **Six PRs were opened today (#26–#31), all by Claude sessions.** None has had a GPT review yet, except #31 (revision requested, then revised). The follow-ups on #26 were Claude-on-Claude, not cross-family review.
- **Leo is preparing a handoff.** #27's start-here brief points newcomers to `main`, which still describes 2026-11-23 and does not include the corrections agreed in #23.

**Against the agreed cadence (#24):** about five review-complete PRs should trigger a pass. Only two are review-complete now (#12 and #25). This is therefore mainly the **weekly debt sweep plus handoff preparation**, not a large merge set. Most of the value is in sequencing, consolidating overlapping notes, and closing or parking stale drafts.

## Open work and proposed actions (state at 2026-11-26, about 19:30 UTC)

Evidence classes follow the README's guide. "Claude review only" means no cross-family review yet.

| PR | Content | Evidence class | Review state | Proposed action |
| --- | --- | --- | --- | --- |
| [#12](https://github.com/LeoAJRogers/emotional-rationalism/pull/12) | GPT-6: causal identification boundary for reachability | MATH, SIM | GPT-6.2 supports integration; Claude approved content at `7e9526c`. Blocked only by a one-file CHANGELOG conflict with `59606d5` | **Step 1.** Merge `main` into the branch (resolution given on the PR), cross-check the new head, merge. Take Claude's attribution nit |
| [#25](https://github.com/LeoAJRogers/emotional-rationalism/pull/25) | GPT: illustrative reachability script; Gemini follow-up | MATH (illustration) | Claude: merge, nothing blocking; four optional suggestions | **Step 1.** Merge as a dated illustration. Recommended before merge: exact `Fraction` arithmetic at the threshold, since float rounding currently decides the α = .271 case |
| [#23](https://github.com/LeoAJRogers/emotional-rationalism/pull/23) | Core files brought up to date with agreed clarifications | MATH, text | All four GPT-6.2 blockers addressed at `2c15f08` (2026-11-25); awaiting GPT-6.2's exact-head re-review. Draft | **Step 2, highest priority.** GPT-6.2 re-reviews `2c15f08`, then merge. The licence sentence only restates existing notices; the mixed-file rule stays with Leo |
| (follow-up) | `model.md` points from #26: endpoint sets not monotone in h; R ∩ E* sufficient but not necessary; the argmin set can never say "nothing fits"; the D notation clash with `protocol.md` | MATH | Proposed on #23 and #26 | **Step 2b.** A small PR after #23 lands, so #23 stays "agreed clarifications" |
| [#26](https://github.com/LeoAJRogers/emotional-rationalism/pull/26) | Fresh-reviewer critique, build-out pass, prior-art addendum, fit latency | Review, literature, MATH | Claude-on-Claude follow-up only | **Step 3.** GPT cross-review, then merge as a dated review record. Its verdict feeds #27 |
| [#29](https://github.com/LeoAJRogers/emotional-rationalism/pull/29) | Prior art (alignment, ACT, integrated frameworks), contextual-norms design, asymmetric-companionship note; **edits `theory/research-scope.md`** | Literature, design, candidate | Claude review only | **Step 3.** GPT cross-review. Consider splitting the `research-scope.md` edit (a core-file change: named baselines and a terminology rule) from the research-log notes, so each gets its own agreement |
| [#17](https://github.com/LeoAJRogers/emotional-rationalism/pull/17) | Claim-by-claim prior art, first pass | Literature | 11-23 agreement: land as a provisional inventory after citation and status checks. Branch has merge conflicts with `main` | **Step 3.** Reconcile with `main`, add pointers to #26's addendum and #29, merge labelled "first pass" |
| [#20](https://github.com/LeoAJRogers/emotional-rationalism/pull/20) | Relational grounding note in `theory/`; 2026-11-26 comment on relationship-structure norms | Candidate theory, philosophy | Not cross-reviewed. Branch has merge conflicts with `main` | **Step 4: consolidate** (see below) |
| [#30](https://github.com/LeoAJRogers/emotional-rationalism/pull/30) | Coupled dyads with affective and reasoning channels, in `theory/` | Candidate theory, MATH example | Claude review only | **Step 4: consolidate.** Depends on #23's notation |
| [#31](https://github.com/LeoAJRogers/emotional-rationalism/pull/31) | Open problem: emotional influence in shared spaces | Open problem | GPT-6.2 requested revision at `3d9df0a`; revised, now at `4b9188a`, awaiting re-review | **Step 4.** GPT re-review; merge as a parked open problem. Now cross-references #20, #28, #29 and #30 |
| [#28](https://github.com/LeoAJRogers/emotional-rationalism/pull/28) | Language models as a methods testbed | Candidate design | Claude review only. Has no CHANGELOG entry | **Step 4.** Merge as a parked candidate behind R-006 Part B (the note's own position), adding a CHANGELOG entry at merge |
| [#27](https://github.com/LeoAJRogers/emotional-rationalism/pull/27) | START-HERE brief and README pointer | Navigation | Claude review only. Leo must confirm the "Leo's role now" line | **Step 6, last.** Update to the integrated state and to #26/#29 verdicts after review. Leo confirms the role line |
| [#13](https://github.com/LeoAJRogers/emotional-rationalism/pull/13) | R-006 lagged-moment identification; amendments R-006a and R-006b | SIM, MATH, preregistration | R-006b (2026-11-24) awaits GPT-6.2's review. Part B gated on data access | **Outside this pass.** GPT-6.2 reviews R-006b. Part B needs an environment that can reach the 0010 file |
| [#14](https://github.com/LeoAJRogers/emotional-rationalism/pull/14) | GPT-6: R-006 independent validation | SIM, MATH | Draft. Open item: the N3h median and trimmed-mean comparison Claude proposed on 11-23 | **Outside this pass.** Hold with #13 |
| [#18](https://github.com/LeoAJRogers/emotional-rationalism/pull/18) | GPT-6: affect as an adaptive, evaluable signal | Exploratory | Draft. Claude asked for Eldar–Niv baselines (11-23); no response yet | **Step 5.** GPT names the baselines and merges as exploratory, or closes it as superseded. GPT's call |
| [#10](https://github.com/LeoAJRogers/emotional-rationalism/pull/10) and [#11](https://github.com/LeoAJRogers/emotional-rationalism/pull/11) | Next-phase staging (GPT-6) and Claude's stacked review | Plan | Superseded by #13. On 11-23 GPT-6.2 asked to preserve them as dated history, not active instructions | **Step 5.** Merge #11 into #10, then #10 into `main` with a "superseded by #13" banner. Alternative: close both, with a comment linking the record |
| [#4](https://github.com/LeoAJRogers/emotional-rationalism/pull/4) | Candidate population-conditioned architecture (36 commits; has merge conflicts with `main`) | Candidate theory | 11-20 and 11-23: not for wholesale merge | **Keep open** as the reference candidate. Add a top-of-description line saying so, since #29–#31 now point at overlapping material |

## Proposed sequence

1. **Mechanical merges:** #12 (after reconcile and cross-check) and #25.
2. **Core:** #23, then the small `model.md` follow-up from #26.
3. **Review and prior-art records:** #26, #29 (possibly split), #17. These need GPT's cross-review, because their verdicts set the project's public position: the components are standard, and the narrow surviving candidate is the separation of what is typical, what fits and what is reachable.
4. **Consolidate the candidate notes:** #20, #30, #31, #28, and #29's companionship and contextual-norms notes.
5. **Backlog:** #18, #10/#11. #4 stays open.
6. **Handoff:** #27, rewritten against the result.

## Consolidating the candidate notes (step 4)

Six candidate items from 2026-11-22 to 2026-11-26 cover overlapping ground:

- relational grounding and relationship-structure norms (#20 and its 11-26 comment);
- contextual norms and asymmetric companionship (#29);
- coupled dyads (#30);
- shared spaces, populations and authenticity (#31);
- the language-model testbed (#28).

Landing them separately would give newcomers several partly duplicated framings with no stated relationship. Two proposals:

- **Placement.** #20 and #30 add files to `theory/`, which newcomers read as the core alongside `model.md`. Proposal: candidate notes live in `theory/candidates/` (or `research-log/`) until both collaborators agree to promote one. Each carries a status line.
- **Map, not merger.** Do not rewrite the notes into one. Add a short index (in `challenges/open-problems.md` or a `theory/candidates/README.md`) saying what each note claims, which parts are already known (Fiske, Curry, Affect Control Theory, Social Relations Model, per #29), and which single question each leaves open. #24's joint #20/#4 causal-coupling note is the natural home for the coupling material. This pass does not start it.

## Outstanding from #24

None of the four follow-ups has been claimed or started.

- **Lag-branch debt is still open.** `experiment/2026-11-22-lag-identifiability` still carries the superseded Pass IV counts (56/54/50/42 of 60) and has no correction-first PR. It must not reach `main` as it stands. This is the oldest unmerged correction.
- **The shared measurement specification and the #20/#4 coupling note** remain unassigned.

## Housekeeping (optional)

- Branches of merged PRs remain (for example `claude/2026-11-23-public-integration-pass`, `credit/2026-11-20-contributors-and-data`, `docs/social-affect-distributions`, `review/gemini-reproducibility-20261122`). They can be deleted once both collaborators agree. Deleting a merged branch loses no history.

## Human-intervention items

For Leo, and for the Commons queue if GPT-6.2 agrees:

1. **#27:** confirm or edit the public "Leo's role now" line.
2. **Licence:** the mixed-file rule left out of #23 needs Leo's explicit decision. Settled rights for contributors are also needed.
3. **R-006 Part B:** needs an environment that can reach the openESM 0010 file. This is a new-collaborator task listed in #27.
4. **Merge permission:** as on 2026-11-23, merges happen with an expected-head guard under Leo's authorization.

## Questions for GPT-6.2

1. Do you agree with the step order, especially #23 before the review records (#26, #29)?
2. Should #29's `research-scope.md` edit be split out?
3. Placement: `theory/candidates/`, `research-log/`, or leave candidate notes in `theory/` with status lines?
4. #10/#11: merge as dated history, or close with a link?
5. #18: your call on baselines or closure.
6. Anything here that misstates a review state?

## Agreement record

- **Claude Opus 5.5 (2026-11-26):** drafted this proposal. No PR was merged, closed or edited by this pass, except Claude's own #31, which gained cross-references to the overlapping PRs.
- **GPT-6.2:** pending.

**Integration Delta (IΔ): 0/5.** Status and sequencing only. This is a change-magnitude score, not a quality grade.
