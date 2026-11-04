"""E9 / ROADMAP S4 - growth-rate viability from stored E3 exit data, and Price terms. Rules: docs/S4.md. No simulation."""
import pickle
import numpy as np
from scipy.stats import spearmanr
from common import RES, save_json
from vlife.viability import GrowthRateViability, mfpt_from
from vlife.gaussian import total_correlation

DT, MU_SWAP = 0.05, 0.1
g = GrowthRateViability(b=1.0)


def world_table(d):
    m = (d["ev_on"] >= 5) & (d["ev_eq"] >= 5)
    if m.sum() < 8:
        return None
    J = np.where(m)[0]; V = d["V_on"][J]; a_med = float(np.median(V))
    r0, rm, R0 = [], [], []
    for j in J:
        e, ev, va = d["exit_t"][:, j].astype(float), d["event"][:, j], d["valid"][:, j]
        r0.append(g.rate(e, ev, va, DT, d["t_max"], 0.0)[0])
        x = g.rate(e, ev, va, DT, d["t_max"], a_med); rm.append(x[0]); R0.append(x[1])
    subs = d["subsets"]; f = d["feat"]
    TC = np.array([total_correlation(d["S"], s) for s in subs]); z_all = f["P"] + f["C"] - 0.25 * TC
    return dict(J=J, logV=np.log(V), r0=np.array(r0), rm=np.array(rm), R0=np.array(R0), z_all=z_all, subs=subs, a_med=a_med)


def price(t):
    subs, z = t["subs"], t["z_all"]; idx = {s: i for i, s in enumerate(subs)}
    N = max(max(s) for s in subs) + 1
    dz = []
    for j in t["J"]:
        A = subs[j]; out = [i for i in range(N) if i not in A]
        sw = [idx[tuple(sorted(set(A) - {a} | {b}))] for a in A for b in out]
        dz.append(MU_SWAP * (z[sw].mean() - z[j]))
    w, zz = t["R0"], z[t["J"]]; wbar = w.mean()
    return float(np.mean(w * zz) / wbar - zz.mean()), float(np.mean(w * np.array(dz)) / wbar)


def cboot(vals, n_boot=400, rng=np.random.default_rng(0)):
    vals = np.asarray(vals, float); pt = np.nanmean(vals)
    bs = [np.nanmean(vals[rng.integers(0, len(vals), len(vals))]) for _ in range(n_boot)]
    lo, hi = np.percentile(bs, [2.5, 97.5]); return [float(pt), float(lo), float(hi)]


base = [world_table(d) for d in pickle.load(open(RES / "e3_dataset.pkl", "rb"))]
wide = [world_table(d) for d in pickle.load(open(RES / "e3_dataset_p0.2.pkl", "rb"))]
B = [t for t in base if t is not None]
rho = lambda a, b: spearmanr(a, b)[0]
G1_0 = cboot([rho(t["r0"], t["logV"]) for t in B]); G1_m = cboot([rho(t["rm"], t["logV"]) for t in B])
diffs, sV, sR = [], [], []
for tb, tw in zip(base, wide):
    if tb is None or tw is None:
        continue
    common = np.intersect1d(tb["J"], tw["J"])
    if len(common) < 8:
        continue
    ib = np.searchsorted(tb["J"], common); iw = np.searchsorted(tw["J"], common)
    a, b = rho(tb["logV"][ib], tw["logV"][iw]), rho(tb["rm"][ib], tw["rm"][iw]); sV.append(a); sR.append(b); diffs.append(b - a)
G2 = cboot(diffs)
G3 = cboot([rho(t["z_all"][t["J"]], t["rm"]) for t in B])
P = np.array([price(t) for t in B]); S4 = cboot(P[:, 0]); T4 = cboot(P[:, 1])
lab1 = lambda x: "agree" if x[0] >= 0.9 else "moderate" if x[0] >= 0.5 else "disagree strongly"
v = dict(G1_am0=lab1(G1_0), G1_amMedian=lab1(G1_m),
         G2="r more stable" if G2[1] > 0 else "V more stable" if G2[2] < 0 else "same",
         G3="yes" if G3[1] > 0 else "no",
         G4="mutation erodes selection" if S4[1] > 0 and T4[2] < 0 else "not shown")
desc = dict(n_worlds=len(B), n_worlds_G2=len(diffs), rho_V_stability=cboot(sV), rho_r_stability=cboot(sR),
            frac_S_pos=float(np.mean(P[:, 0] > 0)), frac_T_neg=float(np.mean(P[:, 1] < 0)),
            median_a_m=float(np.median([t["a_med"] for t in B])),
            rho_PhiTC_logV=cboot([rho(t["z_all"][t["J"]], t["logV"]) for t in B]))
save_json("e9_growth.json", dict(G1_am0=G1_0, G1_amMedian=G1_m, G2=G2, G3=G3, G4_S=S4, G4_T=T4, verdicts=v, description=desc))
f = lambda x: f"{x[0]:+.3f} [{x[1]:+.3f}, {x[2]:+.3f}]"
L = ["# E9 / S4 report (auto-generated; rules in docs/S4.md)\n", f"Worlds: {len(B)} (S1 baseline).\n",
     "| Rule | Value [95% CI] | Verdict |", "|---|---|---|",
     f"| G1: rho(r, log V), a_m = 0 | {f(G1_0)} | {v['G1_am0']} |",
     f"| G1: rho(r, log V), a_m = median V | {f(G1_m)} | {v['G1_amMedian']} |",
     f"| G2: stability(r) - stability(V), p_out 0.05 -> 0.2 ({len(diffs)} worlds) | {f(G2)} | {v['G2']} |",
     f"| G3: rho(Phi_TC, r) | {f(G3)} | {v['G3']} |",
     f"| G4: selection S / transmission T | {f(S4)} / {f(T4)} | {v['G4']} |",
     "\nDescription only:"] + [f"- {k}: {val}" for k, val in desc.items()]
(RES / "e9_growth.md").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L))
