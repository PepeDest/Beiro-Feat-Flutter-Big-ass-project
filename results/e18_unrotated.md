# E18: controlled worlds without rotation (niche A, step A5, part 1)

Rules: docs/A.md. 95 % bootstrap intervals over worlds. Values are mean log R = log(V_on / V_eq).

Sanity checks: {'y_zero_at_omega0': True, 'sigma_nn_zero': True, 'n_whole': 6, 'n_cut': 56, 'min_whole_ok': 6, 'min_cut_ok': 56}

| Rule | Statistic | Value [95 % CI] | Verdict |
|---|---|---|---|
| W1 | whole: mean over ω 1, 2, 4 | -0.003 [-0.013, +0.007] | no effect within +-0.05 |
| W1 | whole, ω 1 | -0.002 [-0.010, +0.007] | no effect within +-0.05 |
| W1 | whole, ω 2 | -0.001 [-0.012, +0.009] | no effect within +-0.05 |
| W1 | whole, ω 4 | -0.006 [-0.020, +0.008] | no effect within +-0.05 |
| C1 | cut, ω 1 | -0.082 [-0.090, -0.074] | shortens life |
| C1 | cut, ω 2 | -0.183 [-0.194, -0.172] | shortens life |
| C1 | cut, ω 4 | -0.287 [-0.302, -0.273] | shortens life |
| C2 | C(ω 4) − C(ω 1) | -0.205 [-0.219, -0.191] | shortens life |
| C3 | mean ρ(x_cross, log R) in world × size, ω 4 | -0.542 [-0.620, -0.470] | shortens life |

Sensitivity (description only), worlds 0-4, dt 0.01: {'W_4': 0.021882863262820646, 'C_4': -0.2911146703077121, 'C_4_main_same_worlds': -0.2758019364786649, 'W_4_main_same_worlds': -0.009310007250819619}
