# Rerun after the code review (phase C)

This file was written on 2026-11-04, **before** any phase C run. The results sections were added after the runs.
Context: `docs/code_review.md`. The reruns use the fixes of phase B:
- **#1** Brownian-bridge correction of the exit check (`--bridge`). At dt = 0.05 the old check made log V too high by
  +0.2 to +1.2, more for fast structures.
- **#5** common random numbers for the driven run and its equilibrium counterpart (`--crn`).
- **#2** E4 uses all 270 eligible merge pairs per world (was 125).
- **#7** survival curve P(T > a) in S4.

All new outputs carry the tag `_v2`. The old files stay; old numbers in the step documents are marked as superseded,
with the new value next to them.

## C0. Settings
- **E3 / E4 baseline `_v2`:** N = 6, τ = 1, p_out = 0.05, 30 worlds per family, 600 trajectories, dt = 0.05,
  t_max = 200, seed 2026 (same worlds as before), `--crn --bridge`. Command:
  `python e3_phi_vs_viability.py --crn --bridge --tag _v2`, then `python e4_merging.py --tag _v2`.
  Expected time: about 12 minutes for E3 (7.6 s per world measured), 2–4 minutes for E4.
- **Analyses on `_v2` (no simulation):** `s1_summary.py --suffix _v2`, `s1b_unitfree.py --suffix _v2`,
  `e9_growth.py --tag _v2`. Only the baseline is rerun, so rules that need all 9 S1 settings are not computed, and
  S4 rule G2 (needs p_out 0.2) is not run. The other 8 S1 settings wait for an explicit go.
- **S3 `_v2`:** `python e5_agency.py --bridge --tag _v2` (same 400 organisms, seed 2026), then `python e5b_lag.py --tag _v2`.
  Expected time: 3–6 minutes.
- **C1 dt control:** `python c1_dt_control.py` (12 worlds: 4 per family, k = 0–3, driven dynamics only).
  Expected time: 15–20 minutes.

## C1. Rules for the dt control (fixed before the run)
Runs per world: a) dt 0.05 with bridge; b) dt 0.005 with bridge; c) dt 0.05 without; d) dt 0.005 without;
e) extrapolation to dt → 0 from c) and d), linear in √dt. Structures with ≥ 5 exits in all four runs.
Monte Carlo error per structure: SE(log V) ≈ 1/√(exits); z = difference / combined SE.

| Rule | Comparison | Verdict |
|---|---|---|
| K1 (main) | a − b: is the corrected V independent of dt? | "agree" if \|mean difference\| < 0.03 and the mean over worlds of sd(z) < 1.5 |
| K2 | a − e: does the corrected V match the dt → 0 extrapolation of the old method? | "agree" if \|mean difference\| < 0.05 and sd(z) < 1.5 (the extrapolation is noisier) |
| K3 | a − d: is the corrected V equal to dt = 0.005 without correction? | same rule as K1 |

Also reported (description only): c − e (bias of the old method), the mean Spearman between the log V rankings,
and ρ(C, log V) among structures of equal size for a, b, c, d.

**Expectations, and why K3 is expected to fail.** The phase B request was to compare the corrected log V with dt = 0.005
without correction. A 1-D check (θ = 0.3 to 9, run before writing these rules) shows that dt = 0.005 without
correction still has a log-bias of +0.08 to +0.40, about one third of the bias at dt = 0.05, because the boundary shift
grows like √dt. In the same check the bridge at dt 0.05 and 0.005 and the extrapolation are all within about 0.05 of
the exact value. So I expect **K1 "agree", K2 "agree", K3 "do not agree"**, with a − d about −0.1 to −0.2.
If K1 fails, the bridge does not remove the dt dependence in multi-dimensional structures, and the E3 rerun must not be
interpreted until this is understood.

## C2. Rules for E3 / E4 `_v2` (fixed before the run)
H1–H4 use the verdict rules of `docs/S1.md` unchanged. In addition:

