"""Observed semantic information of KolchinskyWolpert18 (Sec. V B) in discrete-time linear Gaussian systems (niche B,
step B3, docs/B.md).

Joint state z = (x, y): agent x (first dx coordinates), environment y (the rest, dy coordinates).
Dynamics z_{t+1} = F z_t + w_t, w_t ~ N(0, W), W = blockdiag(W_x, W_y). The start z_0 has the stationary law.
Because W is block diagonal, y_{t+1} and x_{t+1} are independent given (x_t, y_t). So the intervention below keeps
p(y_{t+1} | x_t, y_t, x_{t+1}) as KolchinskyWolpert18 requires.

Intervention (Gaussian form of KolchinskyWolpert18, Eqs. (17)-(18)): one fixed sensor Z_t = K y_t + N_t,
N_t ~ N(0, Sigma_N), at all times t. The agent draws x_{t+1} from the actual p(x_{t+1} | x_t, y) with y drawn from
the INTERVENED posterior p^(y_t | x_t, z_t). With the intervened joint law of (x_t, y_t) at time t:
    M_t = Cov(y, x) Cov(x)^{-1},  L_t = Cov(y | x)^{1/2},  K_w = K L_t,
    J_t = K_w^T (K_w K_w^T + Sigma_N)^{-1},  P_t = J_t K_w  (0 <= P_t <= I),
    x_{t+1} = F_xx x_t + F_xy [M_t x_t + L_t (J_t (z_t - K M_t x_t) + e_t)] + w_x,   e_t ~ N(0, I - P_t).
K = diag(sqrt(s)) R^T and Sigma_N = diag(1 - s), with R a rotation and s in [0, 1]^dy, give every sensor up to an
invertible change of z. s = 1 is the actual dynamics (a one-to-one phi), s = 0 the full scrambling, s in {0, 1}^dy a
deterministic coarse-graining phi(y) = U^T y.

Quantities (nats): V = -H(X_tau). TE = sum_t I(Y_t; X_{t+1} | X_t) [KolchinskyWolpert18, Eq. (16)].
DI = sum_t I(Y_0..t; X_{t+1} | X_0..t), the directed information from Y to X.
DT = sum_t I(Y_0..t; Z_t | Z_0..t-1), the directed information from the environment to the sensor, the measure of
TanakaEsfahaniMitter18. Our code. Checks: tests/test_semantic_b3.py.
"""
import numpy as np
from scipy.linalg import solve_discrete_lyapunov
from vlife.gaussian import conditional_mutual_information
from vlife.semantic import _sqrtm_psd, _logdet, _rotation


def stationary_cov_discrete(F, W):
    """S = F S F^T + W."""
    S = solve_discrete_lyapunov(F, W)
    return (S + S.T) / 2


def sensor(angles, s):
    """(K, Sigma_N) of the sensor with rotation angles and gains s (module docstring)."""
    s = np.clip(np.asarray(s, float), 0.0, 1.0)
    R = _rotation(np.asarray(angles, float), len(s))
    return np.sqrt(s)[:, None] * R.T, np.diag(1.0 - s)


def _step(F, W, dx, S, K, SN):
    """Maps of one intervened step from the joint covariance S of (x_t, y_t)."""
    n = F.shape[0]; dy = n - dx
    Sx, Sxy, Sy = S[:dx, :dx], S[:dx, dx:], S[dx:, dx:]
    M = np.linalg.solve(Sx, Sxy).T
    L = _sqrtm_psd(Sy - M @ Sxy)
    Kw = K @ L
    J = np.linalg.solve(Kw @ Kw.T + SN, Kw).T
    P = J @ Kw
    P = (P + P.T) / 2
    Fxx, Fxy = F[:dx, :dx], F[:dx, dx:]
    Ax = Fxx + Fxy @ M - Fxy @ L @ J @ K @ M           # coefficient of x_t
    Bz = Fxy @ L @ J                                     # coefficient of z_t
    E = Fxy @ L                                          # coefficient of e_t
    return dict(M=M, L=L, J=J, P=P, Ax=Ax, Bz=Bz, E=E, I_P=np.eye(dy) - P)


