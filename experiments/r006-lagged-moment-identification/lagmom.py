"""Within-person lagged-moment statistics for R-006 (revised).

Definitions follow DESIGN.md section 5. Code licence: MIT (repository LICENSE-MIT).

Data layout everywhere: Y has shape (M, D, B, J) = (person-periods, days, beeps per
day, items), NaN where missing; `person` (M,) maps person-periods to people for the
person-level bootstrap. Lag k pairs are (beep b, beep b-k) on the same day.
"""
from math import factorial

import numpy as np
from scipy.special import ndtri

K_HERMITE = 20


# --------------------------------------------------------------------------- helpers
def elem_index(J):
    """Map (j, l) with j <= l to a flat element index, and back."""
    pairs = [(j, l) for j in range(J) for l in range(j, J)]
    idx = {p: i for i, p in enumerate(pairs)}
    for (j, l), i in list(idx.items()):
        idx[(l, j)] = i
    return pairs, idx


def hermite_coeffs(tau, K=K_HERMITE):
    """phi(tau) * He_{n-1}(tau) for n = 1..K (probabilists' Hermite), shape tau.shape + (K,)."""
    out = np.empty(tau.shape + (K,))
    dens = np.exp(-0.5 * tau ** 2) / np.sqrt(2 * np.pi)
    he_prev = np.ones_like(tau)          # He_0
    he = tau.copy()                      # He_1
    out[..., 0] = dens * he_prev
    if K > 1:
        out[..., 1] = dens * he
    for n in range(1, K - 1):            # He_{n+1} = x He_n - n He_{n-1}
        he_next = tau * he - n * he_prev
        out[..., n + 1] = dens * he_next
        he_prev, he = he, he_next
    return out


def solve_latent_r(b, C, iters=50):
    """Solve sum_n b[..., n-1] r^n = C for r (Newton), |r| <= 0.99."""
    K = b.shape[-1]
    n = np.arange(1, K + 1)
    b1 = b[..., 0]
    ok = b1 > 1e-12
    r = np.where(ok, C / np.where(ok, b1, 1.0), 0.0)
    r = np.clip(r, -0.95, 0.95)
    for _ in range(iters):
        rpow = r[..., None] ** (n - 1)              # r^{n-1}
        f = r * (b * rpow).sum(-1) - C
        fp = (n * b * rpow).sum(-1)
        step = np.where(ok & (fp > 1e-12), f / np.where(fp > 1e-12, fp, 1.0), 0.0)
        r_new = np.clip(r - step, -0.99, 0.99)
        if np.max(np.abs(r_new - r)) < 1e-13:
            r = r_new
            break
        r = r_new
    return np.where(ok, r, 0.0)


