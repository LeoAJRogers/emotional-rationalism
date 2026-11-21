"""Exact synthetic checks for action versus assignment under feedback."""

from collections import Counter
from fractions import Fraction
from itertools import product


def trajectories(action_causal, *, assignments=(None, None), actions=(None, None)):
    """Enumerate equiprobable draws, preserving readiness in the audit record."""
    counts = Counter()
    for h0, z0, c0, fresh, z1, c1 in product(range(2), repeat=6):
        for feedback_draw in range(4):
            z0_used = z0 if assignments[0] is None else assignments[0]
            z1_used = z1 if assignments[1] is None else assignments[1]
            intended0 = z0_used if c0 else h0
            a0 = intended0 if actions[0] is None else actions[0]
            y0 = a0 if action_causal else intended0
            h1 = y0 if feedback_draw < 3 else fresh
            intended1 = z1_used if c1 else h1
            a1 = intended1 if actions[1] is None else actions[1]
            y1 = a1 if action_causal else intended1
            counts[h0, z0_used, a0, y0, h1, z1_used, a1, y1] += 1
    return counts


def probability(counts, event, given=lambda row: True):
    eligible = [(row, count) for row, count in counts.items() if given(row)]
    return Fraction(
        sum(count for row, count in eligible if event(row)),
        sum(count for _, count in eligible),
    )


def main():
    randomized = trajectories(True)
    assert randomized == trajectories(False)
    for schedule in product(range(2), repeat=2):
        assert trajectories(True, assignments=schedule) == trajectories(
            False, assignments=schedule
        )

    # Action varies within measured baseline readiness under the mixed protocol.
    for readiness in range(2):
        assert 0 < probability(
            randomized, lambda row: row[2], lambda row: row[0] == readiness
        ) < 1

    def assignment_contrast(index):
        return probability(randomized, lambda row: row[index], lambda row: row[1] == 1) - (
            probability(randomized, lambda row: row[index], lambda row: row[1] == 0)
        )

    first_stage = assignment_contrast(2)
    proximal_itt = assignment_contrast(3)
    distal_itt = assignment_contrast(7)
    assert first_stage == proximal_itt == Fraction(1, 2)
    assert distal_itt == Fraction(3, 16)

    print("First stage = proximal assignment effect = 1/2")
    print("Wald ratio = 1 in both models; distal assignment effect = 3/16")
    for action_causal, expected in [(True, (0, 1)), (False, (Fraction(1, 2),) * 2)]:
        risks = tuple(
            probability(trajectories(action_causal, actions=(a, a)), lambda row: row[7])
            for a in range(2)
        )
        assert risks == expected
        early_risks = tuple(
            probability(trajectories(action_causal, actions=(a, None)), lambda row: row[7])
            for a in range(2)
        )
        assert early_risks == (
            (Fraction(5, 16), Fraction(11, 16)) if action_causal
            else (Fraction(1, 2), Fraction(1, 2))
        )
        print(
            f"action_causal={action_causal}: early action risks="
            f"{tuple(map(str, early_risks))}, sustained action risks={tuple(map(str, risks))}"
        )

    # Holding post-action readiness fixed removes the early action feedback path.
    for readiness in range(2):
        for a in range(2):
            assert probability(
                trajectories(True, actions=(a, None)),
                lambda row: row[7], lambda row: row[4] == readiness,
            ) == Fraction(1 + 2 * readiness, 4)
    print("PASS")


if __name__ == "__main__":
    main()