def run(F, W, dx, K, SN, tau, S0=None):
    """Intervened covariances S_0..S_tau of (x_t, y_t), the transfer entropies TE_0..TE_{tau-1} and the step maps."""
    n = F.shape[0]; dy = n - dx
    S = stationary_cov_discrete(F, W) if S0 is None else S0
    Wx = W[:dx, :dx]
    Fyx, Fyy, Fxy = F[dx:, :dx], F[dx:, dx:], F[:dx, dx:]
    covs, te, maps = [S], [], []
    for _ in range(tau):
        m = _step(F, W, dx, S, K, SN); maps.append(m)
        G = Fxy @ m["L"] @ m["L"].T @ Fxy.T + Wx                         # Var(x_{t+1} | x_t)
        Gy = G - Fxy @ m["L"] @ m["P"] @ m["P"] @ m["L"].T @ Fxy.T     # Var(x_{t+1} | x_t, y_t)
        te.append(0.5 * (_logdet(G) - _logdet(Gy)))
        Ft = np.block([[m["Ax"], m["Bz"] @ K], [Fyx, Fyy]])
        Nx = m["Bz"] @ SN @ m["Bz"].T + m["E"] @ m["I_P"] @ m["E"].T + Wx
        N = np.zeros((n, n)); N[:dx, :dx] = Nx; N[dx:, dx:] = W[dx:, dx:]
        S = Ft @ S @ Ft.T + N
        S = (S + S.T) / 2
        covs.append(S)
    return covs, np.array(te), maps


def viability(F, W, dx, K, SN, tau, S0=None):
    """V = -H(X_tau) in nats."""
    covs, _, _ = run(F, W, dx, K, SN, tau, S0)
    return -0.5 * (dx * np.log(2 * np.pi * np.e) + _logdet(covs[-1][:dx, :dx]))


def transfer_entropy(F, W, dx, K, SN, tau, S0=None):
    """Sum over t of I(Y_t; X_{t+1} | X_t) under the intervention [KolchinskyWolpert18, Eq. (16)]."""
    return float(run(F, W, dx, K, SN, tau, S0)[1].sum())


def trajectory_cov(F, W, dx, K, SN, tau, S0=None):
    """Joint covariance of (x_0..tau, y_0..tau, z_0..tau-1), built from independent noise sources.
    Returns (cov, index lists ix[t], iy[t], iz[t])."""
    n = F.shape[0]; dy = n - dx; k = K.shape[0]
    S = stationary_cov_discrete(F, W) if S0 is None else S0
    covs, _, maps = run(F, W, dx, K, SN, tau, S)
    blk = k + dy + dx + dy
    m_src = n + tau * blk
    Fyx, Fyy = F[dx:, :dx], F[dx:, dx:]
    sq = _sqrtm_psd
    root0 = sq(S)
    X = [root0[:dx]]; Y = [root0[dx:]]; Z = []
    pad = lambda A: np.hstack([A, np.zeros((A.shape[0], m_src - A.shape[1]))])
    X[0], Y[0] = pad(X[0]), pad(Y[0])
    def src(c, R):
        A = np.zeros((R.shape[0], m_src)); A[:, c:c + R.shape[1]] = R
        return A
    for t in range(tau):
        m = maps[t]; c = n + t * blk
        z = K @ Y[t] + src(c, sq(SN))
        x = m["Ax"] @ X[t] + m["Bz"] @ z + src(c + k, m["E"] @ sq(m["I_P"])) + src(c + k + dy, sq(W[:dx, :dx]))
        y = Fyx @ X[t] + Fyy @ Y[t] + src(c + k + dy + dx, sq(W[dx:, dx:]))
        Z.append(z); X.append(x); Y.append(y)
    rows = X + Y + Z
    A = np.vstack(rows)
    cov = A @ A.T
    ix, iy, iz, o = [], [], [], 0
    for t in range(tau + 1):
        ix.append(list(range(o, o + dx))); o += dx
    for t in range(tau + 1):
        iy.append(list(range(o, o + dy))); o += dy
    for t in range(tau):
        iz.append(list(range(o, o + k))); o += k
    return cov, ix, iy, iz


def information_measures(F, W, dx, K, SN, tau, S0=None, which=("te", "di", "dt")):
    """(TE, DI, DT) of the module docstring, or only the names in `which` (the others are None).
    DT is inf when a sensor gain is 1 (no noise on that row)."""
    cov, ix, iy, iz = trajectory_cov(F, W, dx, K, SN, tau, S0)
    flat = lambda L: [i for l in L for i in l]
    te = di = dt = None
    if "te" in which:
        te = sum(conditional_mutual_information(cov, iy[t], ix[t + 1], ix[t]) for t in range(tau))
    if "di" in which:
        di = sum(conditional_mutual_information(cov, flat(iy[:t + 1]), ix[t + 1], flat(ix[:t + 1]))
                 for t in range(tau))
    if "dt" in which:
        if np.min(np.diag(SN)) <= 1e-12:
            dt = np.inf
        else:
            dt = sum(conditional_mutual_information(cov, flat(iy[:t + 1]), iz[t], flat(iz[:t])) for t in range(tau))
    return te, di, dt


