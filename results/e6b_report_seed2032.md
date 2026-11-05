# E6b / S2b report (auto-generated; rules in docs/S2.md)

Units: 120. tau* = 85.60. Pairs for C and TC: 4000. dt = 0.01.

| Rule | Value [95% CI] | Verdict |
|---|---|---|
| G0: rho(h, log V), rocks | +0.998 [+0.991, +0.999] | valid |
| G1: median log(V_on/V_off), oscillators | +3.329 [+3.121, +3.549] | yes |
| G2: stratified AUC of C(tau*) | +0.528 [+0.402, +0.654] | no difference |
| G3: stratified AUC of Phi_TC | +1.000 [+1.000, +1.000] | Phi_TC mislabels rocks |
| Gate | | not triggered |
| G4: rho(C(tau*), log V), rocks | +0.809 [+0.664, +0.907] | yes |

Description only:
- n_bins: 3
- auc_C_unstratified: 0.5752777777777778
- auc_logV_unstratified: 0.6991666666666667
- auc_C_own_lag: 0.2811111111111111
- C_star_median: {'rock': 0.014387048845359018, 'oscillator': 0.010085419185768885}
- logV_range: {'rock': [3.951815374770737, 5.6437014077885195], 'oscillator': [2.7699974621045493, 6.704289244229539]}
- min_exits: 1607
- n_censored_lt5: 0