| Rule | Question | Verdict |
|---|---|---|
| V0 | Is the H3 control exact with common random numbers? | "exact" if \|mean log R\| < 1e-9 in the equilibrium family |
| V1 | Does C still predict life? (README S1 row) | "stands" if ρ(C only, equal size) has CI low > 0 |
| V2 | Is Φ_orig still not a reliable predictor? (baseline H1) | "stands" if H1 is "not supported" |
| V3 | Does the drive still shorten life? (S1 point 3) | "stands" if mean log R < 0 in both driven families and its 2-SE interval excludes 0 |
| V4 | Does H4 still fail with all pairs? (S1 point 2) | "stands" if H4 is "not supported" |
| V5 | Size of the change | Report old and new values of ρ(Φ_orig), ρ(C only) (all and equal size), ρ(−K_H, equal size), the 12 regression coefficients, mean log R per family, and the E4 ρ of ΔΦ and I(A;B). Description only. |

Expectations: V0 "exact". V1–V4 "stand". From the 4-world check in docs/code_review.md (item 1), ρ(C, log V) can move by
up to ±0.15 in a single world; I expect the mean over 90 worlds to move by less than 0.1. Absolute V falls by about 0.3 in
log V. The flux effect (mean log R in driven worlds) may grow slightly in size (about −0.2 → −0.2 to −0.25).
Old values (S0 baseline): ρ(Φ_orig) −0.08 [−0.20, +0.03]; ρ(C only) +0.33 all, +0.55 equal size; ρ(−K_H, equal size)
−0.70; E4 ρ(ΔΦ) −0.20, ρ(I(A;B)) +0.41.

## C2b. Rules for τ 0.5 and τ 2 on `_v2` (fixed 2026-11-04, before these runs; added after the go for them)
**Why.** In S1 the τ settings reused the baseline exit data and recomputed only the information features (docs/S1.md).
After the E3 `_v2` run, the old τ settings would still use the old exit check. So they are redone from the `_v2` exit
data, with no new simulation: `python e3_phi_vs_viability.py --sim_from _v2 --tau 0.5 --tag _tau0.5_v2` (and τ 2), then
`python e4_merging.py --tag _tau0.5_v2` (and `_tau2_v2`). `s1_summary.py --suffix _v2` then reports baseline, τ 0.5 and τ 2
together. As a description, `s1_lambda_scan.py` is rerun on the three `_v2` datasets. Expected time: a few minutes.

| Rule | Question | Verdict |
|---|---|---|
| T1 | H1 at τ 0.5 (old: supported, +0.15) | S1 rule for H1 |
| T2 | H1 at τ 2 (old: not supported) | S1 rule for H1 |
| T3 | Does C still predict life at τ 0.5 and τ 2? | "stands" if ρ(C only, equal size) has CI low > 0 in both |
| T4 | Does H4 still fail at τ 0.5 and τ 2? | "stands" if H4 is "not supported" in both |
| T5 | README S1 claim "its verdict depends on τ" | "stands" if the H1 verdict at τ 0.5 differs from the H1 verdict at τ 1 or at τ 2 (all three `_v2`) |
| T6 | S1b R2 at τ 0.5 and τ 2 (Φ_TC, CI low > 0) | "supported" in each setting, as in docs/S1b_unitfree.md |

Expectations: T1 "supported", T2 "not supported", T3 and T4 "stand", T5 "stands", T6 "supported" in both. These
expectations follow the old results. The bridge changes log V most for fast structures, and the λ scan
(results/s1_lambda_scan.md) shows that H1 at τ 0.5 rests on the C : K_H balance, so T1 is the least certain.
The D-test claim (S1 point 5) uses the baseline value of ρ(−K_H, equal size) as its reference, but the D-test runs keep the
old exit check. It is not re-evaluated here; the new baseline value is reported next to the old one.

## C3. Rules for S1b, S4 and S3 on `_v2` (fixed before the runs)
Same rule texts as in the step documents, applied to the `_v2` data:

| Step | Rules applied | Not applied | Expectation |
|---|---|---|---|
| S1b (`docs/S1b_unitfree.md`) | R2 (Φ_TC, CI low > 0), sign of the TC coefficient in the 3 families (part of R5) | R3, R4, R5 thresholds (need 9 settings) | R2 "supported"; TC coefficient negative in all 3 families |
| S4 (`docs/S4.md`) | G1 (both maturation settings), G3, G4 | G2 (needs the p_out 0.2 dataset) | G1 "agree", G3 "yes", G4 "mutation erodes selection" |
| S3 (`docs/S3.md`) | R1–R5, Gate, S3b R4a–R4c | — | same verdicts as before: R1 "used", R2 "depends on the loop", Gate "not triggered", R3 "yes", R4 "not present", R5 "supported", R4a/R4b "not present", R4c "explained" |

