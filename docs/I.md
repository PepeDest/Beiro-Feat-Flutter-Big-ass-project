# Niche I: `semcontrols`, a package of negative controls for semantic scores

This file starts on 2026-11-27. The plan is in `ROADMAP_DI.md`. The rules come before the code.

## I0. What the package holds (fixed 2026-11-27)

**Why.** Each new semantic score needs controls with known answers. Our controls are in this repository, mixed with
other code. `semcontrols` puts them in one small package. It needs numpy and scipy only, and it does not import
`vlife`.

**Three controls.**

| Control | Systems | Known answer | Source |
|---|---|---|---|
| `homeostat` | The 400 S3 organisms (seed 2026), intact and without feedback (L = 0). Linear, exact | The organism without feedback uses no information. Its simulated VoI is 0 by construction. The intact organism uses information (VoI > 0 in 99 % of organisms, docs/S3.md) | docs/S3.md, docs/C.md (C1) |
| `reader` | 200 random linear systems in which the environment reads the agent: B_xy = 0, B_yx ≠ 0. dx in {1, 2, 3}, dy = 1 | The agent cannot use the environment, because the environment does not act on it. ΔV_KW = 0 and S_KW = 0 for every τ (docs/B.md, B1) | ours, new |
| `rocks` | The 840 S2b units (rocks and oscillators of 7 draws), with V_on, V_off and τ* | Neither class uses information about an environment. A score of use must not rate rocks above oscillators of the same life. The flux ratio log(V_on / V_off) is 0 for rocks and above 0 for oscillators | docs/S2.md, docs/C.md (C2) |

**The test function.** `semcontrols.check(linear_score=..., unit_score=..., unit_values=...)` runs a score on the
controls and gives these tests:

| Test | Question | Verdict |
|---|---|---|
| `homeostat_zero` | Is the score 0 without feedback? | "pass" if \|score\| ≤ tol in all organisms (tol = 10⁻⁹ by default) |
| `homeostat_order` | Does the score put the intact organism above the one without feedback? | the fraction of organisms with score(intact) > score(no feedback), 1000 bootstrap resamples. "pass" if CI low > 0.5 |
| `reader_zero` | Is the score 0 when the environment only reads the agent? | as `homeostat_zero` |
| `rocks_order` | Does the score rate rocks above oscillators of the same life? | the stratified AUC of S2b (tertiles of log V_on), mean over the 7 draws, 10 000 bootstrap resamples of draws. "fail" if CI low > 0.5, else "pass" |

A score can skip a control: the user gives only `linear_score`, or only `unit_score` or precomputed `unit_values`.

**Reference scores in the package.** ΔV_KW (Eq. (6) of KolchinskyWolpert18, V = −H of the target at τ), the stored
semantic information S_KW (dy = 1, the root search of docs/B.md, B4, in the reading V = V_act), CLD for linear
systems (exact Gaussian laws, Monte Carlo JS, docs/C.md), CLD for the units (the mirror method of docs/C.md, C2), and
the flux ratio.

## I1 and I2. Rules (fixed 2026-11-27, before the code)

| Rule | Question | Verdict |
|---|---|---|
| I1a | Are the controls the same as in this repository? | "pass" if the (B, D, S) of the homeostat equal `vlife.agency.homeostat` to 10⁻¹² for all 400 organisms and both versions, and the unit data equal `results/e26_v_dataset.pkl` and `cluster/data/f_units.json` exactly |
| I1b | Do the reference scores give the known answers? | "pass" if all hold: ΔV_KW < 0 without feedback in all 400 organisms (F6 of docs/C.md). S_KW = I(A; h) without feedback in all 400 (F4). \|ΔV_KW\| < 10⁻¹⁰ and S_KW < 10⁻¹⁰ in all 200 reader systems at τ in {0.5, 1, 5}. CLD of the package equals `vlife.negative_controls.cld_gaussian` with the same seeds on 5 organisms, to 10⁻¹² |
| I1c | Does `check` give the verdicts of niche C? | "pass" if, on the 395 organisms of C1, the order fraction of ΔV_KW is 0.787 and of CLD χ₁ 0.600 (to 10⁻³), and the `rocks_order` AUC of the stored χ₃ values is the K1 value 0.711 [0.676, 0.748] of `results/e26_c2_rocks.json` (to 10⁻⁹) |
| I1d | Does the package install and test from the repository? | "pass" if `pip install ./semcontrols` works in a new venv, and its tests pass there |
| I2 | Does the README example run in under 1 minute? | "pass" if the example (ΔV_KW and CLD on each control, with small sizes) runs in under 60 s on this PC |

**Expectations.** All "pass". The new `reader` control has no earlier result. Its known answer comes from the
closed form of docs/B.md (B1: if Φ_XY = 0, V does not depend on P).

**What the README must say.** Each control, its known answer and its source. How a reader adds a score. That a "pass"
on these controls is necessary, not sufficient: the controls test only that a score does not confuse correlation or
passive memory with use.
