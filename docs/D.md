# Niche D: replication and controls in the models of the Rochester group

This file starts on 2026-11-27. The plan is in `ROADMAP_DI.md`. Each step writes its rules before its runs, and the
results come after.

## D0. The two models in our notation (read 2026-11-27)

**How we read the papers.** A reader agent read the arXiv HTML of each paper. We then extracted the text of the arXiv
PDFs and checked Appendix B of Sowinski23 ourselves. Neither paper gives a link to code.

### Sowinski23: the foraging agent (Sec. II, Appendix B, Table II)
- Units: time S/μ, length r. Table II: r = 1, μ = 1, S = 1, R = 4 (sensing radius), v = 20 (Fig. 3), L = 100,
  Δt = 0.02, ε = 0.1 (fuel of one resource), γ = 0.1 (decay rate), Γ = 0.001 (influx). Then n_eq = 0.1, v_⋆ = 5,
  v^⋆ = 50.
- Agent (s, τ, n̂, x). Start: s = 0.5, at the centre, in an environment of N = 1000 resources placed uniformly.
- One step (Appendix B, Fig. 1): end if s ≤ 0. Take the nearest resource y1. If |y1| ≤ r: harvest (s += ε, τ = 0), no
  move. Else if τ = 1: s −= μΔt, x += v n̂ Δt. Else if |y1| ≤ R: τ = 1, s −= μΔt, n̂ = direction of y1 (with sensor
  noise), move. Else: s −= μΔt, move straight. Then reflect at the walls.
- Environment step: each resource is removed with probability 1 − e^{−γΔt}. Then Poisson(λ = ΓL²Δt/ε = 2) new
  resources at uniform places.
- Intervention: the heading at a detection is the true direction rotated by an angle uniform on [−πη, πη].
- Viability V = E[T] (in units S/μ). 10^4 runs for each of 200 values of η: 100 equally spaced on [0, 0.15), 100
  log-spaced on [0.15, 1].
- Syntactic information T = log2(1/η) (Eq. (3)). Semantic threshold: the peak of dV/dT, with a smoothing that the paper
  does not state. Prediction Eq. (4): η_c = arcsin(r/R)/π = 0.0804 for R = 4. Eq. (11): V at η = 1 is
  (s0/μ)/(1 − v/v^⋆) = 0.833 for v = 20. Eqs. (9) and (D3): V_η ≥ V_actual / (1 + λ_max) below the threshold, with
  E_η[λ] = r/y − 1 + sin(πη)/(πη) − (r/y) E(πη | y²/r²)/(πη) (incomplete elliptic integral of the second kind).

**Details that the paper does not state, and our choice.**
| Detail | Our choice |
|---|---|
| Wall rule "if x > L then x ↦ L − x" (a typo: L − x is outside the box for x > L) | x ↦ 2L − x |
| Move at a detection: "x + y1/|y1| Δt" (no v, a typo) | x + v n̂ Δt |
| Initial heading | uniform |
| Fuel cap at S | s ↦ min(s + ε, S), with S = 1. Table II calls S the "maximum stored energy". See the note below the table |
| Fuel cost on a harvest step | none (as in the flowchart) |
| Maximum time | 10^4 time units. A run that reaches it counts as censored and is reported |
| η = 0 in the grid | included (the first value of [0, 0.15)) |

**Note on the fuel cap (2026-11-27, a test before any run, not a result).** Our first choice was no cap. A test with
40 runs for each speed at η = 0 gave agents that do not die at v = 25 and v = 30: most runs reached the time limit of
10^4. With the cap, all runs end before the limit (200 runs for each speed: mean V from 0.82 at v = 5 to 48 at v = 30
at η = 0). The paper shows finite viabilities at all six speeds (Fig. 4). So we use the cap. Without the cap, V at
η = 0 and v = 20 is 24.8, and with the cap 14.5. At η = 1 the cap changes nothing (0.86 in both).

