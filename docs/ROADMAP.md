# Roadmap: next natural steps (ordered by what the results taught us)

Where we stand (`RESULTS.md`): in passive linear-Gaussian worlds the original Φ does not predict MFPT viability, persistence
(C) does, P has a small positive effect, and the merge criterion fails. The open question is therefore **not** "tune β, λ" but
"in which regimes does information pay?". Steps are ordered so that each one either hardens the current result or tests a
specific explanation of it. Each has a goal, deliverables, an acceptance criterion and a decision gate.

Conventions: new experiments go in `experiments/eN_*.py`, write to `results/`, and add rows to `PROVENANCE.md`; new
formulas need a `[Key]` or a novel/hypothesis flag (`REFERENCES.md`).

---
## S0. Verify and reproduce (½ day)
- Look up every entry in `REFERENCES.md` (DOI check); fix errors; upgrade each "N" in `PROVENANCE.md` after a real literature search.
- Re-run `python experiments/run_all.py` and confirm numbers in `RESULTS.md` (seed 2026).
- **Done when** every reference is checked and the novelty column reflects a documented search.
- **Status (2026-10-21): done, with limits.**
  - All 62 references were checked against Crossref and now carry a DOI. No bibliographic error was found. One citation key was misspelled and is now fixed.
  - The full rerun reproduces `RESULTS.md` (largest change 0.003).
  - The novelty search was limited (see the log in `PROVENANCE.md`). Row 20 changed from N to A. Rows 7, 8, 21, 22, 34 and 35 are not searched yet.

## S1. Harden the negative result (1–2 days, mostly compute)
Goal: show H1/H4 failures are not artefacts of τ, p_out, N or ensemble.
- Sweep τ ∈ {0.5, 1, 2}, p_out ∈ {0.01, 0.05, 0.2}, N ∈ {5, 6, 7} using the tag option:
  `python experiments/e3_phi_vs_viability.py --tau 0.5 --p_out 0.05 --tag _tau0.5 --n_worlds 30 --n_traj 600 --t_max 200`
  (≈ 25–40 min per setting on one CPU; N needs a `--N` flag, to be added).
- Optional, zero new simulation: add difference-style scores (e.g. C − leak, C − P) and rescaled/intensive K to `analyse()`.
- Test the D = I confound: draw D diagonal with log-uniform entries so variance no longer tracks timescale; check whether K_H's sign behaviour changes.
- **Done when** a table shows each verdict (H1–H4) per setting. **Gate:** if H1 flips sign under any reasonable setting, the "negative result" is ensemble-dependent and must be reported as such.
- **Status (2026-10-21): done** for one-at-a-time changes of τ, p_out and N, plus the D-test. See `docs/S1.md`.
  - **The gate triggered.** H1 is supported at τ = 0.5 and in the D-test with r = 3.
  - C predicts viability in every setting. H4 fails in every setting.
  - The D-test supports the D = I confound for K_H.
  - Open: the full grid, the difference scores and an intensive K.

## S2. Flux-cut test (physical discriminator, ~1 week) — Track N, part 1
Goal: separate dissipative persistence from equilibrium memory, the distinction Φ cannot currently see.
- Add non-linear units (bistable cubic/tanh with a pitchfork parameter; noisy limit cycle via Stuart–Landau).
- Define V_on / V_off where "off" removes the non-conservative drive (not merely the reversible counterpart used now).
- Expect: equilibrium "rocks" (bistable banks) have high C, V_on/V_off ≈ 1; driven oscillators have V_on/V_off ≫ 1.
- Information terms need estimators here (KSG validated in E1; keep bias controls and surrogate nulls).
- **Done when** a scatter of C vs V_on/V_off shows whether C alone mislabels rocks. **Gate:** if rocks outrank oscillators by C and by Φ, add a dissipation term (entropy production restricted to the structure, cf. Spinney & Ford 2012) to the functional and re-test.

## S3. Information that is used: agency + hidden-state environment (~2 weeks) — Track A
Goal: test the explanation offered for P's small effect ("information only pays when used").
- Environment: a hidden Markov regime (e.g. two-state switching parameter) that changes where a structure's safe set lies.
- Structure: sensor + internal state + actuator coupled to a viability variable (a minimal homeostat).
- Viability: MFPT out of its viability set (unchanged definition, so results stay comparable).
- Value of information by intervention: scramble the sensor→actuator link and measure the drop in V (Kolchinsky & Wolpert 2018 idea; adaptation to this setting: N).
- Compare P, C, leak, and the scramble-based value across structures; include the good-regulator caveat (a perfect regulator may *lower* I(output; disturbance) while storing it internally: Conant & Ashby 1970, Touchette & Lloyd 2000).
- **Done when** P's partial effect on V is shown to depend on the feedback loop (present vs scrambled). **Gate (key decision):** if P stays ≈ 0 with a working feedback loop, the predictive term of Φ is not what drives viability; redesign Φ around closure/autonomy (leak, blanket) or drop T2.

