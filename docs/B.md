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


## B2. Results (added 2026-11-24, after the runs)
Report: `results/e21_b2_semantic.md` and `.json`. Log: `results/e21_run.log`. The run used commit 71fd0b1 (the rules).

| Rule | Verdict | Systems | Expected |
|---|---|---|---|
| Sanity, dx = 1: S_G = I_C | pass, largest gap 1.8·10⁻¹⁰ nats | 19 (1 skipped) | yes |
| H1: projections reach the minimum | **fails in 40 of 48 systems**, largest gap 0.058 nats | 48 (2 skipped) | **no** ("projections suffice", low confidence) |
| H2: the drive projection is the best projection | fails in 47 of 48 systems, largest gap 0.27 nats | 48 | yes |
| H3: partitions do not beat Gaussian garblings | not optimal in 2 of 27 systems | 27 (3 skipped) | yes |

Description:
- Semantic efficiency S_G / I_act (B2a): median 0.25, range 0.002 to 0.98.
- The value of information ΔV is negative in 41 of the 48 B2a systems. With V = −H(X_τ), the actual information makes
  the agent more spread out at time τ than the full scrambling does.
- B2b: in 25 of the 27 systems, no partition of the three families reaches V(actual). In the other 2 (seeds 322 and
  324), a partition reaches it with less information than the Gaussian value: 0.0027 against 0.0043 nats (two
  thresholds), and 0.0008 against 0.0538 nats (|y| < t). In both systems |ΔV| is small (0.004 and 0.001 nats).

**Post-hoc check of H1 (not a rule, `experiments/e21b_posthoc_projection_grid.py`).** A wrong optimizer for the
projections could make H1 fail. A dense grid on the sphere (361 × 181 points, bisection on the level curve) gives the
same S_proj as the optimizer to four decimals in the five systems with the largest gaps. So the failure of H1 is real.

### What B2 shows
1. **For an agent with one coordinate, S has a closed form:** S = −½ log(1 − (cᵀŵ)²), the information of the agent about
   the one direction of the environment that drives it. The proof is short, and the optimizer agrees to 10⁻¹⁰ nats.
2. **For dx ≥ 2, there is no closed form of this kind.** The best Gaussian intervention is usually a noisy garbling,
   not a projection. The drive projection gives only an upper bound I_C ≥ S_G. S_G still needs only an optimization
   over one dy × dy matrix, a few seconds here, not a search over partitions of the state space.
3. **The gate of the roadmap.** Nonlinear partitions beat the Gaussian value in 2 of 27 scalar systems. So over all
   interventions, S_G is an **upper bound** on S, not its exact value. In 25 of 27 systems, no partition that we tried
   reaches V(actual) at all, so in practice S_G was the best value found there.
4. A note for KolchinskyWolpert18: their set Φ holds deterministic coarse-grainings only. In the Gaussian case, the
   noisy garblings reach lower values (H1). So the choice between deterministic and noisy interventions changes the
   value of S. Their paper mentions pre-garbling as the general class, but uses only the deterministic one.

### Limits
- One random construction of systems, τ = 1, dy = 3 (B2a) and dy = 1 (B2b).
- B2b searches three families of partitions only, not all partitions. A wider search can only lower S_NG.
- V = −H(X_τ) follows KolchinskyWolpert18. It rewards a narrow distribution, even a strange one. Part of the B2b
  result comes from this property: a non-Gaussian X_τ has a lower entropy at the same variance.

### Next: B3
The dynamic case: observed semantic information, with interventions at each step, and its link to the minimal directed
information of TanakaEsfahaniMitter18. The rules come first.

## B3. The dynamic case: rules (written 2026-11-24, before the runs)

### What KolchinskyWolpert18 defines (Sec. V B, checked in the PDF text)
- Eq. (16): the transfer entropy TE = Σ_{t=0}^{τ−1} I(X_{t+1}; Y_t | X_t).
- Eqs. (17)–(18): one coarse-graining φ for all times. The intervened channel is p̂(x_{t+1} | x_t, φ(y_t)). It uses
  the actual p(x_{t+1} | x_t, y_t) and the **intervened** joint p̂(x_t, y_t) at time t. The response of the
  environment p(y_{t+1} | x_t, y_t, x_{t+1}) does not change. At t = 0 the intervened joint is the actual one.
