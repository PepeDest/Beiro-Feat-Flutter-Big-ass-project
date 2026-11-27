"""Niche H, step H3 (docs/H.md): a search for systems with S_Z > q_X (H3a) or I_s > q_X (H3b). Rules fixed before
this run. Uses the functions of e31_h_energy.py.

    python experiments/e31b_h3_search.py
"""
import json, sys, time
from multiprocessing import Pool
import numpy as np
from scipy.optimize import minimize
from common import RES, save_json
import e31_h_energy as e
from vlife.gaussian import stationary_cov

LO, HI = np.log(1e-3), np.log(1e3)
G4 = None


def base_system(fam, i):
    return e.family_h()[i] if fam == "H" else e.draw_r(i)


def pack(sy):
    """Free parameters of docs/H.md, H3: log|B_xx entries| (signs fixed), log D_ii of the agent, log T_h."""
    B, D, X, s, h = sy["B"], sy["D"], sy["X"], sy["s"], sy["h"]
    ent = [(a, b) for a in X for b in X if B[a, b] != 0 and not (a == s and b == s)]
    sign = np.array([np.sign(B[a, b]) for a, b in ent])
    th = np.concatenate([[np.log(B[s, s])], np.log(np.abs([B[a, b] for a, b in ent])),
                         np.log(np.diag(D)[X]), [np.log(1 / B[h, h])]])
    return th, ent, sign


def unpack(sy, th, ent, sign):
    th = np.clip(th, LO, HI)
    B, D = sy["B"].copy(), sy["D"].copy()
    X, s, h = sy["X"], sy["s"], sy["h"]
    k = np.exp(th[0]); B[s, s] = k; B[s, h] = -k
    n = len(ent)
    for (a, b), sg, t in zip(ent, sign, th[1:1 + n]):
        B[a, b] = sg * np.exp(t)
    for j, a in enumerate(X):
        D[a, a] = np.exp(th[1 + n + j])
    T_h = np.exp(th[-1]); B[h, h] = D[h, h] = 1 / T_h
    out = dict(sy); out.update(B=B, D=D)
    if np.linalg.eigvals(B[np.ix_(X, X)]).real.min() < 0.01:
        return None
    out["S"] = stationary_cov(B, D)
    return out


def ratio(sy, which, grid):
    r = e.thermo_fast(sy)
    if which == "SZ":
        num = e.solve(sy, grid, "Z")[1]
    else:
        num = r["Is_closed"]
    return num / r["q_X"]


def search(job):
    fam, i, which = job
    grid = e.Grid(4000)
    sy0 = base_system(fam, i)
    th0, ent, sign = pack(sy0)

    def f(th):
        sy = unpack(sy0, th, ent, sign)
        if sy is None:
            return 1e6
        try:
            return -ratio(sy, which, grid)
        except Exception:
            return 1e6
    res = minimize(f, th0, method="Nelder-Mead", options=dict(maxfev=600, xatol=1e-6, fatol=1e-10))
    th = np.clip(res.x, LO, HI)
    return dict(fam=fam, i=i, which=which, start=-f(th0), best=-res.fun, theta=th.tolist(), nfev=int(res.nfev),
                at_limit=bool(np.any(np.isclose(th, LO, atol=1e-3) | np.isclose(th, HI, atol=1e-3))))


def confirm(rec):
    sy0 = base_system(rec["fam"], rec["i"])
    _, ent, sign = pack(sy0)
    sy = unpack(sy0, np.array(rec["theta"]), ent, sign)
    r = e.thermo(sy)
    gf = e.Grid(200_000, 1e-8, 1e6)
    SZ = e.solve(sy, gf, "Z")[1]
    rel = lambda a, b: abs(a - b) / max(abs(a), abs(b), 1e-300)
    checks = dict(H1a=bool(rel(r["l_X"], r["l_X_deriv"]) < 1e-6), H1b=bool(rel(r["Tdot"], r["Tdot_spec"]) < 1e-6),
                  H1c=bool(r["q_X"] >= r["l_X"] >= 0 and r["l_X"] <= r["Tdot"] * (1 + 1e-9) and SZ <= r["Is_closed"]
                           * (1 + 1e-6) and abs(r["sigma_X"] + r["sigma_h"] - r["sigma"]) < 1e-9 * r["sigma"]))
    num = SZ if rec["which"] == "SZ" else r["Is_closed"]
    return dict(ratio_fine=num / r["q_X"], S_Z=SZ, I_s=r["Is_closed"], q_X=r["q_X"], q_s=r["q_s"], l_X=r["l_X"],
                Tdot=r["Tdot"], checks=checks, B=sy["B"].tolist(), D=np.diag(sy["D"]).tolist())


def main():
    t0 = time.time()
    rows = json.load(open(RES / "e31_h_energy.json"))["rows"]
    pick = lambda F, n: [r["i"] for r in sorted([r for r in rows if r["fam"] == F],
                                                  key=lambda r: -r["S_Z"] / r["q_X"])[:n]]
    starts = [("R", i) for i in pick("R", 40)] + [("H", i) for i in pick("H", 8)]
    jobs = [(F, i, w) for w in ("SZ", "Is") for F, i in starts]
    with Pool(4) as p:
        recs = p.map(search, jobs, chunksize=1)
    out, v = dict(), dict()
    for w, rule in (("SZ", "H3a"), ("Is", "H3b")):
        rr = sorted([r for r in recs if r["which"] == w], key=lambda r: -r["best"])
        best = rr[0]
        c = confirm(best)
        ok = c["ratio_fine"] > 1 and all(c["checks"].values())
        v[rule] = "counterexample" if ok else "none found"
        out[rule] = dict(best=best, confirm=c, n_above_1=int(sum(r["best"] > 1 for r in rr)),
                         top5=[(r["fam"], r["i"], r["start"], r["best"], r["at_limit"]) for r in rr[:5]])
    out.update(verdicts=v, seconds=time.time() - t0, all=recs)
    save_json("e31b_h3_search.json", out)
    L = ["# E31b: search for a counterexample to H2a (niche H, step H3)", "", "Rules: docs/H.md, H3.", "",
         "| Rule | Best ratio (search grid) | Fine grid | Starts above 1 | Start | At a limit | Checks | Verdict |",
         "|---|---|---|---|---|---|---|---|"]
    for rule in ("H3a", "H3b"):
        o = out[rule]; b = o["best"]; c = o["confirm"]
        L.append(f"| {rule} | {b['best']:.4f} ({b['fam']} {b['i']}, from {b['start']:.4f}) | {c['ratio_fine']:.4f} | "
                 f"{o['n_above_1']} of {len(starts)} | {b['fam']} {b['i']} | {b['at_limit']} | "
                 f"{'pass' if all(c['checks'].values()) else 'fail'} | {v[rule]} |")
    for rule in ("H3a", "H3b"):
        c = out[rule]["confirm"]
        L.append(f"- {rule} best point: S_Z {c['S_Z']:.4g}, İ_s {c['I_s']:.4g}, q_X {c['q_X']:.4g}, q_s {c['q_s']:.4g}, "
                 f"l_X {c['l_X']:.4g}, Ṫ {c['Tdot']:.4g}.")
    L.append(f"- Time {out['seconds']:.0f} s.")
    (RES / "e31b_h3_search.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
