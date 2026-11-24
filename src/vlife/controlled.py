"""Controlled linear worlds for niche A, step A3 (docs/A.md).

Each world has N = 6 coordinates and stationary covariance S = I. The drift in whitened form is
    B(omega, eta) = Q ( Bdiag(omega) + eta * U ) Q^T,
    Bdiag(omega) = blockdiag_k [[r_k, omega r_k], [-omega r_k, r_k]],   k = 1, 2, 3,
U strictly block-upper-triangular (2 x 2 blocks), Q a random orthogonal matrix. Then D = (B + B^T) / 2.
- The eigenvalues of B are r_k (1 +- i omega) for every eta, so sigma_osc = 2 omega^2 sum_k r_k does not depend on eta.
- eta = 0 gives a normal B, so sigma_nn = 0. eta > 0 makes B nonnormal.
- S = I solves the Lyapunov equation B S + S B^T = 2 D by construction.
Q mixes the coordinates, so a structure (a subset of coordinates) does not match one block.
Construction: ours (block Schur form with a fixed spectrum). [Schur form idea: NagayamaKolchinskyIto26]
"""
import numpy as np

N = 6


def draw(rng, rate_range=(0.3, 3.0)):
    """One world: block rates r (3,), coupling U (6, 6) and rotation Q (6, 6)."""
    r = np.exp(rng.uniform(np.log(rate_range[0]), np.log(rate_range[1]), 3))
    U = np.zeros((N, N))
    for i in range(3):
        for j in range(i + 1, 3):
            U[2 * i:2 * i + 2, 2 * j:2 * j + 2] = rng.normal(size=(2, 2)) * np.sqrt(r[i] * r[j])
    Q, R = np.linalg.qr(rng.normal(size=(N, N)))
    Q = Q * np.sign(np.diag(R))
    return dict(r=r, U=U, Q=Q)


def block_diag(r, omega):
    Bd = np.zeros((N, N))
    for k, rk in enumerate(r):
        Bd[2 * k:2 * k + 2, 2 * k:2 * k + 2] = [[rk, omega * rk], [-omega * rk, rk]]
    return Bd


def eta_cap(w, floor=0.25):
    """Largest eta for which the smallest eigenvalue of the symmetric part stays >= floor * min(r) (bisection).
    The symmetric part does not depend on omega."""
    base = np.diag(np.repeat(w["r"], 2)); Us = (w["U"] + w["U"].T) / 2
    target = floor * w["r"].min()
    lo, hi = 0.0, 1.0
    while np.linalg.eigvalsh(base + hi * Us)[0] >= target:
        hi *= 2
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if np.linalg.eigvalsh(base + mid * Us)[0] >= target else (lo, mid)
    return lo


def matrices(w, omega, eta):
    """Return (B, D, S) for one grid point."""
    K = block_diag(w["r"], omega) + eta * w["U"]
    B = w["Q"] @ K @ w["Q"].T
    D = (B + B.T) / 2
    return B, D, np.eye(N)
