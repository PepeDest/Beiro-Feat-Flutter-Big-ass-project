"""Niche G (docs/G.md): is TE <= DT after the first step? Rules and expectations are in docs/G.md (fixed before the runs).

    python experiments/e29_g_te_dt.py --check     # the Kalman filter DT against the trajectory covariance (before G2)
    python experiments/e29_g_te_dt.py --g1        # G1, Monte Carlo check of the counterexample (this PC)
    python experiments/e29_g_te_dt.py --g2        # G2, the map (this PC, 4 workers)
    python experiments/e29_g_te_dt.py OUT_DIR     # G3 analysis, after the cluster run

The cluster runner calls tasks() and run_task() for G3.
"""
import json, pathlib, sys, time
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vlife.semantic_dynamic import (stationary_cov_discrete, sensor, run, viability, information_measures,  # noqa: E402
                                    _step)
from vlife.gaussian import conditional_mutual_information  # noqa: E402

RES = ROOT / "results"
TAU_MAX, N_SENS = 64, 5
FAMILIES = ("R", "S", "SF", "M")
G3_TAUS = (8, 16, 32, 64)


def _logdet(M):
    s, v = np.linalg.slogdet(M)
    return v


def _orth(rng, n):
    Q, R = np.linalg.qr(rng.normal(size=(n, n)))
    return Q * np.sign(np.diag(R))


def make_system(family, seed, dx=None, dy=None):
    """(F, W, dx, dy, tau_x, tau_y) of docs/G.md, G2."""
    rng = np.random.default_rng([seed, 29])
    if dx is None:
        dx, dy = ((1, 1), (1, 2), (2, 2))[seed % 3]
    n = dx + dy
    if family == "R":
        A = rng.normal(size=(n, n)); rho = rng.uniform(0.3, 0.999)
        F = rho * A / np.max(np.abs(np.linalg.eigvals(A)))
        W = np.diag(rng.uniform(0.3, 1.5, n))
        ey = np.abs(np.linalg.eigvals(F[dx:, dx:])); ex = np.abs(np.linalg.eigvals(F[:dx, :dx]))
        ry, rx = float(np.clip(ey.max(), 1e-9, 0.999999)), float(np.clip(ex.min(), 1e-9, 0.999999))
    else:
        ry = 1.0 - 10 ** rng.uniform(-4, np.log10(0.5))
        rx = rng.uniform(0.9, 0.999) if family == "M" else rng.uniform(0.0, 0.95)
        F = np.zeros((n, n))
        F[dx:, dx:] = ry * _orth(rng, dy); F[:dx, :dx] = rx * _orth(rng, dx)
        F[:dx, dx:] = rng.normal(size=(dx, dy))
        if family == "SF":
            F[dx:, :dx] = 0.1 * rng.normal(size=(dy, dx))
            sr = np.max(np.abs(np.linalg.eigvals(F)))
            if sr > 0.9999:
                F *= 0.9999 / sr
        W = np.zeros((n, n)); W[:dx, :dx] = np.diag(rng.uniform(0.3, 1.5, dx)); W[dx:, dx:] = (1 - ry ** 2) * np.eye(dy)
        rx = max(rx, 1e-9)
    tx, ty = -1.0 / np.log(rx), -1.0 / np.log(ry)
    return F, W, dx, dy, float(tx), float(ty)


def te_dt_steps(F, W, dx, K, SN, tau, S0=None):
    """Per-step TE_t (covariance recursion of B3) and DT_t (Kalman filter on (x, y) with measurement z = K y + N)."""
    n = F.shape[0]; dy = n - dx
    S = stationary_cov_discrete(F, W) if S0 is None else S0
    covs, te, maps = run(F, W, dx, K, SN, tau, S)
    H = np.hstack([np.zeros((K.shape[0], dx)), K])
    Fyx, Fyy = F[dx:, :dx], F[dx:, dx:]
    P = S.copy(); dt = []
    ldSN = _logdet(SN)
    for t in range(tau):
        m = maps[t]
        Sz = H @ P @ H.T + SN
        dt.append(0.5 * (_logdet(Sz) - ldSN))
        G = P @ H.T @ np.linalg.inv(Sz)
        Pu = P - G @ H @ P
        Ft = np.block([[m["Ax"], np.zeros((dx, dy))], [Fyx, Fyy]])
        Nx = m["E"] @ m["I_P"] @ m["E"].T + W[:dx, :dx]
        Q = np.zeros((n, n)); Q[:dx, :dx] = Nx; Q[dx:, dx:] = W[dx:, dx:]
        P = Ft @ Pu @ Ft.T + Q
        P = (P + P.T) / 2
    return np.array(te), np.array(dt)