- Eqs. (20)–(22): ΔV_obs = V(actual) − V(full scrambling). The optimal intervention has the smallest TE with
  V = V_act. The observed semantic information S_obs is the TE of the optimal intervention.

### Setting (ours)
- Discrete time: z_{t+1} = F z_t + w_t, w_t ~ N(0, W), W = blockdiag(W_x, W_y). Agent x (dx coordinates),
  environment y (dy coordinates). The start z_0 has the stationary law. τ = 4 steps.
- W is block diagonal, so x_{t+1} and y_{t+1} are independent given (x_t, y_t). Thus the intervention keeps
  p(y_{t+1} | x_t, y_t, x_{t+1}), as Eq. (18) requires.

### Gaussian form of Eq. (18) (ours)
One fixed sensor Z_t = K y_t + N_t, N_t ~ N(0, Σ_N), for all t. With the intervened joint law at time t:
- M_t = Cov(y, x) Cov(x)^{-1}, L_t = Cov(y | x)^{1/2}, K_w = K L_t, J_t = K_wᵀ (K_w K_wᵀ + Σ_N)^{-1}, P_t = J_t K_w.
- x_{t+1} = F_xx x_t + F_xy [M_t x_t + L_t (J_t (z_t − K M_t x_t) + e_t)] + w_x, with e_t ~ N(0, I − P_t).
- We use K = diag(√s) Rᵀ and Σ_N = diag(1 − s), with R a rotation and s in [0, 1]^dy. These give every sensor, up to
  an invertible change of z. s = 1 is the actual dynamics. s = 0 is the full scrambling. s in {0, 1}^dy is a
  deterministic coarse-graining φ(y) = Uᵀ y, as in KolchinskyWolpert18.
- The intervened law stays Gaussian. A recursion of the joint covariance gives V and TE exactly.

### Three facts (ours, with proofs)
- **F1. One step does not change the viability.** Under Eq. (18), Σ_y p̂(x' | x, y) p̂(y | x) = Σ_y p(x' | x, y) p̂(y | x).
  So the intervention keeps the law of x_{t+1} given x_t under the intervened joint. At t = 0 the joint is the actual
  one, so p̂(x_1) = p(x_1). Thus ΔV_obs = 0 and S_obs = 0 at τ = 1. This holds for every system, not only Gaussian
  ones. The effect needs τ ≥ 2.
- **F2. The directed information is at most the transfer entropy.** Let DI = Σ_t I(Y_0..t; X_{t+1} | X_0..t). The
  intervened process is Markov in (x_t, y_t), because each step uses new noise. So H(X_{t+1} | X_0..t, Y_0..t) =
  H(X_{t+1} | X_t, Y_t). Also H(X_{t+1} | X_0..t) ≤ H(X_{t+1} | X_t). Thus DI_t ≤ TE_t at each step. Let S_DI be the
  smallest DI with V = V_act. Then S_DI ≤ S_TE.
- **F3. At the first step the sensor carries at least what the agent receives.** Given X_0, the chain
  Y_0 → Z_0 → X_1 holds. So I(Y_0; X_1 | X_0) ≤ I(Y_0; Z_0 | X_0) = I(Y_0; Z_0) − I(X_0; Z_0) ≤ I(Y_0; Z_0). We have
  no proof for t ≥ 1. There, X_t is a noisy record of Z_0..t−1, and the two conditions differ.

### The link to TanakaEsfahaniMitter18
- In Tanaka, the optimal policy is a memoryless linear Gaussian sensor and a Kalman filter. The information is the
  directed information from the source to the sensor output.
- The Gaussian intervention above uses the same class of sensors. But the decoder is the fixed agent (Eq. (18)), not a
  Kalman filter.
- We use the measure of Tanaka on our sensor: DT = Σ_t I(Y_0..t; Z_t | Z_0..t−1). Let D_T* be the smallest DT with
  V = V_act. This is the smallest sensor information, in the measure of Tanaka, that keeps the viability of the agent.
