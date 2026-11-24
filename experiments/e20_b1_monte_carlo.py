"""Niche B, step B1 (docs/B.md): Monte Carlo check of the closed form of V(P) and I_P(X_0; Y_0).
The start is sampled with the garbling itself, and the dynamics use Euler-Maruyama. Pass criterion in docs/B.md."""
import json, pathlib, sys, time
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vlife.gaussian import stationary_cov  # noqa: E402
from vlife.semantic import garbling_matrix, projection, syntactic_information, viability  # noqa: E402

DX, DY, N, BATCHES, DT, TAUS = 2, 3, 100_000, 20, 5e-4, (0.5, 1.0)


def system(seed):
    rng = np.random.default_rng(seed); n = DX + DY
    A = rng.normal(size=(n, n))
    B = A @ A.T / n + 0.5 * np.eye(n) + 0.8 * (A - A.T) / 2
    D = np.diag(rng.uniform(0.3, 1.5, n))
    return B, D, stationary_cov(B, D), rng


def sqrtm(M):
    w, U = np.linalg.eigh(M); return (U * np.sqrt(w)) @ U.T


def sample_start(S, kind, K, SN, rng):
    """x_0, y_0 under the intervention: Z = K Sigma_Y^{-1/2} y + noise, x_0 from the actual p(x_0 | z)."""
    Sx, Sxy, Sy = S[:DX, :DX], S[:DX, DX:], S[DX:, DX:]
    y = rng.normal(size=(N, DY)) @ np.linalg.cholesky(Sy).T
    if kind == "actual":
        Kw, SNz = np.eye(DY), np.zeros((DY, DY))
    elif kind == "full":
        return rng.normal(size=(N, DX)) @ np.linalg.cholesky(Sx).T, y
    else:
        Kw, SNz = K, SN
    Ky = Kw @ np.linalg.inv(sqrtm(Sy))                       # Z = Ky y + noise
    z = y @ Ky.T + (rng.normal(size=(N, len(SNz))) @ np.linalg.cholesky(SNz + 1e-300 * np.eye(len(SNz))).T if SNz.any() else 0)
    Szz = Ky @ Sy @ Ky.T + SNz; Sxz = Sxy @ Ky.T
    G = Sxz @ np.linalg.pinv(Szz); Sc = Sx - G @ Sxz.T
    x = z @ G.T + rng.normal(size=(N, DX)) @ np.linalg.cholesky((Sc + Sc.T) / 2 + 1e-14 * np.eye(DX)).T
    return x, y


def batch_stats(x, y=None):
    out = []
    for b in np.array_split(np.arange(N), BATCHES):
        if y is None:
            out.append(-0.5 * (DX * np.log(2 * np.pi * np.e) + np.linalg.slogdet(np.cov(x[b].T))[1]))
        else:
            Sj = np.cov(np.hstack([x[b], y[b]]).T)
            out.append(0.5 * (np.linalg.slogdet(Sj[:DX, :DX])[1] + np.linalg.slogdet(Sj[DX:, DX:])[1] - np.linalg.slogdet(Sj)[1]))
    out = np.array(out)
    return float(out.mean()), float(out.std(ddof=1) / np.sqrt(BATCHES))


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    t0 = time.time(); rows = []
    for seed in (101, 102, 103, 104):
        B, D, S, rng = system(seed)
        U = rng.normal(size=(DY, 1)); K = rng.normal(size=(2, DY)); SN = np.diag(rng.uniform(0.2, 3.0, 2))
        Ps = dict(actual=np.eye(DY), full=np.zeros((DY, DY)), projection=projection(U), garbling=garbling_matrix(K, SN, S[DX:, DX:]))
        for kind, P in Ps.items():
            Kk = U.T if kind == "projection" else K
            SNk = np.zeros((1, 1)) if kind == "projection" else SN
            x, y = sample_start(S, kind, Kk, SNk, rng)
            I_mc, I_se = batch_stats(x, y)
            rows.append(dict(seed=seed, kind=kind, quantity="I", tau=0.0, formula=syntactic_information(S, DX, P), mc=I_mc, se=I_se))
            z = np.hstack([x, y]); L = np.linalg.cholesky(2 * D * DT); t = 0.0
            for tau in TAUS:
                for _ in range(int(round((tau - t) / DT))):
                    z = z - DT * z @ B.T + rng.normal(size=z.shape) @ L.T
                t = tau
                V_mc, V_se = batch_stats(z[:, :DX])
                rows.append(dict(seed=seed, kind=kind, quantity="V", tau=tau, formula=viability(B, D, S, DX, P, tau), mc=V_mc, se=V_se))
        print(f"system {seed}: done, {time.time() - t0:.0f} s", flush=True)
    for r in rows:
        r["z"] = (r["mc"] - r["formula"]) / r["se"]
    within3 = sum(abs(r["z"]) <= 3 for r in rows); beyond5 = sum(abs(r["z"]) > 5 for r in rows)
    verdict = "pass" if within3 >= 45 and beyond5 == 0 else "fail"
    out = ROOT / "results"
    json.dump(dict(rows=rows, within3=within3, beyond5=beyond5, n_checks=len(rows), verdict=verdict),
              open(out / "e20_b1_monte_carlo.json", "w"), indent=1)
    L = ["# E20: Monte Carlo check of the B1 closed form (niche B)", "", "Criterion and method: docs/B.md, B1.", "",
         f"Checks within 3 SE: {within3} of {len(rows)}. Beyond 5 SE: {beyond5}. Verdict: **{verdict}**.", "",
         "| System | Intervention | Quantity | τ | Formula | Monte Carlo ± SE | z |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['seed']} | {r['kind']} | {r['quantity']} | {r['tau']:g} | {r['formula']:+.4f} | {r['mc']:+.4f} ± {r['se']:.4f} | {r['z']:+.2f} |")
    (out / "e20_b1_monte_carlo.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[:6]))


if __name__ == "__main__":
    main()
