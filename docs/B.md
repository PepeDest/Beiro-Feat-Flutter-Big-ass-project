# Niche B: exact semantic information in linear Gaussian systems

This file starts on 2026-11-24. The plan is in `ROADMAP_ABC.md`. As in `A.md`, each step writes its rules before its
runs, and the results come after.

## B0. Literature check (2026-11-24)

### How we read the papers
We read the full texts of the six papers below. For each paper, a reader agent read the arXiv HTML. We then extracted
the text of the arXiv PDFs and checked the key definitions against it ourselves:
- KolchinskyWolpert18: Sec. V A, Eqs. (4)–(10), read in full.
- TanakaEsfahaniMitter18: Theorem 2 and the max-det problem (18), read in full.
- Sowinski23 and SowinskiFrankGhoshal24: the statements on computational cost, read in full.

Other items come from the reader agents and carry their section numbers. All six references are checked on Crossref or
on the arXiv page (`REFERENCES.md`).

### Search for prior work on our question
- 2026-11-20 (in `ROADMAP_ABC.md`): the 181 papers that cite KolchinskyWolpert18, Sowinski23 or Bartlett25. None
  computes semantic information for continuous or Gaussian variables.
- 2026-11-24: web searches for semantic information with "Gaussian", "linear", "Ornstein–Uhlenbeck",
  "information/viability curve" and "semantic threshold". No hit connects the KolchinskyWolpert18 measure to Gaussian or
  linear systems.
- KolchinskyWolpert18 itself treats finite state spaces only. It says that the approach can be extended to continuous
  state spaces, but it does not do this.

Result: we found no closed form or Gaussian computation of semantic information. This is a search result, not a proof
that none exists.

### Notation
System (agent) X, environment Y. Time 0 is the start, τ is the time of the viability. Σ is a covariance. In whitened
coordinates, Σ_X = I and Σ_Y = I, and C = Σ_X^{-1/2} Σ_XY Σ_Y^{-1/2} is the whitened cross-covariance.

### KolchinskyWolpert18 (Interface Focus 2018)
- **Viability**, Eq. (2): V = −H(X_τ), the negative Shannon entropy of the system marginal at time τ. The paper
  discusses other choices (the probability of a viability set, a relative entropy), but does not use them.
- **Full scrambling**, Eq. (5): p(x_0, y_0) → p(x_0) p(y_0). **Value of information**, Eqs. (6)–(7):
  ΔV = V(actual) − V(full scrambling). It can be negative.
- **Partial intervention**, Eq. (8): a coarse-graining function φ of the environment. The intervened channel is
  p̂(x_0 | y_0) = p(x_0 | φ(y_0)), and the intervened joint is p̂(x_0 | y_0) p(y_0). The marginals of X_0 and Y_0 stay
  the same. The dynamics after time 0 do not change. The paper calls this channel a "Markov approximation", a special
  case of channel pre-garbling. Then I_p̂(X_0; Y_0) = I_p(X_0; φ(Y_0)).
- **Information/viability curve**: D(R) = max over φ of V(p̂_{X_τ}), with I_p̂(X_0; Y_0) = R.
- **Optimal intervention**, Eq. (9): the φ with the smallest I_p̂(X_0; Y_0) that keeps V equal to the actual V.
- **Stored semantic information**, Eq. (10): S = I_p̂opt(X_0; Y_0). Efficiency: S / I_p(X_0; Y_0), in [0, 1].
- **Observed semantic information** (Sec. V B): the same, with the transfer entropy T(Y_t → X_{t+1}) =
  I(Y_t; X_{t+1} | X_t) summed over time, and the intervention applied at each step.
- The paper computes all quantities by a search over φ, on a discrete example (food at 5 places, I = 2.32 bits,
  S = 1.37 bits).

