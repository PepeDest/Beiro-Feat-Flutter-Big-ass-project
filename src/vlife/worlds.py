"""Random OU worlds (the 'microscopic ensemble').  Three families.

All have D = I (unit temperature, unit mobility) and drift matrix B = Bs + G with
  Bs  symmetric positive definite  (conservative / relaxational part)
  G   antisymmetric                (non-reciprocal, non-conservative part; the 'flux')
Because x^T B x = x^T Bs x > 0, every such B is stable. [Lyapunov stability of the symmetric part;
the same decomposition is used in LelievreNierPavliotis13.]
Family design is ours (docs/PROVENANCE.md: 'ensemble design').
"""
from dataclasses import dataclass, field
import numpy as np
from .gaussian import stationary_cov, equilibrium_counterpart

FAMILIES = ("equilibrium", "driven", "modular_driven")


@dataclass
class World:
    B: np.ndarray
    D: np.ndarray
    S: np.ndarray
    family: str
    params: dict = field(default_factory=dict)

    @property
    def N(self):
        return self.B.shape[0]

    def B_eq(self):
        return equilibrium_counterpart(self.D, self.S)


def _random_spd(n, rng, rate_range=(0.3, 3.0)):
    Q, _ = np.linalg.qr(rng.normal(size=(n, n)))
    rates = np.exp(rng.uniform(np.log(rate_range[0]), np.log(rate_range[1]), n))
    return (Q * rates) @ Q.T


def _random_antisym(n, rng, scale):
    M = rng.normal(size=(n, n))
    return scale * (M - M.T) / 2.0


def make_world(family, N=6, rng=None, flux=None, noise_range=None):
    """noise_range=r (S1 D-test, docs/S1.md): D = diag(d), d_i log-uniform in [1/r, r], drawn AFTER B_s and G
    (so the same seed gives the same B_s and G as with D = I), and B = D (B_s + G). G = 0 keeps detailed balance."""
    rng = np.random.default_rng() if rng is None else rng
    if family not in FAMILIES:
        raise ValueError(family)
    D = np.eye(N)
    params = {}
    if family == "modular_driven":
        # Block sizes: N = 6 is the original design. N = 5 and N = 7 were added for the S1 sweep (docs/S1.md).
        sizes = {5: [3, 2], 6: [3, 2, 1], 7: [3, 2, 2]}.get(N, [N])
        Bs = np.zeros((N, N)); i = 0
        for s in sizes:
            Bs[i:i + s, i:i + s] = _random_spd(s, rng); i += s
        off = rng.normal(size=(N, N)); off = 0.1 * (off + off.T) / 2
        mask = np.ones((N, N), bool); i = 0
        for s in sizes:
            mask[i:i + s, i:i + s] = False; i += s
        Bs = Bs + off * mask
        w = np.linalg.eigvalsh(Bs).min()
        if w < 0.05:
            Bs += (0.05 - w) * np.eye(N)
        params["blocks"] = sizes
    else:
        Bs = _random_spd(N, rng)
    if family == "equilibrium":
        G = np.zeros((N, N)); f = 0.0
    else:
        f = float(rng.uniform(1.0, 3.0)) if flux is None else float(flux)
        G = _random_antisym(N, rng, f)
    params["flux_scale"] = f
    B = Bs + G
    if noise_range is not None:
        d = np.exp(rng.uniform(-np.log(noise_range), np.log(noise_range), N))
        D = np.diag(d); B = D @ B; params["noise_range"] = float(noise_range)
    return World(B=B, D=D, S=stationary_cov(B, D), family=family, params=params)