For S3 the bridge changes the exit check of v in all three versions. I expect VoI (mean log V_intact − log V_scrambled,
old +1.27) to change by less than 0.2, because the bias is similar in the intact and the scrambled versions.

A verdict that changes is reported in this file and in the step document, next to the old verdict.

## C4. Which conclusions of README and ROADMAP stand
Written after C1–C3: see "C4 results" at the end of this file.

## C1 results (added 2026-11-04, after the run)
Report: `results/c1_dt_control.md`, `.json`, `.log`. 12 worlds, 436 s.

| Rule | Comparison | Mean difference of log V [95% CI over worlds] | sd(z) | Verdict |
|---|---|---|---|---|
| K1 | bridge dt 0.05 − bridge dt 0.005 | +0.011 [−0.008, +0.029] | 0.86 | agree |
| K2 | bridge dt 0.05 − extrapolation dt → 0 | +0.022 [−0.007, +0.052] | 0.87 | agree |
| K3 | bridge dt 0.05 − no bridge dt 0.005 | −0.131 [−0.152, −0.109] | 0.89 | do not agree (as expected) |
| description | no bridge dt 0.05 − extrapolation (old bias) | +0.482 [+0.437, +0.527] | 1.11 | |

All three verdicts are as written before the run. The corrected V does not depend on dt and matches the dt → 0
extrapolation of the old method within the Monte Carlo error (sd(z) < 1, so the differences are noise). dt = 0.005
without correction still keeps a bias of about +0.13, as the 1-D check predicted, so it is not a valid reference.
The old method at dt = 0.05 is biased by +0.48 in log V on average in these worlds (driven dynamics).
Description: ρ(C, log V) among structures of equal size, mean over the 12 worlds: +0.68 (bridge 0.05), +0.64 (bridge 0.005),
+0.63 (no bridge 0.05), +0.63 (no bridge 0.005). The differences are inside the CIs (about ±0.15).

## C2 results: E3 / E4 baseline `_v2` (added 2026-11-04, after the run)
Reports: `results/e3_report_v2.md`, `e3_summary_v2.json`, `e3_run_v2.log` (E3, 90 worlds, 5,580 structures, about 15 min with
another run in parallel) and `results/e4_report_v2.md`, `e4_merging_v2.json` (E4, 24,300 pairs; the old run had 11,250).

| Rule | Old (S0 baseline) | New (`_v2`) | Verdict |
|---|---|---|---|
| V0: mean log R, equilibrium | +0.019 ± 0.005 | 0.000 (exact) | exact |
| V1: ρ(C only), equal size | +0.55 [+0.49, +0.60] | +0.55 [+0.49, +0.61] | stands |
| V2 / H1: ρ(Φ_orig), all structures | −0.08 [−0.20, +0.03] | −0.01 [−0.12, +0.10] | stands (not supported) |
| V3: mean log R, driven / modular | −0.21 / −0.24 | −0.190 ± 0.013 / −0.245 ± 0.019 | stands |
| V4 / H4: ρ(ΔΦ) against ρ(I(A;B)) with log S | −0.19 against +0.41 | −0.17 [−0.23, −0.11] against +0.36 [+0.32, +0.40] | stands (not supported) |
| H2: signs +P +C −K_H | partial (K_H in driven: CI [−0.067, +0.004]) | partial (P in driven: CI [−0.0004, +0.021]) | same verdict, different reason |
| H3 control | supported | supported | same |

V5, description:

