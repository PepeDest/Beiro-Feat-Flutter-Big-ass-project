import numpy as np
from vlife.controlled import draw, eta_cap, matrices
from vlife.gaussian import stationary_cov, oscillatory_nonnormal_ep


def test_spectrum_is_fixed_and_identity_is_the_stationary_covariance():
    w = draw(np.random.default_rng(11)); ec = eta_cap(w)
    for om in (0.0, 1.0, 4.0):
        target = np.sort_complex(np.concatenate([w["r"] * (1 + 1j * om), w["r"] * (1 - 1j * om)]))
        for f in (0.0, 0.5, 1.0):
            B, D, S = matrices(w, om, f * ec)
            assert np.allclose(np.sort_complex(np.linalg.eigvals(B)), target, atol=1e-8)
            assert np.allclose(stationary_cov(B, D), S, atol=1e-8)
            assert np.linalg.eigvalsh(D)[0] >= 0.25 * w["r"].min() - 1e-9


def test_eta_moves_only_the_nonnormal_part():
    w = draw(np.random.default_rng(12)); ec = eta_cap(w)
    _, so0, sn0 = oscillatory_nonnormal_ep(*matrices(w, 2.0, 0.0))
    _, so1, sn1 = oscillatory_nonnormal_ep(*matrices(w, 2.0, ec))
    assert np.isclose(so0, so1) and np.isclose(so0, 2 * 4.0 * w["r"].sum())
    assert abs(sn0) < 1e-8 and sn1 > 0