- D_T* is not the problem of Tanaka. Our decoder is fixed, V = −H(X_τ) is not a quadratic cost, τ is finite, and the
  sensor does not change with time.
- A noiseless row of the sensor gives DT = ∞. So D_T* exists only when a noisy sensor reaches V_act.

**Conjecture B3-T.** S_DI ≤ S_TE ≤ D_T*. The first inequality is F2. The second follows if TE ≤ DT at every sensor:
then S_TE ≤ TE(sensor of D_T*) ≤ D_T*. "Equal" means S_TE = D_T*.

### Systems and searches
- Group D1: dx = 1, dy = 2, seeds 501–540. Group D2: dx = 2, dy = 2, seeds 601–630.
- F = 0.85 A / ρ(A), with A a matrix of standard normal entries and ρ the spectral radius. W diagonal, entries
  U(0.3, 1.5). We skip a system if |ΔV_obs| < 10^-3 nats.
- S_TE and S_DI: SLSQP with the constraint V = V_act, from 24 random starts and the start s = 1. The actual sensor is
  always added.
- D_T*: SLSQP from 8 random starts, at most 100 iterations, s ≤ 1 − 10^-6. D_T* is "attained" if all s ≤ 1 − 10^-3.
  Otherwise the search goes to a noiseless row, and we report D_T* as not attained (infinite).
- S_proj (dy = 2): the rank-1 coarse-grainings φ(y) = cos(a) y_1 + sin(a) y_2 with V = V_act. We find the roots in a
  on a grid of 360 points in [0, π), with bisection. We add the actual sensor (rank 2).
- Points for T1 and H3: 20 random noisy sensors (s ≤ 1 − 10^-6) and the optima of the three searches.

### Rules
| Rule | Pass condition |
|---|---|
| Sanity A | At τ = 1, five random sensors in each system give |V − V_act| < 10^-10. If it fails, the recursion is wrong and we stop. |
| Sanity T1 | TE − DI ≥ −10^-10 at all tested points. If it fails, the code or the proof F2 is wrong. |
| H1 | Projections suffice: S_proj − S_TE ≤ 10^-4 in all systems. |
| H2 | The actual sensor is not optimal: S_TE < TE_act − 10^-4 in all systems. |
| H3 | TE ≤ DT + 10^-10 at all tested noisy sensors, in all systems. |
| H4 | D_T* is attained and D_T* − S_TE ≤ 10^-4, in all systems. |

**Statement for the roadmap.** If H4 holds: "equal". If H3 holds and H4 fails: "a bound, S_DI ≤ S_TE ≤ D_T*". If H3
fails: "false as a bound", with the systems where TE > DT.

### Expectations (before the runs)
- Sanity A and T1: pass (F1 and F2).
- H1: fails. In B2 noisy garblings beat projections.
- H2: for dx = 1, the agent reads one direction g = P w of the environment, with w the drive. TE depends only on |g|,
  but V also depends on the direction of g. So the set V = V_act generally contains sensors with a smaller |g|. We
  expect H2 to hold in D1. In D2 it fails at least once: the trial seed 998 (below) has S_TE = TE_act.
- H3: F3 proves the first step. We expect H3 to hold, with low confidence.
- H4: fails. The trial seeds give D_T* well above S_TE, or not attained.

### What we saw before the rules
We ran the code on three seeds outside the two groups (997, 998, 999), to measure the time.
| Seed | dx | TE_act | S_TE | D_T* |
|---|---|---|---|---|
| 999 | 1 | 2.937 | 0.434 | 2.234 |
| 997 | 2 | 1.458 | 0.203 | 3.329 |
| 998 | 2 | 0.437 | 0.437 (the actual sensor) | not attained (the search ends at s = 1 − 10^-6, value 55.7) |

On seed 998 the D_T* search took 110 s for 8 starts, and 189 s for 4 starts with 300 iterations. So we set the D_T*
search to 8 starts and 100 iterations. We made this choice after the trials and before the runs on the two groups.

