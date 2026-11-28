"""R-006d: cross-implementation parity of the R-006 T1 statistic (Claude, 2026-11-28).

Synthetic data only. No human data, no network. Preregistered as R-006d in
research-log/prediction-register.md on this branch before the N3h run.

The question: ER #14 (GPT-6) reported an N3h corrected-T1 mean of -0.0783 (SD 0.2635)
against -0.0263 (SD 0.3389) in ER #13 (Claude), and called the two "not matching
sampling distributions". Claude's 11-23 reply on #14 proposed a heavy-tail artefact.
This script separates the two possible sources:

  E1  estimator parity: run BOTH estimators on the SAME simulated datasets;
  E2  simulator parity: compare the T1 distributions from the two simulators;
  E0  reproduction: regenerate #13's stored per-replicate values and #14's summary;
  E3  tail mechanism: does an extreme T1 go with a small pooled denominator?

Both code trees are imported unmodified from clean `git archive` exports:
  dir13 = experiments/r006-lagged-moment-identification at ER #13 head 8bf4650
  dir14 = experiments/r006-independent-validation      at ER #14 head 358abdd

Usage:
  python -I n3h_parity.py DIR13 DIR14 [--world N3h] [--reps 200] [--workers 2] [--out FILE]
Writes one JSON file with per-replicate values and the summary, and prints the summary.
"""
import argparse
import csv
import gzip
import json
import sys
import time
from multiprocessing import Pool

import numpy as np
from scipy import stats as sps

N_PERSONS = 127
G_ORDER = ['W0', 'N3', 'N3h', 'N8', 'W1s+N8', 'W1w+N8', 'N6', 'N7']   # #14 seed order
C_BOOT, G_BOOT = 499, 199                                          # as each branch ran
LM = SIM = G = None


def load(dir13, dir14):
    global LM, SIM, G
    sys.path.insert(0, dir14)
    sys.path.insert(0, dir13)
    import lagmom
    import simulate
    import calibrate_t1_independent
    LM, SIM, G = lagmom, simulate, calibrate_t1_independent


# ----------------------------------------------------------------- estimators
def claude_t1(Y3, correct, counts):
    """#13's within-person T1 on a 3-item array, exactly as lagmom.analyse computes it.
    Returns the point estimate, its 95% bootstrap interval, and the pooled numerator and
    denominator (recomputed with compute_within's own lines and checked bit-for-bit)."""
    person = np.repeat(np.arange(N_PERSONS), 2)
    lmo = LM.LagMoments(Y3, (0, 1, 2), True, lags=(0, 1, 2, 3), correct=correct, jk=True)
    st = [s for s in LM.t1_stats('all') if s.name == 'T1']
    cache = {}
    est, draws = LM.compute_within(lmo, st, person, N_PERSONS, counts, cache)
    lo, hi = LM.ci(draws['T1'])
    # the same quantities compute_within forms internally, for the diagnostics
    w = lmo.n_pairs1.astype(float)
    num = LM.eval_terms(lmo, st[0].num_terms, cache)
    den = LM.eval_terms(lmo, st[0].den_terms, cache)
    okm = lmo.keep & np.isfinite(num) & np.isfinite(den)
    pn = LM.person_sums(w * np.where(okm, num, 0.0), person, okm, N_PERSONS)
    pd = LM.person_sums(w * np.where(okm, den, 0.0), person, okm, N_PERSONS)
    assert pn.sum() / pd.sum() == est['T1']
    return dict(t1=float(est['T1']), lo=lo, hi=hi, num=float(pn.sum()), den=float(pd.sum()),
                pn=pn, n_pp=int(lmo.keep.sum()), jk_fallback=int(lmo.jk_fallback.sum()))


