"""E13 / S6d - longer colonies on a larger grid, numba backend. Rules: docs/S6.md (S6d).
  --m0   : one run 300 x 300, mu = 0.2, 6000 steps; check of the mutation rate of the numba port
  --b1   : 4 runs 300 x 300, mu = 0.114 (backend check against S6c)
  (main) : 600 x 600, mu in {0.057, 0.114, 0.171, 0.228}, --runs per mu (default 8)
Each finished run is appended to results/e13_runs{tag}.pkl (not in the repository) so an interrupted main run keeps its data."""
import argparse, json, pickle, time
import numpy as np
from common import RES, save_json
from vlife.grayscott2 import run
from e11_selection import generations
from e12_mutation import analyse_run, wilson, boot

EPS, MUS = 0.001, (0.057, 0.114, 0.171, 0.228)
S6C = {round(t["mu"], 4): t["fracA"] for t in json.loads((RES / "e12_summary.json").read_text())["table"]}


def job(a):
    seed, mu, n, max_steps = a
    r = run(seed, EPS, types=("A",) * 4, n=n, max_steps=max_steps, stall=2000 if max_steps > 6000 else 10 ** 9, mu=mu)
    gen = generations(r["info"]); alive = r["final_ids"]
    r["gen_median_end"] = float(np.median([gen[i] for i in alive])) if alive else np.nan
    r["gen_max"] = int(max(gen.values())) if gen else 0
    return r


def all_daughters_T(r):
    """S6c post-hoc check: transmission over ALL daughters of A parents, against -mu E[w z]/w_bar (description)."""
    info = r["info"]; mu = r["mu"]; t_end = r["counts"][-1][0]
    kids = {}
    for i, d in info.items():
        if d["parent"] is not None:
            kids.setdefault(d["parent"], []).append(i)
    w, z, zd = [], [], []
    for p, d in info.items():
        if d["div"] is None or d["div"]["t"] > t_end - 3000:
            continue
        D = kids.get(p, []); zz = [(info[i]["div"] or info[i]["last"])["z"] for i in D]
        w.append(len(D)); z.append(d["div"]["z"]); zd.append(np.mean(zz) if zz else 0.0)
    w, z, zd = map(np.array, (w, z, zd))
    if len(w) == 0 or w.mean() == 0:
        return np.nan, np.nan
    wb = w.mean(); return float(np.mean(w * (zd - z)) / wb), float(-mu * np.mean(w * z) / wb)


def summarise(rs):
    A = [analyse_run(r) for r in rs]
    k, n = sum(x["n_A_to_B"] for x in A), sum(x["n_A_pairs"] for x in A)
    Tall = [all_daughters_T(r) for r in rs]
    return dict(mu=rs[0]["mu"], n_runs=len(rs), mut=wilson(k, n), n_pairs=n, fracA=boot([x["fracA"] for x in A]),
                S=boot([x["S"] for x in A]), T=boot([x["T"] for x in A]),
                T_all=float(np.nanmean([t[0] for t in Tall])), T_all_pred=float(np.nanmean([t[1] for t in Tall])),
                steps=float(np.median([x["steps"] for x in A])), n_end=float(np.median([x["n_end"] for x in A])),
                gen_median_end=float(np.median([r["gen_median_end"] for r in rs])), gen_max=int(max(r["gen_max"] for r in rs)))


def pending_jobs(jobs, done):
    """Jobs whose seed is not in the finished runs (resume after an interruption)."""
    seeds = {r["seed"] for r in done}
    return [j for j in jobs if j[0] not in seeds]


