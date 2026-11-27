"""Niche H (docs/H.md): the heat, the learning rate and the observed semantic information rate of the sensor channel,
in the S3 homeostat (family H) and in random linear agents (family R). Rules H1a-H1e, H2a-H2e and the expectations are
in docs/H.md (fixed before this run). Exact formulas, no simulation.

    python experiments/e31_h_energy.py
"""
import json, sys, time
import numpy as np
from scipy.integrate import quad
from scipy.stats import spearmanr
from common import RES, save_json
from vlife.agency import draw_organism, homeostat
from vlife.gaussian import entropy_production

N_R, TOL = 2000, 1e-9


# ------------------------------------------------------------------ systems (docs/H.md, H1. Systems)
def family_h():
    """The 400 S3 organisms, intact. Order (h, s, m, u, v): environment 0, sensor 1, target 4."""
    out = []
    for i in range(400):
        o = draw_organism(np.random.default_rng([2026, i]))
        B, D, S = homeostat(o, "intact")
        out.append(dict(fam="H", i=i, L=o.L, B=B, D=D, S=S, h=0, X=[1, 2, 3, 4], s=1, T=4))
    return out


def draw_r(j):
    rng = np.random.default_rng([8400, j])
    lu = lambda lo, hi: float(np.exp(rng.uniform(np.log(lo), np.log(hi))))
    dx = int(rng.integers(2, 5))
    T_h = lu(1, 20)
    k = lu(0.5, 5); sig_s = lu(0.1, 3)
    n = dx + 1                                        # index 0 is h, agent coordinates are 1..dx
    while True:
        B = np.zeros((n, n)); d = np.zeros(n)
        B[0, 0] = d[0] = 1 / T_h
        B[1, 1] = k; B[1, 0] = -k; d[1] = sig_s ** 2 * k
        ks = [k] + [lu(0.3, 5) for _ in range(dx - 1)]
        for a in range(1, dx):                        # agent coordinate a, matrix index a + 1
            B[a + 1, a + 1] = ks[a]
            B[a + 1, a] = -ks[a] * rng.uniform(-2, 2)
            for b in range(dx):
                if b != a and b != a - 1 and rng.uniform() < 0.3:
                    B[a + 1, b + 1] = 0.5 * np.sqrt(ks[a] * ks[b]) * rng.normal()
            d[a + 1] = lu(0.005, 0.5)
        if np.linalg.eigvals(B[1:, 1:]).real.min() >= 0.01:
            break
    B[dx, 0] = -1.0                                   # push of h on the target
    D = np.diag(d)
    from vlife.gaussian import stationary_cov
    return dict(fam="R", i=j, dx=dx, B=B, D=D, S=stationary_cov(B, D), h=0, X=list(range(1, n)), s=1, T=dx)


