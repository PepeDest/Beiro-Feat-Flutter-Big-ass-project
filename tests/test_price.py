import numpy as np
from vlife.price import price_decomposition


def test_price_identity_exact():
    rng = np.random.default_rng(0)
    w = rng.uniform(0.1, 3, 50); z = rng.normal(size=50); zc = z + rng.normal(size=50) * 0.3
    lhs, sel, tr = price_decomposition(w, z, zc)
    assert np.isclose(lhs * w.mean(), np.cov(w, z, bias=True)[0, 1] + tr * w.mean())
    assert np.isclose(lhs, sel + tr)
