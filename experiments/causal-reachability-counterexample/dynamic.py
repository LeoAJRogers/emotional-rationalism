"""Synthetic two-step dynamic causal counterexample; standard library only."""
from random import Random

N = 100000
SEED = 20261120


def trial(model, intervention=None, explore=0.0, n=N, seed=SEED):
    rng = Random(seed)
    counts = [0, 0, 0]
    for _ in range(n):
        h = rng.randrange(2)
        # Exogenous draws are aligned across models and policies.
        e0, a0 = rng.random(), rng.randrange(2)
        u0 = (a0 if e0 < explore else h) if intervention is None else intervention
        y0 = u0 if model == 'action' else h
        # Feedback: next readiness follows observed outcome with probability .8.
        h1 = y0 if rng.random() < .8 else rng.randrange(2)
        u1 = h1  # Natural action at t=1
        y1 = u1 if model == 'action' else h1
        counts[0] += y0
        counts[1] += y1
        counts[2] += (u0 != y0)
    return tuple(round(c/n, 5) for c in counts)


def main():
    print('model,policy,P(Y0=1),P(Y1=1),P(U0!=Y0)')
    for model in ('action', 'readiness'):
        for policy, intervention, explore in [
            ('natural', None, 0), ('explore10', None, .1),
            ('do0', 0, 0), ('do1', 1, 0)
        ]:
            print(model, policy, *trial(model, intervention, explore), sep=',')
    assert trial('action') == trial('readiness')
    assert trial('action', 1)[0] == 1
    assert trial('readiness', 1)[0] < .55
    assert trial('action', 1)[1] > .85
    assert .45 < trial('readiness', 1)[1] < .55
    print('PASS')


if __name__ == '__main__':
    main()