### SowinskiFrankGhoshal24: the Kuramoto agent (Sec. III, Appendix A)
- Oscillators: dθ_i/dt = ω_i + σ Σ_j A_ij sin(θ_j − θ_i) (Eq. (1)), ω_i standard normal, uniform initial phases. No
  noise in the oscillators. Δt = 1/16. 1500 steps of transient, then 512 steps averaged for r (Eq. (2)).
- Graphs: fully connected (N = 1024, σ = K/N, K on [0, 4]), Poisson and scale-free (N ≈ 1000, ⟨k⟩ ≈ 4, σ on [0, 1],
  configuration model).
- Agent (i, κ_i). At each jump the agent reads θ_i and an estimate φ̂_i of the local mean-field phase φ_i (Eq. (3)),
  sets κ_i = +1 if θ_i > φ̂_i else −1 (Eq. (6)), kicks θ_i ↦ θ_i + ακ_i, and jumps to a random neighbour. α = 0.5,
  β = 0.16, with βN jumps per unit time.
- Intervention: φ̂_i uniform on [φ_i − πη, φ_i + πη]. η on [0, 1], 128 values.
- Efficacy E = 1 − E[r | agent] / E[r] (Eq. (10)). Viability V = ∫ E(σ) ρ(σ) dσ (Eq. (11)), with ρ uniform or
  exponential with mean 0.5, 1 or 2 times σ_c^A.
- Reported: K_c = 1.595 without the agent and K_c^A ≈ 1.988 with the agent (fully connected). The agent lowers the
  synchronisation by about 20 %. Viability per bit 1.5 ± 0.05 then 0.25 ± 0.02 (fully connected, a threshold), 0.886
  (Poisson) and 0.841 (scale-free), linear. E is not zero at η = 1 ("heat bath").

**Details that the paper does not state, and our choice.**
| Detail | Our choice |
|---|---|
| Integration scheme | fourth-order Runge–Kutta for the oscillators. The kicks happen between steps |
| Jumps in one step | Poisson with mean βNΔt, done in order after the step |
| "θ_i > φ̂_i" on a circle | the sign of sin(θ_i − φ̂_i) |
| Next node | a uniform neighbour (Sec. III.1.2). In the fully connected graph, a uniform other node |
| Graphs | Poisson: G(N, 4/(N − 1)). Scale-free: configuration model with P(k) ∝ k^−2.5, 2 ≤ k ≤ 100 (mean 4.1), self-loops and double edges removed. Both: the giant component only. One agent, which starts at a uniform node |
| The x axis of the viability per bit (not defined) | I(η) = 1 − E[h2(p_flip)] bits per kick, with h2 the binary entropy and p_flip the probability of a wrong kick at the node (Sec. III.4 formula, averaged over the nodes of the run) |
| Range of uniform ρ(σ) | the full range of the sweep |
| σ_c^A for the exponential ρ(σ) | the paper values: K_c^A = 1.988 (fully connected) and σ_c^A = 0.5 (graphs) |
| Synchronised range for D2b and D2c | K in [2.5, 4] (fully connected) |

## Rules (fixed 2026-11-27, before the runs)

### D1. The foraging agent
**Sets.** Speeds v in {5, 10, 15, 20, 25, 30} at R = 4, and R in {2, 8} at v = 20 (8 sets). The paper grid of 200
values of η, 10^4 runs each. The main set (v = 20, R = 4) gets 10^5 runs for each η. Seeds: [set, η index, run].

**Threshold estimator (fixed, ours).** On η in [0, 0.15), fit V(η) with a continuous two-segment linear function
(both slopes free) by least squares. The break point is η̂_c. CI: 1000 bootstrap resamples of the runs at each η.
We also report the peak of dV/dT after a Savitzky–Golay smoothing (window 11, order 2) as a second, descriptive value.

