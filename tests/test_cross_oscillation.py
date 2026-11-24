import numpy as np
from vlife.controlled import draw, matrices
from vlife.gaussian import cross_oscillation, oscillatory_nonnormal_ep, stationary_cov


def _unrotated(seed):
    w = draw(np.random.default_rng(seed))
    return dict(w, Q=np.eye(6))


def test_whole_blocks_give_zero_and_a_cut_block_gives_its_full_weight():
    w = _unrotated(21)
    B, D, S = matrices(w, 2.0, 0.0)
    r = w["r"]
    assert abs(cross_oscillation(B, S, [0, 1])) < 1e-9
    assert abs(cross_oscillation(B, S, [0, 1, 4, 5])) < 1e-9
    assert np.isclose(cross_oscillation(B, S, [0]), 2 * 4.0 * r[0])
    assert np.isclose(cross_oscillation(B, S, [0, 2]), 2 * 4.0 * (r[0] + r[1]))
    assert np.isclose(cross_oscillation(B, S, [0, 1, 2]), 2 * 4.0 * r[1])


def test_complement_and_scale_invariance():
    rng = np.random.default_rng(22)
    A = rng.normal(size=(5, 5)); B = A @ A.T / 5 + np.eye(5) + 1.5 * (A - A.T)
    D = np.diag(rng.uniform(0.5, 2.0, 5)); S = stationary_cov(B, D)
    a, c = [0, 3], [1, 2, 4]
    assert np.isclose(cross_oscillation(B, S, a), cross_oscillation(B, S, c))
    T = np.diag(rng.uniform(0.2, 5.0, 5))                 # rescale coordinates: x -> T x
    Bt, St = T @ B @ np.linalg.inv(T), T @ S @ T
    assert np.isclose(cross_oscillation(B, S, a), cross_oscillation(Bt, St, a))


def test_bounded_by_sigma_osc_and_zero_for_real_spectrum():
    rng = np.random.default_rng(23)
    A = rng.normal(size=(4, 4)); B = A @ A.T / 4 + np.eye(4) + (A - A.T)
    D = np.eye(4); S = stationary_cov(B, D)
    so = oscillatory_nonnormal_ep(B, D, S)[1]
    assert 0 <= cross_oscillation(B, S, [1, 2]) <= so + 1e-9
    Br = np.triu(rng.uniform(0.5, 1.0, (4, 4))) + np.eye(4)
    assert cross_oscillation(Br, stationary_cov(Br, D), [0, 1]) == 0.0
