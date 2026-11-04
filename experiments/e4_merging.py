"""E4 - merging ('higher-order object', T3): does super-additivity of Phi predict super-additive survival?

For disjoint structures A, B in one world define
  merged entity  A u B  alive iff BOTH parts are inside their own viability sets   (definition ours; viability.mfpt_union)
  baseline for 'no cooperation': parts' exits independent  =>  hazards add  =>  V_union = 1/(1/V_A + 1/V_B)
  survival synergy  S = V_union * (1/V_A + 1/V_B)          (S > 1: exits cluster in time, merger lives longer than the sum of parts)
  Phi-synergy       dPhi = Phi(A u B) - Phi(A) - Phi(B)
Identity used for interpretation (static, disjoint):  h(AuB) = h(A) + h(B) - I(A;B)  [CoverThomas06 ch.2/8],
hence with K = h:  dPhi = (dP + beta dC) + lambda * I(A_t;B_t).
Key honest question: is dPhi anything more than the static dependence I(A;B)?  (baseline predictor)
"""
import argparse, pickle, itertools
import numpy as np
from scipy.stats import spearmanr
from common import RES, save_json
from vlife.viability import mfpt_from
from vlife.gaussian import mutual_information
from vlife.stats import cluster_bootstrap

ap = argparse.ArgumentParser(); ap.add_argument("--tag", default=""); TAG = ap.parse_args().tag
data = pickle.load(open(RES / f"e3_dataset{TAG}.pkl", "rb"))
beta, lam = 1.0, 0.25
rows = []     # one dict per pair
for wi, d in enumerate(data):
    subs = d["subsets"]; idx = {s: i for i, s in enumerate(subs)}; f = d["feat"]
    Phi = f["P"] + beta * f["C"] - lam * f["KH"]
    for a, b in itertools.combinations(subs, 2):
        # The merged entity must be a proper subset (it needs a non-empty environment): size <= N - 1, and <= 5 as before.
        if set(a) & set(b) or len(a) + len(b) > min(5, d["B"].shape[0] - 1) or min(a) > min(b):
            continue
        u = tuple(sorted(a + b)); i, j, k = idx[a], idx[b], idx[u]
        both = d["valid"][:, i] & d["valid"][:, j]
        Va, ea, _ = mfpt_from(d["exit_t"][:, i], d["event"][:, i], both)
        Vb, eb, _ = mfpt_from(d["exit_t"][:, j], d["event"][:, j], both)
        t = np.minimum(d["exit_t"][:, i], d["exit_t"][:, j]); ev = d["event"][:, i] | d["event"][:, j]
        Vu, eu, nv = mfpt_from(t, ev, both)
        if min(ea, eb) < 5 or nv < 50:
            continue
        rows.append(dict(w=wi, fam=d["family"], logS=np.log(Vu * (1 / Va + 1 / Vb)),
                         dPhi=Phi[k] - Phi[i] - Phi[j], dP=f["P"][k] - f["P"][i] - f["P"][j],
                         dC=f["C"][k] - f["C"][i] - f["C"][j], dKH=f["KH"][k] - f["KH"][i] - f["KH"][j],
                         I_AB=mutual_information(d["S"], list(a), list(b))))
print("pairs:", len(rows))
W = np.array([r["w"] for r in rows])
def col(name): return np.array([r[name] for r in rows])
logS = col("logS")
preds = {"dPhi_orig": col("dPhi"), "static MI I(A;B)": col("I_AB"), "dP": col("dP"), "dC": col("dC"), "-lam*dKH (=lam*I(A;B))": -lam * col("dKH")}

def mean_rho(world_ids, name, fam=None):
    r = []
    for w in world_ids:
        m = (W == w)
        if fam is not None and data[w]["family"] != fam: continue
        if m.sum() < 6 or np.ptp(preds[name][m]) == 0: continue
        r.append(spearmanr(preds[name][m], logS[m])[0])
    return np.nanmean(r) if r else np.nan

out = {"n_pairs": len(rows), "frac_logS_positive": float(np.mean(logS > 0)), "median_logS": float(np.median(logS)),
       "identity_check_max_abs": float(np.max(np.abs(col("dKH") + col("I_AB"))))}
for fam in (None, "equilibrium", "driven", "modular_driven"):
    key = fam or "all"; out[key] = {}
    for name in preds:
        pt, lo, hi = cluster_bootstrap(len(data), lambda b, n=name, f=fam: mean_rho(b, n, f), 300)
        out[key][name] = dict(rho=float(pt), lo=float(lo), hi=float(hi))
    m = np.ones(len(rows), bool) if fam is None else np.array([r["fam"] == fam for r in rows])
    out[key]["sign_agreement_dPhi_vs_S>1"] = float(np.mean((preds["dPhi_orig"][m] > 0) == (logS[m] > 0)))
    out[key]["frac_dPhi_positive"] = float(np.mean(preds["dPhi_orig"][m] > 0))
save_json(f"e4_merging{TAG}.json", out)
L = ["# E4 report (auto-generated)\n", f"pairs analysed: {out['n_pairs']};  fraction with S>1: {out['frac_logS_positive']:.2f};  "
     f"identity max|dKH + I(A;B)| = {out['identity_check_max_abs']:.2e}\n",
     "Mean within-world Spearman rho between predictor and log S (95% cluster-bootstrap CI)\n",
     "| family | predictor | rho | CI low | CI high |\n|---|---|---|---|---|"]
for fam in ("all", "equilibrium", "driven", "modular_driven"):
    for name in preds:
        v = out[fam][name]; L.append(f"| {fam} | {name} | {v['rho']:+.3f} | {v['lo']:+.3f} | {v['hi']:+.3f} |")
    L.append(f"| {fam} | sign agreement dPhi>0 <-> S>1 | {out[fam]['sign_agreement_dPhi_vs_S>1']:.2f} | | |")
(RES / f"e4_report{TAG}.md").write_text("\n".join(L)); print("\n".join(L))
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].scatter(preds["dPhi_orig"], logS, s=4, alpha=.3); ax[0].set_xlabel("dPhi_orig"); ax[0].set_ylabel("log S"); ax[0].axhline(0, c="k", lw=.5); ax[0].axvline(0, c="k", lw=.5)
ax[1].scatter(preds["static MI I(A;B)"], logS, s=4, alpha=.3, c="tab:orange"); ax[1].set_xlabel("static I(A;B)"); ax[1].set_ylabel("log S"); ax[1].axhline(0, c="k", lw=.5)
plt.tight_layout(); plt.savefig(RES / f"e4_merging{TAG}.png", dpi=130)