# ------------------------------------------------------------------ thermodynamics and information (docs/H.md, H1)
def thermo(sy):
    B, D, S, X, s, h = sy["B"], sy["D"], sy["S"], sy["X"], sy["s"], sy["h"]
    Dd = np.diag(D); Si = np.linalg.inv(S); M = B - D @ Si
    sig = np.diag(M @ S @ M.T) / Dd
    q = np.diag(B @ S @ M.T) / Dd
    r = dict(sigma=entropy_production(B, D, S), sigma_X=float(sig[X].sum()), sigma_h=float(sig[h]),
             q_X=float(q[X].sum()), q_s=float(q[s]), l_X=float(np.diag(M)[X].sum()),
             cs=float((Dd[X] * np.diag(Si)[X]).sum()))
    # second method: d/dtau I(X_{t+tau}; h_t) at 0+
    Sx, Sh, C = S[np.ix_(X, X)], S[h, h], S[X, h]
    Cp = (-B @ S)[X, h]
    A = Sx - np.outer(C, C) / Sh
    dA = -(np.outer(Cp, C) + np.outer(C, Cp)) / Sh
    r["l_X_deriv"] = float(-0.5 * np.trace(np.linalg.solve(A, dA)))
    r["I_Xh"] = float(0.5 * (np.linalg.slogdet(Sx)[1] - np.linalg.slogdet(A)[1]))
    # transfer entropy rate h -> X: closed form and numerical spectral integral with the full matrices
    b, Dh = B[h, h], D[h, h]
    a = float(sum(B[i, h] ** 2 / (2 * Dd[i]) for i in X))
    r["Tdot"] = 0.5 * (np.sqrt(b ** 2 + 2 * a * Dh) - b)
    Bxx, inp, Dx = B[np.ix_(X, X)], -B[X, h], D[np.ix_(X, X)]

    def f(w):
        Rw = np.linalg.inv(1j * w * np.eye(len(X)) + Bxx)
        g = Rw @ inp
        N = Rw @ (2 * Dx) @ Rw.conj().T
        return np.log1p(2 * Dh / (b ** 2 + w ** 2) * float(np.real(g.conj() @ np.linalg.solve(N, g))))
    pts = [0, 1e-2, 0.1, 1, 10, 100, 1e3, np.inf]
    r["Tdot_spec"] = sum(quad(f, lo, hi, limit=400, epsabs=0, epsrel=1e-11)[0] for lo, hi in zip(pts[:-1], pts[1:])) \
        * 2 / (4 * np.pi)
    k = -B[s, h]
    r["Is_closed"] = 0.5 * (np.sqrt(b ** 2 + 2 * (k ** 2 / (2 * Dd[s])) * Dh) - b)
    return r


def thermo_fast(sy):
    """q_X and the closed-form I_s only (for the H3 search, e31b_h3_search.py)."""
    B, D, S, X, s, h = sy["B"], sy["D"], sy["S"], sy["X"], sy["s"], sy["h"]
    Dd = np.diag(D); M = B - D @ np.linalg.inv(S)
    q = np.diag(B @ S @ M.T) / Dd
    b, Dh, k = B[h, h], D[h, h], -B[s, h]
    return dict(q_X=float(q[X].sum()), Is_closed=0.5 * (np.sqrt(b ** 2 + 2 * (k ** 2 / (2 * Dd[s])) * Dh) - b))


# ------------------------------------------------------------------ semantic information rate (docs/H.md, H1)
class Grid:
    def __init__(self, n=20_000, lo=1e-6, hi=1e5):
        self.w = np.geomspace(lo, hi, n)
        dw = np.diff(self.w)
        self.q = np.zeros(n); self.q[:-1] += dw / 2; self.q[1:] += dw / 2
        self.q *= 2.0                                 # the integrands are even in omega


def spectra(sy, grid):
    B, D, X, s, h, T = sy["B"], sy["D"], sy["X"], sy["s"], sy["h"], sy["T"]
    Bxx = B[np.ix_(X, X)]
    inp = -B[X, h]
    w = grid.w
    R = np.linalg.inv(1j * w[:, None, None] * np.eye(len(X))[None] + Bxx[None])
    iT, i0 = X.index(T), X.index(s)
    Gs = R[:, iT, i0] * inp[i0]
    Gp = sum(R[:, iT, j] * inp[j] for j in range(len(X)) if j != i0)
    Sh = 2 * D[h, h] / (B[h, h] ** 2 + w ** 2)
    Np = 2 * D[s, s] / inp[i0] ** 2
    c = Sh * Gs * np.conj(Gp)
    # Var(x_T) at H = 1 from the spectrum, against S (a sanity value, reported)
    noise = sum(np.abs(R[:, iT, j]) ** 2 * 2 * D[X[j], X[j]] for j in range(len(X)))
    var1 = float((grid.q * (np.abs(Gs + Gp) ** 2 * Sh + noise)).sum() / (2 * np.pi))
    return Sh, Np, c, var1


def info_rate(q, Sh, Np, H2):
    return float((q * np.log((Sh + Np) / ((1 - H2) * Sh + Np))).sum() / (4 * np.pi))


