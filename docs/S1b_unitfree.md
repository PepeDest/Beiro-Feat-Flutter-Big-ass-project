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
| R2 (H1 for Φ_TC) | supported in 9 of 9 settings (same on corrected data) | ρ from ~~+0.33~~ ~~+0.27~~ +0.23 to ~~+0.53~~ +0.50 (night run, `_v2`, all 9 settings corrected). All CIs exclude 0. (~~Phase C: baseline, τ 0.5, τ 2 corrected; the other 6 settings use the old exit check.~~ Superseded 2026-11-05: all 9 settings now redone.) |
| R3 (stable when D changes) | not stable (same on corrected data) | The R2 verdict is the same in all three D settings. The change from baseline to r = 3 is ~~+0.1008~~ +0.1194 (night run, `_v2`), and the limit was 0.1. For comparison, Φ_orig changes by ~~+0.27~~ +0.26. (~~Phase C: not re-evaluated, because the D-test runs still use the old exit check.~~ Superseded 2026-11-05: re-evaluated on the corrected D-test runs.) |
| R4 (TC helps over P + C) | helps (same on corrected data) | Φ_TC is higher than P + C in 9 of 9 settings, by ~~+0.015 to +0.086~~ +0.016 to +0.145 (night run, `_v2`). The CIs overlap, so each single gain is small. (Phase C: higher in 3 of 3 corrected settings, by +0.054, +0.016 and +0.145 at baseline, τ 0.5, τ 2; ~~the 9-setting count is not recomputed~~ superseded 2026-11-05: recomputed, 9 of 9.) |
| R5 (TC sign) | stable, negative (same on corrected data) | The TC coefficient is negative in all 3 families in all 9 settings. (Phase C: still negative in all 3 families in the 3 corrected settings. Night run 2026-11-05: negative in all 3 families in all 9 corrected settings.) |

**Superseded (2026-11-04, phase C, docs/RERUN.md):** baseline, τ 0.5 and τ 2 were redone with the corrected exit check
(Brownian-bridge correction, common random numbers; tag `_v2`). New table: `results/s1b_table_v2.md` and
`results/s1b_unitfree_v2.json` (old files kept). ~~The other 6 settings still use the old exit check.~~
**Superseded (2026-11-05):** now redone, the other 6 settings (p_out 0.01, p_out 0.2, N 5, N 7, D-test r 2, r 3) were run
with the corrected exit check in the night run (docs/RERUN.md C5). All 9 rows below are on corrected data, and R2–R5 are
computed on all 9.

| setting | Φ_TC (R2) | P + C | Φ_TC, equal size | −TC, equal size | TC coef eq / driven / modular |
|---|---|---|---|---|---|
| baseline | ~~+0.41 [+0.34, +0.48]~~ +0.34 [+0.27, +0.42] supported | ~~+0.36~~ +0.29 [+0.21, +0.37] | ~~+0.56~~ +0.57 | ~~+0.15~~ +0.19 [+0.12, +0.26] | ~~−0.118 / −0.034 / −0.045~~ −0.156 / −0.047 / −0.059 |
| τ 0.5 | ~~+0.33 [+0.24, +0.42]~~ +0.27 [+0.18, +0.35] supported | ~~+0.32~~ +0.25 [+0.16, +0.34] | ~~+0.61~~ +0.64 | ~~+0.15~~ +0.19 | ~~−0.095 / −0.042 / −0.054~~ −0.128 / −0.053 / −0.068 |
| τ 2 | ~~+0.48 [+0.42, +0.53]~~ +0.47 [+0.42, +0.52] supported | ~~+0.39~~ +0.32 [+0.25, +0.40] | ~~+0.47~~ +0.49 | ~~+0.15~~ +0.19 | ~~−0.138 / −0.019 / −0.027~~ −0.180 / −0.033 / −0.041 |
| p_out 0.01 | ~~+0.33 [+0.26, +0.40]~~ +0.23 [+0.16, +0.31] supported (night run, `_v2`) | ~~+0.28~~ +0.18 [+0.10, +0.26] | ~~+0.55~~ +0.57 | ~~+0.14~~ +0.19 [+0.12, +0.26] | ~~−0.118 / −0.031 / −0.045~~ −0.165 / −0.059 / −0.065 |
| p_out 0.2 | ~~+0.53 [+0.46, +0.59]~~ +0.50 [+0.44, +0.57] supported (night run, `_v2`) | ~~+0.48~~ +0.45 [+0.38, +0.52] | ~~+0.54~~ +0.58 | ~~+0.13~~ +0.19 [+0.12, +0.26] | ~~−0.106 / −0.026 / −0.033~~ −0.136 / −0.036 / −0.044 |
| N 5 | ~~+0.40 [+0.33, +0.46]~~ +0.34 [+0.28, +0.41] supported (night run, `_v2`) | ~~+0.35~~ +0.28 [+0.21, +0.36] | ~~+0.54~~ +0.57 | ~~+0.17~~ +0.20 [+0.12, +0.28] | ~~−0.140 / −0.030 / −0.036~~ −0.192 / −0.049 / −0.056 |
| N 7 | ~~+0.40 [+0.31, +0.48]~~ +0.34 [+0.26, +0.42] supported (night run, `_v2`) | ~~+0.35~~ +0.29 [+0.20, +0.38] | ~~+0.58~~ +0.63 | ~~+0.22~~ +0.27 [+0.19, +0.33] | ~~−0.111 / −0.026 / −0.032~~ −0.147 / −0.049 / −0.043 |
| D-test r 2 | ~~+0.48 [+0.43, +0.52]~~ +0.43 [+0.39, +0.47] supported (night run, `_v2`) | ~~+0.43~~ +0.38 [+0.33, +0.43] | ~~+0.67~~ +0.69 | ~~+0.17~~ +0.19 [+0.13, +0.26] | ~~−0.173 / −0.056 / −0.060~~ −0.226 / −0.078 / −0.083 |
| D-test r 3 | ~~+0.51 [+0.47, +0.54]~~ +0.46 [+0.43, +0.50] supported (night run, `_v2`) | ~~+0.47~~ +0.41 [+0.38, +0.45] | ~~+0.71~~ +0.73 | ~~+0.15~~ +0.19 [+0.12, +0.25] | ~~−0.203 / −0.071 / −0.083~~ −0.268 / −0.104 / −0.118 |

