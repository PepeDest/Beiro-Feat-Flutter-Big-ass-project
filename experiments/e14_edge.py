"""E14 / S6e - colony-edge hypothesis of S6c. Rules: docs/S6.md (S6e).
Same run loop as grayscott2.run (numba, mutation at division), plus the edge index e of spots:
e = fraction of empty grid points (v <= V_THR) in a 41 x 41 periodic window around the spot centre."""
import argparse, time
import numpy as np
from scipy import ndimage
from common import RES, save_json
from vlife.grayscott import label_periodic, V_THR, NOISE
from vlife.grayscott2 import advance, seed_field, Tracker2, _seed_rng

W, EPS, MU = 41, 0.001, 0.114


def edge_index(v, lab, m):
    """e per label 1..m: empty fraction in a W x W periodic window at the label's centre of mass (wrap-aware enough for
    spots far smaller than the grid: the centre is the mean of the label's pixel positions)."""
    empty = ndimage.uniform_filter((v <= V_THR).astype(float), size=W, mode="wrap")
    cen = ndimage.center_of_mass(np.ones_like(v), lab, range(1, m + 1))
    n = v.shape[0]
    return np.array([empty[int(round(i)) % n, int(round(j)) % n] for i, j in cen])


def run_edge(seed, n=300, F=0.0367, k=0.0649, max_steps=150000, every=10, stall=2000, snap=500):
    _seed_rng(seed); mrng = np.random.default_rng([seed, 77])
    q = n // 4; centers = [(q, q), (q, 3 * q), (3 * q, q), (3 * q, 3 * q)]
    u, v, a, b = seed_field(n, centers, ("A",) * 4)
    tr = Tracker2(); best, best_t, t = 0, 0, 0
    div_auc_pairs = []      # (e of dividing parent, e of all spots in the previous frame) per division frame
    snaps = []              # (e array, type array) every `snap` steps
    prev = None             # (e, labels -> ids) of the previous frame
    while t < max_steps:
        advance(u, v, a, b, F, k, EPS, every, NOISE); t += every
        lab, m = label_periodic(v > V_THR)
        new_ids, daughters = tr.assign(lab, m, t)
        if daughters and prev is not None:
            e_prev, id_to_e = prev
            parents = {pid for _, pid in daughters}
            div_auc_pairs.append(([id_to_e[p] for p in parents if p in id_to_e], e_prev))
        for L, pid in daughters:
            if tr.info[pid]["last"]["z"] == 1 and mrng.random() < MU:
                r = lab == L; a[r], b[r] = b[r].copy(), a[r].copy()
        tr.record(lab, m, a, b, new_ids)
        if m:
            e = edge_index(v, lab, m)
            prev = (e, {new_ids[L]: e[L - 1] for L in range(1, m + 1)})
            if t % snap == 0:
                z = np.array([tr.info[new_ids[L]]["last"]["z"] for L in range(1, m + 1)])
                snaps.append((e, z))
        if m > best:
            best, best_t = m, t
        elif t - best_t >= stall:
            break
    return dict(seed=seed, div=div_auc_pairs, snaps=snaps, steps=t, n_end=m)


def auc(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) == 0 or len(y) == 0:
        return np.nan
    from scipy.stats import rankdata
    r = rankdata(np.concatenate([x, y]))
    return float((r[:len(x)].sum() - len(x) * (len(x) + 1) / 2) / (len(x) * len(y)))


def run_stats(r):
    X1 = np.nanmean([auc(d, allv) for d, allv in r["div"] if len(d)])
    x2 = [auc(e[z == 1], e[z == 0]) for e, z in r["snaps"] if (z == 1).sum() >= 10 and (z == 0).sum() >= 10]
    top, bot, share = [], [], []
    for e, z in r["snaps"]:
        if len(e) >= 20:
            q1, q3 = np.quantile(e, [0.25, 0.75]); top.append(z[e >= q3].mean()); bot.append(z[e <= q1].mean())
    for d, allv in r["div"]:
        if len(d) and len(allv) >= 8:
            share.append(np.mean(np.array(d) >= np.quantile(allv, 0.75)))
    return dict(X1=float(X1), X2=float(np.nanmean(x2)) if x2 else np.nan, fracA_top=float(np.mean(top)) if top else np.nan,
                fracA_bottom=float(np.mean(bot)) if bot else np.nan, div_share_top=float(np.mean(share)) if share else np.nan,
                n_snaps_X2=len(x2), steps=r["steps"], n_end=r["n_end"])


def boot(v, n=1000, rng=np.random.default_rng(0)):
    v = np.asarray(v, float); v = v[~np.isnan(v)]
    bs = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(n)]; lo, hi = np.percentile(bs, [2.5, 97.5])
    return [float(v.mean()), float(lo), float(hi)]


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--runs", type=int, default=8); ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--max_steps", type=int, default=150000)
    a = ap.parse_args(); t0 = time.time()
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(a.workers) as ex:
        rs = list(ex.map(run_edge, [9700 + i for i in range(a.runs)], *([[300] * a.runs, [0.0367] * a.runs, [0.0649] * a.runs, [a.max_steps] * a.runs])))
    S = [run_stats(r) for r in rs]
    R = {k: boot([s[k] for s in S]) for k in ("X1", "X2", "fracA_top", "fracA_bottom", "div_share_top")}
    v = dict(X1="yes" if R["X1"][1] > 0.6 else "no", X2="yes" if R["X2"][1] > 0.5 else "no")
    v["X3"] = "supported" if v["X1"] == "yes" and v["X2"] == "yes" else "not supported"
    save_json("e14_edge.json", dict(results=R, verdicts=v, per_run=S, seconds=time.time() - t0))
    f = lambda x: f"{x[0]:.3f} [{x[1]:.3f}, {x[2]:.3f}]"
    L = ["# E14 / S6e colony-edge test (auto-generated; rules in docs/S6.md, S6e)\n",
         f"Runs: {len(rs)} (300 x 300, all A, mu = {MU}, eps = {EPS}). Time {time.time() - t0:.0f} s.\n",
         "| Rule | Value [95% CI over runs] | Verdict |", "|---|---|---|",
         f"| X1: AUC, e of dividing parents vs all spots | {f(R['X1'])} | {v['X1']} |",
         f"| X2: AUC, e of type A vs type B | {f(R['X2'])} | {v['X2']} |",
         f"| X3: edge hypothesis | | {v['X3']} |", "", "Description:",
         f"- fraction of type A, top quartile of e: {f(R['fracA_top'])}; bottom quartile: {f(R['fracA_bottom'])}",
         f"- share of divisions by spots in the top quartile of e: {f(R['div_share_top'])} (0.25 if divisions ignored e)"]
    (RES / "e14_edge.md").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L))
