# Niche H: the energy cost of semantic information in linear systems

This file starts on 2026-11-27. The plan is in `ROADMAP_DI.md`. Each step writes its rules before its runs, and the
results come after.

## H0. Literature check (2026-11-27)

**What we read.** The abstracts and the parts of the text that we name below. We did not read every proof.

| Source | What it gives us |
|---|---|
| KolchinskyWolpert18 (Interface Focus 8, 20180041) | Semantic information and the "thermodynamic multiplier" κ = (value of information) / (syntactic information). The paper defines κ for the stored case and gives an example (κ_stored ≈ 9.5 for a food-seeking agent). It does not compute the entropy production that pays for the observed information. |
| HorowitzEsposito14 (PRX 4, 031015) | Bipartite systems: the information flow İ^X and the second law of a subsystem. In the steady state, the heat rate of X (in units of k_B) is at least İ^X. |
| BaratoHartichSeifert14 (NJP 16, 103024) | The "learning rate" l_X: the rate at which the dynamics of X increase I(X; Y). In the steady state, l_X = İ^X. Efficiency η = l_X / (heat rate of X) ≤ 1. |
| HartichBaratoSeifert14 (J. Stat. Mech. P02016) | The information flow is at most the transfer entropy rate: l_X ≤ Ṫ_{Y→X}. |
| HartichBaratoSeifert16 (PRE 93, 022116) | Sensory capacity C = l_X / Ṫ_{Y→X} ≤ 1. If C = 1, then η ≤ 1/2. |
| MatsumotoSagawa18 (PRE 97, 042103) | A sufficient statistic gives C = 1. Example: a linear Langevin model of E. coli chemotaxis, with C near 1. |
| MatsumotoSasaDechant25 (arXiv 2504.09981) | A learning-rate matrix and a bound tighter than the second law. In the steady state, Eq. (49): heat rate of X ≥ l_X + l_X² / tr(D_X 𝓘_XX) + a mean-velocity term (zero here). 𝓘 is the Fisher information matrix. |
| NagayamaKolchinskyIto26 (arXiv 2606.07263) | The split of the entropy production of linear systems into an oscillatory part and a non-normal part. Used in niche A. |

**Search for prior work (2026-11-27).** We know of no paper that puts the observed semantic information of
KolchinskyWolpert18 next to the entropy production of the agent, in any model. This is a search result, not a proof.

**What we take from H0.**
1. The learning rate is the quantity that the second law prices. The transfer entropy rate is larger. The semantic
   information is a part of the transfer entropy. So the open question is where the semantic information falls
   relative to the learning rate and to the heat.
2. In linear systems with a diagonal noise matrix, all these quantities have closed forms (below, ours). We check each
   closed form with a second method.

## H1. Setting and closed forms (ours, written 2026-11-27, before the runs)

**System.** dz = −B z dt + √(2D) dW, with z = (y, x). y = h is a scalar environment that the agent does not change
(B_yx = 0). x is the agent with dx coordinates. D is diagonal, so the system is bipartite. Each coordinate i is an
overdamped degree of freedom with mobility 1 and temperature D_ii. This is an assumption: for the homeostat it gives
the "heat" a meaning only by analogy. S is the stationary covariance, M = B − D S⁻¹. All rates are in nats per unit
time.

**Thermodynamics (steady state).**
- Partial entropy production of coordinate i: σ_i = (M S Mᵀ)_ii / D_ii ≥ 0. σ = Σ_i σ_i (already in `gaussian.py`).
- Heat rate of coordinate i (entropy given to its bath): q_i = (B S Mᵀ)_ii / D_ii.
- Proof: q_i − σ_i = ((B − M) S Mᵀ)_ii / D_ii = M_ii. Also Σ_i M_ii = tr M = 0, because the Lyapunov equation
  B S + S Bᵀ = 2D, multiplied by S⁻¹ on the right, gives tr B = tr(D S⁻¹).
