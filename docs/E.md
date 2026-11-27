# Niche E: semantic information of E. coli chemotaxis

This file starts on 2026-11-27. The plan is in `ROADMAP_DI.md`. Each step writes its rules before its runs, and the
results come after.

## E0. The model of MattinglyKaminoMachtaEmonet21 in our notation (read 2026-11-27)

**How we read the paper.** We extracted the text of the arXiv PDF (arXiv:2102.11732, 83 pages with the supplementary
text) and read the main text, Table S1 and the supplementary sections on the drift speed (Eqs. (14)–(27)), the
information-performance bound (Eqs. (67)–(70)), the "relevant bits" (Eqs. (71)–(78)) and the information rate from the
signal to the kinase (Eqs. (84)–(102)).

**The model (linear, Gaussian, stationary, shallow gradient).**
- Signal s(t) = g v_x(t), with g = d log c / dx the steepness of the gradient and v_x the up-gradient velocity.
  V(t) = ⟨v_x(t) v_x(0)⟩ = a_v e^{−λ|t|} (Eq. (92)), so V(ω) = 2 a_v λ / (λ² + ω²) (Eq. (95)).
- Kinase response K(t) = G (1 − e^{−t/τ1}) e^{−t/τ2} for t ≥ 0 (Eq. (96)), and
  K(ω) = (G/τ1) / ((1/τ2 + iω)(1/τ1 + 1/τ2 + iω)) (Eq. (97)).
- Kinase noise: an Ornstein–Uhlenbeck process with N(ω) = 2 D_n / (1/τ_n² + ω²) (Eq. (100)).
- Kinase activity a(t) = (K ∗ s)(t) + n(t).
- Information rate (Eq. (86), shallow gradient): İ_{s→a} = (1/4π) ∫ g² V(ω) |K(ω)|² / N(ω) dω = β g² (Eq. (102)).
- Drift speed (Eq. (19)): v_d is proportional to ⟨ε(t) cos θ(t)⟩, the covariance of the tumble-rate modulation ε at
  time t and the heading at time t. In the linear regime ε is proportional to the kinase output.
- "Relevant bits" (Eqs. (71)–(78)): the information rate splits into a part about the current signal s(t) and a part
  about the past signals given s(t). The drift speed depends only on the first part: v_d ∝ (İ_{s(t)→m})^{1/2}.
- Efficiency: the cells climb at 66 ± 5 % of the bound set by İ_{s→a} (main text). Because v_d ∝ √İ, this means that
  about 0.66² = 0.44 of the kinase information acts as information about the current signal at the motors.

**Table S1 (the values we use).** a_v = 157.1 ± 0.5 μm²/s², λ = λ_tot = 0.862 ± 0.005 s⁻¹, G = 1.73 ± 0.03,
τ2 = 9.9 ± 0.3 s, τ1 = 0.05 s (literature value, used for β; the fit value 0.22 ± 0.01 s includes CheY/CheZ binding),
D_n = (7.2 ± 0.3) × 10⁻⁴ s⁻¹, τ_n = 11.75 ± 0.04 s, β = 0.22 ± 0.03 bits/s/mm⁻², χ = 4300 ± 150 μm²/s.

**What the paper does not do.** It does not use the intervention approach of KolchinskyWolpert18. It finds the
"relevant" part of the information by an optimisation over behavioural strategies, not by an intervention on the
signal with the pathway fixed.

**Search for prior work (2026-11-27).** We know of no paper that computes the semantic information of
KolchinskyWolpert18 for chemotaxis or for any measured signalling pathway. This is a search result, not a proof.

## Rules (fixed 2026-11-27, before the runs)

### E1. Reproduce β
Compute β from Table S1 in two ways: Eq. (102) (closed form) and a numerical integral of Eq. (86). Propagate the
errors of Table S1 by 10 000 Monte Carlo draws (each parameter normal with its standard error, τ1 fixed at 0.05 s).

