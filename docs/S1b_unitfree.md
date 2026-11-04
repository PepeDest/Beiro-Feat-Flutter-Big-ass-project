# S1b: a complexity term that does not depend on units

This file was written on 2026-10-21, **before** any S1b number existed. The results section at the end was added after the analysis.

## Why
Φ_orig = P + βC − λK_H uses the differential entropy K_H = h(A_t). If a variable x_i is measured in other units
(x_i → c_i x_i), K_H of every structure that holds x_i changes by log c_i. Different structures hold different variables,
so the ranking of structures by Φ_orig changes with the units. P, C and the viability V (exit from a Mahalanobis ball)
do not change with the units. So the K_H term makes Φ_orig depend on an arbitrary choice. S1 also showed that with
D = I, K_H mostly measures slowness (docs/S1.md).

## The new term
Multi-information (total correlation) of a structure A with k variables:

  TC(A) = Σ_i h(x_i) − h(A) = −½ log det R_A,

with R_A the correlation matrix of A (stationary law). TC = 0 for one variable. TC does not change with the units,
because it uses only correlations. [Watanabe60]. It measures how much the parts of A depend on each other.

New score, with the same weights as Φ_orig (no tuning): **Φ_TC = P + C − 0.25 · TC.**

## Data
The 9 S1 datasets (baseline, τ 0.5, τ 2, p_out 0.01, p_out 0.2, N 5, N 7, D-test r 2, D-test r 3). No new simulation.
Same structures, same mask (5 or more exits) and same cluster bootstrap over worlds as E3.

## Rules (fixed before the analysis)
| Rule | Question | Outcome |
|---|---|---|
| R1 | Is TC free of units? | A test rescales each variable by a random factor. The Φ_TC ranking must stay the same, and the Φ_orig ranking must change. |
| R2 | H1 for Φ_TC in each setting | "supported" if the CI low of the mean within-world ρ(Φ_TC, log V) is > 0, else "not supported". |
| R3 | Is Φ_TC stable when D changes? | "stable" if the R2 verdict is the same in baseline, D-test r 2 and D-test r 3, and \|ρ(r 3) − ρ(baseline)\| < 0.1. Else "not stable". |
| R4 | Does the TC term help? | Compare ρ(Φ_TC) with ρ(P + C) (point values). "helps" if Φ_TC is higher in 7 or more of 9 settings. "hurts" if it is lower in 7 or more. Else "no clear effect". |
| R5 | Is the TC sign stable? | Regress within-world log V on standardised (P, C, TC, IAX). "stable" if the TC coefficient has the same point sign in all 3 families in 8 or more of 9 settings. The sign is reported. |

Expectation written before the analysis: TC removes the unit problem and the D = I link to slowness. It does **not**
remove the τ problem of S1, because τ changes the scale of C and P, and TC does not depend on τ. So R3 can pass while
the τ settings still disagree.

Also reported, as description only (no rule): ρ(−TC) among structures of equal size, and Φ_orig for comparison.

## Results (added 2026-10-21, after the analysis)
The full table is in `results/s1b_table.md` (made by `experiments/s1b_unitfree.py`). Numbers are mean within-world ρ with log V.

| Rule | Verdict | Numbers |
|---|---|---|
| R1 (free of units) | passes | `tests/test_gaussian.py::test_total_correlation_is_free_of_units` |
| R2 (H1 for Φ_TC) | supported in 9 of 9 settings | ρ from +0.33 to +0.53. All CIs exclude 0. |
| R3 (stable when D changes) | not stable | The R2 verdict is the same in all three D settings. The change from baseline to r = 3 is +0.1008, and the limit was 0.1. For comparison, Φ_orig changes by +0.27. |
| R4 (TC helps over P + C) | helps | Φ_TC is higher than P + C in 9 of 9 settings, by +0.015 to +0.086. The CIs overlap, so each single gain is small. |
| R5 (TC sign) | stable, negative | The TC coefficient is negative in all 3 families in all 9 settings. |

Other observations (description only):
- Among structures of equal size, ρ(Φ_TC) is between +0.47 and +0.71.
- ρ(−TC) among structures of equal size is between +0.13 and +0.22. At fixed size, structures with less internal dependence live longer.
- ρ(−TC) is the same at τ = 0.5, 1 and 2 (+0.15). This is a check: TC and V do not depend on τ.

### The expectation was partly wrong
I expected TC to leave the τ problem of S1. It did not: Φ_TC is supported at all three τ values. The likely reason is the
scale: TC changes much less across structures than K_H does, so the penalty never outweighs C. This explanation is post hoc.
A check on the baseline data supports it. The within-world spread of the penalty term is 0.25 × sd(TC) = 0.017, against
0.25 × sd(K_H) = 0.397. The spread of C is 0.304, 0.124 and 0.034 at τ = 0.5, 1 and 2, so it stays larger than the TC penalty at every τ.

### What this means
- The negative H1 result of RESULTS.md comes from the K_H term. When K_H is replaced by a term free of units, the
  functional P + C − λ·TC predicts viability in every S1 setting, with the original λ = 0.25 and no tuning.
- Internal dependence (TC) acts as a cost: at fixed P and C, a more integrated structure leaves its viability set sooner.
  This agrees in sign with the "complexity cost" of the original proposal. In this passive linear world, it does not
  agree with "integration helps survival".
- C still carries most of the effect: P + C alone gives +0.28 to +0.48.
- Limits: linear-Gaussian, passive worlds only. λ = 0.25 was kept, not chosen for TC. TC is one choice among other
  unit-free terms. The I(A;B) merge result (H4) is not tested again here.
