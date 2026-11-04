"""E8 / ROADMAP S5 - boundaries by conditional independence. Rules: docs/S5.md.
  --calibrate : thresholds from 10 calibration worlds per family (seed 7), saved to results/e8_thresholds.json
  (default)   : 40 test worlds per family (seed 2026), rules B1, B2, D1."""
import argparse, json, time
from itertools import combinations
import numpy as np
from common import RES, save_json
from vlife.blankets import make_planted_world, sample, estimates, static_graph, dynamic_graph, blanket_of, edge_scores
from vlife.gaussian import lagged_cov, joint_cov, mutual_information, total_correlation

DELTA, N_SAMP, FAMS = 0.5, 20000, ("equilibrium", "driven")
GRID_S, GRID_D = np.linspace(0.01, 0.3, 30), np.linspace(0.02, 0.6, 30)


def world_data(job):
    fam, seed, k = job
    rng = np.random.default_rng([seed, FAMS.index(fam), k])
    w = make_planted_world(fam, rng)
    S_hat, C_hat = estimates(sample(w["B"], w["S"], N_SAMP, DELTA, rng))
    return w, S_hat, C_hat


def calib_job(job):
    w, S_hat, C_hat = world_data(job)
    fs = [edge_scores(static_graph(S_hat, t)[0], w["adj"])[2] for t in GRID_S]
    fd = [edge_scores(dynamic_graph(S_hat, C_hat, DELTA, t)[0], w["adj"])[2] for t in GRID_D]
    return fs, fd


def test_job(job):
    thr = job[3]; w, S_hat, C_hat = world_data(job[:3]); fam = w["family"]; N = len(w["S"])
    C_ex = lagged_cov(w["B"], w["S"], DELTA)
    graphs = {"static exact": static_graph(w["S"], 1e-8), "dynamic exact": dynamic_graph(w["S"], C_ex, DELTA, 1e-8),
              "static finite": static_graph(S_hat, thr[fam]["static"]), "dynamic finite": dynamic_graph(S_hat, C_hat, DELTA, thr[fam]["dynamic"])}
    out = dict(family=fam, rec={}, edges={})
    for name, (g, _) in graphs.items():
        out["rec"][name] = [blanket_of(g, I) == Bl for I, Bl in w["orgs"]]
        out["edges"][name] = edge_scores(g, w["adj"])
    r = graphs["static exact"][1]; iu = np.triu_indices(N, 1)
    ie = [abs(r[a, e]) for I, Bl in w["orgs"] for a in I for e in range(N) if e not in I and e not in Bl]
    out["static_IE_max"] = float(max(ie)); out["static_edge_median"] = float(np.median(np.abs(r[iu][w["adj"][iu]])))
    # discovery: all triples, exact features (environment = complement, tau = 1)
    J = joint_cov(w["B"], w["S"], 1.0); trip = list(combinations(range(N), 3)); sc = {k: [] for k in ("Phi_TC", "C", "TC", "closure")}
    for A in trip:
        A = list(A); X = [i for i in range(N) if i not in A]
        C = mutual_information(J, A, [N + a for a in A]); P = mutual_information(J, A, [N + x for x in X])
        TC = total_correlation(w["S"], A); IAX = mutual_information(w["S"], A, X)
        sc["Phi_TC"].append(P + C - 0.25 * TC); sc["C"].append(C); sc["TC"].append(TC); sc["closure"].append(TC - IAX)
    idx = {t: j for j, t in enumerate(trip)}; out["pct"] = {}
    for k, v in sc.items():
        v = np.array(v); out["pct"][k] = [float(np.mean(v < v[idx[I]]) + 0.5 * np.mean(v == v[idx[I]])) for I, _ in w["orgs"]]
    return out


