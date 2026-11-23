# Niche A: which part of dissipation shortens the life of a structure?

This file was written on 2026-11-23, **before** any A2 result existed. The results section at the end is added after the
analysis. The plan is in `ROADMAP_ABC.md`.

## A0. Literature check (2026-11-23)
- **The decomposition.** Nagayama, Kolchinsky and Ito (arXiv 2606.07263, v1 and v2) split the steady-state entropy
  production σ of an Ornstein–Uhlenbeck process into σ_osc = Σₙ Im(λₙ)²/Re(λₙ) and σ_nn = σ − σ_osc. σ_nn is zero if and
  only if D^{-1/2} B D^{1/2} is normal. They link σ_nn to faster relaxation. They do not study exit times or persistence.
  The formula is the same in v1 and v2.
- **Its citing papers.** Semantic Scholar lists 5 citing papers (2026-11-20). None uses it for exit times or persistence.
- **Nonnormality and escape (prior art).** Troude and Sornette show that nonnormality speeds up noise-driven escape. In
  their Kramers problem the effective temperature grows with the square of the condition number
  [TroudeSornette25, TroudeSornette25b]. Other recent preprints report the same direction (arXiv 2510.07938, 2607.14786).
  So "nonnormality shortens life" is **not new** as a general statement.
- **What is different here.** Their effect comes from a larger variance. Our viability set is the 1 − p_out ellipsoid of
  the **stationary** law of each structure, and the control V_eq has the same stationary law. So a larger variance cannot
  explain a change in our log R = log(V_on/V_eq). Only the time correlations change. The question is which part of the
  dissipation goes with that change. We found no paper that asks this.
- **Not read yet.** The full text of the Troude–Sornette papers, and the exit-time variational principles for
  nonsymmetric diffusions (arXiv 2006.16446). This is a limit of A0.

## A1. Code (done 2026-11-23)
`vlife.gaussian.oscillatory_nonnormal_ep(B, D, S)` returns (σ, σ_osc, σ_nn). Tests in
`tests/test_oscillatory_nonnormal.py` (5 pass):
1. σ_osc + σ_nn = σ, and both parts are non-negative, in 10 random driven worlds.
2. σ_nn agrees with the projection definition of the paper (whitening, complex Schur form, projection with the H⁻¹
   inner product), with D = I and with a random diagonal D.
3. Equilibrium worlds: both parts are zero.
4. A normal drift B = aI + G with D = I: σ_nn = 0.
5. A symmetric B with two temperatures: σ_osc = 0 and σ_nn = σ.

Not done: the bead-spring example of the paper.

## What we looked at before writing the rules
Only the predictors, not the lives. In the S1 driven and modular worlds the nonnormal share s = σ_nn/σ has these
quantiles (10 %, 50 %, 90 %):

| Data | driven | modular |
|---|---|---|
| S1 baseline (`_v2`, D = I) | 0.03, 0.08, 0.21 | 0.01, 0.05, 0.16 |
| S1 D-test r = 3 (`_D3_v2`) | 0.06, 0.17, 0.25 | 0.02, 0.10, 0.29 |

The correlation of log σ_osc and log σ_nn across worlds is between 0.12 and 0.36. So the two parts vary enough, and
they are not the same variable.

## A2. Rules (fixed before the analysis)
**Data.** The S1 datasets `results/e3_dataset_v2.pkl` (baseline) and `results/e3_dataset_D3_v2.pkl` (D-test, r = 3),
corrected exit check. Driven and modular worlds pooled: 60 worlds per dataset. No new simulation.

**Outcome.** For each world, y = the mean over its 62 structures of log R = log(V_on/V_eq). V_eq is the life under the
reversible dynamics with the same stationary law (common random numbers). So y measures what the drive does to life at
fixed static statistics.

**Predictors.** For each world, σ, σ_osc and σ_nn from (B, D, S). To remove the time unit, divide each by the mean
relaxation rate λ̄ = tr(B)/N: x = σ/λ̄, x_osc = σ_osc/λ̄, x_nn = σ_nn/λ̄. The share s = σ_nn/σ has no unit.

**Statistics.** 2000 bootstrap resamples of worlds, seed 2026, 95 % percentile intervals. Spearman ρ for rank
correlations. Least squares for the regression, with z-scored log predictors.

