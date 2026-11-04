# Night log (unsupervised work, 2026-11-04 23:50 UTC to 2026-11-05 07:00 UTC)

Branch `review-fixes` only. One round every 15 minutes (cron at minutes 7, 22, 37, 52). Plan and rules: the night
instructions; experiment rules go in the step documents before each run (phase C: docs/RERUN.md).

## Choices made without asking
- 23:55 The night list says "the other 8 settings of S1". τ 0.5 and τ 2 were already redone from the `_v2` data in
  phase C (C2b), so 6 settings remain: p_out 0.2, N 5, D2, D3, N 7, p_out 0.01. Run order: shortest first, so that most
  settings are done even if a long one fails.
- 23:55 Run logs are written to the scratchpad while a run is going and copied to `results/` when it ends, so the
  15-minute commits do not catch half-written logs.

## Rounds
| Time (UTC) | Finished | Running | Next |
|---|---|---|---|
| 23:55 | Phase C points 1–4 (before the night). C5 rules written (docs/RERUN.md). | — | C5: `_p0.2_v2` (estimate 15–25 min), then N 5, D2, D3, N 7, p_out 0.01 |
