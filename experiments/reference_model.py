"""Illustrative finite-state model; no human data or intervention claims."""
import argparse
from fractions import Fraction as F


def terminal_probability(horizon, rates, target):
    # Bellman recursion: maximize terminal target probability, not loss.
    a, s = F(target == 'A'), F(target == 'S')
    rates = tuple(F(p) for p in rates)
    for _ in range(horizon):
        a = max((1-p)*a + p*s for p in rates)
    return a


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--horizon', type=int, default=3)
    parser.add_argument('--alpha', type=F, default=F(1, 2))
    parser.add_argument('--rates', type=F, nargs='+', default=[F(1, 10), F(1, 4)])
    args = parser.parse_args()
    if args.horizon < 0 or not 0 < args.alpha <= 1 or not all(0 <= p <= 1 for p in args.rates):
        parser.error('Require horizon >= 0, 0 < alpha <= 1, rates in [0,1].')
    # Exact analytic oracle for the absorbing two-state case.
    for h in range(20):
        for rates in ([F(0)], [F(1)], [F(1, 10)], [F(1, 10), F(1, 4)], args.rates):
            assert terminal_probability(h,rates,'S') == 1-(1-max(rates))**h
            assert terminal_probability(h,rates,'A') == (1-min(rates))**h
    assert terminal_probability(3,[F(1, 10)],'S') == F(271, 1000)
    probs = {e: terminal_probability(args.horizon,args.rates,e) for e in ('A','S')}
    # All policies' P(S) lie in this interval; endpoint policies and their
    # mixtures attain the whole interval. P(A) is exactly 1-P(S).
    lo, hi = 1-probs['A'], probs['S']
    joint = max(lo, args.alpha) <= min(hi, 1-args.alpha)
    print('Illustrative only; exact analytic self-checks passed.')
    print('Fitting set (stipulated 0–1 loss J(A)=1, J(S)=0): S')
    for e,p in probs.items():
        print(f'Max terminal P({e}) = {float(p):.6f} (exact: {p})')
    print('Reachable set:', ', '.join(e for e,p in probs.items() if p >= args.alpha) or '(empty)')
    print(f'Joint feasible P(S) interval: [{lo}, {hi}]; P(A) = 1-P(S).')
    print('One policy attains both targets at threshold:', 'yes' if joint else 'no')
    print('Target-wise maxima may require different policies; not a joint distribution.')


if __name__ == '__main__':
    main()
