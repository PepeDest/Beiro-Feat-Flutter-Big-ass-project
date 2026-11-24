"""Niche B, step B2 (docs/B.md): stored semantic information S of KolchinskyWolpert18 in linear Gaussian systems.

B2a: Gaussian garblings, dx = 2, dy = 3, seeds 201-250. S_G (all 0 <= P <= I), S_proj (projections), I_C (drive
     projection). Sanity: dx = 1, dy = 3, seeds 401-420, where S_G = I_C is a theorem.
B2b: dx = dy = 1, seeds 301-330. S_NG over deterministic partitions of y (one threshold, two thresholds, |y| < t)
     against S_G = I(actual) of the Gaussian family.
Rules H1-H3, the sanity check and the expectations are in docs/B.md (fixed before this script ran).
"""
import json, pathlib, sys, time
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vlife.gaussian import stationary_cov  # noqa: E402
from vlife.semantic import (viability, syntactic_information, value_of_information, drive_information,  # noqa: E402
                            min_information)
from vlife.semantic_nonlinear import (scalar_parameters, entropy_x_tau, information, interval_cells,  # noqa: E402
                                      symmetric_cells)

TAU, MIN_DV, N_STARTS = 1.0, 1e-3, 32


def system(seed, dx, dy):
    rng = np.random.default_rng(seed); n = dx + dy
    A = rng.normal(size=(n, n))
    B = A @ A.T / n + 0.5 * np.eye(n) + 0.8 * (A - A.T) / 2
    D = np.diag(rng.uniform(0.3, 1.5, n))
    return B, D, stationary_cov(B, D)


def b2a_row(seed, dx, dy, families):
    B, D, S = system(seed, dx, dy)
    dV = value_of_information(B, D, S, dx, TAU)
    row = dict(seed=seed, dx=dx, dV=float(dV), I_act=float(syntactic_information(S, dx, np.eye(dy))),
               I_C=float(drive_information(B, D, S, dx, TAU)))
    if abs(dV) < MIN_DV:
        row["skipped"] = True
        return row
    for fam in families:
        best, _, n_best, n_feas = min_information(B, D, S, dx, TAU, fam, N_STARTS, np.random.default_rng([seed, 7]))
        row[f"S_{fam}"] = float(best); row[f"nbest_{fam}"] = int(n_best); row[f"nfeas_{fam}"] = int(n_feas)
    return row


def roots(fun, grid, iters=40):
    """Points where fun changes sign between neighbours of grid, refined by bisection."""
    vals = np.array([fun(t) for t in grid]); out = []
    for i in range(len(grid) - 1):
        lo, hi, flo = grid[i], grid[i + 1], vals[i]
        if np.sign(flo) == np.sign(vals[i + 1]) or not np.isfinite(flo * vals[i + 1]):
            continue
        for _ in range(iters):
            mid = (lo + hi) / 2; fm = fun(mid)
            lo, hi, flo = (mid, hi, fm) if np.sign(fm) == np.sign(flo) else (lo, mid, flo)
        out.append((lo + hi) / 2)
    return out


