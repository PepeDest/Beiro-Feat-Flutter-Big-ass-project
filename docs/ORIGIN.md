# Origin: what this project started from, and how it got here

This file makes the zip self-contained. It condenses the original proposal and the discussion that shaped the project, so
nobody needs the chat history. (Condensed, not verbatim; the original script is in `legacy/`.)

## 1. The original proposal ("Toward a Variational Theory of Life")
- Start from microscopic degrees of freedom Ω = {x_1…x_N} with stochastic dynamics U_t and an external stochastic process E_t. No cells, genes or replication rules.
- *Individuality is emergent.* Boundaries should be **discovered, not imposed**: score every candidate subset A ⊂ Ω.
- Three quantities: coherence C(A) = I(A_t; A_{t+1}); predictive information P(A) = I(A_t; E_{t+1}); complexity K(A) = H(A_t).
- Organisational functional **Φ(A) = P + β·C − λ·K**; an organism is **A\* = argmax Φ**.
- *Replication* conjectured as a bifurcation A\*(μ) → A₁\* ∪ A₂\* as a resource parameter μ varies ("what is reproduced is organisation, not matter").
- Long-term aim: a renormalisation-group description of life; life as stable extrema of an organisational functional.
- The original code: 8 variables, block-structured coupling, an AR(1) environment driving variables 0–2, all 255 subsets scored on the subset *mean*.

## 2. The commentary that added ideas (chat, "document 3")
- Life propagates attractors; crystals grow a pattern, cells copy a process ("reproducer(A) → reproducer(A) + reproducer(A)").
- Replication as an invariance: R(L) ≈ L + L; life as an "eigenvector of reproduction".
- Once cells replicate, descendants become part of each other's environment.
- Two interacting cells can become a higher-level entity C when C predicts better than A and B separately (topological boundary in interaction space); recursion gives tissues, organisms, societies.
- "Telos" as a tendency toward larger coherent wholes; "life = propagation of effective theories".
- Our assessment: good intuitions, loose algebra. R(L) ≈ L + L is a doubling relation, not an eigenvalue problem (the right object is a population operator with a Perron–Frobenius mode); the crystal/cell distinction is better stated as exponential vs polynomial growth plus unlimited heredity.

## 3. Review findings that changed the plan (experiment E0 reproduces them)
1. The "discovered" organism is the planted structure: the winning block {0,1,2} wins even with the environmental drive removed (its coupling block is supercritical, gain 1.083).
2. E is Markov, so A holds no information about E_{t+1} beyond E_t (partial correlation 0.000): A is a lossy thermometer, not a model.
3. Mutual information in nats, entropy in bits: β and λ mixed units.
4. Binned MI on an autocorrelated series (effective N ≈ 76 of 3000) is biased.
5. C ≤ H means a bank of stable bits (a "rock") maximises C − λK: persistence is not self-maintenance.
6. Replication as "two equal maxima" is symmetry, not heredity.

## 4. The reframing: three meanings of telos
- **T1** selection effect (teleonomy). **T2** variational postulate (Φ is extremised). **T3** arrow of organisation (a Lyapunov-like functional at the level of organisations).
- Decision: **T3 is the claim; Option B is the method.** Option B: define a physical viability V from dynamics alone, then *test* whether Φ's terms predict V. Option A ideas (slow variables, Gaussian predictive bottleneck, thermodynamic cost of prediction) are kept as **instruments**, not as justification.
- The Price equation gives T3 its formal shape: selection term Cov(w, z) (measured here) plus transmission term E[wΔz] (needs heredity; not measured).

## 5. Decisions taken (decision log)
| Decision | Choice | Why |
|---|---|---|
| Viability definition | **mean first-passage time** out of a stationary-occupancy-matched Mahalanobis ball | clean, physical, no information theory; growth rate needs birth/death rules = more assumptions |
| Growth-rate viability | left as an extension point (`GrowthRateViability`, `price.py`) | requested: "leave tracks"; needs heredity |
| Citations | every formula tagged or flagged novel | requested; `PROVENANCE.md` |
| Scope | linear-Gaussian worlds first | exact information terms validate machinery before nonlinear estimation |
| Environment | complement Ω∖A, not an exogenous process | removes an internal contradiction of the proposal |
| Replication | parked; only merge/split (ΔΦ) kept | needs heredity, a separate ingredient |

## 6. What the first full run found (summary; details `RESULTS.md`)
The original Φ does not rank structures by viability in passive linear worlds (pooled ρ = −0.08); persistence C does
(+0.55 among equal-size structures); P has a small positive partial effect; the Φ merge criterion fails against static
dependence. A negative result for this functional in this ensemble; action, nonlinearity and heredity untested.
