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


def _invariance_residual(M, rows):
    Q = np.linalg.qr(rows.T)[0]; X = M @ Q
    return np.linalg.norm(X - Q @ (Q.T @ X)) / np.linalg.norm(X)


def test_tica_subspace_is_a_real_invariant_subspace():
    # Fix #3 (docs/code_review.md): the TICA basis must span an invariant subspace of S^-1 C_tica, also when the
    # leading modes are complex. The old recipe (real part of each eigenvector) does not.
    split = 0
    for s in range(20):
        w = make_world("driven", 6, np.random.default_rng(100 + s))
        Ct = lagged_cov(w.B, w.S, 1.0).T; M = np.linalg.solve(w.S, Ct)
        for k in (1, 2, 3):
            mu, rows, m = tica_subspace(Ct, w.S, k)
            assert m in (k, k + 1) and rows.shape == (m, 6)
            assert np.allclose(rows @ rows.T, np.eye(m), atol=1e-10)
            assert _invariance_residual(M, rows) < 1e-8
            split += m == k + 1
    assert split > 0                                     # the pair-keeping branch is exercised


def test_tica_subspace_equals_gib_when_reversible():
    w = make_world("equilibrium", 6, np.random.default_rng(1))
    Sxy = lagged_cov(w.B, w.S, 1.0).T
    lam, V, _ = gib_modes(w.S, w.S, Sxy)
    for k in (1, 2, 3):
        _, rows, m = tica_subspace(Sxy, w.S, k)
        assert m == k and subspace_gap(V[:k], rows) < 1e-6


def test_gib_projection_rejects_a_fully_determined_direction():
    # Fix #10 (docs/code_review.md): lambda_1 = 0 used to give a division by zero and an infinite row.
    import pytest
    Sx, Sy, Sxy = np.eye(2), np.eye(2), np.diag([1.0, 0.5])            # x_1 = y_1 exactly
    lam, _, bc = gib_modes(Sx, Sy, Sxy)
    assert np.isclose(lam.min(), 0.0, atol=1e-12)
    with pytest.raises(ValueError):
        gib_projection(Sx, Sy, Sxy, 5.0)
    assert gib_projection(Sx, Sy, Sxy, 0.5).shape == (0, 2)            # below every critical beta: no active mode
