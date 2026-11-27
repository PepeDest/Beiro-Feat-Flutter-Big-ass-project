"""Niche F (docs/F.md): a map of the free choices of CLD on the 840 units of C2.
Rules and expectations are in docs/F.md (fixed before any run).

    python experiments/e28_f_cld_map.py --export     # writes cluster/data/f_units.json from results/e26_v_dataset.pkl
    python experiments/e28_f_cld_map.py OUT_DIR      # the analysis, after the cluster run

The cluster runner calls tasks() and run_task(). One task is one unit.
"""
import json, pathlib, sys
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vlife.nonlinear import Unit, initial, run, step  # noqa: E402

DATA = ROOT / "cluster" / "data" / "f_units.json"
N_WALK, N_SMALL, N_GRID, T_BURN, DT = 80_000, 20_000, 41, 50.0, 0.01
BINS = (20, 40, 80)
FUNCS = ("js", "kl_pq", "kl_qp", "hel2", "tv")
PSEUDO = 0.5                  # walkers added to each cell for the two KL divergences (docs/F.md)


def export():
    import pickle
    draws = pickle.load(open(ROOT / "results" / "e26_v_dataset.pkl", "rb"))
    units = [dict(seed=int(s), i=int(r["i"]), kind=r["kind"], p=r["p"], V=float(r["V_on"]), tau_star=float(d["tau_star"]))
             for s, d in sorted(draws.items()) for r in d["rows"]]
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(units))
    print("wrote", DATA, len(units), "units")


def tasks(smoke=False):
    units = json.loads(DATA.read_text())
    if smoke:
        units = sorted([u for u in units if u["seed"] == 2026], key=lambda u: u["V"])[:4]
    out = []
    for u in units:
        T = max(u["tau_star"], u["V"])
        out.append(dict(job="f", name=f"f_{u['seed']}_{u['i']:03d}", unit=u, cost=T / DT * 2 * N_WALK * 1.13e-7,
                        smoke=smoke))
    return out


def divergences(counts):
    """The five functionals D(p || q), q = (p + R p)/2, R the point mirror of the grid. counts: a (bins, bins) array."""
    p = counts / counts.sum()
    q = 0.5 * (p + p[::-1, ::-1])
    m = 0.5 * (p + q)
    with np.errstate(divide="ignore", invalid="ignore"):
        js = 0.5 * (np.where(p > 0, p * np.log2(p / m), 0).sum() + np.where(q > 0, q * np.log2(q / m), 0).sum())
        cs = counts + PSEUDO
        ps = cs / cs.sum(); qs = 0.5 * (ps + ps[::-1, ::-1])
        kl_pq = (ps * np.log2(ps / qs)).sum(); kl_qp = (qs * np.log2(qs / ps)).sum()
    hel2 = 1.0 - np.sqrt(p * q).sum()
    tv = 0.5 * np.abs(p - q).sum()
    return dict(js=float(js), kl_pq=float(kl_pq), kl_qp=float(kl_qp), hel2=float(hel2), tv=float(tv))


def _hist(x, v, xr, vr, bins):
    i = np.clip(((x + xr) / (2 * xr) * bins).astype(int), 0, bins - 1)
    j = np.clip(((v + vr) / (2 * vr) * bins).astype(int), 0, bins - 1)
    return np.bincount(i * bins + j, minlength=bins * bins).reshape(bins, bins).astype(float)


def run_task(t):
    u = t["unit"]
    n = 2000 if t.get("smoke") else N_WALK
    ns = 500 if t.get("smoke") else N_SMALL
    unit = Unit(u["kind"], u["p"])
    rng = np.random.default_rng([u["seed"], u["i"], 41])
    g1 = np.linspace(0.0, u["tau_star"], N_GRID); g2 = np.linspace(0.0, u["V"], N_GRID)
    times = sorted(set(np.round(np.concatenate([g1, g2, [u["V"] / 2]]) / DT).astype(int)))
    x, v = initial(unit, 2 * n, rng)
    x, v = run(unit, x, v, T_BURN, True, DT, rng)
    flip = x < 0
    x, v = np.where(flip, -x, x), np.where(flip, -v, v)
    xr, vr = 1.1 * np.abs(x).max(), 1.1 * np.abs(v).max()
    coin = rng.random(n) < 0.5
    x[n:][coin], v[n:][coin] = -x[n:][coin], -v[n:][coin]
    rec = {f"{f}_{b}_{w}_{g}": [] for f in FUNCS for b in BINS for w in ("small", "large") for g in ("known", "null")}
    k_now = 0
    for k in times:
        for _ in range(k - k_now):
            x, v = step(unit, x, v, True, DT, rng)
        k_now = k
        for b in BINS:
            for w, m in (("small", ns), ("large", n)):
                for g, sl in (("known", slice(0, m)), ("null", slice(n, n + m))):
                    d = divergences(_hist(x[sl], v[sl], xr, vr, b))
                    for f in FUNCS:
                        rec[f"{f}_{b}_{w}_{g}"].append(d[f])
    return dict(steps=[int(k) for k in times], dt=DT, series={k: np.round(np.array(s), 7).tolist() for k, s in rec.items()})


# ------------------------------------------------------------------ analysis
def _time_avg(t, y):
    return float(np.trapezoid(y, t) / (t[-1] - t[0]))


