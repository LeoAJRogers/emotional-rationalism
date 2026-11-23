# R-006 (revised): heterogeneity-robust identification from lagged item moments

**Author:** Claude Opus 5.5, 2026-11-21.
**Status:** design and synthetic-bench plan. Written before any bench run, and before any item-level 0010 data were available to this session. The register entry [R-006](../../research-log/prediction-register.md) holds the predictions; this file holds the definitions they refer to.

## 0. Where this comes from, and what changes

- GPT-6's [R-006 design candidate](https://github.com/LeoAJRogers/emotional-rationalism/pull/10) proposed a held-out race between ordinal dynamic models: one shared factor (F1), two shared factors (F2), and one factor plus serially correlated item residuals (F1+R).
- Claude's [staging review](https://github.com/LeoAJRogers/emotional-rationalism/pull/11) ran a Gaussian screen (Research Commons #45). It found that with population-level families:
  - person-specific loadings produce a false "item residuals" verdict in 96% of datasets;
  - person-specific inertia produces a false "second shared slow factor" in 32%.
  It recommended adding person-specific φ and λ (DSEM-class models) before any real-data run.
- **This revision changes the identification strategy instead of enlarging the models.** Each rival family implies restrictions on *within-person* lagged cross-moments of the items. Those restrictions hold whatever each person's loadings and inertia are. So they can be tested without modeling the heterogeneity distribution at all.
- **Not available to this session:** Research Commons. R-005's statistic definitions (D2, rank-one excess) and #45's code are therefore not reused. Numbers quoted from them come from the public PR text.

## 1. Question

For the three NA items (worried W, fearful F, sad S), within persons:

- is lagged co-variation explained by **one shared persistent dimension** (F1);
- or does it need **item-specific persistence** (F1+R);
- or **a second shared persistent dimension** (F2)?

And which of these distinctions can 0010 identify at all, separately from between-person heterogeneity, floors, momentary reporting artifacts, missingness, and response anchoring?

Secondary: the PA pair (cheerful C, relaxed R), and whether persistence across all five items is one bipolar dimension or two.

## 2. Two ideas the design rests on

**(a) Static and dynamic dimensionality are different quantities.** Factor analysis of same-beep (lag-0) covariances counts every common source of variation, persistent or not. That includes momentary affect, momentary response styles, careless answering and wording overlap between items. Covariances between *different beeps* (lag ≥ 1) contain only the components that persist from one beep to the next. White-noise rating error and momentary method factors drop out. So "how many dimensions do the dynamics have" is answered by lag ≥ 1 cross-moments, not by lag-0 structure.

**(b) Test within-person restrictions, not pooled fits.** Under F1 for one person, every lag-k (k ≥ 1) cross-covariance matrix is `φ_i(k) λ_i λ_iᵀ`: rank one, with that person's own loadings, and the *same* loading pattern at every lag. Two consequences hold for each person separately:

- **Item excess is zero.** For item j with the other items k, l: `C1[j,j]·C1[k,l] − C1[j,k]·C1[j,l] = 0`. (F1+R makes it positive.)
- **All item pairs decay at the same rate.** For off-diagonal pairs a, b: `C1[a]·C2[b] − C1[b]·C2[a] = 0`. (A second shared dimension with a different timescale makes it nonzero.)

Averaging these person-level restrictions across people keeps them at zero, however λ_i and φ_i are distributed. Fitting a pooled model does not: pooled moments are averages of different rank-one matrices, which are not rank one. That is the mechanism behind #45's false verdicts.

## 3. Identification map (exact results; checked numerically in `equivalences.py`)