# --------------------------------------------------------------------------- core
class LagMoments:
    """Centered, scaled, optionally Hermite-corrected lag-k pair products for one item
    set, for the full data (version 0) and every leave-one-day-out version (1..D)."""

    def __init__(self, Y, items, discrete, lags=(0, 1, 2, 3), min_beeps=15,
                 min_pairs=8, min_days=3, correct=True, jk=True):
        self.use_jk = jk
        X = np.asarray(Y, float)[..., list(items)]
        M, D, B, J = X.shape
        self.M, self.D, self.B, self.J = M, D, B, J
        self.lags = tuple(lags)
        self.pairs, self.eidx = elem_index(J)
        E = len(self.pairs)
        obs = ~np.isnan(X).any(-1)                                   # (M,D,B)
        lag1 = obs[:, :, 1:] & obs[:, :, :-1]
        self.n_beeps = obs.sum((1, 2))
        self.n_pairs1 = lag1.sum((1, 2))
        self.dayobs = obs.any(2)                                     # (M,D)
        self.n_days = self.dayobs.sum(1)
        keep = ((self.n_beeps >= min_beeps) & (self.n_pairs1 >= min_pairs)
                & (self.n_days >= min_days))
        # versions: 0 = full, 1+d = leave day d out
        V = D + 1
        mask = np.repeat(obs[None], V, 0)
        for d in range(D):
            mask[d + 1, :, d, :] = False
        Xz = np.where(np.isnan(X), 0.0, X)
        n = mask.sum((2, 3)).astype(float)                           # (V,M)
        with np.errstate(invalid="ignore", divide="ignore"):
            mean = (Xz[None] * mask[..., None]).sum((2, 3)) / n[..., None]   # (V,M,J)
            Xc = (Xz[None] - mean[:, :, None, None, :]) * mask[..., None]
            var = (Xc ** 2).sum((2, 3)) / n[..., None]
            s = np.sqrt(var.mean(-1))                                  # (V,M)
        good = np.isfinite(s) & (s > 1e-12)
        keep &= good[0]
        self.keep = keep
        s_safe = np.where(good, s, 1.0)
        Xs = Xc / s_safe[:, :, None, None, None]
        self.version_ok = good                                       # (V,M)
        self.mask = mask

        # pair products for each lag
        self.P, self.Vk = {}, {}
        jj = np.array([p[0] for p in self.pairs])
        ll = np.array([p[1] for p in self.pairs])
        for k in self.lags:
            P = np.zeros((V, M, D, B, E))
            Vk = np.zeros((V, M, D, B), bool)
            if k == 0:
                Vk[:] = mask
                P[:] = Xs[..., jj] * Xs[..., ll]
            else:
                a = Xs[:, :, :, k:, :]
                bm = Xs[:, :, :, :-k, :]
                Vk[:, :, :, k:] = mask[:, :, :, k:] & mask[:, :, :, :-k]
                P[:, :, :, k:, :] = 0.5 * (a[..., jj] * bm[..., ll] + a[..., ll] * bm[..., jj])
            P *= Vk[..., None]
            self.P[k], self.Vk[k] = P, Vk

        # optional ordinal (Hermite) correction
        self.corrected = bool(discrete and correct)
        self.r_hat = {}
        if self.corrected:
            cats = np.arange(1, 7)                                    # boundaries c|c+1
            le = (Xz[None, ..., None] <= cats) & mask[..., None, None]   # (V,M,D,B,J,6)
            F = le.sum((2, 3)) / n[..., None, None]                   # (V,M,J,6)
            inside = (F > 0) & (F < 1)
            tau = ndtri(np.clip(F, 1e-12, 1 - 1e-12))
            h = hermite_coeffs(tau)                                   # (V,M,J,6,K)
            a = (h * inside[..., None]).sum(-2) / s_safe[..., None, None]   # (V,M,J,K)
            fact = np.array([factorial(m) for m in range(1, K_HERMITE + 1)], float)
            bcoef = a[:, :, jj, :] * a[:, :, ll, :] / fact            # (V,M,E,K)
            for k in self.lags:
                N = self.Vk[k].sum((2, 3)).astype(float)
                with np.errstate(invalid="ignore", divide="ignore"):
                    C = self.P[k].sum((2, 3)) / N[..., None]          # (V,M,E)
                C = np.where(np.isfinite(C), C, 0.0)
                r = solve_latent_r(bcoef, C)
                rpow = r[..., None] ** np.arange(1, K_HERMITE + 1)
                corr = (bcoef[..., 1:] * rpow[..., 1:]).sum(-1)       # n >= 2 terms
                if k == 0:                                            # lag-0 diagonal unused
                    corr[..., jj == ll] = 0.0
                self.r_hat[k] = r
                self.P[k] = self.P[k] - corr[:, :, None, None, :] * self.Vk[k][..., None]

        # per-day sums
        self.Sd = {k: self.P[k].sum(3) for k in self.lags}            # (V,M,D,E)
        self.Nd = {k: self.Vk[k].sum(3) for k in self.lags}           # (V,M,D)

    # ------------------------------------------------------------- moments
    def moment(self, k, e):
        """Per person-period mean pair product for element e at lag k: (V,M)."""
        S = self.Sd[k][..., e].sum(-1)
        N = self.Nd[k].sum(-1)
        with np.errstate(invalid="ignore", divide="ignore"):
            return S / N, N[0]

    # ------------------------------------------------------------- U-statistics
    def ustat(self, k, e, k2, f, variant="all"):
        """Disjoint-pair U-statistic estimating E[P_k[e]] * E[P_k2[f]]: (V,M)."""
        Pa, Pb = self.P[k][..., e], self.P[k2][..., f]               # (V,M,D,B)
        Va, Vb = self.Vk[k], self.Vk[k2]
        Sa, Sb = Pa.sum(-1), Pb.sum(-1)                              # (V,M,D)
        Na, Nb = Va.sum(-1).astype(float), Vb.sum(-1).astype(float)
        B = self.B
        ov = np.zeros(Sa.shape)
        nov = np.zeros(Sa.shape)
        if variant in ("all", "day"):
            for o in sorted({0, -k, k2, k2 - k}):
                if o >= 0:
                    ov += (Pa[..., :B - o] * Pb[..., o:]).sum(-1)
                    nov += (Va[..., :B - o] & Vb[..., o:]).sum(-1)
                else:
                    ov += (Pa[..., -o:] * Pb[..., :B + o]).sum(-1)
                    nov += (Va[..., -o:] & Vb[..., :B + o]).sum(-1)
        if variant == "all":
            num = Sa.sum(-1) * Sb.sum(-1) - ov.sum(-1)
            den = Na.sum(-1) * Nb.sum(-1) - nov.sum(-1)
        elif variant == "day":
            num = (Sa * Sb).sum(-1) - ov.sum(-1)
            den = (Na * Nb).sum(-1) - nov.sum(-1)
        elif variant == "cross":
            num = Sa.sum(-1) * Sb.sum(-1) - (Sa * Sb).sum(-1)
            den = Na.sum(-1) * Nb.sum(-1) - (Na * Nb).sum(-1)
        else:
            raise ValueError(variant)
        with np.errstate(invalid="ignore", divide="ignore"):
            return num / den

    # ------------------------------------------------------------- jackknife
    def jackknife(self, est):
        """Day jackknife of a (V,M) estimate -> (M,). Falls back to the full-data
        estimate where any leave-one-day-out version is undefined."""
        full = est[0]
        if not self.use_jk:
            self.jk_fallback = np.zeros(self.M, bool)
            return full
        loo = est[1:]                                                # (D,M)
        dob = self.dayobs.T                                          # (D,M)
        okv = (self.version_ok[1:] | ~dob) & (np.isfinite(loo) | ~dob)
        all_ok = okv.all(0) & np.isfinite(full)
        Dm = self.n_days.astype(float)
        loo_mean = np.where(dob, np.where(np.isfinite(loo), loo, 0.0), 0.0).sum(0) / np.maximum(Dm, 1)
        jk = Dm * full - (Dm - 1) * loo_mean
        self.jk_fallback = (~all_ok) & self.keep
        return np.where(all_ok, jk, full)