| Rule | Question | Statistic | Verdict |
|---|---|---|---|
| R1 | Does a larger nonnormal share go with a shorter life? | ρ(s, y) | "shortens life" if CI high < 0, "lengthens life" if CI low > 0, else "no effect" |
| R2 | What does each part do at a fixed other part? | y = a + β_osc z(log x_osc) + β_nn z(log x_nn) | the labels of R1, for β_osc and for β_nn |
| R3 | Do the two parts act differently? | Δβ = β_nn − β_osc | "the parts differ" if the CI excludes 0, else "not separated" |
| R4 | Gate of the roadmap | R3 in the two datasets | "the decomposition adds information" if R3 is "the parts differ" in at least one dataset, else "gate triggers" |

Each rule runs on both datasets. Also reported (description only): ρ(x, y) for total dissipation, R1 and R2 per family,
and a scatter plot of y against s.

**Expectations written before the analysis.**
- R1 "shortens life" in both datasets. Reason: the paper links σ_nn to faster relaxation. In a set fixed by the
  stationary law, faster loss of memory means more exits per unit time.
- R2: β_nn "shortens life". β_osc "no effect", or a smaller effect than β_nn.
- R3 "the parts differ" in the D-test at least, where the nonnormal share is larger. R4 then "adds information".
- If R4 is "gate triggers", niche A becomes a short negative note, as the roadmap says.

**Known limits, before the analysis.**
- 60 worlds per dataset is a small sample for a regression with two predictors.
- σ_osc and σ_nn are properties of the whole world. y is a mean over structures, so this is a world-level test. The
  structure-level test is A4.
- The two families have different designs. Pooling them can hide a family effect. The per-family description shows it.

## A2. Results (added 2026-11-23, after the analysis)
Report: `results/e15_nonnormal_life.md`, `.json` and `.png`. Log: `results/e15_run.log`. The first run stopped at the
screen print, after it wrote the report files. Only the print changed, and the second run gave the same report (fixed
seed).

| Rule | Statistic | S1 baseline (60 worlds) | S1 D-test r = 3 (60 worlds) |
|---|---|---|---|
| R1 | ρ(s, y) | +0.71 [+0.56, +0.82], lengthens life | +0.78 [+0.62, +0.86], lengthens life |
| R2 | β_osc | −0.09 [−0.10, −0.07], shortens life | −0.07 [−0.09, −0.06], shortens life |
| R2 | β_nn | −0.00 [−0.01, +0.01], no effect | −0.01 [−0.02, +0.00], no effect |
| R3 | β_nn − β_osc | +0.09 [+0.06, +0.11], the parts differ | +0.07 [+0.04, +0.09], the parts differ |
| description | ρ(x, y), total dissipation | −0.95 [−0.97, −0.91] | −0.95 [−0.97, −0.91] |

R4: **the decomposition adds information.** The gate does not trigger.

The per-family values have the same signs in all four cases (ρ(s, y) from +0.63 to +0.75, β_osc from −0.06 to −0.10,
β_nn from −0.01 to 0.00).

### The expectations were wrong
I expected the nonnormal part to shorten life. It does not: β_nn shows no effect in both datasets. The **oscillatory**
part carries the whole effect. So a larger nonnormal share goes with a **longer** life (R1), because at a fixed total a
larger share means a smaller oscillatory part. Only R3 and R4 came out as expected.

### What A2 shows
1. **Total dissipation per relaxation time predicts what the drive costs in life.** Across worlds, ρ = −0.95 in both
   datasets. This is a world-level description, not a rule.
2. **The cost comes from the oscillatory part.** At a fixed nonnormal part, one standard deviation of log x_osc shortens
   the mean life by about 7–9 % (β_osc −0.07 to −0.09 in log units). At a fixed oscillatory part, the nonnormal part has
   no effect that we can see.
3. **The result is the same with D = I and with a random diagonal D.**

### A post-hoc reading (not tested)
Our viability set is fixed by the stationary law, and V_eq has the same stationary law. So only the dynamics can change
the life. Oscillations rotate the state among coordinates. A rotation brings values from outside a structure into it,
so the structure loses memory of its own state faster. Nonnormal transient amplification changes the variance in
Troude–Sornette, but here the set is calibrated to the variance. This reading is a guess. Step A3 can test it.

### Limits
- 60 worlds per dataset, world-level predictors, structure-level lives averaged in each world.
- Both datasets use the same B_s and G draws (the D-test draws D after them). So the two datasets are not independent
  samples of B.
- The predictors are divided by λ̄ = tr(B)/N. Another time unit can change the sizes of the β values.

### Next: A3 (rules to write before the runs)
Controlled worlds that change one part at a time:
- fix the eigenvalues of B and change only the nonnormality. A2 predicts **no change** in life.
- fix the nonnormality and change only the imaginary parts of the eigenvalues. A2 predicts a **shorter** life.

