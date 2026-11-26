import numpy as np
from scipy.integrate import quad
from vlife.negative_controls import js_gaussian, cld_gaussian, js_mirror, cld_mirror, time_average
from vlife.semantic_apply import value_on, stored_semantic
from vlife.gaussian import mutual_information
from vlife.agency import draw_organism, homeostat
from vlife.nonlinear import Unit


def _js_1d(s1, s2):
    p = lambda x, s: np.exp(-x * x / (2 * s * s)) / (s * np.sqrt(2 * np.pi))
    m = lambda x: 0.5 * (p(x, s1) + p(x, s2))
    f = lambda x, s: p(x, s) * np.log2(p(x, s) / m(x))
    L = 12 * max(s1, s2)
    return 0.5 * (quad(f, -L, L, args=(s1,), limit=200)[0] + quad(f, -L, L, args=(s2,), limit=200)[0])


def test_js_gaussian_against_quadrature():
    js, se = js_gaussian(np.array([[1.0]]), np.array([[2.5 ** 2]]), n=400_000)
    assert abs(js - _js_1d(1.0, 2.5)) < 4 * se + 1e-4
    js0, _ = js_gaussian(np.eye(3), np.eye(3), n=10_000)
    assert abs(js0) < 1e-12


def test_cld_at_time_zero_is_js_of_joint_and_product():
    """2-D joint (x, y) with correlation r: compare chi(0) * Omega with a grid integral of JS(p || p_x p_y)."""
    r = 0.6
    S0 = np.array([[1.0, r], [r, 1.0]])
    B, D = np.eye(2), np.eye(2)
    omega, chi, se = cld_gaussian(B, D, S0, [0], [1], [0.0], n=400_000)
    assert np.isclose(omega, -0.5 * np.log2(1 - r * r))
    g = np.linspace(-8, 8, 801); X, Y = np.meshgrid(g, g); dA = (g[1] - g[0]) ** 2
    p = np.exp(-(X * X - 2 * r * X * Y + Y * Y) / (2 * (1 - r * r))) / (2 * np.pi * np.sqrt(1 - r * r))
    q = np.exp(-(X * X + Y * Y) / 2) / (2 * np.pi)
    m = 0.5 * (p + q)
    js = 0.5 * (np.sum(p * np.log2(p / m)) + np.sum(q * np.log2(q / m))) * dA
    assert abs(chi[0] * omega - js) < 4 * se[0] * omega + 1e-4


def test_cld_decays_for_a_stable_system():
    B = np.array([[1.0, -0.5], [0.0, 0.7]]); D = np.diag([0.2, 0.3])
    from vlife.gaussian import stationary_cov
    S0 = stationary_cov(B, D)
    _, chi, _ = cld_gaussian(B, D, S0, [0], [1], [0.0, 1.0, 20.0], n=100_000)
    assert chi[0] > chi[1] > 0 and chi[2] < 1e-3


def test_F6_no_feedback_gives_negative_value_and_full_stored_information():
    o = draw_organism(np.random.default_rng(7))
    B, D, S = homeostat(o, "nofeedback")
    agent, env = [1, 2, 3, 4], [0]
    for tau in (0.3, 1.0, 4.0):
        assert value_on(B, D, S, agent, env, tau, [3]) < 0
    S_kw, how = stored_semantic(B, D, S, agent, env, 1.0, target=[3])
    assert how.startswith("root") and np.isclose(S_kw, mutual_information(S, agent, env))


def test_js_mirror_is_zero_for_a_symmetric_sample_and_known_for_disjoint_halves():
    rng = np.random.default_rng(1)
    x, v = rng.normal(size=200_000), rng.normal(size=200_000)
    xs, vs = np.concatenate([x, -x]), np.concatenate([v, -v])
    assert js_mirror(xs, vs, 5.0, 5.0) < 1e-12
    xp = np.abs(x) + 0.01                                   # all mass at x > 0, so p and R p are disjoint
    assert np.isclose(js_mirror(xp, v, 5.0, 5.0), _disjoint_js(), atol=1e-9)
    assert np.isclose(_disjoint_js(), 0.3113, atol=1e-4)


def _disjoint_js():
    """JS(p || (p + q) / 2) for p, q with disjoint supports: m = 3/4 p + 1/4 q."""
    kl_p = np.log2(4 / 3)                                    # p against m on supp p
    kl_q = 0.5 * np.log2((1 / 2) / (3 / 4)) + 0.5 * np.log2((1 / 2) / (1 / 4))
    return 0.5 * kl_p + 0.5 * kl_q


def test_cld_mirror_rock_keeps_memory_and_null_is_small():
    rock = Unit("rock", dict(h=0.4))                         # high barrier: rare well switches
    well = Unit("well", dict(k=1.0))                         # one well: the sign of x is lost fast
    ts = [0.0, 5.0]
    r = cld_mirror(rock, 4000, ts, 0.01, np.random.default_rng(2), t_burn=5.0)
    w = cld_mirror(well, 4000, ts, 0.01, np.random.default_rng(3), t_burn=5.0)
    assert r["chi"][0] > 0.25 and w["chi"][0] > 0.25          # both start near 0.311 bits
    assert r["chi"][1] > 0.15 and w["chi"][1] < 0.02
    assert abs(r["chi_null"][1]) < 0.05 and abs(w["chi_null"][1]) < 0.05


def test_time_average():
    assert np.isclose(time_average([0, 1, 2], np.array([1.0, 1.0, 1.0])), 1.0)
    assert np.isclose(time_average([0, 2], np.array([0.0, 2.0])), 1.0)
