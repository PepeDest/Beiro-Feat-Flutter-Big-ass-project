"""Niche A, step A4 (docs/A.md): local oscillatory and nonnormal dissipation of a structure against its life change.

For each structure A (size 2-5) in the S1 driven and modular worlds:
  x_osc,A, x_nn,A = parts of oscillatory_nonnormal_ep(B_AA, D_AA) divided by tr(B_AA)/|A|   (local block: our choice)
  log R_A = log(V_on / V_eq), structures with >= 5 exits in both runs
Strata: world x size. Rules P1-P4 and the expectations are in docs/A.md (fixed before this script ran).
"""
import json, pathlib, pickle, sys
import numpy as np
from scipy.stats import spearmanr, rankdata

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vlife.gaussian import oscillatory_nonnormal_ep, structure_entropy_production  # noqa: E402

DATASETS = {"baseline": "e3_dataset_v2.pkl", "Dtest_r3": "e3_dataset_D3_v2.pkl"}
SIZES = (2, 3, 4, 5)


def strata(path):
    """List of worlds. Each world: dict size -> arrays (x_osc, x_nn, s_A, logR)."""
    worlds = []
    for w in pickle.load(open(path, "rb")):
        if w["family"] == "equilibrium":
            continue
        m_ok = (w["ev_on"] >= 5) & (w["ev_eq"] >= 5)
        per = {k: dict(x_osc=[], x_nn=[], s_A=[], logR=[]) for k in SIZES}
        for j, s in enumerate(w["subsets"]):
            if len(s) not in SIZES or not m_ok[j]:
                continue
            s = list(s)
            B, D = w["B"][np.ix_(s, s)], w["D"][np.ix_(s, s)]
            lam = np.trace(B) / len(s)
            _, so, sn = oscillatory_nonnormal_ep(B, D)
            p = per[len(s)]
            p["x_osc"].append(so / lam); p["x_nn"].append(sn / lam)
            p["s_A"].append(structure_entropy_production(w["B"], w["D"], w["S"], s) / lam)
            p["logR"].append(np.log(w["V_on"][j] / w["V_eq"][j]))
        worlds.append({k: {kk: np.array(vv) for kk, vv in v.items()} for k, v in per.items()})
    return worlds


def _rho(a, b):
    if len(a) < 5 or np.ptp(a) == 0 or np.ptp(b) == 0:
        return np.nan
    return spearmanr(a, b)[0]


def _zr(v):
    r = rankdata(v)
    return (r - r.mean()) / r.std() if r.std() > 0 else np.zeros_like(r)


def stats(worlds):
    r_osc, r_nn, r_sA = [], [], []
    by_size = {k: dict(osc=[], nn=[]) for k in SIZES}
    Y, X = [], []
    for w in worlds:
        for k in SIZES:
            p = w[k]
            if len(p["logR"]) < 5:
                continue
            a, b, c = _rho(p["x_osc"], p["logR"]), _rho(p["x_nn"], p["logR"]), _rho(p["s_A"], p["logR"])
            r_osc.append(a); r_nn.append(b); r_sA.append(c)
            by_size[k]["osc"].append(a); by_size[k]["nn"].append(b)
            Y.append(_zr(p["logR"])); X.append(np.column_stack([_zr(p["x_osc"]), _zr(p["x_nn"])]))
    bet = np.linalg.lstsq(np.vstack(X), np.concatenate(Y), rcond=None)[0]
    out = dict(P1=np.nanmean(r_osc), P2=np.nanmean(r_nn), b_osc=bet[0], b_nn=bet[1], P4=bet[1] - bet[0],
               sA=np.nanmean(r_sA))
    for k in SIZES:
        out[f"P1_size{k}"] = np.nanmean(by_size[k]["osc"]); out[f"P2_size{k}"] = np.nanmean(by_size[k]["nn"])
    return out


def life_label(ci):
    return "shortens life" if ci[1] < 0 else ("lengthens life" if ci[0] > 0 else "no effect")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    res = {}
    for name, fn in DATASETS.items():
        worlds = strata(ROOT / "results" / fn)
        point = stats(worlds)
        rng = np.random.default_rng(2026); boots = {k: [] for k in point}
        for _ in range(2000):
            st = stats([worlds[i] for i in rng.integers(0, len(worlds), len(worlds))])
            for k in st:
                boots[k].append(st[k])
        ci = {k: (float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5))) for k, v in boots.items()}
        res[name] = dict(n_worlds=len(worlds), point={k: float(v) for k, v in point.items()}, ci=ci,
                         P1=life_label(ci["P1"]), P2=life_label(ci["P2"]), P3_osc=life_label(ci["b_osc"]),
                         P3_nn=life_label(ci["b_nn"]),
                         P4="the parts differ" if (ci["P4"][0] > 0 or ci["P4"][1] < 0) else "not separated")
    out = ROOT / "results"
    json.dump(res, open(out / "e17_structure_level.json", "w"), indent=1)

    def cell(k, key, lab=None):
        p, c = res[k]["point"][key], res[k]["ci"][key]
        return f"{p:+.3f} [{c[0]:+.3f}, {c[1]:+.3f}]" + (f", {res[k][lab]}" if lab else "")
    L = ["# E17: local dissipation parts of a structure against its life change (niche A, step A4)", "",
         "Rules: docs/A.md. 95 % cluster-bootstrap intervals over worlds.", "",
         "| Rule | Statistic | baseline | D-test r = 3 |", "|---|---|---|---|",
         f"| P1 | mean ρ(x_osc,A, log R) | {cell('baseline', 'P1', 'P1')} | {cell('Dtest_r3', 'P1', 'P1')} |",
         f"| P2 | mean ρ(x_nn,A, log R) | {cell('baseline', 'P2', 'P2')} | {cell('Dtest_r3', 'P2', 'P2')} |",
         f"| P3 | β_osc | {cell('baseline', 'b_osc', 'P3_osc')} | {cell('Dtest_r3', 'b_osc', 'P3_osc')} |",
         f"| P3 | β_nn | {cell('baseline', 'b_nn', 'P3_nn')} | {cell('Dtest_r3', 'b_nn', 'P3_nn')} |",
         f"| P4 | β_nn − β_osc | {cell('baseline', 'P4', 'P4')} | {cell('Dtest_r3', 'P4', 'P4')} |",
         f"| description | mean ρ(σ_A / λ̄_A, log R), S2c measure | {cell('baseline', 'sA')} | {cell('Dtest_r3', 'sA')} |",
         "", "Per size (description only):", "", "| Size | P1 baseline | P2 baseline | P1 D-test | P2 D-test |",
         "|---|---|---|---|---|"]
    for k in SIZES:
        b, d = res["baseline"]["point"], res["Dtest_r3"]["point"]
        L.append(f"| {k} | {b[f'P1_size{k}']:+.3f} | {b[f'P2_size{k}']:+.3f} | {d[f'P1_size{k}']:+.3f} | {d[f'P2_size{k}']:+.3f} |")
    (out / "e17_structure_level.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
