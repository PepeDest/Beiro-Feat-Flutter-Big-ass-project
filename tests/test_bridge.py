"""Fix #1 (docs/code_review.md): discrete monitoring at dt = 0.05 biases the MFPT upward, more for fast structures.
The Brownian-bridge option must give the exact MFPT (backward equation) at the settings of the experiments."""
import numpy as np
import pytest
from scipy.stats import chi2
from vlife.viability import simulate_exits, mfpt_all
from vlife.agency import simulate_exit_threshold
from test_viability import bvp_mfpt_1d

DT, P_OUT, THETAS = 0.05, 0.05, (0.3, 1.0, 3.0, 9.0)


def exact_1d(theta, D=1.0):
    a = np.sqrt(chi2.ppf(1 - P_OUT, 1) * D / theta)
    x, T = bvp_mfpt_1d(theta, D, a)
    p = np.exp(-x ** 2 * theta / (2 * D)); inside = np.abs(x) < a
    return (T * p)[inside].sum() / p[inside].sum(), a


def exact_radial(theta, d, D=1.0, n=4001):
    """Isotropic OU in d dimensions, exit from the ball of stationary mass 1 - p_out. Radial backward equation
    D T'' + (D (d - 1)/r - theta r) T' = -1, T'(0) = 0, T(R) = 0; averaged over the stationary law inside."""
    R = np.sqrt(chi2.ppf(1 - P_OUT, d) * D / theta)
    r = np.linspace(0, R, n); h = r[1] - r[0]
    A = np.zeros((n, n)); b = -np.ones(n)
    A[0, 0], A[0, 1] = -2 * d * D / h ** 2, 2 * d * D / h ** 2          # at r = 0: d D T''(0) = -1
    for i in range(1, n - 1):
        drift = D * (d - 1) / r[i] - theta * r[i]
        A[i, i - 1] = D / h ** 2 - drift / (2 * h); A[i, i] = -2 * D / h ** 2; A[i, i + 1] = D / h ** 2 + drift / (2 * h)
    A[-1, -1] = 1; b[-1] = 0
    T = np.linalg.solve(A, b); w = r ** (d - 1) * np.exp(-theta * r ** 2 / (2 * D))
    return (T * w).sum() / w.sum()


@pytest.mark.parametrize("theta", THETAS)
def test_bridge_matches_exact_mfpt_1d(theta):
    ex, a = exact_1d(theta)
    B, S = np.array([[theta]]), np.array([[1.0 / theta]])
    kw = dict(p_out=P_OUT, n_traj=8000, dt=DT, t_max=300.0 / theta)
    V = mfpt_all(simulate_exits(B, S, [(0,)], rng=np.random.default_rng(1), bridge=True, **kw))[0][0]
    assert abs(V / ex - 1) < 0.05, (theta, V, ex)
    V_old = mfpt_all(simulate_exits(B, S, [(0,)], rng=np.random.default_rng(1), **kw))[0][0]
    assert V_old / ex > 1.2                                               # the documented bias of the old method
    Va = simulate_exit_threshold(B, S, 0, a, 8000, DT, 300.0 / theta, np.random.default_rng(2), bridge=True)[0]
    assert abs(Va / ex - 1) < 0.05, (theta, Va, ex)


def test_bridge_matches_exact_mfpt_2d_ball():
    theta = 3.0; ex = exact_radial(theta, 2)
    B, S = theta * np.eye(2), np.eye(2) / theta
    V = mfpt_all(simulate_exits(B, S, [(0, 1)], P_OUT, 8000, DT, 100.0, np.random.default_rng(3), bridge=True))[0][0]
    V_old = mfpt_all(simulate_exits(B, S, [(0, 1)], P_OUT, 8000, DT, 100.0, np.random.default_rng(3)))[0][0]
    assert abs(V / ex - 1) < 0.05 and V_old / ex > 1.2, (V, V_old, ex)


def test_default_path_is_unchanged():
    # Values of the old code (before fix #1), same seeds: bridge=False must give exactly the same numbers.
    from vlife.worlds import make_world
    from vlife.agency import draw_organism, homeostat, V
    w = make_world("driven", 4, np.random.default_rng(5))
    d = simulate_exits(w.B, w.S, [(0,), (1, 2), (0, 1, 3)], 0.05, 300, 0.05, 30.0, np.random.default_rng(9))
    assert d.exit_t.sum() == 6257.35 and int(d.event.sum()) == 845 and not d.bridge
    assert mfpt_all(d)[0].tolist() == [5.983451957295374, 5.891958041958042, 5.434892086330936]
    o = draw_organism(np.random.default_rng(3)); B, D, S = homeostat(o, "intact")
    r = simulate_exit_threshold(B, S, V, 1.2816 * np.sqrt(S[V, V]), 300, 0.05, 50.0, np.random.default_rng(4))
    assert r == (7.430168776371308, 237, 238)
