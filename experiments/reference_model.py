"""Illustrative finite-state model; no human data or intervention claims."""
import argparse


def terminal_probability(horizon, rates, target):
    # Bellman recursion: maximize terminal target probability, not loss.
    a, s = float(target == 'A'), float(target == 'S')
    for _ in range(horizon):
        a = max((1-p)*a + p*s for p in rates)
    return a


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--horizon', type=int, default=3)
    parser.add_argument('--alpha', type=float, default=.5)
    parser.add_argument('--rates', type=float, nargs='+', default=[.1, .25])
    args = parser.parse_args()
    if args.horizon < 0 or not 0 < args.alpha <= 1 or not all(0 <= p <= 1 for p in args.rates):
        parser.error('Require horizon >= 0, 0 < alpha <= 1, rates in [0,1].')
    # Analytic oracle for the absorbing two-state case.
    for h in range(20):
        for rates in ([0], [1], [.1], [.1,.25], args.rates):
            assert abs(terminal_probability(h,rates,'S')-(1-(1-max(rates))**h)) < 1e-12
            assert abs(terminal_probability(h,rates,'A')-(1-min(rates))**h) < 1e-12
    probs = {e: terminal_probability(args.horizon,args.rates,e) for e in ('A','S')}
    print('Illustrative only; analytic self-checks passed.')
    print('Fitting set (fixed illustrative loss): S')
    for e,p in probs.items():
        print(f'Max terminal P({e}) = {p:.6f}')
    print('Reachable set:', ', '.join(e for e,p in probs.items() if p >= args.alpha) or '(empty)')
    print('Target-wise maxima may require different policies; not a joint distribution.')


if __name__ == '__main__':
    main()
