"""Post-hoc check for niche E (not a rule, added 2026-11-27 after the run). In E2a no random class Z garbling met
V = V_actual, so the check was empty for class Z. Here: perturb the optimum at random, then mix it with
H_max = 1{Re K > 0} (the largest V of class Z) to meet V = V_actual exactly. No draw may beat the optimum."""
import json, sys
import numpy as np
from e30_e_coli import P0, Grid, solve, spectra, RES

p = {k: v for k, (v, s) in P0.items()}
g = Grid(4000)
I_full, S_opt, V_act, H, (I, V) = solve(p, g, "Z")
K = spectra(g.w, p)[1]
Hmax = (np.real(K) > 0).astype(float)
rng = np.random.default_rng(3003)
x = np.log(g.w); best, n = np.inf, 0
for k in range(1000):
    c = rng.normal(size=12) * rng.uniform(0.01, 0.5)
    d = sum(c[j] * np.cos(j * (x - x[0]) / (x[-1] - x[0]) * np.pi) for j in range(12))
    Hr = np.clip(H + d, 0.0, 1.0)
    v0, v1 = V(Hr), V(Hmax)
    t = (V_act - v0) / (v1 - v0)
    if not 0.0 <= t <= 1.0:
        Hr = np.clip(H * rng.uniform(0.5, 1.5), 0, 1); v0 = V(Hr); t = (V_act - v0) / (v1 - v0)
        if not 0.0 <= t <= 1.0:
            continue
    Hf = Hr + t * (Hmax - Hr)
    n += 1; best = min(best, I(Hf))
out = dict(S_opt=S_opt, best=best, ratio=best / S_opt, n_feasible=n, passed=bool(best >= S_opt * (1 - 1e-9)))
(RES / "e30b_posthoc_z_check.json").write_text(json.dumps(out, indent=1))
print(out)
