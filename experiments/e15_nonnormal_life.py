"""Niche A, step A2 (docs/A.md): which part of the entropy production goes with a shorter life?

World-level test on the existing S1 data. No new simulation.
  y   = mean over the structures of a world of log(V_on / V_eq)
  x   = sigma / lam_bar, x_osc = sigma_osc / lam_bar, x_nn = sigma_nn / lam_bar,  lam_bar = tr(B) / N
  s   = sigma_nn / sigma
Rules R1-R4 and the expectations are in docs/A.md (fixed before this script ran).
Decomposition: NagayamaKolchinskyIto26, via vlife.gaussian.oscillatory_nonnormal_ep.
"""
import argparse, json, pathlib, pickle, sys
import numpy as np
from scipy.stats import spearmanr

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vlife.gaussian import oscillatory_nonnormal_ep  # noqa: E402

DATASETS = {"baseline": "e3_dataset_v2.pkl", "Dtest_r3": "e3_dataset_D3_v2.pkl"}
FAMILIES = ("driven", "modular_driven")


def world_table(path):
    rows = []
    for w in pickle.load(open(path, "rb")):
        if w["family"] not in FAMILIES:
            continue
        s, so, sn = oscillatory_nonnormal_ep(w["B"], w["D"], w["S"])
        lam = np.trace(w["B"]) / w["B"].shape[0]
        y = float(np.mean(np.log(w["V_on"] / w["V_eq"])))
        rows.append(dict(family=w["family"], y=y, x=s / lam, x_osc=so / lam, x_nn=sn / lam, share=sn / s))
    return rows


def _z(v):
    return (v - v.mean()) / v.std()


def betas(rows):
    y = np.array([r["y"] for r in rows])
    X = np.column_stack([np.ones(len(rows)), _z(np.log([r["x_osc"] for r in rows])), _z(np.log([r["x_nn"] for r in rows]))])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    return b[1], b[2]


def stats(rows):
    y = np.array([r["y"] for r in rows])
    rho_s = spearmanr([r["share"] for r in rows], y)[0]
    rho_x = spearmanr([r["x"] for r in rows], y)[0]
    b_osc, b_nn = betas(rows)
    return dict(rho_share=rho_s, rho_total=rho_x, b_osc=b_osc, b_nn=b_nn, d_beta=b_nn - b_osc)


def boot(rows, n_boot, seed):
    rng = np.random.default_rng(seed)
    out = {k: [] for k in stats(rows)}
    n = len(rows)
    for _ in range(n_boot):
        st = stats([rows[i] for i in rng.integers(0, n, n)])
        for k, v in st.items():
            out[k].append(v)
    return {k: (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))) for k, v in out.items()}


def life_label(ci):
    return "shortens life" if ci[1] < 0 else ("lengthens life" if ci[0] > 0 else "no effect")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n_boot", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=2026)
    a = ap.parse_args()
    res = {}
    for name, fn in DATASETS.items():
        rows = world_table(ROOT / "results" / fn)
        point, ci = stats(rows), boot(rows, a.n_boot, a.seed)
        fam = {}
        for f in FAMILIES:
            sub = [r for r in rows if r["family"] == f]
            st = stats(sub)
            fam[f] = dict(n=len(sub), rho_share=st["rho_share"], b_osc=st["b_osc"], b_nn=st["b_nn"])
        res[name] = dict(
            n_worlds=len(rows), point=point, ci=ci, per_family=fam,
            R1=life_label(ci["rho_share"]), R2_osc=life_label(ci["b_osc"]), R2_nn=life_label(ci["b_nn"]),
            R3="the parts differ" if (ci["d_beta"][0] > 0 or ci["d_beta"][1] < 0) else "not separated",
            rows=rows)
    r4 = "the decomposition adds information" if any(res[k]["R3"] == "the parts differ" for k in res) else "gate triggers"
    out = ROOT / "results"
    json.dump(dict(R4=r4, **{k: {kk: vv for kk, vv in v.items()} for k, v in res.items()}),
              open(out / "e15_nonnormal_life.json", "w"), indent=1)
    L = ["# E15: nonnormal and oscillatory dissipation against life (niche A, step A2)", "",
         "Rules: docs/A.md. 95 % bootstrap intervals over worlds.", "",
         "| Rule | Statistic | baseline | D-test r = 3 |", "|---|---|---|---|"]
    def cell(k, key, lab=None):
        p, c = res[k]["point"][key], res[k]["ci"][key]
        return f"{p:+.2f} [{c[0]:+.2f}, {c[1]:+.2f}]" + (f", {res[k][lab]}" if lab else "")
    L.append(f"| R1 | ρ(s, y) | {cell('baseline', 'rho_share', 'R1')} | {cell('Dtest_r3', 'rho_share', 'R1')} |")
    L.append(f"| R2 | β_osc | {cell('baseline', 'b_osc', 'R2_osc')} | {cell('Dtest_r3', 'b_osc', 'R2_osc')} |")
    L.append(f"| R2 | β_nn | {cell('baseline', 'b_nn', 'R2_nn')} | {cell('Dtest_r3', 'b_nn', 'R2_nn')} |")
    L.append(f"| R3 | β_nn − β_osc | {cell('baseline', 'd_beta', 'R3')} | {cell('Dtest_r3', 'd_beta', 'R3')} |")
    L.append(f"| description | ρ(x total, y) | {cell('baseline', 'rho_total')} | {cell('Dtest_r3', 'rho_total')} |")
    L += ["", f"R4: **{r4}**", "", "Per family (description only):", "",
          "| Data | Family | n | ρ(s, y) | β_osc | β_nn |", "|---|---|---|---|---|---|"]
    for k in res:
        for f, v in res[k]["per_family"].items():
            L.append(f"| {k} | {f} | {v['n']} | {v['rho_share']:+.2f} | {v['b_osc']:+.3f} | {v['b_nn']:+.3f} |")
    for k in res:
        y = np.array([r["y"] for r in res[k]["rows"]])
        L.append(f"\n{k}: mean y = {y.mean():+.3f} (s.e. {y.std() / np.sqrt(len(y)):.3f}) over {len(y)} worlds.")
    (out / "e15_nonnormal_life.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, axs = plt.subplots(1, 2, figsize=(9, 3.6))
        for ax, k in zip(axs, res):
            for f, m in zip(FAMILIES, "os"):
                rr = [r for r in res[k]["rows"] if r["family"] == f]
                ax.scatter([r["share"] for r in rr], [r["y"] for r in rr], marker=m, label=f, s=18)
            ax.set_xlabel("nonnormal share s = σ_nn / σ"); ax.set_ylabel("mean log(V_on / V_eq)"); ax.set_title(k)
            ax.axhline(0, lw=0.5, c="k")
        axs[0].legend(fontsize=8); fig.tight_layout(); fig.savefig(out / "e15_nonnormal_life.png", dpi=150)
    except ImportError:
        pass
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("\n".join(L))


if __name__ == "__main__":
    main()
