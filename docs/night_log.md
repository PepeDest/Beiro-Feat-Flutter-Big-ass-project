# Night log (unsupervised work, 2026-11-04 23:50 UTC to 2026-11-05 07:00 UTC)

## Summary of the night (written 2026-11-05 06:00–06:28 UTC)

| List item | Result | What changes in the conclusions | What is left |
|---|---|---|---|
| 1. Phase C points 1–4 | done before the night | — | — |
| 2. The other S1 settings (6 left; τ 0.5 and τ 2 were done in phase C) | all 6 rerun with the corrected exit check (docs/RERUN.md, C5) | Nothing breaks: C predicts life in all 9 settings, H4 fails in all 9, the equilibrium control is exact in all 9, the D-test rule holds (−0.74 → −0.28 → −0.04). H1 (Φ_orig) is now also supported at D-test r 2 (+0.11 [+0.02, +0.19]). H2 improves at N 5 (supported) and N 7 (partial). S1b R2–R5 and S4 G2 keep their verdicts. | S2c rules D3–D5 still use the old exit check (e7 needs the e6/e6b data files) |
| 3. Phase D: KSG at high MI | D1: KSG adequate, bias ≤ 0.18 nats (6.7 %) at 2–3 nats in 4-D, ring geometry included | S2 numbers stand; the oscillators' C (2.71 nats) is probably 0.1–0.2 nats low; e6/e6b/e7 not rerun (rule) | — |
| 4. Phase E: S6d, longer colonies | numba port of the mutation (checked: M0, B1); 32 colonies at 600 × 600, twice the generations | With more generations f falls above μ_c (0.27 → 0.16 at 2 μ_c) and holds below; no sharper threshold. "No sharp error threshold in finite colonies" holds. | larger grid or colonies with removal; the GPU runs with the new noise hash |
| 5. dt bias share (D-test, S3 VoI) | measured (P5): shares between −0.15 and +0.07 | The D-test shift and the S3 VoI are not artefacts of the exit check. | — |
| 6. S6c edge hypothesis (S6e) | not supported: X1 0.57 (limit 0.6), X2 0.32 | The faster type sits inside the colony, not at its edge, so the S6c explanation is wrong; why A survives more than in mean field is open. | a test of the post-hoc "interior reservoir" reading |
| 7. Align README, ROADMAP, code_review.md | done for S1, S1b, S3, S4, S6d, S6e; review table has a status column | — | S2c (not rerun) |
| 8a. More seeds (S2b) | replicate with 120 new units: G0, G1, G3, G4 replicate; **G2 and the gate do not** (AUC 0.46 [0.35, 0.62] against 0.76) | The S2b claim "at a long lag C rates rocks higher" is not robust, and the gate that made a dissipation term mandatory rests on one draw (README and ROADMAP updated). | S6c with more seeds (180 runs) does not fit on this machine in one night |
| 8b. Half dt | S3 at dt 0.025: all verdicts hold, VoI +1.262 against +1.265. S2 and S2b at dt 0.005: all verdicts hold, the S2b gate included. | S2, S2b and S3 do not depend on the step. With 8a: the S2b gate depends on the draw of units, not on the step. | — (flux ratio change: −0.08 in S2, −0.01 in S2b, both "small") |
| 8c. Tests | 13 new tests for functions without one, plus tests for the night's new code: 75 tests pass | — | — |

Problems during the night: S6d main was stopped once by the 2-hour background limit (resumed from the saved runs); one
commit (6efebe1) was made with a failing test, fixed in the next commit (b678207). Details below.

Branch `review-fixes` only. One round every 15 minutes (cron at minutes 7, 22, 37, 52). Plan and rules: the night
instructions; experiment rules go in the step documents before each run (phase C: docs/RERUN.md).

## Choices made without asking
- 23:55 The night list says "the other 8 settings of S1". τ 0.5 and τ 2 were already redone from the `_v2` data in
  phase C (C2b), so 6 settings remain: p_out 0.2, N 5, D2, D3, N 7, p_out 0.01. Run order: shortest first, so that most
  settings are done even if a long one fails.
- 23:55 Run logs are written to the scratchpad while a run is going and copied to `results/` when it ends, so the
  15-minute commits do not catch half-written logs.

- 23:53 D1 (KSG test, a few minutes on one core) ran in parallel with the S1 run, because it is small; the S1 settings
  themselves run one at a time, as asked.
- 23:55 D1 says "adequate", so by its rule e6, e6b and e7 are not rerun for the estimator. e7 could still be redone on the
  corrected S1 data (S2c rules D3–D5), but it needs the e6/e6b data files, which are not on this machine; rerunning e6 and
  e6b (same seeds, about 30 min) only to feed e7 is planned after the S1 settings, if time allows.
- 23:55 Phase E (S6d) needs long runs; the S1 settings use all cores until about 04:00–05:00. Prudent order: write the S6d
  rules and port the mutation to the numba version now (no long CPU use), run the short mutation check, and start the
  long S6d runs only when the S1 settings are done.
