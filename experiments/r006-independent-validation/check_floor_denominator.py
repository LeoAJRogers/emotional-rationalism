"""Tiny synthetic-only regression check for R-006 Part B floor sensitivity.

No real data loaded. Run: python check_floor_denominator.py
"""
import numpy as np

v = np.array([1., 1., 6., 7.] + [np.nan] * 6)
buggy = np.nanmean(v == 1)         # NaN == 1 is False; denominator is 10
observed = v[np.isfinite(v)]
correct = np.mean(observed == 1)   # denominator is 4
assert np.isclose(buggy, 0.2)
assert np.isclose(correct, 0.5)
assert (buggy < 0.5) and not (correct < 0.5)
print(f"bad scheduled-slot floor rate={buggy:.3f}, correct observed floor rate={correct:.3f}")
print("PASS: previously 'low-floor' included; correctly excluded")
