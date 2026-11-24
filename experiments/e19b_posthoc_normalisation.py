"""Niche A, A5, post-hoc check (not a rule, docs/A.md): does the division by lambda_A alone carry rule T1?
Run: python experiments/e19b_posthoc_normalisation.py <repository root>. Point values only."""
import pickle, sys, pathlib
import numpy as np
from scipy.stats import spearmanr
ROOT = pathlib.Path(sys.argv[1]); sys.path.insert(0, str(ROOT / "src"))
from vlife.gaussian import cross_oscillation
sys.stdout.reconfigure(encoding="utf-8")
for fn in ("e3_dataset_v2.pkl", "e3_dataset_D3_v2.pkl"):
    r_raw, r_lam = [], []
    for w in pickle.load(open(ROOT / "results" / fn, "rb")):
        if w["family"] == "equilibrium":
            continue
        ok = (w["ev_on"] >= 5) & (w["ev_eq"] >= 5)
        for k in (2, 3, 4, 5):
            idx = [j for j, s in enumerate(w["subsets"]) if len(s) == k and ok[j]]
            if len(idx) < 5:
                continue
            y = [np.log(w["V_on"][j] / w["V_eq"][j]) for j in idx]
            raw = [cross_oscillation(w["B"], w["S"], w["subsets"][j]) for j in idx]
            inv = [len(w["subsets"][j]) / np.trace(w["B"][np.ix_(list(w["subsets"][j]), list(w["subsets"][j]))]) for j in idx]
            r_raw.append(spearmanr(raw, y)[0]); r_lam.append(spearmanr(inv, y)[0])
    print(fn, "rho(sigma_cross raw, logR)", round(np.nanmean(r_raw), 3), "rho(1/lambda_A, logR)", round(np.nanmean(r_lam), 3))