## S4. Growth-rate viability (~1 week; needs an offspring map) — Track G
- Implement `GrowthRateViability`: death hazard = 1/MFPT; birth rate from resources; solve Euler–Lotka or the Leslie/projection dominant eigenvalue.
- Swap it into E3 behind the `ViabilityMeasure` interface; compare rankings with MFPT.
- Use `price_decomposition` with explicit parent→offspring traits to measure the **transmission term**.
- **Done when** r and MFPT rankings are compared and the transmission term is estimated. **Gate:** if they disagree strongly, report which better tracks persistence under perturbation.

## S5. Boundaries by conditional independence (~2 weeks) — Track B
- Replace subsets by partitions (interior, blanket, exterior) with I(interior; exterior | blanket) ≈ 0 (Pearl 1988; Friston 2013).
- Candidate generation by slow modes (E2 tools) to scale beyond N ≈ 20; add greedy/spectral search; test submodularity assumptions before relying on them.
- **Done when** boundary discovery recovers planted structures in a world where the answer is *not* encoded in the drive (the failure of the original E0).

## S6. Heredity and replication (open-ended) — Track H
- Needs S3–S5. Physical test beds with real division: Gray–Scott spots (Pearson 1993), active droplets (Zwicker et al. 2017).
- Measure: splitting as ΔΦ < 0 (or the successor functional), parent→daughter information transmitted, copying fidelity vs the Eigen error threshold (Eigen 1971), exponential vs polynomial growth.
- **Done when** a measured heredity fidelity enters the Price transmission term, completing T3.

