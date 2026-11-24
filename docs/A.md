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

## A3. Results (added 2026-11-23, after the run)
Report: `results/e16_controlled.md` and `.json`. Log: `results/e16_run.log` (2916 s, 20 worlds). The data file
`results/e16_controlled.pkl` is not in git (`*.pkl`). All sanity checks pass: y = 0 exactly at ω = 0, η = 0, σ_osc does
not change with η, σ_nn = 0 at η = 0, and every grid point keeps all 62 structures.

| Rule | Contrast | Value [95 % CI] | Verdict | Expected |
|---|---|---|---|---|
| Q1 | y(ω 4, η 0) − y(ω 0, η 0) | −0.308 [−0.322, −0.295] | shortens life | yes |
| Q2 | y(ω 0, η_cap) − y(ω 0, η 0) | −0.053 [−0.061, −0.046] | shortens life | **no** ("no effect within ±0.05") |
| Q3 | y(ω, η_cap) − y(ω, η 0), mean over ω 1, 2, 4 | −0.055 [−0.065, −0.044] | shortens life | **no** ("no effect within ±0.05") |
| Q4 | \|Q1\| − \|Q3\| | +0.253 [+0.233, +0.275] | oscillation dominates | yes |

Mean y over the 20 worlds (description):

| ω | η = 0 | η = 1/3 η_cap | η = 2/3 η_cap | η = η_cap |
|---|---|---|---|---|
| 0 | +0.000 | −0.004 | −0.019 | −0.053 |
| 1 | −0.078 | −0.084 | −0.101 | −0.132 |
| 2 | −0.183 | −0.189 | −0.203 | −0.236 |
| 4 | −0.308 | −0.315 | −0.330 | −0.365 |

### The expectations were partly wrong
Q1 and Q4 came out as expected. Q2 and Q3 did not: nonnormality **also** shortens life, at a fixed spectrum and at a
fixed oscillatory part. The effect is small. At η_cap it is about 5 % of the life, and the CIs exclude zero.

### What A3 shows
1. **Oscillations alone shorten life a lot.** At ω = 4, a typical S1 value, the mean life falls by about 27 %
   (y = −0.31), with the stationary law fixed.
2. **Nonnormality alone shortens life a little.** At η_cap the mean life falls by about 5 %, even with real eigenvalues.
3. **The two effects add up.** At every ω the step from η = 0 to η_cap is between −0.053 and −0.057. So the interaction
   is below 0.01 in y (description, not a rule).
4. **Per unit of dissipation, oscillations cost more** (description). At ω = 4 the two parts are about equal at η_cap
   (σ_osc 113, σ_nn 114, medians), but the oscillatory part costs −0.31 and the nonnormal part −0.06.
5. **This explains the null of A2.** In S1 worlds the nonnormal share is 5–17 % (medians). An effect this small at that
   share is below what 60 worlds can detect.

### Combined reading of A2 and A3
At a fixed stationary law, the life cost of a drive comes mainly from the oscillatory part of its dissipation. The
nonnormal part also costs life, but much less per unit of dissipation. So total dissipation is a good predictor of the
cost (A2, ρ = −0.95) because in typical random worlds most of it is oscillatory. The post-hoc reading of A2 (rotation
mixes outside values into a structure) fits Q1, but A3 does not test it directly.

### Limits
- One construction (S = I, block Schur form, one random rotation per world). Other constructions can give other sizes.
- The size of "per unit of dissipation" depends on the grid. Point 4 is a description, not a rule.
- 20 worlds. The CIs are narrow because the grid is paired within worlds.
- Structures here have no static correlations (S = I).

### Next
A4 (structure level) is still open. Before A4, the result of A2 and A3 is enough for a short note to Nagayama,
Kolchinsky and Ito, after a check by the author.

## A4. Rules (fixed 2026-11-23, before the analysis)
**Question.** A2 and A3 are about whole worlds. A4 asks the same question for single structures in the same world:
do the structures whose own dynamics oscillate more lose more life to the drive?

