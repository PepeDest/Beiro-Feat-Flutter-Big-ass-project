import numpy as np
from vlife.gaussian import stationary_cov, mutual_information
from vlife.semantic import (garbling_matrix, projection, intervened_cov, syntactic_information, propagator,
                            agent_cov_at, viability, value_of_information)


def _system(seed, dx=2, dy=3):
    rng = np.random.default_rng(seed); n = dx + dy
    A = rng.normal(size=(n, n))
    B = A @ A.T / n + 0.5 * np.eye(n) + 0.8 * (A - A.T) / 2
    D = np.diag(rng.uniform(0.3, 1.5, n))
    return B, D, stationary_cov(B, D), dx, dy


def test_propagator_matches_the_lyapunov_solution():
    B, D, S, dx, dy = _system(1)
    for tau in (0.1, 1.0, 5.0):
        Phi, Q = propagator(B, D, tau)
        assert np.allclose(Q, S - Phi @ S @ Phi.T, atol=1e-10)


def test_actual_and_full_scrambling_are_the_two_ends():
    B, D, S, dx, dy = _system(2)
    assert np.allclose(intervened_cov(S, dx, np.eye(dy)), S)
    full = intervened_cov(S, dx, np.zeros((dy, dy)))
    assert np.allclose(full[:dx, dx:], 0) and np.allclose(full[:dx, :dx], S[:dx, :dx])
    assert np.isclose(syntactic_information(S, dx, np.eye(dy)), mutual_information(S, range(dx), range(dx, dx + dy)))
    assert abs(syntactic_information(S, dx, np.zeros((dy, dy)))) < 1e-12


def test_projection_equals_the_information_of_the_coarse_grained_environment():
    B, D, S, dx, dy = _system(3)
    rng = np.random.default_rng(30)
    U = rng.normal(size=(dy, 1))
    P = projection(U)
    # phi(y) = U^T Sigma_Y^{-1/2} y: joint covariance of (x, phi(y))
    w, V = np.linalg.eigh(S[dx:, dx:]); Syih = (V / np.sqrt(w)) @ V.T
    T = np.zeros((dx + 1, dx + dy)); T[:dx, :dx] = np.eye(dx); T[dx:, dx:] = U.T @ Syih
    assert np.isclose(syntactic_information(S, dx, P), mutual_information(T @ S @ T.T, range(dx), [dx]))


def test_garbling_matrix_is_between_zero_and_identity():
    B, D, S, dx, dy = _system(4)
    rng = np.random.default_rng(40)
    P = garbling_matrix(rng.normal(size=(2, dy)), np.diag([0.3, 4.0]), S[dx:, dx:])
    ev = np.linalg.eigvalsh(P)
    assert ev.min() > -1e-12 and ev.max() < 1 + 1e-12


def test_viability_is_affine_in_p_inside_the_log_det():
    B, D, S, dx, dy = _system(5)
    rng = np.random.default_rng(50)
    P1 = projection(rng.normal(size=(dy, 1))); P2 = projection(rng.normal(size=(dy, 2)))
    a = 0.3
    lhs = agent_cov_at(B, D, S, dx, a * P1 + (1 - a) * P2, 1.0)
    rhs = a * agent_cov_at(B, D, S, dx, P1, 1.0) + (1 - a) * agent_cov_at(B, D, S, dx, P2, 1.0)
    assert np.allclose(lhs, rhs)


def test_no_effect_when_the_environment_does_not_drive_the_agent():
    B, D, S, dx, dy = _system(6)
    B[:dx, dx:] = 0.0                                  # x does not depend on y
    S = stationary_cov(B, D)
    assert abs(value_of_information(B, D, S, dx, 2.0)) < 1e-10
