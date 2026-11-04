import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import numpy as np
from vlife.blankets import make_planted_world, static_graph, dynamic_graph, blanket_of
from vlife.gaussian import lagged_cov


def test_planted_blanket_is_the_neighbour_set():
    w = make_planted_world("equilibrium", np.random.default_rng(0))
    for I, Bl in w["orgs"]:
        assert blanket_of(w["adj"], I) == Bl


def test_exact_detectors():
    # Equilibrium: both detectors give the true graph. Driven: the dynamic detector gives the true graph.
    for fam in ("equilibrium", "driven"):
        w = make_planted_world(fam, np.random.default_rng(1))
        assert np.all(np.linalg.eigvals(w["B"]).real > 0)
        C = lagged_cov(w["B"], w["S"], 0.5)
        gd, _ = dynamic_graph(w["S"], C, 0.5, 1e-8)
        assert np.array_equal(gd, w["adj"])
        if fam == "equilibrium":
            gs, _ = static_graph(w["S"], 1e-8)
            assert np.array_equal(gs, w["adj"])
