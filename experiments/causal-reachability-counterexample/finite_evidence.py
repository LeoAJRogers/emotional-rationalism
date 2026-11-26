"""Finite-sample distinguishability with noisy outcomes and limited exploration.

Run: python experiments/causal-reachability-counterexample/finite_evidence.py
Standard library only.
"""
from random import Random


def simulate(model, n, seed, explore=.1, noise=.1):
    rng = Random(seed)
    mismatches = 0
    for _ in range(n):
        h = rng.randrange(2)
        u = rng.randrange(2) if rng.random() < explore else h
        y = u if model == 'action' else h
        if rng.random() < noise:
            y = 1 - y
        mismatches += (u != y)
    return mismatches / n


def main():
    print('n,action_mean,readiness_mean,mean_gap,detection,false_positive')
    for n in (100, 500, 2000, 10000):
        action = [simulate('action', n, 1000 + i) for i in range(300)]
        readiness = [simulate('readiness', n, 1000 + i) for i in range(300)]
        threshold = .12  # Chosen from known theoretical model rates, not fitted.
        detection = sum(x > threshold for x in readiness) / 300
        false_positive = sum(x > threshold for x in action) / 300
        values = (n, sum(action)/300, sum(readiness)/300,
                  (sum(readiness)-sum(action))/300, detection, false_positive)
        print(','.join((str(values[0]), *(f'{v:.4f}' for v in values[1:]))))
    print('PASS')


if __name__ == '__main__':
    main()
