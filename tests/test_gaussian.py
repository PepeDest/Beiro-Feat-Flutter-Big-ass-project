import numpy as np
from vlife.gaussian import *
from vlife.worlds import make_world
from vlife.functional import static_mi, structure_features
from scipy.linalg import expm


def test_bivariate_mi_formula():
    rho = 0.6
    cov = np.array([[1, rho], [rho, 1.0]])
    assert np.isclose(mutual_information(cov, [0], [1]), -0.5 * np.log(1 - rho ** 2))


def test_lyapunov_and_equilibrium_counterpart():
    w = make_world("driven", 6, np.random.default_rng(1))
    assert np.allclose(w.B @ w.S + w.S @ w.B.T, 2 * w.D)
    Be = w.B_eq()
    assert np.allclose(Be @ w.S + w.S @ Be.T, 2 * w.D)


def test_entropy_production_zero_iff_equilibrium():
    w = make_world("equilibrium", 6, np.random.default_rng(2))
    assert abs(entropy_production(w.B, w.D, w.S)) < 1e-9
    w = make_world("driven", 6, np.random.default_rng(2))
    assert entropy_production(w.B, w.D, w.S) > 1e-3
    assert abs(entropy_production(w.B_eq(), w.D, w.S)) < 1e-9


def test_lagged_cov_matches_simulation():
    rng = np.random.default_rng(3)
    w = make_world("driven", 3, rng, flux=1.0)
    tau = 0.7
    P = expm(-w.B * tau); Cn = w.S - P @ w.S @ P.T
    L = np.linalg.cholesky(Cn); x = np.linalg.cholesky(w.S) @ rng.normal(size=(3, 200000))
    y = P @ x + L @ rng.normal(size=(3, 200000))
    emp = y @ x.T / x.shape[1]
    assert np.allclose(emp, lagged_cov(w.B, w.S, tau), atol=0.03)


def test_entropy_additivity_identity():
    # h(A u B) = h(A) + h(B) - I(A;B)  (static, disjoint)   [CoverThomas06 ch.2/8]
    w = make_world("driven", 6, np.random.default_rng(4))
    A, B = (0, 1), (3,)
    lhs = differential_entropy(w.S, list(A) + list(B))
    rhs = differential_entropy(w.S, A) + differential_entropy(w.S, B) - static_mi(w, A, B)
    assert np.isclose(lhs, rhs)


def test_features_nonnegative_and_bounded():
    w = make_world("modular_driven", 6, np.random.default_rng(5))
    f = structure_features(w, 1.0)
    assert (f["C"] >= -1e-9).all() and (f["P"] >= -1e-9).all() and (f["leak"] >= -1e-9).all()


def test_modular_blocks_for_sweep_sizes():
    # S1 sweep (docs/S1.md): modular worlds keep a block structure for N = 5, 6, 7.
    for N, blocks in ((5, [3, 2]), (6, [3, 2, 1]), (7, [3, 2, 2])):
        w = make_world("modular_driven", N, np.random.default_rng(N))
        assert w.params["blocks"] == blocks and sum(blocks) == N
        assert np.allclose(w.B @ w.S + w.S @ w.B.T, 2 * w.D)


def test_diagonal_noise_worlds_for_d_test():
    # S1 D-test (docs/S1.md): same B_s and G as with D = I, B = D (B_s + G), equilibrium stays reversible.
    for fam in ("equilibrium", "driven", "modular_driven"):
        base = make_world(fam, 6, np.random.default_rng(11))
        w = make_world(fam, 6, np.random.default_rng(11), noise_range=3.0)
        d = np.diag(w.D)
        assert np.all((d >= 1 / 3) & (d <= 3)) and np.allclose(w.B, w.D @ base.B)
        assert np.allclose(w.B @ w.S + w.S @ w.B.T, 2 * w.D)
        sigma = entropy_production(w.B, w.D, w.S)
        assert (abs(sigma) < 1e-9) if fam == "equilibrium" else (sigma > 1e-3)


def test_total_correlation_is_free_of_units():
    # S1b rule R1 (docs/S1b_unitfree.md): rescaling each variable keeps the Phi_TC ranking and changes the Phi_orig ranking.
    from scipy.stats import rankdata
    from vlife.worlds import World
    from vlife.functional import all_subsets
    w = make_world("driven", 6, np.random.default_rng(21))
    c = np.diag(np.exp(np.random.default_rng(22).uniform(-2, 2, 6)))
    ci = np.linalg.inv(c)
    w2 = World(B=c @ w.B @ ci, D=c @ w.D @ c, S=c @ w.S @ c, family="driven")
    assert np.allclose(w2.B @ w2.S + w2.S @ w2.B.T, 2 * w2.D)
    subs = all_subsets(6)
    f1, f2 = structure_features(w, 1.0, subs), structure_features(w2, 1.0, subs)
    assert np.allclose(f1["P"], f2["P"]) and np.allclose(f1["C"], f2["C"])
    tc1 = np.array([total_correlation(w.S, s) for s in subs]); tc2 = np.array([total_correlation(w2.S, s) for s in subs])
    assert np.allclose(tc1, tc2) and np.all(tc1 >= -1e-12)
    assert np.isclose(total_correlation(w.S, [0, 1]), mutual_information(w.S, [0], [1]))
    phi_tc = lambda f, tc: f["P"] + f["C"] - 0.25 * tc
    phi_orig = lambda f: f["P"] + f["C"] - 0.25 * f["KH"]
    assert np.array_equal(rankdata(phi_tc(f1, tc1)), rankdata(phi_tc(f2, tc2)))
    assert not np.array_equal(rankdata(phi_orig(f1)), rankdata(phi_orig(f2)))


def test_structure_entropy_production_sums_to_total():
    # S2c (docs/S2c.md): the parts over all coordinates add up to the total; zero in equilibrium worlds.
    for fam, r in (("driven", None), ("modular_driven", 3.0), ("equilibrium", 3.0)):
        w = make_world(fam, 6, np.random.default_rng(31), noise_range=r)
        parts = [structure_entropy_production(w.B, w.D, w.S, [i]) for i in range(6)]
        assert np.isclose(sum(parts), entropy_production(w.B, w.D, w.S)) and min(parts) >= -1e-12
        if fam == "equilibrium":
            assert abs(sum(parts)) < 1e-9