def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [float(p), float(c - h), float(c + h)]


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--calibrate", action="store_true"); ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    from concurrent.futures import ProcessPoolExecutor
    t0 = time.time()
    if a.calibrate:
        thr = {}
        with ProcessPoolExecutor(a.workers) as ex:
            for fam in FAMS:
                res = list(ex.map(calib_job, [(fam, 7, k) for k in range(10)]))
                fs, fd = np.mean([r[0] for r in res], 0), np.mean([r[1] for r in res], 0)
                thr[fam] = dict(static=float(GRID_S[fs.argmax()]), dynamic=float(GRID_D[fd.argmax()]),
                                static_F1=float(fs.max()), dynamic_F1=float(fd.max()))
        (RES / "e8_thresholds.json").write_text(json.dumps(thr, indent=2)); print(json.dumps(thr, indent=2), f"\n{time.time() - t0:.0f}s")
    else:
        thr = json.loads((RES / "e8_thresholds.json").read_text())
        jobs = [(fam, 2026, k, thr) for fam in FAMS for k in range(40)]
        with ProcessPoolExecutor(a.workers) as ex:
            rows = list(ex.map(test_job, jobs))
        print(f"done in {time.time() - t0:.0f}s", flush=True)
        lab = lambda w: "recovers" if w[0] >= 0.8 and w[1] >= 0.7 else "fails" if w[0] <= 0.5 else "partial"
        rng = np.random.default_rng(0); R = {}; L = ["# E8 / S5 report (auto-generated; rules in docs/S5.md)\n",
             f"Thresholds (calibration worlds): {json.dumps(thr)}\n",
             "| Rule | Detector | Family | Blanket recovery [95% CI] | Edge precision / recall | Verdict |", "|---|---|---|---|---|---|"]
        for fam in FAMS:
            fr = [r for r in rows if r["family"] == fam]; R[fam] = {}
            for name in ("static exact", "dynamic exact", "static finite", "dynamic finite"):
                ok = sum(sum(r["rec"][name]) for r in fr); n = 2 * len(fr); w = wilson(ok, n)
                pr = np.mean([r["edges"][name][0] for r in fr]); rc = np.mean([r["edges"][name][1] for r in fr])
                R[fam][name] = dict(rate=w, precision=float(pr), recall=float(rc), verdict=lab(w))
                L.append(f"| {'B1' if 'exact' in name else 'B2'} | {name} | {fam} | {w[0]:.2f} [{w[1]:.2f}, {w[2]:.2f}] | {pr:.2f} / {rc:.2f} | {lab(w)} |")
        L += ["", "| Rule | Score | Family | Median percentile of planted interiors [95% CI] | Verdict |", "|---|---|---|---|---|"]
        for fam in FAMS:
            fr = [r for r in rows if r["family"] == fam]
            for k in ("Phi_TC", "C", "TC", "closure"):
                P = np.array([r["pct"][k] for r in fr]); pt = float(np.median(P))
                bs = [np.median(P[rng.integers(0, len(P), len(P))]) for _ in range(1000)]; lo, hi = np.percentile(bs, [2.5, 97.5])
                v = "finds structures" if pt >= 0.95 and lo >= 0.90 else "does not find"
                R[fam][k] = dict(median_pct=[pt, float(lo), float(hi)], verdict=v)
                L.append(f"| D1 | {k} | {fam} | {pt:.3f} [{lo:.3f}, {hi:.3f}] | {v} |")
        dr = [r for r in rows if r["family"] == "driven"]
        R["aguilera"] = dict(static_IE_max_median=float(np.median([r["static_IE_max"] for r in dr])),
                             static_edge_median=float(np.median([r["static_edge_median"] for r in dr])))
        L += ["", f"Description: driven worlds, exact static partial correlations: median of max |r| between interior and exterior "
              f"{R['aguilera']['static_IE_max_median']:.3f}; median |r| on true edges {R['aguilera']['static_edge_median']:.3f}."]
        save_json("e8_summary.json", R); (RES / "e8_report.md").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L))
