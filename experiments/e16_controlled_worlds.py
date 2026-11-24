"""Niche A, step A3 (docs/A.md): change one part of the dissipation at a time and measure the life.

Worlds: vlife.controlled (S = I, fixed spectrum r_k (1 +- i omega), coupling eta * U, random rotation Q).
Grid: omega in {0, 1, 2, 4}, eta in {0, 1/3, 2/3, 1} * eta_cap. 20 worlds, seeds [2027, k].
For each grid point: life of all 62 structures with the drive (V_on) and under the reversible dynamics with the same
stationary law (V_eq, B_eq = D because S = I). Common random numbers: one seed per world for every run of that world.
y = mean over structures (>= 5 exits in both runs) of log(V_on / V_eq).
Rules Q1-Q4, the sanity checks and the expectations are in docs/A.md (fixed before the run).
"""
import argparse, json, pathlib, pickle, sys, time
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vlife.controlled import draw, eta_cap, matrices  # noqa: E402
from vlife.gaussian import oscillatory_nonnormal_ep  # noqa: E402
from vlife.functional import all_subsets  # noqa: E402
from vlife.viability import simulate_exits, mfpt_all  # noqa: E402

OMEGAS = (0.0, 1.0, 2.0, 4.0)
ETA_FRACS = (0.0, 1 / 3, 2 / 3, 1.0)
MARGIN = 0.05


def run_world(k, seed, n_traj, dt, t_max, p_out):
    w = draw(np.random.default_rng([seed, k]))
    ec = eta_cap(w)
    subsets = all_subsets(6)
    sim = [seed, k, 1]
    eq = {}
    for fi, f in enumerate(ETA_FRACS):              # B_eq = D depends on eta only
        _, D, S = matrices(w, 0.0, f * ec)
        eq[fi] = mfpt_all(simulate_exits(D, S, subsets, p_out, n_traj, dt, t_max, np.random.default_rng(sim), True))
    out = []
    for oi, om in enumerate(OMEGAS):
        for fi, f in enumerate(ETA_FRACS):
            B, D, S = matrices(w, om, f * ec)
            s, so, sn = oscillatory_nonnormal_ep(B, D, S)
            V_on, ev_on, _ = mfpt_all(simulate_exits(B, S, subsets, p_out, n_traj, dt, t_max, np.random.default_rng(sim), True))
            V_eq, ev_eq, _ = eq[fi]
            m = (ev_on >= 5) & (ev_eq >= 5)
            logR = np.log(V_on / V_eq)
            out.append(dict(k=k, omega=om, eta_frac=f, eta=f * ec, sigma=s, sigma_osc=so, sigma_nn=sn,
                            y=float(np.mean(logR[m])) if m.any() else np.nan, n_struct=int(m.sum()),
                            y_all=float(np.mean(logR)), lam_bar=float(np.mean(w["r"]))))
    return out


def table(rows):
    """y as an array (world, omega index, eta index)."""
    ks = sorted({r["k"] for r in rows})
    Y = np.full((len(ks), len(OMEGAS), len(ETA_FRACS)), np.nan)
    for r in rows:
        Y[ks.index(r["k"]), OMEGAS.index(r["omega"]), [i for i, f in enumerate(ETA_FRACS) if np.isclose(f, r["eta_frac"])][0]] = r["y"]
    return Y


def contrasts(Y):
    d_osc = Y[:, 3, 0] - Y[:, 0, 0]                     # Q1: omega 4 against 0, eta 0
    d_nn0 = Y[:, 0, 3] - Y[:, 0, 0]                     # Q2: eta_cap against 0, omega 0
    d_nnw = np.mean(Y[:, 1:, 3] - Y[:, 1:, 0], axis=1)  # Q3: eta_cap against 0, mean over omega 1, 2, 4
    return dict(Q1=d_osc, Q2=d_nn0, Q3=d_nnw)


