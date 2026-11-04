"""E11 / S6b - heritable type that changes division; per-generation Price terms; neutral control. Rules: docs/S6.md (S6b).
  --pilot : choose eps* from single-type colonies;  (default): 32 runs at eps* and 32 at eps = 0, all on the GPU."""
import argparse, json, pickle, time
import numpy as np
from common import RES, save_json
from vlife.gs_opencl import run

EPS_GRID = (0.001, 0.002, 0.003)


def job(a):
    return run(a[0], a[1], types=a[2], max_steps=a[3], stall=a[4])


def cycle_median(r):
    info = r["info"]
    c = [d["div"]["t"] - d["born"] for d in info.values() if d["parent"] is not None and d["div"] is not None]
    return float(np.median(c)) if c else np.nan


def generations(info):
    g = {}
    for i in info:
        j, n = i, 0
        while info[j]["parent"] is not None:
            j = info[j]["parent"]; n += 1
        g[i] = n
    return g


def price_run(r):
    info = r["info"]; t_end = r["counts"][-1][0]; gen = generations(info)
    kids = {}
    for i, d in info.items():
        if d["parent"] is not None:
            kids.setdefault(d["parent"], []).append(i)
    by = {}
    for p, d in info.items():
        if d["div"] is None or d["div"]["t"] > t_end - 3000:
            continue
        D = [i for i in kids.get(p, []) if info[i]["div"] is not None]
        zD = np.mean([info[i]["div"]["z"] for i in D]) if D else 0.0
        by.setdefault(gen[p], []).append((len(D), d["div"]["z"], zD))
    S, T, W, err = [], [], [], 0.0
    for g, L in by.items():
        w, z, zd = (np.array(x, float) for x in zip(*L))
        if len(L) < 5 or w.mean() == 0:
            continue
        wb = w.mean(); s = np.mean(w * z) / wb - z.mean(); t = np.mean(w * (zd - z)) / wb
        dz = np.sum(w * zd) / np.sum(w) - z.mean()          # change of the mean trait, from the actual daughters
        err = max(err, abs(dz - (s + t))); S.append(s); T.append(t); W.append(len(L))
    pairs = [(info[d["parent"]]["div"]["z"], d["div"]["z"]) for d in info.values()
             if d["parent"] is not None and d["div"] is not None and info[d["parent"]]["div"] is not None]
    t_last, m, nA = r["counts"][-1]
    return dict(S=float(np.average(S, weights=W)) if W else np.nan, T=float(np.average(T, weights=W)) if W else np.nan,
                identity_err=float(err), n_gen=len(W), same=int(sum(a == b for a, b in pairs)), pairs=len(pairs),
                fracA=nA / m if m else np.nan)


def growth(r):
    t, N = np.array([(c[0], c[1]) for c in r["counts"]], float).T; Nmax = N.max()
    i0 = np.argmax(N >= 8); i1 = np.argmax(N >= 0.3 * Nmax)
    if i1 <= i0 + 3:
        return None
    tt, nn = t[i0:i1 + 1], np.log(N[i0:i1 + 1])
    r2 = lambda x: 1 - np.sum((nn - np.polyval(np.polyfit(x, nn, 1), x)) ** 2) / np.sum((nn - nn.mean()) ** 2)
    return dict(R2_exp=float(r2(tt)), R2_pow=float(r2(np.log(tt))), power=float(np.polyfit(np.log(tt), nn, 1)[0]),
                N_max=int(Nmax), N_window=[int(N[i0]), int(N[i1])])


def boot(vals, n=1000, rng=np.random.default_rng(0)):
    v = np.asarray(vals, float); v = v[~np.isnan(v)]; pt = v.mean()
    bs = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(n)]; lo, hi = np.percentile(bs, [2.5, 97.5])
    return [float(pt), float(lo), float(hi)]


def pilot(workers):
    t0 = time.time()
    from concurrent.futures import ProcessPoolExecutor
    jobs = [(100 + i, 0.0, ("B",) * 4, 20000, 10 ** 9) for i in range(4)]
    jobs += [(200 + 10 * j + i, e, ("A",) * 4, 20000, 10 ** 9) for j, e in enumerate(EPS_GRID) for i in range(4)]
    with ProcessPoolExecutor(workers) as ex:
        rs = list(ex.map(job, jobs))
    cB = np.median([cycle_median(r) for r in rs[:4]]); nB = np.mean([r["counts"][-1][1] for r in rs[:4]])
    L = ["# S6b pilot (choose eps*; plan in docs/S6.md)\n",
         f"Type B colonies (no effect): median cycle {cB:.0f} steps, mean spots at 20000 steps {nB:.0f}\n",
         "| eps | median cycle A | change against B | mean spots A at 20000 | passes |", "|---|---|---|---|---|"]
    chosen = None
    for j, e in enumerate(EPS_GRID):
        grp = rs[4 + 4 * j: 8 + 4 * j]
        cA = np.median([cycle_median(r) for r in grp]); nA = np.mean([r["counts"][-1][1] for r in grp])
        ch = cA / cB - 1; ok = abs(ch) >= 0.10 and nA >= 32
        L.append(f"| {e} | {cA:.0f} | {ch:+.1%} | {nA:.0f} | {'yes' if ok else 'no'} |")
        if ok and chosen is None:
            chosen = dict(eps=e, change=float(ch), predicted_sign=(1 if ch < 0 else -1))
    L.append(f"\nChosen: {chosen}  ({time.time() - t0:.0f} s)")
    (RES / "e11_pilot.md").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L))
    if chosen:
        (RES / "e11_eps.json").write_text(json.dumps(chosen))