| Measure | Old | New |
|---|---|---|
| ρ(C only), all structures | +0.33 | +0.26 |
| ρ(P only), all / equal size | +0.09 / +0.14 | +0.09 / +0.13 |
| ρ(−K_H), all / equal size | −0.26 / −0.70 | −0.19 / −0.74 |
| ρ(−leak), all | +0.12 | +0.10 |
| fitted linear (cross-fitted), all / equal size | +0.36 / +0.49 | +0.33 / +0.48 |
| ρ(Φ_orig) per family: equilibrium / driven / modular | +0.54 / −0.34 / −0.45 | +0.56 / −0.23 / −0.37 |
| coefficients P, C, K_H, all families | +0.024, +0.095, −0.072 | +0.031, +0.123, −0.111 |
| coefficients P, C, K_H, equilibrium | +0.058, +0.193, −0.236 | +0.066, +0.242, −0.300 |
| coefficients P, C, K_H, driven | +0.010, +0.075, −0.030 | +0.010, +0.093, −0.058 |
| coefficients P, C, K_H, modular | +0.037, +0.113, −0.040 | +0.049, +0.144, −0.075 |
| Price selection term > 0: equilibrium / driven / modular | 100 % / 27 % / 20 % | 100 % / 47 % / 27 % |
| E4: fraction of pairs with S > 1 | 0.88 | 0.77 |
| E4: sign agreement ΔΦ > 0 with S > 1 | 0.50 | 0.56 |

All verdicts are as expected before the run. Two changes in size: the regression coefficients grow by 20–100 % (the
correction removes a bias that compressed the differences between fast and slow structures), and ρ(C only) over all
structures falls from +0.33 to +0.26, while among structures of equal size it does not change.

## C2b results: τ 0.5 and τ 2 from the `_v2` data (added 2026-11-04, after the run)
Reports: `results/e3_report_tau0.5_v2.md`, `e3_report_tau2_v2.md`, the matching `e4_report_*_v2.md`, `s1_table_v2.md`,
`s1_lambda_scan_v2.md`, `s1b_table_v2.md`. A few minutes in total.

| Rule | Old | New | Verdict |
|---|---|---|---|
| T1: H1 at τ 0.5 | supported, +0.15 [+0.03, +0.26] | supported, +0.23 [+0.12, +0.33] | as expected |
| T2: H1 at τ 2 | not supported, −0.23 [−0.33, −0.12] | not supported, −0.16 [−0.26, −0.07] | as expected |
| T3: ρ(C only), equal size, τ 0.5 / τ 2 | +0.68 / +0.48 | +0.69 [+0.65, +0.73] / +0.48 [+0.42, +0.55] | stands |
| T4: H4 at τ 0.5 / τ 2 | not supported / not supported | not supported (ΔΦ −0.16, I(A;B) +0.36) / not supported (ΔΦ −0.01, I(A;B) +0.36) | stands |
| T5: "the H1 verdict depends on τ" | yes | yes (supported at τ 0.5 only) | stands |
| T6: S1b R2 at τ 0.5 / τ 2 | supported +0.33 / supported | supported +0.27 [+0.18, +0.35] / supported +0.47 [+0.42, +0.52] | as expected |

**One verdict changed that no rule of C2b covered:** H2 at τ 2 was "not supported" (K_H had the wrong sign in the driven
and modular families) and is now "partial" (all signs right; the K_H CIs in driven and modular include 0). The K_H
coefficient at τ 2 is −0.010 [−0.038, +0.013] (driven) and −0.013 [−0.040, +0.011] (modular). So the "wrong sign" at τ 2
was within the bias of the old exit check. H2 at τ 0.5 stays "supported".
The λ scan (description) keeps its pattern: a small λ gives a positive ρ at every τ and a large λ a negative ρ;
P + C alone (λ = 0) gives +0.25, +0.29 and +0.32 at τ = 0.5, 1, 2 (old +0.32, +0.36, +0.39).

