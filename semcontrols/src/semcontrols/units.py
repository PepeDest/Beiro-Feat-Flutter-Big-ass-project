"""The nonlinear S2 units: rocks (a double well, passive) and oscillators (active Rayleigh friction, driven).

State (x, v). dx = v dt, dv = (-U'(x) - gamma(v) v) dt + sqrt(2 gamma0 T) dW, gamma0 = 1, T = 0.1.
- rock: U = h (x^2 - 1)^2, gamma = gamma0.
- oscillator: U = omega0^2 x^2 / 2, gamma = gamma0 - alpha + beta v^2 (on). Off: gamma = gamma0.
Euler-Maruyama, velocity first, then position with the new velocity.
"""
from dataclasses import dataclass, field
import numpy as np

GAMMA0, T = 1.0, 0.1


@dataclass
class Unit:
    kind: str
    p: dict
    seed: int = 0
    i: int = 0
    V_on: float = None
    V_off: float = None
    tau_star: float = None
    E_cyc: float = None
    reference: dict = field(default_factory=dict)

    @property
    def uses_information(self):
        return False

    def force(self, x, v, on=True):
        p = self.p
        du = 4 * p["h"] * x * (x * x - 1) if self.kind == "rock" else p["omega0"] ** 2 * x
        g = GAMMA0 - p["alpha"] + p["beta"] * v * v if (self.kind == "oscillator" and on) else GAMMA0
        return -du - g * v


def step(u, x, v, on, dt, rng):
    v = v + u.force(x, v, on) * dt + np.sqrt(2 * GAMMA0 * T * dt) * rng.normal(size=x.shape)
    return x + v * dt, v


def run(u, x, v, t, on, dt, rng):
    for _ in range(int(round(t / dt))):
        x, v = step(u, x, v, on, dt, rng)
    return x, v


def initial(u, n, rng):
    """The start law of S2 (before the burn-in)."""
    if u.kind == "rock":
        x = rng.choice([-1.0, 1.0], n) + 0.1 * rng.normal(size=n); v = np.sqrt(T) * rng.normal(size=n)
    else:
        ph = rng.uniform(0, 2 * np.pi, n); v0 = u.p["v0"]
        x = v0 / u.p["omega0"] * np.cos(ph); v = v0 * np.sin(ph)
    return x, v
