"""Reference scores. Each one takes a control system and returns a number. They are the scores of niches B and C of
variational_life, written again here without imports from that project.

- kw_value: Delta V of KolchinskyWolpert18, Eq. (6), with V = -H(target at tau). Intervention: the full scrambling of
  Cov(agent, env) at t = 0, from the stationary law.
- kw_stored: the stored semantic information of KolchinskyWolpert18, Eqs. (9)-(10), over Gaussian garblings, dy = 1,
  in the reading V(p) = V_act. Root search as in variational_life docs/B.md, B4.
- cld_linear: Causal Leverage Density (Bartlett24, SowinskiEtAl25) for a linear system: JS of the exact Gaussian laws
  with and without the scrambling, divided by I(agent; env) in bits. JS by Monte Carlo.
- cld_unit: CLD of the bit sign(x) of an S2 unit, by the mirror method of docs/C.md, C2.
- flux_ratio: log(V_on / V_off) of an S2 unit (docs/S2.md).
"""
import numpy as np
from .linear import logdet, mutual_information, propagator
from .units import initial, run, step

LN2 = np.log(2.0)


def _scrambled(S, agent, env):
    S = S.copy()
    S[np.ix_(agent, env)] = 0.0
    S[np.ix_(env, agent)] = 0.0
    return S


def _neg_entropy(Sig, idx):
    idx = list(idx)
    return -0.5 * (len(idx) * np.log(2 * np.pi * np.e) + logdet(Sig[np.ix_(idx, idx)]))


def kw_value(sys, tau=1.0):
    """Delta V = V(actual) - V(full scrambling), V = -H(target at tau), in nats."""
    act = sys.cov_at(tau)
    scr = sys.cov_at(tau, _scrambled(sys.S, sys.agent, sys.env))
    return float(_neg_entropy(act, sys.target) - _neg_entropy(scr, sys.target))


def kw_stored(sys, tau=1.0, n_grid=200, iters=50):
    """S_KW in nats, dy = 1. The intervention p in [0, 1] scales Cov(agent, env). S_KW = I_p at the smallest p with
    V(p) = V(1). If V does not depend on p (to 1e-12), S_KW = 0."""
    if len(sys.env) != 1:
        raise ValueError("kw_stored needs one environment coordinate")
    A, E = list(sys.agent), list(sys.env)
    S0 = sys.S
    Phi, Q = (np.eye(S0.shape[0]), np.zeros_like(S0)) if tau == 0 else propagator(sys.B, sys.D, float(tau))

    def S_p(p):
        S = S0.copy()
        S[np.ix_(A, E)] *= p
        S[np.ix_(E, A)] *= p
        return S
    V = lambda p: _neg_entropy(Phi @ S_p(p) @ Phi.T + Q, sys.target)
    Sx, Sxy, Sy = S0[np.ix_(A, A)], S0[np.ix_(A, E)], S0[E[0], E[0]]
    rho2 = float(Sxy[:, 0] @ np.linalg.solve(Sx, Sxy[:, 0]) / Sy)
    I = lambda p: float(-0.5 * np.log(1 - p * p * rho2))
    V_act = V(1.0)
    g = lambda p: V(p) - V_act
    grid = np.linspace(0.0, 1.0, n_grid + 1)
    vals = [g(p) for p in grid[:-1]]
    if max(abs(x) for x in vals) <= 1e-12 * (1 + abs(V_act)):
        return 0.0
    for i in range(n_grid - 1):
        lo, hi, flo = grid[i], grid[i + 1], vals[i]
        if flo == 0.0:
            return I(lo)
        if np.sign(flo) == np.sign(vals[i + 1]):
            continue
        for _ in range(iters):
            mid = (lo + hi) / 2; fm = g(mid)
            lo, hi, flo = (mid, hi, fm) if np.sign(fm) == np.sign(flo) else (lo, mid, flo)
        return I((lo + hi) / 2)
    return I(1.0)


def _logpdf(Z, S):
    L = np.linalg.cholesky(S)
    y = np.linalg.solve(L, Z.T)
    return -0.5 * (np.sum(y * y, axis=0) + S.shape[0] * np.log(2 * np.pi)) - np.sum(np.log(np.diag(L)))


