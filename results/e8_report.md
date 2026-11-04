# E8 / S5 report (auto-generated; rules in docs/S5.md)

Thresholds (calibration worlds): {"equilibrium": {"static": 0.039999999999999994, "dynamic": 0.25999999999999995, "static_F1": 1.0, "dynamic_F1": 0.991658243703213}, "driven": {"static": 0.06999999999999999, "dynamic": 0.27999999999999997, "static_F1": 0.9832865127032523, "dynamic_F1": 1.0}}

| Rule | Detector | Family | Blanket recovery [95% CI] | Edge precision / recall | Verdict |
|---|---|---|---|---|---|
| B1 | static exact | equilibrium | 1.00 [0.95, 1.00] | 1.00 / 1.00 | recovers |
| B1 | dynamic exact | equilibrium | 1.00 [0.95, 1.00] | 1.00 / 1.00 | recovers |
| B2 | static finite | equilibrium | 1.00 [0.95, 1.00] | 1.00 / 1.00 | recovers |
| B2 | dynamic finite | equilibrium | 0.88 [0.78, 0.93] | 0.98 / 0.99 | recovers |
| B1 | static exact | driven | 0.00 [-0.00, 0.05] | 0.17 / 1.00 | fails |
| B1 | dynamic exact | driven | 1.00 [0.95, 1.00] | 1.00 / 1.00 | recovers |
| B2 | static finite | driven | 0.99 [0.93, 1.00] | 1.00 / 0.98 | recovers |
| B2 | dynamic finite | driven | 0.91 [0.83, 0.96] | 0.99 / 1.00 | recovers |

| Rule | Score | Family | Median percentile of planted interiors [95% CI] | Verdict |
|---|---|---|---|---|
| D1 | Phi_TC | equilibrium | 0.018 [0.011, 0.037] | does not find |
| D1 | C | equilibrium | 0.383 [0.289, 0.496] | does not find |
| D1 | TC | equilibrium | 0.992 [0.987, 0.995] | finds structures |
| D1 | closure | equilibrium | 0.996 [0.993, 0.997] | finds structures |
| D1 | Phi_TC | driven | 0.041 [0.014, 0.061] | does not find |
| D1 | C | driven | 0.590 [0.487, 0.699] | does not find |
| D1 | TC | driven | 0.989 [0.983, 0.993] | finds structures |
| D1 | closure | driven | 0.995 [0.993, 0.995] | finds structures |

Description: driven worlds, exact static partial correlations: median of max |r| between interior and exterior 0.034; median |r| on true edges 0.149.
