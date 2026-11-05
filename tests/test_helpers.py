"""Night list item 8c: tests for src/vlife functions that had no direct test."""
import numpy as np
import pytest
from scipy.stats import spearmanr
from vlife.gaussian import conditional_mutual_information, mutual_information, joint_cov, stationary_cov
from vlife.estimators import ksg_mi, binned_mi, effective_sample_size_ar1
from vlife.stats import spearman_within, cluster_bootstrap
from vlife.price import selection_differential, price_decomposition
from vlife.viability import mfpt_from, bridge_crossing_prob
from vlife.blankets import make_planted_world, sample, estimates, edge_scores, static_graph
from vlife.nonlinear import Unit, draw_units, GAMMA0, T


def test_conditional_mi_chain_rule():
    rng = np.random.default_rng(0); M = rng.normal(size=(5, 5)); S = M @ M.T + np.eye(5)
    a, b, c = [0], [1, 2], [3, 4]
    lhs = mutual_information(S, a, b + c)
    assert np.isclose(lhs, mutual_information(S, a, c) + conditional_mutual_information(S, a, b, c))
    assert np.isclose(conditional_mutual_information(S, a, b, []), mutual_information(S, a, b))


def test_stationary_and_joint_cov():
    B = np.array([[1.0, 0.5], [-0.5, 2.0]]); D = np.diag([1.0, 0.5])
    S = stationary_cov(B, D); assert np.allclose(B @ S + S @ B.T, 2 * D)
    J = joint_cov(B, S, 0.0); assert np.allclose(J, np.block([[S, S], [S, S]]))


def test_ksg_on_a_gaussian_pair():
    rng = np.random.default_rng(1); rho = 0.8
    x = rng.normal(size=3000); y = rho * x + np.sqrt(1 - rho ** 2) * rng.normal(size=3000)
    assert abs(ksg_mi(x, y) - (-0.5 * np.log(1 - rho ** 2))) < 0.04
    assert abs(ksg_mi(x, rng.normal(size=3000))) < 0.03


def test_binned_mi_bias_on_independent_data():
    # Plug-in bias for independent variables is about (Bx - 1)(By - 1)/(2n) [Treves95, Paninski03].
    rng = np.random.default_rng(2); n, bins = 2000, 8
    est = np.mean([binned_mi(rng.normal(size=n), rng.normal(size=n), bins) for _ in range(30)])
    assert abs(est - (bins - 1) ** 2 / (2 * n)) < 0.004


def test_effective_sample_size_ar1():
    assert effective_sample_size_ar1(1000, 0.0) == 1000 and np.isclose(effective_sample_size_ar1(1000, 0.5), 1000 / 3)


def test_spearman_within_skips_small_and_constant_groups():
    g = np.repeat([0, 1, 2], [10, 3, 10]); x = np.arange(23.0); y = x.copy(); y[g == 2] = 1.0
    r = spearman_within(x, y, g)
    assert len(r) == 1 and np.isclose(r[0], 1.0)


def test_cluster_bootstrap_contains_the_mean():
    v = np.random.default_rng(3).normal(1.0, 1.0, 200)
    pt, lo, hi = cluster_bootstrap(len(v), lambda b: v[b].mean(), 400)
    assert lo < pt < hi and lo < 1.0 < hi and np.isclose(pt, v.mean())


def test_selection_differential_is_the_price_selection_term():
    rng = np.random.default_rng(4); w = rng.uniform(0.5, 2, 50); z = rng.normal(size=50)
    _, sel, _ = price_decomposition(w, z, z)
    assert np.isclose(selection_differential(w, z), sel)
    assert np.isclose(sel, np.cov(w, z, bias=True)[0, 1] / w.mean())


def test_mfpt_from_censoring():
    t = np.array([1.0, 2.0, 5.0, 5.0]); ev = np.array([True, True, False, False]); valid = np.array([True, True, True, False])
    V, n_ev, n_valid = mfpt_from(t, ev, valid)
    assert (V, n_ev, n_valid) == (8.0 / 2, 2, 3)


def test_bridge_crossing_probability_against_simulation():
    # Brownian bridge from d0 to d1 (distances from a flat boundary), variance s2 over the step.
    rng = np.random.default_rng(5); d0, d1, s2, n, m = 0.3, 0.5, 0.2, 20000, 400
    t = np.linspace(0, 1, m + 1)
    W = np.cumsum(np.concatenate([np.zeros((n, 1)), rng.normal(0, np.sqrt(s2 / m), (n, m))], 1), 1)
    path = d0 + (d1 - d0) * t + W - t * W[:, -1:]
    p_sim = np.mean(path.min(1) <= 0)
    # The m-step paths miss crossings between their points: the same discrete-monitoring effect, a shift of the boundary
    # by 0.5826 sqrt(s2/m) [BroadieGlassermanKou97]. With that shift the formula must match the simulation.
    dl = 0.5826 * np.sqrt(s2 / m)
    assert abs(p_sim - bridge_crossing_prob(d0 + dl, d1 + dl, s2)) < 0.01
    assert bridge_crossing_prob(d0, d1, s2) > p_sim                      # continuous paths cross more often


def test_blanket_estimates_and_edge_scores():
    rng = np.random.default_rng(6); w = make_planted_world("equilibrium", rng)
    S_hat, C_hat = estimates(sample(w["B"], w["S"], 20000, 0.5, rng))
    assert np.max(np.abs(S_hat - w["S"])) < 0.05
    g = static_graph(w["S"], 1e-8)[0]
    assert edge_scores(g, w["adj"]) == (1.0, 1.0, 1.0)
    assert edge_scores(np.zeros_like(g), w["adj"])[2] == 0.0


def test_unit_forces_and_drawn_parameters():
    rock = Unit("rock", dict(h=0.3)); x = np.array([-1.0, 0.0, 1.0]); v = np.zeros(3)
    assert np.allclose(rock.force(x, v), 0.0)                               # wells and barrier top are fixed points
    osc = Unit("oscillator", dict(omega0=1.0, alpha=2.0, beta=1.0, v0=1.0))
    assert np.isclose(osc.force(np.array([0.0]), np.array([1.0]))[0], 0.0)  # friction is zero at v = v0
    assert np.isclose(osc.force(np.array([0.0]), np.array([1.0]), on=False)[0], -GAMMA0)
    units = draw_units(np.random.default_rng(7))
    kinds = [u.kind for u in units]
    assert kinds.count("rock") == 60 and kinds.count("oscillator") == 60 and kinds.count("well") == 30
    assert all(1.5 * T <= u.p["h"] <= 4 * T for u in units if u.kind == "rock")
    assert all(1.0 <= u.p["v0"] <= 1.5 and np.isclose(u.p["beta"], (u.p["alpha"] - GAMMA0) / u.p["v0"] ** 2)
               for u in units if u.kind == "oscillator")
