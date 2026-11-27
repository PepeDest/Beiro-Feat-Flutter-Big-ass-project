# E30: semantic information of E. coli chemotaxis (niche E)

Rules: docs/E.md. Model and Table S1: MattinglyKaminoMachtaEmonet21.

| Rule | Value | Verdict |
|---|---|---|
| E1a | β closed form 0.216489, integral 0.216489 bits/s/mm⁻² | agree |
| E1b | β = 0.2169 [0.1945, 0.2412] (Monte Carlo over Table S1) | agrees |
| E2a | best random garbling / optimum: A 1.4167 (171 feasible), Z inf (0 feasible) | pass |
| E2b | e_Z = 0.4392 [0.4313, 0.4473] | yes |
| E2c | e_A = 0.0863 [0.0852, 0.0874] | descriptive |
| E3a | e_Z against 0.44 ± 0.07 | match |
| E3b | e_A against 0.44 ± 0.07 | differ |

Central values: e_A = 0.0863, e_Z = 0.4391. Grid check (200 000 points): e_A = 0.0863, e_Z = 0.4391. Re K < 0 above ω = 1.426 rad/s. Time 1940 s.
