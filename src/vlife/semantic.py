"""Stored semantic information of Kolchinsky and Wolpert in linear Gaussian systems (niche B, docs/B.md).

Joint state z = (x, y): agent x (first dx coordinates), environment y (the rest).
Dynamics dz = -B z dt + sqrt(2 D) dW. Start z_0 ~ N(0, S0). Viability V = -H(X_tau) [KolchinskyWolpert18, Eq. (2)].

Intervention (Gaussian form of the pre-garbling of KolchinskyWolpert18, Eq. (8)): Z = K y_0 + N, N ~ N(0, Sigma_N),
then x_0 is drawn from the actual p(x_0 | z). In whitened y coordinates the intervention is the matrix
    P = K_w^T (K_w K_w^T + Sigma_N)^{-1} K_w,  K_w = K Sigma_Y^{1/2},  0 <= P <= I.
P = I is the actual distribution, P = 0 the full scrambling, a projection P a deterministic coarse-graining.
Closed forms (ours, docs/B.md, B1):
    Sigma_XY(P) = Sigma_XY Sigma_Y^{-1/2} P Sigma_Y^{1/2}        (marginals of x_0 and y_0 do not change)
    I_P(X_0; Y_0) = -1/2 log det(I - C P^2 C^T),  C = Sigma_X^{-1/2} Sigma_XY Sigma_Y^{-1/2}
    Sigma_{X_tau}(P) = [Phi S0(P) Phi^T + Q_tau]_XX,  Phi = exp(-B tau),  Q_tau = int_0^tau e^{-Bs} 2D e^{-B^T s} ds
so Sigma_{X_tau} is affine in P and V(P) is convex in P.
"""
import numpy as np
from scipy.linalg import expm


def _sqrtm_psd(M):
    w, U = np.linalg.eigh((M + M.T) / 2)
    return (U * np.sqrt(np.clip(w, 0, None))) @ U.T


def _logdet(M):
    s, v = np.linalg.slogdet(M)
    if s <= 0:
        raise ValueError("matrix is not positive definite")
    return v


def garbling_matrix(K, Sigma_N, Sy):
    """P (whitened y coordinates) of the Gaussian garbling Z = K y + N."""
    Kw = K @ _sqrtm_psd(Sy)
    return Kw.T @ np.linalg.solve(Kw @ Kw.T + Sigma_N, Kw)


def projection(U):
    """P of the deterministic coarse-graining phi(y) = U^T Sigma_Y^{-1/2} y: the orthogonal projector on span(U)."""
    Q, _ = np.linalg.qr(U)
    return Q @ Q.T


def intervened_cov(S0, dx, P):
    """Joint covariance of (x_0, y_0) under the intervention P."""
    Sx, Sxy, Sy = S0[:dx, :dx], S0[:dx, dx:], S0[dx:, dx:]
    Syh = _sqrtm_psd(Sy)
    Sxy_P = Sxy @ np.linalg.solve(Syh, P @ Syh)
    out = S0.copy()
    out[:dx, dx:] = Sxy_P
    out[dx:, :dx] = Sxy_P.T
    return out


def syntactic_information(S0, dx, P):
    """I(X_0; Y_0) in nats under the intervention P."""
    Sx, Sxy, Sy = S0[:dx, :dx], S0[:dx, dx:], S0[dx:, dx:]
    C = np.linalg.solve(_sqrtm_psd(Sx), Sxy) @ np.linalg.inv(_sqrtm_psd(Sy))
    return -0.5 * _logdet(np.eye(dx) - C @ P @ P @ C.T)


def propagator(B, D, tau):
    """Phi = exp(-B tau) and Q_tau = int_0^tau e^{-Bs} 2D e^{-B^T s} ds (Van Loan's block exponential [VanLoan78])."""
    n = B.shape[0]
    M = np.zeros((2 * n, 2 * n))
    M[:n, :n] = B; M[:n, n:] = 2 * D; M[n:, n:] = -B.T      # drift A = -B in the form [[-A, G], [0, A^T]]
    E = expm(M * tau)
    Phi = E[n:, n:].T
    Q = Phi @ E[:n, n:]
    return Phi, (Q + Q.T) / 2


def agent_cov_at(B, D, S0, dx, P, tau):
    """Covariance of X_tau when the start is intervened with P."""
    Phi, Q = propagator(B, D, tau)
    St = Phi @ intervened_cov(S0, dx, P) @ Phi.T + Q
    return St[:dx, :dx]


def viability(B, D, S0, dx, P, tau):
    """V = -H(X_tau) in nats (Gaussian differential entropy)."""
    Sxt = agent_cov_at(B, D, S0, dx, P, tau)
    return -0.5 * (dx * np.log(2 * np.pi * np.e) + _logdet(Sxt))


def value_of_information(B, D, S0, dx, tau):
    """Delta V = V(actual) - V(full scrambling) [KolchinskyWolpert18, Eq. (6)]."""
    n_y = S0.shape[0] - dx
    return viability(B, D, S0, dx, np.eye(n_y), tau) - viability(B, D, S0, dx, np.zeros((n_y, n_y)), tau)