def random_sensor(rng, dy):
    m = dy * (dy - 1) // 2
    return sensor(rng.uniform(-np.pi, np.pi, m), rng.uniform(0.0, 1 - 1e-6, dy))


# ------------------------------------------------------------------ check before G2
def check():
    worst = 0.0
    for fam in FAMILIES:
        for k in range(50):
            F, W, dx, dy, *_ = make_system(fam, 79000 + k)
            K, SN = random_sensor(np.random.default_rng([k, 7]), dy)
            te, dt = te_dt_steps(F, W, dx, K, SN, 16)
            te2, _, dt2 = information_measures(F, W, dx, K, SN, 16, which=("te", "dt"))
            worst = max(worst, abs(dt.sum() - dt2), abs(te.sum() - te2))
    worst = float(worst); ok = bool(worst <= 1e-8)
    print(f"check: largest difference {worst:.2e} nats -> {'pass' if ok else 'FAIL'}")
    (RES / "e29_g_check.json").write_text(json.dumps(dict(largest_difference=worst, ok=ok)))
    return ok


# ------------------------------------------------------------------ G1
def g1(n_batch=20, batch=100_000, taus=(16, 64)):
    F = np.array([[0.0, 1.0], [0.0, 0.999]]); W = np.diag([0.5, 1 - 0.999 ** 2]); dx = 1
    K, SN = sensor([], [0.5])
    S0 = stationary_cov_discrete(F, W)
    out = {}
    for tau in taus:
        te_ex, dt_ex = te_dt_steps(F, W, dx, K, SN, tau)
        te_x, _, dt_x = information_measures(F, W, dx, K, SN, tau, which=("te", "dt"))
        vals = []
        for b in range(n_batch):
            rng = np.random.default_rng([2901, tau, b])
            L0 = np.linalg.cholesky(S0)
            st = rng.normal(size=(batch, 2)) @ L0.T
            X, Y, Z = [st[:, :1]], [st[:, 1:]], []
            for t in range(tau):
                Sh = np.cov(np.hstack([X[-1], Y[-1]]).T)          # sample covariance of (x_t, y_t)
                m = _step(F, W, dx, Sh, K, SN)
                z = Y[-1] @ K.T + rng.normal(size=(batch, 1)) * np.sqrt(SN[0, 0])
                e = rng.normal(size=(batch, 1)) * np.sqrt(max(m["I_P"][0, 0], 0.0))
                x = X[-1] @ m["Ax"].T + z @ m["Bz"].T + e @ m["E"].T + rng.normal(size=(batch, 1)) * np.sqrt(W[0, 0])
                y = X[-1] @ F[1:, :1].T + Y[-1] @ F[1:, 1:].T + rng.normal(size=(batch, 1)) * np.sqrt(W[1, 1])
                Z.append(z); X.append(x); Y.append(y)
            A = np.hstack(X + Y + Z)
            C = np.cov(A.T)
            ix = [[t] for t in range(tau + 1)]
            iy = [[tau + 1 + t] for t in range(tau + 1)]
            iz = [[2 * tau + 2 + t] for t in range(tau)]
            fl = lambda L: [i for l in L for i in l]
            te = sum(conditional_mutual_information(C, iy[t], ix[t + 1], ix[t]) for t in range(tau))
            dt = sum(conditional_mutual_information(C, fl(iy[:t + 1]), iz[t], fl(iz[:t])) for t in range(tau))
            vals.append((te, dt))
        v = np.array(vals); mean = v.mean(0); se = v.std(0, ddof=1) / np.sqrt(n_batch)
        gap = v[:, 1] - v[:, 0]
        out[tau] = dict(TE_exact=float(te_ex.sum()), DT_exact=float(dt_ex.sum()), TE_traj=float(te_x), DT_traj=float(dt_x),
                        TE_mc=float(mean[0]), TE_se=float(se[0]), DT_mc=float(mean[1]), DT_se=float(se[1]),
                        gap_mc=float(gap.mean()), gap_ci=[float(gap.mean() - 1.96 * gap.std(ddof=1) / np.sqrt(n_batch)),
                                                          float(gap.mean() + 1.96 * gap.std(ddof=1) / np.sqrt(n_batch))])
        print(tau, out[tau], flush=True)
    agree = all(abs(o["TE_mc"] - o["TE_exact"]) < 0.02 + 3 * o["TE_se"] and abs(o["DT_mc"] - o["DT_exact"]) < 0.02 + 3 * o["DT_se"]
                for o in out.values())
    v = dict(G1a="agree" if agree else "disagree")
    v["G1b"] = "false" if agree and out[64]["gap_ci"][1] < 0 else "not shown"
    (RES / "e29_g1.json").write_text(json.dumps(dict(verdicts=v, taus=out), indent=1))
    print(v)


