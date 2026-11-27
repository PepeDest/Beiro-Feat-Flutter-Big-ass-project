"""Niche D (docs/D.md): the foraging agent of Sowinski23 (D1) and the Kuramoto agent of SowinskiFrankGhoshal24 (D2),
with the zero-information controls (D3). Rules and expectations are in docs/D.md (fixed before any run).

The heavy part runs on the Xeon machines through cluster/run_cluster.py, which calls tasks() and run_task().
analyze(out_dir) reads the task files and writes results/e27_d_rochester.{json,md}.
"""
import json, pathlib, sys
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vlife.rochester import (forager_batch, forager_eta_grid, seeds_for, kuramoto_run, graph_csr)  # noqa: E402

N_BOOT = 1000
# D1 sets: id -> (v, R, runs for each eta, mode). Mode 0 normal, 1 deaf (eta not used).
D1_SETS = {0: (20.0, 4.0, 100_000, 0), 1: (5.0, 4.0, 10_000, 0), 2: (10.0, 4.0, 10_000, 0), 3: (15.0, 4.0, 10_000, 0),
           4: (25.0, 4.0, 10_000, 0), 5: (30.0, 4.0, 10_000, 0), 6: (20.0, 2.0, 10_000, 0), 7: (20.0, 8.0, 10_000, 0)}
D1_DEAF = {10 + k: (v, 4.0, 10_000, 1) for k, v in enumerate((5.0, 10.0, 15.0, 20.0, 25.0, 30.0))}
# D2: topology -> (N, coupling grid, runs with the agent, runs without, runs of the still agent)
D2_TOPO = {"fc": (1024, np.linspace(0.0, 4.0, 64), 128, 512, 32),
           "poisson": (1000, np.linspace(0.0, 1.0, 64), 64, 256, 32),
           "sf": (1000, np.linspace(0.0, 1.0, 64), 64, 256, 32)}
D2_ETA = np.linspace(0.0, 1.0, 32)
TOPO_ID = {"fc": 0, "poisson": 1, "sf": 2}
ALPHA, BETA = 0.5, 0.16


def tasks(smoke=False):
    """Each task: dict(job, name, cost) plus its parameters. cost is a rough number of seconds on one core."""
    out = []
    grid = forager_eta_grid()
    sets = {**D1_SETS, **D1_DEAF}
    for sid, (v, R, n, mode) in sets.items():
        if smoke:
            n = 40
        idx = [0] if mode == 1 else (range(0, 200, 25) if smoke else range(200))
        for k in idx:
            eta = float(grid[k])
            base = {5.0: 0.0006, 10.0: 0.001, 15.0: 0.0025, 20.0: 0.010, 25.0: 0.017, 30.0: 0.029}[v]  # s/run, test PC
            c = n * (base if eta < 0.1 else base / 3 if eta < 0.15 else 0.001)
            out.append(dict(job="d1", name=f"d1_s{sid}_e{k:03d}", sid=sid, k=k, v=v, R=R, eta=eta, n=n, mode=mode,
                            cost=c))
    for topo, (N, cg, n_ag, n_none, n_still) in D2_TOPO.items():
        if smoke:
            cg, n_ag, n_none, n_still = cg[::16], 2, 2, 2
        for ik, K in enumerate(cg):
            ik_full = ik * 16 if smoke else ik
            out.append(dict(job="d2", name=f"d2_{topo}_k{ik_full:02d}_none", topo=topo, ik=ik_full, K=float(K),
                            ie=-1, eta=0.0, agent=0, n=n_none, cost=n_none * 0.25))
            out.append(dict(job="d2", name=f"d2_{topo}_k{ik_full:02d}_still", topo=topo, ik=ik_full, K=float(K),
                            ie=-2, eta=0.0, agent=2, n=n_still, cost=n_still * 0.25))
            for ie, eta in enumerate(D2_ETA if not smoke else D2_ETA[::15]):
                ie_full = ie * 15 if smoke else ie
                out.append(dict(job="d2", name=f"d2_{topo}_k{ik_full:02d}_e{ie_full:02d}", topo=topo, ik=ik_full,
                                K=float(K), ie=ie_full, eta=float(eta), agent=1, n=n_ag, cost=n_ag * 0.27))
    return out


