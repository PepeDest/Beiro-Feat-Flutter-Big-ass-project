"""E3 - THE core test (Option B): does the organisational functional predict physical viability?

For an ensemble of random OU worlds (3 families), every non-empty proper subset A is a candidate structure.
 y  = log V(A)  with V = mean first-passage time out of A's viability set (viability.py)  [physical, no information theory]
 x  = (P, C, KH, IAX) closed-form information features (functional.py)
Questions (pre-registered in docs/THEORY.md sec 5):
 H1  within-world rank correlation of Phi_orig with log V is > 0
 H2  regression of within-world-demeaned log V on features gives signs (+P, +C, -KH) that are stable across families
 H3  flux ratio R = V_driven / V_eq is ~1 in the equilibrium family (control) and is explained by features in driven ones
Outputs: results/e3_dataset.pkl, e3_summary.json, e3_report.md, figures.
"""
import argparse, pickle, time
import numpy as np
from common import RES, save_json
from vlife.worlds import make_world, FAMILIES
from vlife.functional import structure_features, phi_orig, all_subsets, FEATURES
from vlife.viability import simulate_exits, mfpt_all
from vlife.gaussian import entropy_production
from vlife.stats import spearman_within, cluster_bootstrap
from vlife.price import selection_differential


def build_dataset(n_worlds, tau, p_out, n_traj, dt, t_max, seed, N=6, noise_range=None, crn=False):
    """crn=True (fix #5, docs/code_review.md): the driven run and its equilibrium counterpart use the same random numbers
    (common random numbers), so log R = 0 exactly in the equilibrium family. crn=False is the old behaviour (one stream,
    used first by the driven run, then by the counterpart)."""
    data = []
    subsets = all_subsets(N)
    for fam in FAMILIES:
        for k in range(n_worlds):
            rng = np.random.default_rng([seed, FAMILIES.index(fam), k])
            w = make_world(fam, N, rng, noise_range=noise_range)
            f = structure_features(w, tau, subsets)
            if crn:
                sim = [seed, FAMILIES.index(fam), k, 1]
                d_on = simulate_exits(w.B, w.S, subsets, p_out, n_traj, dt, t_max, np.random.default_rng(sim))
                d_eq = simulate_exits(w.B_eq(), w.S, subsets, p_out, n_traj, dt, t_max, np.random.default_rng(sim))
            else:
                d_on = simulate_exits(w.B, w.S, subsets, p_out, n_traj, dt, t_max, rng)
                d_eq = simulate_exits(w.B_eq(), w.S, subsets, p_out, n_traj, dt, t_max, rng)
            V_on, ev_on, nv_on = mfpt_all(d_on); V_eq, ev_eq, nv_eq = mfpt_all(d_eq)
            data.append(dict(family=fam, k=k, B=w.B, S=w.S, D=w.D, feat=f, V_on=V_on, ev_on=ev_on, V_eq=V_eq, ev_eq=ev_eq,
                             sigma=entropy_production(w.B, w.D, w.S), subsets=subsets,
                             exit_t=d_on.exit_t.astype(np.float32), event=d_on.event, valid=d_on.valid,
                             t_max=t_max, tau=tau, p_out=p_out, dt=dt, crn=crn))
            print(f"  {fam} #{k}: median V_on={np.median(V_on):.1f}  censored(<5 ev)={np.mean(ev_on<5):.2f}", flush=True)
    return data


# ---------------------------------------------------------------- analysis
def prepare(data, min_events=5):
    """Within-world demeaned arrays on structures with enough observed exits (avoids censored V)."""
    out = []
    for d in data:
        m = (d["ev_on"] >= min_events) & (d["ev_eq"] >= min_events)
        if m.sum() < 8:
            out.append(None); continue
        y = np.log(d["V_on"][m]); X = np.column_stack([d["feat"][k][m] for k in FEATURES])
        out.append(dict(mask=m, y=y, X=X, yd=y - y.mean(), Xd=X - X.mean(0),
                        logR=np.log(d["V_on"][m] / d["V_eq"][m]), feat={k: d["feat"][k][m] for k in d["feat"] if k != "subsets"}))
    return out


def fit(prep, ids, scale):
    ids = [i for i in ids if prep[i] is not None]
    Xd = np.vstack([prep[i]["Xd"] for i in ids]) / scale
    yd = np.concatenate([prep[i]["yd"] for i in ids])
    return np.linalg.lstsq(Xd, yd, rcond=None)[0]