# ------------------------------------------------------------------ G2
def _g2_job(args):
    fam, seed = args
    F, W, dx, dy, tx, ty = make_system(fam, seed)
    rng = np.random.default_rng([seed, 30])
    fails = []
    for j in range(N_SENS):
        K, SN = random_sensor(rng, dy)
        te, dt = te_dt_steps(F, W, dx, K, SN, TAU_MAX)
        gap = np.cumsum(dt) - np.cumsum(te)
        bad = np.flatnonzero(gap < -1e-6)
        fails.append(int(bad[0]) + 1 if bad.size else 0)
    return dict(family=fam, seed=seed, dx=dx, dy=dy, tau_x=tx, tau_y=ty, tau_fail=fails)


def g2(n_per=5000, workers=4):
    from concurrent.futures import ProcessPoolExecutor
    from scipy.stats import logistic  # noqa: F401
    jobs = [(fam, 70001 + 10000 * k + s) for k, fam in enumerate(FAMILIES) for s in range(n_per)]
    t0 = time.time()
    with ProcessPoolExecutor(workers) as ex:
        rows = list(ex.map(_g2_job, jobs, chunksize=50))
    print(f"G2: {len(rows)} systems, {time.time() - t0:.0f} s", flush=True)
    fail_any = np.array([any(f > 0 for f in r["tau_fail"]) for r in rows])
    fail4 = [r for r in rows if any(0 < f <= 4 for f in r["tau_fail"])]
    v = dict(G2a="never at τ ≤ 4" if not fail4 else f"fails at τ ≤ 4 in {len(fail4)} systems")
    x = np.log(np.array([r["tau_y"] / r["tau_x"] for r in rows]))
    rng = np.random.default_rng(2902)
    def slope(idx):
        from scipy.optimize import minimize
        xx, yy = x[idx], fail_any[idx].astype(float)
        f = lambda b: np.sum(np.logaddexp(0, b[0] + b[1] * xx) - yy * (b[0] + b[1] * xx))
        return minimize(f, [0.0, 0.0], method="BFGS").x[1]
    sl = slope(np.arange(len(rows)))
    bs = [slope(rng.integers(0, len(rows), len(rows))) for _ in range(200)]
    ci = np.percentile(bs, [2.5, 97.5]).tolist()
    v["G2b"] = "yes" if ci[0] > 0 else "no"
    fam = np.array([r["family"] for r in rows])
    fM, fS = fail_any[fam == "M"], fail_any[fam == "S"]
    d = [fM[rng.integers(0, fM.size, fM.size)].mean() - fS[rng.integers(0, fS.size, fS.size)].mean() for _ in range(2000)]
    dci = np.percentile(d, [2.5, 97.5]).tolist()
    v["G2c"] = "yes" if dci[1] < 0 else "no"
    frac = {f: float(fail_any[fam == f].mean()) for f in FAMILIES}
    taus = [f for r in rows for f in r["tau_fail"] if f > 0]
    out = dict(verdicts=v, slope=float(sl), slope_ci=ci, frac_fail=frac, diff_M_minus_S=[float(fM.mean() - fS.mean())] + dci,
               tau_fail_quantiles=np.percentile(taus, [0, 5, 25, 50, 75, 100]).tolist() if taus else None,
               min_tau_fail=int(min(taus)) if taus else None, seconds=time.time() - t0)
    (RES / "e29_g2.json").write_text(json.dumps(dict(out, rows=rows)))
    L = ["# E29 G2: where TE ≤ DT fails (niche G)", "", "Rules: docs/G.md, G2.", "",
         "| Rule | Value | Verdict |", "|---|---|---|",
         f"| G2a | smallest failing τ: {out['min_tau_fail']} | {v['G2a']} |",
         f"| G2b | logistic slope on log(τ_y/τ_x): {sl:.3f} [{ci[0]:.3f}, {ci[1]:.3f}] | {v['G2b']} |",
         f"| G2c | fraction failing, M − S: {out['diff_M_minus_S'][0]:.3f} [{dci[0]:.3f}, {dci[1]:.3f}] | {v['G2c']} |", "",
         "Fraction of systems with a failure by τ = 64: " + ", ".join(f"{k} {x:.3f}" for k, x in frac.items()) + ".",
         f"Quantiles of the failing τ (0, 5, 25, 50, 75, 100 %): {out['tau_fail_quantiles']}. Time {out['seconds']:.0f} s."]
    (RES / "e29_g2.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


# ------------------------------------------------------------------ G3 (cluster)
N_A, N_S1, S_HI = 90, 50, 1 - 1e-3


def tasks(smoke=False):
    seeds = range(73001, 73004) if smoke else range(73001, 73301)
    taus = (8,) if smoke else G3_TAUS
    return [dict(job="g3", name=f"g3_{s}_t{tau:02d}", seed=s, tau=tau, smoke=smoke, cost=4500 * (0.04 * tau / 8 + 0.002))
            for s in seeds for tau in taus]


def run_task(t):
    F, W, dx, dy, tx, ty = make_system("S", t["seed"], 1, 2)
    tau = t["tau"]; S0 = stationary_cov_discrete(F, W)
    I2, O2 = np.eye(2), np.zeros((2, 2))
    V_act = viability(F, W, dx, I2, O2, tau, S0)
    te_act = float(run(F, W, dx, I2, O2, tau, S0)[1].sum())
    na, ns = (12, 8) if t.get("smoke") else (N_A, N_S1)
    best_te, best_dt, best_gap, n_feas = te_act, np.inf, np.inf, 0
    arg_te, arg_dt = "actual", None
    for a in np.linspace(0, np.pi, na, endpoint=False):
        for s1 in np.linspace(0, S_HI, ns):
            g = lambda s2: viability(F, W, dx, *sensor([a], [s1, s2]), tau, S0) - V_act
            lo, hi = 0.0, S_HI
            glo, ghi = g(lo), g(hi)
            if not np.isfinite(glo) or not np.isfinite(ghi) or glo * ghi > 0:
                continue
            for _ in range(40):
                mid = 0.5 * (lo + hi); gm = g(mid)
                if gm * glo <= 0:
                    hi = mid
                else:
                    lo, glo = mid, gm
            s2 = 0.5 * (lo + hi)
            K, SN = sensor([a], [s1, s2])
            te, dt = te_dt_steps(F, W, dx, K, SN, tau, S0)
            te, dt = float(te.sum()), float(dt.sum())
            n_feas += 1
            if te < best_te:
                best_te, arg_te = te, [float(a), float(s1), float(s2)]
            if dt < best_dt:
                best_dt, arg_dt = dt, [float(a), float(s1), float(s2)]
            best_gap = min(best_gap, dt - te)
    return dict(V_act=float(V_act), TE_act=te_act, S_TE=float(best_te), D_T=float(best_dt) if n_feas else None,
                arg_te=arg_te, arg_dt=arg_dt, min_point_gap=float(best_gap) if n_feas else None, n_feasible=n_feas,
                tau_x=tx, tau_y=ty)


def analyze(out_dir):
    rows = [json.loads(f.read_text()) for f in pathlib.Path(out_dir, "g3").glob("*.json")]
    out, v = {}, {}
    for tau in G3_TAUS:
        r = [d["result"] for d in rows if d["task"]["tau"] == tau and d["result"]["n_feasible"] > 0]
        if not r:
            continue
        fails = [x for x in r if x["S_TE"] > x["D_T"] + 1e-4]
        v[f"G3a_tau{tau}"] = "holds" if not fails else f"fails in {len(fails)} systems"
        out[tau] = dict(n=len(r), n_fail=len(fails), median_gap=float(np.median([x["D_T"] - x["S_TE"] for x in r])),
                        n_point_fail=int(sum(x["min_point_gap"] < -1e-6 for x in r)))
    (RES / "e29_g3.json").write_text(json.dumps(dict(verdicts=v, taus=out), indent=1))
    L = ["# E29 G3: does S_TE ≤ D_T* hold at long τ? (niche G)", "", "Rules: docs/G.md, G3.", "",
         "| τ | Systems with a feasible point | S_TE > D_T* + 1e-4 | Median D_T* − S_TE | Systems with TE > DT at some point | Verdict |",
         "|---|---|---|---|---|---|"]
    for tau, o in out.items():
        L.append(f"| {tau} | {o['n']} | {o['n_fail']} | {o['median_gap']:.4f} | {o['n_point_fail']} | {v[f'G3a_tau{tau}']} |")
    (RES / "e29_g3.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if "--check" in sys.argv:
        check()
    elif "--g1" in sys.argv:
        g1()
    elif "--g2" in sys.argv:
        g2()
    else:
        analyze(sys.argv[1] if len(sys.argv) > 1 else ROOT / "cluster_out")
