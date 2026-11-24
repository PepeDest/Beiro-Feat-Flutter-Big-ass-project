"""Niche C, step C2 (docs/C.md): Causal Leverage Density (CLD) of S2b rocks and oscillators, 7 draws (seeds 2026-2032).
Does CLD rate passive memory (rocks) as high as persistence that a drive keeps (oscillators)?

Step 1 runs the V part of e6b_rockmemory.py again (the .pkl files of draws 2027-2032 are not on this PC) and checks
T1 against the committed summaries. Step 2 computes CLD for each unit. Rules (T1, K1-K3, gate) and the expectations are
in docs/C.md (fixed before this script ran).
"""
import json, pickle, sys, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from scipy.stats import spearmanr
from common import RES, save_json
from vlife.nonlinear import draw_units, Unit
from vlife.negative_controls import cld_mirror, time_average
from e6b_rockmemory import job_V, strat_auc, auc, DT

SEEDS = tuple(range(2026, 2033))
N_WALK, N_GRID, T_BURN, N_BOOT = 20_000, 41, 50.0, 10_000


def summary_name(seed):
    return "e6b_summary.json" if seed == 2026 else f"e6b_summary_seed{seed}.json"


def job_cld(job):
    seed, i, kind, p, tau_star, V = job
    grid = list(np.linspace(0.0, tau_star, N_GRID))
    times = sorted(set(grid) | {V / 2})
    r = cld_mirror(Unit(kind, p), N_WALK, times, DT, np.random.default_rng([seed, i, 31]), t_burn=T_BURN)
    chi = dict(zip(times, r["chi"])); null = dict(zip(times, r["chi_null"]))
    g = np.array([chi[t] for t in grid])
    return dict(seed=seed, i=i, chi3=time_average(grid, g), chi1=float(chi[grid[-1]]), chi_own=float(chi[V / 2]),
                null_tau=float(null[grid[-1]]), null_max=float(max(null.values())), curve=g)


