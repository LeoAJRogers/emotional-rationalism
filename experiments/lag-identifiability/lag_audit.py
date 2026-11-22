#!/usr/bin/env python3
"""lag_audit.py - independent audit of experiments/lag-identifiability.

Synthetic only; no human data. Every result line is tagged:
  [MATH]  an algebraic identity, checked numerically (max |difference| printed);
  [ARITH] arithmetic on numbers published in the repository;
  [SIM]   a Monte-Carlo result under the synthetic assumptions stated beside it.
Nothing printed here is an empirical claim about people.

Run:  python -I lag_audit.py           (NumPy only; about 80 s)
      python -I lag_audit.py --quick   (fewer replicates; smoke test)

Defaults follow UNKNOWN_LOADING.md where it is specific (n=240, lag .78, noise
SD .4, fit on first 60%, select on next 20%, coefficient grid .1-.9 x33,
loading grid 0-1 x41). Where it is not (cue generator, noise sharing, tie rule,
candidate order) this script uses benchmark.py's choices: 12-step random-sign
cue blocks, independent channel noise, first-listed candidate wins exact ties,
order A, B, M. The local unknown_loading.py was not available, so its exact
counts are not expected to be reproduced; the structural results do not depend
on them.
"""
import argparse
import numpy as np

SEED = 20261122
N, RHO, BLOCK, SD = 240, 0.78, 12, 0.4
RHO_GRID = np.linspace(0.1, 0.9, 33)
LAM_GRID = np.linspace(0.0, 1.0, 41)
TR = np.arange(0, 144)        # fit: first 60%
VA = np.arange(144, 192)      # select: next 20%; the last 20% is never touched
KINDS = ("A", "B", "M")       # affect lag, belief lag, report lag (clock time, as in the repo)
TIE_RTOL = 1e-9


def onepole(x, rho, init=0.0):
    """y_t = rho*y_{t-1} + (1-rho)*x_t, y_{-1}=init. rho scalar or 1-D. Returns (len(rho), n)."""
    r = np.atleast_1d(np.asarray(rho, float))
    out = np.empty((r.size, len(x)))
    prev = np.full(r.size, float(init))
    for t in range(len(x)):
        prev = r * prev + (1.0 - r) * x[t]
        out[:, t] = prev
    return out