## C3 results: S1b, S4 and S3 on `_v2` (added 2026-11-04, after the runs)
| Step | Rule | Old | New | Verdict |
|---|---|---|---|---|
| S1b | R2 baseline: ρ(Φ_TC, log V) | +0.41 [+0.34, +0.48] | +0.34 [+0.27, +0.42] | supported (same) |
| S1b | TC coefficient, eq / driven / modular (baseline) | −0.118 / −0.034 / −0.045 | −0.156 / −0.047 / −0.059 | negative in all 3 families, also at τ 0.5 and τ 2 (same) |
| S1b | P + C (baseline), description | +0.36 | +0.29 | Φ_TC is above P + C in all 3 corrected settings |
| S4 | G1 a_m = 0 | +0.90 [+0.89, +0.91] | +0.95 [+0.94, +0.96] | agree (same, now clear of the 0.9 limit) |
| S4 | G1 a_m = median V | +0.99 | +0.99 [+0.99, +0.99] | agree (same) |
| S4 | G2 | V more stable | not run (needs p_out 0.2) | — |
| S4 | G3: ρ(Φ_TC, r) | +0.41 [+0.35, +0.48] | +0.35 [+0.29, +0.41] | yes (same) |
| S4 | G4: S / T | +0.009 / −0.001 | +0.008 [+0.005, +0.010] / −0.001 [−0.001, −0.001] | mutation erodes selection (same) |
| S4 | post-hoc CV of exit times (description) | median 1.015 (0.95–1.09) | median 1.037 (0.97–1.11) | lives stay close to exponential |
| S3 | R1: mean VoI | +1.27 [+1.16, +1.40] | +1.27 [+1.14, +1.40] | used (same) |
| S3 | R2: β_P intact / scrambled / difference | +0.75 / +0.38 / +0.37 | +0.76 / +0.37 / +0.38 [+0.25, +0.52] | depends on the loop (same) |
| S3 | R3, R4, R5, Gate | yes / not present / supported / not triggered | +0.41 / +0.30 / +0.21 [+0.11, +0.31]; same verdicts | same |
| S3 | S3b R4a / R4b / R4c | +0.36 / −0.13 / −0.00 | +0.35 / −0.13 / −0.04 [−0.13, +0.07] | not present / not present / explained (same) |
| S3 | organisms kept | 394 | 395 | |

Every C3 verdict is the same as before and as expected. As expected, S3 hardly moves: VoI changes by less than 0.01.

## C4 results: which conclusions of README and ROADMAP stand (added 2026-11-04)
Based on a claim-by-claim map of README.md and docs/ROADMAP.md against the step documents (67 claims). Settings rerun with
the corrected exit check: S1 baseline, τ 0.5, τ 2; S1b, S4 (without G2) and S3 on them. Not rerun: p_out 0.01, p_out 0.2,
N 5, N 7, D-test r 2 and r 3; S2, S2b, S2c; S5 and S6 do not use this exit check.

**Stand, now on corrected data**
- S1 baseline: Φ_orig does not predict viability (H1 not supported), C does (+0.55 among structures of equal size),
  P has a small positive effect, the merge criterion fails (H4), driven dynamics shorten life by about 17–22 %.
- S1: "the verdict of Φ_orig depends on τ" (H1 supported at τ 0.5 only). The ROADMAP S1 gate still triggers.
- S1b: P + C − 0.25·TC predicts life (baseline, τ 0.5, τ 2), and the TC coefficient is negative in every family.
- S3: information pays when it is used: VoI +1.27, life about 3.5 times longer (old text: 3.6); P's effect depends on the loop; the gate is not triggered. S3b unchanged.
- S4: the growth rate ranks like the mean exit time (ρ 0.95 and 0.99), because lives are near exponential (CV 1.04);
  selection on Φ_TC is positive (74 % of worlds) and the random-swap transmission term is small and negative (98 %).

**Stand, but partly on old data (wording should say so)**
- "C predicts life in all 9 settings" and "P + C − 0.25·TC predicts life in all 9 settings": confirmed in the 3 corrected
  settings; the other 6 still use the old exit check.
- "H4 fails in every setting": 3 of 9 corrected.
- "The D-test supports the D = I confound for K_H": the D-test runs are old, and the reference value moved
  (baseline ρ(−K_H, equal size) −0.70 → −0.74). Not re-evaluated.
- S2c "hurts where the drive only stirs" (D4 −0.18, D5 −0.52) and "its link to life changes sign with D" (D3 +0.10
  [+0.01, +0.19]): computed on the old baseline and D-test data; e7 cannot be rerun here (it also needs the S2 data files).
  The D3 sign is the most fragile, because its CI low was +0.01.

**Changed**
- H2 at τ 2: "not supported (wrong sign of K_H)" → "partial". The wrong sign was within the bias of the old check.
- The size of the effects: regression coefficients are 20–100 % larger; ρ(C only) over all structures +0.33 → +0.26;
  the share of merge pairs with S > 1 is 77 %, not 88 % (with all pairs).