def min_observed(F, W, dx, tau, objective="te", n_starts=24, rng=None, tol=1e-7, s_max=1.0, maxiter=300):
    """Smallest objective ("te", "di" or "dt") over sensors with V = V_act [KolchinskyWolpert18, Eqs. (21)-(22)], by
    SLSQP from n_starts random starts (and the start s = 1 for "te" and "di"). The actual sensor is always added for
    "te" and "di". s_max < 1 keeps "dt" finite. Returns (best value, best (angles, s), n near best, n feasible)."""
    from scipy.optimize import minimize
    rng = np.random.default_rng() if rng is None else rng
    n = F.shape[0]; dy = n - dx; m = dy * (dy - 1) // 2
    S0 = stationary_cov_discrete(F, W)
    V_act = viability(F, W, dx, np.eye(dy), np.zeros((dy, dy)), tau, S0)
    split = lambda z: (z[:m], np.clip(z[m:], 0.0, s_max))

    def f(z):
        K, SN = sensor(*split(z))
        if objective == "te":
            return transfer_entropy(F, W, dx, K, SN, tau, S0)
        te, di, dt = information_measures(F, W, dx, K, SN, tau, S0, which=(objective,))
        return di if objective == "di" else dt

    def g(z):
        return viability(F, W, dx, *sensor(*split(z)), tau, S0) - V_act

    bounds = [(-np.pi, np.pi)] * m + [(0.0, s_max)] * dy
    starts = [np.concatenate([rng.uniform(-np.pi, np.pi, m), rng.uniform(0, s_max, dy)]) for _ in range(n_starts)]
    if objective != "dt":
        starts.append(np.concatenate([np.zeros(m), np.ones(dy)]))
    ends = []
    for z0 in starts:
        try:
            r = minimize(f, z0, method="SLSQP", bounds=bounds, constraints=[dict(type="eq", fun=g)],
                         options=dict(maxiter=maxiter, ftol=1e-12))
            if abs(g(r.x)) <= tol and np.isfinite(f(r.x)):
                ends.append((float(f(r.x)), split(r.x)))
        except (ValueError, np.linalg.LinAlgError):
            continue
    if objective != "dt":
        ends.append((float(f(np.concatenate([np.zeros(m), np.ones(dy)]))), (np.zeros(m), np.ones(dy))))
    if not ends:
        return None, None, 0, 0
    best = min(ends, key=lambda e: e[0])
    return best[0], best[1], sum(e[0] <= best[0] + 1e-4 for e in ends), len(ends)


def projection_sensors_dy2(F, W, dx, tau, n_grid=360, iters=50):
    """dy = 2 only. All deterministic coarse-grainings phi(y) = cos(a) y_1 + sin(a) y_2 with V = V_act, found as the
    roots in a of V(a) - V_act on a grid of [0, pi), refined by bisection. Returns a list of (a, TE)."""
    S0 = stationary_cov_discrete(F, W)
    V_act = viability(F, W, dx, np.eye(2), np.zeros((2, 2)), tau, S0)
    def K_of(a):
        return np.array([[np.cos(a), np.sin(a)], [0.0, 0.0]]), np.diag([0.0, 1.0])
    gfun = lambda a: viability(F, W, dx, *K_of(a), tau, S0) - V_act
    grid = np.linspace(0.0, np.pi, n_grid + 1)
    vals = [gfun(a) for a in grid]
    out = []
    for i in range(n_grid):
        lo, hi, flo = grid[i], grid[i + 1], vals[i]
        if np.sign(flo) == np.sign(vals[i + 1]):
            continue
        for _ in range(iters):
            mid = (lo + hi) / 2; fm = gfun(mid)
            lo, hi, flo = (mid, hi, fm) if np.sign(fm) == np.sign(flo) else (lo, mid, flo)
        a = (lo + hi) / 2
        out.append((float(a), transfer_entropy(F, W, dx, *K_of(a), tau, S0)))
    return out