def analyse(data, label, ids, beta=1.0, lam=0.25):
    from scipy.stats import spearmanr
    prep = prepare(data)
    ids = [i for i in ids if prep[i] is not None]
    allX = np.vstack([prep[i]["Xd"] for i in ids]); scale = allX.std(0)
    coef_pt, coef_lo, coef_hi = cluster_bootstrap(len(ids), lambda b: fit(prep, [ids[i] for i in b], scale), 300)

    def scores(p, coef):
        f = p["feat"]
        s = {"Phi_orig(b=1,l=.25)": f["P"] + beta * f["C"] - lam * f["KH"], "C only": f["C"], "P only": f["P"],
             "-KH (simplicity)": -f["KH"], "size (-k)": -f["size"], "-leak (closure)": -f["leak"], "-IAX": -f["IAX"]}
        s["fitted linear (cross-fitted)"] = (p["Xd"] / scale) @ coef     # coef is in standardised units
        return s

    names = list(scores(prep[ids[0]], np.zeros(4)).keys())
    pos = {i: n for n, i in enumerate(ids)}
    even = [i for i in ids if pos[i] % 2 == 0]; odd = [i for i in ids if pos[i] % 2 == 1]
    coef_of = {}                                   # world -> coefficients fitted on the OTHER half (no leakage)
    c_even, c_odd = fit(prep, even, scale), fit(prep, odd, scale)
    for i in even: coef_of[i] = c_odd
    for i in odd: coef_of[i] = c_even

    def world_rho(i, name, stratify):
        p = prep[i]; sc = scores(p, coef_of[i])[name]; y = p["y"]; size = p["feat"]["size"]
        groups = [np.ones(len(y), bool)] if not stratify else [size == k for k in np.unique(size)]
        r = [spearmanr(sc[m], y[m])[0] for m in groups if m.sum() >= 6 and np.ptp(sc[m]) > 0 and np.ptp(y[m]) > 0]
        return np.mean(r) if r else np.nan

    spear, spear_strat = {}, {}
    for name in names:
        for store, strat in ((spear, False), (spear_strat, True)):
            vals = np.array([world_rho(i, name, strat) for i in ids])
            pt, lo, hi = cluster_bootstrap(len(ids), lambda b: np.nanmean(vals[b]), 400)
            store[name] = (float(pt), float(lo), float(hi))
    sel = [selection_differential(np.exp(prep[i]["y"]), prep[i]["feat"]["P"] + beta * prep[i]["feat"]["C"] - lam * prep[i]["feat"]["KH"])
           for i in ids]
    per_world_logR = np.array([np.mean(prep[i]["logR"]) for i in ids])
    return dict(label=label, n_worlds=len(ids), n_structures=int(sum(len(prep[i]["y"]) for i in ids)),
                coef_names=list(FEATURES), coef=coef_pt.tolist(), coef_lo=coef_lo.tolist(), coef_hi=coef_hi.tolist(),
                feature_sd=scale.tolist(), spearman=spear, spearman_within_size=spear_strat,
                price_selection_mean=float(np.mean(sel)), price_selection_frac_positive=float(np.mean(np.array(sel) > 0)),
                logR_mean=float(per_world_logR.mean()), logR_se=float(per_world_logR.std() / np.sqrt(len(ids))))


def make_figures(data, results, tag=""):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    prep = prepare(data); ids = [i for i, p in enumerate(prep) if p is not None]
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
    cols = {"equilibrium": "tab:blue", "driven": "tab:red", "modular_driven": "tab:green"}
    for i in ids:
        p = prep[i]; f = p["feat"]; phi = f["P"] + f["C"] - 0.25 * f["KH"]
        ax[0].scatter(phi - phi.mean(), p["yd"], s=6, alpha=.35, c=cols[data[i]["family"]])
    ax[0].set_xlabel("Phi_orig (within-world, demeaned)"); ax[0].set_ylabel("log MFPT (within-world, demeaned)")
    ax[0].set_title("Original Phi vs viability"); ax[0].axhline(0, c="k", lw=.5); ax[0].axvline(0, c="k", lw=.5)
    r = results["all"]; x = np.arange(4)
    ax[1].bar(x, r["coef"], yerr=[np.array(r["coef"]) - np.array(r["coef_lo"]), np.array(r["coef_hi"]) - np.array(r["coef"])], capsize=4)
    ax[1].set_xticks(x); ax[1].set_xticklabels(["P", "C", "KH", "IAX"]); ax[1].axhline(0, c="k", lw=.5)
    ax[1].set_title("Standardised regression coefficients\n(all worlds; 95% cluster-bootstrap CI)")
    ax[1].set_ylabel("d log V per +1 SD of feature (within-world)")
    names = list(results["all"]["spearman"].keys()); vals = [results["all"]["spearman"][n] for n in names]
    y = np.arange(len(names))
    ax[2].barh(y, [v[0] for v in vals], xerr=[[v[0] - v[1] for v in vals], [v[2] - v[0] for v in vals]], capsize=3)
    ax[2].set_yticks(y); ax[2].set_yticklabels(names, fontsize=8); ax[2].axvline(0, c="k", lw=.5)
    ax[2].set_xlabel("mean within-world Spearman rho with log V"); ax[2].set_title("Which score ranks structures by viability?")
    plt.tight_layout(); plt.savefig(RES / f"e3_phi_vs_viability{tag}.png", dpi=130); plt.close()