def run_task(t):
    if t["job"] == "d1":
        seeds = seeds_for((27, 1, t["sid"], t["k"]), t["n"])
        T, C, H, L = forager_batch(t["v"], t["R"], t["eta"], t["mode"], seeds)
        rng = np.random.default_rng([27, 2, t["sid"], t["k"]])
        boot = np.array([T[rng.integers(0, T.size, T.size)].mean() for _ in range(N_BOOT)])
        return dict(mean=float(T.mean()), se=float(T.std(ddof=1) / np.sqrt(T.size)), n=int(T.size),
                    censored=int(C.sum()), median=float(np.median(T)),
                    quantiles=np.quantile(T, [0.05, 0.25, 0.5, 0.75, 0.95]).tolist(),
                    harvest_mean=float(H.mean()), lock_mean=float(L.mean()), boot=boot.tolist())
    N = D2_TOPO[t["topo"]][0]
    fc = t["topo"] == "fc"
    r, info, nn = [], [], []
    dummy = np.zeros(1, np.int64)
    for j in range(t["n"]):
        key = (27, 3, TOPO_ID[t["topo"]], t["ik"], t["ie"] + 10, j)
        rng = np.random.default_rng(list(key))
        if fc:
            ip, ix, n_used, coup = dummy, dummy, N, t["K"] / N
        else:
            ip, ix, n_used = graph_csr(t["topo"], N, 4.0, rng)
            coup = t["K"]
        seed = int(seeds_for(key, 1)[0])
        rr, ii, _ = kuramoto_run(coup, fc, ip, ix, n_used, t["eta"], ALPHA, BETA, t["agent"], seed)
        r.append(float(rr)); info.append(float(ii)); nn.append(int(n_used))
    return dict(r=r, info=info, n_nodes=nn)


# ------------------------------------------------------------------ analysis
def _load(out_dir, job):
    res = {}
    for f in pathlib.Path(out_dir, job).glob("*.json"):
        d = json.loads(f.read_text())
        res[d["task"]["name"]] = d
    return res


def two_segment(x, y, n_b=600):
    """Continuous two-segment least-squares fit. Returns (break point, sse, coefficients)."""
    x, y = np.asarray(x), np.asarray(y)
    best = (None, np.inf, None)
    for b in np.linspace(x[2], x[-3], n_b):
        X = np.column_stack([np.ones_like(x), np.minimum(x, b), np.maximum(x - b, 0.0)])
        c, *_ = np.linalg.lstsq(X, y, rcond=None)
        sse = float(((X @ c - y) ** 2).sum())
        if sse < best[1]:
            best = (float(b), sse, c)
    return best


def expected_dilation(eta, r=1.0, y=4.0, n=4001):
    """E_eta[lambda] of Sowinski23 Eq. (D3), for 0 < eta <= eta_c."""
    ph = np.pi * eta
    th = np.linspace(0.0, ph, n)
    f = np.sqrt(np.maximum(1.0 - (y / r) ** 2 * np.sin(th) ** 2, 0.0))
    E = np.trapezoid(f, th)
    return r / y - 1.0 + np.sin(ph) / ph - (r / y) * E / ph


