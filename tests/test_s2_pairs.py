import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "experiments"))
import numpy as np


def test_extra_pairs_leave_the_exit_times_unchanged(monkeypatch):
    # Phase D (docs/RERUN.md): more pairs for C and TC come from their own random numbers, so the viability set,
    # the start points and V are the same as with the old number of pairs.
    import e6_fluxcut as e6
    for k, v in dict(N_HDR=400, N_START=100, N_PAIR=200, T_BURN=2.0).items():
        monkeypatch.setattr(e6, k, v)
    p = dict(omega0=1.0, alpha=2.0, beta=1.0 / 1.2 ** 2, v0=1.2)
    a = e6.run_unit((0, "oscillator", p, 7, 3.0))
    b = e6.run_unit((0, "oscillator", p, 7, 3.0, 800))
    assert (a["V_on"], a["V_off"], a["ev_on"]) == (b["V_on"], b["V_off"], b["ev_on"])
    assert a["C"] != b["C"]


def test_e6b_extra_pairs(monkeypatch):
    import e6b_rockmemory as e6b
    for k, v in dict(N_PAIR=200, T_BURN=2.0).items():
        monkeypatch.setattr(e6b, k, v)
    p = dict(h=0.3)
    a = e6b.job_C((1, "rock", p, 7, 1.0, 1.0)); b = e6b.job_C((1, "rock", p, 7, 1.0, 1.0, 600))
    assert np.isfinite(a["C_star"]) and np.isfinite(b["C_star"]) and a["C_star"] != b["C_star"]