| Rule | Question | Verdict |
|---|---|---|
| D1a | Is Eq. (4) right at R = 4, v = 20? | "agrees" if arcsin(r/R)/π is inside the 95 % CI of η̂_c |
| D1b | Does η̂_c follow the geometry? | "agrees" if the 95 % CI of η̂_c contains arcsin(r/R)/π for each R in {2, 4, 8} at v = 20 |
| D1c | Does η̂_c not depend on v? | "agrees" if the 6 CIs of η̂_c at R = 4 all contain 0.0804 |
| D1d | Is Eq. (11) right? | "agrees" if V(η = 1) is within 5 % of (s0/μ)/(1 − v/v^⋆) at each of the 6 speeds |
| D1e | Does the bound of Eq. (9) hold? | V_η / V_actual ≥ 1 / (1 + λ_max), with λ_max = E_η[λ] of Eq. (D3) at y = R, for 0 < η ≤ η_c (the range of Eq. (D3)). "holds" if V_η / V_actual + 2 SE ≥ the bound at all these η of the main set |

### D2. The Kuramoto agent
**Sets.** Fully connected (N = 1024): 64 values of K on [0, 4], 32 values of η on [0, 1], 128 runs for each (K, η),
512 runs without the agent and 32 runs of the still agent for each K. Poisson and scale-free (N = 1000, ⟨k⟩ ≈ 4): 64
values of σ on [0, 1], 32 values of η, 64 graphs for each, 256 runs without the agent and 32 runs of the still agent
for each σ. A run draws a new graph, new frequencies and new phases. Seeds: [topology, K index, η index, run].
The efficacy E(K, η) uses the mean r of the runs with the agent and the mean r of the runs without it. Its CI comes
from 1000 bootstrap resamples of the runs.

| Rule | Question | Verdict |
|---|---|---|
| D2a | Is the shift of the critical coupling right? | K_c from a fit r = A √(K − K_c) on the points with 0.25 < r < 0.7, with and without the agent (fully connected, η = 0). "agrees" if K_c^A − K_c is within ±0.1 of 1.988 − 1.595 = 0.393 |
| D2b | Does the agent lower r by about 20 %? | Mean of E over K in [2.5, 4] at η = 0. "agrees" if it is in [0.15, 0.25] |
| D2c | Is E positive at η = 1? | "yes" if the 95 % CI of the mean E over K in [2.5, 4] at η = 1 is above 0 |
| D2d | Is there a threshold only in the fully connected graph? | V_η (uniform ρ) against I(η). Fit one line and a continuous two-segment line. "agrees" if the two-segment fit wins by BIC in the fully connected graph and loses in the Poisson and scale-free graphs |

### D3. Controls with zero information
- Foraging: a "blind" agent turns to a uniform direction at each detection (η = 1), and a "deaf" agent never turns.
- Kuramoto: a "blind" agent kicks with a random sign (η = 1), and a "still" agent reads but does not kick (α = 0).

| Rule | Question | Verdict |
|---|---|---|
| D3a | How much of the foraging viability needs no information? | F_free = (V_blind − s0/μ) / (V(η = 0) − s0/μ), with a bootstrap CI, at each speed. Descriptive |
| D3b | How much of the Kuramoto viability needs no information? | F_free = V_blind / V(η = 0), uniform ρ and the three exponential ρ, with a bootstrap CI over graphs, for each topology. Descriptive |
| D3c | Control check | "pass" if the still agent gives |E| < 3 SE at all couplings (it must give E = 0) |

**Expectations.** D1a, D1b, D1c: "agrees", with medium confidence (the bound of Eq. (4) is geometric). D1d: "agrees".
D1e: "holds". D2a: "agrees", low confidence (our integration and our jump rule can differ). D2b: "agrees". D2c: "yes".
D2d: low confidence, because we must choose the x axis. D3a: F_free below 0.1. D3b: F_free above 0.3 (the paper says
that the agent acts as a heat bath at η = 1). D3c: "pass".

**Where it runs.** On the Xeon machines (`cluster/`). Each task is one (set, η) for D1 and one (topology, K, η) for D2.