- 00:09 Item 8c (tests for functions without a test) was done early, while the S1 runs use the cores: it needs
  almost no CPU and changes no result. 13 new tests, all pass (73 in total). The bridge test also showed the
  discrete-monitoring effect in the test's own simulated paths; the test accounts for it with the same 0.5826 shift.
- 01:22 Time plan. `_p0.01_v2` ends about 02:50. S6d main needs about 3.5 h on 4 cores, so S6d main would end about
  06:30 and S6e (item 6, about 15 min) might not fit before 07:00. Prudent order, so that every list item gets a result:
  S6d B1 (10 min), then S6e (15 min), then S6d main. S6d main is stopped at about 06:40 if it is not done; its rule
  (docs/S6.md, S6d) already says that the finished runs are then analysed and their number reported.
- 04:07 S6d main is slower at the higher μ (17 of 32 after 102 min); end now about 05:40. After it, in this order:
  8b S3 (about 5–10 min), 8a S2b new units (15–25 min), and 8b S2/S2b at dt 0.005 (40–80 min) only if it can end before
  about 06:45. Reason: keep the final report and the PR update before 07:00, and run the cheapest checks first.
- 04:28 **Failure 1 of S6d main:** stopped at 04:25 by the 2-hour limit of background jobs. My mistake: I asked for
  a longer limit than the tool allows. 20 of 32 runs were saved in the pkl (μ 0.057: 8, 0.114: 8, 0.171: 4); the 4 runs
  in progress were lost. Choice: resume (S6d is list item 4, before item 8), with a new `--resume` option that keeps the
  saved runs and runs the 12 missing seeds (estimate 80–90 min, end about 06:00). If it fails again, the 20 runs are
  analysed, as the S6d rule allows.
- 04:28 **Rule broken:** commit 6efebe1 was made with one failing test. The test command was piped into `tail`,
  so its exit code did not stop the commit. The next commit (b678207) fixed the code; all 75 tests pass. From now on the
  test exit code is checked before every code commit.
- 05:58 New estimate for 8b S2/S2b at dt 0.005, from tonight's speed (this machine is about twice as fast as the one
  of the S2 runs): e6 10–15 min, e6b about 15 min. Both can end about 06:30, so they run now, e6 first; e6b only if e6
  ends before 06:35.

