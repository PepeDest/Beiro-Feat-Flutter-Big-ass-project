import numpy as np
from scipy.linalg import schur, sqrtm
from vlife.gaussian import oscillatory_nonnormal_ep, entropy_production, stationary_cov
from vlife.worlds import make_world


def _nn_by_projection(B, D):
    """sigma_nn from the definition of NagayamaKolchinskyIto26 (Eq. 6-10), as an independent check:
    whiten, take the complex Schur form T of K~, H = (T + T^H)/2, S = (T - T^H)/2, project S on {H X : X diagonal}
    with the H^{-1} inner product, and return the squared distance."""
    V = stationary_cov(B, D)
    Vh = np.real(sqrtm(V))
    Kt = np.linalg.inv(Vh) @ B @ Vh
    T, _ = schur(Kt.astype(complex), output="complex")
    H = (T + T.conj().T) / 2
    Sk = (T - T.conj().T) / 2
    lam = np.diag(T)
    S_star = H @ np.diag(1j * lam.imag / lam.real)
    R = Sk - S_star
    return float(np.real(np.trace(R.conj().T @ np.linalg.inv(H) @ R)))


def test_parts_sum_to_total_and_are_nonnegative():
    rng = np.random.default_rng(3)
    for fam in ("driven", "modular_driven"):
        for _ in range(5):
            w = make_world(fam, 6, rng)
            s, so, sn = oscillatory_nonnormal_ep(w.B, w.D, w.S)
            assert np.isclose(s, entropy_production(w.B, w.D, w.S))
            assert np.isclose(so + sn, s)
            assert so >= -1e-10 and sn >= -1e-10


def test_nonnormal_part_matches_the_projection_definition():
    rng = np.random.default_rng(4)
    for kw in ({}, {"noise_range": 3.0}):
        w = make_world("driven", 6, rng, **kw)
        _, _, sn = oscillatory_nonnormal_ep(w.B, w.D, w.S)
        assert np.isclose(sn, _nn_by_projection(w.B, w.D), rtol=1e-6, atol=1e-9)


def test_equilibrium_has_no_dissipation_in_either_part():
    w = make_world("equilibrium", 6, np.random.default_rng(5))
    s, so, sn = oscillatory_nonnormal_ep(w.B, w.D, w.S)
    assert abs(s) < 1e-10 and abs(so) < 1e-10 and abs(sn) < 1e-10


def test_normal_drift_is_purely_oscillatory():
    # B = a I + G with G antisymmetric and D = I: B is normal, so sigma_nn = 0 and sigma = sum Im^2 / Re.
    rng = np.random.default_rng(6)
    M = rng.normal(size=(4, 4))
    B = 1.3 * np.eye(4) + (M - M.T)
    s, so, sn = oscillatory_nonnormal_ep(B, np.eye(4))
    assert s > 0 and abs(sn) < 1e-8 * s and np.isclose(so, s)


def test_two_temperatures_with_a_conservative_force_is_purely_nonnormal():
    # Symmetric B (a quadratic potential) with two bath temperatures: real eigenvalues, so sigma_osc = 0 and sigma_nn > 0.
    B = np.array([[2.0, 0.7], [0.7, 1.0]])
    D = np.diag([1.0, 3.0])
    s, so, sn = oscillatory_nonnormal_ep(B, D)
    assert abs(so) < 1e-12 and sn > 0 and np.isclose(sn, s)