def summary(Y):
    c = contrasts(Y)
    return dict(Q1=np.mean(c["Q1"]), Q2=np.mean(c["Q2"]), Q3=np.mean(c["Q3"]),
                Q4=abs(np.mean(c["Q1"])) - abs(np.mean(c["Q3"])))


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
    ap.add_argument("--seed", type=int, default=2027)
    ap.add_argument("--n_boot", type=int, default=2000)
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    t0 = time.time(); rows = []
    for k in range(a.n_worlds):
        rows += run_world(k, a.seed, a.n_traj, a.dt, a.t_max, a.p_out)
        print(f"world {k}: done, {time.time() - t0:.0f} s", flush=True)
    out = ROOT / "results"
    pickle.dump(dict(rows=rows, args=vars(a)), open(out / f"e16_controlled{a.tag}.pkl", "wb"))

    # sanity checks (docs/A.md): they must pass, else the run is not valid
    Y = table(rows)
    ref = [r for r in rows if r["omega"] == 0 and r["eta_frac"] == 0]
    checks = dict(
        y_zero_at_equilibrium=bool(all(abs(r["y_all"]) < 1e-12 for r in ref)),
        sigma_osc_fixed_in_eta=bool(all(np.ptp([r["sigma_osc"] for r in rows if r["k"] == k and r["omega"] == om]) < 1e-8 * (1 + max(abs(r["sigma_osc"]) for r in rows if r["k"] == k and r["omega"] == om))
                                        for k in range(a.n_worlds) for om in OMEGAS)),
        sigma_nn_zero_at_eta0=bool(all(abs(r["sigma_nn"]) < 1e-8 * (1 + r["sigma"]) for r in rows if r["eta_frac"] == 0)),
        min_structures=int(min(r["n_struct"] for r in rows)))

    point = summary(Y)
    rng = np.random.default_rng(2026); boots = {q: [] for q in point}
    for _ in range(a.n_boot):
        s = summary(Y[rng.integers(0, len(Y), len(Y))])
        for q in s:
            boots[q].append(s[q])
    ci = {q: (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))) for q, v in boots.items()}
    verdict = {q: label(ci[q]) for q in ("Q1", "Q2", "Q3")}
    verdict["Q4"] = "oscillation dominates" if ci["Q4"][0] > 0 else "not separated"
    json.dump(dict(point=point, ci=ci, verdict=verdict, checks=checks, mean_y=np.nanmean(Y, 0).tolist(),
                   omegas=OMEGAS, eta_fracs=ETA_FRACS, args=vars(a)), open(out / f"e16_controlled{a.tag}.json", "w"), indent=1)
    L = ["# E16: controlled worlds (niche A, step A3)", "", "Rules: docs/A.md. 95 % bootstrap intervals over worlds.", "",
         f"Sanity checks: {checks}", "", "| Rule | Contrast | Value [95 % CI] | Verdict |", "|---|---|---|---|"]
    names = dict(Q1="y(ω 4, η 0) − y(ω 0, η 0)", Q2="y(ω 0, η cap) − y(ω 0, η 0)",
                 Q3="y(ω, η cap) − y(ω, η 0), mean over ω 1, 2, 4", Q4="|Q1| − |Q3|")
    for q in ("Q1", "Q2", "Q3", "Q4"):
        L.append(f"| {q} | {names[q]} | {point[q]:+.3f} [{ci[q][0]:+.3f}, {ci[q][1]:+.3f}] | {verdict[q]} |")
    L += ["", "Mean y over worlds (rows ω, columns η / η_cap):", "", "| ω | " + " | ".join(f"{f:.2f}" for f in ETA_FRACS) + " |",
          "|---|" + "---|" * len(ETA_FRACS)]
    for oi, om in enumerate(OMEGAS):
        L.append(f"| {om:g} | " + " | ".join(f"{v:+.3f}" for v in np.nanmean(Y[:, oi, :], 0)) + " |")
    (out / f"e16_controlled{a.tag}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