### Limits
- Gaussian sensors only. KolchinskyWolpert18 uses deterministic φ, and B2 showed that a non-Gaussian φ can do better.
  So S_TE is an upper bound over all interventions, as in B2.
- The sensor does not change with time, as in KolchinskyWolpert18. A sensor that changes with time can do better. For
  example, by F1 it can fully scramble the last step at no cost.
- One value of τ and one family of F.

**Code.** `src/vlife/semantic_dynamic.py`. Tests: `tests/test_semantic_b3.py` (7 tests: the actual sensor keeps the
stationary law, the full scrambling gives TE = 0, F1, the trajectory covariance against the recursion, F2, a sampling
check of Eq. (18) that gets p̂(y | x, z) by regression on the samples, and the feasibility of the search results).
Run: `experiments/e22_b3_observed.py`.

## B3. Results (run 2026-11-24, `results/e22_b3_observed.md`, log `results/e22_run.log`)

69 of 70 systems count. We skipped seed 502 (|ΔV_obs| = 0.0005).

| Rule | Result | Expectation |
|---|---|---|
| Sanity A | Pass. The largest gap is 8.9e-16 nats. | pass, correct |
| Sanity T1 | Pass. The smallest TE − DI is 5.7e-7 nats. | pass, correct |
| H1 | Fails in 31 of 69: 14 of 39 in D1, 17 of 30 in D2. | fails, correct |
| H2 | Holds in all 39 of D1. Fails in 10 of 30 of D2, where S_TE = TE_act. | correct for both groups |
| H3 | Holds at all 1508 tested sensors. The smallest DT − TE is +0.030 nats. | holds, correct |
| H4 | Fails in all 69. D_T* is not attained in 11 systems. | fails, correct |

**Statement for the roadmap: a bound, S_DI ≤ S_TE ≤ D_T*, not equal.** The first inequality is the theorem F2. The
second is a numerical result at 1508 sensors, and F3 proves it only for the first step.

### Description
- Size of the H1 failures. In D1 they are small: the median gap is 0.0006 nats, the largest 0.11 nats. In D2 they
  are large: the median gap is 0.11 nats, the largest 0.63 nats.
- Semantic efficiency S_TE / TE_act: median 0.56 in D1, 0.68 in D2. The range is 0.001 to 1.
- S_DI / S_TE: median 0.84 in D1, 0.75 in D2, smallest 0.47. So the choice of the measure matters.
- S_TE / D_T*, where D_T* is attained: median 0.15 in D1, 0.17 in D2, largest 0.47. The sensor must carry about six
  times more information than the agent uses.
- In D2, the 10 systems where the actual sensor is optimal (H2 fails) are the same 10 systems where D_T* is not
  attained. In D1, D_T* is not attained only in seed 536. We have no proof of this link. A possible reason: if no
  sensor with less TE reaches V_act, the feasible set stays near the noiseless actual sensor.
- Search quality: in D1 at least 10 starts end at the best S_TE. In D2 the smallest count is 2 starts.

### What B3 means
1. **One step is never enough.** The observed semantic information of KolchinskyWolpert18 is zero at τ = 1 in every
   system (F1). It comes from correlations that the agent builds over two or more steps.
2. **An agent with one variable always uses more transfer entropy than it needs.** In D1 the actual sensor is never
   optimal. With two variables this is not always true.
3. **The link to Tanaka is a bound, not an equality.** The smallest sensor information in the measure of Tanaka is
   always larger than the observed semantic information, about six times in the median. The fixed agent loses most
   of what the sensor gives.

### Limits
- The bound S_TE ≤ D_T* is numerical after the first step. A proof or a counterexample is open.
- D_T* uses a fixed decoder, so it is not the problem of Tanaka. With a Kalman filter as decoder, the gap can be
  smaller.
- Gaussian sensors that do not change with time, τ = 4, one family of F. The D_T* search has a limit of 8 starts and
  100 iterations, so a D_T* value can be too high. This does not change H3, which we test at each sensor.

### Next: B4
Apply the method: (a) the S3 homeostat, the semantic threshold against our VoI, (b) the S1 worlds, semantic
information against Φ_TC. The rules come first.