**Data.** The S1 datasets of A2 (`_v2` and `_D3_v2`), driven and modular worlds, 60 worlds each. No new simulation.

**Local parts (our choice, a "novel" flag).** For a structure A, take the local block (B_AA, D_AA) and its own stationary
covariance. Then σ_osc,A and σ_nn,A come from `oscillatory_nonnormal_ep(B_AA, D_AA)`. Divide by λ̄_A = tr(B_AA)/|A|:
x_osc,A and x_nn,A. The local block ignores the coupling of A to the rest of the world. This is a real limit, see the
expectations.

**Outcome.** log R_A = log(V_on/V_eq) of structure A, for structures with at least 5 exits in both runs.

**Strata.** World × size, for sizes 2 to 5 (size 1 has no dissipation in its own block). Ranks are taken inside each
stratum, so world and size effects do not enter.

**What we looked at before writing the rules.** Only the local predictors. All 6720 local blocks are stable. The median
nonnormal share is 5–11 % (baseline) and 11–28 % (D-test). For size 2, x_osc,A is zero in 19 % (baseline) and 32 %
(D-test) of the structures (real eigenvalues). Inside strata, the mean ρ(x_osc,A, x_nn,A) is 0.15 and 0.05.

**Statistics.** 2000 cluster-bootstrap resamples of worlds, seed 2026, 95 % percentile intervals.

| Rule | Question | Statistic | Verdict |
|---|---|---|---|
| P1 | Do structures with more local oscillation lose more life? | mean over strata of ρ(x_osc,A, log R_A) | "shortens life" if CI high < 0, "lengthens life" if CI low > 0, else "no effect" |
| P2 | Same for the local nonnormal part | mean over strata of ρ(x_nn,A, log R_A) | same labels |
| P3 | Each part at a fixed other part | least squares on ranks standardized inside strata: rank(log R) = β_osc rank(x_osc) + β_nn rank(x_nn) | the labels of P1, for β_osc and for β_nn |
| P4 | Do the two parts act differently? | Δβ = β_nn − β_osc | "the parts differ" if the CI excludes 0, else "not separated" |

Also reported (description only): P1 and P2 for each size, and the same ρ for the S2c measure σ_A (the part of the
total entropy production along the coordinates of A), for comparison.

**Expectations written before the analysis.**
- P1 "shortens life", with a smaller ρ than the world-level effect.
- P2 "no effect", or "shortens life" with a smaller size than P1.
- P4 "the parts differ".
- Alternative, also written now: the post-hoc reading of A2 says that the cost comes from mixing with coordinates
  **outside** A. The local block cannot see that mixing. If P1 is "no effect", the cost is a property of the coupling
  of A to the world, not of the own dynamics of A. Then the next step is a coupling measure, not A4 again.

## A4. Results (added 2026-11-24, after the analysis)
Report: `results/e17_structure_level.md` and `.json`. Log: `results/e17_run.log`.

| Rule | Statistic | S1 baseline | S1 D-test r = 3 | Expected |
|---|---|---|---|---|
| P1 | mean ρ(x_osc,A, log R_A) | +0.21 [+0.15, +0.26], lengthens life | +0.17 [+0.11, +0.23], lengthens life | **no** ("shortens life") |
| P2 | mean ρ(x_nn,A, log R_A) | +0.04 [−0.01, +0.10], no effect | +0.02 [−0.03, +0.08], no effect | yes |
| P3 | β_osc | +0.19 [+0.14, +0.24], lengthens life | +0.16 [+0.10, +0.22], lengthens life | **no** |
| P3 | β_nn | +0.01 [−0.04, +0.06], no effect | +0.01 [−0.05, +0.06], no effect | yes |
| P4 | β_nn − β_osc | −0.18 [−0.25, −0.11], the parts differ | −0.15 [−0.24, −0.06], the parts differ | yes |
| description | mean ρ(σ_A/λ̄_A, log R_A), S2c measure | −0.00 [−0.05, +0.05] | −0.10 [−0.16, −0.04] | |