def cue_blocks(rng, n=N, block=BLOCK):
    return np.repeat(rng.choice([-1.0, 1.0], size=-(-n // block)), block)[:n]


def truth(kind, x, rho=RHO, alpha=0.0, lam=0.0, kin=None):
    """Noise-free observed channels (belief b, report y, proxy p).

    Proxy p = alpha*b + (1-alpha-lam)*z + lam*y, then optional own kinetics
    (one-pole with coefficient kin). alpha = a direct cue/belief pathway into the
    proxy (cue reactivity); lam = the proxy's share of the report pathway
    (UNKNOWN_LOADING's 'report fraction'), or equally of any cue-locked error it
    shares with the report."""
    L = onepole(x, rho)[0]
    b, z, y = {"A": (x, L, L), "B": (L, L, L), "M": (x, x, L)}[kind]
    p = alpha * b + (1.0 - alpha - lam) * z + lam * y
    if kin is not None:
        p = onepole(p, kin)[0]
    return np.stack([b, y, p], axis=1)


def noise(rng, n=N, sd=SD, phi=0.0, r=0.0):
    """Errors for (b, y, p). b: iid. y and p share an AR(1) component
    (autocorrelation phi, variance r*sd^2) plus independent N(0,(1-r)sd^2), so
    every channel keeps marginal SD sd. r=0 gives iid noise."""
    e = rng.normal(0.0, sd, (n, 3))
    if r > 0:
        s = np.empty(n)
        s[0] = rng.normal()
        u = rng.normal(0.0, np.sqrt(1.0 - phi ** 2), n)
        for t in range(1, n):
            s[t] = phi * s[t - 1] + u[t]
        e[:, 1:] = np.sqrt(1.0 - r) * e[:, 1:] + np.sqrt(r) * sd * s[:, None]
    return e


def family(fam, x, L):
    """Candidate predictions P (G, n, 3) over its grid; returns P, rho per point, loading per point."""
    R, n = L.shape
    X = np.broadcast_to(x, (R, n))
    if fam in ("A", "B"):
        b = X if fam == "A" else L
        return np.stack([b, L, L], axis=-1), RHO_GRID, np.full(R, np.nan)
    w = LAM_GRID[None, :, None]
    Xk, Lk = X[:, None, :], L[:, None, :]
    if fam == "M":        # proxy = (1-lam) z + lam y, with z = x, y = L
        p = (1.0 - w) * Xk + w * Lk
    elif fam == "A+":     # affect lag with a free cue-reactive proxy: alpha x + (1-alpha) L
        p = w * Xk + (1.0 - w) * Lk
    else:
        raise ValueError(fam)
    K = LAM_GRID.size
    b = np.broadcast_to(Xk, (R, K, n))
    y = np.broadcast_to(Lk, (R, K, n))
    P = np.stack([b, y, p], axis=-1).reshape(R * K, n, 3)
    return P, np.repeat(RHO_GRID, K), np.tile(LAM_GRID, R)


def fit_and_select(x, obs, fams=KINDS, ch=(0, 1, 2), cov_select=False):
    """Fit each family on TR by grid least squares (first grid point wins in-sample ties),
    score it on VA, and return per-family scores, the order-rule call (first-listed family
    with the best score, as np.argmin does in benchmark.py) and the set of families tied
    with the best score."""
    L = onepole(x, RHO_GRID)
    ch = list(ch)
    out = {"val": {}, "train": {}, "load": {}, "rho": {}}
    for f in fams:
        P, rhos, loads = family(f, x, L)
        res_tr = P[:, TR][:, :, ch] - obs[TR][:, ch]
        tr_mse = np.mean(res_tr ** 2, axis=(1, 2))
        g = int(np.argmin(tr_mse))
        out["train"][f], out["rho"][f], out["load"][f] = tr_mse[g], rhos[g], loads[g]
        res_va = P[g, VA][:, ch] - obs[VA][:, ch]
        if cov_select:
            # Gaussian NLL with the contemporaneous error covariance estimated from this
            # candidate's own training residuals (temporal correlation is not modelled).
            S = np.atleast_2d(np.cov(res_tr[g].T))
            q = np.einsum("ti,ij,tj->t", res_va, np.linalg.inv(S), res_va)
            out["val"][f] = 0.5 * (np.linalg.slogdet(S)[1] + q.mean())
        else:
            out["val"][f] = np.mean(res_va ** 2)
    v = np.array([out["val"][f] for f in fams])
    best = v.min()
    out["winners"] = tuple(f for f, s in zip(fams, v) if s <= best + TIE_RTOL * max(1.0, abs(best)))
    out["call"] = fams[int(np.argmin(v))]
    sv = np.sort(v)
    out["margin"] = sv[1] - sv[0]
    return out


def obs_class(kind, lam=0.0):
    """Mechanism labels whose model can reproduce this truth's observables exactly."""
    if kind == "B":
        return {"B"}
    if kind == "A":
        return {"A", "M"}                       # M with lam = 1 reproduces A exactly (E3)
    return {"A", "M"} if lam == 1.0 else {"M"}


def score(kind, call, lam=0.0):
    c = obs_class(kind, lam)
    if call not in c:
        return "wrong"
    return "identified" if len(c) == 1 else "unidentified"


def seq_rng(kind_idx, rep):
    # Common random numbers: replicate `rep` of mechanism `kind_idx` gets the same cue and
    # noise in every condition, so conditions differ only in what is varied.
    return np.random.default_rng([SEED, kind_idx, rep])


def switches(x, idx):
    seg = x[idx[0] - 1: idx[-1] + 1]
    return int(np.sum(seg[1:] != seg[:-1]))


# --------------------------------------------------------------------------- part 1
def part1_math():
    print("\n=== Part 1. Exact observational equivalences [MATH] ===")
    x = cue_blocks(np.random.default_rng(SEED))
    k = RHO
    A, B, M = (truth(K, x) for K in KINDS)
    d = lambda u, v: float(np.max(np.abs(u - v)))
    print(f"[MATH] E1 report only: max|y_A - y_B| = {d(A[:, 1], B[:, 1]):.1e}, "
          f"max|y_A - y_M| = {d(A[:, 1], M[:, 1]):.1e}")
    print(f"[MATH] E2 belief + report: max|(b,y)_A - (b,y)_M| = {d(A[:, :2], M[:, :2]):.1e}")
    e3 = max(d(truth("A", x, lam=l), truth("M", x, lam=1.0)) for l in LAM_GRID)
    print(f"[MATH] E3 A (any report loading) vs M (report loading 1), all channels: max diff = {e3:.1e}")
    # E3b: process noise. M (loading 1) with affect-level noise w and report-process noise u is
    # pathwise A with innovation (1-k)w + u: w reaches the data only through the report filter.
    g = np.random.default_rng([SEED, 3])
    w, u = g.normal(0.0, 0.3, N), g.normal(0.0, 0.2, N)
    YM, zA = np.empty(N), np.empty(N)
    pm = pa = 0.0
    for t in range(N):
        pm = k * pm + (1 - k) * (x[t] + w[t]) + u[t]                 # M: z = x + w, report lag on z
        pa = k * pa + (1 - k) * x[t] + ((1 - k) * w[t] + u[t])       # A: affect lag, one innovation
        YM[t], zA[t] = pm, pa
    print(f"[MATH] E3b with process noise: M (loading 1; affect noise w, report noise u) vs A with "
          f"innovation (1-k)w + u: max diff = {d(YM, zA):.1e}")
    e4 = max(d(truth("A", x, alpha=a), truth("M", x, lam=1.0 - a)) for a in LAM_GRID)
    print(f"[MATH] E4 A whose proxy has a direct cue/belief path (alpha) vs M with report loading "
          f"1 - alpha, every alpha on the grid: max diff = {e4:.1e}")
    e6 = d(truth("M", x, kin=k), truth("A", x))
    print(f"[MATH] E6 M truth with a report-free proxy whose own kinetics equal the report lag, "
          f"vs A: max diff = {e6:.1e}")
    y1 = onepole(onepole(x, 0.6)[0], 0.9)[0]         # affect lag .6, then report lag .9
    y2 = onepole(onepole(x, 0.9)[0], 0.6)[0]         # placements swapped
    print(f"[MATH] E7 unequal lags (.6 at affect, .9 at report) vs swapped: max diff = {d(y1, y2):.1e}; "
          "report-only data identify only the product of the stage filters")
    clip = lambda u: np.clip(u, -0.5, 0.5)
    print(f"[MATH] E7b bounded report scale between the stages, clip(L(x)) vs L(clip(x)): "
          f"max diff = {d(clip(onepole(x, k)[0]), onepole(clip(x), k)[0]):.2f}; "
          "the symmetry breaks only where the nonlinearity's location is declared")


# --------------------------------------------------------------------------- part 2
PUBLISHED_PASS_IV = {   # UNKNOWN_LOADING.md, rows true A, B, M; columns predicted A, B, M
    0.0: [[18, 0, 2], [1, 19, 0], [0, 1, 19]],
    0.5: [[18, 0, 2], [1, 19, 0], [2, 1, 17]],
    0.75: [[18, 0, 2], [1, 19, 0], [6, 1, 13]],
    1.0: [[18, 0, 2], [1, 19, 0], [14, 1, 5]],
}


def part2_ties(nseq):
    print("\n=== Part 2. Ties and nesting in the unknown-loading design ===")
    print("[ARITH] Published Pass IV matrices re-scored by observational class "
          "(A-truth and M-truth at loading 1 can be reproduced by the other model):")
    for lam, m in PUBLISHED_PASS_IV.items():
        tally = {"identified": 0, "unidentified": 0, "wrong": 0}
        for ti, kind in enumerate(KINDS):
            for pi, call in enumerate(KINDS):
                tally[score(kind, call, lam)] += m[ti][pi]
        published = sum(m[i][i] for i in range(3))
        print(f"        report fraction {lam:.2f}: published correct {published}/60 -> identified "
              f"{tally['identified']}, unidentified {tally['unidentified']}, wrong {tally['wrong']}")

    print(f"\n[SIM] Re-implementation, {nseq} sequences per mechanism, iid noise SD {SD}, candidates "
          "A, B, M (free loading); exact ties go to the first-listed candidate as in benchmark.py.")
    base = {}
    for ki, kind in enumerate(("A", "B")):
        base[kind] = []
        for r in range(nseq):
            rng = seq_rng(ki, r)
            x = cue_blocks(rng)
            o = fit_and_select(x, truth(kind, x) + noise(rng))
            o["sw"] = switches(x, VA)
            base[kind].append(o)
    A = base["A"]
    nested = np.mean([o["train"]["M"] <= o["train"]["A"] for o in A])
    tie = np.mean([len(o["winners"]) > 1 for o in A])
    a_only = np.mean([o["winners"] == ("A",) for o in A])
    m_only = np.mean([o["winners"] == ("M",) for o in A])
    print(f"[MATH] In-sample, M fits A-truth at least as well as A itself in {nested:.0%} of sequences "
          "(its grid contains loading 1).")
    print(f"[SIM]  A-truth calls: exact tie with M at loading 1 in {tie:.0%} (broken by list order), "
          f"A strictly better on the selection split in {a_only:.0%}, M better in {m_only:.0%}.")
    print("       None of these is evidence against M.")
    print("\n       true report | order-rule  | identified | unidentified | wrong")
    for lam in (0.0, 0.5, 0.75, 1.0):
        Mrun = []
        for r in range(nseq):
            rng = seq_rng(2, r)
            x = cue_blocks(rng)
            o = fit_and_select(x, truth("M", x, lam=lam) + noise(rng))
            o["sw"] = switches(x, VA)
            Mrun.append(o)
        rows = {"A": A, "B": base["B"], "M": Mrun}
        n = 3 * nseq
        order_ok = sum(o["call"] == k for k, rs in rows.items() for o in rs)
        tally = {"identified": 0, "unidentified": 0, "wrong": 0}
        for k, rs in rows.items():
            for o in rs:
                tally[score(k, o["call"], lam)] += 1
        print(f"       {lam:>11.2f} | {100 * order_ok / n:>9.1f}%  | {100 * tally['identified'] / n:>8.1f}%  "
              f"| {100 * tally['unidentified'] / n:>10.1f}%  | {100 * tally['wrong'] / n:>4.1f}%")
        if lam == 0.0:
            allr = [o for rs in rows.values() for o in rs]
            bad = [o for k, rs in rows.items() for o in rs if score(k, o["call"], lam) == "wrong"]
            if bad:
                print(f"       [SIM] at loading 0: {np.mean([o['sw'] <= 1 for o in bad]):.0%} of wrong calls had "
                      f"<= 1 cue switch in the 48-point selection window (all sequences: "
                      f"{np.mean([o['sw'] <= 1 for o in allr]):.0%})")


# --------------------------------------------------------------------------- part 3
def part3_correlated(nseq):
    print("\n=== Part 3. Correlated-error rivals ===")
    print("3a. Cue-locked shared error, mirror direction: A truth whose proxy partly tracks the cue/")
    print("    belief directly (weight alpha). Pass IV pipeline unchanged: M gets a free report loading,")
    print("    A gets no free proxy loading. Share of A-truth sequences called 'report lag': [SIM]")
    for sd in (0.4, 0.12):
        cells = []
        for alpha in (0.0, 0.25, 0.5, 1.0):
            calls = []
            for r in range(nseq):
                rng = seq_rng(0, r)
                x = cue_blocks(rng)
                calls.append(fit_and_select(x, truth("A", x, alpha=alpha) + noise(rng, sd=sd))["call"])
            cells.append(f"alpha {alpha:.2f}: {np.mean([c == 'M' for c in calls]):4.0%}")
        print(f"    noise SD {sd:<4}  " + "   ".join(cells))
    same = []
    for r in range(max(nseq // 3, 20)):
        rng = seq_rng(0, r)
        x = cue_blocks(rng)
        alpha = float(rng.uniform())
        v = fit_and_select(x, truth("A", x, alpha=alpha) + noise(rng), fams=("A+", "B", "M"))["val"]
        same.append(abs(v["A+"] - v["M"]) <= TIE_RTOL * max(1.0, v["M"]))
    print(f"    [SIM] Give A the same freedom (free cue loading, 'A+'): A+ and M have identical validation "
          f"scores in {np.mean(same):.0%} of sequences (alpha drawn uniformly; E4).")

    print("\n3b. Cue-independent: report and proxy errors share an AR(1) component (phi .9, share .8),")
    print("    marginal SD .4. Rates over A, B, M truths; 'wrong' = call outside the truth's observational")
    print("    class. Nominal LR = winner vs runner-up, as if the criterion's error model were right. [SIM]")
    print("    true    criterion                      wrong   share of wrong calls  fitted lag of true")
    print("    loading                                calls   with nominal LR>20    model, mean (SD)")
    for lam in (0.0, 0.75):
        for label, phi, r, cov in (("iid noise, SSE", 0.0, 0.0, False),
                                   ("shared AR(1), SSE", 0.9, 0.8, False),
                                   ("shared AR(1), covariance NLL", 0.9, 0.8, True)):
            wrong = strong_wrong = tot = 0
            rho_hat = []
            for ki, kind in enumerate(KINDS):
                for rep in range(nseq):
                    rng = seq_rng(ki, rep)
                    x = cue_blocks(rng)
                    obs = truth(kind, x, lam=lam if kind == "M" else 0.0) + noise(rng, phi=phi, r=r)
                    o = fit_and_select(x, obs, cov_select=cov)
                    tot += 1
                    bad = score(kind, o["call"], lam) == "wrong"
                    wrong += bad
                    rho_hat.append(o["rho"][kind])
                    ll = o["margin"] * len(VA) * (1 if cov else 3 / (2 * SD ** 2))
                    strong_wrong += bad and ll > np.log(20)
            print(f"    {lam:<7.2f} {label:<30} {100 * wrong / tot:5.1f}%   {100 * strong_wrong / max(wrong, 1):5.1f}%"
                  f"                {np.mean(rho_hat):.3f} ({np.std(rho_hat):.3f})")
    print("    (generating lag .78; nearest grid points .775 and .800)")


# --------------------------------------------------------------------------- part 4
def part4_anchor(nsim):
    print("\n=== Part 4. Cheapest discriminating manipulation: anchor x cue (x delay) [SIM] ===")
    print("Trial: steady state at x = -1; pre-cue rating on item 1; cue randomised (switch to +1, or stay);")
    print("first post-cue rating after delay d, randomised, either on item 1 again ('repeat') or on a parallel")
    print("item this person has never answered ('fresh'), randomised. No ratings in between.")
    print("Lag coefficients .78 per step; rating noise SD .4. Entries: mean cue effect, 1 = full update.")
    ds = np.array([1, 2, 4, 8, 16])
    a = k = RHO

    def eff(mech, d, fresh, delta=1.0, react=0.0, kk=k):
        if mech == "A":            # clock-time affect lag; prompt reactivity speeds updating at the prompt
            e = 1 - a ** d
            return e + react * (1 - e)
        if mech == "M_anchor":     # rating anchored on own last answer to this item, weight kk*delta^d
            return np.ones_like(d, float) if fresh else 1 - kk * delta ** d
        if mech == "M_clock":      # report state relaxing in clock time, not tied to answers (repo's M)
            return 1 - k ** d
        raise ValueError(mech)

    # (name, mechanism, kwargs, fresh-item scale factor, fresh-item additive offset)
    mechs = (("A  affect lag", "A", {}, 0.0, 0.0),
             ("A  + prompt reactivity .3", "A", {"react": 0.3}, 0.0, 0.0),
             ("A  + fresh item: scale x1.1, offset +.2", "A", {}, 0.10, 0.2),
             ("M  anchored on last answer", "M_anchor", {}, 0.0, 0.0),
             ("M  anchor fades .78/step", "M_anchor", {"delta": 0.78}, 0.0, 0.0),
             ("M  weak anchor (.3), fading", "M_anchor", {"delta": 0.78, "kk": 0.3}, 0.0, 0.0),
             ("M  clock-time report lag (repo)", "M_clock", {}, 0.0, 0.0))
    print("\n  mechanism                          item    " + " ".join(f"d={d:<4}" for d in ds))
    for name, base, kw, scale, off in mechs:
        if scale or off:
            continue
        for fresh in (False, True):
            v = eff(base, ds.astype(float), fresh, **kw)
            print(f"  {name:<34} {'fresh' if fresh else 'repeat':<7} " + " ".join(f"{u:5.2f} " for u in v))

    def one_study(base, kw, scale, off, ntr, ratio_test):
        d = rng.choice(ds, ntr).astype(float)
        fresh = rng.random(ntr) < 0.5
        sw = rng.random(ntr) < 0.5
        u = rng.choice([-1.0, 1.0], ntr) if ratio_test else -np.ones(ntr)   # starting level
        e = np.where(fresh, eff(base, d, True, **kw), eff(base, d, False, **kw))
        load = rng.normal(1.0, 0.1, ntr) * (1.0 + scale * fresh)
        y = load * u * (1.0 - 2.0 * sw * e) + off * fresh + rng.normal(0.0, SD, ntr)
        if not ratio_test:         # difference-in-differences regression with delay-specific cue effects
            X = np.column_stack([np.ones(ntr), fresh] + [sw * (d == v) for v in ds] + [sw * fresh])
            beta, *_ = np.linalg.lstsq(X, y, rcond=None)
            res = y - X @ beta
            V = np.linalg.inv(X.T @ X) * (res @ res) / (ntr - X.shape[1])
            return abs(beta[-1]) / np.sqrt(V[-1, -1]) > 1.96
        w = y * u                  # sign-aligned; an additive item offset averages out
        E, var = [], []
        for g in (True, False):    # scale-free normalised cue effect per item type: 1 - mean(sw)/mean(stay)
            w1, w0 = w[(fresh == g) & sw], w[(fresh == g) & ~sw]
            m1, m0 = w1.mean(), w0.mean()
            E.append(1.0 - m1 / m0)
            var.append(w1.var(ddof=1) / w1.size / m0 ** 2 + m1 ** 2 * w0.var(ddof=1) / w0.size / m0 ** 4)
        return abs(E[0] - E[1]) / np.sqrt(var[0] + var[1]) > 1.96

    rng = np.random.default_rng([SEED, 4])
    sizes = (160, 640)   # e.g. 40 or 160 people x 4 trials, fresh items drawn from a parallel-item pool
    print("\n  Share of simulated studies rejecting 'no anchoring' (two-sided .05; item loadings N(1, .1^2)")
    print(f"  per trial with roles randomised; {nsim} studies per cell):")
    print("    (i)  cue x item regression, all trials start at -1")
    print("    (ii) scale-free ratio test, starting level randomised to -1 or +1 (recommended)")
    print("    mechanism                                 (i) 160   (i) 640   (ii) 160  (ii) 640")
    for name, base, kw, scale, off in mechs:
        cells = []
        for ratio_test in (False, True):
            for ntr in sizes:
                rej = sum(one_study(base, kw, scale, off, ntr, ratio_test) for _ in range(nsim))
                cells.append(f"{100 * rej / nsim:6.1f}%")
        print(f"    {name:<40} " + "   ".join(cells))
    print("  Delay alone does not separate a fading anchor from affect lag (compare their 'repeat' rows).")
    print("  The repo's clock-time report lag stays equivalent to A here, as E1 requires.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    nseq = 40 if args.quick else 300
    print(f"lag_audit.py | numpy {np.__version__} | seed {SEED} | {nseq} sequences per mechanism")
    part1_math()
    part2_ties(nseq)
    part3_correlated(nseq)
    part4_anchor(200 if args.quick else 1000)


if __name__ == "__main__":
    main()