def solve(sy, grid, cls, sp=None):
    """Return (I_s at H = 1, S, H, extra) for class 'A' or 'Z'."""
    Sh, Np, c, var1 = spectra(sy, grid) if sp is None else sp
    q = grid.q
    I1 = info_rate(q, Sh, Np, np.ones_like(Sh))
    c_act = float((q * c.real).sum())
    if c_act >= 0:
        return I1, 0.0, np.zeros_like(c), dict(c_act=c_act, var1=var1, helpful=False)
    if cls == "A":
        wgt = np.abs(c); ph = -np.conj(c) / np.where(wgt > 0, wgt, 1)
    else:
        wgt = np.clip(-c.real, 0, None); ph = np.ones_like(c)

    def Hm(mu):
        X = (mu * wgt) ** 2 * Sh * (Sh + Np)
        r = np.minimum(1.0, mu * wgt * (Sh + Np) / (Sh + np.sqrt(Sh ** 2 + X)))
        return r * ph
    g = lambda H: float((q * np.real(c * H)).sum())
    lo, hi = -30.0, 30.0
    while g(Hm(10 ** hi)) > c_act:
        hi += 10
        if hi > 300:
            raise RuntimeError("no feasible garbling")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if g(Hm(10 ** mid)) > c_act:
            lo = mid
        else:
            hi = mid
    H = Hm(10 ** hi)
    return I1, info_rate(q, Sh, Np, np.abs(H) ** 2), H, dict(c_act=c_act, var1=var1, helpful=True)


def check_optimum(sy, cls, n_rand=1000):
    """H1d: random garblings mixed with the extreme feasible point never beat the optimum."""
    g4 = Grid(4000)
    sp = spectra(sy, g4)
    Sh, Np, c, _ = sp
    I1, S_opt, H_opt, ex = solve(sy, g4, cls, sp)
    q = g4.q
    g = lambda H: float((q * np.real(c * H)).sum())
    H_ext = -np.conj(c) / np.abs(c) if cls == "A" else (c.real < 0).astype(float)
    g_ext, c_act = g(H_ext), ex["c_act"]
    rng = np.random.default_rng([3101, ord(cls), sy["i"], ord(sy["fam"])])
    x = np.log(g4.w)
    best = np.inf
    for kk in range(n_rand):
        if kk % 2:
            cc = rng.normal(size=8)
            m = 1 / (1 + np.exp(-sum(cc[j] * np.cos(j * (x - x[0]) / (x[-1] - x[0]) * np.pi) for j in range(8))))
        else:
            m = rng.uniform(0, 1, x.size) ** rng.uniform(0.2, 5)
        Hr = m * np.exp(1j * rng.uniform(-np.pi, np.pi, x.size) * rng.uniform(0, 1) ** 2) if cls == "A" else m
        gr = g(Hr)
        if gr > c_act:
            lam = (c_act - g_ext) / (gr - g_ext)
            Hr = lam * Hr + (1 - lam) * H_ext
        best = min(best, info_rate(q, Sh, Np, np.abs(Hr) ** 2))
    return dict(S_opt=S_opt, best=float(best), passed=bool(best >= S_opt * (1 - TOL)))


# ------------------------------------------------------------------ main
def rng_ci(x):
    x = np.asarray(x, float)
    return [float(np.median(x)), float(np.quantile(x, 0.1)), float(np.quantile(x, 0.9))]


