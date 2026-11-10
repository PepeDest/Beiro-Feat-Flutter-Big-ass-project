# E11 / S6b report (auto-generated; rules in docs/S6.md)

eps* = 0.001 (pilot change of cycle time -24.2%, predicted sign of S: +1). Runs: 32 + 32.

| Rule | Selection runs | Control runs (eps = 0) | Verdict |
|---|---|---|---|
| H1: fidelity | 1.0000 (18392 pairs) | 1.0000 (16152 pairs) | high fidelity |
| H2/H3: selection term S | +0.0413 [+0.0384, +0.0440] | -0.0003 [-0.0062, +0.0056] | control clean; selection detected |
| transmission term T | +0.0000 [+0.0000, +0.0000] | +0.0000 [+0.0000, +0.0000] | measured |
| H4: final fraction of type A | +0.7234 [+0.7207, +0.7258] | +0.5016 [+0.4982, +0.5049] | yes |
| H5: max error of the Price identity | 1.1e-16 | 1.1e-16 | exact |
| H6: growth law (exp wins / power wins) | 0 / 32, power median 1.92 (fitted t0: 1.92, description only), window N [8, 174] | | polynomial |
