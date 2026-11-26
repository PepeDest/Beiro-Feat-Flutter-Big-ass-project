"""Niche C (docs/C.md): Causal Leverage Density (CLD) [Bartlett24; SowinskiEtAl25, Eqs. (4)-(7)] on our negative controls.

CLD at time t: chi(t) = JS(p_t || p^_t) / Omega_scr, JS in bits. p_t is the law of the state at t without the
intervention, p^_t the law with it. The intervention acts at t = 0, the dynamics do not change.

C1, linear Gaussian (S3 homeostat): the full scrambling of KolchinskyWolpert18, Cov(A_0, E_0) -> 0, from the stationary
law. Both laws are N(0, .), so JS comes from Monte Carlo with the exact densities. Omega_scr = I(A_0; E_0) in bits.

C2, nonlinear S2 units: the bit b = sign(x) is known at t = 0 (start: stationary law with x > 0) and the intervention
sets it to a fair coin, (x, v) -> (-x, -v) with probability 1/2. The units are symmetric under R(x, v) = (-x, -v), so
p^_t = (p_t + R p_t) / 2. We take p_t from a histogram on a grid that is symmetric about 0, and R p_t is its mirror.
A second group starts with b already scrambled, so its true CLD is 0, and its value is the bias of the estimate.
Omega_scr = 1 bit. Our code. Checks: tests/test_negative_controls.py.
"""
import numpy as np
from vlife.semantic import propagator, _logdet
from vlife.gaussian import mutual_information
from vlife.nonlinear import step, initial, run

LN2 = np.log(2.0)


def _logpdf(Z, S):
    """log density of N(0, S) at the rows of Z."""
    L = np.linalg.cholesky(S)
    y = np.linalg.solve(L, Z.T)
    return -0.5 * (np.sum(y * y, axis=0) + S.shape[0] * np.log(2 * np.pi)) - np.sum(np.log(np.diag(L)))


def js_gaussian(S1, S2, n=200_000, rng=None):
    """JS(N(0, S1) || N(0, S2)) in bits by Monte Carlo with exact densities. Returns (js, standard error)."""
    rng = np.random.default_rng(0) if rng is None else rng
    d = S1.shape[0]
    terms = []
    for Sa, Sb in ((S1, S2), (S2, S1)):
        Z = rng.normal(size=(n, d)) @ np.linalg.cholesky(Sa).T
        la, lb = _logpdf(Z, Sa), _logpdf(Z, Sb)
        lm = np.logaddexp(la, lb) - np.log(2.0)
        terms.append((la - lm) / LN2)                  # log2 p_a / m under p_a
    js = 0.5 * (terms[0].mean() + terms[1].mean())
    se = 0.5 * np.sqrt(terms[0].var() / n + terms[1].var() / n)
    return float(js), float(se)


def scrambled_cov(S0, agent, env):
    """S0 with the agent-environment block set to zero (the full scrambling of KolchinskyWolpert18, Eq. (5))."""
    S = S0.copy()
    S[np.ix_(agent, env)] = 0.0
    S[np.ix_(env, agent)] = 0.0
    return S


def cld_gaussian(B, D, S0, agent, env, times, n=200_000, seed=0, keep=None):
    """CLD chi(t) for each t in `times`, on the coordinates `keep` (default: all). Returns (Omega_bits, chi, se)."""
    keep = list(range(S0.shape[0])) if keep is None else list(keep)
    omega = mutual_information(S0, agent, env) / LN2
    S0h = scrambled_cov(S0, agent, env)
    chi, se = [], []
    for k, t in enumerate(times):
        if t == 0:
            St, Sh = S0, S0h
        else:
            Phi, Q = propagator(B, D, float(t))
            St, Sh = Phi @ S0 @ Phi.T + Q, Phi @ S0h @ Phi.T + Q
        ix = np.ix_(keep, keep)
        js, e = js_gaussian(St[ix], Sh[ix], n, np.random.default_rng([seed, k]))
        chi.append(js / omega); se.append(e / omega)
    return float(omega), np.array(chi), np.array(se)


def js_mirror(x, v, xr, vr, bins=40):
    """Plug-in JS(p || (p + R p) / 2) in bits from samples, on a bins x bins grid symmetric about 0 (bins even).
    Values outside [-xr, xr] x [-vr, vr] go to the edge cells."""
    i = np.clip(((x + xr) / (2 * xr) * bins).astype(int), 0, bins - 1)
    j = np.clip(((v + vr) / (2 * vr) * bins).astype(int), 0, bins - 1)
    H = np.bincount(i * bins + j, minlength=bins * bins).reshape(bins, bins).astype(float)
    p = H / H.sum()
    q = 0.5 * (p + p[::-1, ::-1])
    m = 0.5 * (p + q)
    with np.errstate(divide="ignore", invalid="ignore"):
        a = np.where(p > 0, p * np.log2(p / m), 0.0).sum()
        b = np.where(q > 0, q * np.log2(q / m), 0.0).sum()
    return float(0.5 * (a + b))


def cld_mirror(u, n, times, dt, rng, t_burn=200.0, bins=40):
    """C2: CLD of the bit b = sign(x) for an S2 unit (on dynamics). `times` sorted, the first may be 0.
    Returns dict(chi_known, chi_null, chi) with chi = chi_known - chi_null (Omega_scr = 1 bit)."""
    x, v = initial(u, 2 * n, rng)
    x, v = run(u, x, v, t_burn, True, dt, rng)
    flip = x < 0
    x, v = np.where(flip, -x, x), np.where(flip, -v, v)          # stationary law with x > 0 (by the symmetry R)
    xr, vr = 1.1 * np.abs(x).max(), 1.1 * np.abs(v).max()
    coin = rng.random(n) < 0.5                                   # group 2: b scrambled at t = 0
    x[n:][coin], v[n:][coin] = -x[n:][coin], -v[n:][coin]
    known, null, t_now = [], [], 0.0
    for t in times:
        for _ in range(int(round((t - t_now) / dt))):
            x, v = step(u, x, v, True, dt, rng)
        t_now = t
        known.append(js_mirror(x[:n], v[:n], xr, vr, bins)); null.append(js_mirror(x[n:], v[n:], xr, vr, bins))
    known, null = np.array(known), np.array(null)
    return dict(chi_known=known, chi_null=null, chi=known - null)


def time_average(times, chi):
    """chi_3 = (1 / (t2 - t1)) int chi dt by the trapezoid rule [SowinskiEtAl25, Eq. (6)]."""
    times = np.asarray(times, float)
    return float(np.trapezoid(chi, times) / (times[-1] - times[0]))