# --------------------------------------------------------------------------- statistics
class Term:
    """coef * U(k, e, k2, f, variant) using item indices local to the item set."""

    def __init__(self, coef, k, jl, k2, jl2, variant="all"):
        self.coef, self.k, self.jl, self.k2, self.jl2, self.variant = coef, k, jl, k2, jl2, variant


def eval_terms(LM, terms, cache):  # noqa: D401
    """Return per person-period jackknifed sum of terms (M,) and pooled product (scalar
    numerator contributions are returned separately for the pooled bootstrap)."""
    tot = np.zeros(LM.M)
    for t in terms:
        key = (t.k, LM.eidx[t.jl], t.k2, LM.eidx[t.jl2], t.variant)
        if key not in cache:
            cache[key] = LM.jackknife(LM.ustat(*key))
        tot = tot + t.coef * cache[key]
    return tot


def jk_moments(LM, cache):
    """Per person-period jackknifed moments for every lag/element: dict[(k,e)] -> (M,),
    plus pair counts per lag (M,)."""
    out, cnt = {}, {}
    for k in LM.lags:
        for e in range(len(LM.pairs)):
            key = ("mom", k, e)
            if key not in cache:
                m, N = LM.moment(k, e)
                cache[key] = (LM.jackknife(m), N)
            out[(k, e)], cnt[k] = cache[key]
    return out, cnt


class RatioStat:
    """Statistic = sum_m w_m num_m / sum_m w_m den_m (within-person), and the pooled
    analog with each U replaced by a product of pooled moments."""

    def __init__(self, name, num_terms, den_terms, direction):
        self.name, self.num_terms, self.den_terms, self.direction = name, num_terms, den_terms, direction


def person_sums(values, person, keep, n_persons):
    v = np.where(keep, values, 0.0)
    return np.bincount(person, weights=v, minlength=n_persons)


def boot_counts(n_persons, B, rng):
    return rng.multinomial(n_persons, np.full(n_persons, 1.0 / n_persons), size=B).astype(float)


def compute_within(LM, stats, person, n_persons, counts, cache):
    """Point estimates and bootstrap draws for within-person ratio statistics."""
    w = LM.n_pairs1.astype(float)
    keep = LM.keep
    est, draws = {}, {}
    for st in stats:
        num = eval_terms(LM, st.num_terms, cache)
        den = eval_terms(LM, st.den_terms, cache)
        okm = keep & np.isfinite(num) & np.isfinite(den)
        pn = person_sums(w * np.where(okm, num, 0.0), person, okm, n_persons)
        pd = person_sums(w * np.where(okm, den, 0.0), person, okm, n_persons)
        est[st.name] = pn.sum() / pd.sum()
        with np.errstate(invalid="ignore", divide="ignore"):
            draws[st.name] = (counts @ pn) / (counts @ pd)
    return est, draws


