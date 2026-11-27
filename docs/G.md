# Niche G: transfer entropy and the sensor information of Tanaka

This file starts on 2026-11-27. The plan is in `ROADMAP_DI.md`. Each step writes its rules before its runs, and the
results come after. Notation and code are those of B3 (`docs/B.md`, `src/vlife/semantic_dynamic.py`).

## G0. What we know, and what we saw before the rules

**From B3.** Conjecture B3-T says S_DI ≤ S_TE ≤ D_T*. The second inequality follows if TE ≤ DT at every sensor. F3
proves TE ≤ DT for the first step. B3 tested TE ≤ DT at 1508 sensors, all at τ = 4, and found no failure (smallest
DT − TE: +0.030 nats). The paper of B and C (`paper_bc/main.tex`) says that the bound after the first step is
numerical only.

**An argument against the conjecture (2026-11-27, before any rule).** DT_t = I(Y_0..t; Z_t | Z_0..t−1) conditions on
the full past of the sensor. TE_t = I(Y_t; X_{t+1} | X_t) conditions only on the present agent state. Take an agent
that forgets fast and an environment that changes slowly. Then the past of the sensor fixes y well, and DT_t goes to a
small value. But x_t is a poor record of y, so each step gives new information about y to the agent, and TE_t stays
large. So the sum of TE can grow faster than the sum of DT.

**Probe (2026-11-27, before any rule, not a result).** dx = dy = 1, F = [[0, 1], [0, ρ]], W = diag(0.5, 1 − ρ²),
stationary start, one sensor with gain s = 0.5:

| ρ | DT − TE at τ = 4 | τ = 16 | τ = 64 | τ = 128 |
|---|---|---|---|---|
| 0.99 | +0.643 | +0.795 | +0.869 | +0.963 |
| 0.999 | +0.630 | +0.513 | **−1.383** | **−4.072** |
| 0.9999 | +0.629 | +0.479 | **−1.854** | **−5.417** |

So TE ≤ DT fails at long τ when the environment is slow. The probe used the exact Gaussian code of B3. G1 checks it
with an independent method.

## G1. Independent check of the counterexample: rules (fixed 2026-11-27, before the run)

**Method.** Simulate the intervened process of B3 directly (Eq. (18) of KolchinskyWolpert18 in the Gaussian form of
B3), with 2 × 10^6 independent trajectories in 20 batches of 10^5. At each step, the maps of the intervention come from
the sample covariance of (x_t, y_t), not from the covariance recursion. Estimate each conditional mutual information
from the sample covariance of the whole trajectory, with the Gaussian formula. The standard error comes from the 20
batches. This uses the same model, but not the covariance recursion and not the trajectory covariance of
`semantic_dynamic.py`.

**Systems.** The probe system with ρ = 0.999 and s = 0.5, at τ = 16 and τ = 64.

| Rule | Question | Verdict |
|---|---|---|
| G1a | Do the two methods agree? | "agree" if TE and DT differ by less than 0.02 nats + 3 standard errors, at both τ |
| G1b | Is TE ≤ DT false? | "false" if G1a agrees and the Monte Carlo DT − TE at τ = 64 has a 95 % CI below 0 |

**Expectation.** G1a "agree", G1b "false".

## G2. A map of the failures: rules (fixed 2026-11-27, before the run)

**Systems.** Four families, 5000 systems each, seeds 70001 and up. In each system, 5 random sensors (angles uniform,
gains s uniform on [0, 1 − 10^-6]).
- **R (random, as B3):** F = ρ A / max|eig(A)|, A with normal entries, ρ uniform on [0.3, 0.999]. W diagonal, entries
  uniform on [0.3, 1.5]. dx, dy in {(1, 1), (1, 2), (2, 2)}, in turn.
- **S (slow environment, no feedback):** F_yx = 0. F_yy = ρ_y Q_y, F_xx = ρ_x Q_x, with Q random orthogonal. 1 − ρ_y
  log-uniform on [10^-4, 0.5]. ρ_x uniform on [0, 0.95]. F_xy normal. W_y = (1 − ρ_y²) I, W_x diagonal on [0.3, 1.5].
- **SF (slow environment, with feedback):** as S, but F_yx normal times 0.1, and F scaled down if its spectral radius
  is above 0.9999.
- **M (agent memory):** as S, but ρ_x uniform on [0.9, 0.999].

**Quantities.** For each system and sensor: the cumulative TE(τ) and DT(τ) for τ = 1 to 64, and τ_fail = the first τ
with DT − TE < −10^-6 (or "none"). TE comes from the covariance recursion of B3. DT comes from a Kalman filter on
(x_t, y_t) with the sensor z_t as the measurement: DT_t = ½ log det Cov(z_t | z_0..t−1) − ½ log det Σ_N, because
z_t − K y_t is independent of the rest. This is exact and much faster than the trajectory covariance. Before G2, a test
checks that the two ways give the same DT (within 10^-8 nats) on 50 systems of each family at τ = 16.

| Rule | Question | Verdict |
|---|---|---|
| G2a | Does TE ≤ DT fail at τ ≤ 4 in any system? | "never at τ ≤ 4" if no sensor fails at τ ≤ 4, else "fails at τ ≤ 4 in N systems" |
| G2b | Is the failure linked to a slow environment? | Logistic regression over all systems of "fails by τ = 64" on log(τ_y / τ_x), with τ_y = −1/log ρ_y and τ_x = −1/log ρ_x (for family R: the slowest and the fastest eigenvalue moduli of the blocks F_yy and F_xx). "yes" if the slope is positive with a bootstrap 95 % CI above 0 |
| G2c | Does an agent with a long memory protect the bound? | The fraction of failing systems in M against S, with a bootstrap 95 % CI of the difference. "yes" if M fails less, with the CI below 0 |

**Expectations.** G2a: "never at τ ≤ 4", low confidence (B3 saw no failure at τ = 4). G2b: "yes". G2c: "yes".

## G3. Does S_TE ≤ D_T* still hold? Rules (fixed 2026-11-27, before the run)

**Systems.** Family S with dx = 1, dy = 2, seeds 73001 to 73300 (300 systems). τ in {8, 16, 32, 64}.

**Search.** A grid on the set of sensors with V = V_act: the rotation angle a on 90 points of [0, π), the first gain s_1
on 50 points of [0, 1 − 10^-3], and s_2 by bisection on V(a, s_1, s_2) = V_act (if a root exists in [0, 1 − 10^-3]). On
each point: TE and DT. S_TE^grid and D_T*^grid are the smallest values on the grid. The actual sensor (s = 1) gives TE
and is added for S_TE.

| Rule | Question | Verdict |
|---|---|---|
| G3a | Does S_TE ≤ D_T* hold at each τ? | "holds" if S_TE^grid ≤ D_T*^grid + 10^-4 in all systems with a feasible grid point, else "fails in N systems" (for each τ) |
| G3b | Does the gap grow with τ? | Median of (D_T* − S_TE) over systems at each τ. Descriptive, no verdict |

**Expectation.** G3a: "fails in N systems" with N > 0 at τ = 64, and "holds" at τ = 8. Low confidence: S_TE uses its
own best sensor, which can differ from the best sensor of DT.

**Where it runs.** G1 and G2 run on this PC. G3 runs on the Xeon machines (`cluster/`). G3 uses the Kalman
filter of G2 for DT.
