# Niche F: a map of the free choices of CLD

This file starts on 2026-11-27. The plan is in `ROADMAP_DI.md`. The model, the units and the rule K1 come from C2
(`docs/C.md`). Each step writes its rules before its runs, and the results come after.

## F0. The open choices
SowinskiEtAl25 define χ_LD = D(p ‖ p̂) / Ω_scr (Eq. (7), with D the Jensen–Shannon divergence). The paper leaves open
the scrambled bit, Ω_scr, the time of the measure and the functional. It says that other functionals need a test (Sec.
"Discussion"). C2 used one choice: JS, a 40 × 40 histogram, 20 000 walkers in each group, the time average χ₃ on
[0, τ*], and the subtraction of the histogram bias (the scrambled group). C2 found AUC 0.711 [0.676, 0.748]: CLD rates
the rocks above the oscillators of the same life.

We keep the bit (b = sign(x)) and Ω_scr = 1 bit. The mirror symmetry R(x, v) = (−x, −v) of the units makes the
scrambled law exact for this bit only (`docs/C.md`). So F varies the other three choices and the estimator.

## F1. Rules (fixed 2026-11-27, before the run)

**Units.** The 840 units of C2 (7 draws, seeds 2026 to 2032, the parameters in `results/e26_v_dataset.pkl`). The V of
each unit and τ* of each draw come from C2. No new V.

**Simulation.** For each unit: two groups of 80 000 walkers (known bit, scrambled bit), as in `cld_mirror`, with
dt = 0.01 and a burn-in of 50. Times: 41 equal steps on [0, τ*], 41 equal steps on [0, V], and V/2. The first 20 000
walkers of each group give the 20 000-walker estimates. Seeds [seed, i, 41].

**Choices (5 × 3 × 2 × 4 × 2 = 240).**
| Choice | Options |
|---|---|
| Functional D(p ‖ q), q = (p + Rp)/2 | JS (bits), KL(p ‖ q) (bits), KL(q ‖ p) (bits), squared Hellinger (1 − Σ√(pq)), total variation. The two KL use a pseudo-count of 0.5 walkers in each cell, because KL(q ‖ p) is infinite when a cell of p is empty |
| Histogram | 20 × 20, 40 × 40, 80 × 80 cells |
| Walkers in each group | 20 000, 80 000 |
| Time | χ₃ on [0, τ*], χ₁ at τ*, χ at the own lag V/2, χ₃ on [0, V] |
| Bias | subtract the scrambled group (as C2), or not |

**Score of a choice.** The stratified AUC of C2 (tertiles of log V, AUC = P(rock > oscillator)) in each draw, then the
mean over the 7 draws with 10 000 bootstrap resamples of draws.

| Rule | Question | Verdict |
|---|---|---|
| F1a | Does the C2 choice give the C2 value again? | "agrees" if the AUC of (JS, 40, 20 000, χ₃ on [0, τ*], subtract) is within 0.03 of 0.711 |
| F1b | How many choices pass the control? | For each choice: "passes" if the CI is below 0.5, "mislabels rocks" if the CI is above 0.5, else "no difference". Report the three counts |
| F1c | Which choice matters most? | For each of the four choices, the range of the mean AUC when only that choice changes (median over the other choices). Descriptive |
| Gate | Is the C2 failure an artefact of our choice? | "no" if no choice passes. Else "partly", with the list of the choices that pass |

**Expectations.** F1a "agrees". F1b: the choices with the own lag V/2 or with [0, V] pass, and the choices with τ* do
not. C2 saw a mean unstratified AUC of 0.341 at the own lag. F1c: the time matters most. Gate: "partly". If this holds,
the message to the readers is: the verdict of CLD on a passive system depends on the time of the measure, and the paper
must fix it.

**Where it runs.** On the Xeon machines (`cluster/`). One task is one unit.
