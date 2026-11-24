import numpy as np
from scipy.stats import norm
from vlife.gaussian import stationary_cov
from vlife.semantic import viability, syntactic_information, drive_projection, drive_information, min_information
from vlife.semantic_nonlinear import scalar_parameters, entropy_x_tau, information, interval_cells


def _system(seed, dx, dy):
    rng = np.random.default_rng(seed); n = dx + dy
    A = rng.normal(size=(n, n))
    B = A @ A.T / n + 0.5 * np.eye(n) + 0.8 * (A - A.T) / 2
    D = np.diag(rng.uniform(0.3, 1.5, n))
    return B, D, stationary_cov(B, D)


def test_drive_projection_keeps_the_viability():
    B, D, S = _system(901, 2, 3)
    assert np.isclose(viability(B, D, S, 2, drive_projection(B, D, S, 2, 1.0), 1.0), viability(B, D, S, 2, np.eye(3), 1.0))


def test_scalar_agent_optimum_is_the_drive_projection():
    """dx = 1: no feasible P has less information than Pi_W (Cauchy-Schwarz argument in docs/B.md)."""
    B, D, S = _system(902, 1, 3)
    best, P, n_best, n_feas = min_information(B, D, S, 1, 1.0, "general", n_starts=16, rng=np.random.default_rng(0))
    assert np.isclose(best, drive_information(B, D, S, 1, 1.0), atol=1e-5)


def test_nonlinear_quadrature_limits():
    B, D, S = _system(903, 1, 1)
    a, b, q, c = scalar_parameters(B, D, S, 1.0)
    V_full = viability(B, D, S, 1, np.zeros((1, 1)), 1.0)
    V_act = viability(B, D, S, 1, np.eye(1), 1.0)
    assert abs(-entropy_x_tau(interval_cells([]), a, b, q, c) - V_full) < 1e-4
    assert abs(information(interval_cells([]), c)) < 1e-9
    fine = interval_cells(np.linspace(-3.5, 3.5, 199))
    assert abs(-entropy_x_tau(fine, a, b, q, c) - V_act) < 2e-3
    assert abs(information(fine, c) - syntactic_information(S, 1, np.eye(1))) < 1e-2


def test_median_split_information_against_sampling():
    rng = np.random.default_rng(904); c = 0.6; n = 400000
    x = rng.normal(size=n)
    p = norm.cdf(c * x / np.sqrt(1 - c * c))                  # P(y > 0 | x)
    p = np.clip(p, 1e-12, 1 - 1e-12)
    h = -(p * np.log(p) + (1 - p) * np.log(1 - p))
    assert abs(information(interval_cells([0.0]), c) - (np.log(2) - h.mean())) < 3e-3
