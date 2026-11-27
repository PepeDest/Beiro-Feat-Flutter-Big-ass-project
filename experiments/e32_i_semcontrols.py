"""Niche I (docs/I.md): rules I1a-I1c. The package semcontrols against the code and the results of this repository.

    python experiments/e32_i_semcontrols.py
"""
import json, pickle, sys, time
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from common import ROOT, RES, save_json
sys.path.insert(0, str(ROOT / "semcontrols" / "src"))
import semcontrols as sc
from semcontrols import controls, scores
from semcontrols.linear import mutual_information
from vlife.agency import Organism, draw_organism, homeostat as v_homeostat
from vlife.negative_controls import cld_gaussian

C1_IDS = [d["i"] for d in json.load(open(RES / "e23_b4a_homeostat.json"))["organisms"]]


def cld1(args):
    i, version = args
    return scores.cld_linear(controls.homeostat(i, version), [1.0], 200_000, seed=i)[1][0]


def main():
    t0 = time.time()
    res, v = {}, {}
    # I1a: the controls are the same
    dev = 0.0
    for i in range(400):
        o = draw_organism(np.random.default_rng([2026, i]))
        for ver in ("intact", "nofeedback"):
            B, D, S = v_homeostat(o, ver)
            s = controls.homeostat(i, ver)
            dev = max(dev, *(float(np.abs(a - b).max()) for a, b in ((B, s.B), (D, s.D), (S, s.S))))
    vd = pickle.load(open(RES / "e26_v_dataset.pkl", "rb"))
    fu = {(u["seed"], u["i"]): u for u in json.load(open(ROOT / "cluster" / "data" / "f_units.json"))}
    us = controls.units()
    ok_units = len(us) == 840
    for u in us:
        r = next(r for r in vd[u.seed]["rows"] if r["i"] == u.i)
        f = fu[(u.seed, u.i)]
        ok_units &= (u.kind == r["kind"] == f["kind"] and u.p == r["p"] == f["p"] and u.V_on == r["V_on"] == f["V"]
                     and u.V_off == r["V_off"] and u.E_cyc == r["E_cyc"] and u.tau_star == vd[u.seed]["tau_star"]
                     == f["tau_star"])
    res["I1a"] = dict(max_dev_homeostat=dev, units_equal=bool(ok_units))
    v["I1a"] = "pass" if dev <= 1e-12 and ok_units else "fail"
    # I1b: the known answers
    nf = [controls.homeostat(i, "nofeedback") for i in range(400)]
    dv_nf = np.array([scores.kw_value(s) for s in nf])
    skw_dev = max(abs(scores.kw_stored(s) - mutual_information(s.S, s.agent, s.env)) /
                  mutual_information(s.S, s.agent, s.env) for s in nf)
    rd = controls.readers(200)
    rmax = max(max(abs(scores.kw_value(s, t)), scores.kw_stored(s, t)) for s in rd for t in (0.5, 1.0, 5.0))
    cdev = 0.0
    for i in range(5):
        s = controls.homeostat(i, "intact")
        a = scores.cld_linear(s, [1.0], 200_000, seed=i)
        b = cld_gaussian(s.B, s.D, s.S, s.agent, s.env, [1.0], 200_000, seed=i)
        cdev = max(cdev, abs(a[0] - b[0]), float(np.abs(a[1] - b[1]).max()), float(np.abs(a[2] - b[2]).max()))
    res["I1b"] = dict(frac_dV_negative_nf=float(np.mean(dv_nf < 0)), max_rel_dev_SKW=float(skw_dev),
                      reader_max=float(rmax), cld_max_dev=float(cdev))
    v["I1b"] = "pass" if (np.all(dv_nf < 0) and skw_dev < 1e-9 and rmax < 1e-10 and cdev <= 1e-12) else "fail"
    # I1c: check() gives the verdicts of niche C
    r_dv = sc.check(linear_score=scores.kw_value, homeostat_ids=C1_IDS, n_readers=200)
    with ProcessPoolExecutor(4) as ex:
        chi_i = dict(zip(C1_IDS, ex.map(cld1, [(i, "intact") for i in C1_IDS])))
        chi_n = dict(zip(C1_IDS, ex.map(cld1, [(i, "nofeedback") for i in C1_IDS])))
    lookup = lambda s: chi_i[s.meta["i"]] if s.meta.get("version") == "intact" else chi_n[s.meta["i"]]
    frac_cld = float(np.mean([chi_i[i] > chi_n[i] for i in C1_IDS]))
    r_rock = sc.check(unit_values={(u.seed, u.i): u.reference["cld_chi3"] for u in us})["rocks_order"]
    k1 = json.load(open(RES / "e26_c2_rocks.json"))["results"]["K1"]
    res["I1c"] = dict(frac_dV=r_dv["homeostat_order"]["frac"], frac_cld=frac_cld, rocks=[r_rock["auc"], *r_rock["ci"]],
                      K1=k1, check_kw_value={k: x["verdict"] for k, x in r_dv.items()})
    v["I1c"] = "pass" if (abs(res["I1c"]["frac_dV"] - 0.787) < 1e-3 and abs(frac_cld - 0.600) < 1e-3
                          and max(abs(a - b) for a, b in zip(res["I1c"]["rocks"], k1)) < 1e-9) else "fail"
    # description: the reference scores on the new reader control
    r_cld_reader = [scores.cld_linear(s, [1.0], 50_000, seed=s.meta["j"]) for s in rd]
    res["desc"] = dict(reader_cld_median=float(np.median([c[1][0] for c in r_cld_reader])),
                       reader_cld_min_over_se=float(min(c[1][0] / c[2][0] for c in r_cld_reader)),
                       check_kw_value=r_dv)
    res["seconds"] = time.time() - t0
    save_json("e32_i_semcontrols.json", dict(verdicts=v, results=res))
    L = ["# E32: the semcontrols package against this repository (niche I)", "", "Rules: docs/I.md.", "",
         "| Rule | Value | Verdict |", "|---|---|---|",
         f"| I1a | homeostat (B, D, S): largest difference {dev:.1e}. Units equal: {ok_units} | {v['I1a']} |",
         f"| I1b | ΔV_KW < 0 without feedback in {res['I1b']['frac_dV_negative_nf']:.3f}. S_KW against I(A; h): "
         f"{skw_dev:.1e}. Reader: largest \\|ΔV_KW\\| or S_KW {rmax:.1e}. CLD against vlife: {cdev:.1e} | {v['I1b']} |",
         f"| I1c | order fraction ΔV_KW {res['I1c']['frac_dV']:.4f}, CLD χ₁ {frac_cld:.4f}. rocks_order AUC "
         f"{r_rock['auc']:.4f} [{r_rock['ci'][0]:.4f}, {r_rock['ci'][1]:.4f}] (K1 {k1[0]:.4f}) | {v['I1c']} |", "",
         "Description: `check` with ΔV_KW: " + ", ".join(f"{k} {x['verdict']}" for k, x in r_dv.items()) +
         f". CLD χ₁ on the reader control: median {res['desc']['reader_cld_median']:.4f}, smallest χ₁ / se "
         f"{res['desc']['reader_cld_min_over_se']:.1f}. Time {res['seconds']:.0f} s."]
    (RES / "e32_i_semcontrols.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