def main():
    t0 = time.time()
    sysH = family_h()
    if abs(sysH[0]["L"] - 1.3577157550157608) > 1e-12:
        raise SystemExit("organism 0 does not match results/e23_b4a_homeostat.json. Stop.")
    systems = sysH + [draw_r(j) for j in range(N_R)]
    g = Grid()
    rows = []
    for sy in systems:
        r = thermo(sy)
        sp = spectra(sy, g)
        for cls in ("A", "Z"):
            I1, S, H, ex = solve(sy, g, cls, sp)
            r["S_" + cls] = S
        r.update(Is_grid=I1, helpful=ex["helpful"], c_act=ex["c_act"], var1_grid=ex["var1"],
                 var1=float(sy["S"][sy["T"], sy["T"]]), fam=sy["fam"], i=sy["i"])
        rows.append(r)
    # checks
    rel = lambda a, b: abs(a - b) / max(abs(a), abs(b), 1e-300)
    H1a = max(rel(r["l_X"], r["l_X_deriv"]) for r in rows)
    H1b_T = max(rel(r["Tdot"], r["Tdot_spec"]) for r in rows)
    H1b_I = max(rel(r["Is_closed"], r["Is_grid"]) for r in rows)
    thm = dict(
        split=max(rel(r["sigma_X"] + r["sigma_h"], r["sigma"]) for r in rows),
        q_ge_l=min((r["q_X"] - r["l_X"]) / max(abs(r["q_X"]), 1e-300) for r in rows),
        l_ge_0=min(r["l_X"] / max(r["Tdot"], 1e-300) for r in rows),
        l_le_T=min((r["Tdot"] - r["l_X"]) / r["Tdot"] for r in rows),
        cs=min((r["q_X"] - r["l_X"] - r["l_X"] ** 2 / r["cs"]) / max(abs(r["q_X"]), 1e-300) for r in rows),
        S_le_I=min((r["Is_closed"] - r["S_Z"]) / r["Is_closed"] for r in rows),
        SA_le_SZ=min((r["S_Z"] - r["S_A"]) / max(r["S_Z"], 1e-300) for r in rows))
    H1c = all(v >= -TOL for k, v in thm.items() if k != "split") and thm["split"] < TOL
    sel = [sy for sy, r in zip(systems, rows) if r["helpful"] and sy["fam"] == "H"][:10] + \
          [sy for sy, r in zip(systems, rows) if r["helpful"] and sy["fam"] == "R"][:10]
    chk = [dict(fam=sy["fam"], i=sy["i"], **{c: check_optimum(sy, c) for c in ("A", "Z")}) for sy in sel]
    H1d = all(c[k]["passed"] for c in chk for k in ("A", "Z"))
    gf = Grid(200_000, 1e-8, 1e6)
    grid_dev = 0.0
    for sy in sel:
        r = rows[systems.index(sy)]
        spf = spectra(sy, gf)
        for cls in ("A", "Z"):
            grid_dev = max(grid_dev, rel(solve(sy, gf, cls, spf)[1], r["S_" + cls]))
    H1e = grid_dev < 1e-3
    var_dev = max(rel(r["var1"], r["var1_grid"]) for r in rows)
    v = dict(H1a="pass" if H1a < 1e-6 else "fail", H1b="pass" if (H1b_T < 1e-6 and H1b_I < 1e-4) else "fail",
             H1c="pass" if H1c else "fail", H1d="pass" if H1d else "fail", H1e="pass" if H1e else "fail")
    # H2
    voi = {d["i"]: d["VoI"] for d in json.load(open(RES / "e23_b4a_homeostat.json"))["organisms"]}
    fam = {}
    for F in ("H", "R"):
        rr = [r for r in rows if r["fam"] == F]
        a = lambda k: np.array([r[k] for r in rr], float)
        SZ, SA, qX, lX, qs, Is, Td = a("S_Z"), a("S_A"), a("q_X"), a("l_X"), a("q_s"), a("Is_closed"), a("Tdot")
        hp = a("helpful").astype(bool)

        def bound(lhs, rhs):
            fail = lhs > rhs * (1 + TOL)
            ratio = rhs[lhs > 0] / lhs[lhs > 0]
            return dict(n_fail=int(fail.sum()), min_ratio=float(ratio.min()) if ratio.size else None)
        d = dict(n=len(rr), n_helpful=int(hp.sum()), n_S0=int((SZ == 0).sum()),
                 H2a=bound(SZ, qX), H2b=bound(SZ, lX), H2c=bound(SZ, qs),
                 H2a_A=bound(SA, qX), H2b_A=bound(SA, lX), H2c_A=bound(SA, qs),
                 desc=dict(SZ_over_Is=rng_ci(SZ[hp] / Is[hp]), SA_over_Is=rng_ci(SA[hp] / Is[hp]),
                           SZ_over_qX=rng_ci(SZ[hp] / qX[hp]), SA_over_qX=rng_ci(SA[hp] / qX[hp]),
                           SZ_over_lX=rng_ci(SZ[hp] / lX[hp]), eta=rng_ci(lX / qX), C=rng_ci(lX / Td),
                           Is_over_qs=rng_ci(Is / qs), q_s_over_q_X=rng_ci(qs / qX), qs_neg=int((qs < 0).sum())))
        for k in ("H2a", "H2b", "H2c"):
            v[f"{k}_{F}"] = "holds" if d[k]["n_fail"] == 0 else "fails"
        if F == "H":
            ids = [j for j, r in enumerate(rr) if r["i"] in voi]
            vv = np.array([voi[rr[j]["i"]] for j in ids])
            d["H2e"] = {k: float(spearmanr(a(k)[ids], vv)[0]) for k in ("S_Z", "S_A", "l_X", "q_X", "Is_closed")}
            d["H2e"]["n"] = len(ids)
        fam[F] = d
    out = dict(verdicts=v, checks=dict(H1a=H1a, H1b_T=H1b_T, H1b_I=H1b_I, theorems=thm, H1d=chk, H1e=grid_dev,
                                       var_grid_dev=var_dev),
               families=fam, seconds=time.time() - t0,
               rows=[{k: r[k] for k in ("fam", "i", "sigma", "sigma_X", "q_X", "q_s", "l_X", "Tdot", "Is_closed",
                                         "S_A", "S_Z", "I_Xh", "helpful")} for r in rows])
    save_json("e31_h_energy.json", out)
    f3 = lambda x: f"{x[0]:.3f} [{x[1]:.3f}, {x[2]:.3f}]"
    L = ["# E31: the energy cost of semantic information (niche H)", "", "Rules: docs/H.md.", "",
         "| Rule | Value | Verdict |", "|---|---|---|",
         f"| H1a | largest relative difference of the two l_X: {H1a:.1e} | {v['H1a']} |",
         f"| H1b | Ṫ: {H1b_T:.1e}, İ_s on the grid: {H1b_I:.1e} | {v['H1b']} |",
         "| H1c | " + ", ".join(f"{k} {x:.1e}" for k, x in thm.items()) + f" | {v['H1c']} |",
         f"| H1d | {len(chk)} systems, 1000 garblings per class | {v['H1d']} |",
         f"| H1e | largest change on the fine grid: {grid_dev:.1e} | {v['H1e']} |"]
    for F in ("H", "R"):
        d = fam[F]
        for k, name in (("H2a", "S_Z ≤ q_X"), ("H2b", "S_Z ≤ l_X"), ("H2c", "S_Z ≤ q_s")):
            mr = d[k]["min_ratio"]
            L.append(f"| {k} ({F}) | {name}: {d[k]['n_fail']} failures of {d['n']}, smallest ratio "
                     f"{'—' if mr is None else f'{mr:.3g}'} (class A: {d[k + '_A']['n_fail']} failures) | "
                     f"{v[f'{k}_{F}']} |")
    L += ["", "Description (median [10 %, 90 %], systems where the sensor helps):"]
    for F in ("H", "R"):
        d = fam[F]
        L.append(f"- Family {F}: {d['n']} systems, {d['n_helpful']} where the sensor helps, S = 0 in {d['n_S0']}. "
                 + ", ".join(f"{k} {f3(x)}" for k, x in d["desc"].items() if isinstance(x, list)) +
                 f", q_s < 0 in {d['desc']['qs_neg']}.")
    he = fam["H"]["H2e"]
    L.append(f"- H2e (family H, {he['n']} organisms): ρ with VoI: " +
             ", ".join(f"{k} {x:+.3f}" for k, x in he.items() if k != "n") + ".")
    L.append(f"- Var(x_T) from the spectrum against S: largest relative difference {var_dev:.1e}. "
             f"Time {out['seconds']:.0f} s.")
    (RES / "e31_h_energy.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