def gpt_t1(Y3, cor, rep):
    """#14's T1 via its own run(), plus the pooled numerator and denominator recomputed
    with run()'s own lines and checked bit-for-bit against run()['t1']."""
    r = G.run(Y3, cor=cor, nboot=G_BOOT, seed=rep)
    # --- lines copied from calibrate_t1_independent.run (point-estimate path only)
    gs, qs, cnt, keep, _ = G.estimate(Y3, drop_day=None, cor=cor)
    Dcount = np.isfinite(Y3).all(-1).any(-1).sum(-1)
    allgs, allqs, allok = [], [], []
    for d in range(G.D):
        g, q, n, ok, version_ok = G.estimate(Y3, drop_day=d, cor=cor)
        allgs.append(g); allqs.append(q); allok.append(version_ok)
    allgs, allqs, allok = np.array(allgs), np.array(allqs), np.array(allok)
    observedday = np.isfinite(Y3).all(-1).any(-1).T
    valid_l = (allok | ~observedday).all(axis=0) & keep
    weights = observedday[:, :, None]
    avg_g = (allgs * weights).sum(axis=0) / np.maximum(Dcount[:, None], 1)
    avg_q = (allqs * weights).sum(axis=0) / np.maximum(Dcount[:, None], 1)
    gj = np.where(valid_l[:, None], Dcount[:, None] * gs - (Dcount[:, None] - 1) * avg_g, gs)
    qj = np.where(valid_l[:, None], Dcount[:, None] * qs - (Dcount[:, None] - 1) * avg_q, qs)
    wg = (cnt[:, None] * gj).sum(-1).reshape(N_PERSONS, 2)
    wq = (cnt[:, None] * qj).sum(-1).reshape(N_PERSONS, 2)
    wg = (wg * keep.reshape(N_PERSONS, 2)).sum(-1)
    wq = (wq * keep.reshape(N_PERSONS, 2)).sum(-1)
    # ---
    assert wg.sum() / wq.sum() == r['t1']
    return dict(t1=r['t1'], lo=r['lo'], hi=r['hi'], fire=r['fire'], num=float(wg.sum()),
                den=float(wq.sum()), pn=wg, n_pp=r['used'], jk_fallback=r['fallback'])


def claude_t1_iters(Y3, iters):
    """#13's corrected T1 with its Newton solver capped at `iters` (default 50). Used only
    to test whether any E1 exception comes from the 40-versus-50 iteration difference."""
    old = LM.solve_latent_r.__defaults__
    LM.solve_latent_r.__defaults__ = (iters,)
    try:
        one = np.ones((1, N_PERSONS))
        return claude_t1(Y3, True, one)['t1']
    finally:
        LM.solve_latent_r.__defaults__ = old


def concentration(pn):
    """Largest single person's share of the numerator's absolute mass."""
    a = np.abs(pn)
    return float(a.max() / a.sum()) if a.sum() > 0 else float('nan')


# ----------------------------------------------------------------- one replicate
def one(args):
    world, rep = args
    t0 = time.time()
    seed_c = 100000 * (list(SIM.WORLDS).index(world) + 1) + rep        # #13 bench.run_one
    Y5, _ = SIM.simulate(SIM.WORLDS[world], seed=seed_c)
    data = {'C': Y5[..., list(LM.NA_IDX)]}
    seed_g = 100000 * (G_ORDER.index(world) + 1) + rep                  # #14 main()
    data['G'] = G.sim(np.random.default_rng(seed_g), world)
    counts = LM.boot_counts(N_PERSONS, C_BOOT, np.random.default_rng(rep))   # #13 analyse
    row = dict(rep=rep, seed_c=seed_c, seed_g=seed_g)
    for dname, Y in data.items():
        for tag, corr in (('cor', True), ('lin', False)):
            c = claude_t1(Y, corr, counts)
            g = gpt_t1(Y, corr, rep)
            for est, res in (('C', c), ('G', g)):
                k = f'{dname}data_{est}est_{tag}'
                row[k] = {x: v for x, v in res.items() if x != 'pn'}
                row[k]['conc'] = concentration(res['pn'])
        row[f'{dname}data_Cest_cor']['t1_iters40'] = claude_t1_iters(Y, 40)
        row[f'{dname}data_Cest_cor']['t1_iters200'] = claude_t1_iters(Y, 200)
    row['seconds'] = round(time.time() - t0, 2)
    return row


# ----------------------------------------------------------------- summaries
def describe(x):
    x = np.asarray(x, float)
    return dict(n=int(x.size), mean=float(x.mean()), sd=float(x.std(ddof=1)),
                median=float(np.median(x)), trim10=float(sps.trim_mean(x, 0.1)),
                kurtosis_pearson=float(sps.kurtosis(x, fisher=False, bias=False)),
                min=float(x.min()), max=float(x.max()))