### Sowinski23 (PRX Life 2023)
- A foraging agent with fuel, heading and position. Resources appear and decay in a 2-D box.
- **Viability**: the expected lifetime E[T], not an entropy.
- **Syntactic information**: the transfer entropy of one detection event, Eq. (3): T = log2(1/η).
- **Intervention**: sensor noise. A uniform angle error of width 2πη, η in (0, 1], replaces the ideal heading.
- **Semantic threshold**: the peak of dV/dT. Eq. (4) gives the critical noise η_c = (1/π) arcsin(r/R), with r the
  harvest radius and R the sensing radius.
- **Cost**: simulation, 10^4 runs for each of 200 noise values. The paper states that the KolchinskyWolpert18 method has
  "formal and computational issues" for extensive state spaces. The authors chose the ballistic strategy for its
  analytical tractability.
- No Gaussian or linear model.

### SowinskiFrankGhoshal24 (Phys. Rev. Research 2024)
- A four-step protocol, in words: (1) split the system into agent and environment, (2) coarse-grain and measure the
  correlations (mutual information, transfer entropy), (3) choose a viability measure, (4) scramble the correlations and
  find the semantic threshold, where the scrambled viability leaves the actual viability.
- Model: Kuramoto oscillators on networks, with an agent that kicks oscillators. Viability: the drop of the order
  parameter. Intervention: a uniform noise on the estimate of the local phase by the agent.
- The paper states that the KolchinskyWolpert18 formalism is computationally intractable for large state spaces. It says
  that the search over partitions becomes unmanageable above several hundred states.
- No Gaussian or linear model.

### TanakaEsfahaniMitter18 (IEEE TAC 2018)
- Plant x_{t+1} = A x_t + B u_t + w_t, w_t ~ N(0, W). The policy sees x_t. Quadratic cost J ≤ D.
- Minimise the directed information I(x^T → u^T) = Σ_t I(x^t; u_t | u^{t−1}) at J ≤ D.
- Theorem 2 (time-invariant case): the minimum is the value of a max-det problem (18). Minimise
  ½ log det Π^{-1} + ½ log det W, with Tr(Θ P) + Tr(W S) ≤ D, Π ≻ 0, P ⪯ A P Aᵀ + W, and
  [[P − Π, P Aᵀ], [A P, A P Aᵀ + W]] ⪰ 0.
- The optimal policy is a linear Gaussian sensor, a Kalman filter and a certainty-equivalence controller. Gaussianity is
  a result, not an assumption.

### SabagTianKostinaHassibi23 (IEEE TAC 2023)
- The same plant, and the controller also sees y_t = C x_t + v_t. An encoder sends f_t to the controller.
- Minimise the conditional directed information I(x^T → f^T ‖ y^T) at J ≤ Γ.
- The optimal encoder is a memoryless Gaussian measurement f_t = D x_t + m_t. An SDP gives the time-invariant policy
  (Theorem 3, Eq. (24), from the arXiv v1 text).

### Kolchinsky26 (arXiv 2026)
- Target Y and sources X_i, each jointly Gaussian with Y. Theorem 1: a channel is Blackwell-below another if and only if
  its posterior covariance of Y is larger in the Loewner order.
- Theorems 2 and 3: Gaussian channels are optimal for the Blackwell redundancy and the Blackwell union information.
  Both are convex log-det programs in one d_Y × d_Y matrix (Eqs. (8) and (12)), with a closed form for two sources.
- The paper does not mention semantic information, viability or interventions.

### What B0 gives us
1. **The gap is real.** Two groups state that the cost of the computation is the obstacle. No paper that we found
   computes the KolchinskyWolpert18 quantities for continuous or Gaussian variables.
2. **The control papers do not answer the question.** Tanaka and Sabag minimise information at a fixed cost of
   control, so they design a sensor. KolchinskyWolpert18 asks how much of the existing information an existing agent
   needs, with the dynamics of the agent fixed. B3 tests if the two problems meet in the dynamic case.
3. **The Blackwell link is not direct.** KolchinskyWolpert18 garbles the input of the channel Y → X (pre-garbling).
   The Blackwell order of Kolchinsky26 garbles the output (post-garbling). In whitened Gaussian terms, pre-garbling
   gives the cross-covariance C P, and post-garbling gives G C. B2 must check which tools of Kolchinsky26 still apply.

