# Results of the full run (90 worlds, 5,580 structures, ~~11,250~~ 24,300 merge pairs)

**Note (2026-11-04, docs/code_review.md item 2):** the 11,250 merge pairs are not all eligible pairs. A filter in
`experiments/e4_merging.py` (`min(a) > min(b)`) kept 125 of the 270 eligible pairs per world, and the dropped pairs
depend on the variable index. The E4 numbers below come from this subset. A rerun without the filter is planned.
**Superseded (2026-11-04, phase C, docs/RERUN.md):** the rerun is done. E4 `_v2` uses all 270 pairs per world (24,300 pairs).

Settings: N = 6, τ = 1, p_out = 0.05, 600 trajectories per world, dt = 0.05, seed 2026. Raw outputs: `results/`.
Figures: `e3_phi_vs_viability.png`, `e4_merging.png`, `e2_gib_slowmodes.png`, `e1_estimators.png`.
**Superseded (2026-11-04, phase C, docs/RERUN.md):** the exit check at dt = 0.05 made log V too high by +0.2 to +1.2,
more for fast structures (docs/code_review.md item 1), and the equilibrium control used separate random numbers (item 5).
Phase C reran E3 and E4 on the same worlds with the Brownian-bridge correction, common random numbers and all merge pairs
(tag `_v2`: `results/e3_summary_v2.json`, `e4_merging_v2.json`, figures `e3_phi_vs_viability_v2.png`, `e4_merging_v2.png`).
The dt control (`results/c1_dt_control.md`) shows that the corrected V agrees with dt = 0.005 + bridge and with a
dt → 0 extrapolation; the old method was biased by +0.48 in log V on average. Below, old numbers are struck out and the
new value is written next to them.

**Reproduction (S0, 2026-10-21).** A clean rerun of `python experiments/run_all.py` (seed 2026, Python 3.14.3, numpy 2.5.4,
scipy 1.18.1, scikit-learn 1.9.1) gives every number on this page again. Results of the rerun:
- E0, E1 and E2 match to about 1e-14.
- In E3, the largest change is 0.003 (the `-IAX` score, not reported here). All other changes are 0.001 or less.
- E4 matches exactly.
- The E3 simulation took 1631 s on 4 cores.
- The shipped `e3_report.md` header said `n_traj=200, t_max=150`. That header was wrong: the report was rebuilt with `--reuse` and default arguments. The data came from `n_traj=600, t_max=200`, and the rerun confirms these settings. The shipped files are kept in `results_shipped/`.

**Note (2026-11-04, phase C):** this reproduction refers to the old code (exit check without bridge correction, separate
random numbers, filtered merge pairs). It is still true for that code. The numbers it reproduces are now superseded on
purpose where they are marked on this page.

**Process note (honesty).** Hypotheses H1–H4 (THEORY §5) were written before E3/E4 results were read. Two analysis
changes were made *after* seeing the first E3 output, and both are disclosed here: (a) a bug fix (the fitted score used
unstandardised features with standardised coefficients); (b) the addition of a size-stratified ranking, because Φ's apparent
success in the equilibrium family looked like a size effect. The sign interpretation of K_H below is also post-hoc.

