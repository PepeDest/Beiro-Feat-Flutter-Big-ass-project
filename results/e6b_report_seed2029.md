# E6b / S2b report (auto-generated; rules in docs/S2.md)

Units: 120. tau* = 94.74. Pairs for C and TC: 4000. dt = 0.01.

| Rule | Value [95% CI] | Verdict |
|---|---|---|
| G0: rho(h, log V), rocks | +0.997 [+0.991, +0.999] | valid |
| G1: median log(V_on/V_off), oscillators | +3.413 [+3.033, +3.710] | yes |
| G2: stratified AUC of C(tau*) | +0.518 [+0.414, +0.640] | no difference |
| G3: stratified AUC of Phi_TC | +1.000 [+1.000, +1.000] | Phi_TC mislabels rocks |
| Gate | | not triggered |
| G4: rho(C(tau*), log V), rocks | +0.913 [+0.813, +0.957] | yes |

Description only:
- n_bins: 3
- auc_C_unstratified: 0.6052777777777778
- auc_logV_unstratified: 0.7369444444444444
- auc_C_own_lag: 0.19
- C_star_median: {'rock': 0.015664612953464108, 'oscillator': 0.009210301640902863}
- logV_range: {'rock': [3.986950425946041, 5.703868068771855], 'oscillator': [2.833088297741177, 6.746753519236675]}
- min_exits: 1648
- n_censored_lt5: 0
