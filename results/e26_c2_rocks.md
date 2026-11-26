# E26: Causal Leverage Density of S2b rocks and oscillators (niche C, step C2)

Rules: docs/C.md, C2.

T1 (rebuilt S2b data equal the summaries in all 7 draws): pass. Walkers: 20000 in each group. dt = 0.01.

| Rule | Question | Value | Verdict |
|---|---|---|---|
| K1 | Stratified AUC of χ₃(0, τ*), rock > oscillator, mean over 7 draws | 0.711 [0.676, 0.748] | CLD mislabels rocks |
| K2 | Stratified AUC of χ₁(τ*) | 0.632 [0.576, 0.696] | CLD mislabels rocks |
| K3 | ρ(χ₃, log V) over rocks | 0.997 [0.996, 0.998] | yes |
| Gate | Does CLD pass the control? | | fails: use the flux ratio V_on / V_off |

| Seed | τ* | AUC χ₃ | AUC χ₁ | median χ₃ rock / osc | AUC own lag (unstratified) | AUC C(τ*) (S2b) | bias at τ* |
|---|---|---|---|---|---|---|---|
| 2026 | 118.3 | 0.784 | 0.784 | 0.0510 / 0.0273 | 0.280 | 0.757 | 0.0049 |
| 2027 | 79.5 | 0.646 | 0.514 | 0.0529 / 0.0417 | 0.406 | 0.463 | 0.0049 |
| 2028 | 100.3 | 0.655 | 0.635 | 0.0529 / 0.0334 | 0.317 | 0.637 | 0.0049 |
| 2029 | 94.7 | 0.727 | 0.599 | 0.0529 / 0.0366 | 0.362 | 0.518 | 0.0050 |
| 2030 | 87.5 | 0.682 | 0.565 | 0.0535 / 0.0421 | 0.406 | 0.491 | 0.0049 |
| 2031 | 91.4 | 0.766 | 0.635 | 0.0534 / 0.0366 | 0.256 | 0.629 | 0.0050 |
| 2032 | 85.6 | 0.717 | 0.690 | 0.0528 / 0.0385 | 0.362 | 0.528 | 0.0049 |

Description: mean AUC at the own lag V/2 0.341. Mean AUC of C(τ*) in S2b 0.575. Time 150 min.
