"""E12 / S6c - one-way mutation A -> B at division, error threshold. Rules: docs/S6.md (S6c). GPU + CPU workers."""
import argparse, pickle, time
import numpy as np
from common import RES, save_json
from vlife.gs_opencl import run
from e11_selection import generations

MU_C, MU_C_EXP, EPS = 0.114, 0.088, 0.001
FACTORS = (0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0)


def job(a):
    seed, mu = a
    return run(seed, EPS, types=("A",) * 4, max_steps=150000, stall=2000, mu=mu)


def analyse_run(r):
    info = r["info"]; t_end = r["counts"][-1][0]; gen = generations(info); mu = r["mu"]
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
    S, T, Tp, W = [], [], [], []
    for g, L in by.items():
        w, z, zd = (np.array(x, float) for x in zip(*L))
        if len(L) < 5 or w.mean() == 0:
            continue
        wb = w.mean(); S.append(np.mean(w * z) / wb - z.mean()); T.append(np.mean(w * (zd - z)) / wb)
        Tp.append(-mu * np.mean(w * z) / wb); W.append(len(L))
    # all daughters of type-A parents (also those that do not divide again: counting only dividing daughters misses
    # the slower B daughters); type at their own division, else at their last frame
    pA = [(d["div"] or d["last"])["z"] for d in info.values() if d["parent"] is not None
          and info[d["parent"]]["div"] is not None and info[d["parent"]]["div"]["z"] == 1]
    t_last, m, nA = r["counts"][-1]
    avg = lambda x: float(np.average(x, weights=W)) if W else np.nan
    return dict(mu=mu, S=avg(S), T=avg(T), Tpred=avg(Tp), fracA=nA / m if m else np.nan, n_A_pairs=len(pA),
                n_A_to_B=int(sum(1 for z in pA if z == 0)), steps=int(t_last), n_end=int(m))


def wilson(k, n, z=1.96):
    if n == 0:
        return [np.nan, np.nan, np.nan]
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [float(p), float(c - h), float(c + h)]


def boot(v, n=1000, rng=np.random.default_rng(0)):
    v = np.asarray(v, float); v = v[~np.isnan(v)]; bs = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(n)]
    lo, hi = np.percentile(bs, [2.5, 97.5]); return [float(v.mean()), float(lo), float(hi)]


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int, default=5); ap.add_argument("--runs", type=int, default=20)
    ap.add_argument("--tag", default="", help="suffix of the output files (the S6f rerun uses _hash2)")
    a = ap.parse_args(); t0 = time.time()
    mus = [round(MU_C * f, 4) for f in FACTORS]
    jobs = [(7000 + 100 * j + i, mu) for j, mu in enumerate(mus) for i in range(a.runs)]
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(a.workers) as ex:
        rs = list(ex.map(job, jobs, chunksize=1))
    print(f"{len(rs)} runs done in {time.time() - t0:.0f} s", flush=True)
    pickle.dump(rs, open(RES / f"e12_runs{a.tag}.pkl", "wb"))
    A = [analyse_run(r) for r in rs]; table = []
    for mu in mus:
        L = [x for x in A if x["mu"] == mu]
        k, n = sum(x["n_A_to_B"] for x in L), sum(x["n_A_pairs"] for x in L)
        table.append(dict(mu=mu, mut=wilson(k, n), n_pairs=n, fracA=boot([x["fracA"] for x in L]), S=boot([x["S"] for x in L]),
                          T=boot([x["T"] for x in L]), Tpred=float(np.nanmean([x["Tpred"] for x in L])),
                          steps=float(np.median([x["steps"] for x in L])), n_end=float(np.median([x["n_end"] for x in L]))))
    M1 = all(t["mut"][1] <= t["mu"] <= t["mut"][2] for t in table if t["mu"] > 0 and t["n_pairs"] > 0)
    M2 = all(abs(t["T"][0] - t["Tpred"]) <= 0.2 * abs(t["Tpred"]) for t in table if t["mu"] >= 0.25 * MU_C - 1e-9)
    low = [t for t in table if t["mu"] <= 0.5 * MU_C + 1e-9]; high = [t for t in table if t["mu"] >= 2 * MU_C - 1e-9]
    M3 = all(t["fracA"][1] > 0.5 for t in low) and all(t["fracA"][2] < 0.1 for t in high)
    f = np.array([t["fracA"][0] for t in table]); m_ = np.array(mus); mu_hat = np.nan
    for i in range(len(f) - 1):
        if f[i] >= 0.1 > f[i + 1]:
            mu_hat = float(m_[i] + (f[i] - 0.1) / (f[i] - f[i + 1]) * (m_[i + 1] - m_[i])); break
    M4 = ("consistent with mean field" if 0.5 * MU_C <= mu_hat <= 2 * MU_C else "not consistent") if not np.isnan(mu_hat) else "no crossing in the grid"
    closer = "regular cycles (0.114)" if np.isnan(mu_hat) or abs(mu_hat - MU_C) <= abs(mu_hat - MU_C_EXP) else "exponential cycles (0.088)"
    v = dict(M1="as set" if M1 else "not as set", M2="matches" if M2 else "does not match", M3="threshold present" if M3 else "no clear threshold",
             M4=M4, closer=closer, mu_hat=mu_hat)
    save_json(f"e12_summary{a.tag}.json", dict(table=table, verdicts=v))
    g = lambda x: f"{x[0]:.3f} [{x[1]:.3f}, {x[2]:.3f}]"
    out = ["# E12 / S6c report (auto-generated; rules in docs/S6.md)\n", f"Runs: {len(rs)} ({a.runs} per mu). mu_c predicted 0.114 (regular cycles), 0.088 (exponential cycles).\n",
           "| mu | measured A->B fraction | final fraction of A | S per generation | T measured | T predicted | median steps | median spots |", "|---|---|---|---|---|---|---|---|"]
    out += [f"| {t['mu']:.4f} | {g(t['mut'])} ({t['n_pairs']}) | {g(t['fracA'])} | {t['S'][0]:+.4f} | {t['T'][0]:+.4f} | {t['Tpred']:+.4f} | {t['steps']:.0f} | {t['n_end']:.0f} |" for t in table]
    out += ["", f"- M1 (mutation as set): {v['M1']}", f"- M2 (T matches the mutation): {v['M2']}", f"- M3 (error threshold): {v['M3']}",
            f"- M4: mu where f crosses 0.1 = {mu_hat:.4f}: {v['M4']}; closer mean-field value: {closer}"]
    (RES / f"e12_report{a.tag}.md").write_text("\n".join(out) + "\n", encoding="utf-8"); print("\n".join(out))