### A first observation for B1 (ours, checked by sampling, not yet a rule)
Take the Gaussian form of a pre-garbling: Z = K Y + N, N ~ N(0, Σ_N), and draw the intervened X from the actual
p(x | z). In whitened coordinates:
- Let P = Kᵀ (K Kᵀ + Σ_N)^{-1} K. Then 0 ⪯ P ⪯ I, and every such P comes from some (K, Σ_N).
- The intervened cross-covariance is C P. The marginals of X and Y do not change.
- The syntactic information is I_p̂(X_0; Y_0) = −½ log det(I − C P² Cᵀ). This equals I(X; Z) only when P is a
  projection, which is the deterministic coarse-graining of KolchinskyWolpert18.
- For linear dynamics, the covariance of X_τ is affine in P. So V = −½ log det Σ_{X_τ}(P) + const is convex in P.

A sampling check (`experiments/b0_garbling_check.py`, 400 000 draws, 2 × 3 dimensions) gives the cross-covariance within 0.003 and I within 0.001 nats of
the formulas. A consequence to test in B2: the maximum of a convex function over {0 ⪯ P ⪯ I} lies at an extreme point,
and the extreme points are the projections. So deterministic coarse-grainings can be enough in the Gaussian case. This
is a conjecture, because the constraint on I is not linear in P.

## B1. The static case in closed form (written 2026-11-24, before the Monte Carlo check)

**Setting.** Joint state z = (x, y), agent x with dx coordinates, environment y with dy coordinates. Linear dynamics
dz = −B z dt + √(2D) dW. The start z_0 ~ N(0, S_0) is the stationary law. Viability V = −H(X_τ), as in
KolchinskyWolpert18, Eq. (2). The intervention acts at time 0 only (stored semantic information).

