"""Niche B, step B4b (docs/B.md): stored semantic information against Phi_TC on the structures of the S1 baseline worlds
(phase C data, results/e3_dataset_v2.pkl). Open question 6 of the paper. No new simulation of exit times.
Rules (W0, W1, Q1-Q4) and the expectations are in docs/B.md (fixed before this script ran).
"""
import json, pickle, sys, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from scipy.stats import spearmanr
from common import RES, save_json
from vlife.gaussian import total_correlation, stationary_cov, mutual_information
from vlife.stats import cluster_bootstrap
from vlife.semantic_apply import stored_semantic, value_on

TAU, N_STARTS, LAM, N_BOOT = 1.0, 8, 0.25, 400


def world_rows(args):
    k, d = args
    m = (d["ev_on"] >= 5) & (d["ev_eq"] >= 5)
    if m.sum() < 8:                                   # same mask as S1b
        return None
    N = d["S"].shape[0]
    subs = [s for s, keep in zip(d["subsets"], m) if keep]
    f = {key: d["feat"][key][m] for key in ("P", "C", "size")}
    f["TC"] = np.array([total_correlation(d["S"], s) for s in subs])
    S_G, dV, I_act, method = [], [], [], []
    for j, s in enumerate(subs):
        agent, env = list(s), [i for i in range(N) if i not in s]
        val, how = stored_semantic(d["B"], d["D"], d["S"], agent, env, TAU, N_STARTS, np.random.default_rng([k, j]))
        S_G.append(val); method.append(how)
        dV.append(value_on(d["B"], d["D"], d["S"], agent, env, TAU))
        I_act.append(mutual_information(d["S"], agent, env))
    f.update(S_G=np.array(S_G), dV=np.array(dV), I_act=np.array(I_act))
    return dict(k=k, family=d["family"], y=np.log(d["V_on"][m]), f=f, method=method,
                W1=float(np.abs(d["S"] - stationary_cov(d["B"], d["D"])).max()))


def rho(sc, y, size, stratify):
    """Same as S1b: Spearman in one world, pooled or as the mean over sizes with at least 6 structures."""
    groups = [np.ones(len(y), bool)] if not stratify else [size == q for q in np.unique(size)]
    r = [spearmanr(sc[g], y[g])[0] for g in groups if g.sum() >= 6 and np.ptp(sc[g]) > 0 and np.ptp(y[g]) > 0]
    return np.mean(r) if r else np.nan


def scores(f):
    return {"Phi_TC": f["P"] + f["C"] - LAM * f["TC"], "S_G": f["S_G"], "dV_KW": f["dV"], "I_act": f["I_act"],
            "efficiency": f["S_G"] / np.maximum(f["I_act"], 1e-300)}


def mean_rho(W, name, stratify):
    vals = np.array([rho(scores(w["f"])[name], w["y"], w["f"]["size"], stratify) for w in W])
    pt, lo, hi = cluster_bootstrap(len(W), lambda b: np.nanmean(vals[b]), N_BOOT)
    return [float(pt), float(lo), float(hi)], vals


