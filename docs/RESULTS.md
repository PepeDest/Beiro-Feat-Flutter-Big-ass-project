# Results of the full run (90 worlds, 5,580 structures, 11,250 merge pairs)

**Note (2026-11-04, docs/code_review.md item 2):** the 11,250 merge pairs are not all eligible pairs. A filter in
`experiments/e4_merging.py` (`min(a) > min(b)`) kept 125 of the 270 eligible pairs per world, and the dropped pairs
depend on the variable index. The E4 numbers below come from this subset. A rerun without the filter is planned.

Settings: N = 6, τ = 1, p_out = 0.05, 600 trajectories per world, dt = 0.05, seed 2026. Raw outputs: `results/`.
Figures: `e3_phi_vs_viability.png`, `e4_merging.png`, `e2_gib_slowmodes.png`, `e1_estimators.png`.

**Reproduction (S0, 2026-10-21).** A clean rerun of `python experiments/run_all.py` (seed 2026, Python 3.14.3, numpy 2.5.4,
scipy 1.18.1, scikit-learn 1.9.1) gives every number on this page again. Results of the rerun:
- E0, E1 and E2 match to about 1e-14.
- In E3, the largest change is 0.003 (the `-IAX` score, not reported here). All other changes are 0.001 or less.
- E4 matches exactly.
- The E3 simulation took 1631 s on 4 cores.
- The shipped `e3_report.md` header said `n_traj=200, t_max=150`. That header was wrong: the report was rebuilt with `--reuse` and default arguments. The data came from `n_traj=600, t_max=200`, and the rerun confirms these settings. The shipped files are kept in `results_shipped/`.

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
| GIB vs TICA subspaces, driven worlds | gap ≈ 0.5–0.9 rad (E2) |
| KSG estimator vs exact | bias ≲ 0.01 nats for n ≥ 250 |
| Legacy binned estimator vs exact | bias +0.16 nats (n = 250), +0.03 (n = 1000) (E1) |
| Legacy script: planted block recovered with NO environmental drive | yes, 5/5 seeds (E0) |

## E3 — does Φ predict viability?
Mean within-world Spearman ρ between score and log MFPT (95% cluster-bootstrap CI), all 90 worlds:

| score | all structures | among equal-size structures |
|---|---|---|
| **Φ_orig (β=1, λ=0.25)** | **−0.08 [−0.20, +0.03]** | +0.10 [+0.03, +0.18] |
| C only | +0.33 [+0.24, +0.42] | **+0.55 [+0.49, +0.60]** |
| P only | +0.09 [+0.05, +0.13] | +0.14 [+0.09, +0.18] |
| −K_H | −0.26 [−0.35, −0.16] | −0.70 [−0.74, −0.65] |
| −leak (closure) | +0.12 [+0.07, +0.17] | +0.13 [+0.08, +0.18] |
| fitted linear (P, C, K_H, IAX), cross-fitted | +0.36 [+0.28, +0.44] | +0.49 [+0.43, +0.56] |

Per family, Φ_orig overall: equilibrium **+0.54**, driven **−0.34**, modular-driven **−0.45**. Among equal-size structures:
+0.38, −0.07, 0.00. In the equilibrium family *size alone* (smaller lives longer) gives +0.47, so Φ's success there is
largely a size effect.

Standardised regression coefficients (Δ log V per +1 SD, within-world):

| family | P | C | K_H | IAX |
|---|---|---|---|---|
| all | +0.024 | +0.095 | −0.072 | 0.000 (CI ∋ 0) |
| equilibrium | +0.058 | +0.193 | −0.236 | −0.041 |
| driven | +0.010 | +0.075 | −0.030 (CI ∋ 0) | +0.011 |
| modular driven | +0.037 | +0.113 | −0.040 | 0.000 (CI ∋ 0) |

