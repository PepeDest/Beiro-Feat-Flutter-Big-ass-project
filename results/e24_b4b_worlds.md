# E24: stored semantic information against Φ_TC on the S1 structures (niche B, step B4b)

Rules: docs/B.md, B4b.

W0 (Φ_TC equals S1b phase C): pass. W1 (S is stationary): pass. 90 worlds, 5580 structures.

| Score | ρ with log V, pooled | ρ with log V, equal size |
|---|---|---|
| Phi_TC | +0.343 [+0.274, +0.418] | +0.572 [+0.516, +0.624] |
| S_G | +0.197 [+0.167, +0.226] | +0.170 [+0.132, +0.203] |
| dV_KW | -0.161 [-0.205, -0.112] | -0.174 [-0.220, -0.120] |
| I_act | +0.124 [+0.100, +0.151] | +0.201 [+0.172, +0.229] |
| efficiency | -0.006 [-0.076, +0.069] | +0.038 [-0.000, +0.075] |

| Rule | Question | Value | Verdict |
|---|---|---|---|
| Q1 | Does S_G rank structures (pooled)? | +0.197 [+0.167, +0.226] | ranks structures |
| Q2 | Does ΔV_KW rank structures (pooled)? | -0.161 [-0.205, -0.112] | does not rank structures |
| Q3 | ρ(Φ_TC) − ρ(S_G), pooled | +0.146 [+0.085, +0.209] | Phi_TC better |
| Q4 | ρ(Φ_TC) − ρ(S_G), equal size | +0.402 [+0.344, +0.464] | Phi_TC better |

Description:
- Methods: {'root (dy = 1)': 11, 'root (dy = 1): only p = 1': 529, 'drive (dx = 1)': 540, 'search': 4500}.
- Semantic efficiency S_G / I_act: median 0.556. ΔV_KW > 0 in 0.311.
- Over all structures: ρ(S_G, Φ_TC) = +0.460, ρ(S_G, size) = +0.180.
- By family (pooled ρ with log V): driven: Φ_TC +0.419 [+0.320, +0.509], S_G +0.181 [+0.117, +0.249], ΔV_KW -0.137 [-0.214, -0.065]; equilibrium: Φ_TC +0.006 [-0.065, +0.077], S_G +0.198 [+0.170, +0.229], ΔV_KW -0.261 [-0.300, -0.228]; modular_driven: Φ_TC +0.604 [+0.549, +0.654], S_G +0.213 [+0.168, +0.257], ΔV_KW -0.086 [-0.194, +0.029].
