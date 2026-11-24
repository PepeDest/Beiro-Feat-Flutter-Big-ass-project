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


_PROP_CACHE = {}


def propagator(B, D, tau):
    """Phi = exp(-B tau) and Q_tau = int_0^tau e^{-Bs} 2D e^{-B^T s} ds (Van Loan's block exponential [VanLoan78]).
    Results are cached by the bytes of (B, D, tau), because the optimizers of B2 call this many times."""
    key = (np.asarray(B, float).tobytes(), np.asarray(D, float).tobytes(), float(tau), B.shape)
    if key not in _PROP_CACHE:
        if len(_PROP_CACHE) > 256:
            _PROP_CACHE.clear()
        _PROP_CACHE[key] = _propagator(B, D, tau)
    Phi, Q = _PROP_CACHE[key]
    return Phi.copy(), Q.copy()


def _propagator(B, D, tau):
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


# ---------------------------------------------------------------- B2: stored semantic information (docs/B.md, B2)
def drive_projection(B, D, S0, dx, tau):
    """Pi_W: orthogonal projector (whitened y) on the row space of W = Phi_XY Sigma_Y^{1/2}, the directions of the
    environment that drive the agent up to time tau. P = Pi_W keeps Sigma_{X_tau} exactly (Pi_W W^T = W^T)."""
    Phi, _ = propagator(B, D, tau)
    W = Phi[:dx, dx:] @ _sqrtm_psd(S0[dx:, dx:])
    U, s, _ = np.linalg.svd(W.T, full_matrices=False)
    U = U[:, s > 1e-12 * max(s.max(), 1e-300)]
    return U @ U.T


def drive_information(B, D, S0, dx, tau):
    """I_C = I(X_0; Pi_W Y_0) = -1/2 log det(I - C Pi_W C^T): the information of the agent about the drive directions.
    For dx = 1 this equals the stored semantic information over all Gaussian garblings (Cauchy-Schwarz, docs/B.md)."""
    return syntactic_information(S0, dx, drive_projection(B, D, S0, dx, tau))


def _rotation(angles, n):
    """Orthogonal matrix exp(A - A^T), with the n(n-1)/2 free entries of A given by `angles`."""
    A = np.zeros((n, n)); A[np.triu_indices(n, 1)] = angles
    return expm(A - A.T)


def _unit(a):
    """Unit vector in R^3 from two angles."""
    return np.array([np.cos(a[0]) * np.sin(a[1]), np.sin(a[0]) * np.sin(a[1]), np.cos(a[1])])


def min_information(B, D, S0, dx, tau, family="general", n_starts=64, rng=None, tol=1e-7):
    """Smallest I_P(X_0; Y_0) over P in `family` with V(P) = V(I) (KolchinskyWolpert18, Eqs. (9)-(10)), by SLSQP from
    n_starts random starts. family: "general" (0 <= P <= I, also starts at P = I), "rank1" (P = u u^T) or
    "corank1" (P = I - v v^T), the last two for dy = 3 only. P = I and P = Pi_W are always feasible and are added.
    Returns (best I, best P, number of feasible ends within 1e-4 nats of the best, number of feasible ends)."""
    from scipy.optimize import minimize
    rng = np.random.default_rng() if rng is None else rng
    dy = S0.shape[0] - dx; m = dy * (dy - 1) // 2
    V_act = viability(B, D, S0, dx, np.eye(dy), tau)
    if family == "general":
        def P_of(z):
            Q = _rotation(z[:m], dy)
            return Q @ np.diag(np.clip(z[m:], 0.0, 1.0)) @ Q.T
        bounds = [(-np.pi, np.pi)] * m + [(0.0, 1.0)] * dy
        starts = [np.concatenate([rng.uniform(-np.pi, np.pi, m), rng.uniform(0, 1, dy)]) for _ in range(n_starts)]
        starts.append(np.concatenate([np.zeros(m), np.ones(dy)]))
    else:
        if dy != 3:
            raise ValueError("rank1 and corank1 need dy = 3")
        def P_of(z):
            u = _unit(z)
            return np.outer(u, u) if family == "rank1" else np.eye(dy) - np.outer(u, u)
        bounds = None
        starts = [rng.uniform(-np.pi, np.pi, 2) for _ in range(n_starts)]

    def f(z):
        return syntactic_information(S0, dx, P_of(z))

    def g(z):
        return viability(B, D, S0, dx, P_of(z), tau) - V_act

    ends = []
    for z0 in starts:
        try:
            r = minimize(f, z0, method="SLSQP", bounds=bounds, constraints=[dict(type="eq", fun=g)],
                         options=dict(maxiter=500, ftol=1e-12))
        except (ValueError, np.linalg.LinAlgError):
            continue
        try:
            if abs(g(r.x)) <= tol:
                ends.append((f(r.x), P_of(r.x)))
        except (ValueError, np.linalg.LinAlgError):
            continue
    for P in (np.eye(dy), drive_projection(B, D, S0, dx, tau)):
        ends.append((syntactic_information(S0, dx, P), P))
    best = min(ends, key=lambda e: e[0])
    return best[0], best[1], sum(e[0] <= best[0] + 1e-4 for e in ends), len(ends)