- The equilibrium control: log R is exactly 0, not "+2 %, plausibly Monte Carlo noise".
- S0 "the shipped results reproduce (largest change 0.003)": still true for the old code, but the numbers of
  RESULTS.md are now superseded on purpose.

**Not affected by phase C**: S2 and S2b (own nonlinear simulator, dt = 0.01), S5, S6, S6b, S6c.
**Already stale before phase C** (code review items 4, 11 and ROADMAP text): "Price identity exact to 1e-16" (true by
construction), the growth exponent 1.92 (depends on the time origin), and the ROADMAP lines "not measured yet" and
"no test with mutation", which the S6c status line contradicts.

## C5. Rules for the other 6 S1 settings on corrected data (fixed 2026-11-04 about 23:51 UTC, before these runs; first written as 23:55)
**Runs.** One at a time, all cores, same seeds and settings as the old S1 runs (30 worlds per family, 600 trajectories,
dt 0.05, t_max 200), now with `--crn --bridge` and the tag `<old tag>_v2`, each followed by `e4_merging.py --tag <tag>`:
`_p0.2_v2` (`--p_out 0.2`), `_N5_v2` (`--N 5`), `_D2_v2` (`--noise_range 2`), `_D3_v2` (`--noise_range 3`),
`_N7_v2` (`--N 7`), `_p0.01_v2` (`--p_out 0.01`). Order: shortest first. Estimated time on this machine with all cores:
15–25 min each for p_out 0.2, N 5, D2, D3; about 1.5 h each for N 7 and p_out 0.01; about 4–5 h in total.
After the last run: `s1_summary.py --suffix _v2` (all 9 settings), `s1b_unitfree.py --suffix _v2` (R3–R5 can now be
computed), `e9_growth.py --tag _v2 --wide_tag _p0.2_v2` (S4 rule G2).

| Rule | Question | Verdict |
|---|---|---|
| W1 | Does C predict life in all 9 corrected settings? | "stands" if ρ(C only, equal size) has CI low > 0 in all 9 |
| W2 | Does H4 fail in all 9? | "stands" if H4 is "not supported" in all 9 |
| W3 | Is the H3 control exact in all 9? | "exact" if \|mean log R\| < 1e-9 in the equilibrium family of every setting |
| W4 | In which settings is H1 supported (S1 gate)? | Listed. Old: τ 0.5 and D-test r 3. |
| W5 | D-test rule of docs/S1.md on corrected data | "supported" if ρ(−K_H, equal size) in `_D3_v2` moves toward 0 by more than 0.2 from the corrected baseline (−0.74), and `_D2_v2` lies between the baseline and `_D3_v2`; else "not supported" |
| W6 | S1b rules R2–R5 on all 9 corrected settings | thresholds of docs/S1b_unitfree.md, unchanged |
| W7 | S4 rule G2 with `_p0.2_v2` | rule of docs/S4.md, unchanged |
| W8 | Size of the change, per setting | old and new H1 ρ, ρ(C only, equal size), ρ(−K_H, equal size), mean log R. Description only. |

Expectations: every old verdict holds: W1 "stands", W2 "stands", W3 "exact", W4 "τ 0.5 and D-test r 3", W5 "supported"
(old: −0.70 → −0.29 → −0.08), W6 as in S1b (R2 supported in 9 of 9, R5 stable and negative), W7 "V more stable".
The least certain is W5 and the H1 verdict of the D-test r 3: the D-test makes rates up to about 9, where the old check
had its largest bias (+1.2 in log V), so the old D-test shift can be partly an artefact of the check. List item 5 of the
night plan measures this directly.
If a run fails twice, it is recorded in docs/night_log.md and the next setting starts.

## D. KSG at high mutual information (code review item 6; rules fixed 2026-11-04 about 23:53 UTC, before the run; first written as 00:05, which was wrong)
**Run D1.** `python d1_ksg_highmi.py`: KSG (k = 4, as in S2) on 4-dimensional pairs X = (x1, x2), Y = (y1, y2) with exact
I(X; Y) = 0.5, 1, 2, 2.7 and 3.5 nats, n = 4000 (as S2/S2b) and n = 16000, 20 repetitions, in two geometries with the same
exact MI: Gaussian, and "ring" (an invertible map of each 2-vector to curved, ring-like sets; MI does not change under
invertible maps of X and Y separately). Expected time: a few minutes.