---
## Dependencies
S0 → everything (credibility). S1 independent. S2 and S3 independent of each other; both precede S6. S4 needs an offspring map (could start with S6's simplest case). S5 can run in parallel.

## Decision points that can change the whole programme
1. After S1: is the negative result robust? If not, revise claims before building further.
2. After S3: does P matter once information is used? If no, redefine Φ (closure/autonomy-based) rather than tune weights.
3. After S2: does C mislabel equilibrium memory? If yes, a dissipation term is mandatory, not optional.
4. After S4/S6: is there a measurable transmission term? Without it, T3 remains half-tested (selection only).

## What would count as support for T3
Φ-like scores predict viability **and** the effect survives (i) the flux cut (not mere memory), (ii) removal of the feedback loop's benefit (information is used), (iii) a positive Price selection term in most worlds, and (iv) a measured, nonzero transmission term. Anything less is partial support.

---
The status sections below are dated snapshots, written when each step ended. Some of their numbers changed after
the code review. The current state is in the last section, "Where the programme stands".

## Status of S3 (2026-10-22)
Done for a linear homeostat with a Gaussian hidden state (docs/S3.md). Information is used (mean VoI +1.27). P's effect
depends on the loop (β_P +0.75 intact against +0.38 scrambled). The gate is not triggered, so P stays in Φ.
Open: a two-state switching regime and other τ values. The lagged good-regulator test (S3b) is done: the pattern does not appear, and the R4 sign comes from the time scale of v.

## Status of S2 (2026-10-22)
Done with inertial units and active Rayleigh friction (docs/S2.md). The flux cut works (oscillators: V_on/V_off ≈ 5.5,
passive units exactly 1). C rates every oscillator above every rock, so the gate is not triggered. Post-hoc checks show
this rock class is a weak test: rock exits mostly avoid the barrier, and C at τ = 1 measures motion inside the well.
Open: a well-based viability set and C at longer τ.

## Status of S2b (2026-10-23)
Sharper rock test done (docs/S2.md, S2b). The gate triggers at a common long lag τ* (C AUC 0.76 rock > oscillator), so by
decision point 3 a dissipation term is needed. The trigger is weak: the rock signal is near the estimator noise, the Φ_TC
result comes from TC, and with each unit's own lag C favours oscillators. The flux ratio separates the classes cleanly.
Next: test a dissipation term (entropy production or drive power) in Φ.

## Status of the dissipation term (S2c, 2026-10-23)
Tested on existing data (docs/S2c.md). Dissipation tracks life among drive-sustained oscillators (+0.70). As a bonus in Φ
it hurts in linear worlds where the drive only stirs (−0.18 and −0.52), and its link to life changes sign with D.
So raw dissipation is not a good general term. The flux ratio separates the cases but needs a drive-off simulation.
Open: a closed-form term for "dissipation that sustains the structure".

## Status of S5 (2026-10-24)
Done for planted linear structures (docs/S5.md). Conditional independence recovers planted blankets (static and dynamic,
exact and finite) except the static detector in exact mode in driven worlds. The static blanket breaks down as the drive
grows (recovery 1.00 → 0.46 at drive × 4). The dynamic blanket stays exact. Φ_TC ranks planted structures at the bottom,
TC and closure at the top. Open: structures that are not denser than the background, search over sizes, slow-mode candidates.

## Status of S4 (2026-11-03)
Done with one birth rule for all structures (docs/S4.md). Lives are near exponential (CV 1.015), so r ranks structures like
V (ρ 0.90–0.99), and the gate does not trigger. The Price transmission term is measured with a random-swap offspring map:
small and negative in 98 % of worlds. Open: a birth rule from resources, and non-exponential lives (S2 units).

## Status of S6 (2026-11-04, first test bed)
Gray–Scott spots with a neutral dye (docs/S6.md). Spots replicate (4 → about 230). The dye gives a measured fidelity
(ρ = 0.975) that enters the Price transmission term, so the ROADMAP "done" criterion is met in form. But for a neutral
trait the selection term is +4.72, mostly from mixing generations (+0.47 within generations). So Price terms need
per-generation bookkeeping and a neutral control. The growth-law test does not discriminate in the window used.
Native heredity of spot size is weak (+0.17 at fixed time). Open: a trait that changes division (real selection), active droplets.

## Status of S6b (2026-11-04)
Two heritable types in Gray–Scott spots, type A divides 24 % faster (docs/S6.md, S6b). Fidelity 1.0000, selection term
+0.039 per generation (control −0.005, clean), type A rises to 72 % (control 50 %), Price identity exact to 1e-16, growth
polynomial (exponent 1.92). The transmission term is 0 because there is no mutation. Open: mutation and error threshold,
an organisational trait, active droplets.

## Status of S6c (2026-11-04)
One-way mutation A → B at division (docs/S6.md, S6c), 180 GPU runs. The mutation rate is as set. A nonzero transmission
term from copying errors is measured: it matches the mutation rate within about 3 % when it counts all daughters (the
pre-registered version, dividing daughters only, is 50–60 % of it, so M2 failed). No sharp error threshold: the fraction
of the faster type falls smoothly and crosses 0.1 at μ = 0.33, about 3 times the mean-field 0.114. A finite-time mean field
keeps much less of the faster type than the colonies do, so space appears to protect it (not tested).

## Where the programme stands (2026-11-11)
All seven steps S0–S6 have results. Every step that the code review touched was run again with the corrected code
(`docs/code_review.md`, `docs/RERUN.md`, `docs/night_log.md`, and S6f in `docs/S6.md`). The four conditions of
"What would count as support for T3":
1. **Φ-like scores predict viability: in part.** P + C − 0.25·TC and C alone predict life in all 9 S1 settings (S1, S1b).
   Φ_orig predicts life in 3 of 9 settings only (τ 0.5 and the two D-test settings). The flux cut separates
   drive-sustained structures from passive ones (S2). C alone does not: at a long lag it rates passive rocks slightly
   above oscillators (AUC 0.57 [0.51, 0.65] over 7 draws of units, a weak effect). A raw dissipation term is not a fix: it tracks life among oscillators, but as a bonus in Φ it hurts in linear worlds
   (S2c, also on the corrected data).
2. **Information that is used pays: yes.** Breaking the sensor–actuator link shortens life about 3.5 times (S3, VoI
   +1.27). The result is the same at half the step.
3. **A positive Price selection term: yes.** In spot colonies with a heritable type that divides faster (S6b, +0.04 per
   generation, the same with the corrected GPU noise), and for Φ_TC in linear worlds with a common birth rule (S4).
4. **A measured, nonzero transmission term: yes.** With one-way mutation at division, the term matches the mutation rate
   (S6c, S6d).

So T3 has partial support: conditions 2, 3 and 4 hold, condition 1 holds in part.

Open questions:
- No single score is right in all test beds. The best candidate, P + C − 0.25·TC, is tested in linear worlds only.
- Why does the faster type survive better than a mean-field model predicts? It does not stay at the colony edge (S6e).
- Is there an error threshold with many more generations (a larger grid, or colonies with removal of spots)?
- A term for "dissipation that builds the structure" that does not need a drive-off simulation.
