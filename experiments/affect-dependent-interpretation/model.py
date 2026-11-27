"""Affect-dependent belief update: exact finite-state illustration.

Illustrative model only. No human data, no fitted parameters, no causal claims
about people. Every probability is an exact rational number (fractions.Fraction).

State (e, k): affect e in {S, A} (low / high alarm) and a threat-credence level
k in {0..N} (belief b = k/N that the situation is threatening). Each step:

  1. the person chooses an action u in {none, correct, reinforce} from their
     own information, here declared to be (e, k) (full self-observation);
  2. a cue o arrives (ambiguous by default; 'threat' during a pulse);
  3. belief updates: k' ~ B(. | k, o, u, e)      <- e enters B: the extension
  4. affect updates: e' = A with prob rho*[e = A] + (1 - rho) * k'/N.

B is split into the parts that the note keeps apart:
  - interpretation   up[e], down[e]: how the same ambiguous cue moves k in state e;
  - reasoning capacity  omega[e]: probability that a reasoning attempt changes k;
  - reasoning direction: 'correct' moves k toward the reference reading
    (benign here, k - 1); 'reinforce' moves k toward the reading congruent
    with current affect (k + 1 in A, k - 1 in S); 'none' leaves it;
  - selection: which action the person's *usual* policy pi0 picks in state e.
    Selection is a property of a policy, not of B.

The original model is the nested baseline in which up, down and omega do not
depend on e. The fitting response is stipulated as S (q on the benign reading,
J(A) = 1, J(S) = 0), as in theory/model.md's worked example.

Run:  python3 model.py            (prints all tables in README.md)
      python3 model.py --check    (assertions only)
"""
import argparse
from fractions import Fraction as F
from itertools import product

S, A = 'S', 'A'
ACTIONS = ('none', 'correct', 'reinforce')


class Spec:
    def __init__(self, name, N=4, rho=F(1, 2), up=None, down=None, omega=None):
        self.name, self.N, self.rho = name, N, F(rho)
        self.up = {e: F(v) for e, v in (up or {S: 0, A: 0}).items()}
        self.down = {e: F(v) for e, v in (down or {S: F(1, 2), A: F(1, 2)}).items()}
        self.omega = {e: F(v) for e, v in (omega or {S: F(1, 2), A: F(1, 2)}).items()}
        for d in (self.up, self.down, self.omega):
            assert all(0 <= v <= 1 for v in d.values())
        for e in (S, A):
            assert self.up[e] + self.down[e] <= 1

    def states(self):
        return [(e, k) for e in (S, A) for k in range(self.N + 1)]

    def clip(self, k):
        return max(0, min(self.N, k))

    def belief_kernel(self, e, k, cue, u):
        """Distribution over k' given current affect e (the extension's input)."""
        out = {}
        if cue == 'threat':                      # credible threat cue, read the same in any state
            after_cue = {self.clip(k + 1): F(1)}
        else:                                    # ambiguous cue, read through current affect
            after_cue = {}
            for kk, p in ((k + 1, self.up[e]), (k - 1, self.down[e]),
                          (k, 1 - self.up[e] - self.down[e])):
                if p:
                    after_cue[self.clip(kk)] = after_cue.get(self.clip(kk), 0) + p
        for k1, p1 in after_cue.items():
            if u == 'none':
                moves = {k1: F(1)}
            else:
                step = -1 if u == 'correct' else (+1 if e == A else -1)
                w = self.omega[e]
                moves = {}
                for kk, p in ((self.clip(k1 + step), w), (k1, 1 - w)):
                    if p:
                        moves[kk] = moves.get(kk, 0) + p
            for k2, p2 in moves.items():
                out[k2] = out.get(k2, 0) + p1 * p2
        return out

    def step(self, state, u, cue='ambiguous'):
        e, k = state
        out = {}
        for k2, pb in self.belief_kernel(e, k, cue, u).items():
            pa = self.rho * (e == A) + (1 - self.rho) * F(k2, self.N)
            for e2, pe in ((A, pa), (S, 1 - pa)):
                if pe:
                    out[(e2, k2)] = out.get((e2, k2), 0) + pb * pe
        assert sum(out.values()) == 1
        return out


# ---------- policies ----------------------------------------------------------

def policy_none(state):
    return {'none': F(1)}


def policy_always(u):
    return lambda state: {u: F(1)}


