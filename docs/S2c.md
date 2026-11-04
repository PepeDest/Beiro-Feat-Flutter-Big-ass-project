# S2c: a dissipation term in Φ

This file was written on 2026-10-23, **before** any S2c code or result existed. The results section at the end was added after the analysis.

## Why
S2b triggered the ROADMAP gate: at a long lag, C rates passive rocks above drive-sustained oscillators. Decision point 3
says that Φ then needs a dissipation term. S2c tests such a term on data that already exist. No new simulation.

## Dissipation measures
- **Nonlinear units (S2, S2b).** In steady state the mean energy is constant. So the heat that flows into the bath equals
  the drive power: γ₀(⟨v²⟩ − T) = ⟨(α − βv²) v²⟩. The entropy production of the medium is then σ = drive power / T
  [standard stochastic energetics, SpinneyFord12]. σ = 0 for rocks and plain wells. A test checks the energy balance.
  Caveat: the energy depot is part of the model, so σ counts only the heat into the bath.
- **Linear worlds (S1).** For dx = −Bx dt + √(2D) dW with diagonal D, the total entropy production
  σ = tr(Mᵀ D⁻¹ M S), M = B − D S⁻¹, is a sum over coordinates: σ = Σᵢ (M S Mᵀ)ᵢᵢ / Dᵢᵢ. The part of the
  probability current along the coordinates of a structure A gives **σ_A = Σ_{i∈A} (M S Mᵀ)ᵢᵢ / Dᵢᵢ**.
  The decomposition is ours (simple algebra). A test checks that the sum over all coordinates equals entropy_production().

## Score with a dissipation term
Φ_D = Φ_TC + σ·τ. Here Φ_TC is the S1b score (C − 0.25 TC, plus P in linear worlds), and τ is the lag at which C is
measured. σ·τ is the entropy produced over one lag, in nats, so the term has the same unit as C. Weight 1, no tuning.
Rocks and plain wells have σ = 0, so Φ_D always puts every oscillator above every rock. **That is a check by
construction, not a test.** It is reported once.

## Rules (fixed before the analysis)
Bootstrap: 1000 resamples of units (S2, S2b) or 400 cluster resamples of worlds (S1).

| Rule | Data | Question | Verdict |
|---|---|---|---|
| D1 | S2b oscillators | Does more dissipation mean a longer drive-sustained life? ρ(σ, log V_on) | "yes" if CI low > 0, "no" if CI high < 0, else "no clear effect" |
| D2 | S2b oscillators | Does more dissipation mean more dependence on the drive? ρ(σ, log V_on/V_off) | same labels |
| D3 | S1 baseline, driven and modular worlds | Does the dissipation of a structure change its life? Mean within-world ρ(σ_A, log V), among structures of equal size | "shortens life" if CI high < 0, "lengthens life" if CI low > 0, else "no effect" |
| D4 | S1 baseline, driven and modular worlds | Does the term help Φ_TC there? Δρ = ρ(Φ_D, log V) − ρ(Φ_TC, log V), mean within world, all structures | "helps" if CI low > 0, "hurts" if CI high < 0, else "no effect" |
| D5 | S1 D-test r = 3, driven and modular worlds | D3 and D4 again, in worlds where variance and time scale are not tied | same labels as D3 and D4 |

Also reported (description only): D1 and D2 on S2 data (outer-edge viability), and the check by construction.

**Expectations written before the analysis.** D1 "yes" and D2 "yes": a stronger pump keeps a stronger cycle. D3
"shortens life": in S1 the flux shortened life by about 20 %. D4 "hurts". If D3 and D4 come out like this, raw dissipation
is not a good term: it helps where the drive builds the structure and hurts where the drive only stirs it.

## Results (added 2026-10-23, after the analysis)
Report: `results/e7_dissipation.md` (made by `experiments/e7_dissipation.py`). Tests for the energy balance and for the
σ_A sum pass.

| Rule | Data | Value [95% CI] | Verdict |
|---|---|---|---|
| D1: ρ(σ, log V_on), oscillators | S2b | +0.70 [+0.55, +0.80] | yes |
| D2: ρ(σ, log V_on/V_off), oscillators | S2b | +0.58 [+0.39, +0.71] | yes |
| D3: ρ(σ_A, log V), equal size | S1 baseline, 60 worlds | +0.10 [+0.01, +0.19] | lengthens life |
| D4: ρ(Φ_D) − ρ(Φ_TC) | S1 baseline | −0.18 [−0.23, −0.13] | hurts |
| D5 (D3) | S1 D-test r = 3, 60 worlds | −0.25 [−0.33, −0.16] | shortens life |
| D5 (D4) | S1 D-test r = 3 | −0.52 [−0.59, −0.46] | hurts |

Description only: on S2 data (outer-edge viability), ρ(σ, log V_on) = +0.36 and ρ(σ, log R) = +0.83. Median σ of the
oscillators is 9.5 per time unit. Check by construction: Φ_D puts every oscillator above every rock (AUC 0.00).

### The expectation was partly wrong
I expected D3 "shortens life" in the baseline. It came out "lengthens life" (+0.10, small). In the D-test worlds it is
"shortens life" (−0.25). So the sign of the link between dissipation and life depends on the noise structure D, as the
sign of K_H did in S1. I did not test why.

### What S2c shows
1. **Where the drive builds the structure, dissipation tracks life.** Among oscillators, more dissipation gives a longer
   life (+0.70) and a stronger dependence on the drive (+0.58).
2. **Where the drive only stirs a passive structure, a dissipation bonus hurts Φ.** In linear worlds, adding σ_A·τ to Φ_TC
   lowers its ranking quality in both settings (−0.18 and −0.52).
3. **Raw dissipation is not a good general term.** Its direct link to life changes sign with D in linear worlds, and as a
   bonus it hurts there.
4. **What the gate needs** is a term that separates "the drive builds the structure" from "the drive stirs it". The flux
   ratio log(V_on/V_off) does this by definition: +3.1 for oscillators in S2b, 0 for passive units. (In S1 a related
   ratio, a driven world against its reversible counterpart with the same stationary law, was about −0.2: there the drive
   shortened life.) But the flux ratio needs a second simulation with the drive off, so it is a test, not a closed-form term.

### Limits
- One nonlinear drive model. In it, σ counts only the heat into the bath, not the energy taken from the depot.
- σ_A is our decomposition of the linear entropy production. Other decompositions exist.
- The weight of the term (1) and the time unit (τ) are fixed choices, not tuned.