def analyze_d1(out_dir):
    res = _load(out_dir, "d1")
    grid = forager_eta_grid()
    sets = {}
    for sid in list(D1_SETS) + list(D1_DEAF):
        rows = {int(n.split("_e")[1]): d for n, d in res.items() if n.startswith(f"d1_s{sid}_")}
        if rows:
            sets[sid] = rows
    out, verdict = {}, {}
    s0 = 0.5
    for sid, rows in sets.items():
        if sid >= 10:
            continue
        v, R, n, _ = D1_SETS[sid]
        ks = sorted(rows)
        eta = grid[ks]; V = np.array([rows[k]["result"]["mean"] for k in ks]); SE = np.array([rows[k]["result"]["se"] for k in ks])
        B = np.array([rows[k]["result"]["boot"] for k in ks])          # (n_eta, N_BOOT)
        lin = eta < 0.15
        bc, _, _ = two_segment(eta[lin], V[lin])
        bb = [two_segment(eta[lin], B[lin, b], 300)[0] for b in range(B.shape[1])]
        ci = np.percentile(bb, [2.5, 97.5]).tolist()
        pred = float(np.arcsin(1.0 / R) / np.pi)
        # descriptive: peak of dV/dT after Savitzky-Golay smoothing
        from scipy.signal import savgol_filter
        pos = eta > 0
        T = np.log2(1.0 / eta[pos]); o = np.argsort(T)
        w = min(11, (int(pos.sum()) - 1) // 2 * 2 + 1)                 # 11 on the full grid (smaller only in tests)
        Vs = savgol_filter(V[pos][o], w, min(2, w - 1))
        dV = np.gradient(Vs, T[o])
        peak_eta = float(2.0 ** -T[o][np.argmax(dV)])
        e1 = int(np.argmin(np.abs(eta - 1.0)))
        out[sid] = dict(v=v, R=R, runs=n, eta_c_hat=bc, ci=ci, eta_c_pred=pred, peak_eta_sg=peak_eta,
                        V_actual=float(V[0]), V_actual_se=float(SE[0]), V_eta1=float(V[e1]), V_eta1_se=float(SE[e1]),
                        eq11=float(s0 / (1.0 - v / 50.0)), censored=int(sum(rows[k]["result"]["censored"] for k in ks)),
                        curve=dict(eta=eta.tolist(), V=V.tolist(), se=SE.tolist()))
        Fb = (B[e1] - s0) / (B[0] - s0)
        out[sid]["F_free"] = [float((V[e1] - s0) / (V[0] - s0))] + np.percentile(Fb, [2.5, 97.5]).tolist()
        deaf = sets.get(10 + [5.0, 10.0, 15.0, 20.0, 25.0, 30.0].index(v)) if R == 4.0 else None
        if deaf:
            dv = deaf[0]["result"]
            Fd = (np.array(dv["boot"]) - s0) / (B[0] - s0)
            out[sid]["F_free_deaf"] = [float((dv["mean"] - s0) / (V[0] - s0))] + np.percentile(Fd, [2.5, 97.5]).tolist()
        if sid == 0:
            sel = (eta > 0) & (eta <= pred)
            bound = np.array([1.0 / (1.0 + expected_dilation(e, 1.0, R)) for e in eta[sel]])
            ratio = V[sel] / V[0]
            se_r = ratio * np.sqrt((SE[sel] / V[sel]) ** 2 + (SE[0] / V[0]) ** 2)
            out[0]["D1e_min_margin"] = float(np.min(ratio + 2 * se_r - bound))
    inside = lambda o: o["ci"][0] <= o["eta_c_pred"] <= o["ci"][1]
    if 0 in out:
        verdict["D1a"] = "agrees" if inside(out[0]) else "disagrees"
        verdict["D1e"] = "holds" if out[0]["D1e_min_margin"] >= 0 else "fails"
    if all(s in out for s in (0, 6, 7)):
        verdict["D1b"] = "agrees" if all(inside(out[s]) for s in (0, 6, 7)) else "disagrees"
    sp = [s for s in (1, 2, 3, 0, 4, 5) if s in out]
    if len(sp) == 6:
        verdict["D1c"] = "agrees" if all(out[s]["ci"][0] <= 0.0804 <= out[s]["ci"][1] for s in sp) else "disagrees"
        verdict["D1d"] = ("agrees" if all(abs(out[s]["V_eta1"] / out[s]["eq11"] - 1) <= 0.05 for s in sp)
                          else "disagrees")
    return out, verdict


def _boot_mean(a, rng, n=N_BOOT):
    a = np.asarray(a)
    return np.array([a[rng.integers(0, a.size, a.size)].mean() for _ in range(n)])


def analyze_d2(out_dir):
    from scipy.optimize import curve_fit
    res = _load(out_dir, "d2")
    out, verdict = {}, {}
    rng = np.random.default_rng(2702)
    for topo, (N, cg, *_ ) in D2_TOPO.items():
        none = {d["task"]["ik"]: d["result"]["r"] for n, d in res.items() if n.startswith(f"d2_{topo}_") and n.endswith("_none")}
        still = {d["task"]["ik"]: d["result"]["r"] for n, d in res.items() if n.startswith(f"d2_{topo}_") and n.endswith("_still")}
        ag = {(d["task"]["ik"], d["task"]["ie"]): d["result"] for n, d in res.items()
              if n.startswith(f"d2_{topo}_") and d["task"]["agent"] == 1}
        if not none or not ag:
            continue
        iks = sorted(none); ies = sorted({k[1] for k in ag})
        K = np.array([cg[i] for i in iks])
        r0 = np.array([np.mean(none[i]) for i in iks])
        B0 = np.array([_boot_mean(none[i], rng) for i in iks])                 # (nK, boot)
        E = np.full((len(iks), len(ies)), np.nan); EB = np.full((len(iks), len(ies), N_BOOT), np.nan)
        I = np.full((len(iks), len(ies)), np.nan)
        for a, i in enumerate(iks):
            for b, e in enumerate(ies):
                if (i, e) in ag:
                    rr = ag[(i, e)]["r"]
                    E[a, b] = 1 - np.mean(rr) / r0[a]
                    EB[a, b] = 1 - _boot_mean(rr, rng) / B0[a]
                    I[a, b] = np.nanmean(ag[(i, e)]["info"])
        etas = D2_ETA[ies]
        o = dict(K=K.tolist(), r_none=r0.tolist(), eta=etas.tolist(), E=E.tolist(), info=I.tolist())
        hi = (K >= 2.5) & (K <= 4.0) if topo == "fc" else (K >= 0.625) & (K <= 1.0)
        if topo == "fc":
            def kc_fit(r):
                m = (r > 0.25) & (r < 0.7)
                if m.sum() < 3:
                    return np.nan
                p, _ = curve_fit(lambda k, A, kc: A * np.sqrt(np.maximum(k - kc, 0.0)), K[m], r[m], p0=[0.7, 1.6])
                return float(p[1])
            ra = r0 * (1 - E[:, 0])
            o["Kc"], o["KcA"] = kc_fit(r0), kc_fit(ra)
            verdict["D2a"] = "agrees" if abs((o["KcA"] - o["Kc"]) - 0.393) <= 0.1 else "disagrees"
            mE0 = float(np.nanmean(E[hi, 0])); o["E_sync_eta0"] = mE0
            verdict["D2b"] = "agrees" if 0.15 <= mE0 <= 0.25 else "disagrees"
            m1 = np.nanmean(EB[hi, -1], axis=0)
            o["E_sync_eta1"] = [float(np.nanmean(E[hi, -1]))] + np.percentile(m1, [2.5, 97.5]).tolist()
            verdict["D2c"] = "yes" if o["E_sync_eta1"][1] > 0 else "no"
        # D2d: V (uniform rho) against I(eta)
        Vu = np.nanmean(E, axis=0); Iu = np.nanmean(I, axis=0)
        srt = np.argsort(Iu); x, y = Iu[srt], Vu[srt]
        n = len(x)
        c1 = np.polyfit(x, y, 1); sse1 = float(((np.polyval(c1, x) - y) ** 2).sum())
        _, sse2, _ = two_segment(x, y)
        bic1 = n * np.log(sse1 / n) + 2 * np.log(n); bic2 = n * np.log(sse2 / n) + 4 * np.log(n)
        o.update(V_uniform=Vu.tolist(), I_mean=Iu.tolist(), bic_line=float(bic1), bic_two=float(bic2),
                 slope_line=float(c1[0]))
        o["two_segment_wins"] = bool(bic2 < bic1)
        # D3b: F_free = V(eta = 1) / V(eta = 0), uniform and exponential rho
        sc = 1.988 if topo == "fc" else 0.5
        F = {}
        for lab, w in (("uniform", np.ones_like(K)),) + tuple((f"exp{m}", np.exp(-K / (m * sc))) for m in (0.5, 1, 2)):
            w = w / w.sum()
            V0 = np.nansum(w[:, None] * EB[:, 0], axis=0); V1 = np.nansum(w[:, None] * EB[:, -1], axis=0)
            F[lab] = [float(np.nansum(w * E[:, -1]) / np.nansum(w * E[:, 0]))] + np.percentile(V1 / V0, [2.5, 97.5]).tolist()
        o["F_free"] = F
        # D3c: the still agent
        if still:
            ok = True
            for a, i in enumerate(iks):
                if i in still:
                    Es = 1 - np.mean(still[i]) / r0[a]
                    se = np.std(1 - _boot_mean(still[i], rng) / B0[a])
                    ok &= abs(Es) < 3 * se + 1e-12
            o["still_pass"] = bool(ok)
        out[topo] = o
    if all(t in out for t in ("fc", "poisson", "sf")):
        verdict["D2d"] = ("agrees" if out["fc"]["two_segment_wins"] and not out["poisson"]["two_segment_wins"]
                          and not out["sf"]["two_segment_wins"] else "disagrees")
        verdict["D3c"] = "pass" if all(out[t].get("still_pass", False) for t in out) else "fail"
    return out, verdict


def analyze(out_dir):
    d1, v1 = analyze_d1(out_dir)
    d2, v2 = analyze_d2(out_dir)
    v = dict(v1, **v2)
    res = dict(verdicts=v, d1=d1, d2=d2)
    (ROOT / "results" / "e27_d_rochester.json").write_text(json.dumps(res, indent=1))
    L = ["# E27: the models of the Rochester group (niche D)", "", "Rules: docs/D.md.", "",
         "| Rule | Verdict |", "|---|---|"] + [f"| {k} | {x} |" for k, x in sorted(v.items())]
    L += ["", "| D1 set | v | R | η̂_c [95 % CI] | Eq. (4) | SG peak | V_actual | V(η=1) | Eq. (11) | F_free | F_free deaf |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for sid, o in sorted(d1.items()):
        fd = o.get("F_free_deaf")
        L.append(f"| {sid} | {o['v']:.0f} | {o['R']:.0f} | {o['eta_c_hat']:.4f} [{o['ci'][0]:.4f}, {o['ci'][1]:.4f}] | "
                 f"{o['eta_c_pred']:.4f} | {o['peak_eta_sg']:.4f} | {o['V_actual']:.2f} | {o['V_eta1']:.3f} | "
                 f"{o['eq11']:.3f} | {o['F_free'][0]:.3f} | {fd[0]:.3f} |" if fd else
                 f"| {sid} | {o['v']:.0f} | {o['R']:.0f} | {o['eta_c_hat']:.4f} [{o['ci'][0]:.4f}, {o['ci'][1]:.4f}] | "
                 f"{o['eta_c_pred']:.4f} | {o['peak_eta_sg']:.4f} | {o['V_actual']:.2f} | {o['V_eta1']:.3f} | "
                 f"{o['eq11']:.3f} | {o['F_free'][0]:.3f} | |")
    L += ["", "| D2 graph | K_c | K_c^A | E sync η=0 | slope V/I | two segments win | F_free uniform | F_free exp1 |",
          "|---|---|---|---|---|---|---|---|"]
    for t, o in d2.items():
        L.append(f"| {t} | {o.get('Kc', float('nan')):.3f} | {o.get('KcA', float('nan')):.3f} | "
                 f"{o.get('E_sync_eta0', float('nan')):.3f} | {o['slope_line']:.3f} | {o['two_segment_wins']} | "
                 f"{o['F_free']['uniform'][0]:.3f} | {o['F_free']['exp1'][0]:.3f} |")
    (ROOT / "results" / "e27_d_rochester.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    analyze(sys.argv[1] if len(sys.argv) > 1 else ROOT / "cluster_out")