def diff_rho(W, a, b, stratify):
    va, vb = mean_rho(W, a, stratify)[1], mean_rho(W, b, stratify)[1]
    pt, lo, hi = cluster_bootstrap(len(W), lambda i: np.nanmean(va[i]) - np.nanmean(vb[i]), N_BOOT)
    return [float(pt), float(lo), float(hi)]


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    t0 = time.time()
    data = pickle.load(open(RES / "e3_dataset_v2.pkl", "rb"))
    with ProcessPoolExecutor(4) as ex:
        W = [w for w in ex.map(world_rows, list(enumerate(data))) if w is not None]
    print(f"semantic information done for {len(W)} worlds, {time.time() - t0:.0f} s", flush=True)
    ref = json.load(open(RES / "s1b_unitfree_v2.json"))["results"]["_base"]
    mine = mean_rho(W, "Phi_TC", False)[0], mean_rho(W, "Phi_TC", True)[0]
    W0 = all(abs(x - y) <= 1e-9 for a, b in zip(mine, (ref["Phi_TC"], ref["Phi_TC (equal size)"])) for x, y in zip(a, b))
    W1 = max(w["W1"] for w in W) < 1e-8
    if not (W0 and W1):
        raise SystemExit(f"check fails: W0 {W0}, W1 {W1} (docs/B.md, B4b). Stop.")
    res = {name: dict(pooled=mean_rho(W, name, False)[0], equal_size=mean_rho(W, name, True)[0])
           for name in ("Phi_TC", "S_G", "dV_KW", "I_act", "efficiency")}
    res["diff_PhiTC_minus_SG"] = dict(pooled=diff_rho(W, "Phi_TC", "S_G", False), equal_size=diff_rho(W, "Phi_TC", "S_G", True))
    fam = {}
    for F in sorted({w["family"] for w in W}):
        WF = [w for w in W if w["family"] == F]
        fam[F] = {name: mean_rho(WF, name, False)[0] for name in ("Phi_TC", "S_G", "dV_KW")}
    allf = lambda key: np.concatenate([w["f"][key] for w in W])
    desc = dict(n_worlds=len(W), n_structures=int(sum(len(w["y"]) for w in W)),
                methods={m: sum(x == m for w in W for x in w["method"]) for m in {x for w in W for x in w["method"]}},
                eff_median=float(np.median(allf("S_G") / allf("I_act"))),
                frac_dV_pos=float(np.mean(allf("dV") > 0)),
                rho_SG_PhiTC_all=float(spearmanr(allf("S_G"), np.concatenate([scores(w["f"])["Phi_TC"] for w in W]))[0]),
                rho_SG_size_all=float(spearmanr(allf("S_G"), allf("size"))[0]), by_family=fam)
    lab = lambda d: "Phi_TC better" if d[1] > 0 else "S_G better" if d[2] < 0 else "no clear difference"
    v = dict(W0="pass", W1="pass",
             Q1="ranks structures" if res["S_G"]["pooled"][1] > 0 else "does not rank structures",
             Q2="ranks structures" if res["dV_KW"]["pooled"][1] > 0 else "does not rank structures",
             Q3=lab(res["diff_PhiTC_minus_SG"]["pooled"]), Q4=lab(res["diff_PhiTC_minus_SG"]["equal_size"]))
    save_json("e24_b4b_worlds.json", dict(verdicts=v, results=res, description=desc,
                                           worlds=[dict(k=w["k"], family=w["family"], y=w["y"], method=w["method"],
                                                        **{key: w["f"][key] for key in w["f"]}) for w in W]))
    f = lambda x: f"{x[0]:+.3f} [{x[1]:+.3f}, {x[2]:+.3f}]"
    L = ["# E24: stored semantic information against Φ_TC on the S1 structures (niche B, step B4b)", "",
         "Rules: docs/B.md, B4b.", "", f"W0 (Φ_TC equals S1b phase C): pass. W1 (S is stationary): pass. "
         f"{desc['n_worlds']} worlds, {desc['n_structures']} structures.", "",
         "| Score | ρ with log V, pooled | ρ with log V, equal size |", "|---|---|---|"]
    for name in ("Phi_TC", "S_G", "dV_KW", "I_act", "efficiency"):
        L.append(f"| {name} | {f(res[name]['pooled'])} | {f(res[name]['equal_size'])} |")
    L += ["", "| Rule | Question | Value | Verdict |", "|---|---|---|---|",
          f"| Q1 | Does S_G rank structures (pooled)? | {f(res['S_G']['pooled'])} | {v['Q1']} |",
          f"| Q2 | Does ΔV_KW rank structures (pooled)? | {f(res['dV_KW']['pooled'])} | {v['Q2']} |",
          f"| Q3 | ρ(Φ_TC) − ρ(S_G), pooled | {f(res['diff_PhiTC_minus_SG']['pooled'])} | {v['Q3']} |",
          f"| Q4 | ρ(Φ_TC) − ρ(S_G), equal size | {f(res['diff_PhiTC_minus_SG']['equal_size'])} | {v['Q4']} |", "",
          "Description:", f"- Methods: {desc['methods']}.",
          f"- Semantic efficiency S_G / I_act: median {desc['eff_median']:.3f}. ΔV_KW > 0 in {desc['frac_dV_pos']:.3f}.",
          f"- Over all structures: ρ(S_G, Φ_TC) = {desc['rho_SG_PhiTC_all']:+.3f}, ρ(S_G, size) = {desc['rho_SG_size_all']:+.3f}.",
          "- By family (pooled ρ with log V): " + "; ".join(
              f"{F}: Φ_TC {f(x['Phi_TC'])}, S_G {f(x['S_G'])}, ΔV_KW {f(x['dV_KW'])}" for F, x in fam.items()) + "."]
    (RES / "e24_b4b_worlds.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
