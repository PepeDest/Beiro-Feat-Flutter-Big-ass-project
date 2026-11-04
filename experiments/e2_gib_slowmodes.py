"""E2 - instruments from 'option A': Gaussian information bottleneck (critical-beta ladder) and slow modes.
Shows (i) new effective degrees of freedom switch on at discrete critical trade-offs [Chechik05],
(ii) GIB and TICA directions coincide for reversible worlds and split for irreversible ones [WuNoe20 context]."""
import numpy as np
from common import RES, save_json
from vlife.worlds import make_world
from vlife.gaussian import lagged_cov
from vlife.gib import gib_modes, gib_projection, gib_objective, tica_modes, subspace_gap

out = {}
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
for fam, col in (("equilibrium", "tab:blue"), ("driven", "tab:red")):
    gaps, ladders = [], []
    for s in range(20):
        w = make_world(fam, 6, np.random.default_rng(100 + s)); tau = 1.0
        Sxy = lagged_cov(w.B, w.S, tau).T
        lam, V, bc = gib_modes(w.S, w.S, Sxy); ladders.append(bc)
        mu, Vt = tica_modes(Sxy, w.S)
        gaps.append([subspace_gap(V[:k], Vt[:k]) for k in (1, 2, 3)])
    out[fam] = dict(mean_subspace_gap_k123=np.mean(gaps, 0), first_critical_beta_mean=float(np.mean([b[0] for b in ladders])))
    betas = np.linspace(1, 60, 600)
    w = make_world(fam, 6, np.random.default_rng(100)); Sxy = lagged_cov(w.B, w.S, 1.0).T
    nmodes = [gib_projection(w.S, w.S, Sxy, b).shape[0] for b in betas]
    ax[0].step(betas, nmodes, where="post", c=col, label=f"{fam} (example world)")
    ax[1].boxplot(np.array(gaps), positions=np.array([1, 2, 3]) + (0.2 if fam == "driven" else -0.2), widths=0.3,
                  boxprops=dict(color=col), medianprops=dict(color=col))
ax[0].set_xlabel("trade-off beta"); ax[0].set_ylabel("# active GIB modes"); ax[0].legend(); ax[0].set_title("Mode ladder (bifurcations of the variational problem)")
ax[1].set_xticks([1, 2, 3]); ax[1].set_xlabel("k (number of modes)"); ax[1].set_ylabel("largest principal angle GIB vs TICA (rad)")
ax[1].set_title("GIB vs TICA subspaces: blue=equilibrium, red=driven"); ax[1].set_yscale("symlog", linthresh=1e-8)
plt.tight_layout(); plt.savefig(RES / "e2_gib_slowmodes.png", dpi=130)
save_json("e2_gib_slowmodes.json", out); print(out)