Per size (description): P1 grows with size, from about +0.04 at size 2 to +0.21–0.30 at size 5. P2 stays between
−0.02 and +0.10.

### The main expectation was wrong, in sign
Across worlds, more oscillation means a larger life cost (A2, A3). Across structures **inside** a world, the opposite
holds: structures whose **own** block oscillates more lose **less** life to the drive. The local nonnormal part has no
effect, as expected.

### A post-hoc reading (not tested)
This fits the alternative written before the analysis, and makes it sharper. A rotation that stays inside A does not
change the distance of A from the edge of its set. With S = I, a rotation inside a block keeps the norm of that block
exactly. A rotation that crosses the boundary of A moves values from outside into A. So:
- the cost of a drive comes from oscillations that **cross** the boundary of a structure;
- a structure that **contains** its oscillations is protected.

A structure with a strong own oscillation contains more of the rotation of the world. Larger structures contain more,
and P1 grows with size. This reading also explains why total dissipation predicts the cost at world level: more
rotation means more rotation across boundaries.

### Limits
- The local block ignores the coupling of A to the world. P1 shows that this matters, but A4 does not measure the
  coupling.
- Ranks inside strata: A4 says nothing about the size of the effect in life units.

## A5. Rules (fixed 2026-11-24, before the runs)
**Question.** A4 gave a post-hoc reading: the life cost of a drive comes from oscillations that **cross** the boundary
of a structure, and a structure that **contains** its oscillations is protected. A5 tests this reading in two parts.
Part 1 uses worlds where the answer follows from the algebra. Part 2 uses a new measure on the S1 data.

### Part 1: controlled worlds without rotation (`experiments/e18_unrotated_worlds.py`)
**Worlds.** `vlife.controlled.draw` with seeds [2028, k], k = 0 to 19 (new seeds, not the A3 worlds). We set Q = I and
η = 0. Then B is block diagonal: block k is r_k [[1, ω], [−ω, 1]] on coordinates 2k and 2k+1, S = I and D = diag(r).
Grid: ω ∈ {0, 1, 2, 4}. At ω = 0, B = D = B_eq, so the run at ω = 0 is the reversible run for every ω.

**Structures.** All 62 structures of 6 coordinates. "Whole": a union of whole blocks (6 structures, sizes 2 and 4).
"Cut": all others (56 structures).

**Prediction from the algebra, before any run.** For a whole structure, the rotation inside each block is
antisymmetric, so d|x_k|² does not contain ω. The simulator keeps this exactly: the exact propagator is a rotation times
exp(−r_k dt), the noise of each block is isotropic, and the bridge correction uses only the block norms. So the exit
time of a whole structure has the same distribution at every ω, and log R = 0 in distribution. For a cut structure,
the rotation moves values from the partner coordinate outside A into A.

**Simulation.** As in A3: 600 trajectories, dt 0.05, t_max 200, p_out 0.05, bridge correction, common random numbers
(seed [2028, k, 1] for every run of world k). Structures with at least 5 exits in both runs.

**Sanity checks (the run is not valid if one fails).** log R = 0 exactly at ω = 0. σ_nn = 0 at every ω.

**Statistics.** Per world: W_ω and C_ω, the mean log R over the whole and over the cut structures. 2000 bootstrap
resamples of worlds, seed 2026, 95 % percentile intervals. Labels as in A3: "shortens life" if the CI is below 0,
"lengthens life" if above 0, "no effect within ±0.05" if the CI is inside [−0.05, +0.05], else "inconclusive".