def pi0_threshold(kstar, r):
    """Usual behaviour with affect-dependent selection: in A at or above the
    threshold k*, reinforce with prob r; otherwise do nothing. A hypothesis
    about selection, not an established property."""
    def pol(state):
        e, k = state
        if e == A and k >= kstar:
            return {'reinforce': F(r), 'none': 1 - F(r)}
        return {'none': F(1)}
    return pol


def pi0_ramp(r_by_k):
    def pol(state):
        e, k = state
        r = F(r_by_k[k]) if e == A else F(0)
        return {'reinforce': r, 'none': 1 - r} if r else {'none': F(1)}
    return pol


# ---------- exact computations -----------------------------------------------

def propagate(spec, dist, policy, steps, cue='ambiguous'):
    for _ in range(steps):
        new = {}
        for s, ps in dist.items():
            for u, pu in policy(s).items():
                for s2, p2 in spec.step(s, u, cue).items():
                    new[s2] = new.get(s2, 0) + ps * pu * p2
        dist = new
    return dist


def p_endpoint_S(dist):
    return sum(p for (e, _), p in dist.items() if e == S)


def max_endpoint_S(spec, h):
    """sup over (full-self-observation) policies of Pr(e_{t+h} = S | start),
    by backward induction; deterministic Markov policies suffice here."""
    V = {s: F(s[0] == S) for s in spec.states()}
    for _ in range(h):
        V = {s: max(sum(p * V[s2] for s2, p in spec.step(s, u).items()) for u in ACTIONS)
             for s in spec.states()}
    return V


def value_fixed(spec, policy, h, target):
    V = {s: F(target(s)) for s in spec.states()}
    for _ in range(h):
        V = {s: sum(pu * sum(p * V[s2] for s2, p in spec.step(s, u).items())
                    for u, pu in policy(s).items()) for s in spec.states()}
    return V


def closed_classes(spec, policy):
    states = spec.states()
    succ = {s: {s2 for u, pu in policy(s).items() if pu for s2, p in spec.step(s, u).items() if p}
            for s in states}
    reach = {}
    for s in states:
        seen, stack = {s}, [s]
        while stack:
            x = stack.pop()
            for y in succ[x]:
                if y not in seen:
                    seen.add(y); stack.append(y)
        reach[s] = seen
    classes = []
    for s in states:
        if all(s in reach[y] for y in reach[s]):      # s's reachable set is a closed class
            c = frozenset(reach[s])
            if c not in classes:
                classes.append(c)
    return classes


def solve(M, b):
    """Exact Gaussian elimination over Fractions."""
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(M)]
    for c in range(n):
        piv = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def absorption_and_time(spec, policy, target_set):
    """Exact Pr(ever hit target_set) and, where it is 1, expected hitting time."""
    states = [s for s in spec.states() if s not in target_set]
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    P = [[F(0)] * n for _ in range(n)]
    hit = [F(0)] * n
    for s in states:
        for u, pu in policy(s).items():
            for s2, p in spec.step(s, u).items():
                if s2 in target_set:
                    hit[idx[s]] += pu * p
                else:
                    P[idx[s]][idx[s2]] += pu * p
    # states that cannot reach target have hit prob 0; restrict linear solve to the rest
    can = set(target_set)
    changed = True
    while changed:
        changed = False
        for s in states:
            if s not in can and any(s2 in can for u, pu in policy(s).items() if pu
                                    for s2, p in spec.step(s, u).items() if p):
                can.add(s); changed = True
    live = [s for s in states if s in can]
    li = {s: i for i, s in enumerate(live)}
    m = len(live)
    M = [[(F(1) if i == j else F(0)) - P[idx[a]][idx[b]] for j, b in enumerate(live)]
         for i, a in enumerate(live)]
    h = solve(M, [hit[idx[a]] for a in live]) if m else []
    H = {s: (h[li[s]] if s in li else F(0)) for s in states}
    T = None
    if all(H[s] == 1 for s in states):
        T = dict(zip(states, solve([[(F(1) if i == j else F(0)) - P[i][j] for j in range(n)]
                                     for i in range(n)], [F(1)] * n)))
    return H, T


# ---------- specifications ---------------------------------------------------

HALF, QUARTER = F(1, 2), F(1, 4)
B0 = Spec('B0 baseline (original model, nested)')
E1 = Spec('E1 interpretation only', up={S: 0, A: HALF}, down={S: HALF, A: 0})
E2 = Spec('E2 interpretation + reduced capacity', up={S: 0, A: HALF}, down={S: HALF, A: 0},
          omega={S: HALF, A: QUARTER})
