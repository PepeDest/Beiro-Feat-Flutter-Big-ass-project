# E32: the semcontrols package against this repository (niche I)

Rules: docs/I.md.

| Rule | Value | Verdict |
|---|---|---|
| I1a | homeostat (B, D, S): largest difference 0.0e+00. Units equal: True | pass |
| I1b | ΔV_KW < 0 without feedback in 1.000. S_KW against I(A; h): 4.0e-15. Reader: largest \|ΔV_KW\| or S_KW 0.0e+00. CLD against vlife: 0.0e+00 | pass |
| I1c | order fraction ΔV_KW 0.7873, CLD χ₁ 0.6000. rocks_order AUC 0.7112 [0.6761, 0.7481] (K1 0.7112) | pass |

Description: `check` with ΔV_KW: homeostat_zero fail, homeostat_order pass, reader_zero pass. CLD χ₁ on the reader control: median 0.0326, smallest χ₁ / se -2.2. Time 123 s.
