"""Non-Gaussian interventions in the scalar case dx = dy = 1 (niche B, step B2b, docs/B.md).

Whitened start: x_0 and y_0 standard normal with correlation c. The intervention is a deterministic partition of y
(cells given as boolean masks on a y-grid), as in KolchinskyWolpert18, Eq. (8): y_0 ~ N(0, 1), cell j = phi(y_0), and
x_0 is drawn from p(x_0 | cell j), independent of y_0 inside the cell. Then
    X_tau = a x_0 + b y_0 + xi,   xi ~ N(0, q),   a = Phi_XX sigma_X,  b = Phi_XY sigma_Y,  q = (Q_tau)_XX,
    X_tau | j = (a c) Y' + b Y + N(0, a^2 (1 - c^2) + q),   Y' and Y independent, both N(0, 1) restricted to cell j.
V = -H(X_tau) and I = I(x_0; phi(y_0)) by quadrature on grids. Our code. Checks: tests/test_semantic_b2.py.
"""
import numpy as np
from scipy.stats import norm
from scipy.signal import fftconvolve

YGRID = np.linspace(-8.0, 8.0, 3201)
DYG = YGRID[1] - YGRID[0]


def scalar_parameters(B, D, S0, tau):
    """(a, b, q, c) of the module docstring for a 2 x 2 system."""
    from vlife.semantic import propagator
    Phi, Q = propagator(B, D, tau)
    sx, sy = np.sqrt(S0[0, 0]), np.sqrt(S0[1, 1])
    return Phi[0, 0] * sx, Phi[0, 1] * sy, Q[0, 0], S0[0, 1] / (sx * sy)


def _scaled_density(pdf_y, s, xgrid):
    """Density of s * Y on xgrid, for Y with density pdf_y on YGRID and s != 0."""
    return np.interp(xgrid / s, YGRID, pdf_y, left=0.0, right=0.0) / abs(s)


def entropy_x_tau(cells, a, b, q, c, n_x=8001):
    """H(X_tau) in nats under the partition `cells` (a list of boolean masks on YGRID)."""
    sg = np.sqrt(a * a * (1 - c * c) + q)
    L = 8 * (abs(a * c) + abs(b)) + 10 * sg
    x = np.linspace(-L, L, n_x); h = x[1] - x[0]
    phi = norm.pdf(YGRID)
    gauss = norm.pdf(x, scale=sg)
    total = np.zeros_like(x)
    for m in cells:
        p = phi[m].sum() * DYG
        if p <= 0:
            continue
        f = np.where(m, phi, 0.0) / p
        dens = gauss
        for s in (a * c, b):
            if abs(s) > 1e-12:
                dens = fftconvolve(dens, _scaled_density(f, s, x), mode="same") * h
        total += p * dens
    total = np.clip(total, 1e-300, None)
    total /= total.sum() * h
    return float(-np.sum(total * np.log(total)) * h)


def information(cells, c, n_x=4001):
    """I(x_0; phi(y_0)) in nats = H(phi) - E_x H(phi | x), with y | x ~ N(c x, 1 - c^2)."""
    s = np.sqrt(1 - c * c)
    xs = np.linspace(-8, 8, n_x); wx = norm.pdf(xs)
    phi = norm.pdf(YGRID)
    pj = np.array([phi[m].sum() * DYG for m in cells])
    pj = pj / pj.sum()
    H = -np.sum(pj[pj > 0] * np.log(pj[pj > 0]))
    K = norm.pdf((YGRID[None, :] - c * xs[:, None]) / s)
    Pjx = np.stack([K[:, m].sum(1) for m in cells], 1)
    Pjx /= Pjx.sum(1, keepdims=True)
    Hc = -np.sum(Pjx * np.log(np.clip(Pjx, 1e-300, None)), 1)
    return float(H - np.sum(wx * Hc) / np.sum(wx))


def interval_cells(thresholds):
    """Cells of the partition of y by sorted thresholds (k - 1 thresholds give k intervals)."""
    t = np.concatenate([[-np.inf], np.sort(np.asarray(thresholds, float)), [np.inf]])
    return [(YGRID >= lo) & (YGRID < hi) for lo, hi in zip(t[:-1], t[1:])]


def symmetric_cells(t):
    """Two cells: |y| < t and |y| >= t (a partition that is not made of intervals)."""
    inner = np.abs(YGRID) < t
    return [inner, ~inner]