| Rule | Question | Verdict |
|---|---|---|
| E1a | Do the closed form and the integral agree? | "agree" if they differ by less than 10⁻⁶ relative |
| E1b | Do we get their β? | "agrees" if our β is inside 0.22 ± 0.03 bits/s/mm⁻² |

### E2. Semantic information of the signalling channel
**Agent, environment, channel.** The environment is the signal trajectory s. The agent output is the kinase trajectory
a. The channel s → a is fixed by K and N.

**Viability.** V = Cov(a(t), s(t)) in the stationary state. This is the drift speed up to a positive factor, if the
motor responds linearly to a (Eq. (19)). V = (1/2π) ∫ Re[K(ω)] S(ω) dω, with S = g² V(ω).

**Intervention (a pre-garbling of the channel input, as Eq. (8) of KolchinskyWolpert18).** Replace s by
ŝ = h ∗ s + ξ, with h a linear time-invariant filter with frequency response H(ω), |H| ≤ 1, and ξ a Gaussian noise
independent of s with spectrum (1 − |H|²) S(ω). Then ŝ has the same law as s. H ≡ 1 is the actual cell, H ≡ 0 is full
scrambling. Under the intervention, V(H) = (1/2π) ∫ Re[K H] S dω and, in the shallow gradient of Eq. (86),
İ(H) = (1/4π) ∫ |H|² g² V |K|² / N dω.

**Two classes of interventions.**
- **Class A (all garblings):** H complex. The best H follows from the Lagrange condition at each frequency:
  H(ω) = μ N(ω) / K(ω), with the modulus cut at 1. μ is set by V(H) = V_actual.
- **Class Z (garblings without a time shift):** H real, 0 ≤ H ≤ 1. The best H is
  H(ω) = min(1, max(0, μ N(ω) Re K(ω) / |K(ω)|²)).
Both are convex problems (a quadratic objective, a linear constraint, a convex set), so the Lagrange solution is the
global minimum. A class A garbling can shift the signal in time, so it is not causal. We report both.

**Semantic information.** S_A = İ(H_A*) and S_Z = İ(H_Z*). Efficiencies e_A = S_A / İ_{s→a}, e_Z = S_Z / İ_{s→a}.
These ratios do not depend on g in the shallow gradient. CIs: the 10 000 Monte Carlo draws of E1.

| Rule | Question | Verdict |
|---|---|---|
| E2a | Check of the optimum | "pass" if, on 1000 random feasible H of each class (random modulus and phase on a grid of 4000 frequencies, scaled to meet V = V_actual), none has a lower İ than the optimum |
| E2b | Is the semantic information smaller than the full information? | "yes" if the 95 % CI of e_Z is below 1 |
| E2c | Does the shift in time matter? | Descriptive: e_A and e_Z with CIs |

### E3. Compare with the relevant bits of the paper
| Rule | Question | Verdict |
|---|---|---|
| E3a | Does e_Z match the fraction 0.66² of the paper? | "match" if the 95 % CI of e_Z overlaps [0.44 − 0.07, 0.44 + 0.07] (the error of 0.66 ± 0.05, squared), else "differ" |
| E3b | The same for e_A | as E3a |

**Expectations.** E1a "agree". E1b "agrees". E2a "pass". E2b "yes": the kinase lags the signal, so the frequencies with
Re K < 0 lower the drift, and class Z drops them. E2c: e_A < e_Z, because class A also undoes the lag. E3a and E3b: no
firm expectation. The paper's 0.44 comes from the motors and from behavioural parameters, which our viability does not
use.

**Limits, fixed now.** The viability uses the kinase, not the motors (the paper's bound uses the motors). The
shallow-gradient form of İ is the one of Eq. (86). The signal is not Gaussian in reality (Sec. "Information rate from
signal to kinase activity: approach"), and the paper says that the Gaussian form is a good approximation in shallow
gradients. We use the measured median cell only.

**Where it runs.** This PC, `experiments/e30_e_coli.py`. A few minutes.
