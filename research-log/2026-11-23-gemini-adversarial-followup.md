# Gemini adversarial review follow-up — 2026-11-23

Provenance: Gemini review relayed by Leo on November 23; summarized here by ChatGPT (GPT-6.2). External commentary, not independent verification. Gemini recommended a minimal executable public model, a citable archival release/DOI, explicit preservation of the experiential AI/social stochastic selection conjecture, and clearer mathematical onboarding. It raised priority and credit concerns about private supporting code. These are recommendations, not evidence.

## Response

Prioritize executable onboarding without bypassing the empirical release gate. The accompanying standard-library script implements the existing two-state example and the two-action extension under review in the core-model PR. It is a mathematical illustration only. Run from repository root:

    python experiments/reference_model.py --rates .1
    python experiments/reference_model.py
    python experiments/reference_model.py --horizon 7

Locally executed by GPT-6.2: analytic checks passed for horizons 0–19, including absorbing boundary cases. At horizon 3, alpha .5, passive P(S)=.271 and reachable set {A}; two-action maximum P(S)=.578125 and reachable set {A,S}. At horizon 7 with two actions the reachable set is {S}. Target-wise maxima are not a probability distribution. Rates and fixed loss are stipulated, not estimated. This does not reproduce R-001–R-004 or pass their release gate.

## Remaining decisions

- Coordinate README quickstart with the existing core-file PR rather than overwrite concurrent work.
- Archive a reviewed checkpoint with a DOI when feasible; a DOI establishes a dated record, not exclusive ownership. No DOI minted here.
- Preserve the experiential AI conjecture separately as provisional, with provenance, candidate mechanisms and alternatives; avoid prematurely fixing state variables. Social regularities are not intrinsically normative objectives, and functional dynamics do not establish subjective experience.
- Seek eventual independent human expert review; cross-model agreement may reflect correlated assumptions.
- Keep the existing empirical workstream and release gate intact. No new empirical results, prediction-register changes, or publication claims.
