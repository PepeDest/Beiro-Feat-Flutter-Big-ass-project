"""Niche A, step A5 part 1 (docs/A.md): controlled worlds WITHOUT the random rotation (Q = I), eta = 0.

Each oscillating pair is a known 2 x 2 block (coordinates 2k, 2k+1). A structure is "whole" if it is a union of whole
blocks (6 structures), else "cut" (56 structures).
Grid: omega in {0, 1, 2, 4}. 20 worlds, seeds [2028, k]. At eta = 0 and omega = 0, B = D = B_eq, so that run is the
reversible run for every omega. Common random numbers: one seed per world for every run of that world.
Rules W1, C1-C3, the sanity checks, the sensitivity run and the expectations are in docs/A.md (fixed before the run).
"""
import argparse, json, pathlib, pickle, sys, time
import numpy as np
from scipy.stats import spearmanr

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vlife.controlled import draw, matrices  # noqa: E402
from vlife.gaussian import cross_oscillation, oscillatory_nonnormal_ep  # noqa: E402
from vlife.functional import all_subsets  # noqa: E402
from vlife.viability import simulate_exits, mfpt_all  # noqa: E402

OMEGAS = (0.0, 1.0, 2.0, 4.0)
MARGIN = 0.05
SUBSETS = all_subsets(6)
WHOLE = np.array([all(((i ^ 1) in s) for i in s) for s in SUBSETS])     # i ^ 1 is the partner of i in its block


def run_world(k, seed, n_traj, dt, t_max, p_out, omegas=OMEGAS):
    w = draw(np.random.default_rng([seed, k])); w["Q"] = np.eye(6)
    sim = [seed, k, 1]
    B0, D, S = matrices(w, 0.0, 0.0)
    V_eq, ev_eq, _ = mfpt_all(simulate_exits(B0, S, SUBSETS, p_out, n_traj, dt, t_max, np.random.default_rng(sim), True))
    rows = []
    for om in omegas:
        B, D, S = matrices(w, om, 0.0)
        _, so, sn = oscillatory_nonnormal_ep(B, D, S)
        if om == 0.0:
            V_on, ev_on = V_eq, ev_eq
        else:
            V_on, ev_on, _ = mfpt_all(simulate_exits(B, S, SUBSETS, p_out, n_traj, dt, t_max, np.random.default_rng(sim), True))
        lam = np.array([np.trace(B[np.ix_(list(s), list(s))]) / len(s) for s in SUBSETS])
        xc = np.array([cross_oscillation(B, S, s) for s in SUBSETS]) / lam
        rows.append(dict(k=k, omega=om, sigma_osc=so, sigma_nn=sn, logR=np.log(V_on / V_eq),
                         ok=(ev_on >= 5) & (ev_eq >= 5), x_cross=xc, size=np.array([len(s) for s in SUBSETS])))
    return rows


def world_stats(rows):
    """Per world: W_omega and C_omega (mean log R of whole and cut structures) for omega 1, 2, 4, and the C3 rho."""
    by = {r["omega"]: r for r in rows}
    out = {}
    for om in OMEGAS[1:]:
        r = by[om]
        out[f"W_{om:g}"] = np.mean(r["logR"][WHOLE & r["ok"]])
        out[f"C_{om:g}"] = np.mean(r["logR"][~WHOLE & r["ok"]])
    r = by[4.0]; rho = []
    for k in range(1, 6):
        m = (r["size"] == k) & r["ok"]
        if m.sum() >= 5 and np.ptp(r["x_cross"][m]) > 0:
            rho.append(spearmanr(r["x_cross"][m], r["logR"][m])[0])
    out["C3"] = np.mean(rho)
    return out


def summary(ws):
    s = {q: np.mean([w[q] for w in ws]) for q in ws[0]}
    s["W1"] = np.mean([s["W_1"], s["W_2"], s["W_4"]])
    s["C2"] = s["C_4"] - s["C_1"]
    return s


