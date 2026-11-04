"""E5 / ROADMAP S3 - is information used? Linear homeostat, intact vs scrambled vs no feedback. Rules: docs/S3.md."""
import argparse, pickle, time
import numpy as np
from scipy.stats import spearmanr
from common import RES, save_json
from vlife.agency import draw_organism, homeostat, simulate_exit_threshold, ORGANISM, H, V
from vlife.gaussian import joint_cov, mutual_information, conditional_mutual_information, total_correlation

VERSIONS = ("intact", "scrambled", "nofeedback")


def features(B, S, tau):
    n = S.shape[0]; J = joint_cov(B, S, tau); A = ORGANISM; At1 = [n + a for a in A]
    X = [i for i in range(n) if i not in A]
    return dict(P=mutual_information(J, A, [n + H]), C=mutual_information(J, A, At1), TC=total_correlation(S, A),
                Ivh=mutual_information(S, [V], [H]), leak=conditional_mutual_information(J, At1, X, A))


def run_one(job):
    i, seed, tau, n_traj, t_max = job
    o = draw_organism(np.random.default_rng([seed, i]))
    sys_ = {ver: homeostat(o, ver) for ver in VERSIONS}
    c = 1.2816 * np.sqrt(sys_["nofeedback"][2][V, V])
    out = dict(i=i, org=o.__dict__, c=c)
    for k, ver in enumerate(VERSIONS):
        B, D, S = sys_[ver]
        Vv, ev, nv = simulate_exit_threshold(B, S, V, c, n_traj, 0.05, t_max, np.random.default_rng([seed, i, k]))
        out[ver] = dict(V=Vv, ev=ev, nv=nv, **features(B, S, tau))
    return out


def boot(n, fn, n_boot=1000, seed=0):
    rng = np.random.default_rng(seed); pt = np.asarray(fn(np.arange(n)))
    bs = np.array([fn(rng.integers(0, n, n)) for _ in range(n_boot)])
    lo, hi = np.nanpercentile(bs, [2.5, 97.5], axis=0)
    return pt, lo, hi