| Rule | Question | Verdict |
|---|---|---|
| D1 | Is KSG wrong by a lot where S2 uses it? | "wrong by a lot" if, at n = 4000 and exact MI 2–3 nats, \|bias\| > 0.2 nats or > 10 % in either geometry; else "adequate" |
| D2 | Does more data fix it? | Description: bias at n = 16000 against n = 4000 |

**What follows from D1 (fixed now).** If D1 is "adequate", e6, e6b and e7 are not rerun, and the S2 numbers stand with
the validated range extended. If D1 is "wrong by a lot", e6 and e6b are rerun with 4 times more pairs for C and TC
(16000 instead of 4000; everything else, including the seeds of the units, unchanged; tag `_v2`), then e7 on these data.
Rules for that rerun: the S2 rules F1–F4 and the S2b rules G0–G4 and the gate, unchanged; S2c rules D1–D2 (nonlinear part)
unchanged. A verdict that changes is reported next to the old one.
Expectation: KSG underestimates high MI (negative bias), more in the ring geometry, and less with more data. I expect
"wrong by a lot" for the ring geometry at 2.7 nats. If so, I expect the S2 verdict F2 ("C favours oscillators", AUC 0.00)
to stand, because the gap between the classes is large, and the S2b verdict G2 (signal of about 0.01 nats near the noise)
to be the least certain.

### D1 results (added 2026-11-04 23:55 UTC, after the run)
Report: `results/d1_ksg_highmi.md`, `.json`, `_run.log`. 74 s.

| Exact MI (nats) | n = 4000, Gaussian | n = 4000, ring | n = 16000, Gaussian | n = 16000, ring |
|---|---|---|---|---|
| 0.5 | +0.004 | −0.032 | +0.008 | −0.010 |
| 1.0 | +0.009 | −0.050 | +0.016 | −0.010 |
| 2.0 | −0.002 | −0.113 | +0.025 | −0.024 |
| 2.7 | −0.023 | −0.180 | +0.020 | −0.056 |
| 3.5 | −0.081 | −0.297 | +0.004 | −0.109 |

(values are the bias, mean estimate − exact)

**D1: "adequate".** The largest bias at n = 4000 and 2–3 nats is −0.18 nats (6.7 %, ring geometry), below both limits
(0.2 nats, 10 %). **D2:** 16000 pairs cut the ring bias by about 3 times. The expectation "wrong by a lot for the ring at
2.7 nats" was wrong: the bias is negative and larger in the ring geometry, as expected, but it stays under the limits.
So by the rule fixed before the run, e6, e6b and e7 are not rerun for the estimator. What this means for S2: the
oscillators' median C of 2.71 nats is probably about 0.1–0.2 nats too low, and the rocks' 1.57 a little too low;
the gap of about 1.1 nats between the classes, and the verdict F2, stand. The validated range of KSG now covers 0.5–3.5
nats in 4 dimensions.

## P5. How much of the D-test shift and of the S3 VoI came from the dt bias (rules fixed 2026-11-05 00:04 UTC, before the analysis)
No new run: old results (old exit check) against the corrected `_v2` results, same worlds and seeds.
- **D-test.** Δ = ρ(−K_H, equal size) in D-test r 3 minus the baseline value. Old Δ_old = −0.08 − (−0.70) = +0.62.
  Share of the shift that came from the old check: s = 1 − Δ_new / Δ_old. The same for D-test r 2 and for H1 (ρ(Φ_orig)).
- **S3.** s = (VoI_old − VoI_new) / VoI_old; also for β_P (intact) and for the loop difference of β_P.

| s | Label |
|---|---|
| > 0.5 | "mostly from the dt bias" |
| 0.2 to 0.5 | "partly from the dt bias" |
| −0.2 to 0.2 | "little from the dt bias" |
| < −0.2 | "the dt bias hid part of the effect" |

Expectations: S3 "little" (VoI moved by −0.008, already known from C3). D-test: uncertain; the D-test makes rates up to about
9, where the old check was worst, so I expect "partly" for the K_H shift.