The R2 verdict is "supported" in all ~~3~~ 9 corrected settings, and the TC coefficient is negative in every family.

Other observations (description only):
- Among structures of equal size, ρ(Φ_TC) is between ~~+0.47~~ +0.49 and ~~+0.71~~ +0.73 (phase C: τ 2 corrected to +0.49; ~~the maximum, D-test r 3, is old~~ night run, `_v2`: the maximum, D-test r 3, is now +0.73).
- ρ(−TC) among structures of equal size is between ~~+0.13 and +0.22~~ +0.19 and +0.27 (night run, `_v2`). At fixed size, structures with less internal dependence live longer. (Phase C: +0.19 in the 3 corrected settings, ~~inside this range; the range ends come from old settings~~ superseded 2026-11-05: all 9 settings corrected; +0.19 in 7 of them, +0.20 at N 5 and +0.27 at N 7.)
- ρ(−TC) is the same at τ = 0.5, 1 and 2 (~~+0.15~~ +0.19, phase C). This is a check: TC and V do not depend on τ.

### The expectation was partly wrong
I expected TC to leave the τ problem of S1. It did not: Φ_TC is supported at all three τ values. The likely reason is the
scale: TC changes much less across structures than K_H does, so the penalty never outweighs C. This explanation is post hoc.
A check on the baseline data supports it. The within-world spread of the penalty term is 0.25 × sd(TC) = 0.017, against
0.25 × sd(K_H) = 0.397. The spread of C is 0.304, 0.124 and 0.034 at τ = 0.5, 1 and 2, so it stays larger than the TC penalty at every τ.
**Note (2026-11-04, phase C):** this check uses only the features, which do not depend on the exit check. The feature
spreads in the `_v2` summaries are the same (sd(K_H) 1.587, sd(C) 0.304 / 0.124 / 0.034), so the check stands. sd(TC) is
not stored in the json files; the value 0.017 is from the old analysis, and TC also does not depend on the exit check.
On the corrected data Φ_TC is still supported at all three τ values.

### What this means
- The negative H1 result of RESULTS.md comes from the K_H term. When K_H is replaced by a term free of units, the
  functional P + C − λ·TC predicts viability in every S1 setting, with the original λ = 0.25 and no tuning.
- Internal dependence (TC) acts as a cost: at fixed P and C, a more integrated structure leaves its viability set sooner.
  This agrees in sign with the "complexity cost" of the original proposal. In this passive linear world, it does not
  agree with "integration helps survival".
- C still carries most of the effect: P + C alone gives ~~+0.28~~ ~~+0.25~~ +0.18 to ~~+0.48~~ +0.45 (night run, `_v2`, all 9 settings) (phase C: corrected values +0.29, +0.25,
  +0.32 at baseline, τ 0.5, τ 2; ~~the other 6 settings, including the maximum, still use the old exit check~~ superseded
  2026-11-05: now redone; the minimum is p_out 0.01 (+0.18) and the maximum p_out 0.2 (+0.45)).
- Limits: linear-Gaussian, passive worlds only. λ = 0.25 was kept, not chosen for TC. TC is one choice among other
  unit-free terms. The I(A;B) merge result (H4) is not tested again here.
