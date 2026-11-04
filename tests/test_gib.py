import numpy as np
from scipy.optimize import minimize
from vlife.gib import *
from vlife.worlds import make_world
from vlife.gaussian import lagged_cov


def _random_xy(rng, n=3):
    M = rng.normal(size=(2 * n, 2 * n)); J = M @ M.T + 0.5 * np.eye(2 * n)
    return J[:n, :n], J[n:, n:], J[:n, n:]


def test_gib_analytic_solution_is_optimal():
    rng = np.random.default_rng(0)
    Sx, Sy, Sxy = _random_xy(rng)
    lam, V, bc = gib_modes(Sx, Sy, Sxy)
    assert np.all(lam > 0) and np.all(lam <= 1 + 1e-9)
    beta = 0.5 * (bc[0] + bc[1]) if bc[1] > bc[0] else 1.5 * bc[0]       # between 1st and 2nd critical value
    A = gib_projection(Sx, Sy, Sxy, beta)
    assert A.shape[0] == int(np.sum(beta >= bc))
    Lan = gib_objective(A, Sx, Sy, Sxy, beta)
    best = np.inf
    for s in range(6):
        a0 = np.random.default_rng(s).normal(size=(3, 3)) * 0.5
        r = minimize(lambda v: gib_objective(v.reshape(3, 3), Sx, Sy, Sxy, beta), a0.ravel(), method="BFGS")
        best = min(best, r.fun)
    assert Lan <= best + 1e-5 and abs(Lan - best) < 1e-3, (Lan, best)   # analytic == numerical optimum


def _gib_vs_tica(world, tau, k):
    C = lagged_cov(world.B, world.S, tau)               # E[x_{t+tau} x_t^T]
    Sxy = C.T                                           # E[x_t x_{t+tau}^T]
    lam, V, _ = gib_modes(world.S, world.S, Sxy)
    mu, Vt = tica_modes(Sxy, world.S)
    return subspace_gap(V[:k], Vt[:k])


def test_gib_equals_tica_when_reversible():
    w = make_world("equilibrium", 6, np.random.default_rng(1))
    assert _gib_vs_tica(w, 1.0, 2) < 1e-6


def test_gib_differs_from_tica_when_irreversible():
    gaps = [_gib_vs_tica(make_world("driven", 6, np.random.default_rng(s)), 1.0, 2) for s in range(5)]
    assert max(gaps) > 1e-3