def label(ci):
    if ci[1] < 0:
        return "shortens life"
    if ci[0] > 0:
        return "lengthens life"
    if -MARGIN <= ci[0] and ci[1] <= MARGIN:
        return f"no effect within +-{MARGIN}"
    return "inconclusive"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n_worlds", type=int, default=20)
    ap.add_argument("--n_traj", type=int, default=600)
    ap.add_argument("--dt", type=float, default=0.05)
    ap.add_argument("--t_max", type=float, default=200.0)
    ap.add_argument("--p_out", type=float, default=0.05)
    ap.add_argument("--seed", type=int, default=2028)
    ap.add_argument("--n_boot", type=int, default=2000)
    ap.add_argument("--sens_worlds", type=int, default=5)
    ap.add_argument("--sens_dt", type=float, default=0.01)
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    t0 = time.time(); rows = []
    for k in range(a.n_worlds):
        rows += run_world(k, a.seed, a.n_traj, a.dt, a.t_max, a.p_out)
        print(f"world {k}: done, {time.time() - t0:.0f} s", flush=True)
    sens = []
    for k in range(a.sens_worlds):                          # sensitivity (description only): smaller time step
        sens += run_world(k, a.seed, a.n_traj, a.sens_dt, a.t_max, a.p_out, omegas=(0.0, 4.0))
        print(f"sensitivity world {k}: done, {time.time() - t0:.0f} s", flush=True)
    out = ROOT / "results"
    pickle.dump(dict(rows=rows, sens=sens, args=vars(a)), open(out / "e18_unrotated.pkl", "wb"))

    checks = dict(
        y_zero_at_omega0=bool(all(np.all(r["logR"] == 0) for r in rows if r["omega"] == 0)),
        sigma_nn_zero=bool(all(abs(r["sigma_nn"]) < 1e-8 * (1 + r["sigma_osc"]) for r in rows)),
        n_whole=int(WHOLE.sum()), n_cut=int((~WHOLE).sum()),
        min_whole_ok=int(min((r["ok"] & WHOLE).sum() for r in rows)),
        min_cut_ok=int(min((r["ok"] & ~WHOLE).sum() for r in rows)))
    ws = [world_stats([r for r in rows if r["k"] == k]) for k in range(a.n_worlds)]
    point = summary(ws)
    rng = np.random.default_rng(2026); boots = {q: [] for q in point}
    for _ in range(a.n_boot):
        s = summary([ws[i] for i in rng.integers(0, len(ws), len(ws))])
        for q in s:
            boots[q].append(s[q])
    ci = {q: (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))) for q, v in boots.items()}
    verdict = {q: label(ci[q]) for q in ("W1", "W_1", "W_2", "W_4", "C_1", "C_2", "C_4", "C2", "C3")}
    sw = {r["k"]: r for r in sens if r["omega"] == 4.0}
    sens_d = dict(W_4=float(np.mean([np.mean(r["logR"][WHOLE & r["ok"]]) for r in sw.values()])),
                  C_4=float(np.mean([np.mean(r["logR"][~WHOLE & r["ok"]]) for r in sw.values()])),
                  C_4_main_same_worlds=float(np.mean([ws[k]["C_4"] for k in sw])),
                  W_4_main_same_worlds=float(np.mean([ws[k]["W_4"] for k in sw])))
    json.dump(dict(point={q: float(v) for q, v in point.items()}, ci=ci, verdict=verdict, checks=checks,
                   sensitivity=sens_d, args=vars(a)), open(out / "e18_unrotated.json", "w"), indent=1)
    names = dict(W1="whole: mean over ω 1, 2, 4", W_1="whole, ω 1", W_2="whole, ω 2", W_4="whole, ω 4", C_1="cut, ω 1",
                 C_2="cut, ω 2", C_4="cut, ω 4", C3="mean ρ(x_cross, log R) in world × size, ω 4")
    L = ["# E18: controlled worlds without rotation (niche A, step A5, part 1)", "",
         "Rules: docs/A.md. 95 % bootstrap intervals over worlds. Values are mean log R = log(V_on / V_eq).", "",
         f"Sanity checks: {checks}", "", "| Rule | Statistic | Value [95 % CI] | Verdict |", "|---|---|---|---|"]
    for q, rule in (("W1", "W1"), ("W_1", "W1"), ("W_2", "W1"), ("W_4", "W1"), ("C_1", "C1"), ("C_2", "C1"), ("C_4", "C1")):
        L.append(f"| {rule} | {names[q]} | {point[q]:+.3f} [{ci[q][0]:+.3f}, {ci[q][1]:+.3f}] | {verdict[q]} |")
    L.append(f"| C2 | C(ω 4) − C(ω 1) | {point['C2']:+.3f} [{ci['C2'][0]:+.3f}, {ci['C2'][1]:+.3f}] | {verdict['C2']} |")
    L.append(f"| C3 | {names['C3']} | {point['C3']:+.3f} [{ci['C3'][0]:+.3f}, {ci['C3'][1]:+.3f}] | {verdict['C3']} |")
    L += ["", f"Sensitivity (description only), worlds 0-{a.sens_worlds - 1}, dt {a.sens_dt}: {sens_d}"]
    (out / "e18_unrotated.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
