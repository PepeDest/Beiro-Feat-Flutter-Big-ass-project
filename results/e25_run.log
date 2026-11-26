# E25: negative control in the S3 homeostat (niche C, step C1)

Rules: docs/C.md, C1.

A0 (rebuilt S3 data equal phase C): pass. Organisms: 395. Versions: intact, no feedback.

| Rule | Question | Value | Verdict |
|---|---|---|---|
| N1 | ΔV_KW zero without feedback? | max \|ΔV\| 0.32, ΔV < 0 in 1.000, median -0.2551 | not zero |
| N2 | S_KW zero without feedback? | smallest 0.283 nats, median efficiency 1.000 (= 1 in 1.000) | not zero |
| N3 | CLD zero without feedback? | smallest χ₁ 0.0303, smallest χ₁ / se 60.4, median χ₁ 0.0943 | not zero |
| N4 | ΔV_KW: fraction intact > no feedback | 0.787 [0.747, 0.823] | intact higher |
| N4 | S_KW: fraction intact > no feedback | 0.433 [0.385, 0.481] | no feedback higher |
| N4 | CLD χ₁: fraction intact > no feedback | 0.600 [0.552, 0.646] | intact higher |

Description (medians):

| Score | Intact | No feedback |
|---|---|---|
| dV | -0.0230 | -0.2551 |
| dV_A | +0.0114 | -0.0564 |
| I_act | +0.7726 | +0.8144 |
| S_kw | +0.7726 | +0.8144 |
| S_kw_geq | +0.0000 | +0.0000 |
| omega_bits | +1.1146 | +1.1750 |
| chi1 | +0.0952 | +0.0943 |
| chi1_agent | +0.0486 | +0.0381 |
| chi3 | +0.0576 | +0.0544 |

- ΔV on the whole agent < 0 without feedback in 0.577 of organisms.
- S_KW in the reading V ≥ V_act is 0 without feedback in 1.000 of organisms.
- Efficiency S_KW / I_act, intact: median 1.000.
- Methods: {'root (dy = 1): only p = 1': 790}.
- The simulated VoI is 0 by construction without feedback (the actuator reads nothing).