**Formula (ours).** With the intervention matrix P of B0 (whitened y coordinates, 0 ⪯ P ⪯ I):
- Σ_XY(P) = Σ_XY Σ_Y^{-1/2} P Σ_Y^{1/2}. The other blocks of S_0 do not change.
- I_P(X_0; Y_0) = −½ log det(I − C P² Cᵀ).
- Φ = exp(−Bτ), Q_τ = ∫_0^τ e^{−Bs} 2D e^{−Bᵀs} ds (Van Loan's block exponential [VanLoan78]).
- Σ_{X_τ}(P) = [Φ S_0(P) Φᵀ + Q_τ]_XX. In blocks of Φ: Σ_{X_τ}(P) = A_0 + M(P) + M(P)ᵀ, with
  M(P) = Φ_XX Σ_XY(P) Φ_XYᵀ and A_0 the part that does not depend on P.
- V(P) = −½ (dx log 2πe + log det Σ_{X_τ}(P)).

Two direct consequences:
- If the environment does not drive the agent (Φ_XY = 0), V does not depend on P. Then the agent has no stored
  semantic information, whatever its mutual information with the environment.
- Σ_{X_τ} is affine in P, so V is convex in P (B0).

**Code.** `src/vlife/semantic.py`. Tests: `tests/test_semantic.py` (6 tests: the propagator against the Lyapunov
solution, the two ends P = I and P = 0, a projection against the information of the coarse-grained environment, the
range of P, the affine form, and the case Φ_XY = 0).

**Monte Carlo check (`experiments/e20_b1_monte_carlo.py`).** Independent of the formula in two places: the start is
sampled with the garbling itself (draw y_0, build Z, draw x_0 from the actual p(x_0 | z)), and the dynamics use
Euler–Maruyama with dt = 5·10⁻⁴.
- 4 systems (dx = 2, dy = 3, seeds 101 to 104), τ = 0.5 and 1.
- 4 interventions: actual (P = I), full scrambling (P = 0), a deterministic coarse-graining (a random rank-1
  projection), and a random Gaussian garbling.
- 100 000 trajectories in 20 batches. For each case: V and I_P(X_0; Y_0) from the sample covariance, mean and standard
  error (SE) over the batches. I_P does not depend on τ. That gives 48 checks (32 of V, 16 of I).
- **Pass criterion, fixed now:** at least 45 of the 48 checks within 3 SE of the formula, and none beyond 5 SE.
  Known bias: Euler–Maruyama changes the covariance by about dt·‖B‖, about 0.1 %, which is below 1 SE.


## B1. Results (added 2026-11-24, after the run)
Report: `results/e20_b1_monte_carlo.md` and `.json`. Logs: `results/e20_run.log`.

**Two problems with the script, both fixed before any result was read:**
- Before the run: the garbling matrix of the script used K on raw y, but the sampling used K on whitened y. Commit
  14e8c45 fixed it.
- The first run (`results/e20_run1_crashed.log`) stopped at the file write (a numpy integer in the JSON). No result
  reached the disk. The second run used the same seeds, so it draws the same numbers.

**Verdict by the fixed criterion: fail.** 44 of 48 checks are within 3 SE, and 4 checks are beyond 5 SE (the
criterion asks for at least 45 and none).

| Quantity | Checks within 3 SE | Largest abs(z) |
|---|---|---|
| V(P), all interventions and both τ | 32 of 32 | 2.81 |
| I_P(X_0; Y_0), P = I, projection, garbling | 12 of 12 | 2.74 |
| I_P(X_0; Y_0), full scrambling (P = 0) | 0 of 4 | 8.61 |

**Why the 4 checks fail.** The 4 failures are the full scrambling, where the true information is 0. There, the sample
estimate is +0.0006 to +0.0008 nats in every system. The plug-in estimate of a Gaussian mutual information from a
sample covariance has a known upward bias of about dx·dy/(2n) = 0.0006 nats at n = 5000 per batch. At P = 0 the SE is
only 0.0001, so this bias is 7 to 9 SE. The criterion did not allow for this bias. That was our error when we wrote it.

**Post-hoc check (not a rule, `experiments/e20b_posthoc_bias.py`).** After we subtract 0.0006 nats from each I
estimate, all 16 I checks are within 2.42 SE.

**What B1 shows.** The closed form of V(P) agrees with an independent simulation in all 32 cases, for the actual start,
the full scrambling, a deterministic coarse-graining and a random Gaussian garbling. The formula of I_P agrees in all
cases where the true value is not 0. At 0, the only gap is the known bias of the estimator. We do not change the verdict
of the criterion. We report it as written, with this explanation.

## B2. Rules (fixed 2026-11-24, before the runs)

**Question.** In linear Gaussian systems, what is the stored semantic information S of KolchinskyWolpert18 (Eqs. (9)
and (10))? S is the smallest I_P(X_0; Y_0) over the interventions P that keep V(P) = V(actual). Two sub-questions:
- B2a: inside the Gaussian garblings 0 ⪯ P ⪯ I, do the deterministic ones (the projections) reach the minimum? Is there
  a closed form?
- B2b: can a non-Gaussian intervention (a nonlinear partition of y) reach V(actual) with less information than the
  best Gaussian garbling? This is the gate of `ROADMAP_ABC.md`.

**Candidate closed form (ours).** Let W = Φ_XY Σ_Y^{1/2}: the directions of the environment that drive the agent up to
time τ (whitened y). Let Π_W be the projector on the row space of W. Then P = Π_W keeps Σ_{X_τ} exactly, because
Π_W Wᵀ = Wᵀ. So I_C = I(X_0; Π_W Y_0) = −½ log det(I − C Π_W Cᵀ) is always feasible, and S_G ≤ S_proj ≤ I_C.

**A proof for dx = 1 (ours, a sketch).** With one agent coordinate, Σ_{X_τ}(P) is a scalar affine in cᵀ P w, with c the
whitened cross-covariance and w = Wᵀ. So V(P) = V(I) means cᵀ P w = cᵀ w (if cᵀ w ≠ 0). And I_P grows with ‖P c‖².
Cauchy–Schwarz gives cᵀ w = (P c)ᵀ w ≤ ‖P c‖ ‖w‖, so ‖P c‖² ≥ (cᵀ w)² / ‖w‖². The projection P = w wᵀ / ‖w‖² reaches
this bound. So for dx = 1, **S = I_C = −½ log(1 − (cᵀ ŵ)²)**, with ŵ = w / ‖w‖: the stored semantic information is the
information of the agent about the one direction of the environment that drives it. For dx ≥ 2, the condition
V(P) = V(I) fixes only the determinant of Σ_{X_τ}, not the whole matrix. So the sketch does not carry over.

**Code.** `semantic.drive_projection`, `semantic.drive_information`, `semantic.min_information` (SLSQP with 32 random
starts, plus P = I and P = Π_W, equality tolerance 10⁻⁷ nats). `semantic_nonlinear.py` for B2b (quadrature on grids).
Tests: `tests/test_semantic_b2.py`. Script: `experiments/e21_b2_semantic.py`. τ = 1. Systems as in B1 (stationary
start). Systems with |ΔV| < 10⁻³ nats are skipped and counted.

### B2a: Gaussian garblings (dx = 2, dy = 3, seeds 201 to 250)
- S_G: the minimum over all 0 ⪯ P ⪯ I. S_proj: the minimum over the rank-1 and rank-2 projections, together with P = I
  and P = Π_W.
- **Sanity check (the optimizer is not valid if it fails):** 20 systems with dx = 1 (seeds 401 to 420), where the proof
  above gives S_G = I_C. Pass if |S_G − I_C| ≤ 10⁻⁴ nats in all of them.

| Rule | Question | Verdict |
|---|---|---|
| H1 | Do projections reach the minimum? | "projections suffice" if S_proj − S_G ≤ 10⁻⁴ nats in every system, else "fails in N systems" |
| H2 | Is the drive projection the best projection? | "the drive projection is optimal" if I_C − S_proj ≤ 10⁻⁴ nats in every system, else "fails in N systems" |

Description only: the semantic efficiency S_G / I_act, and the number of starts that reach the best value.

### B2b: non-Gaussian partitions (dx = dy = 1, seeds 301 to 330)
- With dy = 1, the only Gaussian garbling with V(P) = V(I) is P = 1, so S_G = I_act.
- Partitions of y, searched by brute force: one threshold (321 grid points on [−4, 4]), two cells |y| < t and |y| ≥ t
  (200 points on (0, 4]), two thresholds (61 values of t₁ on [−3, 3] times 60 values of t₂ > t₁). Each sign change of
  V − V(actual) between grid neighbours is refined by bisection. S_NG is the smallest I over these roots.

| Rule | Question | Verdict |
|---|---|---|
| H3 | Do partitions fail to beat Gaussian garblings? | "Gaussian garblings are optimal" if S_NG ≥ S_G − 10⁻³ nats in every system (or no partition is feasible), else "not optimal in N systems" |

### What we looked at before writing the rules
- The tests use seeds 901 to 904. They check the code: the proof for dx = 1 holds for the optimizer on one system, and
  the quadrature gives V(full) and V(actual) in its two limits.
- A timing run used the throwaway seeds 998 and 999 with 8 starts. We printed only the time and the names of the
  output fields, not the values.

### Expectations written before the runs
- Sanity: pass (it is a theorem).
- H1: we expect "projections suffice", with low confidence. We have no proof for dx = 2.
- H2: we expect "fails in N systems" with N > 0. The constraint fixes only a determinant, so a rank-1 projection can
  keep V with less information than Π_W.
- H3: we expect "not optimal in N systems" with N > 0. A non-Gaussian X_τ has a lower entropy than a Gaussian with the
  same variance, so V = −H can reach V(actual) with less information. If this happens, the Gaussian value S_G is only
  an upper bound on S over all interventions, as the gate of the roadmap says.

