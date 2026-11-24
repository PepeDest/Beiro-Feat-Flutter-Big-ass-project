"""Niche B, B2, post-hoc check (not a rule, docs/B.md): is S_proj of E21 the true minimum over projections?
Dense grid on the sphere for P = u u^T and P = I - v v^T, the level curve V(P) = V(I) found by sign changes along
the polar angle and refined by bisection. Systems: the five largest gaps S_proj - S_G of E21."""
import json, pathlib, sys
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "experiments"))
from e21_b2_semantic import system, TAU  # noqa: E402
from vlife.semantic import viability, syntactic_information  # noqa: E402

def unit(a, b):
    return np.array([np.cos(a) * np.sin(b), np.sin(a) * np.sin(b), np.cos(b)])

d = json.load(open(ROOT / "results" / "e21_b2_semantic.json"))
rows = sorted([r for r in d["b2a"] if not r.get("skipped")], key=lambda r: r["gap1"], reverse=True)[:5]
for r in rows:
    B, D, S = system(r["seed"], 2, 3); Va = viability(B, D, S, 2, np.eye(3), TAU)
    best = np.inf
    for kind in ("rank1", "corank1"):
        P_of = (lambda u: np.outer(u, u)) if kind == "rank1" else (lambda u: np.eye(3) - np.outer(u, u))
        g = lambda a, b: viability(B, D, S, 2, P_of(unit(a, b)), TAU) - Va
        for a in np.linspace(0, np.pi, 361):
            bs = np.linspace(0, np.pi, 181); gv = np.array([g(a, b) for b in bs])
            for i in np.flatnonzero(np.sign(gv[:-1]) != np.sign(gv[1:])):
                lo, hi = bs[i], bs[i + 1]
                for _ in range(40):
                    mid = (lo + hi) / 2
                    lo, hi = (mid, hi) if np.sign(g(a, mid)) == np.sign(gv[i]) else (lo, mid)
                best = min(best, syntactic_information(S, 2, P_of(unit(a, (lo + hi) / 2))))
    best = min(best, r["I_act"], r["I_C"])
    print(f"seed {r['seed']}: S_proj (E21) {r['S_proj']:.4f}, grid {best:.4f}, S_G {r['S_general']:.4f}")
