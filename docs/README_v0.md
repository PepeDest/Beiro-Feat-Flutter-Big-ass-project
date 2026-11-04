# vlife — Variational Life Lab

A small, tested research code base asking one question:

> **Does an information-theoretic organisational functional Φ predict the *physical* viability of structures in a
> microscopic stochastic world?**  (If yes, "telos" becomes a consequence of survival selection; if no, Φ is the wrong functional.)

It replaces the original script's circular "discover the organism" demo with a falsifiable test: define viability from the
dynamics alone (mean first-passage time out of a structure's own viability set), compute information features in closed
form, and measure how well each predicts viability across an ensemble of random worlds.

**Headline result of the shipped run (see `docs/RESULTS.md`):** in passive linear-Gaussian worlds the original Φ does *not*
predict viability (pooled ρ = −0.08), persistence (C) does, and the Φ-based merge criterion fails. That is an honest negative
for this functional in this ensemble, not a refutation of the broader idea (action loops, nonlinearity and heredity are untested).

## Quick start
```bash
pip install -r requirements.txt && pip install -e .
pytest -q tests                              # 12 tests, ~3 s
python experiments/run_all.py --quick        # ~3 min sanity run (small ensemble)
python experiments/run_all.py                # full run, ~25-40 min on one CPU
```
Shipped `results/` come from the full run (seed 2026).

## Layout
| Path | What |
|---|---|
| `src/vlife/gaussian.py` | exact OU quantities: stationary/lagged covariance, MI, entropy, entropy production |
| `src/vlife/worlds.py` | random world ensemble (equilibrium / driven / modular-driven) |
| `src/vlife/functional.py` | structure features (P, C, K_H, IAX, leak) and Φ_orig |
| `src/vlife/viability.py` | **MFPT viability** (exact propagator, censoring-aware) + `GrowthRateViability` stub |
| `src/vlife/gib.py` | Gaussian information bottleneck ladder, slow modes (TICA) |
| `src/vlife/price.py` | Price-equation decomposition (selection vs transmission) |
| `src/vlife/estimators.py`, `stats.py` | KSG / binned MI, effective sample size, cluster bootstrap |
| `experiments/e0…e4` | audit of legacy code · estimator validation · GIB/slow modes · Φ vs viability · merging |
| `legacy/` | your original script (only print-string line breaks escaped) |
| `docs/ORIGIN.md` | **start here if new**: the original proposal, the review findings, T1–T3 framing, decision log (self-contained history) |
| `docs/THEORY.md` | formal statement, hypotheses (pre-registered), proofs/derivations |
| `docs/PROVENANCE.md` | **every formula: established / adapted / hypothesis / novel / analogy, with source** |
| `docs/REFERENCES.md` | bibliography (written from memory, **not machine-verified**) |
| `docs/RESULTS.md`, `LIMITATIONS.md` | results with verdicts · weak points |
| `docs/ROADMAP.md` | **ordered next steps S0–S6** with deliverables, acceptance criteria and decision gates (incl. growth-rate viability) |

## Reading order for a newcomer
1. `docs/ORIGIN.md` (where this came from), then `docs/THEORY.md` §0–1 (what is claimed, what changed).
2. `experiments/e0_audit_legacy.py` output (why the original was circular).
3. `docs/RESULTS.md` (what the test found), then `LIMITATIONS.md`.

## Citation policy
Every formula in code carries a `[Key]` tag resolved in `docs/REFERENCES.md`, or is flagged novel/hypothesis in
`docs/PROVENANCE.md`. "Novel" means *no source recalled*, not *searched and absent*; please verify before publishing.

## Next steps
See `docs/ROADMAP.md`. The most informative next experiment is S3 (give structures actuators and a hidden-state environment so information can be *used*); the cheapest is S1 (robustness sweeps; `e3_phi_vs_viability.py --tau … --p_out … --tag …`).
