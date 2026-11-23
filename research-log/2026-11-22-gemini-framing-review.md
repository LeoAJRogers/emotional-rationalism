# External framing review and reproducibility plan — 2026-11-22

**Source:** Gemini review supplied by the project initiator, 2026-11-22. This is an external model critique, not independent replication or verification of the reported statistics. This entry records the review and the research director's response; no new experiment was run.

## Review observations

The review praised (1) separation of descriptive transitions, conditional evaluation and reachability, (2) explicit uncertainty and negative results, and (3) attribution and educational-demo boundaries. It raised three tensions: public quantitative estimates without public scripts, potential prescriptive interpretation of the title, and dense qualification in the README.

## Director's assessment

**Highest priority — reproducibility.** The public evidence checkpoint currently links to public source data but not the exact executable analysis, transforms, version pins, split definitions or resulting aggregate checks. This limits external verification. Public availability of source data does not imply permission to redistribute participant-level extracts. We should publish a minimal, auditable analysis package only after checking source licenses, privacy constraints, and exact output agreement.

**Communication.** Keep the title, while stating near the landing-page opening that the research describes and tests interactions among beliefs, affect, context and feasible actions; it does not prescribe control of emotion. Keep statistical caveats close to the estimates they qualify. Improve navigation rather than deleting uncertainty.

**Scientific priority.** Reproducibility is necessary but insufficient: the core test is whether a proposed mechanism makes discriminating predictions beyond rival models, including observation noise, reporting scale, time-varying context and simpler history models.

## Proposed public reproducibility release gate

1. Inventory each public numerical claim, exact source dataset/version, participant and transition inclusion criteria, preprocessing, model specifications, random seeds, bootstrap unit and confidence-interval method.
2. Verify dataset terms, participant privacy and any restrictions on redistributing derived records. Prefer retrieval instructions over bundled individual-level data.
3. Create a minimal executable pipeline with pinned dependencies and one documented command for each result, including expected outputs and numerical tolerances.
4. Run from a clean environment, compare each result against the published checkpoint, and log failures and corrections without silently overwriting historical predictions.
5. Add a rival-model comparison protocol with leakage-safe person-level partitioning, predeclared evaluation metrics and uncertainty; distinguish within-source reproducibility from independent-sample replication.
6. Only then label the public package reproducible. Until that gate passes, retain the explicit statement that code and aggregates are private.

## Priorities and non-goals

- **P0:** Discriminating rival-model tests and empirical identifiability.
- **P1:** Minimal public reproducibility package with privacy/licensing review.
- **P2:** Landing-page definition and newcomer navigation.
- **Not claimed:** a validated slow affective mechanism, clinical relevance, independent data replication, or a causal explanation for predictive history gain.

The numerical values quoted in the public README were **not** independently rechecked in this review pass. This note is an agenda and audit trail, not a new evidentiary checkpoint.