- Learning rate (information flow) of the agent: l_X = Σ_{i∈X} M_ii. Proof: J = −M z p and ∇ ln p = −S⁻¹ z give
  ∫ J_i ∂_i ln p dz = M_ii. The term with ln p(x) is zero in the steady state, so the sum over X is the flow of
  HorowitzEsposito14.
- Heat rate of the agent q_X = Σ_{i∈X} q_i = σ_X + l_X. So q_X ≥ l_X is the second law of the subsystem.
- A tighter form (our proof by Cauchy–Schwarz, the linear case of MatsumotoSasaDechant25, Eq. (49)):
  M_ii = E[(M z)_i (S⁻¹ z)_i], so l_X² ≤ σ_X · Σ_{i∈X} D_ii (S⁻¹)_ii, and q_X ≥ l_X + l_X² / Σ_{i∈X} D_ii (S⁻¹)_ii.

**Second method for l_X.** l_X = d/dτ I(X_{t+τ}; h_t) at τ = 0⁺, from C(τ) = [e^{−Bτ} S]_{X,h}: the derivative of
½ log det Σ_X − ½ log det(Σ_X − C Σ_h⁻¹ Cᵀ) with C' = [−B S]_{X,h}.

**Transfer entropy rate from h to the agent.** h does not depend on x, so the transfer entropy rate equals the
directed and the mutual information rate. Two methods:
- Kalman–Bucy filter (Duncan's theorem): with a = Σ_{i∈X} B_ih² / (2 D_ii), the stationary error variance P solves
  a P² + 2 B_hh P − 2 D_hh = 0, and Ṫ = ½ a P.
- Spectrum: Ṫ = (1/4π) ∫ log(1 + S_h(ω) gᴴ N⁻¹ g) dω, with g the response of x to h and N the noise spectrum of x.
  The factors (iω + B_xx) cancel, so gᴴ N⁻¹ g = a and Ṫ = ½ (√(B_hh² + 2 a D_hh) − B_hh).
- Consequence: Ṫ depends only on the direct pushes of h on the agent, not on the inner structure of the agent.

**The sensor channel.** Coordinate 0 of the agent is a pure sensor: ds = k (h − s) dt + √(2 d_s) dW, with no input from
other agent coordinates. Its information rate is İ_s = ½ (√(B_hh² + 2 a_s D_hh) − B_hh), with a_s = k² / (2 d_s).
Input noise (referred to h): N' = 2 d_s / k².

**Observed semantic information rate of the sensor channel.** This is the construction of niche E (docs/E.md, E2)
on the sensor channel only. The intervention replaces h in the drift of s by ĥ = H ∗ h + ξ, with |H| ≤ 1 and ξ a
Gaussian noise independent of h, with spectrum (1 − |H|²) S_h. So ĥ has the law of h. The other push of h on the agent
(on the target coordinate) does not change. It is physics, not a message.
- Viability: V = −Var(x_T), the variance of the target coordinate T. The S3 limit |v| < c is fixed, so a smaller
  variance means a longer life.
- With G_s and G_p the responses of x_T to the sensor input and to the push, and c(ω) = S_h G_s conj(G_p):
  Var(x_T)(H) = const + (1/π) ∫ Re(c H) dω (the terms in |H|² cancel). The constraint V(H) ≥ V(1) is linear in H.
- Information through the channel: İ_s(H) = (1/4π) ∫ log[(S_h + N') / ((1 − |H|²) S_h + N')] dω. This is convex in
  H, so the problem is convex and the Lagrange solution is the global minimum.
- Class A (H complex): H = −r c̄ / |c|, with w = |c|. Class Z (no shift in time, H real, 0 ≤ H ≤ 1): H = r where
  Re c < 0, with w = −Re c, and H = 0 elsewhere. In both, r = min(1, [−S_h + √(S_h² + μ² w² S_h (S_h + N'))] / (μ w S_h)),
  and a bisection on μ meets the constraint.
- If ∫ Re c dω ≥ 0, the sensor does not lower Var(x_T). Then H = 0 is feasible and S = 0. We count these systems.
- S_Z and S_A are the minimum İ_s(H) in each class. Numerical grid: 20 000 log-spaced frequencies on [10⁻⁶, 10⁵],
  trapezoid weights, as in `experiments/e30_e_coli.py`.

**Stored semantic information.** In the homeostat (scalar h, V on v), the stored form of niche B equals the full
information I(X₀; h₀) (docs/B.md, F4). So H1 reports I(X; h) only and does not compute the stored form again.

## H1. Systems (fixed 2026-11-27)

- **Family H (homeostat).** The 400 organisms of S3: `draw_organism(default_rng([2026, i]))`, i = 0..399, intact
  version. Agent (s, m, u, v), sensor s, target v. Check before use: organism 0 has L = 1.3577157550 (the value in
  `results/e23_b4a_homeostat.json`). For the description only: the simulated VoI of the 395 organisms of
  `results/e23_b4a_homeostat.json`.
- **Family R (random agents).** 2000 systems, `rng = default_rng([8400, j])`, j = 0..1999.
  - dx uniform in {2, 3, 4}. T_h log-uniform in [1, 20], B_hh = D_hh = 1/T_h (Var h = 1).
  - Sensor (coordinate 0): k log-uniform in [0.5, 5], σ_s log-uniform in [0.1, 3], d_s = σ_s² k. Row 0 has only
    B_00 = k and B_0h = −k.
  - Coordinates i = 1..dx−1: k_i log-uniform in [0.3, 5], B_ii = k_i, B_{i,i−1} = −k_i g_i with g_i uniform in
    [−2, 2]. Each other entry B_ij (i ≥ 1, j ≠ i, j ≠ i−1) is nonzero with probability 0.3, with value
    0.5 √(k_i k_j) times a standard normal number. Noise D_ii log-uniform in [0.005, 0.5].
  - Target T = dx − 1, push B_Th = −1.
  - If an eigenvalue of B_xx has a real part below 0.01, draw B_xx again with the same rng.

## H1. Rules (fixed 2026-11-27, before the runs)

Checks of the code. If a check fails, we stop and look for the error before any result.

| Rule | Question | Verdict |
|---|---|---|
| H1a | Do the two methods for l_X agree? | "pass" if the relative difference is below 10⁻⁶ in all 2400 systems |
| H1b | Do the two methods for Ṫ agree, and does the grid give İ_s at H = 1? | "pass" if below 10⁻⁶ (Ṫ, numerical integral against the closed form) and below 10⁻⁴ (İ_s on the grid) in all systems |
| H1c | Do the theorems hold? σ_X + σ_h = σ, q_X ≥ l_X ≥ 0, l_X ≤ Ṫ, the Cauchy–Schwarz form, S_Z ≤ İ_s, S_A ≤ S_Z | "pass" if each holds in all systems, with a tolerance of 10⁻⁹ relative |
| H1d | Is the semantic optimum the minimum? | On 20 systems (the first 10 of each family with ∫ Re c < 0), 1000 random garblings of each class, each mixed with the extreme feasible point (class A: H = −c̄/|c|, class Z: H = 1{Re c < 0}) to meet the constraint exactly. "pass" if none has İ_s below the optimum by more than 10⁻⁹ relative |
| H1e | Grid check | On the same 20 systems, a grid of 200 000 points on [10⁻⁸, 10⁶] changes S_Z and S_A by less than 10⁻³ relative |

## H2. Rules (fixed 2026-11-27, before the runs)

The question: does the heat of the agent pay for the information that it uses? Each "bound" below is tested on every
system. A "holds" verdict is a numerical result on these families, not a proof.

| Rule | Question | Verdict |
|---|---|---|
| H2a | Is S_Z ≤ q_X (the heat rate of the agent)? | "holds" if true in all systems of a family, else "fails", with the number of failures and the smallest q_X / S_Z |
| H2b | Is S_Z ≤ l_X (the learning rate)? | as H2a |
| H2c | Is S_Z ≤ q_s (the heat rate of the sensor alone)? | as H2a |
| H2d | Descriptive, for each family: medians and 10–90 % ranges of S_Z / İ_s, S_Z / q_X, l_X / q_X (η), l_X / Ṫ (C), and the same for class A | — |
| H2e | Descriptive, family H only: Spearman ρ of S_Z, l_X and q_X with the simulated VoI | — |

Each family gets its own verdict. We report the number of systems with S = 0.

**Expectations.** H1a to H1e "pass". H2a "holds" in family H: the actuator u has a small noise (D = 0.01) and follows
m, so its heat is large. No firm expectation for family R. H2b: no firm expectation. A sensor with a low sensory
capacity has l_X well below Ṫ, so the semantic part can be larger than l_X. H2c: no firm expectation.

**Limits, fixed now.** The heat needs the assumption of one bath for each coordinate, with temperature D_ii. The
semantic information is the one of the sensor channel, not of all paths from h to the agent. Linear Gaussian systems
only, steady state only.

**Where it runs.** This PC, `experiments/e31_h_energy.py`. A few minutes.

## H1 and H2. Results (run 2026-11-27, `results/e31_h_energy.md`, 449 s on this PC)

| Rule | Value | Verdict | Expectation |
|---|---|---|---|
| H1a | largest relative difference of the two l_X: 1.4e-10 | pass | pass. Met |
| H1b | Ṫ: 2.6e-13. İ_s on the grid: 5.9e-5 | pass | pass. Met |
| H1c | all theorems hold. The smallest margins: q_X − l_X 0.24 q_X, l_X ≥ 0.004 Ṫ, Ṫ − l_X ≥ 0.0009 Ṫ | pass | pass. Met |
| H1d | 20 systems, 1000 garblings for each class, none below the optimum | pass | pass. Met |
| H1e | largest change on the fine grid: 2.3e-4 | pass | pass. Met |
| H2a | S_Z ≤ q_X. Family H: 0 failures of 400, smallest q_X / S_Z = 29.9. Family R: 0 failures of 2000, smallest 1.22. Class A: 0 failures | holds (H), holds (R) | holds (H). Met. No expectation for R |
| H2b | S_Z ≤ l_X. Family H: 3 failures of 400, smallest l_X / S_Z = 0.72. Family R: 155 failures of 2000, smallest 0.14. Class A: 1 and 53 failures | fails (H), fails (R) | no firm expectation |
| H2c | S_Z ≤ q_s. Family H: 117 failures, smallest 0.14. Family R: 241 failures, smallest 0.13 | fails (H), fails (R) | no firm expectation |

The sensor helps (∫ Re c < 0) in all 400 organisms of family H and in 988 of the 2000 systems of family R. In the other
1012 systems of family R, S = 0.

**Description (H2d, median [10 %, 90 %], systems where the sensor helps).**
| Ratio | Family H | Family R |
|---|---|---|
| S_Z / İ_s (semantic part of the channel) | 0.56 [0.23, 0.84] | 0.82 [0.17, 1.00] |
| S_A / İ_s | 0.31 [0.08, 0.65] | 0.37 [0.06, 0.80] |
| S_Z / q_X (used information per unit of heat) | 0.002 [0.000, 0.012] | 0.008 [0.000, 0.120] |
| S_Z / l_X | 0.27 [0.12, 0.47] | 0.41 [0.08, 1.18] |
| η = l_X / q_X (all systems) | 0.007 [0.000, 0.041] | 0.025 [0.001, 0.168] |
| C = l_X / Ṫ (all systems) | 0.48 [0.15, 0.82] | 0.54 [0.16, 0.92] |

**H2e (family H, 395 organisms, Spearman ρ with the simulated VoI of S3).** S_Z +0.57, S_A +0.56, İ_s +0.46,
l_X +0.30, q_X −0.34. For comparison (B4a, `results/e23_b4a_homeostat.json`): ΔV_KW +0.36, P +0.41.

**Post-hoc observations (not rules).**
1. In the systems where S_Z > l_X, S_Z / İ_s is near 1 (median 0.88 in family H, 1.00 in family R) and η is very
   small (median 5e-5 in family H). These agents need almost all of the channel, and their own dynamics make little
   new correlation with h.
2. The transfer entropy rate is not below the heat: Ṫ / q_X reaches 1.11 in family R. İ_s / q_X stays below 0.82 in
   all 2400 systems. We did not expect this, and we have no proof for it.

### What H1 and H2 show
1. **The learning rate does not bound the semantic information.** The second law prices the learning rate l_X. The
   observed semantic information rate of the sensor channel can be larger than l_X, by up to seven times in family R.
   So "the agent pays for the information that it uses" is false if one measures the payment with the learning rate.
2. **The heat of the agent bounds the semantic information in all 2400 systems, with a wide margin in the
   homeostat.** The heat is about 500 times the used information in the median organism (S_Z / q_X = 0.002). This is
   a numerical result. In family R the smallest margin is 1.22, so a search for a counterexample is the next test (H3).
3. **The heat of the sensor alone does not bound it.** In 117 organisms of family H the sensor gives less heat than
   the semantic information that passes through it. The heat that "pays" is the heat of the parts after the sensor.
4. **The semantic rate ranks the S3 organisms better than the earlier measures.** ρ = +0.57 with the simulated VoI,
   against +0.41 for P and +0.36 for the stored value ΔV_KW. This is a description, not a rule.

### Limits
- One bath for each coordinate, with the temperature D_ii. Other physical models of the same equations give other
  heats.
- The semantic information is the one of the sensor channel only.
- Two families, drawn by us. The bound of H2a is numerical.

## H3. A search for a counterexample to H2a (rules fixed 2026-11-27, after the H2 results, before the search)

**Why.** H2a holds in all 2400 systems, but the smallest margin in family R is 1.22. A random draw rarely finds the
worst case. Post-hoc observation 2 (İ_s ≤ q_X) is also untested. H3 searches for systems that break each bound.

**Search.**
- Starts: the 40 systems of family R and the 8 organisms of family H with the largest S_Z / q_X in
  `results/e31_h_energy.json`.
- Free parameters: the logarithm of the modulus of each nonzero entry of B_xx (the signs stay fixed, the sensor keeps
  B_00 = −B_0h = k), the logarithm of each D_ii of the agent, and log T_h (with B_hh = D_hh = 1/T_h). The push on the
  target stays −1. Each logarithm stays in [log 10⁻³, log 10³].
- Objective: the largest S_Z / q_X (H3a), and in a second search the largest İ_s / q_X (H3b). A point with an
  eigenvalue of B_xx below 0.01 in real part gets the value −∞.
- Method: Nelder–Mead, at most 600 evaluations for each start and each objective, on the grid of 4000 frequencies.
- Confirmation of the best point: the grid of 200 000 frequencies, and the checks H1a, H1b and H1c on that system.

| Rule | Question | Verdict |
|---|---|---|
| H3a | Is there a system with S_Z > q_X? | "counterexample" if the best ratio is above 1 on the fine grid and the system passes H1a to H1c. Else "none found", with the largest ratio |
| H3b | Is there a system with İ_s > q_X? | as H3a |

We report if the best point lies at a limit of the box. **Expectations:** no firm expectation for H3a. H3b: a
counterexample is likely, because İ_s / q_s reaches 8 in H2 and the search can make the heat after the sensor small.

**Where it runs.** This PC, `experiments/e31b_h3_search.py`, 4 workers.
