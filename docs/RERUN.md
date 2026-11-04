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
Written after C1–C3, in a section at the end of this file.

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
