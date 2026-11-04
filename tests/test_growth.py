import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import numpy as np
from vlife.viability import GrowthRateViability


def test_exponential_lives_give_r_equal_b_minus_mu():
    # S4: with exponential lives and a_m = 0, Euler-Lotka gives r = b - 1/V and R0 = b V.
    rng = np.random.default_rng(0); mu, t_max, dt = 0.5, 60.0, 0.01
    t = rng.exponential(1 / mu, 200000); ev = t < t_max; t = np.minimum(np.round(t / dt) * dt, t_max)
    g = GrowthRateViability(b=1.0, a_m=0.0)
    r, R0 = g.rate(t, ev, np.ones(len(t), bool), dt, t_max)
    assert abs(r - (1.0 - mu)) < 0.02 and abs(R0 - 1.0 / mu) < 0.05


def test_maturation_separates_equal_mean_lives():
    # Same mean life, but one curve loses many members early: with a maturation age, its r is lower.
    rng = np.random.default_rng(1); n, dt, t_max = 100000, 0.01, 200.0
    a = rng.exponential(4.0, n)                                    # exponential, mean 4
    b = np.where(rng.random(n) < 0.5, rng.exponential(0.5, n), rng.exponential(7.5, n))   # mixture, mean 4
    g = GrowthRateViability(b=1.0, a_m=2.0); ones = np.ones(n, bool)
    ra, _ = g.rate(np.round(a / dt) * dt, a < t_max, ones, dt, t_max); rb, _ = g.rate(np.round(b / dt) * dt, b < t_max, ones, dt, t_max)
    assert abs(a.mean() - b.mean()) < 0.1 and abs(ra - rb) > 0.02
