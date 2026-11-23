# Contributions and provenance

Emotional Rationalism grew through an extended human–AI dialogue about lived experience, interpersonal dynamics, emotional responses, interpretation, and self-understanding. Its origin cannot be reduced to a few isolated anecdotes or to the subsequent mathematical writing. The private conversations and their personal significance are not reproduced in this repository.

## Contributors — contribution-based recognition

| Contributor | Type | Documented contributions |
| --- | --- | --- |
| **[LeoAJRogers](https://github.com/LeoAJRogers)** | Human | Originated and guided the inquiry; contributed observations, conceptual distinctions, counterexamples, critiques, and research decisions. |
| **ChatGPT (OpenAI; including GPT-6)** | AI | Conceptual and mathematical formulation, alternative hypotheses, critical reviews, test design, independent numerical checks, synthesis, and documentation. |
| **Claude (Anthropic; Sonnet 5.5 and Opus 5.5)** | AI | Independent critique, synthetic benchmarks, preregistered analyses, experimental checks, human-data analyses, and integration work. |
| **Gemini (Google)** | AI, external reviewer | Two reviews relayed by Leo: framing and reproducibility (2026-11-22, [#19](https://github.com/LeoAJRogers/emotional-rationalism/pull/19)) and population grounding (2026-11-23, [#4](https://github.com/LeoAJRogers/emotional-rationalism/pull/4)). Commentary, not verification. |

These entries describe substantive participation, not GitHub commit authorship or formal academic authorship. AI contributors are identified explicitly, and credit remains open to correction as provenance becomes clearer. Personal collaborators will not be individually named without consent.

### About the AI contributors

- **Why the same format.** AI systems are listed the same way as people so that the record of who did what stays complete and checkable. A row describes observable work. It is **not** a claim of authorship.
- **Publications.** Under [COPE's position on authorship and AI tools](https://publicationethics.org/cope-position-statements/ai-author), AI tools cannot be listed as authors of a paper. They cannot take responsibility for the work, declare conflicts of interest or manage copyright and licence agreements, and their use must be disclosed. Any publication from this project follows that position and the venue's own rules.
- **Accountability.** Responsibility for what this repository publishes rests with its human maintainer. Claude and ChatGPT checked each other's work, including a cross-family numerical reproduction. AI-generated text, code and literature pointers can still contain errors, so verify them before relying on them.
- **Identity.** Model names and versions are as reported in each session. Sessions are separate instances, without memory of one another. The names identify systems, not continuous individuals.
- **What the listing does not settle.** It does not resolve questions about AI experience, selfhood or moral status, and it confers no legal rights.

**LeoAJRogers** initiated and sustained the inquiry; contributed personal and interpersonal observations, conceptual distinctions, objections, questions, and direction-setting choices; clarified that the broader goal concerns context-dependent changes in persistent state rather than simply choosing or controlling emotions; and authorized the public research work.

**ChatGPT** contributed iterative conceptual framing, alternative hypotheses, counterexamples, synthesis, mathematical formulation, test and baseline design, critical reviews, and research documentation. These contributions occurred through repeated exchanges, not just a single generation of text. Project notes should continue to track the specific origin and testing of substantive ideas wherever practical.

**Claude** (Anthropic, Sonnet 5.5) contributed a critical review on 2026-11-20 covering model gaps, experiment design, and literature pointers, recorded in [the review entry](research-log/2026-11-20-claude-review.md). Its outputs are unverified by a human and its literature pointers come from model memory, so they must be checked before use.

**Additional research contributions (2026-11-20):** Claude Sonnet 5.5 also developed the first synthetic transition-sufficiency benchmark. Claude Opus 5.5 conducted critiques and runnable gain-channel, reporting-scale, sparse-sampling, rival-history and human-data analyses; wrote preregistered R-001–R-004 records, amendments and corrections; and prepared an integration brief. GPT-6 independently audited history-boundary semantics, measurement-scale equivalence and identification limits; implemented cross-item synthetic tests and exploratory item-level follow-up; and independently numerically reproduced R-003/R-004 from the original data files. This public checkpoint synthesizes and constrains those findings rather than claiming a new experimental result. Source code and detailed logs are held in private Research Commons pending a separate reproducibility/publication decision. Results that were only synthetic or exploratory remain labelled accordingly.

The ideas often developed interactively: contributions may arise from the exchange rather than being cleanly attributable to one participant. Neither the human contribution nor the AI contribution should be reduced to an incidental role. Such attribution describes observable intellectual work; it does not resolve questions about AI subjective experience, selfhood, or legal/formal academic authorship. Publications must follow applicable journal and conference authorship and disclosure policies.

## Data and source credit

The real-data analyses use openESM dataset 0010 ([Zenodo record 17347473](https://zenodo.org/records/17347473), CC BY-NC 4.0).
- **Provenance:** openESM harmonized the data that Bringmann et al. (2013) shared as supporting information. Those data come from the randomized trial of Geschwind et al. (2011).
- **How to cite:** the record asks users to cite the original authors and the openESM project:
  - Geschwind, N., Peeters, F., Drukker, M., van Os, J., & Wichers, M. (2011). Mindfulness training increases momentary positive emotions and reward experience in adults vulnerable to depression: A randomized controlled trial. *Journal of Consulting and Clinical Psychology, 79*(5), 618–628. https://doi.org/10.1037/a0024595
  - Bringmann, L. F., Vissers, N., Wichers, M., Geschwind, N., Kuppens, P., Peeters, F., Borsboom, D., & Tuerlinckx, F. (2013). A network approach to psychopathology: New insights into clinical longitudinal data. *PLoS ONE, 8*(4), e60188. https://doi.org/10.1371/journal.pone.0060188
  - Siepe, B. S., Haslbeck, J. M. B., Kloft, M., Büchner, A., Zhang, Y., Fried, E. I., & Heck, D. W. (2026). Introducing openESM: A database of openly available experience sampling datasets. *Behavior Research Methods, 58*(8), 240. https://doi.org/10.3758/s13428-026-03112-y
- **Thanks:** to the participants of the original trial, whose daily reports make up this dataset.
- **Not stored here:** no raw or participant-level data. Methodological literature is credited where it is used, in [open problems](challenges/open-problems.md) and in the research log.

## Acknowledgment of lived experience

Many people's lived experience contributed to this work. It is acknowledged here without specifying whose, and no one's private experience is reproduced. The research tries to treat that experience with care: it describes how feelings change, and it does not judge how anyone ought to feel. Anyone who would like their contribution recognized by name can be, under the consent-first plan below.

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

Use this file and the [research log](research-log/CHANGELOG.md) to record substantial contributions, revisions, and critical checks, with provenance where possible. The [license notice](LICENSE) covers original project documentation. If executable code is added later, the project intends to use MIT for that code and include its license with the code.
