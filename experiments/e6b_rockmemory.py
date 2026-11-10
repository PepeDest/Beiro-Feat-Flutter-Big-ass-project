"""E6b / S2b - sharper rock test: well-based and cycle-based viability, C at a long lag tau*. Rules: docs/S2.md (S2b)."""
import argparse, os, pickle, time
import numpy as np
from scipy.stats import spearmanr
from common import RES, save_json
from vlife.nonlinear import draw_units, initial, run, Unit, alive_rule, exit_times_rule
from vlife.estimators import ksg_mi

N_START, N_PAIR, T_BURN = 2000, 4000, 200.0
DT = float(os.environ.get("VLIFE_S2_DT", "0.01"))      # night item 8b: VLIFE_S2_DT=0.005 halves the step (default 0.01)


def burn(u, n, rng):
    x, v = initial(u, n, rng); return run(u, x, v, T_BURN, True, DT, rng)


def job_V(job):
    i, kind, p, seed, t_max = job
    u = Unit(kind, p); rng = np.random.default_rng([seed, i, 21])
    x, v = burn(u, N_START + N_PAIR, rng)
    E_cyc = float(np.median(0.5 * v * v + 0.5 * p["omega0"] ** 2 * x * x)) if kind == "oscillator" else None
    xs, vs = x[:N_START], v[:N_START]
    valid, fn = alive_rule(u, xs, vs, E_cyc)
    on = exit_times_rule(u, xs.copy(), vs.copy(), valid, fn, True, DT, t_max, np.random.default_rng([seed, i, 22]))
    off = on if kind == "rock" else exit_times_rule(u, xs.copy(), vs.copy(), valid, fn, False, DT, t_max, np.random.default_rng([seed, i, 22]))
    return dict(i=i, kind=kind, p=p, E_cyc=E_cyc, V_on=on[0], ev_on=on[1], nv=on[2], V_off=off[0], ev_off=off[1])


def job_C(job):
    i, kind, p, seed, tau_star, tau_own = job[:6]; n_pair = job[6] if len(job) > 6 else N_PAIR
    u = Unit(kind, p); rng = np.random.default_rng([seed, i, 23])
    x, v = burn(u, N_PAIR, rng)
    if n_pair > N_PAIR:     # phase D: extra pairs from their own random numbers
        r2 = np.random.default_rng([seed, i, 24]); xe, ve = burn(u, n_pair - N_PAIR, r2)
        x, v = np.concatenate([x, xe]), np.concatenate([v, ve])
    z0 = np.column_stack([x, v])
    TC = ksg_mi(x, v, k=4)
    out = {"i": i, "TC": TC}
    for name, tau in (("C_star", tau_star), ("C_own", tau_own)):
        xq, vq = run(u, x.copy(), v.copy(), tau, True, DT, rng)
        out[name] = ksg_mi(z0, np.column_stack([xq, vq]), k=4)
    return out


def auc(a, b):
    a, b = np.asarray(a), np.asarray(b)
    return float(((a[:, None] > b[None, :]).mean() + 0.5 * (a[:, None] == b[None, :]).mean()))


def strat_auc(s, y, k):
    cuts = np.quantile(y, [1 / 3, 2 / 3]); b = np.digitize(y, cuts)
    vals = [auc(s[(b == j) & (k == "rock")], s[(b == j) & (k == "oscillator")]) for j in range(3)
            if ((b == j) & (k == "rock")).sum() >= 5 and ((b == j) & (k == "oscillator")).sum() >= 5]
    return (float(np.mean(vals)) if len(vals) >= 2 else np.nan), len(vals)


