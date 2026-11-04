"""Closed-form information and thermodynamic quantities for stationary Ornstein-Uhlenbeck (OU) worlds.

World:  dx = -B x dt + sqrt(2 D) dW      (B: drift matrix, D: diffusion matrix, both N x N)
Everything here is exact (no sampling), which is why the linear-Gaussian family is the
validation ground for the whole project.

Provenance tags in brackets refer to docs/REFERENCES.md; see docs/PROVENANCE.md for status.
"""
import numpy as np
from scipy.linalg import solve_continuous_lyapunov, expm


def stationary_cov(B, D):
    """Stationary covariance S solving  B S + S B^T = 2 D  (continuous Lyapunov equation).
    [Gardiner04 ch.4.4.6 / Risken89 ch.6; solver: BartelsStewart72 via scipy]"""
    return solve_continuous_lyapunov(B, 2.0 * D)


def lagged_cov(B, S, tau):
    """C(tau) = E[x_{t+tau} x_t^T] = exp(-B tau) S   for a stationary OU process.
    [Gardiner04 ch.4.4.6 (regression theorem); Risken89 ch.6]"""
    return expm(-B * tau) @ S


def joint_cov(B, S, tau):
    """Covariance of the stacked vector z = (x_t ; x_{t+tau}) (size 2N).
    Cov(x_{t+tau}, x_t) = C(tau)  [Gardiner04 ch.4.4.6]."""
    C = lagged_cov(B, S, tau)
    return np.block([[S, C.T], [C, S]])


def _logdet(M):
    sign, ld = np.linalg.slogdet(M)
    if sign <= 0:
        raise np.linalg.LinAlgError("covariance block not positive definite")
    return ld


def mutual_information(cov, a, b):
    """I(a;b) in NATS for jointly Gaussian variables: 0.5*log( det S_a det S_b / det S_ab ).
    [CoverThomas06 ch.8 (Gaussian entropy) and ch.2 (I = h(a)+h(b)-h(a,b))]"""
    a, b = list(a), list(b)
    return 0.5 * (_logdet(cov[np.ix_(a, a)]) + _logdet(cov[np.ix_(b, b)])
                  - _logdet(cov[np.ix_(a + b, a + b)]))


def conditional_mutual_information(cov, a, b, c):
    """I(a;b|c) in nats (Gaussian). [CoverThomas06 ch.2 chain rule + ch.8]"""
    a, b, c = list(a), list(b), list(c)
    if not c:
        return mutual_information(cov, a, b)
    ac, bc, abc = a + c, b + c, a + b + c
    return 0.5 * (_logdet(cov[np.ix_(ac, ac)]) + _logdet(cov[np.ix_(bc, bc)])
                  - _logdet(cov[np.ix_(c, c)]) - _logdet(cov[np.ix_(abc, abc)]))


def differential_entropy(cov, idx):
    """h(x_idx) = 0.5*( k log(2 pi e) + log det S_idx ) in nats. [CoverThomas06 Thm 8.4.1]
    NOTE: differential entropy is NOT invariant under rescaling of x (see docs/LIMITATIONS.md)."""
    idx = list(idx)
    return 0.5 * (len(idx) * np.log(2 * np.pi * np.e) + _logdet(cov[np.ix_(idx, idx)]))


def entropy_production(B, D, S):
    """Steady-state entropy production rate (units of k_B per time) of a linear OU process:
        sigma = tr( M^T D^{-1} M S ),   M = B - D S^{-1}.
    Derivation: stationary probability current J = -M x p, sigma = int J^T D^{-1} J / p dx.
    Zero iff detailed balance (M = 0).
    [Standard form for Fokker-Planck systems: Tome06, SpinneyFord12. The specialisation to the
     linear case written here is a short derivation (docs/THEORY.md sec 2), not copied from a paper.]"""
    M = B - D @ np.linalg.inv(S)
    return float(np.trace(M.T @ np.linalg.inv(D) @ M @ S))


def equilibrium_counterpart(D, S):
    """Drift matrix B_eq = D S^{-1}: a detailed-balance (reversible) dynamics with THE SAME
    stationary distribution N(0,S) as the driven system. Check: B_eq S + S B_eq^T = 2D.
    Comparing driven vs this counterpart isolates the effect of irreversibility at fixed static statistics.
    [Idea of comparing irreversible vs reversible diffusions with the same invariant measure:
     HwangHwangMaSheu93, HwangHwangMaSheu05, LelievreNierPavliotis13 (convergence rates).
     Applying it to EXIT TIMES of structures is our use: see PROVENANCE 'flux ratio'.]"""
    return D @ np.linalg.inv(S)


def total_correlation(cov, idx):
    """Multi-information (total correlation) TC = sum_i h(x_i) - h(x_idx) = -0.5*log det R_idx in nats,
    R = correlation matrix. Does not change when single variables are rescaled (unlike differential_entropy).
    Zero for one variable. [Watanabe60; Gaussian form from CoverThomas06 Thm 8.4.1]. Used in S1b (docs/S1b_unitfree.md)."""
    idx = list(idx)
    sub = cov[np.ix_(idx, idx)]
    return 0.5 * (float(np.sum(np.log(np.diag(sub)))) - _logdet(sub))


def structure_entropy_production(B, D, S, idx):
    """Part of the steady-state entropy production along the coordinates idx (diagonal D):
    sigma_A = sum_{i in A} (M S M^T)_ii / D_ii, M = B - D S^{-1}. The sum over all coordinates is entropy_production().
    Decomposition: our algebra (docs/S2c.md); total form [Tome06, SpinneyFord12]."""
    M = B - D @ np.linalg.inv(S)
    q = np.diag(M @ S @ M.T) / np.diag(D)
    return float(np.sum(q[list(idx)]))
