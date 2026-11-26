"""Stored semantic information of KolchinskyWolpert18 applied to our earlier systems (niche B, step B4, docs/B.md):
(a) the S3 homeostat (agency.py), (b) the structures of the S1 worlds (worlds.py).

The functions of semantic.py need the agent in the first coordinates. Here `agent` and `env` are index lists in the
original order, and we permute B, D and S0 before the call. Viability V = -H(X_tau) on a `target` subset of the agent
(the whole agent by default, as in KolchinskyWolpert18, Eq. (2)). Our code. Checks: tests/test_semantic_b4.py.
"""
import numpy as np
from vlife.semantic import (propagator, intervened_cov, syntactic_information, drive_information, min_information,
                            _logdet)


def permute(B, D, S0, agent, env):
    """B, D, S0 with the agent first, then the environment."""
    p = list(agent) + list(env)
    ix = np.ix_(p, p)
    return B[ix], D[ix], S0[ix]


def viability_target(B, D, S0, dx, P, tau, target):
    """-H of the coordinates `target` (local indices in the agent) at time tau, intervention P (agent first)."""
    Phi, Q = propagator(B, D, tau)
    St = Phi @ intervened_cov(S0, dx, P) @ Phi.T + Q
    t = list(target)
    return -0.5 * (len(t) * np.log(2 * np.pi * np.e) + _logdet(St[np.ix_(t, t)]))


def value_on(B, D, S0, agent, env, tau, target=None):
    """Delta V = V(P = I) - V(P = 0) [KolchinskyWolpert18, Eq. (6)], V on `target` (local indices, default all)."""
    Bp, Dp, Sp = permute(B, D, S0, agent, env)
    dx, dy = len(agent), len(env)
    t = range(dx) if target is None else target
    return (viability_target(Bp, Dp, Sp, dx, np.eye(dy), tau, t)
            - viability_target(Bp, Dp, Sp, dx, np.zeros((dy, dy)), tau, t))


def half_value_information(B, D, S0, agent, env, tau, target):
    """dy = 1 and one target coordinate only. Var(target at tau) = a + b p is affine in the scalar intervention p, so
    V(p) = -1/2 log(a + b p) + const. Returns (p_half, R_half, I_act): p_half solves V(p) = (V(0) + V(1)) / 2, and
    R_half = I_p at p_half. None for p_half and R_half when b = 0."""
    Bp, Dp, Sp = permute(B, D, S0, agent, env)
    dx = len(agent)
    Phi, Q = propagator(Bp, Dp, tau)
    var = lambda p: (Phi @ intervened_cov(Sp, dx, np.array([[p]])) @ Phi.T + Q)[target, target]
    a = var(0.0); b = var(1.0) - a
    I_act = syntactic_information(Sp, dx, np.eye(1))
    if abs(b) < 1e-14 * max(abs(a), 1e-300):
        return None, None, float(I_act)
    p = (np.sqrt(a * (a + b)) - a) / b
    return float(p), float(syntactic_information(Sp, dx, np.array([[p]]))), float(I_act)


def stored_semantic(B, D, S0, agent, env, tau, n_starts=8, rng=None, n_grid=200, iters=50, target=None):
    """S_G [KolchinskyWolpert18, Eqs. (9)-(10)] over Gaussian garblings, V = -H(X_tau) of the whole agent, or of the
    `target` coordinates (local indices in the agent, dy = 1 only; added for niche C, docs/C.md).
    dx = 1: S_G = I_C, the drive information (B2 theorem). dy = 1: the roots of V(p) = V_act on a grid of [0, 1] with
    bisection, and S_G = I at the smallest root (I_p grows with p). Else: min_information of semantic.py, family
    "general". Returns (S_G, method)."""
    Bp, Dp, Sp = permute(B, D, S0, agent, env)
    dx, dy = len(agent), len(env)
    if target is not None and dy != 1:
        raise ValueError("target needs dy = 1")
    if dx == 1:
        return float(drive_information(Bp, Dp, Sp, 1, tau)), "drive (dx = 1)"
    if dy == 1:
        t = range(dx) if target is None else list(target)
        V = lambda p: viability_target(Bp, Dp, Sp, dx, np.array([[p]]), tau, t)
        V_act = V(1.0)
        g = lambda p: V(p) - V_act
        grid = np.linspace(0.0, 1.0, n_grid + 1)
        vals = [g(p) for p in grid[:-1]]
        for i in range(n_grid - 1):                      # the last cell ends at p = 1, a root of g by definition
            lo, hi, flo = grid[i], grid[i + 1], vals[i]
            if flo == 0.0:
                return float(syntactic_information(Sp, dx, np.array([[lo]]))), "root (dy = 1)"
            if np.sign(flo) == np.sign(vals[i + 1]):
                continue
            for _ in range(iters):
                mid = (lo + hi) / 2; fm = g(mid)
                lo, hi, flo = (mid, hi, fm) if np.sign(fm) == np.sign(flo) else (lo, mid, flo)
            return float(syntactic_information(Sp, dx, np.array([[(lo + hi) / 2]]))), "root (dy = 1)"
        return float(syntactic_information(Sp, dx, np.eye(1))), "root (dy = 1): only p = 1"
    best, _, _, _ = min_information(Bp, Dp, Sp, dx, tau, "general", n_starts, rng)
    return float(best), "search"
