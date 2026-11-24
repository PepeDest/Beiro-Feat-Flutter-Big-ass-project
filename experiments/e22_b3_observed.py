"""Niche B, step B3 (docs/B.md): observed semantic information of KolchinskyWolpert18 (Sec. V B) in discrete-time
linear Gaussian systems, and its link to the directed information of TanakaEsfahaniMitter18.

Group D1: dx = 1, dy = 2, seeds 501-540. Group D2: dx = 2, dy = 2, seeds 601-630. tau = 4 steps.
Rules (sanity A, sanity T1, H1-H4) and the expectations are in docs/B.md (fixed before this script ran).
"""
import json, pathlib, sys, time
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vlife.semantic_dynamic import (stationary_cov_discrete, sensor, viability, transfer_entropy,  # noqa: E402
                                    information_measures, min_observed, projection_sensors_dy2)

TAU, MIN_DV, N_STARTS, S_MAX_DT, N_RANDOM = 4, 1e-3, 24, 1 - 1e-6, 20
N_STARTS_DT, MAXITER_DT, S_ATTAINED = 8, 100, 1 - 1e-3   # DT is slow near s = 1 (docs/B.md, B3)


def system(seed, dx, dy):
    rng = np.random.default_rng(seed); n = dx + dy
    A = rng.normal(size=(n, n))
    F = 0.85 * A / np.max(np.abs(np.linalg.eigvals(A)))
    W = np.diag(rng.uniform(0.3, 1.5, n))
    return F, W