def scores(rec, u):
    """The 4 time choices x 2 bias choices for each (functional, bins, walkers) of one unit."""
    t = np.array(rec["steps"]) * rec["dt"]
    k_tau = int(round(u["tau_star"] / DT)); k_V = int(round(u["V"] / DT)); k_h = int(round(u["V"] / 2 / DT))
    st = np.array(rec["steps"])
    m1 = st <= k_tau; m2 = st <= k_V
    i_tau = int(np.flatnonzero(st == k_tau)[0]); i_h = int(np.flatnonzero(st == k_h)[0])
    out = {}
    for f in FUNCS:
        for b in BINS:
            for w in ("small", "large"):
                kn = np.array(rec["series"][f"{f}_{b}_{w}_known"]); nu = np.array(rec["series"][f"{f}_{b}_{w}_null"])
                for bias, y in (("sub", kn - nu), ("raw", kn)):
                    out[(f, b, w, "chi3_tau", bias)] = _time_avg(t[m1], y[m1])
                    out[(f, b, w, "chi1_tau", bias)] = float(y[i_tau])
                    out[(f, b, w, "own_half", bias)] = float(y[i_h])
                    out[(f, b, w, "chi3_V", bias)] = _time_avg(t[m2], y[m2])
    return out


def analyze(out_dir):
    sys.path.insert(0, str(ROOT / "experiments"))
    from e6b_rockmemory import strat_auc
    units = {f"f_{u['seed']}_{u['i']:03d}": u for u in json.loads(DATA.read_text())}
    S = {}
    for fp in pathlib.Path(out_dir, "f").glob("*.json"):
        d = json.loads(fp.read_text()); name = d["task"]["name"]
        S[name] = scores(d["result"], units[name])
    seeds = sorted({u["seed"] for n, u in units.items() if n in S})
    choices = sorted(next(iter(S.values())).keys())
    rng = np.random.default_rng(2801)
    res = {}
    for c in choices:
        per = []
        for s in seeds:
            names = [n for n in S if units[n]["seed"] == s]
            val = np.array([S[n][c] for n in names]); lV = np.log([units[n]["V"] for n in names])
            kind = np.array([units[n]["kind"] for n in names])
            per.append(strat_auc(val, lV, kind)[0])
        per = np.array(per, float)
        bs = [np.nanmean(per[rng.integers(0, len(per), len(per))]) for _ in range(10_000)]
        lo, hi = np.nanpercentile(bs, [2.5, 97.5])
        lab = "passes" if hi < 0.5 else "mislabels rocks" if lo > 0.5 else "no difference"
        res["|".join(map(str, c))] = dict(auc=float(np.nanmean(per)), lo=float(lo), hi=float(hi), verdict=lab,
                                          per_draw=per.tolist())
    c2 = res["js|40|small|chi3_tau|sub"]
    v = dict(F1a="agrees" if abs(c2["auc"] - 0.711) <= 0.03 else "disagrees")
    cnt = {k: sum(r["verdict"] == k for r in res.values()) for k in ("passes", "mislabels rocks", "no difference")}
    v["F1b"] = cnt
    passing = sorted(k for k, r in res.items() if r["verdict"] == "passes")
    v["Gate"] = "no" if not passing else "partly"
    # F1c: range of the mean AUC when one choice changes, median over the other choices
    keys = [tuple(k.split("|")) for k in res]
    rng_of = {}
    for pos, label in enumerate(("functional", "bins", "walkers", "time", "bias")):
        spans = []
        others = {k[:pos] + k[pos + 1:] for k in keys}
        for o in others:
            vals = [res["|".join(k)]["auc"] for k in keys if k[:pos] + k[pos + 1:] == o]
            spans.append(max(vals) - min(vals))
        rng_of[label] = float(np.median(spans))
    v["F1c"] = rng_of
    out = dict(verdicts=v, passing=passing, choices=res, n_units=len(S))
    (ROOT / "results" / "e28_f_cld_map.json").write_text(json.dumps(out, indent=1))
    L = ["# E28: a map of the free choices of CLD (niche F)", "", "Rules: docs/F.md.", "",
         f"Units: {len(S)}. F1a (C2 choice gives 0.711 again): {v['F1a']} (AUC {c2['auc']:.3f} [{c2['lo']:.3f}, {c2['hi']:.3f}]).",
         f"F1b counts: {cnt}. Gate: {v['Gate']}.", f"F1c (median range of the AUC for each choice): "
         + ", ".join(f"{k} {x:.3f}" for k, x in rng_of.items()), "",
         "| Functional | Bins | Walkers | Time | Bias | AUC [95 % CI] | Verdict |", "|---|---|---|---|---|---|---|"]
    for k in sorted(res, key=lambda k: res[k]["auc"]):
        r = res[k]; f, b, w, tm, bi = k.split("|")
        L.append(f"| {f} | {b} | {w} | {tm} | {bi} | {r['auc']:.3f} [{r['lo']:.3f}, {r['hi']:.3f}] | {r['verdict']} |")
    (ROOT / "results" / "e28_f_cld_map.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[:8]))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if "--export" in sys.argv:
        export()
    else:
        analyze(sys.argv[1] if len(sys.argv) > 1 else ROOT / "cluster_out")
