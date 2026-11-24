"""Niche A, step A5 part 2 (docs/A.md): the oscillation that crosses the boundary of a structure, on the S1 data.

For each structure A (size 2-5) in the S1 driven and modular worlds:
  x_cross,A = cross_oscillation(B, S, A) / lambda_A,   x_osc,A = local part of A4 / lambda_A,   lambda_A = tr(B_AA)/|A|
  log R_A = log(V_on / V_eq), structures with >= 5 exits in both runs
Strata: world x size. Rules T1-T2 and the expectations are in docs/A.md (fixed before this script ran).
"""
import json, pathlib, pickle, sys
import numpy as np
from scipy.stats import spearmanr, rankdata

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vlife.gaussian import cross_oscillation, oscillatory_nonnormal_ep  # noqa: E402

DATASETS = {"baseline": "e3_dataset_v2.pkl", "Dtest_r3": "e3_dataset_D3_v2.pkl"}
SIZES = (2, 3, 4, 5)


def strata(path):
    worlds = []
    for w in pickle.load(open(path, "rb")):
        if w["family"] == "equilibrium":
            continue
        ok = (w["ev_on"] >= 5) & (w["ev_eq"] >= 5)
        per = {k: dict(x_cross=[], x_osc=[], logR=[]) for k in SIZES}
        for j, s in enumerate(w["subsets"]):
            if len(s) not in SIZES or not ok[j]:
                continue
            s = list(s)
            lam = np.trace(w["B"][np.ix_(s, s)]) / len(s)
            p = per[len(s)]
            p["x_cross"].append(cross_oscillation(w["B"], w["S"], s) / lam)
            p["x_osc"].append(oscillatory_nonnormal_ep(w["B"][np.ix_(s, s)], w["D"][np.ix_(s, s)])[1] / lam)
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
    rc, Y, X = [], [], []
    by_size = {k: [] for k in SIZES}
    for w in worlds:
        for k in SIZES:
            p = w[k]
            if len(p["logR"]) < 5:
                continue
            a = _rho(p["x_cross"], p["logR"]); rc.append(a); by_size[k].append(a)
            Y.append(_zr(p["logR"])); X.append(np.column_stack([_zr(p["x_cross"]), _zr(p["x_osc"])]))
    bet = np.linalg.lstsq(np.vstack(X), np.concatenate(Y), rcond=None)[0]
    out = dict(T1=np.nanmean(rc), b_cross=bet[0], b_osc=bet[1])
    for k in SIZES:
        out[f"T1_size{k}"] = np.nanmean(by_size[k])
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
                         T1=life_label(ci["T1"]), T2=life_label(ci["b_cross"]), T2_osc=life_label(ci["b_osc"]))
    out = ROOT / "results"
    json.dump(res, open(out / "e19_cross_oscillation_s1.json", "w"), indent=1)

    def cell(k, key, lab=None):
        p, c = res[k]["point"][key], res[k]["ci"][key]
        return f"{p:+.3f} [{c[0]:+.3f}, {c[1]:+.3f}]" + (f", {res[k][lab]}" if lab else "")
    L = ["# E19: oscillation across the boundary of a structure, S1 data (niche A, step A5, part 2)", "",
         "Rules: docs/A.md. 95 % cluster-bootstrap intervals over worlds.", "",
         "| Rule | Statistic | baseline | D-test r = 3 |", "|---|---|---|---|",
         f"| T1 | mean ρ(x_cross,A, log R) | {cell('baseline', 'T1', 'T1')} | {cell('Dtest_r3', 'T1', 'T1')} |",
         f"| T2 | β_cross (with x_osc,A) | {cell('baseline', 'b_cross', 'T2')} | {cell('Dtest_r3', 'b_cross', 'T2')} |",
         f"| description | β_osc,A (with x_cross,A) | {cell('baseline', 'b_osc', 'T2_osc')} | {cell('Dtest_r3', 'b_osc', 'T2_osc')} |",
         "", "Per size (description only):", "", "| Size | T1 baseline | T1 D-test |", "|---|---|---|"]
    for k in SIZES:
        L.append(f"| {k} | {res['baseline']['point'][f'T1_size{k}']:+.3f} | {res['Dtest_r3']['point'][f'T1_size{k}']:+.3f} |")
    (out / "e19_cross_oscillation_s1.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
