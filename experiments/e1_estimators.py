"""E1 - validate estimators against exact Gaussian closed forms (and quantify the legacy binned-MI bias)."""
import numpy as np
from scipy.linalg import expm
from common import RES, save_json
from vlife.worlds import make_world
from vlife.gaussian import joint_cov, mutual_information
from vlife.estimators import ksg_mi, binned_mi

rng = np.random.default_rng(7)
w = make_world("driven", 4, rng, flux=1.0); tau = 0.25
J = joint_cov(w.B, w.S, tau); N = 4
exact_C = mutual_information(J, [0], [N + 0])                       # I(x0_t ; x0_{t+tau})
exact_P = mutual_information(J, [0], [N + 1, N + 2, N + 3])         # I(x0_t ; x1..3_{t+tau})
P = expm(-w.B * tau); Cn = w.S - P @ w.S @ P.T
Lc, Ls = np.linalg.cholesky(Cn), np.linalg.cholesky(w.S)
out = {"exact_C": exact_C, "exact_P": exact_P, "rows": []}
print(f"exact C={exact_C:.4f} nats, exact P={exact_P:.4f} nats")
for n in (250, 1000, 4000):
    est = {"ksg_C": [], "binned_C": [], "ksg_P": []}
    for rep in range(20):
        x = rng.normal(size=(n, N)) @ Ls.T                       # i.i.d. pairs (x_t, x_{t+tau})
        y = x @ P.T + rng.normal(size=(n, N)) @ Lc.T
        est["ksg_C"].append(ksg_mi(x[:, 0], y[:, 0])); est["binned_C"].append(binned_mi(x[:, 0], y[:, 0], 12))
        est["ksg_P"].append(ksg_mi(x[:, 0], y[:, 1:]))
    row = {"n": n}
    for k, ex in (("ksg_C", exact_C), ("binned_C", exact_C), ("ksg_P", exact_P)):
        row[k] = dict(mean=float(np.mean(est[k])), sd=float(np.std(est[k])), bias=float(np.mean(est[k]) - ex))
    out["rows"].append(row); print(row)
save_json("e1_estimators.json", out)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
ns = [r["n"] for r in out["rows"]]
plt.figure(figsize=(6, 4))
for k, ls in (("ksg_C", "o-"), ("binned_C", "s--"), ("ksg_P", "^-")):
    plt.errorbar(ns, [r[k]["bias"] for r in out["rows"]], yerr=[r[k]["sd"] for r in out["rows"]], fmt=ls, label=k, capsize=3)
plt.axhline(0, c="k", lw=.5); plt.xscale("log"); plt.xlabel("independent samples"); plt.ylabel("estimate - exact (nats)")
plt.legend(); plt.title("Estimator bias vs closed form"); plt.tight_layout(); plt.savefig(RES / "e1_estimators.png", dpi=130)
