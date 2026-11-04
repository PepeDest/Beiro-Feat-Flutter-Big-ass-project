"""S2 - nonlinear inertial units for the flux-cut test (docs/S2.md).

State z = (x, v).  dx = v dt,  dv = (-U'(x) - gamma(v) v) dt + sqrt(2 gamma0 T) dW.
 rock:        U = h (x^2 - 1)^2,       gamma = gamma0 (on and off)
 oscillator:  U = omega0^2 x^2 / 2,    gamma_on = gamma0 - alpha + beta v^2 (active Rayleigh friction,
              energy-depot model [SchweitzerEbelingTilch98, Romanczuk12]),  gamma_off = gamma0
 well:        U = k x^2 / 2,           gamma = gamma0 (control)
Off dynamics has constant friction and noise 2 gamma0 T, so it relaxes to the Boltzmann law [Kramers40].
Integrator: Euler-Maruyama (velocity first, then position with the new velocity)."""
from dataclasses import dataclass, field
import numpy as np

GAMMA0, T = 1.0, 0.1


@dataclass
class Unit:
    kind: str
    p: dict = field(default_factory=dict)

    def force(self, x, v, on=True):
        p = self.p
        if self.kind == "rock":
            du = 4 * p["h"] * x * (x * x - 1)
        elif self.kind == "oscillator":
            du = p["omega0"] ** 2 * x
        else:
            du = p["k"] * x
        g = GAMMA0 - p["alpha"] + p["beta"] * v * v if (self.kind == "oscillator" and on) else GAMMA0
        return -du - g * v

    def drive_power(self, v):
        """Mean power of the active part of the friction, (alpha - beta v^2) v^2. Zero for passive units."""
        if self.kind != "oscillator":
            return 0.0
        return float(np.mean((self.p["alpha"] - self.p["beta"] * v * v) * v * v))


def draw_units(rng, n_rock=60, n_osc=60, n_well=30):
    lu = lambda lo, hi: float(np.exp(rng.uniform(np.log(lo), np.log(hi))))
    units = [Unit("rock", dict(h=T * lu(1.5, 4))) for _ in range(n_rock)]
    for _ in range(n_osc):
        a, v0 = float(rng.uniform(1.5, 3)), float(rng.uniform(1.0, 1.5))   # v0 range changed after the pilot (docs/S2.md)
        units.append(Unit("oscillator", dict(omega0=lu(0.5, 2), alpha=a, beta=(a - GAMMA0) / v0 ** 2, v0=v0)))
    units += [Unit("well", dict(k=lu(0.5, 2))) for _ in range(n_well)]
    return units


def step(u, x, v, on, dt, rng):
    v = v + u.force(x, v, on) * dt + np.sqrt(2 * GAMMA0 * T * dt) * rng.normal(size=x.shape)
    return x + v * dt, v


def run(u, x, v, t, on, dt, rng):
    for _ in range(int(round(t / dt))):
        x, v = step(u, x, v, on, dt, rng)
    return x, v


def initial(u, n, rng):
    if u.kind == "rock":
        x = rng.choice([-1.0, 1.0], n) + 0.1 * rng.normal(size=n); v = np.sqrt(T) * rng.normal(size=n)
    elif u.kind == "oscillator":
        ph = rng.uniform(0, 2 * np.pi, n); v0 = u.p["v0"]
        x = v0 / u.p["omega0"] * np.cos(ph); v = v0 * np.sin(ph)
    else:
        x = np.sqrt(T / u.p["k"]) * rng.normal(size=n); v = np.sqrt(T) * rng.normal(size=n)
    return x, v


class HDR:
    """Highest-density region holding (1 - p_out) of the mass of the samples (2D histogram)."""

    def __init__(self, x, v, p_out=0.05, bins=40, smooth=1.0):
        from scipy.ndimage import gaussian_filter
        pad = lambda a: (a.min() - 0.05 * np.ptp(a), a.max() + 0.05 * np.ptp(a))
        H, self.ex, self.ev = np.histogram2d(x, v, bins=bins, range=[pad(x), pad(v)])
        H = gaussian_filter(H, smooth, mode="constant")    # light smoothing: a raw histogram fits the noise (S2 design change)
        d = np.sort(H.ravel())[::-1]; cum = np.cumsum(d) / d.sum()
        self.q = d[np.searchsorted(cum, 1 - p_out)]
        self.mask = H >= self.q

    def inside(self, x, v):
        i = np.searchsorted(self.ex, x, side="right") - 1; j = np.searchsorted(self.ev, v, side="right") - 1
        ok = (i >= 0) & (i < self.mask.shape[0]) & (j >= 0) & (j < self.mask.shape[1])
        out = np.zeros(x.shape, bool)
        out[ok] = self.mask[i[ok], j[ok]]
        return out


def exit_times(u, x, v, hdr, on, dt=0.01, t_max=500.0, rng=None):
    """Mean exit time from the HDR set, started from (x, v) points; V = exposure / exits [CoxOakes84]."""
    rng = np.random.default_rng() if rng is None else rng
    valid = hdr.inside(x, v); alive = valid.copy()
    t_exit = np.full(x.shape, float(t_max)); event = np.zeros(x.shape, bool)
    for s in range(1, int(round(t_max / dt)) + 1):
        if not alive.any():
            break
        x, v = step(u, x, v, on, dt, rng)
        out = alive & ~hdr.inside(x, v)
        t_exit[out] = s * dt; event |= out; alive &= ~out
    ev = int(event[valid].sum())
    return float(t_exit[valid].sum()) / max(ev, 1), ev, int(valid.sum())


# ---------------------------------------------------------------- S2b: viability sets that measure memory (docs/S2.md)
def alive_rule(u, x, v, E_cyc=None):
    """Return (valid, alive_fn). Rock: stays in the well it starts in (dies at the other well's core, |x| > 0.5).
    Oscillator: stays on its cycle (dies when E = v^2/2 + omega0^2 x^2/2 < 0.25 E_cyc)."""
    if u.kind == "rock":
        s = np.sign(x); valid = np.abs(x) > 0.5
        return valid, (lambda x, v: s * x > -0.5)
    if u.kind == "oscillator":
        en = lambda x, v: 0.5 * v * v + 0.5 * u.p["omega0"] ** 2 * x * x
        return en(x, v) > 0.25 * E_cyc, (lambda x, v: en(x, v) > 0.25 * E_cyc)
    raise ValueError("S2b uses rocks and oscillators only")


def exit_times_rule(u, x, v, valid, alive_fn, on, dt=0.01, t_max=3000.0, rng=None):
    """Mean exit time for a general alive rule; V = exposure / exits [CoxOakes84]."""
    rng = np.random.default_rng() if rng is None else rng
    alive = valid.copy(); t_exit = np.full(x.shape, float(t_max)); event = np.zeros(x.shape, bool)
    for s in range(1, int(round(t_max / dt)) + 1):
        if not alive.any():
            break
        x, v = step(u, x, v, on, dt, rng)
        out = alive & ~alive_fn(x, v)
        t_exit[out] = s * dt; event |= out; alive &= ~out
    ev = int(event[valid].sum())
    return float(t_exit[valid].sum()) / max(ev, 1), ev, int(valid.sum())
