"""E7 / S2c - dissipation term in Phi, on existing S2, S2b and S1 data. Rules: docs/S2c.md. No simulation."""
import pickle
import numpy as np
from scipy.stats import spearmanr
from common import RES, save_json
from vlife.nonlinear import T
from vlife.gaussian import total_correlation, structure_entropy_production

rng = np.random.default_rng(0)
f3 = lambda x: f"{x[0]:+.3f} [{x[1]:+.3f}, {x[2]:+.3f}]"


def boot_units(n, fn, n_boot=1000):
    pt = fn(np.arange(n)); bs = [fn(rng.integers(0, n, n)) for _ in range(n_boot)]
    lo, hi = np.nanpercentile(bs, [2.5, 97.5]); return [float(pt), float(lo), float(hi)]


def label(x, pos="yes", neg="no", mid="no clear effect"):
    return pos if x[1] > 0 else neg if x[2] < 0 else mid


# ---------------------------------------------------------------- part A: nonlinear units (S2, S2b)
s2 = pickle.load(open(RES / "e6_dataset.pkl", "rb"))
power = {r["i"]: r["power"] for r in s2}
s2b = pickle.load(open(RES / "e6b_dataset.pkl", "rb")); rows_b, tau_star = s2b["rows"], s2b["tau_star"]
A = {}
for name, rows in (("S2b", rows_b), ("S2", s2)):
    osc = [r for r in rows if r["kind"] == "oscillator"]
    sig = np.array([power[r["i"]] / T for r in osc]); lV = np.log([r["V_on"] for r in osc])
    lR = lV - np.log([r["V_off"] for r in osc]); n = len(osc)
    A[name] = dict(rho_sigma_logV=boot_units(n, lambda i: spearmanr(sig[i], lV[i])[0]),
                   rho_sigma_logR=boot_units(n, lambda i: spearmanr(sig[i], lR[i])[0]),
                   sigma_median=float(np.median(sig)))
kind = np.array([r["kind"] for r in rows_b])
phiD = np.array([r["C_star"] - 0.25 * r["TC"] + power[r["i"]] / T * tau_star for r in rows_b])
check = float(np.mean(phiD[kind == "rock"][:, None] > phiD[kind == "oscillator"][None, :]))
v = dict(D1=label(A["S2b"]["rho_sigma_logV"]), D2=label(A["S2b"]["rho_sigma_logR"]))


# ---------------------------------------------------------------- part B: linear worlds (S1 baseline and D-test r = 3)
def linear(tag):
    data = pickle.load(open(RES / f"e3_dataset{tag}.pkl", "rb"))
    r3, d4 = [], []
    for d in data:
        if d["family"] == "equilibrium":
            continue
        m = (d["ev_on"] >= 5) & (d["ev_eq"] >= 5)
        if m.sum() < 8:
            continue
        Dm = d.get("D", np.eye(d["B"].shape[0])); subs = [s for s, k in zip(d["subsets"], m) if k]
        sA = np.array([structure_entropy_production(d["B"], Dm, d["S"], s) for s in subs])
        TC = np.array([total_correlation(d["S"], s) for s in subs]); f = d["feat"]
        y = np.log(d["V_on"][m]); size = f["size"][m]; tau = d["tau"]
        phi = f["P"][m] + f["C"][m] - 0.25 * TC; phiD = phi + sA * tau
        rs = [spearmanr(sA[size == k], y[size == k])[0] for k in np.unique(size) if (size == k).sum() >= 6]
        r3.append(np.nanmean(rs)); d4.append(spearmanr(phiD, y)[0] - spearmanr(phi, y)[0])
    r3, d4 = np.array(r3), np.array(d4)
    cb = lambda a: boot_units(len(a), lambda i: np.nanmean(a[i]), 400)
    return dict(n_worlds=len(r3), D3=cb(r3), D4=cb(d4))


B = {"baseline": linear(""), "Dtest_r3": linear("_D3")}
lab3 = lambda x: label(x, "lengthens life", "shortens life", "no effect")
lab4 = lambda x: label(x, "helps", "hurts", "no effect")
v.update(D3=lab3(B["baseline"]["D3"]), D4=lab4(B["baseline"]["D4"]),
         D5=f"D3: {lab3(B['Dtest_r3']['D3'])}, D4: {lab4(B['Dtest_r3']['D4'])}")
save_json("e7_dissipation.json", dict(nonlinear=A, linear=B, check_auc_phiD_S2b=check, verdicts=v))
L = ["# E7 / S2c report (auto-generated; rules in docs/S2c.md)\n",
     "| Rule | Data | Value [95% CI] | Verdict |", "|---|---|---|---|",
     f"| D1: rho(sigma, log V_on), oscillators | S2b | {f3(A['S2b']['rho_sigma_logV'])} | {v['D1']} |",
     f"| D2: rho(sigma, log V_on/V_off), oscillators | S2b | {f3(A['S2b']['rho_sigma_logR'])} | {v['D2']} |",
     f"| D3: rho(sigma_A, log V), equal size | S1 baseline ({B['baseline']['n_worlds']} worlds) | {f3(B['baseline']['D3'])} | {v['D3']} |",
     f"| D4: rho(Phi_D) - rho(Phi_TC) | S1 baseline | {f3(B['baseline']['D4'])} | {v['D4']} |",
     f"| D5: D3 | S1 D-test r 3 ({B['Dtest_r3']['n_worlds']} worlds) | {f3(B['Dtest_r3']['D3'])} | {lab3(B['Dtest_r3']['D3'])} |",
     f"| D5: D4 | S1 D-test r 3 | {f3(B['Dtest_r3']['D4'])} | {lab4(B['Dtest_r3']['D4'])} |",
     "\nDescription only:",
     f"- S2 (outer-edge viability): rho(sigma, log V_on) {f3(A['S2']['rho_sigma_logV'])}, rho(sigma, log R) {f3(A['S2']['rho_sigma_logR'])}",
     f"- median sigma of oscillators: {A['S2b']['sigma_median']:.2f} per time unit",
     f"- check by construction, S2b: AUC of Phi_D (rock > oscillator) = {check:.2f}"]
(RES / "e7_dissipation.md").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L))