## A3. Rules (fixed 2026-11-23, before the runs)
**Question.** A2 is a correlation across random worlds. A3 changes one part of the dissipation at a time, in worlds
made for the test, and measures the life.

**Worlds** (`src/vlife/controlled.py`, our construction). N = 6, stationary covariance S = I. The drift is
B = Q (Bdiag(ω) + η U) Qᵀ with three 2 × 2 blocks [[r_k, ω r_k], [−ω r_k, r_k]], a block-upper-triangular coupling U
and a random rotation Q. D = (B + Bᵀ)/2.
- The eigenvalues are r_k (1 ± iω) for every η. So σ_osc = 2ω² Σ r_k does not change with η.
- η = 0 gives a normal B (σ_nn = 0). A larger η gives a larger σ_nn.
- Q mixes the coordinates, so a structure does not match one block.
- Rates r_k are log-uniform in [0.3, 3], as in S1. η_cap keeps the smallest eigenvalue of D at 0.25 · min r_k or above.

**Grid.** ω ∈ {0, 1, 2, 4} and η ∈ {0, 1/3, 2/3, 1} · η_cap. In S1 the median of max |Im λ / Re λ| per world is 3.9,
so ω = 4 is a typical S1 value. 20 worlds, seeds [2027, k].

**What we looked at before writing the rules.** Only the dissipation of the grid, not the lives. Medians over 20 worlds:

| ω | σ_osc | σ_nn at η = 0, 1/3, 2/3, 1 (· η_cap) |
|---|---|---|
| 0 | 0 | 0, 0.26, 1.30, 5.49 |
| 1 | 7.06 | 0, 0.53, 2.75, 12.8 |
| 2 | 28.2 | 0, 1.32, 6.97, 33.4 |
| 4 | 113 | 0, 4.47, 23.6, 114 |

So at η_cap the nonnormal part is as large as the oscillatory part, or larger. In S1 it was 5–17 % of the total. A
2-world smoke test (60 trajectories, t_max 40) checked that the code runs and that the sanity checks pass. Its results
were not read and its files were deleted.

**Simulation.** As in S1: 62 structures, p_out = 0.05, 600 trajectories, dt = 0.05, t_max = 200, Brownian-bridge exit
check. Life with the drive V_on, and life under B_eq = D, the reversible dynamics with the same stationary law. One seed
per world for every run of that world (common random numbers). y = mean over structures with at least 5 exits in both
runs of log(V_on/V_eq).

**Sanity checks (the run is not valid if one fails).** y = 0 exactly at ω = 0, η = 0 (then B = B_eq). σ_osc does not
change with η. σ_nn = 0 at η = 0.

**Rules.** 2000 bootstrap resamples of worlds, seed 2026, 95 % percentile intervals. Labels for Q1–Q3: "shortens life"
if CI high < 0, "lengthens life" if CI low > 0, "no effect within ±0.05" if the CI is inside [−0.05, +0.05], else
"inconclusive". 0.05 in log units is a 5 % change in life.

| Rule | Question | Contrast |
|---|---|---|
| Q1 | Do oscillations alone shorten life? | y(ω 4, η 0) − y(ω 0, η 0) |
| Q2 | Does nonnormality alone, with real eigenvalues, change life? | y(ω 0, η_cap) − y(ω 0, η 0) |
| Q3 | Does nonnormality change life at a fixed oscillation? | y(ω, η_cap) − y(ω, η 0), mean over ω = 1, 2, 4 |
| Q4 | Is the oscillatory effect larger? | \|Q1\| − \|Q3\|: "oscillation dominates" if CI low > 0, else "not separated" |

Also reported (description only): the mean y for each of the 16 grid points.

**Expectations written before the runs** (from A2):
- Q1 "shortens life".
- Q2 and Q3 "no effect within ±0.05".
- Q4 "oscillation dominates".

**What a different result means.**
- If Q2 or Q3 is "shortens life", the A2 null for σ_nn came from the small nonnormal share of S1 worlds. Then
  nonnormality also costs life when it is large, as Troude and Sornette suggest for escape.
- If Q1 is not "shortens life", the A2 link between σ_osc and life does not come from the oscillations as such. Then it
  can come from a feature of S1 worlds that goes with σ_osc.

**Known limits, before the runs.**
- S = I, so structures have no static correlations. This removes the information terms of S1, but A3 does not need them.
- Changing η also changes D, so the reference B_eq = D changes with η. log R always compares a world with its own
  reversible counterpart, as in A2.
- 20 worlds. The grid is the same for all worlds, so the contrasts are paired.
