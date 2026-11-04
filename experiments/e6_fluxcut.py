"""E6 / ROADMAP S2 - flux cut: rocks vs drive-sustained oscillators vs plain wells. Rules: docs/S2.md."""
import argparse, pickle, time
import numpy as np
from scipy.stats import spearmanr
from common import RES, save_json
from vlife.nonlinear import draw_units, initial, run, HDR, exit_times, Unit
from vlife.estimators import ksg_mi

N_HDR, N_START, N_PAIR, T_BURN, TAU, DT = 16000, 2000, 4000, 200.0, 1.0, 0.01


def run_unit(job):
    i, kind, p, seed, t_max = job[:5]; n_pair = job[5] if len(job) > 5 else N_PAIR
    u = Unit(kind, p); rng = np.random.default_rng([seed, i])
    x, v = initial(u, N_HDR + N_START + N_PAIR, rng); x, v = run(u, x, v, T_BURN, True, DT, rng)
    hdr = HDR(x[:N_HDR], v[:N_HDR])
    xs, vs = x[N_HDR:N_HDR + N_START], v[N_HDR:N_HDR + N_START]
    xp, vp = x[N_HDR + N_START:], v[N_HDR + N_START:]
    xq, vq = run(u, xp.copy(), vp.copy(), TAU, True, DT, rng)
    if n_pair > N_PAIR:     # phase D: extra pairs from their own random numbers; set, starts and V stay as before
        r2 = np.random.default_rng([seed, i, 5]); xe, ve = initial(u, n_pair - N_PAIR, r2); xe, ve = run(u, xe, ve, T_BURN, True, DT, r2)
        xeq, veq = run(u, xe.copy(), ve.copy(), TAU, True, DT, r2)
        xp, vp, xq, vq = np.concatenate([xp, xe]), np.concatenate([vp, ve]), np.concatenate([xq, xeq]), np.concatenate([vq, veq])
    C = ksg_mi(np.column_stack([xp, vp]), np.column_stack([xq, vq]), k=4)
    TC = ksg_mi(xp, vp, k=4)
    on = exit_times(u, xs.copy(), vs.copy(), hdr, True, DT, t_max, np.random.default_rng([seed, i, 7]))
    off = exit_times(u, xs.copy(), vs.copy(), hdr, False, DT, t_max, np.random.default_rng([seed, i, 7]))
    return dict(i=i, kind=kind, p=p, C=C, TC=TC, V_on=on[0], ev_on=on[1], nv=on[2], V_off=off[0], ev_off=off[1],
                power=u.drive_power(vp))


def auc(a, b):
    a, b = np.asarray(a), np.asarray(b)
    return float(((a[:, None] > b[None, :]).mean() + 0.5 * (a[:, None] == b[None, :]).mean()))


def strat_auc(score, logV, kind):
    m = kind != "well"; s, y, k = score[m], logV[m], kind[m]
    cuts = np.quantile(y, [1 / 3, 2 / 3]); b = np.digitize(y, cuts)
    vals = [auc(s[(b == j) & (k == "rock")], s[(b == j) & (k == "oscillator")]) for j in range(3)
            if ((b == j) & (k == "rock")).sum() >= 5 and ((b == j) & (k == "oscillator")).sum() >= 5]
    return (float(np.mean(vals)) if len(vals) >= 2 else np.nan), len(vals)