def se(ci):
    return (ci[2] - ci[1]) / 3.92


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--m0", action="store_true"); ap.add_argument("--b1", action="store_true")
    ap.add_argument("--runs", type=int, default=8); ap.add_argument("--workers", type=int, default=4); ap.add_argument("--n", type=int, default=600)
    ap.add_argument("--resume", action="store_true", help="keep the runs already in the pkl and run only the missing seeds")
    a = ap.parse_args(); t0 = time.time()
    from concurrent.futures import ProcessPoolExecutor, as_completed
    if a.m0:
        r = job((8999, 0.2, 300, 6000)); A = analyse_run(r)
        w = wilson(A["n_A_to_B"], A["n_A_pairs"]); v = "as set" if w[1] <= 0.2 <= w[2] else "not as set"
        save_json("e13_m0.json", dict(mutations=r["mutations"], fraction=w, verdict=v))
        txt = f"# S6d M0 (numba port, mu = 0.2, 6000 steps)\n\nA -> B among daughters of A parents: {A['n_A_to_B']} of {A['n_A_pairs']} = {w[0]:.3f} [{w[1]:.3f}, {w[2]:.3f}]; mutations drawn {r['mutations'][0]} of {r['mutations'][1]}. Verdict M0: {v}. Time {time.time() - t0:.0f} s.\n"
        (RES / "e13_m0.md").write_text(txt, encoding="utf-8"); print(txt); raise SystemExit
    tag = "_b1" if a.b1 else ""
    jobs = [(9500 + i, 0.114, 300, 150000) for i in range(4)] if a.b1 else \
           [(9000 + 100 * j + i, mu, a.n, 300000) for j, mu in enumerate(MUS) for i in range(a.runs)]
    pk = RES / f"e13_runs{tag}.pkl"; rs = []
    if a.resume and pk.exists():
        rs = pickle.load(open(pk, "rb")); jobs = pending_jobs(jobs, rs)
        print(f"resume: {len(rs)} runs kept, {len(jobs)} to run", flush=True)
    with ProcessPoolExecutor(a.workers) as ex:
        futs = [ex.submit(job, j) for j in jobs]
        for f in as_completed(futs):
            rs.append(f.result()); pickle.dump(rs, open(pk, "wb"))
            print(f"{len(rs)} runs in the pkl, {time.time() - t0:.0f} s", flush=True)
    table = [summarise([r for r in rs if r["mu"] == mu]) for mu in sorted({r["mu"] for r in rs})]
    if a.b1:
        t = table[0]; ref = S6C[0.114]
        v = dict(B1="consistent" if abs(t["fracA"][0] - ref[0]) < 2 * np.hypot(se(t["fracA"]), se(ref)) else "not consistent",
                 gen_median_end_300=t["gen_median_end"])
    else:
        b1 = json.loads((RES / "e13_summary_b1.json").read_text()) if (RES / "e13_summary_b1.json").exists() else None
        g300 = b1["table"][0]["gen_median_end"] if b1 else np.nan
        T = {round(t["mu"], 4): t for t in table}
        below = lambda mu: mu in T and T[mu]["fracA"][2] < S6C[mu][1]
        overlap = lambda mu: mu in T and not (T[mu]["fracA"][2] < S6C[mu][1] or T[mu]["fracA"][1] > S6C[mu][2])
        E1 = {mu: ("falls" if below(mu) else "does not fall") for mu in (0.171, 0.228)}
        E2 = "holds" if overlap(0.057) else ("falls" if below(0.057) else "rises")
        v = dict(E0=("yes" if np.nanmedian([t["gen_median_end"] for t in table]) >= 1.5 * g300 else "no") if b1 else "no B1 data",
                 E1=E1, E2=E2, E3="sharper" if all(x == "falls" for x in E1.values()) and E2 == "holds" else "not sharper",
                 E4=("met" if 0.228 in T and T[0.228]["fracA"][2] < 0.1 else "not met"),
                 M1=all(t["mut"][1] <= t["mu"] <= t["mut"][2] for t in table), gen_median_end_300=g300)
    save_json(f"e13_summary{tag}.json", dict(table=table, verdicts=v, n_runs=len(rs), seconds=time.time() - t0))
    g = lambda x: f"{x[0]:.3f} [{x[1]:.3f}, {x[2]:.3f}]"
    L = [f"# E13 / S6d report{' (B1 backend check)' if a.b1 else ''} (auto-generated; rules in docs/S6.md, S6d)\n",
         f"Runs: {len(rs)}. Time {time.time() - t0:.0f} s. Grid {300 if a.b1 else a.n}.\n",
         "| mu | A->B fraction | f (final fraction of A) | f at 300 x 300 (S6c) | S | T | T all daughters / predicted | median steps | median generation at end (max) |",
         "|---|---|---|---|---|---|---|---|---|"]
    L += [f"| {t['mu']:.4f} | {g(t['mut'])} | {g(t['fracA'])} | {g(S6C.get(round(t['mu'], 4), [np.nan] * 3))} | {t['S'][0]:+.4f} | {t['T'][0]:+.4f} | "
          f"{t['T_all']:+.4f} / {t['T_all_pred']:+.4f} | {t['steps']:.0f} | {t['gen_median_end']:.0f} ({t['gen_max']}) |" for t in table]
    L += ["", f"Verdicts: {v}"]
    (RES / f"e13_report{tag}.md").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L))