| Rule | Question | Statistic |
|---|---|---|
| W1 | Do whole structures lose no life? | W = mean of W_1, W_2, W_4. Also each W_ω |
| C1 | Do cut structures lose life? | C_1, C_2 and C_4 |
| C2 | Is the loss larger with faster oscillation? | C_4 − C_1 |
| C3 | Does the new measure rank the cut structures? | at ω = 4, mean over world × size strata of ρ(x_cross,A, log R_A) |

x_cross,A is defined in part 2. In these worlds it is 0 for a whole structure and 2ω² Σ r_k / λ̄_A over the cut blocks.

**Sensitivity (description only).** Worlds 0 to 4 again at ω = 4 with dt 0.01. Known limit: at r = 3 and ω = 4, the
rotation turns 0.6 rad per step. The exit check on the time grid can miss crossings of a cut structure, and this makes
the loss look smaller. Whole structures are not affected (see the argument above).

### Part 2: a measure of oscillation across the boundary, on the S1 data (`experiments/e19_cross_oscillation_s1.py`)
**Measure (our choice, a "novel" flag).** `gaussian.cross_oscillation(B, S, A)`. For each complex pair of eigenvalues
λ_m of B, take its weight in σ_osc, 2 Im(λ_m)²/Re(λ_m). Take the right eigenvector v_m and scale each coordinate by
its stationary standard deviation. w_m is the share of the squared modulus of the scaled vector on A. Then
σ_cross,A = Σ_m 2 Im(λ_m)²/Re(λ_m) · 4 w_m (1 − w_m), and x_cross,A = σ_cross,A / λ̄_A, λ̄_A = tr(B_AA)/|A| as in A4.
A mode inside A or outside A adds 0. A mode split in half adds its full weight. Tests:
`tests/test_cross_oscillation.py`.

**Data, outcome, strata.** As in A4: the S1 datasets `_v2` and `_D3_v2`, driven and modular worlds, sizes 2 to 5,
log R_A for structures with at least 5 exits in both runs, ranks inside world × size strata.

| Rule | Question | Statistic | Verdict |
|---|---|---|---|
| T1 | Do structures with more oscillation across their boundary lose more life? | mean over strata of ρ(x_cross,A, log R_A) | labels of A4 |
| T2 | Does this hold at a fixed local oscillation? | ranks standardized in strata: rank(log R) = β_cross rank(x_cross) + β_osc rank(x_osc,A) | labels of A4, for β_cross |

Also reported (description only): β_osc in the same model, and T1 for each size.

### What we looked at before writing the rules
- Part 2, predictors only, no outcome: x_cross,A is never 0 in S1 (3360 structures per dataset). The median ratio
  σ_cross,A / σ_osc of the world is 0.87 (baseline) and 0.83 (D-test), so the modes of S1 worlds spread over many
  coordinates. Inside strata, the mean ρ(x_cross,A, x_osc,A) is −0.12 and −0.11.
- Part 1, a code check: two dry runs with a throwaway seed (99), 1 to 2 worlds and 40 to 60 trajectories. We saw their
  numbers. W was within ±0.06 of 0 and C was negative at every ω. These runs are not data for A5, and we deleted
  their output.

### Expectations written before the runs
- W1 "no effect within ±0.05", for W and for each W_ω. A different result means a bug, because the argument above
  covers the simulator exactly.
- C1 "shortens life" at ω = 1, 2 and 4. C2 "shortens life". C3 "shortens life".
- T1 and T2 "shortens life" in both datasets.
- Alternative, also written now: the S1 modes spread over many coordinates, so x_cross,A can be close to the world σ_osc
  for most structures. If part 1 passes and T1 is "no effect", the reading holds for block worlds, but this measure
  does not carry it to S1 worlds.

## A5. Results (added 2026-11-24, after the runs)
Reports: `results/e18_unrotated.md` and `.json`, `results/e19_cross_oscillation_s1.md` and `.json`. Logs:
`results/e18_run.log`, `results/e19_run.log`. The runs used commit 9106337 (the rules).

### Part 1: controlled worlds without rotation
All sanity checks pass: log R = 0 exactly at ω = 0, σ_nn = 0, and all 62 structures have at least 5 exits in every run.

