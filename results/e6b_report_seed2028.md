# E6b / S2b report (auto-generated; rules in docs/S2.md)

Units: 120. tau* = 100.33. Pairs for C and TC: 4000. dt = 0.01.

| Rule | Value [95% CI] | Verdict |
|---|---|---|
| G0: rho(h, log V), rocks | +0.998 [+0.993, +0.999] | valid |
| G1: median log(V_on/V_off), oscillators | +3.282 [+2.946, +3.543] | yes |
| G2: stratified AUC of C(tau*) | +0.637 [+0.531, +0.796] | C mislabels rocks |
| G3: stratified AUC of Phi_TC | +1.000 [+1.000, +1.000] | Phi_TC mislabels rocks |
| Gate | | triggered: dissipation term mandatory |
| G4: rho(C(tau*), log V), rocks | +0.839 [+0.667, +0.923] | yes |

Description only:
- n_bins: 3
- auc_C_unstratified: 0.6708333333333333
- auc_logV_unstratified: 0.7711111111111111
- auc_C_own_lag: 0.1836111111111111
- C_star_median: {'rock': 0.010418806137476366, 'oscillator': 0.001679398710712654}
- logV_range: {'rock': [3.9469385419366585, 5.67942434215016], 'oscillator': [2.9594702528995547, 7.380094639820238]}
- min_exits: 1629
- n_censored_lt5: 0
