# E16: controlled worlds (niche A, step A3)

Rules: docs/A.md. 95 % bootstrap intervals over worlds.

Sanity checks: {'y_zero_at_equilibrium': True, 'sigma_osc_fixed_in_eta': True, 'sigma_nn_zero_at_eta0': True, 'min_structures': 62}

| Rule | Contrast | Value [95 % CI] | Verdict |
|---|---|---|---|
| Q1 | y(ω 4, η 0) − y(ω 0, η 0) | -0.308 [-0.322, -0.295] | shortens life |
| Q2 | y(ω 0, η cap) − y(ω 0, η 0) | -0.053 [-0.061, -0.046] | shortens life |
| Q3 | y(ω, η cap) − y(ω, η 0), mean over ω 1, 2, 4 | -0.055 [-0.065, -0.044] | shortens life |
| Q4 | |Q1| − |Q3| | +0.253 [+0.233, +0.275] | oscillation dominates |

Mean y over worlds (rows ω, columns η / η_cap):

| ω | 0.00 | 0.33 | 0.67 | 1.00 |
|---|---|---|---|---|
| 0 | +0.000 | -0.004 | -0.019 | -0.053 |
| 1 | -0.078 | -0.084 | -0.101 | -0.132 |
| 2 | -0.183 | -0.189 | -0.203 | -0.236 |
| 4 | -0.308 | -0.315 | -0.330 | -0.365 |
