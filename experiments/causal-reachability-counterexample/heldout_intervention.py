"""Train observational conditional predictor, test assigned-action outcomes."""
from random import Random

N = 100000
SEED = 20261120


def experiment(model):
    rng = Random(SEED)
    natural = []
    assigned = []
    for _ in range(N):
        h = rng.randrange(2)
        u = h
        natural.append((u, u if model == 'action' else h))
        h = rng.randrange(2)
        u = 1
        assigned.append((u, u if model == 'action' else h))
    selected = [y for u, y in natural if u == 1]
    predicted = sum(selected) / len(selected)
    observed = sum(y for _, y in assigned) / len(assigned)
    return predicted, observed


def main():
    print('model,observational_prediction,assigned_outcome,absolute_error')
    for model in ('action', 'readiness'):
        p, q = experiment(model)
        print(f'{model},{p:.5f},{q:.5f},{abs(p-q):.5f}')
        assert p == 1
        if model == 'action':
            assert q == 1
        else:
            assert .48 < q < .52
    print('PASS')


if __name__ == '__main__':
    main()
