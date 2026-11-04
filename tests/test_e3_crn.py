import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "experiments"))
import numpy as np


def _data(crn):
    from e3_phi_vs_viability import build_dataset
    return build_dataset(1, 1.0, 0.05, 80, 0.05, 6.0, 7, crn=crn)


def test_common_random_numbers_make_the_equilibrium_control_exact():
    # Fix #5 (docs/code_review.md): with crn, the equilibrium counterpart B_eq = D S^-1 equals B (to 1e-15) and uses the
    # same random numbers, so every exit time is the same and log R = 0 exactly.
    data = _data(True)
    eq = next(d for d in data if d["family"] == "equilibrium")
    assert np.allclose(eq["V_on"], eq["V_eq"], rtol=1e-12) and eq["crn"]
    dr = next(d for d in data if d["family"] == "driven")
    assert not np.allclose(dr["V_on"], dr["V_eq"])          # the driven counterpart differs


def test_without_crn_the_control_is_only_equal_in_distribution():
    eq = next(d for d in _data(False) if d["family"] == "equilibrium")
    assert not np.allclose(eq["V_on"], eq["V_eq"])          # old behaviour: separate random numbers


def test_bridge_option_is_recorded_and_shortens_life():
    # Fix #1: the bridge adds the exits missed between two checks, so V falls (by about 0.2-0.4 in log V at dt = 0.05).
    from e3_phi_vs_viability import build_dataset
    a = build_dataset(1, 1.0, 0.05, 200, 0.05, 30.0, 7, crn=True, bridge=False)
    b = build_dataset(1, 1.0, 0.05, 200, 0.05, 30.0, 7, crn=True, bridge=True)
    for x, y in zip(a, b):
        assert y["bridge"] and not x["bridge"]
        assert np.mean(np.log(y["V_on"]) - np.log(x["V_on"])) < -0.1
