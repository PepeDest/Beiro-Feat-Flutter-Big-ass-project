import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import numpy as np
from scipy.stats import chi2
from vlife.agency import Organism, draw_organism, homeostat, simulate_exit_threshold, H, U, V
from vlife.gaussian import mutual_information
from vlife.viability import simulate_exits, mfpt_all


def test_all_versions_stable_and_stationary():
    rng = np.random.default_rng(0)
    for _ in range(20):
        o = draw_organism(rng)
        for ver in ("intact", "scrambled", "nofeedback"):
            B, D, S = homeostat(o, ver)
            assert np.all(np.linalg.eigvals(B).real > 0)
            assert np.allclose(B @ S + S @ B.T, 2 * D)


def test_scramble_keeps_actuator_statistics_and_removes_information():
    o = draw_organism(np.random.default_rng(1))
    _, _, Si = homeostat(o, "intact"); _, _, Ss = homeostat(o, "scrambled"); _, _, Sn = homeostat(o, "nofeedback")
    assert np.isclose(Si[U, U], Ss[U, U])                      # same input statistics for the actuator
    assert mutual_information(Si, [U], [H]) > 1e-3             # intact actuator knows about h
    assert abs(mutual_information(Ss, [U], [H])) < 1e-10        # scrambled actuator does not
    assert abs(mutual_information(Sn, [U], [H])) < 1e-10


def test_good_regulator_reduces_variance_of_v():
    o = Organism(T_h=10, sigma_s=0.1, k_s=5, k_m=5, k_u=5, k_v=0.3, L=1.0)
    var = {ver: homeostat(o, ver)[2][V, V] for ver in ("intact", "nofeedback", "scrambled")}
    assert var["intact"] < 0.2 * var["nofeedback"] and var["nofeedback"] < var["scrambled"]


def test_threshold_simulator_matches_mahalanobis_simulator_in_1d():
    B = np.array([[0.7]]); S = np.array([[1 / 0.7]])
    ck = chi2.ppf(0.9, 1); c = np.sqrt(ck * S[0, 0])
    Va, ea, _ = simulate_exit_threshold(B, S, 0, c, n_traj=300, t_max=50, rng=np.random.default_rng(5))
    Vb, eb, _ = mfpt_all(simulate_exits(B, S, [(0,)], p_out=0.1, n_traj=300, t_max=50, rng=np.random.default_rng(5)))
    assert ea == eb[0] and np.isclose(Va, Vb[0])
