"""The three controls of semcontrols, with their known answers (README.md, and docs/I.md of variational_life)."""
import json
from importlib import resources
import numpy as np
from .linear import LinearSystem
from .units import Unit

H, S_, M, U, V = 0, 1, 2, 3, 4


def _organism(i, seed=2026):
    """The S3 organism i: the same draws, in the same order, as vlife.agency.draw_organism(default_rng([seed, i]))."""
    rng = np.random.default_rng([seed, i])
    lu = lambda lo, hi: float(np.exp(rng.uniform(np.log(lo), np.log(hi))))
    return dict(T_h=lu(2, 20), sigma_s=lu(0.1, 3), k_s=lu(0.5, 5), k_m=lu(0.5, 5), k_u=lu(0.5, 5),
                k_v=lu(0.2, 1), L=float(rng.uniform(0, 1.5)))


def homeostat(i, version="intact", seed=2026):
    """S3 homeostat i (docs/S3.md). z = (h, s, m, u, v): environment h, agent (s, m, u, v), target v.
    version 'intact' or 'nofeedback' (loop gain L = 0). Known answer: the organism without feedback uses no
    information (its actuator reads nothing)."""
    o = _organism(i, seed)
    B = np.zeros((5, 5)); d = np.zeros(5)
    B[H, H] = 1 / o["T_h"]; d[H] = 1 / o["T_h"]
    B[S_, S_] = o["k_s"]; B[S_, H] = -o["k_s"]; d[S_] = o["sigma_s"] ** 2 * o["k_s"]
    B[M, M] = o["k_m"]; B[M, S_] = -o["k_m"]; d[M] = 0.01
    L = 0.0 if version == "nofeedback" else o["L"]
    B[U, U] = o["k_u"]; B[U, M] = o["k_u"] * L; d[U] = 0.01
    B[V, V] = o["k_v"]; B[V, H] = -1.0; B[V, U] = -1.0; d[V] = 0.05 * o["k_v"]
    return LinearSystem(name=f"homeostat {i} {version}", B=B, D=np.diag(d), agent=[S_, M, U, V], env=[H], target=[V],
                        uses_information=(version == "intact" and L > 0), meta=dict(i=i, version=version, **o))


def homeostat_pairs(ids=range(400), seed=2026):
    """[(intact, nofeedback)] for the organisms `ids`."""
    return [(homeostat(i, "intact", seed), homeostat(i, "nofeedback", seed)) for i in ids]


def reader(j, seed=8500):
    """A linear system in which the environment reads the agent and does not act on it (B_xy = 0, B_yx != 0).
    z = (x_1..x_dx, y), dx in {1, 2, 3}, dy = 1, target = the whole agent. Known answer: the agent cannot use
    information about y, so a score of use must give 0."""
    rng = np.random.default_rng([seed, j])
    lu = lambda lo, hi: float(np.exp(rng.uniform(np.log(lo), np.log(hi))))
    dx = int(rng.integers(1, 4))
    n = dx + 1
    while True:
        B = np.zeros((n, n))
        k = [lu(0.3, 5) for _ in range(dx)]
        for a in range(dx):
            B[a, a] = k[a]
            for b in range(dx):
                if b != a and rng.uniform() < 0.5:
                    B[a, b] = 0.5 * np.sqrt(k[a] * k[b]) * rng.normal()
        if np.linalg.eigvals(B[:dx, :dx]).real.min() >= 0.01:
            break
    B[dx, dx] = 1 / lu(1, 20)
    B[dx, :dx] = rng.normal(size=dx)
    d = np.array([lu(0.01, 1) for _ in range(n)])
    return LinearSystem(name=f"reader {j}", B=B, D=np.diag(d), agent=list(range(dx)), env=[dx],
                        target=list(range(dx)), uses_information=False, meta=dict(j=j, dx=dx))


def readers(n=200, seed=8500):
    return [reader(j, seed) for j in range(n)]


def units():
    """The 840 S2b units (7 draws, seeds 2026-2032, 60 rocks and 60 oscillators each), with V_on, V_off, tau* and the
    CLD values of docs/C.md (C2) in `reference`. Known answer: no unit uses information about an environment."""
    raw = json.loads(resources.files("semcontrols").joinpath("data/units.json").read_text())
    out = []
    for r in raw["units"]:
        out.append(Unit(kind=r["kind"], p=r["p"], seed=r["seed"], i=r["i"], V_on=r["V_on"], V_off=r["V_off"],
                        tau_star=r["tau_star"], E_cyc=r["E_cyc"],
                        reference=dict(cld_chi3=r["cld_chi3"], cld_chi1=r["cld_chi1"])))
    return out
