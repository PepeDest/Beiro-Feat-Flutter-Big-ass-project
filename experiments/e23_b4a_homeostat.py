"""Niche B, step B4a (docs/B.md): the value of information of KolchinskyWolpert18 in closed form, against the simulated
VoI of the S3 homeostat. No new simulation of exit times.

Before this script: `python experiments/e5_agency.py --tag _b4 --workers 4` rebuilds the S3 phase C data (the
`.pkl` files are not in git). Check A0 compares its summary with results/e5_summary_v2.json.
Rules (A0, R1-R3) and the expectations are in docs/B.md (fixed before this script ran).
"""
import json, pickle, sys
import numpy as np
from scipy.stats import spearmanr
from common import RES, save_json
from vlife.agency import Organism, homeostat
from vlife.semantic_apply import value_on, half_value_information

AGENT, ENV, TARGET_V = [1, 2, 3, 4], [0], 3          # agent (s, m, u, v), environment h, v is local index 3
TAU, TAUS_DESC = 1.0, (0.5, 2.0, 5.0)
VERSIONS = ("intact", "scrambled", "nofeedback")


def boot(n, fn, n_boot=1000, seed=0):
    rng = np.random.default_rng(seed); pt = float(fn(np.arange(n)))
    bs = np.array([fn(rng.integers(0, n, n)) for _ in range(n_boot)])
    lo, hi = np.nanpercentile(bs, [2.5, 97.5])
    return [pt, float(lo), float(hi)]


def same(a, b):
    """True if two JSON values are equal, numbers to 1e-9."""
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= 1e-9 * max(1.0, abs(a))
    return a == b


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    new = json.load(open(RES / "e5_summary_b4.json")); old = json.load(open(RES / "e5_summary_v2.json"))
    A0 = same(new["results"], old["results"]) and new["verdicts"] == old["verdicts"]
    if not A0:
        raise SystemExit("A0 fails: the rebuilt S3 data differ from phase C. Stop (docs/B.md, B4a).")
    rows = [r for r in pickle.load(open(RES / "e5_dataset_b4.pkl", "rb")) if min(r[v]["ev"] for v in VERSIONS) >= 5]
    n = len(rows)
    out = []
    for r in rows:
        B, D, S = homeostat(Organism(**r["org"]), "intact")
        d = dict(i=r["i"], L=r["org"]["L"], VoI=float(np.log(r["intact"]["V"]) - np.log(r["scrambled"]["V"])),
                 P=r["intact"]["P"], dV_v=float(value_on(B, D, S, AGENT, ENV, TAU, [TARGET_V])),
                 dV_A=float(value_on(B, D, S, AGENT, ENV, TAU)))
        for t in TAUS_DESC:
            d[f"dV_v_tau{t}"] = float(value_on(B, D, S, AGENT, ENV, t, [TARGET_V]))
        p, R, I_act = half_value_information(B, D, S, AGENT, ENV, TAU, TARGET_V)
        d.update(p_half=p, R_half=R, I_act=I_act, r_half=None if R is None else R / I_act)
        out.append(d)
    a = lambda k: np.array([d[k] for d in out], float)
    voi, dv, P = a("VoI"), a("dV_v"), a("P")
    rho = lambda x, y: (lambda ids: spearmanr(x[ids], y[ids])[0])
    res = dict(n=n, rho_dV_VoI=boot(n, rho(dv, voi)), rho_P_VoI=boot(n, rho(P, voi)),
               diff=boot(n, lambda ids: spearmanr(dv[ids], voi[ids])[0] - spearmanr(P[ids], voi[ids])[0]),
               sign_agree=float(np.mean(np.sign(dv) == np.sign(voi))), frac_dV_pos=float(np.mean(dv > 0)),
               rho_dVA_VoI=boot(n, rho(a("dV_A"), voi)),
               rho_dV_VoI_tau={t: boot(n, rho(a(f"dV_v_tau{t}"), voi)) for t in TAUS_DESC},
               rho_L_dV=float(spearmanr(a("L"), dv)[0]))
    rh = np.array([np.nan if d["r_half"] is None else d["r_half"] for d in out])
    ok = np.isfinite(rh)
    res["r_half"] = dict(n=int(ok.sum()), median=float(np.median(rh[ok])), q10=float(np.quantile(rh[ok], 0.1)),
                         q90=float(np.quantile(rh[ok], 0.9)), rho_with_VoI=float(spearmanr(rh[ok], voi[ok])[0]))
    v = dict(A0="pass",
             R1="ranks the value" if res["rho_dV_VoI"][1] > 0 else "does not rank the value",
             R2="signs agree" if res["sign_agree"] >= 0.9 else "signs do not agree",
             R3="better than P" if res["diff"][1] > 0 else "worse than P" if res["diff"][2] < 0 else "no clear difference")
    save_json("e23_b4a_homeostat.json", dict(verdicts=v, results=res, organisms=out))
    f = lambda x: f"{x[0]:+.3f} [{x[1]:+.3f}, {x[2]:+.3f}]"
    L = ["# E23: value of information in closed form against the S3 VoI (niche B, step B4a)", "", "Rules: docs/B.md, B4a.",
         "", f"A0 (rebuilt S3 data equal phase C): pass. Organisms: {n}.", "",
         "| Rule | Question | Value | Verdict |", "|---|---|---|---|",
         f"| R1 | ρ(ΔV_KW, VoI) | {f(res['rho_dV_VoI'])} | {v['R1']} |",
         f"| R2 | Fraction with the same sign | {res['sign_agree']:.3f} (ΔV_KW > 0 in {res['frac_dV_pos']:.3f}) | {v['R2']} |",
         f"| R3 | ρ(ΔV_KW, VoI) − ρ(P, VoI) | {f(res['diff'])} (ρ(P, VoI) = {f(res['rho_P_VoI'])}) | {v['R3']} |", "",
         "Description:", f"- ρ(ΔV on the whole organism, VoI) = {f(res['rho_dVA_VoI'])}.",
         "- ρ(ΔV_KW, VoI) at other τ: " + ", ".join(f"τ = {t}: {f(x)}" for t, x in res["rho_dV_VoI_tau"].items()) + ".",
         f"- ρ(L, ΔV_KW) = {res['rho_L_dV']:+.3f}.",
         f"- Half-value information R_½ / I_act ({res['r_half']['n']} organisms): median {res['r_half']['median']:.3f}, "
         f"10 % {res['r_half']['q10']:.3f}, 90 % {res['r_half']['q90']:.3f}. ρ with VoI {res['r_half']['rho_with_VoI']:+.3f}."]
    (RES / "e23_b4a_homeostat.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
