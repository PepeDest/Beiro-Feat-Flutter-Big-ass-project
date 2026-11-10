import numpy as np
from vlife.growthlaw import growth_fits


def test_power_law_with_a_late_origin():
    # Fix #11 (docs/code_review.md): N = ((t - 800)/50)^2. With t0 = 0 the exponent is far from 2; with t0 fitted it is 2.
    t = np.arange(810, 6000, 10.0); N = np.maximum(np.round(((t - 800) / 50) ** 2), 1)
    g = growth_fits(t, N)
    assert abs(g["power_t0"] - 2) < 0.05 and abs(g["t0_fit"] - 800) < 60
    assert abs(g["power"] - 2) > 0.5
    assert g["R2_pow_t0"] >= g["R2_pow"]


def test_exponential_growth_is_recognised_and_small_colonies_are_skipped():
    t = np.arange(0, 20000, 10.0); N = np.round(4 * np.exp(t / 3000))
    g = growth_fits(t, N)
    assert g["R2_exp"] > g["R2_pow"] and abs(g["rate"] - 1 / 3000) < 1e-4
    assert growth_fits(t, np.minimum(N, 7)) is None                      # never reaches 8 spots


def test_same_fields_as_the_old_fit():
    # R2_exp, R2_pow and power keep the old definition (window N >= 8 to 0.3 N_max, t0 = 0).
    rng = np.random.default_rng(0); t = np.arange(10, 30000, 10.0); N = np.round(4 + (t / 900) ** 1.9 + rng.normal(0, 1, len(t)))
    g = growth_fits(t, N)
    i0 = np.argmax(N >= 8); i1 = np.argmax(N >= 0.3 * N.max()); tt, nn = t[i0:i1 + 1], np.log(N[i0:i1 + 1])
    assert np.isclose(g["power"], np.polyfit(np.log(tt), nn, 1)[0]) and g["N_window"] == [int(N[i0]), int(N[i1])]
