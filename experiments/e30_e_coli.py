"""Niche E (docs/E.md): semantic information of the E. coli chemotaxis pathway, with the measured model of
MattinglyKaminoMachtaEmonet21 (Table S1). Rules E1-E3 and the expectations are in docs/E.md (fixed before this run).
Exact formulas in the frequency domain, no simulation."""
import json, pathlib, sys, time
import numpy as np
from scipy.integrate import quad

ROOT = pathlib.Path(__file__).resolve().parents[1]
RES = ROOT / "results"
LN2 = np.log(2.0)
G_MM = 1e-3                     # g = 1 mm^-1 in um^-1, so that the rate per g^2 is in bits/s/mm^-2
# Table S1: (value, standard error)
P0 = dict(a_v=(157.1, 0.5), lam=(0.862, 0.005), G=(1.73, 0.03), tau2=(9.9, 0.3), tau1=(0.05, 0.0),
          D_n=(7.2e-4, 0.3e-4), tau_n=(11.75, 0.04))
N_MC = 10_000


def spectra(w, p):
    S = G_MM ** 2 * 2 * p["a_v"] * p["lam"] / (p["lam"] ** 2 + w ** 2)
    K = (p["G"] / p["tau1"]) / ((1 / p["tau2"] + 1j * w) * (1 / p["tau1"] + 1 / p["tau2"] + 1j * w))
    N = 2 * p["D_n"] / (1 / p["tau_n"] ** 2 + w ** 2)
    return S, K, N


def beta_closed(p):
    """Eq. (102) of MattinglyKaminoMachtaEmonet21, in bits/s/mm^-2."""
    t1, t2, tn, lam = p["tau1"], p["tau2"], p["tau_n"], p["lam"]
    num = t2 / tn ** 2 * (1 / t1 + 2 / t2 + lam) + lam * (1 / t1 + 1 / t2)
    den = (1 / t1 + 1 / t2) * (1 / t1 + 2 / t2) * (lam + 1 / t2) * (1 / t1 + 1 / t2 + lam)
    return 1 / LN2 * 0.25 * (G_MM / t1 * p["G"]) ** 2 * p["a_v"] / p["D_n"] * num / den


def beta_integral(p):
    f = lambda w: (lambda S, K, N: S * abs(K) ** 2 / N)(*spectra(w, p))
    pts = [1e-3, 1e-2, 0.1, 1, 10, 100, 1e3]
    v = sum(quad(f, a, b, limit=500, epsabs=0, epsrel=1e-12)[0] for a, b in zip([0] + pts, pts + [np.inf]))
    return 2 * v / (4 * np.pi) / LN2          # the integrand is even


class Grid:
    """Log grid on (0, inf) with trapezoid weights. Integrals over the real line are 2x the half line."""
    def __init__(self, n=20_000, lo=1e-7, hi=1e5):
        self.w = np.geomspace(lo, hi, n)
        dw = np.diff(self.w)
        self.q = np.zeros(n); self.q[:-1] += dw / 2; self.q[1:] += dw / 2
        self.q *= 2.0


def solve(p, grid, cls):
    """The best garbling of class 'A' or 'Z' (docs/E.md, E2). Returns (I_full, S, V_act, H)."""
    S, K, N = spectra(grid.w, p)
    q = grid.q
    R = S * np.abs(K) ** 2 / N
    I = lambda H: float((q * np.abs(H) ** 2 * R).sum() / (4 * np.pi) / LN2)
    V = lambda H: float((q * np.real(K * H) * S).sum() / (2 * np.pi))
    V_act = V(np.ones_like(grid.w))
    if cls == "A":
        Hm = lambda mu: np.minimum(1.0, mu * N / np.abs(K)) * np.exp(-1j * np.angle(K))
    else:
        Hm = lambda mu: np.clip(mu * N * np.real(K) / np.abs(K) ** 2, 0.0, 1.0)
    lo, hi = 0.0, 1.0
    while V(Hm(hi)) < V_act:
        hi *= 2.0
        if hi > 1e30:
            raise RuntimeError("no feasible garbling")
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if V(Hm(mid)) < V_act:
            lo = mid
        else:
            hi = mid
    H = Hm(hi)
    return I(np.ones_like(grid.w)), I(H), V_act, H, (I, V)


def check_optimum(p, cls, n_rand=1000, seed=3001):
    """E2a: random feasible garblings on a grid of 4000 frequencies never beat the optimum."""
    g = Grid(4000)
    I_full, S_opt, V_act, H, (I, V) = solve(p, g, cls)
    rng = np.random.default_rng([seed, ord(cls)])
    best, n_ok = np.inf, 0
    for k in range(n_rand):
        m = rng.uniform(0, 1, g.w.size) ** rng.uniform(0.2, 5)
        if k % 2:                       # half of the draws: smooth random curves on the log frequency axis
            x = np.log(g.w); c = rng.normal(size=8)
            m = 1 / (1 + np.exp(-sum(c[j] * np.cos(j * (x - x[0]) / (x[-1] - x[0]) * np.pi) for j in range(8))))
        if cls == "A":
            Hr = m * np.exp(1j * rng.uniform(-np.pi, np.pi) * rng.uniform(0, 1, g.w.size) ** 3 - 1j * np.angle(
                spectra(g.w, p)[1]) * rng.integers(0, 2))
        else:
            Hr = m
        v = V(Hr)
        if v < V_act:
            continue
        Hr = Hr * V_act / v
        n_ok += 1
        best = min(best, I(Hr))
    return dict(S_opt=S_opt, best_random=float(best), n_feasible=n_ok, passed=bool(best >= S_opt * (1 - 1e-9)))