E3 = Spec('E3 interpretation + no capacity in A', up={S: 0, A: HALF}, down={S: HALF, A: 0},
          omega={S: HALF, A: 0})
C1 = Spec('C1 capacity only', omega={S: HALF, A: QUARTER})
R9 = Spec('R9 slow-affect rival (rho = 9/10, no e in B)', rho=F(9, 10))
SPECS = (B0, E1, E2, E3, C1, R9)
START = (A, 4)          # high alarm, threat credence 1
NA = (A, 4)
Z = (S, 0)


def fmt(x, nd=3):
    return f'{float(x):.{nd}f}'


def run(check_only=False):
    out = []
    say = out.append

    # 1. Nesting: with e-independent parameters B does not depend on e.
    for s in SPECS:
        indep = all(s.up[S] == s.up[A] and s.down[S] == s.down[A] and s.omega[S] == s.omega[A]
                    for _ in [0])
        for k, cue, u in product(range(s.N + 1), ('ambiguous', 'threat'), ('none', 'correct')):
            if indep:
                assert s.belief_kernel(S, k, cue, u) == s.belief_kernel(A, k, cue, u)
        if indep:
            # 'reinforce' = an e-indexed choice between two e-independent actions:
            # 'raise' (k+1 w.p. omega) in A and 'lower' (k-1 w.p. omega, same as 'correct') in S.
            # So in the baseline, reinforcing is selection, and B stays e-independent.
            for k, cue in product(range(s.N + 1), ('ambiguous', 'threat')):
                lower = s.belief_kernel(S, k, cue, 'correct')
                assert s.belief_kernel(S, k, cue, 'reinforce') == lower
                assert s.belief_kernel(A, k, cue, 'correct') == lower

    # 2. Equilibria under the passive policy (no reasoning), identical ambiguous cues.
    say('## Closed classes under no reasoning, identical ambiguous cues')
    for s in SPECS:
        cls = closed_classes(s, policy_none)
        say(f'- {s.name}: {len(cls)} closed class(es): '
            + '; '.join('{' + ', '.join(f'{e}{k}' for e, k in sorted(c)) + '}' for c in cls))
    assert len(closed_classes(B0, policy_none)) == 1
    assert sorted(map(sorted, closed_classes(E1, policy_none))) == [[NA], [Z]]
    say('Under always-correct reasoning: '
        + '; '.join(f'{s.name.split()[0]}: {len(closed_classes(s, policy_always("correct")))}'
                    for s in SPECS) + ' closed class(es).')
    assert len(closed_classes(E1, policy_always('correct'))) == 1
    assert len(closed_classes(E2, policy_always('correct'))) == 1
    assert len(closed_classes(E3, policy_always('correct'))) == 2

    # 3. Path dependence: probability of ending absorbed in (S,0), by start, E1, passive.
    H1, _ = absorption_and_time(E1, policy_none, {Z})
    say('\n## E1, no reasoning: Pr(eventually absorbed at S0) by starting state')
    say('| start | ' + ' | '.join(f'k={k}' for k in range(5)) + ' |')
    say('|---|' + '---|' * 5)
    for e in (S, A):
        say(f'| {e} | ' + ' | '.join(fmt(H1[(e, k)]) if (e, k) != Z else '1' for k in range(5)) + ' |')
    H0, T0 = absorption_and_time(B0, policy_none, {Z})
    assert all(v == 1 for v in H0.values())
    assert H1[NA] == 0 and 0 < H1[(A, 2)] < 1

    # 4. Metastability: down[A] = eps > 0 restores one closed class; dwell time.
    say('\n## Knife-edge: interpretation leak eps = down[A], no reasoning')
    say('| eps | closed classes | E[steps to S0 from A4] |')
    say('|---|---|---|')
    dwell = {}
    for eps in (F(1, 2), F(1, 4), F(1, 8), F(1, 16), F(1, 64), F(1, 256)):
        s = Spec('E1eps', up={S: 0, A: min(HALF, 1 - eps)}, down={S: HALF, A: eps})
        nc = len(closed_classes(s, policy_none))
        _, T = absorption_and_time(s, policy_none, {Z})
        dwell[eps] = T[NA]
        say(f'| {eps} | {nc} | {fmt(T[NA], 1)} |')
    vals = [dwell[e] for e in sorted(dwell, reverse=True)]
    assert all(a < b for a, b in zip(vals, vals[1:]))
    say(f'Baseline B0 for comparison: E[steps to S0 from A4] = {fmt(T0[NA], 1)}')

    # 5. Hysteresis: m threat cues from rest at S0, then ambiguous cues, no reasoning.
    say('\n## Hysteresis: after m threat cues from S0, Pr(e = S) after H further ambiguous steps (no reasoning)')
    say('| spec | m | H=5 | H=20 | H=80 | Pr(ever back to S0) |')
    say('|---|---|---|---|---|---|')
    hyst = {}
    for s in (B0, E1, R9):
        Hs, _ = absorption_and_time(s, policy_none, {Z})
        for m in (1, 2, 4):
            d = propagate(s, {Z: F(1)}, policy_none, m, cue='threat')
            row = [p_endpoint_S(propagate(s, d, policy_none, H)) for H in (5, 20, 80)]
            back = sum(p * (1 if st == Z else Hs[st]) for st, p in d.items())
            hyst[(s.name, m)] = back
            say(f'| {s.name.split()[0]} | {m} | ' + ' | '.join(fmt(x) for x in row) + f' | {fmt(back)} |')
    assert all(hyst[(B0.name, m)] == 1 and hyst[(R9.name, m)] == 1 for m in (1, 2, 4))
    assert hyst[(E1.name, 1)] > hyst[(E1.name, 2)] > hyst[(E1.name, 4)]

    # 6. Recalcitrant vs congruent alarm (discriminating signature) after a 4-step pulse.
    say('\n## Joint signature 5 steps after a 4-step pulse (no reasoning)')
    say('| spec | Pr(A, k<=1) recalcitrant | Pr(A, k>=3) congruent | ratio congruent/recalcitrant |')
    say('|---|---|---|---|')
    sig = {}
    for s in (B0, E1, R9):
        d = propagate(s, propagate(s, {Z: F(1)}, policy_none, 4, cue='threat'), policy_none, 5)
        rec = sum(p for (e, k), p in d.items() if e == A and k <= 1)
        con = sum(p for (e, k), p in d.items() if e == A and k >= 3)
        sig[s.name] = (rec, con)
        say(f'| {s.name.split()[0]} | {fmt(rec)} | {fmt(con)} | {fmt(con / rec, 2) if rec else "inf"} |')
    assert sig[E1.name][1] / sig[E1.name][0] > sig[R9.name][1] / sig[R9.name][0]

    # 7. Reachability of the fitting state S from A4.
    say('\n## Optimal feasible reachability: max Pr(e_{t+h} = S | A4)')
    hs = (1, 2, 3, 5, 10, 20, 40)
    say('| spec | ' + ' | '.join(f'h={h}' for h in hs) + ' | limit (hitting S0) |')
    say('|---|' + '---|' * (len(hs) + 1))
    reach = {}
    for s in SPECS:
        row = [max_endpoint_S(s, h)[START] for h in hs]
        Hc, _ = absorption_and_time(s, policy_always('correct'), {Z})
        reach[s.name] = (row, Hc[START])
        say(f'| {s.name.split()[0]} | ' + ' | '.join(fmt(x) for x in row) + f' | {fmt(Hc[START])} |')
    # E3: capture with no capacity: unreachable at every horizon from A4.
    assert all(x == 0 for x in reach[E3.name][0]) and reach[E3.name][1] == 0
    # Ordering B0 >= E1 >= E2 >= E3 pointwise.
    for a, b in ((B0, E1), (E1, E2), (E2, E3)):
        assert all(x >= y for x, y in zip(reach[a.name][0], reach[b.name][0]))
    # Horizon window where S is reachable at alpha = 1/2 under B0 but not under E1.
    for h in range(3, 8):
        assert max_endpoint_S(B0, h)[START] >= HALF > max_endpoint_S(E1, h)[START]
    # Monotone convergence check of the always-correct policy is the optimum for hitting:
    for s in (B0, E1, E2):
        assert reach[s.name][1] == 1

    say('\nSmallest horizon with max Pr(S) >= alpha, from A4:')
    say('| spec | alpha=1/2 | alpha=3/4 | alpha=9/10 |')
    say('|---|---|---|---|')
    first = {}
    for s in SPECS:
        cells = []
        for alpha in (HALF, F(3, 4), F(9, 10)):
            h_found = None
            Vs = {x: F(x[0] == S) for x in s.states()}
            for hh in range(0, 201):
                if hh:
                    Vs = {x: max(sum(p * Vs[y] for y, p in s.step(x, u).items()) for u in ACTIONS)
                          for x in s.states()}
                if Vs[START] >= alpha:
                    h_found = hh
                    break
            first[(s.name, alpha)] = h_found
            cells.append(str(h_found) if h_found is not None else 'none <= 200')
        say(f'| {s.name.split()[0]} | ' + ' | '.join(cells) + ' |')

    # 8. Within-A starting points under E3: reachable only below the hitting bound.
    H3, _ = absorption_and_time(E3, policy_always('correct'), {Z})
    say('\nE3, best policy (always correct): limiting Pr(hit S0) by start in A: '
        + ', '.join(f'A{k}: {fmt(H3[(A, k)])}' for k in range(5)))
    # Endpoint membership is not the same as hitting: sup over h <= 200 of the
    # optimal endpoint probability, by start in A.
    Vs = {x: F(x[0] == S) for x in E3.states()}
    best = {k: Vs[(A, k)] for k in range(5)}
    for hh in range(1, 201):
        Vs = {x: max(sum(p * Vs[y] for y, p in E3.step(x, u).items()) for u in ACTIONS)
              for x in E3.states()}
        for k in range(5):
            best[k] = max(best[k], Vs[(A, k)])
    say('E3, sup over h <= 200 of max Pr(e_{t+h} = S): '
        + ', '.join(f'A{k}: {fmt(best[k])}' for k in range(5))
        + '. So in E3 the fitting state is outside R_{h,alpha}(A_k) at every h <= 200 whenever alpha exceeds that value.')
    assert best[4] == 0 and all(H3[(A, k)] - best[k] < F(1, 10**6) for k in range(5))

    # 9. Selection alone leaves optimal reachability unchanged; it moves the passive value.
    START2 = (A, 2)
    say('\n## Selection versus kernel: usual-policy vs optimal Pr(e_{t+10} = S), from A2')
    say('| spec | optimal | pi0 = none | pi0 = threshold k*=3, r=1/2 | pi0 = ramp | pi0 = always correct |')
    say('|---|---|---|---|---|---|')
    ramp = pi0_ramp([0, F(1, 8), F(1, 4), F(3, 8), F(1, 2)])
    thr = pi0_threshold(3, HALF)
    sel = {}
    for s in (B0, E1, E2):
        opt = max_endpoint_S(s, 10)[START2]
        vals = [value_fixed(s, pol, 10, lambda x: x[0] == S)[START2]
                for pol in (policy_none, thr, ramp, policy_always('correct'))]
        sel[s.name] = (opt, vals)
        say(f'| {s.name.split()[0]} | {fmt(opt)} | ' + ' | '.join(fmt(v) for v in vals) + ' |')
        assert all(v <= opt for v in vals)
    # The threshold and ramp usual policies are close at the endpoint (identification).
    for s in (B0, E1, E2):
        assert abs(sel[s.name][1][1] - sel[s.name][1][2]) < F(1, 20)

    # 10. State-dependent regulation effectiveness: effect of 'always correct' vs
    #     'none' on Pr(e_{t+5} = S), by start, with and without a capacity difference.
    say('\n## Effect of corrective reasoning by starting state: Pr_correct(S at h=5) - Pr_none(S at h=5)')
    say('| spec | ' + ' | '.join(f'{e}{k}' for e in (S, A) for k in range(5)) + ' |')
    say('|---|' + '---|' * 10)
    eff = {}
    for s in (B0, E1, C1, E2):
        Vc = value_fixed(s, policy_always('correct'), 5, lambda x: x[0] == S)
        Vn = value_fixed(s, policy_none, 5, lambda x: x[0] == S)
        eff[s.name] = {x: Vc[x] - Vn[x] for x in s.states()}
        say(f'| {s.name.split()[0]} | ' + ' | '.join(fmt(eff[s.name][(e, k)]) for e in (S, A)
                                                    for k in range(5)) + ' |')
    # Baseline: at fixed belief the effect does not depend on affect (exactly).
    assert all(eff[B0.name][(S, k)] == eff[B0.name][(A, k)] for k in range(5))
    # Capacity only: weaker in A at every k > 0.
    assert all(eff[C1.name][(A, k)] < eff[C1.name][(S, k)] for k in range(1, 5))
    # Interpretation only (equal capacity): the sign of the affect difference changes with k.
    assert eff[E1.name][(A, 0)] > eff[E1.name][(S, 0)] and eff[E1.name][(A, 4)] < eff[E1.name][(S, 4)]

    text = '\n'.join(out)
    if not check_only:
        print(text)
    print('\nAll exact assertions passed.')
    return text


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--check', action='store_true')
    run(ap.parse_args().check)