def row(seed, dx, dy):
    F, W = system(seed, dx, dy)
    S0 = stationary_cov_discrete(F, W)
    I, O = np.eye(dy), np.zeros((dy, dy))
    V_act, V_full = viability(F, W, dx, I, O, TAU, S0), viability(F, W, dx, O, I, TAU, S0)
    rng = np.random.default_rng([seed, 11])
    # sanity A: tau = 1 does not depend on the sensor
    V1 = viability(F, W, dx, I, O, 1, S0)
    sanA = max(abs(viability(F, W, dx, *sensor(rng.uniform(-np.pi, np.pi, 1), rng.uniform(0, 1, dy)), 1, S0) - V1)
               for _ in range(5))
    TE_act, DI_act, _ = information_measures(F, W, dx, I, O, TAU, S0)
    r = dict(seed=seed, dx=dx, dV=float(V_act - V_full), TE_act=float(TE_act), DI_act=float(DI_act),
             sanityA=float(sanA))
    if abs(r["dV"]) < MIN_DV:
        r["skipped"] = True
        return r
    out = {}
    for obj in ("te", "di", "dt"):
        dt = obj == "dt"
        best, arg, n_best, n_feas = min_observed(F, W, dx, TAU, obj, N_STARTS_DT if dt else N_STARTS,
                                                 np.random.default_rng([seed, 7]), s_max=S_MAX_DT if dt else 1.0,
                                                 maxiter=MAXITER_DT if dt else 300)
        out[obj] = (best, arg)
        r[f"S_{obj}"] = None if best is None else float(best)
        r[f"nbest_{obj}"], r[f"nfeas_{obj}"] = int(n_best), int(n_feas)
        if arg is not None:
            r[f"arg_{obj}"] = [list(map(float, arg[0])), list(map(float, arg[1]))]
    roots = projection_sensors_dy2(F, W, dx, TAU)
    r["n_proj_roots"] = len(roots)
    r["S_proj"] = float(min([TE_act] + [te for _, te in roots]))
    # points for T1 (DI <= TE) and H3 (TE <= DT): random noisy sensors and the optima
    pts = [sensor(rng.uniform(-np.pi, np.pi, 1), rng.uniform(0, S_MAX_DT, dy)) for _ in range(N_RANDOM)]
    for obj in ("te", "di", "dt"):
        if out[obj][1] is not None:
            pts.append(sensor(*out[obj][1]))
    t1, h3 = [], []
    for K, SN in pts:
        te, di, dt = information_measures(F, W, dx, K, SN, TAU, S0)
        t1.append(te - di)
        if np.isfinite(dt):
            h3.append(dt - te)
    r["min_TE_minus_DI"] = float(min(t1)); r["min_DT_minus_TE"] = float(min(h3)); r["n_h3_points"] = len(h3)
    r["DT_attained"] = bool(out["dt"][1] is not None and max(out["dt"][1][1]) <= S_ATTAINED)
    if out["dt"][1] is not None:
        te_at_dt = information_measures(F, W, dx, *sensor(*out["dt"][1]), TAU, S0)[0]
        r["TE_at_DT_opt"] = float(te_at_dt)
    return r


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    t0 = time.time(); rows = []
    for dx, seeds in ((1, range(501, 541)), (2, range(601, 631))):
        for s in seeds:
            rows.append(row(s, dx, 2))
            print(f"system {s} (dx = {dx}): done, {time.time() - t0:.0f} s", flush=True)

    sanA_ok = all(r["sanityA"] < 1e-10 for r in rows)
    U = [r for r in rows if not r.get("skipped")]
    t1_ok = all(r["min_TE_minus_DI"] >= -1e-10 for r in U)
    h1_fail = [r["seed"] for r in U if r["S_proj"] - r["S_te"] > 1e-4]
    h2_fail = [r["seed"] for r in U if not r["S_te"] < r["TE_act"] - 1e-4]
    h3_fail = [r["seed"] for r in U if r["min_DT_minus_TE"] < -1e-10]
    h4_none = [r["seed"] for r in U if not r["DT_attained"]]                # D_T* = infinity: not equal
    h4_fail = [r["seed"] for r in U if r["DT_attained"] and r["S_dt"] - r["S_te"] > 1e-4]
    if not h4_fail and not h4_none:
        statement = "equal: D_T* = S_TE"
    elif not h3_fail:
        statement = "a bound: S_DI <= S_TE <= D_T*, not equal"
    else:
        statement = "false as a bound: TE > DT at some sensors"
    verdict = dict(
        sanityA="pass" if sanA_ok else "fail: the recursion is not valid",
        sanityT1="pass" if t1_ok else "fail: DI > TE somewhere, the code or the proof is wrong",
        H1="projections suffice" if not h1_fail else f"fails in {len(h1_fail)} of {len(U)} systems",
        H2="the actual sensor is never optimal" if not h2_fail else f"fails in {len(h2_fail)} of {len(U)} systems",
        H3="TE <= DT at all tested sensors" if not h3_fail else f"fails in {len(h3_fail)} of {len(U)} systems",
        H4="D_T* = S_TE" if not (h4_fail or h4_none) else
           f"fails in {len(h4_fail) + len(h4_none)} of {len(U)} systems ({len(h4_none)} with D_T* not attained)",
        statement=statement)
    out = ROOT / "results"
    json.dump(dict(verdict=verdict, rows=rows, h1_fail=h1_fail, h2_fail=h2_fail, h3_fail=h3_fail, h4_fail=h4_fail,
                   h4_none=h4_none), open(out / "e22_b3_observed.json", "w"), indent=1)
    eff = [r["S_te"] / r["TE_act"] for r in U]
    L = ["# E22: observed semantic information in discrete-time linear Gaussian systems (niche B, step B3)", "",
         "Rules: docs/B.md, B3.", "",
         f"Sanity A (tau = 1 does not depend on the sensor): {verdict['sanityA']}, largest gap "
         f"{max(r['sanityA'] for r in rows):.2e} nats.",
         f"Sanity T1 (DI <= TE): {verdict['sanityT1']}.", "",
         "| Rule | Question | Verdict | Systems |", "|---|---|---|---|",
         f"| H1 | Do deterministic coarse-grainings reach the minimum, S_proj = S_TE? | {verdict['H1']} | {len(U)} (skipped {len(rows) - len(U)}) |",
         f"| H2 | Is the actual sensor not optimal, S_TE < TE_act? | {verdict['H2']} | {len(U)} |",
         f"| H3 | Is TE <= DT at every tested noisy sensor (so S_TE <= D_T*)? | {verdict['H3']} | {len(U)} |",
         f"| H4 | Is the minimum of DT equal to S_TE? | {verdict['H4']} | {len(U)} |", "",
         f"Statement for the roadmap: **{statement}**.", "",
         f"Description: semantic efficiency S_TE / TE_act: median {np.median(eff):.3f}, range {min(eff):.3f} to "
         f"{max(eff):.3f}.", "",
         "| Seed | dx | ΔV | TE_act | S_proj | S_TE | S_DI | D_T* | TE at the D_T* sensor | min (DT − TE) |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    f = lambda v: "none" if v is None else f"{v:.4f}"
    for r in U:
        dts = f(r['S_dt']) if r["DT_attained"] else "not attained"
        L.append(f"| {r['seed']} | {r['dx']} | {r['dV']:+.4f} | {r['TE_act']:.4f} | {r['S_proj']:.4f} | {f(r['S_te'])} | "
                 f"{f(r['S_di'])} | {dts} | {f(r.get('TE_at_DT_opt'))} | {r['min_DT_minus_TE']:+.4f} |")
    (out / "e22_b3_observed.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[:16]))


if __name__ == "__main__":
    main()