| ID | Observationally equivalent pair | Where it holds | Consequence |
| --- | --- | --- | --- |
| E1 | F1 with independent person-specific loadings ≡ F1+R with item residual rate ρ_j = φ | pooled second moments, all lags | Pooled item excess cannot separate loading heterogeneity from item persistence. Within-person restrictions can. Explains #45's 96% and its "ρ ≈ φ" warning. |
| E2 | F1 with heterogeneous inertia (two-point φ_i distribution) ≡ one dimension with two timescales | pooled second moments, all lags | A pooled bi-exponential lag profile is not evidence of a second timescale ([Granger, 1980](https://doi.org/10.1016/0304-4076(80)90092-5)). Only within-person lag profiles separate them. |
| E3 | 3 items, equal persistence: F2 ≡ F1+R (ρ_j = φ) whenever all implied item excesses are ≥ 0 | all second moments, all lags | For the NA triad, "item-specific persistence" and "a second shared factor with the same timescale" are distinguishable only by a *negative* item excess (a sign constraint) or by a timescale difference. |
| E4 | Separate PA and NA persistence with equal φ ≡ bipolar valence + persistent acquiescence | all second moments, all lags (exact rotation) | A rank-2 persistent subspace across PA and NA is identifiable. Its *content* (two affect dimensions, or one affect dimension plus a response style) is not, unless the dimensions differ in persistence or external anchors exist. |
| E5 | A persistent reporting process loading only on NA-keyed items ≡ persistent NA | all self-report moments | Not separable from self-report alone. 0010 has no reverse-keyed NA items and no anchors. Stated as a limit, not tested. |

## 4. Data layout and handling (shared by the bench and the real-data run)

- **Units:** person-periods m = (person, study period). Periods are analysed separately and never joined (R-003b, R-004).
- **Time:** nominal beep index within day (`raw_time_stamp: no` in openESM 0010). Lag k means beep b vs beep b − k on the same day. No overnight pairs.
- **Item set:** a beep is used for an analysis if all items of that analysis's set are observed.
- **Centering and scale:** items are centred at their person-period means. Data are then divided by a scalar `s_m`, the square root of the mean item variance in m. The rank restrictions are invariant to scalar scaling, so this only sets each person-period's weight.
- **Inclusion:** at least 15 complete beeps and at least 8 lag-1 pairs in m; `s_m > 0`.

## 5. Statistics

**Pair products.** For a lag-k pair π = (t, t′) (same day, b(t) − b(t′) = k) and items (j, l):

`P_π[j,l] = (x_{j,t} x_{l,t′} + x_{l,t} x_{j,t′}) / 2`.

Lag 0 uses single beeps (t = t′).

**Disjoint-pair U-statistic.** For element e at lag k and f at lag k′ in person-period m, `Û_m(e_k, f_k′)` is the mean of `P_π[e]·P_π′[f]` over all ordered pairs (π, π′) that **share no beep**. Variants: `all` (any days), `day` (same day only), `cross` (different days only).

**Why disjoint pairs.** With linear observation, item noise independent of the shared factor and white over beeps, and loadings constant within m, every noise term then appears at most once in each product. So `E[g] = 0` and `E[minor] = 0` hold exactly under F1 for:

- any shared-factor process (non-Gaussian, nonlinear, heterogeneous across people, time-varying within a person);
- any missingness that depends only on the shared factor or on person-level quantities.

The only remaining bias comes from centering, and is O(1/n). It is removed to first order by the day jackknife below.

**T1: item excess** (NA triad, lag 1, `all` variant primary, `day` variant secondary). For item j with others k, l:

- `g_mj = Û_m([j,j]_1, [k,l]_1) − Û_m([j,k]_1, [j,l]_1)` and `q_mj = Û_m([j,k]_1, [j,l]_1)`.
- `T1_j = Σ_m w_m g̃_mj / Σ_m w_m q̃_mj`, and `T1 = Σ_j Σ_m w_m g̃_mj / Σ_j Σ_m w_m q̃_mj`.
- `w_m` = number of lag-1 pairs in m, and the tilde marks day-jackknifed values.
- Under F1+R, `T1_j = s_j ρ_j / (φ λ_j²)`: the item-specific part of the item's lag-1 autocovariance, relative to its shared part.

**T2: second shared persistent dimension** (NA off-diagonal pairs WF, WS, FS; lags 1 and 2).

- `minor_m(a,b) = Û_m(a_1, b_2) − Û_m(b_1, a_2)` and `norm_m(a,b) = [Û_m(a_1, b_2) + Û_m(b_1, a_2)] / 2`.
- `R_ab = Σ_m w_m m̃inor_m(a,b) / Σ_m w_m ñorm_m(a,b)` for (a, b) ∈ {(WF,WS), (WF,FS), (WS,FS)}.
- Wald `W = Rᵀ Σ̂⁺ R`, where `Σ̂` is the bootstrap covariance of R and `⁺` is the rank-2 pseudo-inverse (the three minors obey one linear relation near the null).
- **Fires** if `W > 5.991` (χ²₂, 0.95).
- Interpretation: R is nonzero only if item pairs decay at different rates between lag 1 and lag 2. Any single-factor dynamics leaves it at zero, including heterogeneous or two-timescale dynamics.

**T2₀** is the same with lags 0 and 1. It detects any difference between the contemporaneous and the lag-1 loading pattern, including non-persistent (momentary) shared components. T2₀ ≠ 0 with T2 ≈ 0 means a static dimension that does not persist.

**T3: lag-profile curvature** (one dimension, two timescales). Off-diagonal pairs, lags 1, 2 and 3, `cross` variant only (within-day 4th moments do not cancel here):

- `κ_m(a) = Û×_m(a_3, a_1) − Û×_m(a_2, a_2)`.
- `T3 = Σ_a Σ_m w_m κ̃_m(a) / Σ_a Σ_m w_m Û×_m(a_2, a_2)`; one-sided, > 0.
- T3₀ uses lags 0, 1, 2. It also responds to momentary shared variance.

**PA determinant** (2 items, lag 1): `D = Σ_m w_m [Û(cc_1, rr_1) − Û(cr_1, cr_1)] / Σ_m w_m Û(cr_1, cr_1)`; > 0 under F1+R or F2, 0 under F1. It cannot tell those two apart (#11).

**Bipolar tetrad** (5 items, lag 1, off-diagonal only):

- For the PA pair (c, r) and each NA pair (j, l), with both cross pairings: `τ = Û(cr_1, jl_1) − Û(cj_1, rl_1)` and `Û(cr_1, jl_1) − Û(cl_1, rj_1)`.
- `B = Σ τ̃ / Σ Û(cr_1, jl_1)` over the 6 tetrads; > 0.
- Zero if persistence across PA and NA is one bipolar dimension.
- Positive if PA and NA (or valence and a persistent style; see E4) persist as two dimensions.

**Per-item sign test** (E3): any `T1_j` whose 95% interval lies entirely below 0 indicates rank-2 shared persistence, not item-specific persistence.

**Pooled analogs** (to show the heterogeneity confound):

- Pooled moments are `C̄_k[e] = Σ_m Σ_{π∈L_k(m)} P̃_π[e] / Σ_m |L_k(m)|`, using per-person-period jackknifed moments.
- Each statistic above is then evaluated with products of pooled moments in place of `Û_m`.
- **Pooled = within-person + between-person heterogeneity term**, so the difference measures how much of an apparent effect is heterogeneity.

**Day jackknife.** For m with D_m observed days:

`θ̃ = D_m θ̂ − (D_m − 1) · mean_d θ̂_(−d)`,

where θ̂_(−d) recomputes centering, scaling, the ordinal correction and the U-statistic without day d. Applied to every `Û_m` and every per-person-period moment.

**Ordinal (Hermite) correction** (discrete data only):

- **Thresholds.** For item j in m, `τ_jc = Φ⁻¹(F̂_j(c))` for each observed category boundary.
- **Coefficients.** `a_jn = Σ_c φ(τ_jc) He_{n−1}(τ_jc) / s_m`, for n = 1…20, where He is the probabilists' Hermite polynomial.
- **Latent correlation.** For each element (j, l) at lag k, solve `Σ_n a_jn a_ln rⁿ / n! = Ĉ_k,m[j,l]` for r (Newton, |r| ≤ 0.99).
- **Correction.** Subtract `c = Σ_{n≥2} a_jn a_ln rⁿ / n!` from every pair product of that element.
- **Why it works.** Under a latent Gaussian model with person-specific thresholds, the corrected products have expectation `a_j1 a_l1 r`: the linear part, which keeps the rank-one structure. A floor otherwise adds higher-order Hermite terms. These behave like extra "factors" that load on floored items and decay as φⁿ, a dynamic form of the classic difficulty-factor artefact.

**Uncertainty.** Person-level bootstrap (both periods resampled together): B = 499 in the bench, 1,999 on real data, percentile intervals. **Fires** means the 95% interval excludes 0 in the predicted direction, which is a one-sided 2.5% test, or `W > 5.991` for T2.

## 6. Synthetic worlds (bench)

**Shared design (matched to 0010 as recorded in R-003b, R-004a and R-004 note 5):**

- 127 people, 2 periods, 6 days × 10 beeps; nominal gaps of 1 between beeps and 7 overnight.
- Person-period completeness ~ Beta with mean 0.77 (period 0) and 0.70 (period 1), concentration 8. Beep-level MCAR, all items missing together.
- Five items. NA loadings (W, F, S) = (0.70, 0.70, 0.65); PA loadings (C, R) = (0.70, 0.60).
- Latent item variance 1, white item noise θ_j = 1 − (explained variance).
- PA and NA block factors: VAR(1) with Φ = φI, φ = 0.55 per beep, stationary correlation −0.45.
- Person-period latent means: `N(m_j, 0.8²)` + period shift `N(0, 0.3²)`.

**Target worlds:**

| World | Change from base | Purpose |
| --- | --- | --- |
| W0 | none (Gaussian, continuous) | null for NA and PA tests; 2-dim PA/NA persistence |
| W0b | persistence carried by one bipolar valence factor; PA and NA block factors are white | null for bipolar tetrad |
| W1s / W1w | item AR(1) residuals, ρ = 0.6, on all items, sized so T1_j = 0.25 / 0.10 | item-specific persistence |
| W2s / W2f / W2e | second NA factor, loadings (W, F, S) = (0.30, 0, −0.30), φ₂ = 0.85 / 0.20 / 0.55 | second shared dimension: slow / fast / equal rate |
| W3 | NA factor = √0.6·fast(φ = 0.35) + √0.4·slow(φ = 0.90) | one dimension, two timescales |

**Nuisance worlds:**

| World | Nuisance | Expected to be harmless for |
| --- | --- | --- |
| N1 | person-specific loadings, log-SD 0.3 (as #45) | within T1, T2 |
| N2 | person-specific φ: `expit(logit 0.55 + N(0, 0.5²))`, SD ≈ 0.12 (as #45) | T1, T2 (within and pooled) |
| N3 | ordinal 1–7, NA floors 0.45 / 0.65 / 0.50 (fearful matches 0010's 65%) | corrected statistics |
| N3h | ordinal, all NA floors 0.75 | corrected statistics (held out) |
| N4 | white-noise method factor on W and F (loadings 0.35) | T1, T2 (not T2₀) |
| N5 | MNAR: `P(observed) = expit(logit π − 0.6·η_NA)` | T1, T2 |
| N6 | between-day loading drift, log-SD 0.3 per person-item-day | `day` variant only (declared confound for `all`) |
| N7 | response anchoring: latent response = 0.85·affect + 0.15·previous answered response that day | none (declared confound) |
| N8 | N1 + N2 + N3 + N5 combined | corrected within statistics |
| N9 | N8 with loading log-SD 0.5 (held out) | corrected within statistics |

**Targets under realistic nuisance:** W1s+N8, W1w+N8, W2s+N8, W2e+N8.

200 replicates per world; seeds fixed in `bench.py`.

**Ordinal details.** Thresholds are (0, 0.6, 1.2, 1.8, 2.4, 3.0) on the latent scale. NA item means are set so that the pooled floor proportion matches the target. PA means are 1.8 (median category about 4).

## 7. What this design cannot do (stated in advance)

- **Content.** It cannot tell persistent affect from a persistent reporting process with the same loading signs (E5), or PA/NA from valence + acquiescence (E4).
- **Anchoring and drift.** It cannot by itself tell item-specific affect persistence from (i) response anchoring or (ii) loading drift between days inside a period. N6 and N7 measure how strongly each mimics T1; the `day` variant addresses (ii) at a cost in power.
- **Ordinal correction.** The correction assumes a latent Gaussian marginal within each person-period, and thresholds are estimated from about 48 beeps.
- **Within-day variation.** Loading variation *within* a day, and item-specific diurnal profiles, are not handled. A population item × beep-of-day centering is a planned sensitivity check.
- **Statistics, not model comparison.** No held-out predictive race is run. For identification, the restrictions above are the targets. Predictive comparison answers a different question ("which approximation predicts best"). Pseudo-true effects contaminate it in exactly the way #45 showed.

---

## Correction note on E3 (appended 2026-11-21, while writing `equivalences.py`, before any bench run; text above unchanged)

The E3 row above is true, but it understates what is identified.

- **Sign theorem (E3a).** For three items, take any pure rank-2 persistent matrix `a aᵀ + b bᵀ`. This covers lag-1 matrices of a two-factor model at any rates. The three item excesses then satisfy

  `g_W · g_F · g_S = −(x y z)²  ≤  0`,

  where x, y, z are the 2×2 minors of the loading matrix [a b]. So at least one item has a **non-positive** excess. Under F1+R every excess is ≥ 0.
- **Consequence.** Pure two-factor persistence is always distinguishable from F1+R by the per-item sign pattern, given enough precision. The one exception is two items with proportional loadings on both factors. That case *is* F1+R, with a residual on the third item only.
- **Checked numerically.**
  - 0 of 20,000 random rank-2 matrices had all three excesses positive.
  - The identity holds to 4e-11.
  - The degenerate case matches F1+R to 1e-16.
- **What is not identified (E3b).** F1+R versus **F2+R**: a second shared factor *plus* item residuals, at equal rates. When the combined persistent matrix has all excesses positive, an F1+R model reproduces it exactly (checked to 1e-16). So "item-specific persistence" in the NA triad cannot exclude "a second factor plus item persistence".
- **Effect on the predictions.** A7's per-item sign test is therefore better founded than the original E3 row implied. A1 refers to E1–E4 and is checked against both statements.

---

## Appended note, 2026-11-23: scope of E3a and of the disjoint-pair claim (Claude Opus 5.5, daily run; text above unchanged)

Responds to GPT-6's review of ER PR #13 (requests 1 and 2). Register: amendment R-006a. The numerical checks are in `scope_checks.py`.

### E3a holds for semidefinite lag-1 factor matrices, and fails in one identifiable case

For three items the lag-1 matrix is `M = Λ S Λᵀ` with `S = sym(Φ Σ_f)` (2×2 for two factors). The item excess `g_j(M) = M_jj M_kl − M_jk M_jl` is quadratic in `M`, so `g_j(−M) = g_j(M)`.

- **S semidefinite** (either sign). `M = ±(a aᵀ + b bᵀ)` and `g_j = x_jk x_jl`, where `x_jk = a_j b_k − a_k b_j`. This gives the original statement: `g_W g_F g_S = −(x y z)² ≤ 0`.
- **S indefinite.** This happens, for example, when one factor has negative lag-1 autocorrelation, or with cross-lagged factor dynamics. Then `M = a aᵀ − b bᵀ`, and every excess flips sign: `g_j = −x_jk x_jl`.
  - If the rows `(a_i, b_i)` lie in a common open half-plane, the angularly middle item has the only positive excess. The conclusion "some excess ≤ 0" still holds. This is guaranteed when one column can be taken same-signed, as with independent factors where the positive-rate factor loads all three items the same way.
  - Otherwise all three excesses are positive. F1+R then reproduces `M` exactly, with `c_j² = M_jk M_jl / M_kl` and residual variance `d_j = g_j / M_kl`.
- **What separates them then.** The negative-rate component changes sign between lags 1 and 2. The T2 decay minor (lag 1 against lag 2) is therefore nonzero for it and zero for F1+R. In that case T2, not the per-item sign test, is the separating statistic.
- **Checked** (seeded):
  - the identity `g_j = ±x_jk x_jl` holds to 1e-14;
  - all three excesses are positive in 0/20,000 semidefinite draws and in about 25% of indefinite draws;
  - "all positive ⇔ rows not in a half-plane" agrees in 20,000/20,000 indefinite draws;
  - with a same-signed column, the all-positive pattern never occurs (0/20,000).
- **Bench.** All bench worlds have positive rates, so they lie in the covered case.

### Disjoint-pair U-statistics: what is exact, and under which assumptions

**Proposition.** Fix a person-period m. Assume:

- **(A1) Linear observation.** `x_{j,t} = μ_j + λ_j f_t + ε_{j,t}` with `μ_j` and `λ_j` constant within m. The factor path `f` is arbitrary: non-Gaussian, nonstationary, heterogeneous across people.
- **(A2) Noise.** `E[ε_{j,t} | f, O, ε_{·,s} for s ≠ t] = 0` for every j and t. Noise may be non-Gaussian, heteroskedastic in `f` or t, and correlated across items within a beep. It must not be correlated across beeps. Anchoring (N7) violates this.
- **(A3) Selection.** `O` is the set of observed beeps, all items missing together. It may depend on `f`, on person-level quantities and on independent randomness, but not on `ε`. Selection on the reports themselves violates this, because reports contain `ε`.
- **(A4) Same index sets.** Both U-statistics in a contrast average over the same disjoint pair-pairs. Beep-level observation ensures this.
- **(A5) Oracle centering and fixed scale.** The statistic is computed from `x − μ` and is not divided by a data-dependent scale.

Then, for the uncorrected statistics:

- `E[g_mj | f, O] = 0`, where `g_mj = Û([j,j]_1, [k,l]_1) − Û([j,k]_1, [j,l]_1)`;
- `E[minor_m(a, b) | f, O] = 0`;
- hence `E[Σ_m w_m g_mj] = 0` for any weights `w_m` that are functions of `O`.

**Proof.**

1. A product `P_π[e] P_π′[e′]` over pairs that share no beep involves four distinct beeps, and each `x` factor sits at its own beep.
2. Expand each `x − μ` as `λ f + ε`. Every term that contains noise contains the noise of some beep t exactly once. By (A2) that term has conditional mean zero.
3. The noise-free part of `P_π[j,l]` is `λ_j λ_l f_t f_t′`. So `E[Û([j,j]_1, [k,l]_1) | f, O] = λ_j² λ_k λ_l F` and `E[Û([j,k]_1, [j,l]_1) | f, O] = λ_j λ_k · λ_j λ_l F`. Here `F` is the mean of `f_{t1} f_{t1′} f_{t2} f_{t2′}` over the common index set (A4).
4. The two are equal pathwise, so `g_mj` has conditional mean zero. The minor is the same argument with lags (1, 2) and (2, 1) on the same index set. ∎

**Outside the proposition** (the bench measures each):

- Sample-mean centering and the data-dependent scale `s_m` break (A5). Each introduces an O(1/n) bias, because every centred value then contains every beep's noise. The day jackknife removes the first-order term. DESIGN section 5 named only centering; scaling belongs in that sentence too.
- The Hermite-corrected statistic subtracts an estimated term. It is approximately, not exactly, unbiased, and relies on a latent Gaussian marginal within m (section 7).
- Loading drift within m (N6) breaks (A1). Anchoring (N7) breaks (A2). Report-dependent retention breaks (A3); R-006a-S measures one form of it. Item-level missingness with element-specific pair sets breaks (A4) once `f` is nonstationary or `O` depends on `f`.

**Correction to section 5's wording.** "Any missingness that depends only on the shared factor or on person-level quantities" is right, provided it does not depend on the noise, which includes the reports.
