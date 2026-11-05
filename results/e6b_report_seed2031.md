# E6b / S2b report (auto-generated; rules in docs/S2.md)

Units: 120. tau* = 91.40. Pairs for C and TC: 4000. dt = 0.01.

| Rule | Value [95% CI] | Verdict |
|---|---|---|
| G0: rho(h, log V), rocks | +0.997 [+0.990, +0.998] | valid |
| G1: median log(V_on/V_off), oscillators | +3.264 [+3.013, +3.443] | yes |
| G2: stratified AUC of C(tau*) | +0.629 [+0.467, +0.742] | no difference |
| G3: stratified AUC of Phi_TC | +1.000 [+1.000, +1.000] | Phi_TC mislabels rocks |
| Gate | | not triggered |
| G4: rho(C(tau*), log V), rocks | +0.760 [+0.584, +0.881] | yes |

Description only:
- n_bins: 2
- auc_C_unstratified: 0.645
- auc_logV_unstratified: 0.7930555555555555
- auc_C_own_lag: 0.16361111111111112
- C_star_median: {'rock': 0.014764020362555641, 'oscillator': 0.00688929698073526}
- logV_range: {'rock': [3.9814109489044323, 5.666272037443134], 'oscillator': [2.833586446406551, 7.014663248888719]}
- min_exits: 1623
- n_censored_lt5: 0
