# E6b / S2b report (auto-generated; rules in docs/S2.md)

Units: 120. tau* = 111.38. Pairs for C and TC: 4000. dt = 0.005.

| Rule | Value [95% CI] | Verdict |
|---|---|---|
| G0: rho(h, log V), rocks | +0.998 [+0.992, +0.999] | valid |
| G1: median log(V_on/V_off), oscillators | +3.125 [+2.795, +3.348] | yes |
| G2: stratified AUC of C(tau*) | +0.704 [+0.576, +0.822] | C mislabels rocks |
| G3: stratified AUC of Phi_TC | +1.000 [+1.000, +1.000] | Phi_TC mislabels rocks |
| Gate | | triggered: dissipation term mandatory |
| G4: rho(C(tau*), log V), rocks | +0.711 [+0.515, +0.844] | yes |

Description only:
- n_bins: 2
- auc_C_unstratified: 0.6916666666666667
- auc_logV_unstratified: 0.8311111111111111
- auc_C_own_lag: 0.16277777777777777
- C_star_median: {'rock': 0.012330205543653605, 'oscillator': 0.0043503387929844095}
- logV_range: {'rock': [3.91922678819638, 5.671091920767215], 'oscillator': [2.8538904080096037, 6.168033072208494]}
- min_exits: 1638
- n_censored_lt5: 0