def boot_diff(a, b, fn, n=10000, seed=20261128):
    """Two-sample bootstrap 95% percentile CI for fn(a) - fn(b); fn takes an axis."""
    rng = np.random.default_rng(seed)
    a, b = np.asarray(a, float), np.asarray(b, float)
    ia = rng.integers(0, a.size, (n, a.size))
    ib = rng.integers(0, b.size, (n, b.size))
    d = fn(a[ia], axis=1) - fn(b[ib], axis=1)
    return float(fn(a, axis=0) - fn(b, axis=0)), [float(np.quantile(d, .025)), float(np.quantile(d, .975))]


def stored_13(dir13, world):
    """#13's stored per-replicate w_T1 (cor, lin) and its 95% interval, as printed."""
    out = {}
    with gzip.open(f'{dir13}/results/bench_per_replicate.csv.gz', 'rt') as fh:
        for r in csv.DictReader(fh):
            if r['world'] == world:
                out[(int(r['rep']), r['version'])] = (r['w_T1'], r['w_T1_lo'], r['w_T1_hi'], int(r['seed']))
    return out


def printed_match(value, text, rel=5e-5):
    """True if `value` agrees with a printed 5-significant-figure number."""
    v = float(text)
    return abs(value - v) <= rel * max(abs(v), 1e-3)