def js_gaussian(S1, S2, n=200_000, rng=None):
    """JS(N(0, S1) || N(0, S2)) in bits by Monte Carlo with the exact densities. Returns (js, standard error)."""
    rng = np.random.default_rng(0) if rng is None else rng
    d = S1.shape[0]
    terms = []
    for Sa, Sb in ((S1, S2), (S2, S1)):
        Z = rng.normal(size=(n, d)) @ np.linalg.cholesky(Sa).T
        la, lb = _logpdf(Z, Sa), _logpdf(Z, Sb)
        lm = np.logaddexp(la, lb) - np.log(2.0)
        terms.append((la - lm) / LN2)
    js = 0.5 * (terms[0].mean() + terms[1].mean())
    se = 0.5 * np.sqrt(terms[0].var() / n + terms[1].var() / n)
    return float(js), float(se)


def cld_linear(sys, times=(1.0,), n=200_000, seed=0, keep=None):
    """CLD chi(t) on the coordinates `keep` (default: all of z). Returns (Omega in bits, chi array, se array)."""
    keep = list(range(sys.S.shape[0])) if keep is None else list(keep)
    omega = mutual_information(sys.S, sys.agent, sys.env) / LN2
    S0h = _scrambled(sys.S, sys.agent, sys.env)
    chi, se = [], []
    ix = np.ix_(keep, keep)
    for k, t in enumerate(times):
        St, Sh = sys.cov_at(t), sys.cov_at(t, S0h)
        js, e = js_gaussian(St[ix], Sh[ix], n, np.random.default_rng([seed, k]))
        chi.append(js / omega); se.append(e / omega)
    return float(omega), np.array(chi), np.array(se)


def _js_mirror(x, v, xr, vr, bins):
    i = np.clip(((x + xr) / (2 * xr) * bins).astype(int), 0, bins - 1)
    j = np.clip(((v + vr) / (2 * vr) * bins).astype(int), 0, bins - 1)
    Hh = np.bincount(i * bins + j, minlength=bins * bins).reshape(bins, bins).astype(float)
    p = Hh / Hh.sum()
    q = 0.5 * (p + p[::-1, ::-1])
    m = 0.5 * (p + q)
    with np.errstate(divide="ignore", invalid="ignore"):
        a = np.where(p > 0, p * np.log2(p / m), 0.0).sum()
        b = np.where(q > 0, q * np.log2(q / m), 0.0).sum()
    return float(0.5 * (a + b))


def cld_unit(u, n=20_000, n_times=41, dt=0.01, t_burn=50.0, bins=40, rng=None):
    """CLD of the bit b = sign(x) of an S2 unit on [0, tau*] (Omega = 1 bit). A second group starts with b scrambled,
    and its value (the bias of the histogram) is subtracted. Returns dict(chi3, chi1): the time average and the value
    at tau*."""
    rng = np.random.default_rng([u.seed, u.i, 31]) if rng is None else rng
    times = np.linspace(0.0, u.tau_star, n_times)
    x, v = initial(u, 2 * n, rng)
    x, v = run(u, x, v, t_burn, True, dt, rng)
    flip = x < 0
    x, v = np.where(flip, -x, x), np.where(flip, -v, v)
    xr, vr = 1.1 * np.abs(x).max(), 1.1 * np.abs(v).max()
    coin = rng.random(n) < 0.5
    x[n:][coin], v[n:][coin] = -x[n:][coin], -v[n:][coin]
    chi, t_now = [], 0.0
    for t in times:
        for _ in range(int(round((t - t_now) / dt))):
            x, v = step(u, x, v, True, dt, rng)
        t_now = t
        chi.append(_js_mirror(x[:n], v[:n], xr, vr, bins) - _js_mirror(x[n:], v[n:], xr, vr, bins))
    chi = np.array(chi)
    return dict(chi3=float(np.trapezoid(chi, times) / (times[-1] - times[0])), chi1=float(chi[-1]))


def flux_ratio(u):
    """log(V_on / V_off): 0 for a passive unit, above 0 when a drive keeps the unit alive."""
    return float(np.log(u.V_on / u.V_off))
