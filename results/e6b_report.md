# E6b / S2b report (auto-generated; rules in docs/S2.md)

Units: 120. tau* = 118.31.

| Rule | Value [95% CI] | Verdict |
|---|---|---|
| G0: rho(h, log V), rocks | +0.999 [+0.994, +0.999] | valid |
| G1: median log(V_on/V_off), oscillators | +3.138 [+2.793, +3.414] | yes |
| G2: stratified AUC of C(tau*) | +0.757 [+0.598, +0.856] | C mislabels rocks |
| G3: stratified AUC of Phi_TC | +1.000 [+1.000, +1.000] | Phi_TC mislabels rocks |
| Gate | | triggered: dissipation term mandatory |
| G4: rho(C(tau*), log V), rocks | +0.762 [+0.601, +0.875] | yes |

Description only:
- n_bins: 2
- auc_C_unstratified: 0.7077777777777777
- auc_logV_unstratified: 0.8238888888888889
- auc_C_own_lag: 0.17833333333333334
- C_star_median: {'rock': 0.012412181983789239, 'oscillator': -0.00038779453374360173}
- logV_range: {'rock': [3.930651438533346, 5.682109323851661], 'oscillator': [2.821570938706006, 6.215266516840487]}
- min_exits: 1642
- n_censored_lt5: 0
