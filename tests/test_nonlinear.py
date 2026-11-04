import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import numpy as np
from vlife.nonlinear import Unit, initial, run, HDR, exit_times, T


def test_off_dynamics_reaches_equilibrium_temperature():
    # Fluctuation-dissipation: with the drive off, <v^2> = T (docs/S2.md).
    u = Unit("oscillator", dict(omega0=1.0, alpha=2.0, beta=1.0, v0=1.0))
    rng = np.random.default_rng(0); x, v = initial(u, 3000, rng)
    x, v = run(u, x, v, 40.0, False, 0.01, rng)
    assert abs(np.mean(v * v) / T - 1) < 0.1


def test_active_oscillator_keeps_its_cycle():
    u = Unit("oscillator", dict(omega0=1.0, alpha=2.0, beta=1.0, v0=1.0))
    rng = np.random.default_rng(1); x, v = initial(u, 2000, rng)
    x, v = run(u, x, v, 40.0, True, 0.01, rng)
    assert np.mean(v * v) > 3 * T          # a cycle: <v^2> well above the equilibrium value T


def test_hdr_holds_95_percent_and_rock_ratio_is_one():
    u = Unit("rock", dict(h=0.25))
    rng = np.random.default_rng(2); x, v = initial(u, 20000, rng); x, v = run(u, x, v, 30.0, True, 0.01, rng)
    hdr = HDR(x[:16000], v[:16000])
    assert abs(hdr.inside(x[16000:], v[16000:]).mean() - 0.95) < 0.02
    a = exit_times(u, x[16000:16500], v[16000:16500], hdr, True, t_max=20, rng=np.random.default_rng(9))
    b = exit_times(u, x[16000:16500], v[16000:16500], hdr, False, t_max=20, rng=np.random.default_rng(9))
    assert a == b


def test_s2b_rules():
    # Rock: a deeper well gives a longer well-switch time. Oscillator: the cycle rule holds most on-stationary points.
    from vlife.nonlinear import alive_rule, exit_times_rule
    Vs = []
    for h in (0.15, 0.25):
        u = Unit("rock", dict(h=h)); rng = np.random.default_rng(4); x, v = initial(u, 600, rng); x, v = run(u, x, v, 20.0, True, 0.01, rng)
        valid, fn = alive_rule(u, x, v)
        Vs.append(exit_times_rule(u, x, v, valid, fn, True, t_max=400, rng=np.random.default_rng(5))[0])
    assert Vs[1] > Vs[0]
    u = Unit("oscillator", dict(omega0=1.0, alpha=2.0, beta=1.0, v0=1.2)); rng = np.random.default_rng(6)
    x, v = initial(u, 2000, rng); x, v = run(u, x, v, 40.0, True, 0.01, rng)
    E = 0.5 * v * v + 0.5 * x * x; valid, fn = alive_rule(u, x, v, np.median(E))
    assert valid.mean() > 0.9 and fn(x, v).mean() == valid.mean()


def test_energy_balance_heat_equals_drive_power():
    # S2c: in steady state, heat into the bath gamma0 (<v^2> - T) equals the drive power <(alpha - beta v^2) v^2>.
    from vlife.nonlinear import GAMMA0
    u = Unit("oscillator", dict(omega0=1.0, alpha=2.0, beta=1.0, v0=1.0))
    rng = np.random.default_rng(7); x, v = initial(u, 20000, rng); x, v = run(u, x, v, 60.0, True, 0.005, rng)
    heat = GAMMA0 * (np.mean(v * v) - T)
    assert abs(heat - u.drive_power(v)) < 0.05 * abs(heat)