def draw(rng):
    return {k: (v if s == 0 else rng.normal(v, s)) for k, (v, s) in P0.items()}


def main():
    t0 = time.time()
    p = {k: v for k, (v, s) in P0.items()}
    bc, bi = beta_closed(p), beta_integral(p)
    g = Grid()
    res = dict(beta_closed=bc, beta_integral=bi)
    for cls in ("A", "Z"):
        I_full, S, V_act, H, _ = solve(p, g, cls)
        res[cls] = dict(I_full=I_full, S=S, e=S / I_full, V_act=V_act)
    # grid check at the central values
    gf = Grid(200_000, 1e-8, 1e6)
    res["grid_check"] = {cls: solve(p, gf, cls)[1] / solve(p, gf, cls)[0] for cls in ("A", "Z")}
    res["grid_check_beta"] = solve(p, gf, "Z")[0]
    # Monte Carlo over Table S1
    rng = np.random.default_rng(3002)
    mc = {"beta": [], "eA": [], "eZ": []}
    for _ in range(N_MC):
        q = draw(rng)
        mc["beta"].append(beta_closed(q))
        for cls in ("A", "Z"):
            I_full, S, *_ = solve(q, g, cls)
            mc["e" + cls].append(S / I_full)
    ci = {k: [float(np.mean(v)), *np.percentile(v, [2.5, 97.5]).tolist()] for k, v in mc.items()}
    chk = {cls: check_optimum(p, cls) for cls in ("A", "Z")}
    # where the class Z optimum drops frequencies (Re K < 0) and where it is cut at 1
    S_, K_, N_ = spectra(g.w, p)
    w_neg = float(g.w[np.argmax(np.real(K_) < 0)])
    v = dict(E1a="agree" if abs(bc - bi) / bc < 1e-6 else "disagree",
             E1b="agrees" if 0.19 <= bc <= 0.25 else "disagrees",
             E2a="pass" if all(c["passed"] for c in chk.values()) else "fail",
             E2b="yes" if ci["eZ"][2] < 1 else "no")
    for cls in ("Z", "A"):
        lo, hi = ci["e" + cls][1], ci["e" + cls][2]
        v["E3a" if cls == "Z" else "E3b"] = "match" if (lo <= 0.51 and hi >= 0.37) else "differ"
    out = dict(verdicts=v, central=res, mc=ci, check=chk, omega_ReK_negative=w_neg, seconds=time.time() - t0)
    (RES / "e30_e_coli.json").write_text(json.dumps(out, indent=1))
    f = lambda x: f"{x[0]:.4f} [{x[1]:.4f}, {x[2]:.4f}]"
    L = ["# E30: semantic information of E. coli chemotaxis (niche E)", "", "Rules: docs/E.md. Model and Table S1: "
         "MattinglyKaminoMachtaEmonet21.", "",
         "| Rule | Value | Verdict |", "|---|---|---|",
         f"| E1a | β closed form {bc:.6f}, integral {bi:.6f} bits/s/mm⁻² | {v['E1a']} |",
         f"| E1b | β = {f(ci['beta'])} (Monte Carlo over Table S1) | {v['E1b']} |",
         f"| E2a | best random garbling / optimum: A {chk['A']['best_random'] / chk['A']['S_opt']:.4f} "
         f"({chk['A']['n_feasible']} feasible), Z {chk['Z']['best_random'] / chk['Z']['S_opt']:.4f} "
         f"({chk['Z']['n_feasible']} feasible) | {v['E2a']} |",
         f"| E2b | e_Z = {f(ci['eZ'])} | {v['E2b']} |",
         f"| E2c | e_A = {f(ci['eA'])} | descriptive |",
         f"| E3a | e_Z against 0.44 ± 0.07 | {v['E3a']} |",
         f"| E3b | e_A against 0.44 ± 0.07 | {v['E3b']} |", "",
         f"Central values: e_A = {res['A']['e']:.4f}, e_Z = {res['Z']['e']:.4f}. Grid check (200 000 points): "
         f"e_A = {res['grid_check']['A']:.4f}, e_Z = {res['grid_check']['Z']:.4f}. Re K < 0 above ω = {w_neg:.3f} rad/s. "
         f"Time {out['seconds']:.0f} s."]
    (RES / "e30_e_coli.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