def compute_pooled(LM, stats, person, n_persons, counts, cache):
    """Pooled analogs: products of pair-weighted pooled (jackknifed) moments."""
    mom, cnt = jk_moments(LM, cache)
    keep = LM.keep
    # person-level sums of N_k * moment and N_k
    psum, pcnt = {}, {}
    for (k, e), m in mom.items():
        N = cnt[k].astype(float)
        okm = keep & np.isfinite(m)
        psum[(k, e)] = person_sums(N * np.where(okm, m, 0.0), person, okm, n_persons)
        if k not in pcnt:
            pcnt[k] = person_sums(N, person, keep, n_persons)

    def pooled(k, e, weights=None):
        if weights is None:
            return psum[(k, e)].sum() / pcnt[k].sum()
        return (weights @ psum[(k, e)]) / (weights @ pcnt[k])

    est, draws = {}, {}
    for st in stats:
        def val(terms, weights=None):
            tot = 0.0
            for t in terms:
                e, f = LM.eidx[t.jl], LM.eidx[t.jl2]
                tot = tot + t.coef * pooled(t.k, e, weights) * pooled(t.k2, f, weights)
            return tot
        est[st.name] = val(st.num_terms) / val(st.den_terms)
        with np.errstate(invalid="ignore", divide="ignore"):
            draws[st.name] = val(st.num_terms, counts) / val(st.den_terms, counts)
    return est, draws


# --------------------------------------------------------------------------- definitions
def t1_stats(variant="all"):
    """Item excess for a 3-item set (local indices 0,1,2): per item and overall."""
    stats, nums, dens = [], [], []
    for j in range(3):
        k, l = [x for x in range(3) if x != j]
        num = [Term(1.0, 1, (j, j), 1, (k, l), variant), Term(-1.0, 1, (j, k), 1, (j, l), variant)]
        den = [Term(1.0, 1, (j, k), 1, (j, l), variant)]
        stats.append(RatioStat(f"T1_{j}", num, den, +1))
        nums += num
        dens += den
    stats.append(RatioStat("T1", nums, dens, +1))
    return stats


OFF3 = [(0, 1), (0, 2), (1, 2)]
MINOR_PAIRS = [(0, 1), (0, 2), (1, 2)]   # indices into OFF3


def t2_stats(lag_a=1, lag_b=2, prefix="T2"):
    """Relative minors for pair-rate homogeneity between lag_a and lag_b."""
    stats = []
    for (ia, ib) in MINOR_PAIRS:
        a, b = OFF3[ia], OFF3[ib]
        num = [Term(1.0, lag_a, a, lag_b, b), Term(-1.0, lag_a, b, lag_b, a)]
        den = [Term(0.5, lag_a, a, lag_b, b), Term(0.5, lag_a, b, lag_b, a)]
        stats.append(RatioStat(f"{prefix}_{ia}{ib}", num, den, 0))
    return stats


def t3_stats(lags=(1, 2, 3), name="T3"):
    """Lag-profile curvature on off-diagonal pairs, cross-day products only."""
    k1, k2, k3 = lags
    num, den = [], []
    for a in OFF3:
        num += [Term(1.0, k3, a, k1, a, "cross"), Term(-1.0, k2, a, k2, a, "cross")]
        den += [Term(1.0, k2, a, k2, a, "cross")]
    return [RatioStat(name, num, den, +1)]


def pa_det_stats():
    num = [Term(1.0, 1, (0, 0), 1, (1, 1)), Term(-1.0, 1, (0, 1), 1, (0, 1))]
    den = [Term(1.0, 1, (0, 1), 1, (0, 1))]
    return [RatioStat("PA_det", num, den, +1)]


def bipolar_stats():
    """5 items in order (C, R, W, F, S): local 0,1 = PA; 2,3,4 = NA."""
    num, den = [], []
    c, r = 0, 1
    for (j, l) in [(2, 3), (2, 4), (3, 4)]:
        for (x, y) in [((c, j), (r, l)), ((c, l), (r, j))]:
            num += [Term(1.0, 1, (c, r), 1, (j, l)), Term(-1.0, 1, x, 1, y)]
            den += [Term(1.0, 1, (c, r), 1, (j, l))]
    return [RatioStat("BIP", num, den, +1)]


