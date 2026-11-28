"""Deterministic audit of R-006's disjoint-pair T1 cancellation.

No external dependencies. Run: python experiments/r006-independent-validation/check_disjoint_pairs.py
This is a finite-sample algebraic test, NOT a stochastic calibration study.
"""
def item_excess(loadings):
    factors = [[1.3, -.7, 2.1, .4, 1.7],
               [-.9, 1.1, .8, -1.4, 2.3],
               [.5, 1.8, -.6, 1.2, -.2]]
    pairs = []
    for d in range(3):
        for b in range(1, 5):
            if (d, b) in {(0, 3), (2, 2)}:
                continue
            pairs.append(((d, b), (d, b - 1)))

    def pair_product(pair, j, k):
        (d, b), (_, c) = pair
        return (loadings[d][j] * factors[d][b] * loadings[d][k] * factors[d][c]
                + loadings[d][k] * factors[d][b] * loadings[d][j] * factors[d][c]) / 2

    def ustat(j, k, l, m):
        vals = [pair_product(a, j, k) * pair_product(b, l, m)
                for a in pairs for b in pairs if set(a).isdisjoint(b)]
        return sum(vals) / len(vals)

    return [ustat(j, j, k, l) - ustat(j, k, j, l)
            for j, (k, l) in enumerate(((1, 2), (0, 2), (0, 1)))]

def main():
    fixed = item_excess([[.7, .6, .5]] * 3)
    drift = item_excess([[.7, .6, .5], [.5, .8, .4], [.9, .4, .7]])
    assert max(abs(v) for v in fixed) < 1e-12
    assert max(abs(v) for v in drift) > 1e-4
    print("Fixed loadings, arbitrary factors and gaps:", fixed)
    print("Between-day loading drift, same factors and gaps:", drift)
    print("PASS: exact fixed-loading cancellation; counterexample under drift")

if __name__ == "__main__":
    main()
