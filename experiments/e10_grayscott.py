"""E10 / ROADMAP S6 - Gray-Scott spots: growth law, native heredity, dye heredity, Price terms. Rules: docs/S6.md.
  --pilot : P0, spot replication check with the parameter fallback list; writes results/e10_params.json
  (default): 8 runs with the chosen parameters, rules R1-R4."""
import argparse, json, pickle, time
import numpy as np
from scipy.stats import spearmanr
from common import RES, save_json
from vlife.grayscott import run
from vlife.growthlaw import growth_fits

FALLBACK = [(0.0367, 0.0649), (0.035, 0.065), (0.030, 0.062)]


def job(a):
    seed, F, k, max_steps, stall = a
    return run(seed, F, k, max_steps=max_steps, stall=stall)


def pairs(r):
    info = r["info"]; out = []
    for i, d in info.items():
        p = d["parent"]
        if p is not None and d["div"] is not None and info[p]["div"] is not None:
            out.append((info[p]["div"]["area"], d["div"]["area"], info[p]["div"]["z"], d["div"]["z"]))
    return np.array(out).reshape(-1, 4)


def growth(r):
    """Fix #11: shared fit (vlife.growthlaw). Same window and same R2_exp, R2_pow, power as before; adds t0_fit, power_t0."""
    t, N = np.array(r["counts"]).T.astype(float)
    return growth_fits(t, N)


def price(r):
    info = r["info"]; divs = {i: d for i, d in info.items() if d["div"] is not None}
    cyc = [divs[i]["div"]["t"] - divs[i]["born"] for i in divs if divs[i]["parent"] is not None]
    if not cyc:
        return None
    t_end = r["counts"][-1][0]; cut = t_end - 2 * np.median(cyc)
    w, zp, dz = [], [], []
    for p, d in divs.items():
        if d["div"]["t"] > cut:
            continue
        kids = [i for i, x in info.items() if x["parent"] == p]
        kd = [info[i]["div"]["z"] - d["div"]["z"] for i in kids if info[i]["div"] is not None]
        w.append(len(kd)); zp.append(d["div"]["z"]); dz.append(np.mean(kd) if kd else 0.0)
    w, zp, dz = map(np.array, (w, zp, dz))
    if w.sum() == 0:
        return None
    wb = w.mean()
    return dict(S=float(np.mean(w * zp) / wb - zp.mean()), T=float(np.mean(w * dz) / wb), n_parents=int(len(w)),
                cycle_median=float(np.median(cyc)))


def run_boot(per_run, fn, n_boot=1000, rng=np.random.default_rng(0)):
    pt = fn(list(range(len(per_run))))
    bs = [fn(list(rng.integers(0, len(per_run), len(per_run)))) for _ in range(n_boot)]
    lo, hi = np.nanpercentile(bs, [2.5, 97.5]); return [float(pt), float(lo), float(hi)]


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--pilot", action="store_true"); ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args(); t0 = time.time()
    from concurrent.futures import ProcessPoolExecutor
    if a.pilot:
        L = ["# S6 pilot P0 (spot replication; plan in docs/S6.md)\n", "| F | k | spots after 20000 steps | divisions | pass |", "|---|---|---|---|---|"]
        chosen = None
        for F, k in FALLBACK:
            r = run(2026, F, k, max_steps=20000, stall=10 ** 9)
            n = r["counts"][-1][1]; ok = n >= 32
            L.append(f"| {F} | {k} | {n} | {len(r['divisions'])} | {'yes' if ok else 'no'} |")
            if ok:
                chosen = dict(F=F, k=k); break
        (RES / "e10_pilot.md").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L), f"\n{time.time() - t0:.0f}s")
        if chosen:
            (RES / "e10_params.json").write_text(json.dumps(chosen))
    else:
        p = json.loads((RES / "e10_params.json").read_text())
        with ProcessPoolExecutor(a.workers) as ex:
            runs = list(ex.map(job, [(2026 + i, p["F"], p["k"], 100000, 2000) for i in range(8)]))
        print(f"runs done in {time.time() - t0:.0f}s", flush=True)
        pickle.dump(runs, open(RES / "e10_runs.pkl", "wb"))
        G = [growth(r) for r in runs]; PR = [pairs(r) for r in runs]; PC = [price(r) for r in runs]
        nexp = sum(g["R2_exp"] > g["R2_pow"] for g in G if g); npow = sum(g["R2_pow"] > g["R2_exp"] for g in G if g)
        R1 = "exponential" if nexp >= 6 else "polynomial" if npow >= 6 else "mixed"
        pool = lambda ids, c1, c2: spearmanr(np.vstack([PR[i] for i in ids])[:, c1], np.vstack([PR[i] for i in ids])[:, c2])[0]
        R2 = run_boot(PR, lambda ids: pool(ids, 0, 1)); R3 = run_boot(PR, lambda ids: pool(ids, 2, 3))
        slope = lambda ids: np.polyfit(np.vstack([PR[i] for i in ids])[:, 2], np.vstack([PR[i] for i in ids])[:, 3], 1)[0]
        F4 = run_boot(PR, slope)
        ok = [c for c in PC if c]; S4 = run_boot(ok, lambda ids: np.mean([ok[i]["S"] for i in ids]))
        T4 = run_boot(ok, lambda ids: np.mean([ok[i]["T"] for i in ids]))
        v = dict(R1=R1, R2="native heredity" if R2[1] > 0 else "none found", R3="pipeline detects heredity" if R3[1] > 0.5 else "not detected")
        n_pairs = int(sum(len(x) for x in PR))
        res = dict(params=p, growth=G, R2=R2, R3=R3, fidelity_slope=F4, S=S4, T=T4, n_pairs=n_pairs, price_runs=ok,
                   merges=[r["merges"] for r in runs], verdicts=v)
        save_json("e10_summary.json", res)
        f = lambda x: f"{x[0]:+.3f} [{x[1]:+.3f}, {x[2]:+.3f}]"
        L = ["# E10 / S6 report (auto-generated; rules in docs/S6.md)\n", f"Parameters {p}. Runs: 8. Parent-daughter pairs: {n_pairs}.\n",
             "| Rule | Value [95% CI] | Verdict |", "|---|---|---|",
             f"| R1: growth law (runs where exp fit wins / power fit wins) | {nexp} / {npow}; power exponent median {np.median([g['power'] for g in G if g]):.2f} (with fitted t0: {np.median([g['power_t0'] for g in G if g]):.2f}, description only) | {R1} |",
             f"| R2: rho(parent area, daughter area) | {f(R2)} | {v['R2']} |",
             f"| R3: rho(parent dye, daughter dye) | {f(R3)} | {v['R3']} |",
             f"| R4: fidelity slope (dye) | {f(F4)} | measured |",
             f"| R4: Price selection S / transmission T | {f(S4)} / {f(T4)} | measured |",
             "\nPer run growth: " + "; ".join(f"N_max {g['N_max']}, R2 exp {g['R2_exp']:.3f}, R2 pow {g['R2_pow']:.3f}, p {g['power']:.2f}" for g in G if g),
             f"\nMerges per run: {[r['merges'] for r in runs]}"]
        (RES / "e10_report.md").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L))
