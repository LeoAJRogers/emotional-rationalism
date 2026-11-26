# Prior-art addendum to PR #17 (Claude Opus 5.5, 2026-11-26)

**Status:** supplements the open first-pass comparison in PR #17 (`2026-11-22-claude-prior-art-comparison.md`), whose verdicts this pass reached independently and does not change: C1 already known; C2 narrowed; C3 mathematics known, application narrowed; C4 unresolved, narrowed. Listed here are only precedents and points that #17 does not include. Sources were opened to confirm existence and the claim made; primary papers were not read in full. Absence of a precedent is not evidence of absence. See also the independent review logged the same day, which adds CoMERG.

## Additional precedents

**Dynamics (C1)**
- Rutledge-style exponentially weighted history has a preregistered replication: Vanhasbroeck et al. (2021). R-003's two-EWMA finding matches this form.
- Input-driven computational affect models compared on data: Vanhasbroeck et al. (2022), *Affective Science* 3. Closest to ER's cue term.
- Dejonckheere et al. (2019), *Nature Human Behaviour* 3: complex dynamic measures add little beyond mean levels. Consistent with R-003's near-zero nonlinear gain.
- DSEM (Asparouhov, Hamaker & Muthén, 2018) for person-specific parameters and period-level shifts, relevant to R-004.

**Belief-to-affect lag**
- Sherman & Kim (2002), *Affective perseverance*: affect outlived invalidated cognition in four studies; opposite-valence invalidation changed it, neutral invalidation did not. A model of the lag should reproduce this asymmetry.
- Teasdale & Barnard (1993), Interacting Cognitive Subsystems: "knowing with the head" versus "knowing with the heart". Teasdale co-developed MBCT, the therapy in openESM 0010, so reviewers will expect this citation.
- Mitchell, *Affective persistence and the normative phenomenology of emotion* (philosophy of recalcitrant emotion).
- Kuppens et al. (2012), appraisal and core-affect dynamics measured jointly over time.

**Fittingness (C2)**
- D'Arms & Jacobson (2023), *Rational Sentimentalism* (OUP): a full theory built on emotional fittingness. **Naming note:** this title is close to "Emotional Rationalism", and "emotional rationalism" is also used loosely for the general idea that emotion and reason work together. The README should say how the project differs from both.
- Tamir et al. (2016), desired emotions follow personal values across cultures.
- Clinical precedent: checking whether a feeling fits the facts is a standard DBT skill ("Check the Facts").

**Reachability (C3)**
- Amin et al. (2006), the earlier controlled discrete-time stochastic hybrid reachability paper preceding Abate et al. (2008).
- Etkin, Büchel & Gross (2015), *Nature Reviews Neuroscience*: emotion regulation in reinforcement-learning terms.

**Population reference**
- Hochschild (1979), feeling rules: socially shared norms for what one should feel. Tsai's ideal affect.
- Pitfall: what most people feel is not what fits (the moralistic-fallacy point in reverse). A reflected population reference should be a benchmark, not a fit standard. The AI-alignment literature has not been searched for population-reference ideas; that remains open.

**Social coupling**
- Butler (2011), temporal interpersonal emotion systems (TIES), and the `rties` R package.
- Gottman, Murray et al. (2002), *The Mathematics of Marriage*: coupled difference equations with uninfluenced set points, emotional inertia and influence functions. Any multi-agent extension should start here.

## Sources

Amin et al. 2006, https://link.springer.com/chapter/10.1007%2F11730637_7 · Asparouhov, Hamaker & Muthén 2018, https://www.StatModel.com/download/DSEM.pdf · Butler 2011, https://typeset.io/pdf/temporal-interpersonal-emotion-systems-the-ties-that-form-3zky8mndvo.pdf · Butler & Barnard (rties), https://pmc.ncbi.nlm.nih.gov/articles/PMC6786942 · D'Arms & Jacobson 2023, https://academic.oup.com/book/45567 · Dejonckheere et al. 2019, https://www.nature.com/articles/s41562-019-0555-0 · Etkin, Büchel & Gross 2015, https://is.muni.cz/el/fss/jaro2023/PSYn4580/110769722/The_neural_bases_of_emotion_regulation.pdf · Gottman et al. 2002, https://typeset.io/pdf/the-mathematics-of-marriage-dynamic-nonlinear-models-38e9iq90o8.pdf · Hochschild 1979, https://edisciplinas.usp.br/mod/resource/view.php?id=2208909 · Kuppens et al. 2012, https://www.frontiersin.org/articles/10.3389/fpsyg.2012.00380/pdf · Mitchell, https://philarchive.org/archive/MITAPA-8 · Sherman & Kim 2002, https://escholarship.org/uc/item/5mv891bh · Tamir et al. 2016, https://cris.huji.ac.il/en/publications/desired-emotions-across-cultures-a-value-based-account/ · Teasdale & Barnard 1993, https://www.mrc-cbu.cam.ac.uk/bibliography/articles/2849 · Vanhasbroeck et al. 2021, https://eld.bl.uk/catalog/100135088217_0x000001 · Vanhasbroeck et al. 2022, https://pmc.ncbi.nlm.nih.gov/articles/PMC9537408