## Validation (things that worked)
| Check | Result |
|---|---|
| MFPT simulator vs 1-D backward equation | agrees within 5% (with discrete-monitoring shift), `tests/` |
| Independent parts: hazards add | within 8%, `tests/` |
| Gaussian IB analytic solution vs direct optimisation | equal to 1e-3, `tests/` |
| GIB vs TICA subspaces, reversible worlds | gap ≈ 1e-13 rad (identical, as proved in THEORY §6) |
| GIB vs TICA subspaces, driven worlds | ~~gap ≈ 0.5–0.9 rad (E2)~~ superseded (fix #3): mean gap 0.62–0.72 rad for k = 1–3, range 0.12–1.41 rad over worlds (E2 rerun, end of this page) |
| KSG estimator vs exact | bias ≲ 0.01 nats for n ≥ 250 |
| Legacy binned estimator vs exact | bias +0.16 nats (n = 250), +0.03 (n = 1000) (E1) |
| Legacy script: planted block recovered with NO environmental drive | yes, 5/5 seeds (E0) |

## E3 — does Φ predict viability?
Mean within-world Spearman ρ between score and log MFPT (95% cluster-bootstrap CI), all 90 worlds:

| score | all structures | among equal-size structures |
|---|---|---|
| **Φ_orig (β=1, λ=0.25)** | **~~−0.08 [−0.20, +0.03]~~ −0.01 [−0.12, +0.10]** (phase C, `_v2`) | ~~+0.10 [+0.03, +0.18]~~ +0.08 [+0.00, +0.16] |
| C only | ~~+0.33 [+0.24, +0.42]~~ +0.26 [+0.17, +0.34] | **~~+0.55 [+0.49, +0.60]~~ +0.55 [+0.49, +0.61]** |
| P only | ~~+0.09 [+0.05, +0.13]~~ +0.09 [+0.05, +0.13] | ~~+0.14 [+0.09, +0.18]~~ +0.13 [+0.09, +0.18] |
| −K_H | ~~−0.26 [−0.35, −0.16]~~ −0.19 [−0.29, −0.10] | ~~−0.70 [−0.74, −0.65]~~ −0.74 [−0.78, −0.70] |
| −leak (closure) | ~~+0.12 [+0.07, +0.17]~~ +0.10 [+0.05, +0.15] | ~~+0.13 [+0.08, +0.18]~~ +0.11 [+0.06, +0.16] |
| fitted linear (P, C, K_H, IAX), cross-fitted | ~~+0.36 [+0.28, +0.44]~~ +0.33 [+0.25, +0.41] | ~~+0.49 [+0.43, +0.56]~~ +0.48 [+0.42, +0.54] |

New values in this table and below: phase C, `_v2` (`results/e3_summary_v2.json`).

Per family, Φ_orig overall: equilibrium **~~+0.54~~ +0.56**, driven **~~−0.34~~ −0.23**, modular-driven **~~−0.45~~ −0.37**.
Among equal-size structures: ~~+0.38, −0.07, 0.00~~ +0.37, −0.12, 0.00. In the equilibrium family *size alone* (smaller
lives longer) gives ~~+0.47~~ +0.50, so Φ's success there is largely a size effect.

Standardised regression coefficients (Δ log V per +1 SD, within-world):

| family | P | C | K_H | IAX |
|---|---|---|---|---|
| all | ~~+0.024~~ +0.031 | ~~+0.095~~ +0.123 | ~~−0.072~~ −0.111 | 0.000 (CI ∋ 0), same in `_v2` |
| equilibrium | ~~+0.058~~ +0.066 | ~~+0.193~~ +0.242 | ~~−0.236~~ −0.300 | ~~−0.041~~ −0.044 |
| driven | ~~+0.010~~ +0.010 (CI ∋ 0: [−0.0004, +0.021]) | ~~+0.075~~ +0.093 | ~~−0.030 (CI ∋ 0)~~ −0.058 [−0.099, −0.025] | ~~+0.011~~ +0.017 |
| modular driven | ~~+0.037~~ +0.049 | ~~+0.113~~ +0.144 | ~~−0.040~~ −0.075 | ~~0.000~~ −0.002 (CI ∋ 0) |

The coefficients grow by 20–100 %: the old exit check compressed the differences between fast and slow structures.

Flux ratio log(V_driven / V_eq): equilibrium ~~+0.02 ± 0.005~~ 0.000 exactly (control; about 2%, plausibly Monte-Carlo noise since all
structures in a world share trajectories — not investigated further); driven ~~−0.21 ± 0.015~~ −0.190 ± 0.013; modular
~~−0.24 ± 0.018~~ −0.245 ± 0.019.
**Superseded (2026-11-04, phase C, docs/RERUN.md):** the "plausibly Monte-Carlo noise" guess is confirmed. With common
random numbers for the driven run and its equilibrium counterpart, the equilibrium log R is exactly 0.000 (rule V0 "exact").
Price selection term Cov(w/w̄, Φ_orig) is positive in 100% of equilibrium worlds, ~~27%~~ 47% of driven, ~~20%~~ 27% of modular.

### Verdicts on pre-registered hypotheses
- **H1 (Φ_orig ranks structures by viability): not supported.** Pooled ρ = ~~−0.08~~ −0.01 [−0.12, +0.10] (phase C, `_v2`), CI includes 0. Works only in the equilibrium family and there is largely a size effect. Verdict unchanged in phase C.
- **H2 (signs +P, +C, −K, stable across families): partially supported.** Signs of P and C are positive in every family; ~~K_H is negative in three of four (CI includes 0 in driven)~~ K_H is negative in all four with every CI excluding 0, and P in driven has CI [−0.0004, +0.021] (phase C, `_v2`). Magnitudes are **not** universal (K_H coefficient differs ~~about 8×~~ about 5× (−0.300 against −0.058) between equilibrium and driven; IAX changes sign). P's effect is small (≈ ~~0.01–0.06~~ 0.01–0.07 SD per SD).
  **Superseded (2026-11-04, phase C, docs/RERUN.md):** same verdict "partial", but for a different reason (the P coefficient in driven, not K_H).
- **H3 (control and flux ratio): control passes (~~≈ +2%~~ exactly 0 with common random numbers); the "explained by features" half was not tested.** Driven dynamics shorten persistence of marginal structures by about 20% at fixed stationary law (V_driven/V_eq ≈ 0.8). This is *consistent in direction* with the accelerated-mixing results for non-reversible diffusions (Hwang et al.), but we did not test that link.
  **Superseded (2026-11-04, phase C, docs/RERUN.md):** about 17 % (driven) and 22 % (modular), V_driven/V_eq ≈ 0.83 and 0.78 (log R −0.190 and −0.245). The direction stands.
- **H4 (ΔΦ predicts survival synergy beyond static I(A;B)): not supported.** See below. Verdict unchanged in phase C (ρ(ΔΦ) −0.17 against ρ(I(A;B)) +0.36, all 24,300 pairs).

## E4 — merging
S = V_union (1/V_A + 1/V_B) exceeds 1 in ~~88%~~ 77% of pairs (phase C, `_v2`, all 24,300 pairs). Within-world Spearman ρ with log S:

| predictor | all | equilibrium | driven | modular |
|---|---|---|---|---|
| ΔΦ_orig | ~~−0.20 [−0.25, −0.13]~~ −0.17 [−0.23, −0.11] | ~~−0.56~~ −0.49 | ~~−0.07~~ −0.06 (CI ∋ 0) | ~~+0.04~~ +0.03 (CI ∋ 0) |
| static I(A;B) (= λ·I term of ΔΦ) | **~~+0.41 [+0.37, +0.45]~~ +0.36 [+0.32, +0.40]** | ~~+0.57~~ +0.52 | ~~+0.33~~ +0.30 | ~~+0.33~~ +0.27 |
| ΔP | ~~−0.45~~ −0.42 | ~~−0.56~~ −0.50 | ~~−0.42~~ −0.39 | ~~−0.37~~ −0.36 |
| ΔC | ~~+0.05~~ +0.07 (CI ∋ 0) | ~~−0.57~~ −0.49 | ~~+0.36~~ +0.35 | ~~+0.36~~ +0.35 |

New values: phase C, `_v2` (`results/e4_merging_v2.json`), with the corrected exit check and all merge pairs.

Sign agreement between ΔΦ > 0 and S > 1 is ~~0.50 (chance)~~ 0.56 (phase C). Static dependence alone predicts synergy; the Φ super-additivity
criterion does not improve on it, and its P-term points the wrong way (merging shrinks the environment, lowering P).

## Update after S1 (2026-10-21): read docs/S1.md
The S1 robustness sweep changes the H1 verdict. H1 is supported at τ = 0.5 and when D is not the identity (D-test r = 3).
So the H1 result below holds for this baseline only. It depends on τ, on the fixed λ = 0.25 and on D = I.
C predicts viability in all 9 settings, and H4 fails in all 9 settings. Details and the corrected claims are in `docs/S1.md`.
**Note (2026-11-04, phase C, docs/RERUN.md):** baseline, τ 0.5 and τ 2 were redone with the corrected exit check. H1 is
still supported at τ 0.5 (~~+0.15~~ +0.23 [+0.12, +0.33]) and not at τ 1 or τ 2, C still predicts viability and H4 still
fails in these 3 settings. The other 6 settings (p_out 0.01, p_out 0.2, N 5, N 7, D-test r 2, r 3) still use the old exit check.

**Update after S1b (2026-10-21): read docs/S1b_unitfree.md.** Replace K_H by the multi-information TC, which does not depend
on units. Then P + C − 0.25·TC predicts viability in all 9 S1 settings (ρ ~~+0.33 to +0.53~~ +0.27 to +0.53, all CIs exclude 0), and the TC
coefficient is negative everywhere. The K_H term caused the negative H1 result.
**Note (2026-11-04, phase C):** the new range uses the corrected values for baseline (+0.34), τ 0.5 (+0.27) and τ 2 (+0.47);
the other 6 settings still use the old exit check.

## What this does and does not show
- In **passive linear-Gaussian worlds**, with **MFPT out of a Mahalanobis ball** as viability, the proposed Φ is **not** a good predictor of viability, and the merge criterion fails.
- What does track viability is **persistence (C)**, which is partly expected by construction (slow structures live long; D = I ties variance to slowness, which also makes K_H a proxy for timescale and explains its mixed marginal/conditional sign).
- Predictive information P has a small positive partial effect. This is what one should expect *if information only pays when it is used*: nothing in these worlds acts on P.
- This is **not** a refutation of T3 in general. It refutes this functional in this ensemble. The untested regimes (action loops, hidden-state environments, nonlinear metastability, heredity) are exactly those where the theory was supposed to bite (ROADMAP).
- The result is a concrete next step: the discriminating experiment is Track A/N, where information can be *used* and where equilibrium "rocks" exist.

## E2 rerun after fix #3 (rules fixed 2026-11-04, before the run)
**Why.** E2 compared GIB and TICA subspaces using the real part of complex TICA eigenvectors, and could split a conjugate
pair (docs/code_review.md, item 3). The rerun uses `gib.tica_subspace` (real basis, pairs kept together). Same 20 worlds
per family (seeds 100–119), τ = 1. The old gap is computed again in the same run, for comparison. Output:
`results/e2_gib_slowmodes_realbasis.json` and `.png`. The old `results/e2_gib_slowmodes.json` stays.

| Rule | Question | Verdict |
|---|---|---|
| E2a | Control: do GIB and TICA still coincide in reversible worlds? | "passes" if the largest new gap over equilibrium worlds is < 1e-6 for k = 1, 2, 3 |
| E2b | Do GIB and TICA still differ in every driven world? | "yes" if the smallest new gap over driven worlds is > 1e-3 for k = 1, 2, 3 |
| E2c | Was the old driven gap an artefact of the recipe? | "old values superseded" if the mean new gap differs from the mean old gap by more than 0.05 rad for some k, else "old values stand" |

Expectations: E2a "passes", E2b "yes". E2c "old values superseded", because the old recipe did not give an invariant
subspace in any of the 20 driven worlds (median residual 0.85, measured with the tests of fix #3).

### E2 rerun: results (added 2026-11-04, after the run)
Output: `results/e2_gib_slowmodes_realbasis.json`, `.png`, `.log`. Run time a few seconds.

| k | equilibrium, largest new gap | driven, mean old gap | driven, mean new gap [min, max] | driven worlds where a conjugate pair was kept (m = k + 1) |
|---|---|---|---|---|
| 1 | 1.9e-13 | 0.911 | 0.623 [0.122, 1.208] | 90 % |
| 2 | 2.1e-12 | 0.544 | 0.666 [0.122, 1.208] | 10 % |
| 3 | 3.0e-13 | 0.895 | 0.718 [0.120, 1.409] | 85 % |

| Rule | Verdict |
|---|---|
| E2a (control) | passes |
| E2b (GIB and TICA differ in every driven world) | yes (smallest gap 0.12 rad) |
| E2c (old values) | old values superseded (changes of −0.29, +0.12, −0.18 rad) |

What this changes: the qualitative E2 result stands. GIB and TICA coincide in reversible worlds and differ in every
driven world. The size of the gap was partly an artefact: with the old recipe the mean gap went down and up with k
(0.91, 0.54, 0.89); with a real invariant basis it grows slowly with k (0.62, 0.67, 0.72). When a pair is kept, the
TICA span has dimension k + 1 and is compared with the first k + 1 GIB modes.

## Update after phase C (2026-11-04)
Rules and full old/new tables: `docs/RERUN.md` (sections C1, C2, C2b, C3 and their results). The exit check now uses the
Brownian-bridge correction, the equilibrium control uses common random numbers, and E4 uses all merge pairs (tag `_v2`).
- **Stands:** H1 not supported at the baseline (ρ(Φ_orig) −0.01 [−0.12, +0.10]), C predicts viability (+0.55 among
  structures of equal size, unchanged), H4 not supported with all 24,300 pairs (ρ(ΔΦ) −0.17 against ρ(I(A;B)) +0.36),
  driven dynamics shorten life (log R −0.190 driven, −0.245 modular). Same E3 data size: 90 worlds, 5,580 structures.
- **Control:** the equilibrium log R is exactly 0.000 with common random numbers (was +0.019, "plausibly Monte-Carlo noise").
- **Sizes changed:** the regression coefficients are 20–100 % larger, ρ(C only) over all structures fell from +0.33 to
  +0.26, ρ(−K_H, equal size) is −0.74 (was −0.70), and the share of merge pairs with S > 1 is 0.77 (was 0.88).
- **H2:** still "partial", but now because of P in the driven family (CI [−0.0004, +0.021]), not K_H.
- **Not rerun:** the S1 settings p_out 0.01, p_out 0.2, N 5, N 7 and the D-test r 2, r 3 still use the old exit check.
  Claims that need all 9 S1 settings are confirmed only in the 3 corrected ones (baseline, τ 0.5, τ 2).
