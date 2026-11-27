"""Tests of semcontrols: the controls and the known answers. They need numpy, scipy and pytest only."""
import numpy as np
import pytest
from semcontrols import check, controls, scores
from semcontrols.linear import mutual_information


def test_organism_0_matches_s3():
    # The L value of organism 0 in variational_life results/e23_b4a_homeostat.json
    assert controls.homeostat(0).meta["L"] == pytest.approx(1.3577157550157608, abs=1e-15)


def test_homeostat_is_stationary():
    for i in range(20):
        for v in ("intact", "nofeedback"):
            s = controls.homeostat(i, v)
            assert np.linalg.eigvals(s.B).real.min() > 0
            assert np.allclose(s.B @ s.S + s.S @ s.B.T, 2 * s.D, atol=1e-12)


def test_kw_value_negative_without_feedback():
    # F6 of variational_life docs/C.md: Delta V_KW < 0 for every organism without feedback
    for i in range(50):
        assert scores.kw_value(controls.homeostat(i, "nofeedback")) < 0


def test_kw_stored_is_full_information_without_feedback():
    # F4 and F6 of docs/C.md: S_KW = I(A; h)
    for i in range(20):
        s = controls.homeostat(i, "nofeedback")
        assert scores.kw_stored(s) == pytest.approx(mutual_information(s.S, s.agent, s.env), rel=1e-9)


@pytest.mark.parametrize("tau", [0.5, 1.0, 5.0])
def test_reader_gives_zero(tau):
    # B1 of docs/B.md: if the environment does not act on the agent, V does not depend on the intervention
    for s in controls.readers(200):
        assert abs(scores.kw_value(s, tau)) < 1e-10
        assert scores.kw_stored(s, tau) < 1e-10


def test_reader_has_correlation():
    # The control is not trivial: the agent and the environment are correlated
    mi = [mutual_information(s.S, s.agent, s.env) for s in controls.readers(200)]
    assert min(mi) > 0


def test_units():
    us = controls.units()
    assert len(us) == 840
    for seed in range(2026, 2033):
        d = [u for u in us if u.seed == seed]
        assert sum(u.kind == "rock" for u in d) == 60 and sum(u.kind == "oscillator" for u in d) == 60
    assert all(scores.flux_ratio(u) == 0 for u in us if u.kind == "rock")
    assert all(scores.flux_ratio(u) > 0 for u in us if u.kind == "oscillator")


def test_rocks_order_reproduces_c2():
    # K1 of docs/C.md: the stratified AUC of the CLD chi_3 values, 0.711 [0.676, 0.748]
    r = check(unit_values={(u.seed, u.i): u.reference["cld_chi3"] for u in controls.units()})["rocks_order"]
    assert r["auc"] == pytest.approx(0.7111576859868282, abs=1e-9)
    assert r["ci"] == pytest.approx([0.6760929640551343, 0.7481136408279331], abs=1e-9)
    assert r["verdict"] == "fail"


def test_flux_ratio_passes_rocks_order():
    r = check(unit_score=scores.flux_ratio)["rocks_order"]
    assert r["verdict"] == "pass" and r["ci"][1] < 0.5


def test_check_on_kw_value():
    r = check(linear_score=scores.kw_value, homeostat_ids=range(40), n_readers=20, n_boot=200)
    assert r["homeostat_zero"]["verdict"] == "fail"
    assert r["reader_zero"]["verdict"] == "pass"
    assert set(r) == {"homeostat_zero", "homeostat_order", "reader_zero"}


def test_cld_unit_runs():
    u = [u for u in controls.units() if u.kind == "rock"][0]
    out = scores.cld_unit(u, n=500, n_times=3)
    assert np.isfinite(out["chi3"]) and np.isfinite(out["chi1"])


def test_cld_linear_positive_on_homeostat():
    omega, chi, se = scores.cld_linear(controls.homeostat(0, "nofeedback"), n=20_000)
    assert omega > 0 and chi[0] > 3 * se[0]