def summarise(rows, dir13, dir14, world):
    S = {}
    reps = [r['rep'] for r in rows]
    get = lambda key, f='t1': np.array([r[key][f] for r in rows], float)

    # E0a: #13 stored values regenerate (C data, C estimator) at printed precision
    st = stored_13(dir13, world)
    e0a = {}
    for tag in ('cor', 'lin'):
        ok_t1 = ok_ci = seeds = 0
        bad = []
        for r in rows:
            if (r['rep'], tag) not in st:
                continue
            t1s, los, his, seed = st[(r['rep'], tag)]
            res = r[f'Cdata_Cest_{tag}']
            seeds += seed == r['seed_c']
            m1 = printed_match(res['t1'], t1s)
            m2 = printed_match(res['lo'], los) and printed_match(res['hi'], his)
            ok_t1 += m1
            ok_ci += m2
            if not (m1 and m2):
                bad.append([r['rep'], res['t1'], t1s, res['lo'], los])
        e0a[tag] = dict(stored=sum(1 for k in st if k[1] == tag), t1_match=ok_t1,
                        ci_match=ok_ci, seed_match=seeds, mismatches=bad[:10])
    S['E0a_reproduce_13'] = e0a

    # E0b: #14 stored summary regenerates (G data, G estimator)
    js = json.load(open(f'{dir14}/results/t1_targeted_calibration_summary.json'))['data'].get(world)
    t1c, t1l = get('Gdata_Gest_cor'), get('Gdata_Gest_lin')
    lin_fire = [r['Gdata_Gest_lin']['fire'] for r in rows]
    mine = dict(n=len(rows), fires=int(sum(r['Gdata_Gest_cor']['fire'] for r in rows)),
                mean=float(t1c.mean()), sd=float(t1c.std(ddof=1)),
                linear_fires=int(sum(lin_fire)), linear_mean=float(t1l.mean()))
    S['E0b_reproduce_14'] = dict(stored=js, regenerated=mine)

    # E1: estimator parity on the same datasets
    e1 = {}
    for d in ('C', 'G'):
        for tag in ('cor', 'lin'):
            c, g = get(f'{d}data_Cest_{tag}'), get(f'{d}data_Gest_{tag}')
            diff = np.abs(c - g)
            tol = np.maximum(1e-8, 1e-8 * np.abs(c))
            cd, gd = get(f'{d}data_Cest_{tag}', 'den'), get(f'{d}data_Gest_{tag}', 'den')
            e1[f'{d}data_{tag}'] = dict(
                n=int(c.size), within_tol_1e8=int((diff <= tol).sum()), within_abs_1e9=int((diff <= 1e-9).sum()),
                max_abs_diff=float(diff.max()), max_rel_den_diff=float(np.max(np.abs(cd - gd) / np.abs(cd))),
                worst=[[int(reps[i]), float(c[i]), float(g[i])] for i in np.argsort(-diff)[:5]])
    # E1b: the Newton cap. #13 at 40 iterations against #14 (which stops at 40); and
    # #13 at 50 or 40 against 200 iterations, to see whether any solve is unconverged.
    for d in ('C', 'G'):
        g = get(f'{d}data_Gest_cor')
        c40, c50, c200 = (get(f'{d}data_Cest_cor', f) for f in ('t1_iters40', 't1', 't1_iters200'))
        tol = lambda x: np.maximum(1e-8, 1e-8 * np.abs(x))
        e1[f'{d}data_cor_newton'] = dict(
            c40_vs_g_within_tol=int((np.abs(c40 - g) <= tol(c40)).sum()),
            c50_vs_c200_within_tol=int((np.abs(c50 - c200) <= tol(c200)).sum()),
            c40_vs_c200_within_tol=int((np.abs(c40 - c200) <= tol(c200)).sum()),
            max_abs_c50_minus_c200=float(np.abs(c50 - c200).max()),
            max_abs_c40_minus_c200=float(np.abs(c40 - c200).max()))
    S['E1_estimator_parity'] = e1

    # E2: distributions; the original comparison is C-pipeline vs G-pipeline
    e2 = {}
    for est in ('C', 'G'):
        for tag in ('cor', 'lin'):
            a, b = get(f'Gdata_{est}est_{tag}'), get(f'Cdata_{est}est_{tag}')
            md, md_ci = boot_diff(a, b, np.median)
            tm, tm_ci = boot_diff(a, b, lambda x, axis: sps.trim_mean(x, 0.1, axis=axis))
            welch = (a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / a.size + b.var(ddof=1) / b.size)
            ks = sps.ks_2samp(a, b)
            e2[f'{est}est_{tag}'] = dict(Gdata=describe(a), Cdata=describe(b),
                                         median_diff_G_minus_C=[md, md_ci],
                                         trim10_diff_G_minus_C=[tm, tm_ci],
                                         welch_z=float(welch), ks_D=float(ks.statistic), ks_p=float(ks.pvalue))
    S['E2_distributions'] = e2
    S['pipelines_as_published'] = dict(C13=describe(get('Cdata_Cest_cor')), G14=describe(get('Gdata_Gest_cor')))

    # E3: tail mechanism (corrected T1, each estimator on its own data, then pooled)
    e3 = {}
    for d, est in (('C', 'C'), ('G', 'G')):
        t1, den = get(f'{d}data_{est}est_cor'), get(f'{d}data_{est}est_cor', 'den')
        conc = get(f'{d}data_{est}est_cor', 'conc')
        dev = np.abs(t1 - np.median(t1))
        tail = dev >= np.quantile(dev, 0.95)
        e3[f'{d}data_{est}est'] = dict(
            spearman_dev_vs_den=float(sps.spearmanr(dev, den).statistic),
            spearman_dev_vs_conc=float(sps.spearmanr(dev, conc).statistic),
            den_median=float(np.median(den)), den_min=float(den.min()),
            den_median_in_top5pct_dev=float(np.median(den[tail])),
            conc_median=float(np.median(conc)), conc_median_in_top5pct_dev=float(np.median(conc[tail])))
    S['E3_tail_mechanism'] = e3
    S['seconds_per_rep_median'] = float(np.median([r['seconds'] for r in rows]))
    return S


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dir13')
    ap.add_argument('dir14')
    ap.add_argument('--world', default='N3h')
    ap.add_argument('--reps', type=int, default=200)
    ap.add_argument('--start', type=int, default=0)
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--out', default='results/n3h_parity.json')
    a = ap.parse_args()
    load(a.dir13, a.dir14)
    import warnings
    warnings.filterwarnings('ignore')
    jobs = [(a.world, r) for r in range(a.start, a.start + a.reps)]
    t0 = time.time()
    with Pool(a.workers, initializer=load, initargs=(a.dir13, a.dir14)) as pool:
        rows = []
        for i, row in enumerate(pool.imap(one, jobs)):
            rows.append(row)
            if (i + 1) % 20 == 0:
                print(f'{i + 1}/{len(jobs)} reps, {time.time() - t0:.0f}s', flush=True)
    S = summarise(rows, a.dir13, a.dir14, a.world)
    S['_meta'] = dict(world=a.world, reps=a.reps, start=a.start, seconds=round(time.time() - t0, 1),
                      python=sys.version.split()[0], numpy=np.__version__,
                      scipy=__import__('scipy').__version__, c_boot=C_BOOT, g_boot=G_BOOT)
    with open(a.out, 'w') as fh:
        json.dump(dict(summary=S, rows=rows), fh, indent=1)
    print(json.dumps(S, indent=1))


if __name__ == '__main__':
    main()
