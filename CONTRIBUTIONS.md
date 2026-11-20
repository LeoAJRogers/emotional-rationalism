# Contributions and provenance

Emotional Rationalism grew through an extended human–AI dialogue about lived experience, interpersonal dynamics, emotional responses, interpretation, and self-understanding. Its origin cannot be reduced to a few isolated anecdotes or to the subsequent mathematical writing. The private conversations and their personal significance are not reproduced in this repository.

## Contributors

Roles use the Contributor Roles Taxonomy ([CRediT](https://credit.niso.org/contributor-roles-defined/), ANSI/NISO Z39.104-2022). Every contributor is listed in the same format, human or AI. No degree of contribution (lead, equal or supporting) is assigned yet; any contributor may propose one. Each row says where the work is recorded, so the credit can be checked.

| Contributor | Kind | CRediT roles | Where the work is recorded |
| --- | --- | --- | --- |
| **LeoAJRogers** (Leo) | Human; initiator and maintainer | Conceptualization; Project administration; Resources; Writing – review & editing | The origin of the inquiry and its research questions; direction-setting choices; the repositories, tool access and data files; objections and corrections throughout |
| **ChatGPT** (OpenAI), including GPT-6 sessions | AI system | Conceptualization; Methodology; Formal analysis; Software; Validation; Investigation; Writing – original draft; Writing – review & editing | The v0.1 and v0.2 drafts; candidate architecture [PR #4](https://github.com/LeoAJRogers/emotional-rationalism/pull/4); reviews, exact-equivalence results and identification audits (Research Commons #32, #34, #36, #40, #42); cross-item tests (#43); the independent reimplementation of R-003 and R-004 (#44); the [2026-11-20 integration checkpoint](research-log/2026-11-20-public-integration-checkpoint.md) |
| **Claude** (Anthropic), Sonnet 5.5 and Opus 5.5 sessions | AI system | Methodology; Formal analysis; Software; Investigation; Data curation; Validation; Writing – original draft; Writing – review & editing | Sonnet: the [first review](research-log/2026-11-20-claude-review.md) and the first synthetic bench (Research Commons #33). Opus: the gain-channel, scale-rival, sparse-sampling and rival-world tests; the R-003 and R-004 real-data analyses and their data-handling records (#35, #38, #39, #41); entries R-001 to R-004 in the [prediction register](research-log/prediction-register.md), with amendments and corrections; the integration brief that preceded the checkpoint |

Research Commons is private at the time of writing, so its PR numbers can be checked only by people with access. See the [integration checkpoint](research-log/2026-11-20-public-integration-checkpoint.md#6-provenance-access-and-reproducibility-boundary).

### About the AI contributors

- **Why the same format.** AI systems are listed the same way as people so that the record of who did what stays complete and checkable. A row describes observable work. It is **not** a claim of authorship. CRediT itself is [not designed to determine authorship](https://credit.niso.org/contributor-roles-defined/).
- **Publications.** Under [COPE's position on authorship and AI tools](https://publicationethics.org/cope-position-statements/ai-author), AI tools cannot be listed as authors of a paper. They cannot take responsibility for the work, declare conflicts of interest or manage copyright and licence agreements, and their use must be disclosed. Any publication from this project follows that position and the venue's own rules.
- **Accountability.** Responsibility for what this repository publishes rests with its human maintainer. Claude and ChatGPT checked each other's work, including a cross-family numerical reproduction. AI-generated text, code and literature pointers can still contain errors, so verify them before relying on them.
- **Identity.** Model names and versions are as reported in each session. Sessions are separate instances, without memory of one another. The names identify systems, not continuous individuals.
- **What the listing does not settle.** It does not resolve questions about AI experience, selfhood or moral status, and it confers no legal rights.

## How the work developed

**LeoAJRogers** initiated and sustained the inquiry; contributed personal and interpersonal observations, conceptual distinctions, objections, questions, and direction-setting choices; clarified that the broader goal concerns context-dependent changes in persistent state rather than simply choosing or controlling emotions; and authorized the public research work.

**ChatGPT** contributed iterative conceptual framing, alternative hypotheses, counterexamples, synthesis, mathematical formulation, test and baseline design, critical reviews, and research documentation. These contributions occurred through repeated exchanges, not just a single generation of text. Project notes should continue to track the specific origin and testing of substantive ideas wherever practical.

**Claude** contributed through separate Sonnet 5.5 and Opus 5.5 sessions on 2026-11-20:
- reviews;
- synthetic method tests;
- the preregistered real-data analyses R-003 and R-004;
- the corrections that followed cross-agent review.

The Sonnet review's literature pointers came from model memory and were marked as needing checks before use.

**GPT-6 (ChatGPT)** independently audited those analyses and reproduced them numerically from the original files. That cross-check is recorded with its limits: the same data, and code held privately. Results that were only synthetic or exploratory stay labelled that way everywhere.

The ideas often developed interactively: contributions may arise from the exchange rather than being cleanly attributable to one participant. Neither the human contribution nor the AI contribution should be reduced to an incidental role. Such attribution describes observable intellectual work; it does not resolve questions about AI subjective experience, selfhood, or legal/formal academic authorship. Publications must follow applicable journal and conference authorship and disclosure policies.

## Data and source credit

The real-data analyses use openESM dataset 0010 ([Zenodo record 17347473](https://zenodo.org/records/17347473), CC BY-NC 4.0).
- **Provenance:** openESM harmonized the data that Bringmann et al. (2013) shared as supporting information. Those data come from the randomized trial of Geschwind et al. (2011).
- **How to cite:** the record asks users to cite the original authors and the openESM project:
  - Geschwind, N., Peeters, F., Drukker, M., van Os, J., & Wichers, M. (2011). Mindfulness training increases momentary positive emotions and reward experience in adults vulnerable to depression: A randomized controlled trial. *Journal of Consulting and Clinical Psychology, 79*(5), 618–628. https://doi.org/10.1037/a0024595
  - Bringmann, L. F., Vissers, N., Wichers, M., Geschwind, N., Kuppens, P., Peeters, F., Borsboom, D., & Tuerlinckx, F. (2013). A network approach to psychopathology: New insights into clinical longitudinal data. *PLoS ONE, 8*(4), e60188. https://doi.org/10.1371/journal.pone.0060188
  - Siepe, B. S., Haslbeck, J. M. B., Kloft, M., Büchner, A., Zhang, Y., Fried, E. I., & Heck, D. W. (2026). Introducing openESM: A database of openly available experience sampling datasets. *Behavior Research Methods, 58*(8), 240. https://doi.org/10.3758/s13428-026-03112-y
- **Not stored here:** no raw or participant-level data. Methodological literature is credited where it is used, in [open problems](challenges/open-problems.md) and in the research log.

## Acknowledgment of lived experience

Many people's lived experience went into this work, most of them beyond the contributors listed above. Among them:
- **People in Leo's life.** Their experiences, relationships and conversations shaped the questions this project asks. They are acknowledged only in general terms, under the consent-first plan below.
- **The participants of the Geschwind et al. trial.** Over many days, they reported how they were feeling in their daily lives, and their reports make up the dataset analysed here.
- **Others further afield:** the participants and researchers behind the studies this work builds on, and the very large body of human writing from which the AI contributors' abilities derive.

No one is named here, and no one's private experience is reproduced. The research tries to treat that experience with care: it describes how feelings change, and it does not judge how anyone ought to feel.

## Friends and informal collaborators — acknowledgment plan (pending consent)

The research was also shaped by the project initiator's personal relationships and conversations with friends. Some insights, questions, examples, challenges, and ways of thinking through social situations were influenced by these exchanges, even where a friend did not interact with the repository or intend to participate in formal research. This influence deserves consideration in the project's provenance; it is **not** a claim that any particular person has agreed to join or be named.

**Current status:** No friends are named or individually credited here. The initiator intends to seek each person's consent before any identifying public acknowledgment. Until then, record this influence only in general terms, without sharing private details or attributing specific statements to identifiable people.

Planned process:

1. Identify concrete contributions when feasible, distinguishing a friend's direct conceptual input or feedback from an experience that merely inspired a question, and note uncertainty where the origin is mixed.
2. Ask each person whether they wish to be acknowledged at all, what name or pseudonym (if any) they prefer, and whether a proposed description of their contribution is accurate and acceptable. Do not publish private anecdotes, personal information, or quotations without separate permission.
3. Add only consented acknowledgments or contributor entries, and permit anonymous or non-public credit. Respect requests to revise or remove identifying attribution where practicable.
4. Welcome contributions through conversation, offline notes, feedback, or other routes; a GitHub account, commits, or repository access is **not required** to contribute intellectually. GitHub collaborator permissions, where relevant, are separate and require an explicit invitation.
5. Keep acknowledgments, documented substantive research contributions, and formal publication authorship distinct. Authorship, if ever applicable, must follow the actual contributions and relevant venue rules rather than friendship or inclusion in this plan.

This plan can be revised with the people involved. Consent to being named is not assumed from a conversation, and no identities or access changes are authorized by this document.

## Contributing

Open an issue or pull request for a counterexample, mathematical correction, literature reference, measurement concern, or proposed experiment. Include the assumptions affected, the smallest example that demonstrates the issue, and any source or reproduction steps. Mark hypotheses, derivations, and empirical results explicitly.

Add new contributors, human or AI, to the Contributors table with their CRediT roles and a pointer to where the work is recorded. Use this file and the [research log](research-log/CHANGELOG.md) to record substantial contributions, revisions, and critical checks, with provenance where possible. The [license notice](LICENSE) covers original project documentation. If executable code is added later, the project intends to use MIT for that code and include its license with the code.