| Rule | Statistic | Value [95 % CI] | Verdict | Expected |
|---|---|---|---|---|
| W1 | W, whole structures, mean over ω 1, 2, 4 | −0.003 [−0.013, +0.007] | no effect within ±0.05 | yes |
| W1 | W_1 / W_2 / W_4 | −0.002 / −0.001 / −0.006, all CIs inside [−0.020, +0.009] | no effect within ±0.05 | yes |
| C1 | C_1, cut structures | −0.082 [−0.090, −0.074] | shortens life | yes |
| C1 | C_2 | −0.183 [−0.194, −0.172] | shortens life | yes |
| C1 | C_4 | −0.287 [−0.302, −0.273] | shortens life | yes |
| C2 | C_4 − C_1 | −0.205 [−0.219, −0.191] | shortens life | yes |
| C3 | mean ρ(x_cross,A, log R_A), ω 4 | −0.54 [−0.62, −0.47] | shortens life | yes |

Sensitivity (description), worlds 0 to 4 at ω = 4: with dt 0.01, W_4 = +0.022 and C_4 = −0.291. With dt 0.05 on the
same worlds, W_4 = −0.009 and C_4 = −0.276. The time step changes the loss of cut structures by about 5 %.

### Part 2: oscillation across the boundary, S1 data

| Rule | Statistic | S1 baseline | S1 D-test r = 3 | Expected |
|---|---|---|---|---|
| T1 | mean ρ(x_cross,A, log R_A) | −0.31 [−0.37, −0.26], shortens life | −0.39 [−0.44, −0.33], shortens life | yes |
| T2 | β_cross, at a fixed x_osc,A | −0.30 [−0.35, −0.25], shortens life | −0.38 [−0.43, −0.32], shortens life | yes |
| description | β_osc,A, at a fixed x_cross,A | +0.18 [+0.13, +0.23], lengthens life | +0.14 [+0.09, +0.19], lengthens life | |

Per size (description): T1 is between −0.24 and −0.41 (baseline) and between −0.34 and −0.49 (D-test) at every size.

For comparison (from A4): the local oscillation gave ρ = +0.21 and +0.17, and the S2c measure σ_A gave −0.00 and
−0.10. The new measure is the strongest structure-level predictor of the life cost in this project so far.

**Post-hoc check (not a rule, point values only).** Does the division by λ̄_A carry T1? Without the division,
ρ(σ_cross,A, log R_A) is −0.31 and −0.35. The division alone, ρ(1/λ̄_A, log R_A), gives −0.08 and −0.17. So the
effect comes from σ_cross,A. Script: `experiments/e19b_posthoc_normalisation.py`.

### What A5 shows
All 6 rules of A5 give the expected verdict. So the post-hoc reading of A4 passes a test, in two kinds of worlds:
- In worlds where the oscillating pairs are known, a structure that contains whole pairs loses no life to the drive, at
  every speed of oscillation. A structure that cuts a pair loses life, more at a faster oscillation.
- In the S1 worlds, the share of oscillation that crosses the boundary of a structure predicts its life cost. At a
  fixed crossing share, more local oscillation still means a longer life, as in A4.

So the oscillatory part σ_osc of Nagayama, Kolchinsky and Ito costs life only through the modes that a structure cuts.
The world-level effect of A2 and A3 follows: more rotation in a world means more rotation across boundaries.

### Limits
- Part 1 uses one construction (2 × 2 blocks, S = I, η = 0) and 20 worlds.
- The measure has two choices of ours: the split factor 4 w (1 − w) and the scaling by diag S. We did not test others.
- The S1 data is the same as in A2 and A4. The measure was written after A4 showed the effect, so part 2 is a test of a
  measure built for this reading, on old data. Part 1 is the new evidence.
- The eigenvectors of a nonnormal B are not orthogonal. The measure uses right eigenvectors only.