def b2b_row(seed):
    B, D, S = system(seed, 1, 1)
    a, b, q, c = scalar_parameters(B, D, S, TAU)
    V_act = viability(B, D, S, 1, np.eye(1), TAU)
    dV = value_of_information(B, D, S, 1, TAU)
    I_act = float(syntactic_information(S, 1, np.eye(1)))
    row = dict(seed=seed, dV=float(dV), I_act=I_act, S_G=I_act, c=float(c))
    if abs(dV) < MIN_DV:
        row["skipped"] = True
        return row
    g = lambda cells: -entropy_x_tau(cells, a, b, q, c) - V_act
    found = []                                                   # (family, parameters, I)
    for t in roots(lambda t: g(interval_cells([t])), np.linspace(-4, 4, 321)):
        found.append(("one threshold", [float(t)], information(interval_cells([t]), c)))
    for t in roots(lambda t: g(symmetric_cells(t)), np.linspace(0.02, 4, 200)):
        found.append(("|y| < t", [float(t)], information(symmetric_cells(t), c)))
    for t1 in np.linspace(-3, 3, 61)[:-1]:
        grid2 = np.linspace(t1 + 0.05, 3.5, 60)
        for t2 in roots(lambda t2: g(interval_cells([t1, t2])), grid2, iters=30):
            found.append(("two thresholds", [float(t1), float(t2)], information(interval_cells([t1, t2]), c)))
    row["n_feasible"] = len(found)
    if found:
        best = min(found, key=lambda f: f[2])
        row.update(S_NG=float(best[2]), best_family=best[0], best_params=best[1])
    else:
        row["S_NG"] = None
    return row


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    t0 = time.time()
    sanity = [b2a_row(s, 1, 3, ["general"]) for s in range(401, 421)]
    print(f"sanity done, {time.time() - t0:.0f} s", flush=True)
    a_rows = []
    for s in range(201, 251):
        a_rows.append(b2a_row(s, 2, 3, ["general", "rank1", "corank1"]))
        print(f"B2a system {s}: done, {time.time() - t0:.0f} s", flush=True)
    b_rows = []
    for s in range(301, 331):
        b_rows.append(b2b_row(s))
        print(f"B2b system {s}: done, {time.time() - t0:.0f} s", flush=True)

    san = [r for r in sanity if not r.get("skipped")]
    sanity_ok = all(abs(r["S_general"] - r["I_C"]) <= 1e-4 for r in san)
    A = [r for r in a_rows if not r.get("skipped")]
    for r in A:
        r["S_proj"] = min(r["S_rank1"], r["S_corank1"])
        r["gap1"] = r["S_proj"] - r["S_general"]; r["gap2"] = r["I_C"] - r["S_proj"]
    h1_fail = [r["seed"] for r in A if r["gap1"] > 1e-4]
    h2_fail = [r["seed"] for r in A if r["gap2"] > 1e-4]
    Bv = [r for r in b_rows if not r.get("skipped")]
    h3_fail = [r["seed"] for r in Bv if r["S_NG"] is not None and r["S_NG"] < r["S_G"] - 1e-3]
    verdict = dict(
        sanity="pass" if sanity_ok else "fail: the optimizer is not valid",
        H1="projections suffice" if not h1_fail else f"fails in {len(h1_fail)} of {len(A)} systems",
        H2="the drive projection is optimal" if not h2_fail else f"fails in {len(h2_fail)} of {len(A)} systems",
        H3="Gaussian garblings are optimal" if not h3_fail else f"not optimal in {len(h3_fail)} of {len(Bv)} systems")
    out = ROOT / "results"
    json.dump(dict(verdict=verdict, sanity=sanity, b2a=a_rows, b2b=b_rows, h1_fail=h1_fail, h2_fail=h2_fail,
                   h3_fail=h3_fail), open(out / "e21_b2_semantic.json", "w"), indent=1)
    eff = [r["S_general"] / r["I_act"] for r in A]
    L = ["# E21: stored semantic information in linear Gaussian systems (niche B, step B2)", "",
         "Rules: docs/B.md, B2.", "",
         f"Sanity (dx = 1, S_G = I_C): {verdict['sanity']}, {len(san)} systems, largest gap "
         f"{max(abs(r['S_general'] - r['I_C']) for r in san):.2e} nats.", "",
         "| Rule | Question | Verdict | Systems |", "|---|---|---|---|",
         f"| H1 | Do projections reach the minimum, S_proj = S_G? | {verdict['H1']} | {len(A)} (skipped {len(a_rows) - len(A)}) |",
         f"| H2 | Is the drive projection the best projection, I_C = S_proj? | {verdict['H2']} | {len(A)} |",
         f"| H3 | Do partitions fail to beat Gaussian garblings, S_NG >= S_G? | {verdict['H3']} | {len(Bv)} (skipped {len(b_rows) - len(Bv)}) |",
         "", "Description (B2a): semantic efficiency S_G / I_act: median "
         f"{np.median(eff):.3f}, range {min(eff):.3f} to {max(eff):.3f}. "
         f"Largest gap1 = {max(r['gap1'] for r in A):.2e}, largest gap2 = {max(r['gap2'] for r in A):.2e} nats.", "",
         "| Seed | ΔV | I_act | I_C | S_proj | S_G | starts at best (general) |", "|---|---|---|---|---|---|---|"]
    for r in A:
        L.append(f"| {r['seed']} | {r['dV']:+.4f} | {r['I_act']:.4f} | {r['I_C']:.4f} | {r['S_proj']:.4f} | "
                 f"{r['S_general']:.4f} | {r['nbest_general']} of {r['nfeas_general']} |")
    L += ["", "B2b (dx = dy = 1):", "", "| Seed | ΔV | c | S_G = I_act | S_NG | family | feasible partitions |",
          "|---|---|---|---|---|---|---|"]
    for r in Bv:
        sng = "none" if r["S_NG"] is None else f"{r['S_NG']:.4f}"
        L.append(f"| {r['seed']} | {r['dV']:+.4f} | {r['c']:+.3f} | {r['S_G']:.4f} | {sng} | {r.get('best_family', '')} | {r['n_feasible']} |")
    (out / "e21_b2_semantic.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[:12]))


if __name__ == "__main__":
    main()