def main(workers, runs):
    t0 = time.time()
    from concurrent.futures import ProcessPoolExecutor
    ch = json.loads((RES / "e11_eps.json").read_text()); sign = ch["predicted_sign"]
    ty = lambda i: ("A", "B", "B", "A") if i % 2 == 0 else ("B", "A", "A", "B")
    jobs = [(3000 + i, ch["eps"], ty(i), 150000, 2000) for i in range(runs)]
    jobs += [(5000 + i, 0.0, ty(i), 150000, 2000) for i in range(runs)]
    with ProcessPoolExecutor(workers) as ex:
        rs = list(ex.map(job, jobs))
    print(f"runs done in {time.time() - t0:.0f} s", flush=True)
    pickle.dump(rs, open(RES / "e11_runs.pkl", "wb"))
    sel, ctl = rs[:runs], rs[runs:]
    P = {"selection": [price_run(r) for r in sel], "control": [price_run(r) for r in ctl]}
    R = {}
    for k, L in P.items():
        R[k] = dict(S=boot([x["S"] for x in L]), T=boot([x["T"] for x in L]), fracA=boot([x["fracA"] for x in L]),
                    fidelity=sum(x["same"] for x in L) / max(sum(x["pairs"] for x in L), 1),
                    pairs=sum(x["pairs"] for x in L), identity_err=max(x["identity_err"] for x in L))
    G = [growth(r) for r in sel]
    nexp = sum(g["R2_exp"] > g["R2_pow"] for g in G if g); npow = sum(g["R2_pow"] > g["R2_exp"] for g in G if g)
    S, C = R["selection"], R["control"]
    pos = S["S"][1] > 0; neg = S["S"][2] < 0
    lab_sel = "selection detected" if (pos if sign > 0 else neg) else "wrong sign" if (neg if sign > 0 else pos) else "not detected"
    h4 = "yes" if (S["fracA"][1] > 0.5 if sign > 0 else S["fracA"][2] < 0.5) else "no"
    if not (C["fracA"][1] <= 0.5 <= C["fracA"][2]):
        h4 += " (control not at 0.5)"
    v = dict(H1="high fidelity" if min(S["fidelity"], C["fidelity"]) >= 0.95 else "low fidelity",
             H2="control clean" if C["S"][1] <= 0 <= C["S"][2] else "control not clean", H3=lab_sel, H4=h4,
             H5="exact" if max(S["identity_err"], C["identity_err"]) < 1e-9 else "not exact",
             H6="exponential" if nexp >= 0.75 * len(G) else "polynomial" if npow >= 0.75 * len(G) else "mixed")
    save_json("e11_summary.json", dict(eps=ch, results=R, growth=G, verdicts=v))
    f = lambda x: f"{x[0]:+.4f} [{x[1]:+.4f}, {x[2]:+.4f}]"
    g0 = next((g for g in G if g), None)
    out = ["# E11 / S6b report (auto-generated; rules in docs/S6.md)\n",
           f"eps* = {ch['eps']} (pilot change of cycle time {ch['change']:+.1%}, predicted sign of S: {sign:+d}). Runs: {runs} + {runs}.\n",
           "| Rule | Selection runs | Control runs (eps = 0) | Verdict |", "|---|---|---|---|",
           f"| H1: fidelity | {S['fidelity']:.4f} ({S['pairs']} pairs) | {C['fidelity']:.4f} ({C['pairs']} pairs) | {v['H1']} |",
           f"| H2/H3: selection term S | {f(S['S'])} | {f(C['S'])} | {v['H2']}; {v['H3']} |",
           f"| transmission term T | {f(S['T'])} | {f(C['T'])} | measured |",
           f"| H4: final fraction of type A | {f(S['fracA'])} | {f(C['fracA'])} | {v['H4']} |",
           f"| H5: max error of the Price identity | {S['identity_err']:.1e} | {C['identity_err']:.1e} | {v['H5']} |",
           f"| H6: growth law (exp wins / power wins) | {nexp} / {npow}, power median {np.median([g['power'] for g in G if g]):.2f}, window N {g0['N_window'] if g0 else '-'} | | {v['H6']} |"]
    (RES / "e11_report.md").write_text("\n".join(out) + "\n", encoding="utf-8"); print("\n".join(out))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--workers", type=int, default=4); ap.add_argument("--runs", type=int, default=32)
    a = ap.parse_args()
    pilot(a.workers) if a.pilot else main(a.workers, a.runs)
