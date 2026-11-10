"""Physical viability V of a structure, defined from the dynamics WITHOUT information theory.

MFPT viability (implemented)
----------------------------
Viability set of structure A:  V_A = { x_A :  x_A^T S_A^{-1} x_A < c_k },  c_k = chi2_k quantile (1 - p_out)
i.e. the Mahalanobis ball containing a fraction (1 - p_out) of the STATIONARY probability mass,
so structures of different size k are compared at equal occupancy.
Viability V(A) := mean first-passage time (MFPT) out of V_A, started from the stationary
distribution conditioned on being inside V_A.

 * Backward-equation / MFPT theory:   [PontryaginAndronovVitt33, Gardiner04 ch.5, Redner01, HanggiTalknerBorkovec90]
 * Viability-set language:            [Aubin91]  (viability kernel); here the set is chosen operationally.
 * Using a stationary-occupancy-matched Mahalanobis ball as the viability set, and MFPT as the
   'viability' V compared against information functionals:  NOVEL (not found in the literature
   by the authors; see docs/PROVENANCE.md).  Sensitivity to p_out must be reported (E3 does).

Numerics
 * Exact OU propagator x' = exp(-B dt) x + xi, Cov(xi) = S - exp(-B dt) S exp(-B dt)^T  [Gillespie96 for 1-D;
   multivariate form follows from Gardiner04 ch.4.4.6]. No Euler time-stepping error.
 * Exit is only checked on the dt grid, which biases MFPT upward (missed excursions): [Mannella99]. For a 1-D
   barrier the bias is equivalent to moving the boundary outward by ~0.5826*sigma*sqrt(dt) [BroadieGlassermanKou97];
   tests/test_viability.py validates the simulator against the backward equation WITH that shift. The bias is NOT the
   same for every structure: the shift relative to the radius of the set grows like sqrt(theta * dt), theta = relaxation
   rate of the structure, so fast structures are biased more. 1-D OU, dt = 0.05, p_out = 0.05: log V is too high by
   +0.23 at theta = 0.3, +0.42 at theta = 1, +0.71 at theta = 3, +1.21 at theta = 9. In E3 worlds it changes the ranking
   of structures (Spearman 0.85-0.98 against dt = 0.005). See docs/code_review.md, item 1.
   (Earlier text, superseded 2026-11-04: "The bias is systematic (same for every structure at equal dt), so rankings
   are affected much less than absolute values.")
 * Rate estimator with right-censoring at t_max:  V = (total exposure time)/(number of exits)
   (exponential-survival MLE, [CoxOakes84]); equals the plain mean exit time when nothing is censored.
   The exit time from a stationary start is not exactly exponential; V is therefore an OPERATIONAL
   quantity, not a claim about quasi-stationary rates [ColletMartinezSanMartin13 for the latter].
 * Structure-level 'flux ratio'  R = V_driven / V_eq  where V_eq uses the equilibrium counterpart with the same
   stationary law (gaussian.equilibrium_counterpart).  The ratio itself is NOVEL; its motivation is the
   non-reversible-diffusion literature [HwangHwangMaSheu05, LelievreNierPavliotis13, FreidlinWentzell98].

Population-growth-rate viability (implemented in S4, docs/S4.md)
-------------------------------------------------------------------
See GrowthRateViability and docs/ROADMAP.md.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
from scipy.linalg import expm
from scipy.stats import chi2


@dataclass
class ExitData:
    subsets: list
    exit_t: np.ndarray   # (n_traj, S) exit time, = t_max if censored
    event: np.ndarray    # (n_traj, S) bool: exit observed
    valid: np.ndarray    # (n_traj, S) bool: started inside the viability set
    t_max: float
    dt: float
    bridge: bool = False  # Brownian-bridge correction used (fix #1)


def _stack_precisions(S, subsets, p_out):
    N = S.shape[0]
    Q = np.zeros((len(subsets), N, N)); c = np.empty(len(subsets))
    for j, s in enumerate(subsets):
        s = list(s)
        Q[j][np.ix_(s, s)] = np.linalg.inv(S[np.ix_(s, s)])
        c[j] = chi2.ppf(1.0 - p_out, len(s))
    return Q, c


def bridge_crossing_prob(d0, d1, s2):
    """Probability that a Brownian bridge with variance s2 over the step crosses a flat boundary at distances d0, d1 > 0
    from its two end points: exp(-2 d0 d1 / s2) [Mannella99; Giraudo and Sacerdote 1999, Biol. Cybern. 81:525]."""
    return np.exp(-2.0 * d0 * d1 / s2)


def simulate_exits(B, S, subsets, p_out=0.05, n_traj=200, dt=0.05, t_max=100.0, rng=None, bridge=False):
    """Exit times from the viability sets of all subsets (module docstring).
    bridge=True (fix #1, docs/code_review.md): between two checks, a trajectory that is inside at both ends is also
    counted as exited with the Brownian-bridge crossing probability exp(-2 d0 d1 / s2). The boundary is linearised in
    g(x) = sqrt(x_A^T S_A^-1 x_A): d = sqrt(c) - g at each end, s2 = grad g^T (2 D dt) grad g averaged over the two ends,
    with 2D = B S + S B^T (Lyapunov). The exit time stays on the dt grid (end of the step). 1-D check against the backward
    equation at dt = 0.05, p_out = 0.05: error <= 2.1 % for theta = 0.3 to 9, against +24 % to +239 % without the bridge
    (tests/test_bridge.py). bridge=False is the old method and uses the same random numbers as before."""
    rng = np.random.default_rng() if rng is None else rng
    N = S.shape[0]
    Q, c = _stack_precisions(S, subsets, p_out)
    nS = len(subsets)
    Qflat = np.concatenate(list(Q), axis=1)            # (N, nS*N)

    def maha(x):
        y = (x @ Qflat).reshape(x.shape[0], nS, N)
        return (y * x[:, None, :]).sum(-1)

    Phi = expm(-B * dt)
    Cn = S - Phi @ S @ Phi.T
    Cn = (Cn + Cn.T) / 2 + 1e-12 * np.eye(N)
    L = np.linalg.cholesky(Cn)
    x = rng.normal(size=(n_traj, N)) @ np.linalg.cholesky(S).T
    if bridge:
        D2dt = (B @ S + S @ B.T) * dt                   # 2 D dt
        D2dt = (D2dt + D2dt.T) / 2
        sqc = np.sqrt(c)

        def maha_s2(x):
            y = (x @ Qflat).reshape(x.shape[0], nS, N)   # rows: Q_j x (Q_j symmetric)
            q = (y * x[:, None, :]).sum(-1)
            return q, ((y @ D2dt) * y).sum(-1) / np.maximum(q, 1e-300)
        q0, s20 = maha_s2(x)
        valid = q0 < c
    else:
        valid = maha(x) < c
    alive = valid.copy()
    exit_t = np.full((n_traj, nS), float(t_max)); event = np.zeros((n_traj, nS), bool)
    for step in range(1, int(round(t_max / dt)) + 1):
        if not alive.any():
            break
        x = x @ Phi.T + rng.normal(size=(n_traj, N)) @ L.T
        if bridge:
            q1, s21 = maha_s2(x)
            newly = alive & (q1 >= c)
            u = rng.random((n_traj, nS))
            stay = alive & ~newly
            with np.errstate(invalid="ignore"):
                p = bridge_crossing_prob(sqc - np.sqrt(q0), sqc - np.sqrt(q1), 0.5 * (s20 + s21))
            newly |= stay & (u < p)
            q0, s20 = q1, s21
        else:
            newly = alive & (maha(x) >= c)
        exit_t[newly] = step * dt
        event |= newly
        alive &= ~newly
    return ExitData(list(subsets), exit_t, event, valid, t_max, dt, bridge)


def mfpt_from(exit_t, event, valid):
    """Censoring-aware mean first-passage time. Inputs are (n,) arrays. Returns (V, n_events, n_valid).
    With 0 events V = total exposure, a LOWER BOUND, not an estimate; callers must check n_events (the experiments drop
    structures with fewer than 5 exits; ViabilityMeasure.evaluate returns nan for them, docs/code_review.md item 9)."""
    v = valid
    ev = int(event[v].sum())
    exposure = float(exit_t[v].sum())
    return exposure / max(ev, 1), ev, int(v.sum())


def mfpt_all(data: ExitData):
    out = [mfpt_from(data.exit_t[:, j], data.event[:, j], data.valid[:, j]) for j in range(len(data.subsets))]
    V, ev, nv = (np.array(z) for z in zip(*out))
    return V, ev.astype(int), nv.astype(int)


def mfpt_union(data: ExitData, i, j):
    """Survival of the MERGED entity A u B, defined as 'both parts inside their own viability sets'
    (so exit time = min of the parts' exit times). [Definition is ours: NOVEL]"""
    valid = data.valid[:, i] & data.valid[:, j]
    t = np.minimum(data.exit_t[:, i], data.exit_t[:, j])
    ev = data.event[:, i] | data.event[:, j]
    return mfpt_from(t, ev, valid)


# ---------------------------------------------------------------- extension points
class ViabilityMeasure(ABC):
    """Interface so that other viability definitions can be swapped into experiments."""
    name = "abstract"

    @abstractmethod
    def evaluate(self, world, subsets, rng):
        """Return an array of viabilities, one per subset."""


class MFPTViability(ViabilityMeasure):
    """evaluate returns nan for structures with fewer than min_events observed exits (fix #9: V is then censored)."""
    name = "mfpt"

    def __init__(self, min_events=5, **kw):
        self.min_events, self.kw = min_events, kw

    def evaluate(self, world, subsets, rng):
        d = simulate_exits(world.B, world.S, subsets, rng=rng, **self.kw)
        V, ev, _ = mfpt_all(d)
        return np.where(ev >= self.min_events, V, np.nan)


class GrowthRateViability(ViabilityMeasure):
    """Population growth rate r from the survival curve l(a) of a structure (S4, docs/S4.md).

    Birth rule (the same for every structure): constant rate b from maturation age a_m on. Euler-Lotka:
        1 = b * integral_{a_m}^inf exp(-r a) l(a) da      [Lotka1907, Charlesworth94]
    Net reproductive number R0 = b * integral_{a_m}^inf l(a) da. With exponential lives and a_m = 0, r = b - 1/V,
    so r ranks like V. r differs from V only through the shape of l(a).
    l(a) is the fraction of valid trajectories still inside at age a (all censoring is at t_max, so this equals the
    Kaplan-Meier estimate). After t_max the curve continues with hazard 1/V."""
    name = "growth_rate"

    def __init__(self, b=1.0, a_m=0.0, min_events=5, **sim_kw):
        self.b, self.a_m, self.min_events, self.sim_kw = b, a_m, min_events, sim_kw

    @staticmethod
    def survival(exit_t, valid, dt, t_max, event=None):
        """l(a) = fraction of valid trajectories with exit time > a, on the grid 0, dt, ..., t_max.
        Exit times lie on the dt grid, so the comparison uses a tolerance of dt/2: this gives the same curve for float32
        and float64 times. Censored trajectories (event False) are alive at every grid age, also at t_max.
        Fix #7 (docs/code_review.md): the old code used a tolerance of 1e-9 and returned P(T >= a), and with the float32
        times stored by E3 it returned P(T > a) at about 40 % of the grid points."""
        t = np.asarray(exit_t, float)[valid]
        if event is not None:
            t = np.where(np.asarray(event, bool)[valid], t, np.inf)
        t = np.sort(t)
        grid = np.arange(0.0, t_max + dt / 2, dt)
        return grid, 1.0 - np.searchsorted(t, grid + dt / 2, side="right") / len(t)

    def rate(self, exit_t, event, valid, dt, t_max, a_m=None):
        a_m = self.a_m if a_m is None else a_m
        V = mfpt_from(exit_t, event, valid)[0]
        grid, l = self.survival(exit_t, valid, dt, t_max, event)
        m = grid >= a_m - 1e-12; g, lm = grid[m], l[m]
        tail_l, h = l[-1], 1.0 / V

        def laplace(r):        # integral_{a_m}^inf exp(-r a) l(a) da, grid part (trapezoid) + exponential tail
            body = np.trapezoid(np.exp(-r * g) * lm, g) if len(g) > 1 else 0.0
            return body + tail_l * np.exp(-r * t_max) / (r + h)

        from scipy.optimize import brentq
        f = lambda r: self.b * laplace(r) - 1.0
        lo = -h + 1e-9
        r = brentq(f, lo, 100.0) if f(lo) > 0 > f(100.0) else (lo if f(lo) <= 0 else 100.0)
        return float(r), float(self.b * laplace(0.0))

    def from_exits(self, data, a_m=None):
        """Return arrays (r, R0), one value per subset, from ExitData."""
        out = [self.rate(data.exit_t[:, j], data.event[:, j], data.valid[:, j], data.dt, data.t_max, a_m)
               for j in range(len(data.subsets))]
        r, R0 = (np.array(z) for z in zip(*out))
        return r, R0

    def evaluate(self, world, subsets, rng):
        d = simulate_exits(world.B, world.S, subsets, rng=rng, **self.sim_kw)
        ev = d.event.sum(0)            # fix #9: nan when the curve is censored before min_events exits
        return np.where(ev >= self.min_events, self.from_exits(d)[0], np.nan)
