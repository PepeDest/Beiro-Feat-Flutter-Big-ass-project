"""Organisational features of a candidate structure A (a subset of the N variables).

Environment := the complement X = Omega \\ A   (this fixes the 'exogenous E_t' inconsistency of the
original proposal; docs/THEORY.md sec 1).  All information quantities are in NATS, all from
closed-form Gaussian expressions (gaussian.py).

Features
  C    = I(A_t ; A_{t+tau})            internal coherence       [project hypothesis]
  P    = I(A_t ; X_{t+tau})            predictive information about the rest   [BialekNemenmanTishby01 style]
  IAX  = I(A_t ; X_t)                  present-environment coupling
         (IAX - P is the 'non-predictive information' of Still et al. [Still12]; see caveat below)
  KH   = h(A_t)                        differential entropy ('complexity' K of the original proposal)
  leak = I(A_{t+tau}; X_t | A_t)       one-step transfer entropy X->A [Schreiber00]: lack of informational closure
         (closure idea: BertschingerOlbrichAyJost08; this exact scalar is our simplification)
Phi_orig = P + beta*C - lambda*KH      the project's original functional (hypothesis, not established).

Caveat (honest): Still12's bound is derived for a system driven by an EXOGENOUS signal. Here A and X
are mutually coupled, so IAX - P is used as an analogy only. [Novel extension; unproven.]
"""
from itertools import combinations
import numpy as np
from .gaussian import (joint_cov, mutual_information, conditional_mutual_information,
                       differential_entropy)

FEATURES = ("P", "C", "KH", "IAX")


def all_subsets(N):
    """All non-empty PROPER subsets (the complement must be non-empty)."""
    return [s for k in range(1, N) for s in combinations(range(N), k)]


def merge_pairs(subsets, N, max_size=5):
    """All unordered pairs (a, b) of disjoint structures whose union is a proper subset of size <= min(max_size, N - 1).
    Each pair appears once (itertools.combinations). E4 used to drop pairs with min(a) > min(b) as well, which removed
    54 % of the eligible pairs for N = 6, depending on the variable index (docs/code_review.md, item 2)."""
    limit = min(max_size, N - 1)
    return [(a, b) for a, b in combinations(subsets, 2) if not set(a) & set(b) and len(a) + len(b) <= limit]


def structure_features(world, tau, subsets=None):
    N = world.N
    subsets = all_subsets(N) if subsets is None else subsets
    J = joint_cov(world.B, world.S, tau)
    out = {k: np.empty(len(subsets)) for k in ("C", "P", "IAX", "KH", "leak", "size")}
    for j, s in enumerate(subsets):
        c = [i for i in range(N) if i not in s]
        At, At1 = list(s), [N + i for i in s]
        Xt, Xt1 = c, [N + i for i in c]
        out["C"][j] = mutual_information(J, At, At1)
        out["P"][j] = mutual_information(J, At, Xt1)
        out["IAX"][j] = mutual_information(J, At, Xt)
        out["KH"][j] = differential_entropy(J, At)
        out["leak"][j] = conditional_mutual_information(J, At1, Xt, At)
        out["size"][j] = len(s)
    out["subsets"] = subsets
    return out


def static_mi(world, A, B):
    """I(A_t ; B_t) for disjoint index tuples (same time). Used for the merge baseline."""
    return mutual_information(world.S, list(A), list(B))


def phi_orig(feat, beta=1.0, lam=0.25):
    """Original proposal: Phi = P + beta*C - lambda*K, with K = h(A_t)  (hypothesis)."""
    return feat["P"] + beta * feat["C"] - lam * feat["KH"]