def boot_draws(vals, n_boot=N_BOOT, seed=0):
    vals = np.asarray(vals, float); rng = np.random.default_rng(seed)
    bs = [np.nanmean(vals[rng.integers(0, len(vals), len(vals))]) for _ in range(n_boot)]
    lo, hi = np.nanpercentile(bs, [2.5, 97.5])
    return [float(np.nanmean(vals)), float(lo), float(hi)]


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    t0 = time.time()
    draws, T1 = {}, []
    with ProcessPoolExecutor(4) as ex:
        for seed in SEEDS:
            units = [(i, u) for i, u in enumerate(draw_units(np.random.default_rng([seed, 99]))) if u.kind != "well"]
            rows = list(ex.map(job_V, [(i, u.kind, u.p, seed, 3000.0) for i, u in units]))
            tau_star = float(np.median([r["V_on"] for r in rows if r["kind"] == "rock"]))
            g1 = float(np.median([np.log(r["V_on"] / r["V_off"]) for r in rows if r["kind"] == "oscillator"]))
            ref = json.load(open(RES / summary_name(seed)))
            ok = abs(tau_star - ref["tau_star"]) <= 1e-9 * ref["tau_star"] and abs(g1 - ref["results"]["G1"][0]) <= 1e-9
            T1.append(dict(seed=seed, tau_star=tau_star, ref_tau_star=ref["tau_star"], G1=g1, ref_G1=ref["results"]["G1"][0], ok=ok))
            draws[seed] = dict(rows=rows, tau_star=tau_star, auc_C_ref=ref["results"]["G2"][0])
            print(f"seed {seed}: tau* {tau_star:.4f} (ref {ref['tau_star']:.4f}), T1 {ok}, {time.time() - t0:.0f} s", flush=True)
        pickle.dump(draws, open(RES / "e26_v_dataset.pkl", "wb"))
        if not all(t["ok"] for t in T1):
            save_json("e26_c2_T1_fail.json", T1)
            raise SystemExit("T1 fails: the rebuilt S2b data differ from the summaries. Stop (docs/C.md, C2).")
        jobs = [(seed, r["i"], r["kind"], r["p"], d["tau_star"], r["V_on"]) for seed, d in draws.items() for r in d["rows"]]
        cl = {(c["seed"], c["i"]): c for c in ex.map(job_cld, jobs)}
    print(f"CLD done, {time.time() - t0:.0f} s", flush=True)
    per = {}
    for seed, d in draws.items():
        rows = d["rows"]; kind = np.array([r["kind"] for r in rows]); lV = np.log([r["V_on"] for r in rows])
        c = lambda k: np.array([cl[(seed, r["i"])][k] for r in rows])
        rk, osc = kind == "rock", kind == "oscillator"
        a3, nb3 = strat_auc(c("chi3"), lV, kind); a1, nb1 = strat_auc(c("chi1"), lV, kind)
        per[seed] = dict(tau_star=d["tau_star"], auc_chi3=a3, bins_chi3=nb3, auc_chi1=a1, bins_chi1=nb1,
                         rho_chi3_logV_rocks=float(spearmanr(c("chi3")[rk], lV[rk])[0]),
                         auc_own_unstratified=auc(c("chi_own")[rk], c("chi_own")[osc]),
                         auc_chi3_unstratified=auc(c("chi3")[rk], c("chi3")[osc]),
                         median_chi3={"rock": float(np.median(c("chi3")[rk])), "oscillator": float(np.median(c("chi3")[osc]))},
                         median_chi1={"rock": float(np.median(c("chi1")[rk])), "oscillator": float(np.median(c("chi1")[osc]))},
                         null_tau_median=float(np.median(c("null_tau"))), null_max=float(c("null_max").max()),
                         auc_C_ref=d["auc_C_ref"])
    K1 = boot_draws([per[s]["auc_chi3"] for s in SEEDS]); K2 = boot_draws([per[s]["auc_chi1"] for s in SEEDS])
    K3 = boot_draws([per[s]["rho_chi3_logV_rocks"] for s in SEEDS])
    lab = lambda x: "CLD mislabels rocks" if x[1] > 0.5 else "CLD favours oscillators" if x[2] < 0.5 else "no difference"
    v = dict(T1="pass", K1=lab(K1), K2=lab(K2), K3="yes" if K3[1] > 0 else "no")
    v["Gate"] = "passes" if v["K1"] == "CLD favours oscillators" else "fails: use the flux ratio V_on / V_off"
    desc = dict(auc_own_mean=float(np.mean([per[s]["auc_own_unstratified"] for s in SEEDS])),
                auc_C_ref_mean=float(np.mean([per[s]["auc_C_ref"] for s in SEEDS])), seconds=time.time() - t0)
    save_json("e26_c2_rocks.json", dict(verdicts=v, results=dict(T1=T1, K1=K1, K2=K2, K3=K3), per_draw=per,
                                        description=desc, units=list(cl.values())))
    f = lambda x: f"{x[0]:.3f} [{x[1]:.3f}, {x[2]:.3f}]"
    L = ["# E26: Causal Leverage Density of S2b rocks and oscillators (niche C, step C2)", "", "Rules: docs/C.md, C2.", "",
         f"T1 (rebuilt S2b data equal the summaries in all 7 draws): pass. Walkers: {N_WALK} in each group. dt = {DT}.", "",
         "| Rule | Question | Value | Verdict |", "|---|---|---|---|",
         f"| K1 | Stratified AUC of χ₃(0, τ*), rock > oscillator, mean over 7 draws | {f(K1)} | {v['K1']} |",
         f"| K2 | Stratified AUC of χ₁(τ*) | {f(K2)} | {v['K2']} |",
         f"| K3 | ρ(χ₃, log V) over rocks | {f(K3)} | {v['K3']} |",
         f"| Gate | Does CLD pass the control? | | {v['Gate']} |", "",
         "| Seed | τ* | AUC χ₃ | AUC χ₁ | median χ₃ rock / osc | AUC own lag (unstratified) | AUC C(τ*) (S2b) | bias at τ* |",
         "|---|---|---|---|---|---|---|---|"]
    for s in SEEDS:
        p = per[s]
        L.append(f"| {s} | {p['tau_star']:.1f} | {p['auc_chi3']:.3f} | {p['auc_chi1']:.3f} | "
                 f"{p['median_chi3']['rock']:.4f} / {p['median_chi3']['oscillator']:.4f} | {p['auc_own_unstratified']:.3f} | "
                 f"{p['auc_C_ref']:.3f} | {p['null_tau_median']:.4f} |")
    L += ["", f"Description: mean AUC at the own lag V/2 {desc['auc_own_mean']:.3f}. Mean AUC of C(τ*) in S2b "
          f"{desc['auc_C_ref_mean']:.3f}. Time {desc['seconds'] / 60:.0f} min."]
    (RES / "e26_c2_rocks.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