def analyse(rows, n_boot=1000):
    kind = np.array([r["kind"] for r in rows]); C = np.array([r["C"] for r in rows]); TC = np.array([r["TC"] for r in rows])
    logV = np.log([r["V_on"] for r in rows]); logR = logV - np.log([r["V_off"] for r in rows]); phi = C - 0.25 * TC
    idx = {k: np.where(kind == k)[0] for k in ("rock", "oscillator", "well")}
    rng = np.random.default_rng(0)

    def stats(ids):
        o = ids[kind[ids] == "oscillator"]
        return [float(np.median(logR[o])), strat_auc(C[ids], logV[ids], kind[ids])[0],
                strat_auc(phi[ids], logV[ids], kind[ids])[0], spearmanr(C[ids], logV[ids])[0]]
    pt = stats(np.arange(len(rows)))
    bs = np.array([stats(np.concatenate([rng.choice(v, len(v)) for v in idx.values()])) for _ in range(n_boot)])
    lo, hi = np.nanpercentile(bs, [2.5, 97.5], axis=0)
    ci = lambda j: [pt[j], float(lo[j]), float(hi[j])]
    F1, F2, F3, F4 = ci(0), ci(1), ci(2), ci(3)
    nb = strat_auc(C, logV, kind)[1]
    lab = lambda x: ("not testable" if nb < 2 else "C mislabels rocks" if x[1] > 0.5 else "C favours oscillators" if x[2] < 0.5 else "no difference")
    v = dict(F1="yes" if F1[1] > np.log(2) else "no", F2=lab(F2), F3=lab(F3).replace("C ", "Phi_TC "),
             F4="yes" if F4[1] > 0 else "no")
    v["Gate"] = "triggered: dissipation term mandatory" if v["F2"] == "C mislabels rocks" and v["F3"] == "Phi_TC mislabels rocks" else "not triggered"
    o = idx["oscillator"]
    desc = dict(n_bins=nb, auc_C_unstratified=auc(C[idx["rock"]], C[o]), auc_logV_unstratified=auc(logV[idx["rock"]], logV[o]),
                rho_C_logR_osc=float(spearmanr(C[o], logR[o])[0]),
                max_abs_logR_passive=float(np.max(np.abs(logR[kind != "oscillator"]))),
                median_power_osc=float(np.median([rows[j]["power"] for j in o])),
                logV_range={k: [float(logV[ix].min()), float(logV[ix].max())] for k, ix in idx.items()},
                C_median={k: float(np.median(C[ix])) for k, ix in idx.items()},
                min_exits_on=int(min(r["ev_on"] for r in rows)))
    return dict(F1=F1, F2=F2, F3=F3, F4=F4), v, desc


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=2026); ap.add_argument("--t_max", type=float, default=500.0)
    ap.add_argument("--workers", type=int, default=4); ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--n_pair", type=int, default=N_PAIR, help="pairs for C and TC (phase D: 16000)"); ap.add_argument("--tag", default="")
    a = ap.parse_args()
    units = draw_units(np.random.default_rng([a.seed, 99]))
    jobs = [(i, u.kind, u.p, a.seed, a.t_max, a.n_pair) for i, u in enumerate(units)]
    if a.pilot:
        jobs = [j for j in jobs if j[1] == "oscillator"][:6] + [j for j in jobs if j[1] == "rock"][:2]
    from concurrent.futures import ProcessPoolExecutor
    t0 = time.time()
    with ProcessPoolExecutor(a.workers) as ex:
        rows = list(ex.map(run_unit, jobs))
    print(f"simulation done in {time.time() - t0:.0f}s", flush=True)
    if a.pilot:
        L = ["# S2 pilot (auto-generated; plan in docs/S2.md)\n", "| kind | V_on | V_off | V_on/V_off | exits on/off |", "|---|---|---|---|---|"]
        L += [f"| {r['kind']} | {r['V_on']:.2f} | {r['V_off']:.2f} | {r['V_on'] / r['V_off']:.2f} | {r['ev_on']}/{r['ev_off']} |" for r in rows]
        (RES / "e6_pilot.md").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L))
    else:
        pickle.dump(rows, open(RES / f"e6_dataset{a.tag}.pkl", "wb"))
        res, v, desc = analyse(rows)
        save_json(f"e6_summary{a.tag}.json", dict(results=res, verdicts=v, description=desc))
        f = lambda x: f"{x[0]:+.3f} [{x[1]:+.3f}, {x[2]:+.3f}]"
        L = ["# E6 / S2 report (auto-generated; rules in docs/S2.md)\n", f"Units: {len(rows)}. Pairs for C and TC: {a.n_pair}.\n",
             "| Rule | Value [95% CI] | Verdict |", "|---|---|---|",
             f"| F1: median log(V_on/V_off), oscillators | {f(res['F1'])} (log 2 = 0.693) | {v['F1']} |",
             f"| F2: stratified AUC of C (rock > oscillator) | {f(res['F2'])} | {v['F2']} |",
             f"| F3: stratified AUC of Phi_TC | {f(res['F3'])} | {v['F3']} |",
             f"| Gate | | {v['Gate']} |",
             f"| F4: rho(C, log V_on), all units | {f(res['F4'])} | {v['F4']} |",
             "\nDescription only:"] + [f"- {k}: {val}" for k, val in desc.items()]
        (RES / f"e6_report{a.tag}.md").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L))
