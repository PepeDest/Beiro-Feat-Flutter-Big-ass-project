# E9 / S4 report (auto-generated; rules in docs/S4.md)

Worlds: 90 (S1 baseline).

| Rule | Value [95% CI] | Verdict |
|---|---|---|
| G1: rho(r, log V), a_m = 0 | +0.953 [+0.944, +0.960] | agree |
| G1: rho(r, log V), a_m = median V | +0.991 [+0.990, +0.992] | agree |
| G2: stability(r) - stability(V), p_out 0.05 -> 0.2 (0 worlds) | +nan [+nan, +nan] | not run (no p_out 0.2 dataset) |
| G3: rho(Phi_TC, r) | +0.353 [+0.288, +0.410] | yes |
| G4: selection S / transmission T | +0.008 [+0.005, +0.010] / -0.001 [-0.001, -0.001] | mutation erodes selection |

Description only:
- n_worlds: 90
- n_worlds_G2: 0
- rho_V_stability: None
- rho_r_stability: None
- frac_S_pos: 0.7444444444444445
- frac_T_neg: 0.9777777777777777
- median_a_m: 2.8135353851842506
- rho_PhiTC_logV: [0.34314085937565586, 0.27426794702839125, 0.4075158995968091]
