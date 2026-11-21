"""Dependency-free synthetic causal reachability counterexample.

Run: python experiments/causal-reachability-counterexample/simulate.py
"""
from random import Random


def observational_data(model, n=10000, seed=20261120):
    rng = Random(seed)
    rows = []
    for _ in range(n):
        h = rng.randrange(2)
        u = h
        y = u if model == "action" else h
        rows.append((u, y))
    return rows


def intervention(model, assigned_u, n=10000, seed=20261120):
    rng = Random(seed)
    return sum(
        (assigned_u if model == "action" else rng.randrange(2))
        for _ in range(n)
    ) / n


def main():
    a, b = observational_data("action"), observational_data("readiness")
    assert a == b, "observed data should be indistinguishable"
    for model in ("action", "readiness"):
        p0 = intervention(model, 0)
        p1 = intervention(model, 1)
        print(
            f"{model}: observational rows identical; "
            f"do(0)={p0:.4f}; do(1)={p1:.4f}; effect={p1-p0:.4f}; "
            f"target reachable at alpha=.75: {max(p0,p1)>=.75}"
        )
    assert intervention("action", 1) == 1.0
    assert intervention("readiness", 1) < .75


if __name__ == "__main__":
    main()
