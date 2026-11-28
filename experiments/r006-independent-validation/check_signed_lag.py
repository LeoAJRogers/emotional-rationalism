"""Independent counterexample to unrestricted R-006 E3a sign interpretation.

Run: python experiments/r006-independent-validation/check_signed_lag.py
Only standard-library Python is required.
"""
from itertools import combinations

A = (0.95775870, -0.19980213, 0.02425957)
B = (1.54582085, 0.54510552, -0.50522874)

def excesses(m):
    return tuple(m[j][j] * m[k][l] - m[j][k] * m[j][l]
                 for j, (k, l) in enumerate(((1, 2), (0, 2), (0, 1))))

def outer_signed(a, b, sign):
    return [[a[i] * a[j] + sign * b[i] * b[j] for j in range(3)] for i in range(3)]

def main():
    psd = excesses(outer_signed(A, B, 1))
    signed = excesses(outer_signed(A, B, -1))
    assert min(signed) > 0, signed
    assert min(psd) <= 0, psd
    print("PSD lag contributions (aa^T + bb^T):", psd)
    print("Signed lag contributions (aa^T - bb^T):", signed)
    print("All three signed-lag excesses are positive:", all(x > 0 for x in signed))
    print("Realizable as lag-one covariance of independent stationary AR(1) factors")
    print("with phi_1=+0.6 and phi_2=-0.6, using loadings A/sqrt(0.6), B/sqrt(0.6).")

if __name__ == "__main__":
    main()