def pinv_rank(S, rank):
    w, U = np.linalg.eigh(S)
    order = np.argsort(w)[::-1][:rank]
    w, U = w[order], U[:, order]
    return (U / w) @ U.T


def wald(est_vec, draw_mat, rank=2):
    ok = np.all(np.isfinite(draw_mat), axis=1)
    S = np.cov(draw_mat[ok].T)
    return float(est_vec @ pinv_rank(S, rank) @ est_vec)


def ci(draws, level=0.95):
    d = draws[np.isfinite(draws)]
    a = (1 - level) / 2
    return float(np.quantile(d, a)), float(np.quantile(d, 1 - a))


# --------------------------------------------------------------------------- analysis
NA_IDX = (2, 3, 4)
PA_IDX = (0, 1)
ALL_IDX = (0, 1, 2, 3, 4)


def analyse(Y, person, discrete, n_boot=499, seed=0, variants=("all", "day"),
            pooled=True, linear_too=True, jk=True):
    """Run every R-006 statistic on one dataset. Returns a flat dict of results."""
    person = np.asarray(person)
    n_persons = int(person.max()) + 1
    rng = np.random.default_rng(seed)
    counts = boot_counts(n_persons, n_boot, rng)
    res = {}
    modes = [("lin", False)]
    if discrete:
        modes = [("cor", True)] + ([("lin", False)] if linear_too else [])
    for tag, correct in modes:
        LMna = LagMoments(Y, NA_IDX, discrete, lags=(0, 1, 2, 3), correct=correct, jk=jk)
        cache = {}
        groups = {
            "T1": t1_stats("all"),
            "T1day": [RatioStat(s.name.replace("T1", "T1day"), s.num_terms, s.den_terms, s.direction)
                      for s in t1_stats("day")] if "day" in variants else [],
            "T2": t2_stats(1, 2, "T2"),
            "T20": t2_stats(0, 1, "T20"),
            "T3": t3_stats((1, 2, 3), "T3"),
            "T30": t3_stats((0, 1, 2), "T30"),
        }
        stats = [s for g in groups.values() for s in g]
        est, draws = compute_within(LMna, stats, person, n_persons, counts, cache)
        _store(res, f"{tag}_w", est, draws, stats)
        res[f"{tag}_n_pp"] = int(LMna.keep.sum())
        res[f"{tag}_jk_fallback"] = int(getattr(LMna, "jk_fallback", np.zeros(1, bool)).sum())
        if pooled:
            pst = groups["T1"] + groups["T2"] + groups["T20"] + groups["T3"]
            pest, pdraws = compute_pooled(LMna, pst, person, n_persons, counts, cache)
            _store(res, f"{tag}_p", pest, pdraws, pst)
        LMpa = LagMoments(Y, PA_IDX, discrete, lags=(1,), correct=correct, jk=jk)
        est, draws = compute_within(LMpa, pa_det_stats(), person, n_persons, counts, {})
        _store(res, f"{tag}_w", est, draws, pa_det_stats())
        LMall = LagMoments(Y, ALL_IDX, discrete, lags=(1,), correct=correct, jk=jk)
        est, draws = compute_within(LMall, bipolar_stats(), person, n_persons, counts, {})
        _store(res, f"{tag}_w", est, draws, bipolar_stats())
    return res


def _store(res, prefix, est, draws, stats):
    t2_names = {}
    for st in stats:
        lo, hi = ci(draws[st.name])
        res[f"{prefix}_{st.name}"] = float(est[st.name])
        res[f"{prefix}_{st.name}_lo"] = lo
        res[f"{prefix}_{st.name}_hi"] = hi
        if st.name.startswith("T1_"):                   # Bonferroni over 3 items (Part B sign test)
            lo3, hi3 = ci(draws[st.name], level=1 - 0.05 / 3)
            res[f"{prefix}_{st.name}_lo3"] = lo3
            res[f"{prefix}_{st.name}_hi3"] = hi3
        for pre in ("T2_", "T20_"):
            if st.name.startswith(pre):
                t2_names.setdefault(pre[:-1], []).append(st.name)
    for grp, names in t2_names.items():
        if len(names) == 3:
            vec = np.array([est[n] for n in names])
            mat = np.column_stack([draws[n] for n in names])
            res[f"{prefix}_{grp}_W"] = wald(vec, mat, rank=2)