def analyse(rows):
    kind = np.array([r["kind"] for r in rows]); lV = np.log([r["V_on"] for r in rows])
    lR = lV - np.log([r["V_off"] for r in rows]); C = np.array([r["C_star"] for r in rows])
    phi = C - 0.25 * np.array([r["TC"] for r in rows]); h = np.array([r["p"].get("h", np.nan) for r in rows])
    idx = {k: np.where(kind == k)[0] for k in ("rock", "oscillator")}; rng = np.random.default_rng(0)

    def stats(ids):
        rk, os_ = ids[kind[ids] == "rock"], ids[kind[ids] == "oscillator"]
        return [spearmanr(h[rk], lV[rk])[0], float(np.median(lR[os_])), strat_auc(C[ids], lV[ids], kind[ids])[0],
                strat_auc(phi[ids], lV[ids], kind[ids])[0], spearmanr(C[rk], lV[rk])[0]]
    pt = stats(np.arange(len(rows)))
    bs = np.array([stats(np.concatenate([rng.choice(v, len(v)) for v in idx.values()])) for _ in range(1000)])
    lo, hi = np.nanpercentile(bs, [2.5, 97.5], axis=0); ci = lambda j: [float(pt[j]), float(lo[j]), float(hi[j])]
    G0, G1, G2, G3, G4 = (ci(j) for j in range(5))
    nb = strat_auc(C, lV, kind)[1]
    lab = lambda x, w: ("not testable" if nb < 2 else f"{w} mislabels rocks" if x[1] > 0.5 else f"{w} favours oscillators" if x[2] < 0.5 else "no difference")
    v = dict(G0="valid" if G0[1] > 0 else "not valid", G1="yes" if G1[1] > np.log(2) else "no", G2=lab(G2, "C"),
             G3=lab(G3, "Phi_TC"), G4="yes" if G4[1] > 0 else "no")
    v["Gate"] = "triggered: dissipation term mandatory" if v["G2"].endswith("mislabels rocks") and v["G3"].endswith("mislabels rocks") else "not triggered"
    Cown = np.array([r["C_own"] for r in rows])
    desc = dict(n_bins=nb, auc_C_unstratified=auc(C[idx["rock"]], C[idx["oscillator"]]),
                auc_logV_unstratified=auc(lV[idx["rock"]], lV[idx["oscillator"]]),
                auc_C_own_lag=auc(Cown[idx["rock"]], Cown[idx["oscillator"]]),
                C_star_median={k: float(np.median(C[ix])) for k, ix in idx.items()},
                logV_range={k: [float(lV[ix].min()), float(lV[ix].max())] for k, ix in idx.items()},
                min_exits=int(min(r["ev_on"] for r in rows)), n_censored_lt5=int(sum(r["ev_on"] < 5 for r in rows)))
    return dict(G0=G0, G1=G1, G2=G2, G3=G3, G4=G4), v, desc


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=2026); ap.add_argument("--t_max", type=float, default=3000.0)
    ap.add_argument("--workers", type=int, default=4); ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--n_pair", type=int, default=N_PAIR, help="pairs for C and TC (phase D: 16000)"); ap.add_argument("--tag", default="")
    a = ap.parse_args()
    units = [(i, u) for i, u in enumerate(draw_units(np.random.default_rng([a.seed, 99]))) if u.kind != "well"]
    if a.pilot:
        rocks = sorted([t for t in units if t[1].kind == "rock"], key=lambda t: t[1].p["h"])
        units = rocks[:2] + rocks[-2:] + [t for t in units if t[1].kind == "oscillator"][:4]
    from concurrent.futures import ProcessPoolExecutor
    t0 = time.time()
    with ProcessPoolExecutor(a.workers) as ex:
        rows = list(ex.map(job_V, [(i, u.kind, u.p, a.seed, a.t_max) for i, u in units]))
    print(f"V phase done in {time.time() - t0:.0f}s", flush=True)
    if a.pilot:
        L = ["# S2b pilot (V only; plan in docs/S2.md)\n", "| kind | h or (omega0, v0) | V_on | V_off | exits on |", "|---|---|---|---|---|"]
        L += [f"| {r['kind']} | {r['p'].get('h', (round(r['p'].get('omega0', 0), 2), round(r['p'].get('v0', 0), 2)))} | {r['V_on']:.1f} | {r['V_off']:.1f} | {r['ev_on']} |" for r in rows]
        (RES / "e6b_pilot.md").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L))
    else:
        tau_star = float(np.median([r["V_on"] for r in rows if r["kind"] == "rock"]))
        print(f"tau* = {tau_star:.2f} (median rock V, fixed before any C)", flush=True)
        t0 = time.time()
        with ProcessPoolExecutor(a.workers) as ex:
            cs = list(ex.map(job_C, [(r["i"], r["kind"], r["p"], a.seed, tau_star, min(r["V_on"] / 2, a.t_max / 2), a.n_pair) for r in rows]))
        print(f"C phase done in {time.time() - t0:.0f}s", flush=True)
        for r, c in zip(rows, cs):
            r.update(c)
        pickle.dump(dict(rows=rows, tau_star=tau_star, n_pair=a.n_pair, dt=DT), open(RES / f"e6b_dataset{a.tag}.pkl", "wb"))
        res, v, desc = analyse(rows)
        save_json(f"e6b_summary{a.tag}.json", dict(tau_star=tau_star, results=res, verdicts=v, description=desc))
        f = lambda x: f"{x[0]:+.3f} [{x[1]:+.3f}, {x[2]:+.3f}]"
        L = ["# E6b / S2b report (auto-generated; rules in docs/S2.md)\n", f"Units: {len(rows)}. tau* = {tau_star:.2f}. Pairs for C and TC: {a.n_pair}. dt = {DT}.\n",
             "| Rule | Value [95% CI] | Verdict |", "|---|---|---|",
             f"| G0: rho(h, log V), rocks | {f(res['G0'])} | {v['G0']} |",
             f"| G1: median log(V_on/V_off), oscillators | {f(res['G1'])} | {v['G1']} |",
             f"| G2: stratified AUC of C(tau*) | {f(res['G2'])} | {v['G2']} |",
             f"| G3: stratified AUC of Phi_TC | {f(res['G3'])} | {v['G3']} |",
             f"| Gate | | {v['Gate']} |",
             f"| G4: rho(C(tau*), log V), rocks | {f(res['G4'])} | {v['G4']} |",
             "\nDescription only:"] + [f"- {k}: {val}" for k, val in desc.items()]
        (RES / f"e6b_report{a.tag}.md").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L))
