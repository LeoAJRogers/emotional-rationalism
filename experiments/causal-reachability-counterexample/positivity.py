"""Synthetic causal identifiability: proxy quality versus action overlap.

Run: python experiments/causal-reachability-counterexample/positivity.py
No third-party dependencies.
"""
from random import Random


def run(model, proxy_accuracy, exploration, n=100000, seed=20261120):
    rng = Random(seed)
    counts = {(u, z): [0, 0] for u in (0, 1) for z in (0, 1)}
    mismatches = 0
    for _ in range(n):
        h = rng.randrange(2)
        u = rng.randrange(2) if rng.random() < exploration else h
        z = h if rng.random() < proxy_accuracy else 1 - h
        y = u if model == "action" else h
        counts[(u, z)][0] += y
        counts[(u, z)][1] += 1
        mismatches += (u != y)
    return mismatches / n, counts


def main():
    print("model,proxy_accuracy,exploration,mismatch_rate,min_cell_n")
    for model in ("action", "readiness"):
        for accuracy in (0.5, 0.9, 1.0):
            for exploration in (0, 0.1):
                mismatch, cells = run(model, accuracy, exploration)
                print(
                    f"{model},{accuracy:.1f},{exploration:.1f},"
                    f"{mismatch:.5f},{min(v[1] for v in cells.values())}"
                )
                if exploration == 0 or model == "action":
                    assert mismatch == 0
                if model == "readiness" and exploration > 0:
                    assert .035 < mismatch < .065
    print("PASS")


if __name__ == "__main__":
    main()
