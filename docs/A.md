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