def analyse(rows):
    keep = [r for r in rows if min(r[v]["ev"] for v in VERSIONS) >= 5]
    n = len(keep)
    g = lambda ver, k: np.array([r[ver][k] for r in keep])
    logV = {v: np.log(g(v, "V")) for v in VERSIONS}
    voi = logV["intact"] - logV["scrambled"]; voi0 = logV["intact"] - logV["nofeedback"]
    F = ("P", "C", "TC")
    pooled = {k: np.concatenate([g("intact", k), g("scrambled", k)]) for k in F}
    mu = {k: pooled[k].mean() for k in F}; sd = {k: pooled[k].std() for k in F}
    Xs = {v: np.column_stack([np.ones(n)] + [(g(v, k) - mu[k]) / sd[k] for k in F]) for v in ("intact", "scrambled")}

    def betaP(ids):
        bi = np.linalg.lstsq(Xs["intact"][ids], logV["intact"][ids], rcond=None)[0][1]
        bs = np.linalg.lstsq(Xs["scrambled"][ids], logV["scrambled"][ids], rcond=None)[0][1]
        return [bi, bs, bi - bs]

    def rho(a, b):
        return lambda ids: spearmanr(a[ids], b[ids])[0]

    phi = {v: g(v, "P") + g(v, "C") - 0.25 * g(v, "TC") for v in ("intact", "scrambled")}
    res = dict(n_organisms=len(rows), n_kept=n, n_dropped=len(rows) - n,
               mean_VoI=boot(n, lambda ids: voi[ids].mean()), frac_VoI_pos=float(np.mean(voi > 0)),
               mean_VoI_vs_nofeedback=boot(n, lambda ids: voi0[ids].mean()), frac_VoI0_pos=float(np.mean(voi0 > 0)),
               betaP=boot(n, betaP), rho_P_VoI=boot(n, rho(g("intact", "P"), voi)),
               rho_Ivh_logV=boot(n, rho(g("intact", "Ivh"), logV["intact"])),
               rho_PhiTC_intact=boot(n, rho(phi["intact"], logV["intact"])),
               rho_PhiTC_scrambled=boot(n, rho(phi["scrambled"], logV["scrambled"])),
               rho_L_VoI=boot(n, rho(np.array([r["org"]["L"] for r in keep]), voi)),
               rho_leak_logV=boot(n, rho(g("intact", "leak"), logV["intact"])))
    t = lambda x: [float(np.ravel(x[0])[0]), float(np.ravel(x[1])[0]), float(np.ravel(x[2])[0])]
    bP = res["betaP"]
    v = {}
    v["R1"] = "used" if res["mean_VoI"][0] > 0 and res["mean_VoI"][1] > 0 else "not used"
    v["R2"] = "depends on the loop" if bP[1][0] > 0 and bP[1][2] > 0 else "does not depend"
    v["Gate"] = ("triggered: P is not what drives viability" if v["R1"] == "used" and bP[1][0] <= 0 else "not triggered")
    v["R3"] = "yes" if res["rho_P_VoI"][1] > 0 else "no"
    v["R4"] = "present" if res["rho_Ivh_logV"][2] < 0 else "not present"
    v["R5"] = "supported" if res["rho_PhiTC_intact"][1] > 0 else "not supported"
    clean = {k: (val if not isinstance(val, tuple) else [np.ravel(a).tolist() for a in val]) for k, val in res.items()}
    return clean, v, keep, voi


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=400); ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--tau", type=float, default=1.0); ap.add_argument("--n_traj", type=int, default=600)
    ap.add_argument("--t_max", type=float, default=1000.0); ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    from concurrent.futures import ProcessPoolExecutor
    t0 = time.time()
    jobs = [(i, a.seed, a.tau, a.n_traj, a.t_max) for i in range(a.n)]
    with ProcessPoolExecutor(a.workers) as ex:
        rows = list(ex.map(run_one, jobs, chunksize=4))
    print(f"simulation done in {time.time() - t0:.0f}s", flush=True)
    pickle.dump(rows, open(RES / f"e5_dataset{a.tag}.pkl", "wb"))
    res, verdicts, keep, voi = analyse(rows)
    save_json(f"e5_summary{a.tag}.json", dict(settings=vars(a), results=res, verdicts=verdicts))
    f3 = lambda x: f"{x[0][0]:+.3f} [{x[1][0]:+.3f}, {x[2][0]:+.3f}]" if isinstance(x[0], list) else f"{x[0]:+.3f} [{x[1]:+.3f}, {x[2]:+.3f}]"
    b = res["betaP"]
    L = ["# E5 / S3 report (auto-generated; rules in docs/S3.md)\n",
         f"Settings: {vars(a)}. Organisms: {res['n_organisms']}, kept {res['n_kept']}, dropped {res['n_dropped']} (fewer than 5 exits).\n",
         "| Rule | Measure | Value [95% CI] | Verdict |", "|---|---|---|---|",
         f"| R1 | mean VoI = log V_intact - log V_scrambled | {f3(res['mean_VoI'])} (VoI > 0 in {res['frac_VoI_pos']:.0%}) | {verdicts['R1']} |",
         f"| R2 | beta_P intact / scrambled / difference | {b[0][0]:+.3f} [{b[1][0]:+.3f}, {b[2][0]:+.3f}] / {b[0][1]:+.3f} [{b[1][1]:+.3f}, {b[2][1]:+.3f}] / {b[0][2]:+.3f} [{b[1][2]:+.3f}, {b[2][2]:+.3f}] | {verdicts['R2']} |",
         f"| Gate | | | {verdicts['Gate']} |",
         f"| R3 | rho(P_intact, VoI) | {f3(res['rho_P_VoI'])} | {verdicts['R3']} |",
         f"| R4 | rho(I(v;h)_intact, log V_intact) | {f3(res['rho_Ivh_logV'])} | {verdicts['R4']} |",
         f"| R5 | rho(Phi_TC, log V) intact | {f3(res['rho_PhiTC_intact'])} (scrambled {f3(res['rho_PhiTC_scrambled'])}) | {verdicts['R5']} |",
         "\nDescription only:",
         f"- mean log V_intact - log V_nofeedback: {f3(res['mean_VoI_vs_nofeedback'])} (> 0 in {res['frac_VoI0_pos']:.0%})",
         f"- rho(L, VoI): {f3(res['rho_L_VoI'])}",
         f"- rho(leak_intact, log V_intact): {f3(res['rho_leak_logV'])}"]
    (RES / f"e5_report{a.tag}.md").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L))
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    Lg = np.array([r["org"]["L"] for r in keep]); P = np.array([r["intact"]["P"] for r in keep])
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    sc = ax[0].scatter(Lg, voi, c=P, s=10, cmap="viridis"); plt.colorbar(sc, ax=ax[0], label="P (intact, nats)")
    ax[0].axhline(0, c="k", lw=.5); ax[0].set_xlabel("loop gain L"); ax[0].set_ylabel("VoI = log V_intact - log V_scrambled")
    for ver, col in (("intact", "tab:blue"), ("scrambled", "tab:red")):
        ax[1].scatter([r[ver]["P"] for r in keep], [np.log(r[ver]["V"]) for r in keep], s=8, alpha=.5, c=col, label=ver)
    ax[1].set_xlabel("P = I(A_t; h_t+tau) (nats)"); ax[1].set_ylabel("log V"); ax[1].legend()
    plt.tight_layout(); plt.savefig(RES / f"e5_agency{a.tag}.png", dpi=130)
