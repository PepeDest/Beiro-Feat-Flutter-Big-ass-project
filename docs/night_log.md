# Night log (unsupervised work, 2026-11-04 23:50 UTC to 2026-11-05 07:00 UTC)

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
