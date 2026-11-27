"""Linear Gaussian systems dz = -B z dt + sqrt(2 D) dW in the stationary state, and exact tools for them."""
from dataclasses import dataclass, field
import numpy as np
from scipy.linalg import expm, solve_continuous_lyapunov


def stationary_cov(B, D):
    """S with B S + S B^T = 2 D."""
    return solve_continuous_lyapunov(B, 2.0 * D)


def logdet(M):
    s, v = np.linalg.slogdet(M)
    if s <= 0:
        raise ValueError("matrix is not positive definite")
    return v


def propagator(B, D, tau):
    """Phi = exp(-B tau) and Q = int_0^tau e^{-Bs} 2D e^{-B^T s} ds, by the block exponential of Van Loan (1978)."""
    n = B.shape[0]
    M = np.zeros((2 * n, 2 * n))
    M[:n, :n] = B; M[:n, n:] = 2 * D; M[n:, n:] = -B.T
    E = expm(M * tau)
    Phi = E[n:, n:].T
    Q = Phi @ E[:n, n:]
    return Phi, (Q + Q.T) / 2


def mutual_information(S, a, b):
    """I(z_a; z_b) in nats for a Gaussian with covariance S."""
    a, b = list(a), list(b)
    return 0.5 * (logdet(S[np.ix_(a, a)]) + logdet(S[np.ix_(b, b)]) - logdet(S[np.ix_(a + b, a + b)]))


@dataclass
class LinearSystem:
    """One control system. `agent`, `env` and `target` are indices of z. `target` is part of the agent: the
    coordinates whose spread sets the viability (for example v in the homeostat). `uses_information` is the known
    answer of the control."""
    name: str
    B: np.ndarray
    D: np.ndarray
    agent: list
    env: list
    target: list
    uses_information: bool
    meta: dict = field(default_factory=dict)
    S: np.ndarray = None

    def __post_init__(self):
        if self.S is None:
            self.S = stationary_cov(self.B, self.D)

    def cov_at(self, tau, S0=None):
        """Covariance of z_tau when z_0 ~ N(0, S0) (default: the stationary law)."""
        S0 = self.S if S0 is None else S0
        if tau == 0:
            return S0
        Phi, Q = propagator(self.B, self.D, float(tau))
        return Phi @ S0 @ Phi.T + Q