def write_report(results, args):
    L = ["# E3 report (auto-generated)\n",
         f"Settings: N={args.N}, tau={args.tau}, p_out={args.p_out}, n_worlds/family={args.n_worlds}, n_traj={args.n_traj}, dt={args.dt}, t_max={args.t_max}\n"]
    for key, r in results.items():
        L.append(f"\n## {r['label']}  (worlds={r['n_worlds']}, structures={r['n_structures']})\n")
        L.append("Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:\n")
        L.append("| feature | coef | CI low | CI high |\n|---|---|---|---|")
        for n, c, lo, hi in zip(r["coef_names"], r["coef"], r["coef_lo"], r["coef_hi"]):
            L.append(f"| {n} | {c:+.3f} | {lo:+.3f} | {hi:+.3f} |")
        L.append("\nMean within-world Spearman rho (score vs log V):\n")
        L.append("| score | rho | CI low | CI high |\n|---|---|---|---|")
        for n, (v, lo, hi) in r["spearman"].items():
            L.append(f"| {n} | {v:+.3f} | {lo:+.3f} | {hi:+.3f} |")
        L.append("\nSame, but ranking only among structures OF EQUAL SIZE (controls the size confound):\n")
        L.append("| score | rho | CI low | CI high |\n|---|---|---|---|")
        for n, (v, lo, hi) in r["spearman_within_size"].items():
            L.append(f"| {n} | {v:+.3f} | {lo:+.3f} | {hi:+.3f} |")
        L.append(f"\nPrice selection term Cov(w/wbar, Phi_orig): mean={r['price_selection_mean']:+.4f}, fraction of worlds >0 = {r['price_selection_frac_positive']:.2f}")
        L.append(f"\nlog(V_driven/V_eq): mean={r['logR_mean']:+.3f} +- {r['logR_se']:.3f} (s.e. over worlds)\n")
    (RES / f"e3_report{args.tag}.md").write_text("\n".join(L))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n_worlds", type=int, default=30); ap.add_argument("--tau", type=float, default=1.0)
    ap.add_argument("--p_out", type=float, default=0.05); ap.add_argument("--n_traj", type=int, default=200)
    ap.add_argument("--dt", type=float, default=0.05); ap.add_argument("--t_max", type=float, default=150.0)
    ap.add_argument("--seed", type=int, default=2026); ap.add_argument("--tag", default="")
    ap.add_argument("--reuse", action="store_true")
    ap.add_argument("--N", type=int, default=6)
    ap.add_argument("--crn", action="store_true", help="fix #5: common random numbers for the driven and equilibrium runs")
    ap.add_argument("--noise_range", type=float, default=None, help="S1 D-test: D = diag(d), d log-uniform in [1/r, r]")
    ap.add_argument("--sim_from", default=None,
                    help="tag of an existing dataset: reuse its exit data and recompute only the features with --tau "
                         "(tau does not enter the simulation)")
    args = ap.parse_args()
    pk = RES / f"e3_dataset{args.tag}.pkl"
    if args.sim_from is not None:
        from vlife.worlds import World
        data = pickle.load(open(RES / f"e3_dataset{args.sim_from}.pkl", "rb"))
        src_args = (data[0]["p_out"], data[0]["t_max"])
        args.p_out, args.t_max = src_args
        for d in data:
            w = World(B=d["B"], D=d.get("D", np.eye(d["B"].shape[0])), S=d["S"], family=d["family"])
            d["feat"] = structure_features(w, args.tau, d["subsets"]); d["tau"] = args.tau
        pickle.dump(data, open(pk, "wb")); print(f"features recomputed with tau={args.tau} on dataset '{args.sim_from}'")
    elif args.reuse and pk.exists():
        data = pickle.load(open(pk, "rb"))
    else:
        t0 = time.time(); data = build_dataset(args.n_worlds, args.tau, args.p_out, args.n_traj, args.dt, args.t_max, args.seed, args.N, args.noise_range, args.crn)
        pickle.dump(data, open(pk, "wb")); print(f"simulation done in {time.time()-t0:.0f}s")
    # Take the report settings from the dataset, not from the command line. With --reuse the command-line
    # defaults can differ from the settings that made the data (this bug was found in S0).
    d0 = data[0]
    args.N, args.tau, args.p_out, args.t_max = d0["B"].shape[0], d0["tau"], d0["p_out"], d0["t_max"]
    args.n_traj, args.n_worlds = d0["exit_t"].shape[0], len(data) // len(FAMILIES)
    results = {"all": analyse(data, "ALL families", range(len(data)))}
    for fam in FAMILIES:
        results[fam] = analyse(data, fam, [i for i, d in enumerate(data) if d["family"] == fam])
    save_json(f"e3_summary{args.tag}.json", results); write_report(results, args)
    make_figures(data, results, args.tag)
    print("report written")
