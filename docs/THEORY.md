# Theory notes (what we claim, what we test, what we do not)

Citation convention: `[Key]` → `REFERENCES.md`; `[N]` → not found in the literature by the authors (needs a check);
`[H]` → project hypothesis. Status of every formula: `PROVENANCE.md`.

## 0. The claim being tested

"Telos" can mean three different things. We keep them separate:

- **T1 — selection effect.** Structures that persist are the ones observed. This is teleonomy in the sense of
  [Pittendrigh58, Mayr74]. Almost a tautology unless "persist" is given a dynamical meaning.
- **T2 — variational postulate.** Organisations extremise a functional Φ. [H] (the original proposal).
- **T3 — arrow of organisation.** Along a selection process, an organisational score tends not to decrease and new
  levels of organisation form when merging is super-additive. [N] (framing).

For context: equilibrium has a Lyapunov functional (free energy; textbook); the linear regime of irreversible
thermodynamics has one (minimum entropy production, [Prigogine55]); replicator dynamics have one (relative entropy /
Fisher's theorem, [Fisher30, Price72, HofbauerSigmund98]); far from equilibrium there is in general none. T3 asks whether a
Lyapunov-like functional exists **at the level of organisations**.

**Strategy (Option B).** Do not postulate Φ. Define a physical viability V from the dynamics alone (no information
theory), then test whether information functionals predict V. If they do, Φ-maximisation is "what survival selection
looks like in information variables", and T3 becomes a consequence rather than a postulate. If they do not, Φ is
the wrong functional, which is also a result.

## 1. Changes relative to the original proposal

| Original | Problem (measured in E0 / reasoned) | Here |
|---|---|---|
| Exogenous environment E_t | contradicts "no organism/environment split"; E Markov ⇒ A holds no model of it (partial corr. = 0) | environment = complement Ω∖A |
| A = mean of a subset | collapses state, noise-averages | full joint state; closed-form Gaussian MI |
| MI in nats, K in bits | β, λ meaningless | everything in nats |
| i.i.d. binned estimator on autocorrelated series | bias, N_eff ≈ 76 of 3000 | exact Gaussian; KSG for validation |
| Argmax of one Φ | arbitrary (β, λ); no outcome measure | regress a physical V on features; fitted weights |
| "No organism hard-coded" | planted block is recovered even without the drive | tested against a viability measure instead |
| Replication as degenerate maxima | symmetry, not heredity | parked (ROADMAP); only merge/split criterion kept |

## 2. The microscopic ensemble

Worlds are stationary OU processes  dx = −Bx dt + √(2D) dW  with D = I, B = B_s + G, B_s symmetric positive definite,
G antisymmetric [Gardiner04, Risken89]. Stationary covariance S solves BS + SBᵀ = 2D; lagged covariance C(τ) = e^{−Bτ}S.

*Entropy production (derivation).* Stationary probability current J = −Bx·p − D∇p, evaluated for p ∝ exp(−½xᵀS⁻¹x):
J = −Mx p with M = B − DS⁻¹. Then σ = ∫ Jᵀ D⁻¹ J / p dx = tr(MᵀD⁻¹MS). σ = 0 ⇔ M = 0 ⇔ detailed balance
[general form: Tome06, SpinneyFord12].

*Equilibrium counterpart.* B_eq = DS⁻¹ has the same stationary law and σ = 0. Comparing V under B and under B_eq isolates
what irreversibility does to persistence **at fixed static statistics** [non-reversible diffusion literature:
HwangHwangMaSheu93/05, LelievreNierPavliotis13; use for exit times of structures: N].

## 3. Structures, features, Φ

A *structure* is a subset A ⊂ {1..N}, A ≠ ∅, A ≠ Ω; X = Ω∖A. With lag τ:

- C = I(A_t; A_{t+τ})  [H]
- P = I(A_t; X_{t+τ})  [H; cf. BialekNemenmanTishby01]
- IAX = I(A_t; X_t),  IAX − P = "non-predictive information" [Still12 — **analogy only**, exogenous-signal assumption violated]  [X]
- K_H = h(A_t)  [H]
- leak = I(A_{t+τ}; X_t | A_t) (one-step transfer entropy X→A, [Schreiber00]); closure idea [BertschingerOlbrichAyJost08]  [A]
- Φ_orig = P + βC − λK_H, β = 1, λ = 0.25 as in the original  [H]

All are exact for Gaussians [CoverThomas06].

## 4. Viability

Viability set V_A = {x_A : x_Aᵀ S_A⁻¹ x_A < χ²_{k, 1−p_out}} (stationary occupancy 1 − p_out for every k).
V(A) = mean first-passage time out of V_A from the stationary law conditioned on V_A [MFPT: PontryaginAndronovVitt33,
Gardiner04 ch.5, Redner01; viability language: Aubin91; this operationalisation: N].
Validated in `tests/test_viability.py` against the 1-D backward equation (with the discrete-monitoring shift
[BroadieGlassermanKou97]).

*Flux ratio* R = V_driven / V_eq [N]. In the equilibrium family R = 1 by construction (control).

## 5. Pre-registered hypotheses (written before looking at E3/E4 results)

- **H1.** Mean within-world Spearman correlation between Φ_orig and log V is > 0 (CI excludes 0).
- **H2.** In the regression of within-world-demeaned log V on standardised (P, C, K_H, IAX) the signs are +, +, −, ? and
  agree across the three families. *If instead P's coefficient is ≤ 0 this does not refute the thermodynamic idea; it
  indicates that in a passive linear world information about the environment has no viability payoff, because nothing
  uses it (no action loop).* Background: a successful regulator can reduce I(output; disturbance) while holding the
  information in an internal state [ConantAshby70, TouchetteLloyd00].
- **H3.** log R ≈ 0 in the equilibrium family (control); in driven families R ≠ 1 and is explained by features.
- **H4 (merging).** ΔΦ = Φ(A∪B) − Φ(A) − Φ(B) predicts survival synergy S beyond the static dependence I(A;B).
  Identity: h(A∪B) = h(A)+h(B) − I(A;B) ⇒ ΔΦ = (ΔP + βΔC) + λ I(A;B) [CoverThomas06; use: N].

*Falsifiers.* H1 fails if the CI includes 0 or is negative. H2 fails if signs are family-dependent. H4 fails if I(A;B)
alone predicts S as well as ΔΦ.

## 6. Instruments from "option A"

**GIB ladder.** For jointly Gaussian (X,Y) the information-bottleneck optimum is linear and new modes switch on at
β_i^c = 1/(1−λ_i), λ_i eigenvalues of S_{x|y}S_x⁻¹ [Chechik05, Tishby99]. We verify numerically that the analytic solution
equals the optimum found by direct minimisation (tests). Interpretation: complexity (number of effective degrees of
freedom) appears at discrete critical trade-offs, a genuine bifurcation sequence of a variational problem.

**GIB ≡ TICA when C(τ) is symmetric (short proof).** GIB directions v satisfy v ᵀ C S⁻¹ C = (1−λ) vᵀ S, i.e. (transposing,
C symmetric) C S⁻¹ C v = (1−λ) S v. TICA solves C v = μ S v, hence C S⁻¹ C v = μ² S v. Same eigenvectors, with 1 − λ = μ².
For the equilibrium family (B symmetric, D = I) C(τ) = e^{−Bτ}B⁻¹ is symmetric. For driven worlds C is not symmetric and
the two subspaces separate (E2 measures the gap). [Hotelling36 for the CCA fact; WuNoe20 for the non-reversible
generalisation context; the measurement of the gap as an irreversibility indicator: N, an observation not a theorem.]

## 7. Price-equation link (T3)

w̄ Δz̄ = Cov(w, z) + E[w Δz]  [Price70, Price72, Frank95]. With z = organisational score and w = viability, the
**selection term** Cov(w, z) ≥ 0 is what H1 measures. The **transmission term** requires heredity (parent→offspring
organisation) and is **not** measured here. So T3 is tested only in its selection half. Using the covariance over
structures of a single world as a descriptive statistic is a loose usage [N/X] because those structures do not reproduce.

## 8. Not addressed (on purpose)

Heredity, action–perception loops with value of information, hidden-state environments, non-linear metastability
("rocks" with many stable states), non-Gaussian estimation at scale. See LIMITATIONS.md and ROADMAP.md.