Flux ratio log(V_driven / V_eq): equilibrium +0.02 ± 0.005 (control; about 2%, plausibly Monte-Carlo noise since all
structures in a world share trajectories — not investigated further); driven −0.21 ± 0.015; modular −0.24 ± 0.018.
Price selection term Cov(w/w̄, Φ_orig) is positive in 100% of equilibrium worlds, 27% of driven, 20% of modular.

### Verdicts on pre-registered hypotheses
- **H1 (Φ_orig ranks structures by viability): not supported.** Pooled ρ = −0.08, CI includes 0. Works only in the equilibrium family and there is largely a size effect.
- **H2 (signs +P, +C, −K, stable across families): partially supported.** Signs of P and C are positive in every family; K_H is negative in three of four (CI includes 0 in driven). Magnitudes are **not** universal (K_H coefficient differs ~8× between equilibrium and driven; IAX changes sign). P's effect is small (≈ 0.01–0.06 SD per SD).
- **H3 (control and flux ratio): control passes (≈ +2%); the "explained by features" half was not tested.** Driven dynamics shorten persistence of marginal structures by about 20% at fixed stationary law (V_driven/V_eq ≈ 0.8). This is *consistent in direction* with the accelerated-mixing results for non-reversible diffusions (Hwang et al.), but we did not test that link.
- **H4 (ΔΦ predicts survival synergy beyond static I(A;B)): not supported.** See below.

## E4 — merging
S = V_union (1/V_A + 1/V_B) exceeds 1 in 88% of pairs. Within-world Spearman ρ with log S:

| predictor | all | equilibrium | driven | modular |
|---|---|---|---|---|
| ΔΦ_orig | −0.20 [−0.25, −0.13] | −0.56 | −0.07 (CI ∋ 0) | +0.04 (CI ∋ 0) |
| static I(A;B) (= λ·I term of ΔΦ) | **+0.41** [+0.37, +0.45] | +0.57 | +0.33 | +0.33 |
| ΔP | −0.45 | −0.56 | −0.42 | −0.37 |
| ΔC | +0.05 (CI ∋ 0) | −0.57 | +0.36 | +0.36 |

Sign agreement between ΔΦ > 0 and S > 1 is 0.50 (chance). Static dependence alone predicts synergy; the Φ super-additivity
criterion does not improve on it, and its P-term points the wrong way (merging shrinks the environment, lowering P).

## Update after S1 (2026-10-21): read docs/S1.md
The S1 robustness sweep changes the H1 verdict. H1 is supported at τ = 0.5 and when D is not the identity (D-test r = 3).
So the H1 result below holds for this baseline only. It depends on τ, on the fixed λ = 0.25 and on D = I.
C predicts viability in all 9 settings, and H4 fails in all 9 settings. Details and the corrected claims are in `docs/S1.md`.

**Update after S1b (2026-10-21): read docs/S1b_unitfree.md.** Replace K_H by the multi-information TC, which does not depend
on units. Then P + C − 0.25·TC predicts viability in all 9 S1 settings (ρ +0.33 to +0.53, all CIs exclude 0), and the TC
coefficient is negative everywhere. The K_H term caused the negative H1 result.

## What this does and does not show
- In **passive linear-Gaussian worlds**, with **MFPT out of a Mahalanobis ball** as viability, the proposed Φ is **not** a good predictor of viability, and the merge criterion fails.
- What does track viability is **persistence (C)**, which is partly expected by construction (slow structures live long; D = I ties variance to slowness, which also makes K_H a proxy for timescale and explains its mixed marginal/conditional sign).
- Predictive information P has a small positive partial effect. This is what one should expect *if information only pays when it is used*: nothing in these worlds acts on P.
- This is **not** a refutation of T3 in general. It refutes this functional in this ensemble. The untested regimes (action loops, hidden-state environments, nonlinear metastability, heredity) are exactly those where the theory was supposed to bite (ROADMAP).
- The result is a concrete next step: the discriminating experiment is Track A/N, where information can be *used* and where equilibrium "rocks" exist.
