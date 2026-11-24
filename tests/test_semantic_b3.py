import numpy as np
from vlife.semantic_dynamic import (stationary_cov_discrete, sensor, run, viability, transfer_entropy, trajectory_cov,
                                    information_measures, min_observed, projection_sensors_dy2)


def _system(seed, dx, dy):
    rng = np.random.default_rng(seed); n = dx + dy
    A = rng.normal(size=(n, n))
    F = 0.85 * A / np.max(np.abs(np.linalg.eigvals(A)))
    W = np.diag(rng.uniform(0.3, 1.5, n))
    return F, W


def test_actual_sensor_keeps_the_stationary_law():
    F, W = _system(911, 1, 2)
    S0 = stationary_cov_discrete(F, W)
    covs, te, _ = run(F, W, 1, np.eye(2), np.zeros((2, 2)), 4)
    assert all(np.allclose(S, S0, atol=1e-10) for S in covs)
    assert np.allclose(te, te[0])


def test_full_scrambling_has_no_transfer_entropy():
    F, W = _system(912, 2, 2)
    _, te, _ = run(F, W, 2, np.zeros((2, 2)), np.eye(2), 4)
    assert np.allclose(te, 0, atol=1e-12)


def test_one_step_viability_does_not_depend_on_the_sensor():
    """Theorem (docs/B.md, B3): the intervention keeps p(x_{t+1} | x_t), so V at tau = 1 never changes."""
    F, W = _system(913, 1, 2)
    rng = np.random.default_rng(0)
    V_act = viability(F, W, 1, np.eye(2), np.zeros((2, 2)), 1)
    for _ in range(5):
        K, SN = sensor(rng.uniform(-3, 3, 1), rng.uniform(0, 1, 2))
        assert abs(viability(F, W, 1, K, SN, 1) - V_act) < 1e-10


def test_trajectory_covariance_matches_the_recursion():
    F, W = _system(914, 1, 2)
    K, SN = sensor([0.7], [0.8, 0.3])
    covs, te, _ = run(F, W, 1, K, SN, 3)
    cov, ix, iy, iz = trajectory_cov(F, W, 1, K, SN, 3)
    for t in range(4):
        idx = ix[t] + iy[t]
        assert np.allclose(cov[np.ix_(idx, idx)], covs[t], atol=1e-10)
    TE, DI, DT = information_measures(F, W, 1, K, SN, 3)
    assert np.isclose(TE, te.sum(), atol=1e-10)


def test_directed_information_is_at_most_the_transfer_entropy():
    """Theorem T1 (docs/B.md, B3)."""
    F, W = _system(915, 2, 2)
    rng = np.random.default_rng(1)
    for _ in range(5):
        K, SN = sensor(rng.uniform(-3, 3, 1), rng.uniform(0, 0.99, 2))
        TE, DI, DT = information_measures(F, W, 2, K, SN, 4)
        assert DI <= TE + 1e-10 and np.isfinite(DT)


def test_recursion_against_sampling_of_eq_18():
    """Independent check of the intervened law: sample the process, and at each step get p^(y | x, z) by a linear
    regression of y on (x, z) over the samples (the Gaussian posterior), not by the formulas of the module."""
    F, W = _system(916, 1, 2); dx, dy, tau, n = 1, 2, 3, 200000
    K, SN = sensor([1.2], [0.5, 0.2])
    rng = np.random.default_rng(2)
    S0 = stationary_cov_discrete(F, W)
    z = rng.multivariate_normal(np.zeros(3), S0, size=n)
    x, y = z[:, :dx], z[:, dx:]
    for _ in range(tau):
        obs = y @ K.T + rng.normal(size=(n, dy)) * np.sqrt(np.diag(SN))
        Rg = np.hstack([x, obs])
        coef, *_ = np.linalg.lstsq(Rg, y, rcond=None)
        res = y - Rg @ coef
        yp = Rg @ coef + rng.multivariate_normal(np.zeros(dy), np.cov(res.T), size=n)
        x_new = x @ F[:dx, :dx].T + yp @ F[:dx, dx:].T + rng.normal(size=(n, dx)) * np.sqrt(W[0, 0])
        y = x @ F[dx:, :dx].T + y @ F[dx:, dx:].T + rng.normal(size=(n, dy)) * np.sqrt(np.diag(W)[dx:])
        x = x_new
    emp = np.cov(np.hstack([x, y]).T)
    covs, _, _ = run(F, W, dx, K, SN, tau)
    assert np.allclose(emp, covs[-1], rtol=0.03, atol=0.02)
    actual = run(F, W, dx, np.eye(dy), np.zeros((dy, dy)), tau)[0][-1]
    full = run(F, W, dx, np.zeros((dy, dy)), np.eye(dy), tau)[0][-1]
    assert not np.allclose(emp, actual, rtol=0.03, atol=0.02)   # the check can tell the sensor from the two ends
    assert not np.allclose(emp, full, rtol=0.03, atol=0.02)


def test_optimizers_return_feasible_points():
    F, W = _system(917, 1, 2)
    best, (a, s), n_best, n_feas = min_observed(F, W, 1, 4, "te", n_starts=4, rng=np.random.default_rng(3))
    K, SN = sensor(a, s)
    V_act = viability(F, W, 1, np.eye(2), np.zeros((2, 2)), 4)
    assert abs(viability(F, W, 1, K, SN, 4) - V_act) < 1e-6
    assert best <= transfer_entropy(F, W, 1, np.eye(2), np.zeros((2, 2)), 4) + 1e-12
    for a, te in projection_sensors_dy2(F, W, 1, 4, n_grid=90):
        K = np.array([[np.cos(a), np.sin(a)], [0, 0]])
        assert abs(viability(F, W, 1, K, np.diag([0.0, 1.0]), 4) - V_act) < 1e-8
