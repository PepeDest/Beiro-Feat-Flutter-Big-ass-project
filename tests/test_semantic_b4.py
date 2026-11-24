import numpy as np
from vlife.gaussian import stationary_cov
from vlife.semantic import value_of_information, viability, syntactic_information
from vlife.semantic_apply import permute, viability_target, value_on, half_value_information, stored_semantic
from vlife.agency import draw_organism, homeostat


def _system(seed, n):
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(n, n))
    B = A @ A.T / n + 0.5 * np.eye(n) + 0.8 * (A - A.T) / 2
    D = np.diag(rng.uniform(0.3, 1.5, n))
    return B, D, stationary_cov(B, D)


def test_value_on_matches_semantic_py_after_a_permutation():
    B, D, S = _system(921, 5)
    agent, env = [3, 1], [0, 2, 4]
    Bp, Dp, Sp = permute(B, D, S, agent, env)
    assert np.isclose(value_on(B, D, S, agent, env, 1.0), value_of_information(Bp, Dp, Sp, 2, 1.0))
    assert np.isclose(viability_target(Bp, Dp, Sp, 2, np.eye(3), 1.0, [0, 1]), viability(Bp, Dp, Sp, 2, np.eye(3), 1.0))


def test_half_value_point_of_the_homeostat():
    o = draw_organism(np.random.default_rng(5))
    B, D, S = homeostat(o, "intact")
    agent, env = [1, 2, 3, 4], [0]
    p, R, I_act = half_value_information(B, D, S, agent, env, 1.0, 3)
    Bp, Dp, Sp = permute(B, D, S, agent, env)
    V = lambda q: viability_target(Bp, Dp, Sp, 4, np.array([[q]]), 1.0, [3])
    assert 0 < p < 1 and np.isclose(V(p), (V(0) + V(1)) / 2)
    assert 0 < R < I_act


def test_scalar_environment_root_search():
    """dy = 1: the result is I at a point with V = V_act, and a fine grid finds no such point with less I."""
    B, D, S = _system(922, 4)
    agent, env = [0, 1, 2], [3]
    S_G, method = stored_semantic(B, D, S, agent, env, 1.0)
    Bp, Dp, Sp = permute(B, D, S, agent, env)
    V = lambda q: viability_target(Bp, Dp, Sp, 3, np.array([[q]]), 1.0, range(3))
    I = lambda q: syntactic_information(Sp, 3, np.array([[q]]))
    ps = np.linspace(0, 1, 20001)
    g = np.array([V(q) for q in ps]) - V(1.0)
    cross = [ps[i] for i in range(len(ps) - 1) if np.sign(g[i]) != np.sign(g[i + 1]) and ps[i + 1] < 1]
    expect = I(cross[0]) if cross else I(1.0)
    assert np.isclose(S_G, expect, atol=1e-4) and S_G <= I(1.0) + 1e-12


def test_scalar_agent_uses_the_drive_information():
    B, D, S = _system(923, 4)
    S_G, method = stored_semantic(B, D, S, [2], [0, 1, 3], 1.0)
    assert method.startswith("drive") and S_G >= 0
