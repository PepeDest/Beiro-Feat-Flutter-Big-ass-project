import numpy as np
from scipy.stats import chi2
from vlife.viability import simulate_exits, mfpt_all, mfpt_union


def bvp_mfpt_1d(theta, D, a, n=4001):
    """Backward equation  -theta x T' + D T'' = -1, T(+-a)=0  [Gardiner04 ch.5.2; Redner01]; finite differences."""
    x = np.linspace(-a, a, n); h = x[1] - x[0]
    A = np.zeros((n, n)); b = -np.ones(n)
    for i in range(1, n - 1):
        A[i, i - 1] = D / h ** 2 + theta * x[i] / (2 * h)
        A[i, i] = -2 * D / h ** 2
        A[i, i + 1] = D / h ** 2 - theta * x[i] / (2 * h)
    A[0, 0] = A[-1, -1] = 1; b[0] = b[-1] = 0
    return x, np.linalg.solve(A, b)


def test_mfpt_matches_backward_equation_1d():
    theta, D, p_out = 1.0, 1.0, 0.3
    S = np.array([[D / theta]]); B = np.array([[theta]])
    a = np.sqrt(chi2.ppf(1 - p_out, 1) * S[0, 0])
    dt = 0.01
    # discrete monitoring ~ boundary shifted OUTWARD by 0.5826*sqrt(2 D dt)  [BroadieGlassermanKou97]
    x, T = bvp_mfpt_1d(theta, D, a + 0.5826 * np.sqrt(2 * D * dt))
    p = np.exp(-x ** 2 * theta / (2 * D)); inside = np.abs(x) < a
    theory = (T * p)[inside].sum() / p[inside].sum()
    d = simulate_exits(B, S, [(0,)], p_out=p_out, n_traj=8000, dt=dt, t_max=80, rng=np.random.default_rng(0))
    V, ev, nv = mfpt_all(d)
    assert ev[0] == nv[0]                       # nothing censored
    assert abs(V[0] - theory) / theory < 0.05, (V[0], theory)


def test_independent_parts_hazards_add():
    # two independent OU variables: merged survival rate = sum of rates (so V_union ~ 1/(1/V_A+1/V_B))
    B = np.diag([1.0, 0.5]); S = np.diag([1.0, 2.0])
    d = simulate_exits(B, S, [(0,), (1,)], p_out=0.2, n_traj=8000, dt=0.02, t_max=100, rng=np.random.default_rng(1))
    V = mfpt_all(d)[0]; Vu = mfpt_union(d, 0, 1)[0]
    assert abs(Vu * (1 / V[0] + 1 / V[1]) - 1) < 0.08


def test_evaluate_returns_nan_for_censored_structures():
    # Fix #9 (docs/code_review.md): with (almost) no exits, V = exposure is a lower bound, so evaluate must not return it.
    from vlife.viability import MFPTViability, GrowthRateViability
    from vlife.worlds import make_world
    w = make_world("equilibrium", 3, np.random.default_rng(0)); subs = [(0,), (1,), (0, 1)]
    short = dict(n_traj=50, dt=0.05, t_max=0.05)           # one step: hardly any exits
    for m in (MFPTViability(**short), GrowthRateViability(**short)):
        assert np.all(np.isnan(m.evaluate(w, subs, np.random.default_rng(1))))
    V = MFPTViability(n_traj=200, dt=0.05, t_max=100.0).evaluate(w, subs, np.random.default_rng(1))
    assert np.all(np.isfinite(V)) and np.all(V > 0)
