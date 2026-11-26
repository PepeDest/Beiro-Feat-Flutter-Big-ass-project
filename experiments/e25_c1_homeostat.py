"""Niche C, step C1 (docs/C.md): negative control in the S3 homeostat. The organism without feedback (L = 0) uses no
information. Do the value of information and the stored semantic information of KolchinskyWolpert18, and the Causal
Leverage Density (CLD), give zero there? No new simulation of exit times.

Data: results/e5_dataset_b4.pkl, rebuilt and checked in B4a. Check A0 runs again. Rules (A0, N1-N4) and the
expectations are in docs/C.md (fixed before this script ran).
"""
import json, pickle, sys
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from common import RES, save_json
from vlife.agency import Organism, homeostat
from vlife.gaussian import mutual_information
from vlife.semantic_apply import value_on, stored_semantic
from vlife.negative_controls import cld_gaussian, time_average
from e23_b4a_homeostat import same, boot

AGENT, ENV, TARGET_V, TAU = [1, 2, 3, 4], [0], 3, 1.0
VERSIONS = ("intact", "nofeedback")
T3 = np.linspace(0.0, 5.0, 21)
N_MC, N_MC_DESC = 200_000, 50_000


def scores(args):
    r, version = args
    B, D, S = homeostat(Organism(**r["org"]), version)
    dV = float(value_on(B, D, S, AGENT, ENV, TAU, [TARGET_V]))
    I_act = float(mutual_information(S, AGENT, ENV))
    S_kw, how = stored_semantic(B, D, S, AGENT, ENV, TAU, target=[TARGET_V])
    omega, chi1, se1 = cld_gaussian(B, D, S, AGENT, ENV, [TAU], N_MC, seed=r["i"])
    _, chiA, _ = cld_gaussian(B, D, S, AGENT, ENV, [TAU], N_MC_DESC, seed=r["i"], keep=AGENT)
    _, chi3, _ = cld_gaussian(B, D, S, AGENT, ENV, T3, N_MC_DESC, seed=r["i"])
    return dict(i=r["i"], version=version, dV=dV, dV_A=float(value_on(B, D, S, AGENT, ENV, TAU)), I_act=I_act,
                S_kw=float(S_kw), method=how, S_kw_geq=0.0 if dV < 0 else float(S_kw), omega_bits=omega,
                chi1=float(chi1[0]), chi1_se=float(se1[0]), chi1_agent=float(chiA[0]), chi3=time_average(T3, chi3))


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    new = json.load(open(RES / "e5_summary_b4.json")); old = json.load(open(RES / "e5_summary_v2.json"))
    if not (same(new["results"], old["results"]) and new["verdicts"] == old["verdicts"]):
        raise SystemExit("A0 fails: the rebuilt S3 data differ from phase C. Stop (docs/C.md, C1).")
    rows = [r for r in pickle.load(open(RES / "e5_dataset_b4.pkl", "rb")) if min(r[v]["ev"] for v in ("intact", "scrambled", "nofeedback")) >= 5]
    n = len(rows)
    with ProcessPoolExecutor(4) as ex:
        out = list(ex.map(scores, [(r, v) for r in rows for v in VERSIONS]))
    by = {v: [d for d in out if d["version"] == v] for v in VERSIONS}
    a = lambda v, k: np.array([d[k] for d in by[v]], float)
    nf = lambda k: a("nofeedback", k)
    res = dict(n=n)
    res["N1"] = dict(max_abs=float(np.abs(nf("dV")).max()), frac_negative=float(np.mean(nf("dV") < 0)),
                     median=float(np.median(nf("dV"))))
    eff = nf("S_kw") / nf("I_act")
    res["N2"] = dict(min=float(nf("S_kw").min()), median_efficiency=float(np.median(eff)),
                     frac_efficiency_1=float(np.mean(np.abs(eff - 1) < 1e-6)))
    res["N3"] = dict(min_chi1=float(nf("chi1").min()), min_ratio_to_se=float((nf("chi1") / nf("chi1_se")).min()),
                     median_chi1=float(np.median(nf("chi1"))))
    res["N4"] = {k: boot(n, lambda ids, k=k: float(np.mean(a("intact", k)[ids] > nf(k)[ids])))
                 for k in ("dV", "S_kw", "chi1")}
    desc = {k: dict(median_intact=float(np.median(a("intact", k))), median_nofeedback=float(np.median(nf(k))))
            for k in ("dV", "dV_A", "I_act", "S_kw", "S_kw_geq", "omega_bits", "chi1", "chi1_agent", "chi3")}
    for k in ("dV", "S_kw", "chi1", "chi3"):
        desc[k]["ratio_nf_to_intact"] = desc[k]["median_nofeedback"] / desc[k]["median_intact"]
    desc["frac_dV_A_negative_nf"] = float(np.mean(nf("dV_A") < 0))
    desc["frac_S_kw_geq_zero_nf"] = float(np.mean(nf("S_kw_geq") == 0))
    desc["methods"] = {m: sum(d["method"] == m for d in out) for m in {d["method"] for d in out}}
    desc["eff_intact_median"] = float(np.median(a("intact", "S_kw") / a("intact", "I_act")))
    order = lambda x: "intact higher" if x[1] > 0.5 else "no feedback higher" if x[2] < 0.5 else "no clear order"
    v = dict(A0="pass", N1="zero" if res["N1"]["max_abs"] < 1e-9 else "not zero",
             N2="zero" if res["N2"]["min"] < 1e-9 and nf("S_kw").max() < 1e-9 else "not zero",
             N3="zero" if np.all(nf("chi1") < 3 * nf("chi1_se")) else "not zero",
             N4={k: order(x) for k, x in res["N4"].items()})
    save_json("e25_c1_homeostat.json", dict(verdicts=v, results=res, description=desc, organisms=out))
    f = lambda x: f"{x[0]:.3f} [{x[1]:.3f}, {x[2]:.3f}]"
    L = ["# E25: negative control in the S3 homeostat (niche C, step C1)", "", "Rules: docs/C.md, C1.", "",
         f"A0 (rebuilt S3 data equal phase C): pass. Organisms: {n}. Versions: intact, no feedback.", "",
         "| Rule | Question | Value | Verdict |", "|---|---|---|---|",
         f"| N1 | ΔV_KW zero without feedback? | max \\|ΔV\\| {res['N1']['max_abs']:.3g}, ΔV < 0 in {res['N1']['frac_negative']:.3f}, median {res['N1']['median']:+.4f} | {v['N1']} |",
         f"| N2 | S_KW zero without feedback? | smallest {res['N2']['min']:.3g} nats, median efficiency {res['N2']['median_efficiency']:.3f} (= 1 in {res['N2']['frac_efficiency_1']:.3f}) | {v['N2']} |",
         f"| N3 | CLD zero without feedback? | smallest χ₁ {res['N3']['min_chi1']:.4f}, smallest χ₁ / se {res['N3']['min_ratio_to_se']:.1f}, median χ₁ {res['N3']['median_chi1']:.4f} | {v['N3']} |"]
    for k, lab in (("dV", "ΔV_KW"), ("S_kw", "S_KW"), ("chi1", "CLD χ₁")):
        L.append(f"| N4 | {lab}: fraction intact > no feedback | {f(res['N4'][k])} | {v['N4'][k]} |")
    L += ["", "Description (medians):", "", "| Score | Intact | No feedback |", "|---|---|---|"]
    for k in ("dV", "dV_A", "I_act", "S_kw", "S_kw_geq", "omega_bits", "chi1", "chi1_agent", "chi3"):
        L.append(f"| {k} | {desc[k]['median_intact']:+.4f} | {desc[k]['median_nofeedback']:+.4f} |")
    L += ["", f"- ΔV on the whole agent < 0 without feedback in {desc['frac_dV_A_negative_nf']:.3f} of organisms.",
          f"- S_KW in the reading V ≥ V_act is 0 without feedback in {desc['frac_S_kw_geq_zero_nf']:.3f} of organisms.",
          f"- Efficiency S_KW / I_act, intact: median {desc['eff_intact_median']:.3f}.",
          f"- Methods: {desc['methods']}.",
          "- The simulated VoI is 0 by construction without feedback (the actuator reads nothing)."]
    (RES / "e25_c1_homeostat.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