## Rounds
| Time (UTC) | Finished | Running | Next |
|---|---|---|---|
| 23:55 | Phase C points 1–4 (before the night). C5 rules written (docs/RERUN.md). | — | C5: `_p0.2_v2` (estimate 15–25 min), then N 5, D2, D3, N 7, p_out 0.01 |
| 23:55 | D1 (KSG adequate). e6/e6b/e7 options for more pairs and tags (tested). | `_p0.2_v2` (E3 + E4) | phase E preparation: S6d rules, mutation in grayscott2 (numba), short check |
| 00:03 | `_p0.2_v2` (451 s). S6d rules, numba mutation port, M0 check (as set: 0.237 [0.181, 0.303] at μ = 0.2). S6e rules and script. Item 5 rules. | `_N5_v2` | `_D2_v2`, `_D3_v2`, `_N7_v2`, `_p0.01_v2`; then S6d B1 and main |
| 00:04 | — | `_N5_v2` (E3 at world 83 of 90) | E4 for N 5, then `_D2_v2` |
| 00:06 | `_N5_v2` (420 s), committed | `_D2_v2` | `_D3_v2`, `_N7_v2`, `_p0.01_v2` |
| 00:07 | — | `_D2_v2` (E3 at world 5 of 90) | `_D3_v2`, `_N7_v2`, `_p0.01_v2` |
| 00:09 | item 8c tests (13 new, 73 pass) | `_D2_v2` | `_D3_v2`, `_N7_v2`, `_p0.01_v2` |
| 00:22 | — | `_D2_v2` (E3 at world 87 of 90) | `_D3_v2` |
| 00:25 | `_D2_v2` (1122 s), committed | `_D3_v2` (estimate about 20 min) | `_N7_v2`, `_p0.01_v2` |
| 00:39 | c5_summary.py prepared | `_D3_v2` (E3 at world 48 of 90) | `_N7_v2`, `_p0.01_v2` |
| 00:47 | `_D3_v2` (1281 s), committed | `_N7_v2` (estimate 40–80 min: old 11678 s times the ratios 0.19–0.41 measured tonight) | `_p0.01_v2`, then S6d |
| 00:52 | — | `_N7_v2` (E3 at world 13 of 90, about 35 min in total at this pace) | `_p0.01_v2`, then S6d B1 and main |
| 01:07 | — | `_N7_v2` (E3 at world 53 of 90) | `_p0.01_v2`, then S6d B1 and main |
| 01:21 | `_N7_v2` (2005 s, E3 + E4; E4 has 61,740 merge pairs with N 7), committed | `_p0.01_v2` (estimate 40–80 min) | then all C5 analyses; S6d B1 and main |
| 01:22 | — | `_p0.01_v2` (E3 at world 2 of 90, about 85 min) | C5 analyses; S6d B1, S6e, S6d main |
| 01:38 | — | `_p0.01_v2` (E3 at world 27 of 90; end about 02:25) | C5 analyses; S6d B1, S6e, S6d main |
| 01:52 | — | `_p0.01_v2` (E3 at world 56 of 90) | C5 analyses; S6d B1, S6e, S6d main |
| 02:08 | — | `_p0.01_v2` (E3 at world 83 of 90) | C5 analyses; S6d B1, S6e, S6d main |
| 02:17 | `_p0.01_v2` (3182 s). **List item 2 done**: C5 rules on all 9 settings (W1–W3, W5 as expected; H1 also supported at D-test r 2). **List item 5 done** (P5): little of the D-test shift and of the S3 VoI came from the dt bias. | S6d B1 (4 runs, 300 × 300) | S6e, then S6d main |
| 02:18 | S6d B1: consistent with S6c (f 0.598 against 0.579; mutation 0.112), 173 s | S6e (8 runs; estimate 5–15 min) | S6d main (32 runs at 600 × 600; new estimate about 2 h from the B1 speed) |
| 02:23 | README and ROADMAP updated for the 9 corrected S1 settings (item 7, part) | S6e; an agent updates S1, S1b, S4, RESULTS docs (no commit until reviewed) | S6d main |
| 02:25 | **List item 6 done**: S6e, edge hypothesis not supported (X1 0.57, X2 0.32: type A is inside the colony) | S6d main (32 runs, 600 × 600; estimate about 3 h, end about 05:30) | review the agent's doc edits; item 7 rest |
| 02:28 | S1, S1b, S4, RESULTS updated for the 9 corrected settings (agent, reviewed) | S6d main | item 7: code_review.md and the S6 parts after S6d |
| 02:38 | code_review.md: status column in the summary table | S6d main (no run finished yet; first batch of 4 expected about 02:50) | item 7: S6 numbers after S6d |
| 02:55 | rules for 8a and 8b; dt option for S2/S3 scripts (tested) | S6d main (4 of 32 done at 02:52; end about 04:55) | after S6d: 8a S2b seed 2027, 8b S3 dt 0.025, S2/S2b dt 0.005 |
| 03:07 | — | S6d main (8 of 32 done, 2030 s; end about 04:50) | 8a, 8b |
| 03:22 | — | S6d main (10 of 32 done, 3391 s; at this pace end about 05:30) | 8a, 8b (about 1 h together) |
| 03:37 | — | S6d main (12 of 32 done, 3686 s) | 8a, 8b |
| 03:52 | — | S6d main (16 of 32 done, 5054 s; end about 05:15) | 8a, 8b |
| 04:07 | — | S6d main (17 of 32 done, 6104 s; end about 05:40) | 8b S3, 8a, then 8b S2 if time allows |
| 04:22 | — | S6d main (20 of 32 done, 6727 s) | 8b S3, 8a, 8b S2 if time allows |
| 04:28 | S6d main stopped by the time limit (20 of 32 saved); resume option (tested) | S6d resume (12 runs) | 8b S3, 8a, 8b S2 only if time allows |
| 04:37 | — | S6d resume (12 runs, first batch running) | 8b S3, 8a |
| 04:52 | — | S6d resume (22 of 32 in the pkl; end about 06:15–06:30) | when cores free up: 8b S3; 8a and 8b S2 probably do not fit before 07:00 |
| 05:07 | — | S6d resume (24 of 32 in the pkl; 8 left at μ 0.228, end about 06:20) | S6d analysis; 8b S3 if it fits; final table |
| 05:23 | — | S6d resume (28 of 32; last 4 runs, end about 05:55) | S6d analysis, 8b S3, then 8a if it ends before about 06:45 |
| 05:37 | — | S6d resume (28 of 32; last 4 running) | S6d analysis, 8b S3, final table |
| 05:46 | **List item 4 done**: S6d (32 colonies): f falls above μ_c with twice the generations (0.27 → 0.16 at 2 μ_c), holds below; threshold not sharper | 8b S3 at dt 0.025 | final table, PR |
| 05:52 | 8b S3 at dt 0.025: all verdicts hold, VoI +1.262 against +1.265 | 8a S2b with new units (seed 2027; estimate 15–25 min) | 8b S2 at dt 0.005 does not fit before 07:00 (40–80 min): not run; final table and PR |
| 05:53 | — | 8a S2b seed 2027 (V phase) | 8a C phase; complete the summary; PR |
| 05:58 | **8a done**: S2b replicate, G2 and the gate do not replicate | — | update PR; stop at 07:00 |
| 06:07 | — | 8b e6 at dt 0.005 (no output yet) | e6b at dt 0.005 if e6 ends before 06:35; PR; stop at 07:00 |
| 06:16 | 8b S2 at dt 0.005: all verdicts hold (936 s) | 8b S2b at dt 0.005 (estimate 15–25 min) | PR; stop at 07:00 |
| 06:23 | — | 8b e6b at dt 0.005 (V phase) | if it ends before 07:00: record it; else stop it and note it; final commit |
| 06:28 | 8b S2b at dt 0.005: all verdicts hold. **List done**; item 8d: nothing useful left to run, so the night ends here (no runs only to keep the machine busy). | — | — |
