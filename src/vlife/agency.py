"""S3 - a linear homeostat that senses a hidden state and acts against it (docs/S3.md).

Variables (intact):     0 h (hidden state), 1 s (sensor), 2 m (internal state), 3 u (actuator), 4 v (viability variable)
Scrambled adds a copy:  5 h', 6 s', 7 m'   and the actuator reads m' instead of m (same input statistics, no information
about h). Scramble idea: KolchinskyWolpert18. No-feedback version: loop gain L = 0.
All processes are linear OU, dx = -B x dt + sqrt(2D) dW, so every information term is exact (gaussian.py).
The model is our design (docs/PROVENANCE.md row 42)."""
from dataclasses import dataclass
import numpy as np
from scipy.linalg import expm
from .gaussian import stationary_cov

H, S_, M, U, V = 0, 1, 2, 3, 4
ORGANISM = [S_, M, U, V]


@dataclass
class Organism:
    T_h: float
    sigma_s: float
    k_s: float
    k_m: float
    k_u: float
    k_v: float
    L: float


def draw_organism(rng):
    lu = lambda lo, hi: float(np.exp(rng.uniform(np.log(lo), np.log(hi))))
    return Organism(T_h=lu(2, 20), sigma_s=lu(0.1, 3), k_s=lu(0.5, 5), k_m=lu(0.5, 5), k_u=lu(0.5, 5),
                    k_v=lu(0.2, 1), L=float(rng.uniform(0, 1.5)))


def homeostat(o: Organism, version="intact"):
    """Return (B, D, S) for version 'intact', 'scrambled' or 'nofeedback'."""
    n = 8 if version == "scrambled" else 5
    B = np.zeros((n, n)); d = np.zeros(n)

    def chain(h, s, m):
        B[h, h] = 1 / o.T_h; d[h] = 1 / o.T_h                         # var(h) = 1
        B[s, s] = o.k_s; B[s, h] = -o.k_s; d[s] = o.sigma_s ** 2 * o.k_s
        B[m, m] = o.k_m; B[m, s] = -o.k_m; d[m] = 0.01
    chain(H, S_, M)
    L = 0.0 if version == "nofeedback" else o.L
    B[U, U] = o.k_u; B[U, 7 if version == "scrambled" else M] = o.k_u * L; d[U] = 0.01
    B[V, V] = o.k_v; B[V, H] = -1.0; B[V, U] = -1.0; d[V] = 0.05 * o.k_v
    if version == "scrambled":
        chain(5, 6, 7)
    D = np.diag(d)
    return B, D, stationary_cov(B, D)


def simulate_exit_threshold(B, S, idx, c, n_traj=600, dt=0.05, t_max=1000.0, rng=None):
    """Exit times of |x_idx| >= c, started from the stationary law conditioned on |x_idx| < c.
    Exact OU propagator [Gillespie96; Gardiner04]. Returns (V, n_exits, n_valid) with V = exposure / exits [CoxOakes84]."""
    rng = np.random.default_rng() if rng is None else rng
    n = S.shape[0]
    Phi = expm(-B * dt)
    Cn = S - Phi @ S @ Phi.T; Cn = (Cn + Cn.T) / 2 + 1e-12 * np.eye(n)
    Lc = np.linalg.cholesky(Cn)
    x = rng.normal(size=(n_traj, n)) @ np.linalg.cholesky(S).T
    valid = np.abs(x[:, idx]) < c
    alive = valid.copy(); t_exit = np.full(n_traj, float(t_max)); event = np.zeros(n_traj, bool)
    for step in range(1, int(round(t_max / dt)) + 1):
        if not alive.any():
            break
        x = x @ Phi.T + rng.normal(size=(n_traj, n)) @ Lc.T
        out = alive & (np.abs(x[:, idx]) >= c)
        t_exit[out] = step * dt; event |= out; alive &= ~out
    ev = int(event[valid].sum())
    return float(t_exit[valid].sum()) / max(ev, 1), ev, int(valid.sum())
