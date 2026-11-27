"""Niche D (docs/D.md): the two models of the Rochester group, written again from the papers.

forager_run: the foraging agent of Sowinski23 (Appendix B, Table II). kuramoto_run: the Kuramoto agent of
SowinskiFrankGhoshal24 (Sec. III, Appendix A). The choices where the papers say nothing are in docs/D.md, D0.
Both functions use numba and a seed for each run, so each run gives the same result on each machine.
"""
import numpy as np
from numba import njit

# ------------------------------------------------------------------ Sowinski23: foraging agent
# modes: 0 = normal (heading noise uniform on [-pi*eta, pi*eta]), 1 = deaf (never turns)
FORAGER = dict(r=1.0, mu=1.0, eps=0.1, gamma=0.1, Gamma=0.001, L=100.0, dt=0.02, s0=0.5, n0=1000)


@njit(cache=True)
def forager_run(v, R, eta, mode, seed, t_max=1.0e4, s_cap=1.0, r=1.0, mu=1.0, eps=0.1, gamma=0.1, Gamma=0.001,
                L=100.0, dt=0.02, s0=0.5, n0=1000):
    """One life. s_cap: the fuel never goes above it (S = 1 of Table II, or np.inf for no cap).
    Returns (T, censored, n_harvest, n_lock)."""
    np.random.seed(seed)
    cap = 8 * n0 + 64
    rx = np.empty(cap); ry = np.empty(cap)
    n = n0
    for k in range(n):
        rx[k] = np.random.random() * L; ry[k] = np.random.random() * L
    x = 0.5 * L; y = 0.5 * L
    a = np.random.random() * 2.0 * np.pi
    hx = np.cos(a); hy = np.sin(a)
    s = s0; tau = 0; t = 0.0
    p_decay = 1.0 - np.exp(-gamma * dt)
    lam = Gamma * L * L * dt / eps
    n_h = 0; n_l = 0
    r2 = r * r; R2 = R * R
    max_steps = int(t_max / dt)
    for _ in range(max_steps):
        if s <= 0.0:
            return t, False, n_h, n_l
        # nearest resource
        kb = -1; db = 1e300
        for k in range(n):
            dx = rx[k] - x; dy = ry[k] - y
            d = dx * dx + dy * dy
            if d < db:
                db = d; kb = k
        if kb >= 0 and db <= r2:                       # harvest, no move, no cost
            s = min(s + eps, s_cap); tau = 0; n_h += 1
            n -= 1; rx[kb] = rx[n]; ry[kb] = ry[n]
        else:
            if tau == 0 and mode == 0 and kb >= 0 and db <= R2:
                tau = 1; n_l += 1
                a = np.arctan2(ry[kb] - y, rx[kb] - x)
                if eta > 0.0:
                    a += (2.0 * np.random.random() - 1.0) * np.pi * eta
                hx = np.cos(a); hy = np.sin(a)
            s -= mu * dt
            x += v * hx * dt; y += v * hy * dt
            if x < 0.0:
                x = -x; hx = -hx
            elif x > L:
                x = 2.0 * L - x; hx = -hx
            if y < 0.0:
                y = -y; hy = -hy
            elif y > L:
                y = 2.0 * L - y; hy = -hy
        # environment: decay, then growth
        k = 0
        while k < n:
            if np.random.random() < p_decay:
                n -= 1; rx[k] = rx[n]; ry[k] = ry[n]
            else:
                k += 1
        m = np.random.poisson(lam)
        for _j in range(m):
            if n < cap:
                rx[n] = np.random.random() * L; ry[n] = np.random.random() * L; n += 1
        t += dt
    return t, True, n_h, n_l


@njit(cache=True)
def forager_batch(v, R, eta, mode, seeds, t_max=1.0e4, s_cap=1.0):
    """One run for each seed in `seeds` (uint32 array)."""
    n_runs = seeds.size
    T = np.empty(n_runs); C = np.zeros(n_runs, np.bool_); H = np.empty(n_runs); K = np.empty(n_runs)
    for i in range(n_runs):
        T[i], C[i], H[i], K[i] = forager_run(v, R, eta, mode, seeds[i], t_max, s_cap)
    return T, C, H, K


def seeds_for(key, n):
    """n independent uint32 seeds for a task key (a tuple of ints)."""
    return np.random.SeedSequence(list(key)).generate_state(n).astype(np.int64)


def forager_eta_grid():
    """The 200 values of eta of Sowinski23 (Appendix B)."""
    return np.concatenate([np.linspace(0.0, 0.15, 100, endpoint=False), np.geomspace(0.15, 1.0, 100)])


# ------------------------------------------------------------------ SowinskiFrankGhoshal24: Kuramoto agent
def graph_csr(kind, N, k_mean, rng):
    """(indptr, indices, N_used) of an undirected simple graph. kind: 'fc', 'poisson' (G(N, k/N)) or 'sf'
    (configuration model, P(k) ~ k^-2.5, 2 <= k <= 100). For 'poisson' and 'sf': the giant component only."""
    if kind == "fc":
        return None, None, N
    if kind == "poisson":
        p = k_mean / (N - 1)
        iu, ju = np.triu_indices(N, 1)
        keep = rng.random(iu.size) < p
        edges = np.stack([iu[keep], ju[keep]], 1)
    elif kind == "sf":
        ks = np.arange(2, 101); pk = ks.astype(float) ** -2.5; pk /= pk.sum()
        deg = rng.choice(ks, size=N, p=pk)
        if deg.sum() % 2:
            deg[rng.integers(N)] += 1
        stubs = np.repeat(np.arange(N), deg); rng.shuffle(stubs)
        e = stubs.reshape(-1, 2)
        e = e[e[:, 0] != e[:, 1]]
        e = np.unique(np.sort(e, 1), axis=0)
        edges = e
    else:
        raise ValueError(kind)
    import scipy.sparse as sp
    from scipy.sparse.csgraph import connected_components
    A = sp.coo_matrix((np.ones(len(edges)), (edges[:, 0], edges[:, 1])), shape=(N, N))
    A = ((A + A.T) > 0).astype(np.int8).tocsr()
    nc, lab = connected_components(A, directed=False)
    big = np.argmax(np.bincount(lab))
    idx = np.flatnonzero(lab == big)
    A = A[idx][:, idx].tocsr()
    return A.indptr.astype(np.int64), A.indices.astype(np.int64), len(idx)


@njit(cache=True)
def _rhs(theta, omega, coup, fc, indptr, indices, out, c, sn):
    N = theta.size
    for j in range(N):
        c[j] = np.cos(theta[j]); sn[j] = np.sin(theta[j])
    if fc:
        zr = 0.0; zi = 0.0
        for j in range(N):
            zr += c[j]; zi += sn[j]
        for i in range(N):
            # sum_j sin(theta_j - theta_i) = Im(Z e^{-i theta_i})
            out[i] = omega[i] + coup * (zi * c[i] - zr * sn[i])
    else:
        for i in range(N):
            acc = 0.0
            for p in range(indptr[i], indptr[i + 1]):
                j = indices[p]
                acc += sn[j] * c[i] - c[j] * sn[i]
            out[i] = omega[i] + coup * acc


@njit(cache=True)
def kuramoto_run(coup, fc, indptr, indices, N, eta, alpha, beta, agent, seed, n_trans=1500, n_avg=512, dt=1.0 / 16):
    """One run. coup = sigma (graphs) or K/N (fully connected). agent: 0 none, 1 agent, 2 still (reads, no kick).
    Returns (mean r over the last n_avg steps, mean information per kick in bits, number of kicks)."""
    np.random.seed(seed)
    theta = np.empty(N); omega = np.empty(N)
    for i in range(N):
        theta[i] = (2.0 * np.random.random() - 1.0) * np.pi
        omega[i] = np.random.standard_normal()
    k1 = np.empty(N); k2 = np.empty(N); k3 = np.empty(N); k4 = np.empty(N); tmp = np.empty(N); c = np.empty(N); sn = np.empty(N)
    node = np.random.randint(N)
    lam = beta * N * dt
    r_sum = 0.0; info_sum = 0.0; n_k = 0
    for step in range(n_trans + n_avg):
        _rhs(theta, omega, coup, fc, indptr, indices, k1, c, sn)
        for i in range(N):
            tmp[i] = theta[i] + 0.5 * dt * k1[i]
        _rhs(tmp, omega, coup, fc, indptr, indices, k2, c, sn)
        for i in range(N):
            tmp[i] = theta[i] + 0.5 * dt * k2[i]
        _rhs(tmp, omega, coup, fc, indptr, indices, k3, c, sn)
        for i in range(N):
            tmp[i] = theta[i] + dt * k3[i]
        _rhs(tmp, omega, coup, fc, indptr, indices, k4, c, sn)
        for i in range(N):
            theta[i] += dt / 6.0 * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i])
        if agent > 0:
            Zr = 0.0; Zi = 0.0
            if fc:
                for j in range(N):
                    Zr += np.cos(theta[j]); Zi += np.sin(theta[j])
            nj = np.random.poisson(lam)
            for _j in range(nj):
                # local mean field of the node (neighbours; all other nodes if fully connected)
                zr = 0.0; zi = 0.0
                if fc:                                          # global field kept up to date, minus the node
                    zr = Zr - np.cos(theta[node]); zi = Zi - np.sin(theta[node])
                else:
                    for p in range(indptr[node], indptr[node + 1]):
                        zr += np.cos(theta[indices[p]]); zi += np.sin(theta[indices[p]])
                phi = np.arctan2(zi, zr)
                d = theta[node] - phi
                d = np.arctan2(np.sin(d), np.cos(d))            # in (-pi, pi]
                kappa = 1.0 if np.sin(d) > 0.0 else -1.0
                phih = phi + (2.0 * np.random.random() - 1.0) * np.pi * eta
                kh = 1.0 if np.sin(theta[node] - phih) > 0.0 else -1.0
                # information of this kick: 1 - h2(p_flip), Sec. III.4 of SowinskiFrankGhoshal24
                ec = min(abs(d) / np.pi, 1.0 - abs(d) / np.pi)
                if eta <= ec:
                    pf = 0.0
                elif eta < 1.0 - ec:
                    pf = 0.5 * (1.0 - ec / eta)
                else:
                    pf = 1.0 - 1.0 / (2.0 * eta)
                h = 0.0
                if 0.0 < pf < 1.0:
                    h = -(pf * np.log2(pf) + (1.0 - pf) * np.log2(1.0 - pf))
                info_sum += 1.0 - h; n_k += 1
                if agent == 1:
                    if fc:
                        Zr -= np.cos(theta[node]); Zi -= np.sin(theta[node])
                    theta[node] += alpha * kh
                    if fc:
                        Zr += np.cos(theta[node]); Zi += np.sin(theta[node])
                # jump
                if fc:
                    nxt = np.random.randint(N - 1)
                    node = nxt if nxt < node else nxt + 1
                else:
                    deg = indptr[node + 1] - indptr[node]
                    node = indices[indptr[node] + np.random.randint(deg)]
        if step >= n_trans:
            zr = 0.0; zi = 0.0
            for j in range(N):
                zr += np.cos(theta[j]); zi += np.sin(theta[j])
            r_sum += np.sqrt(zr * zr + zi * zi) / N
    return r_sum / n_avg, (info_sum / n_k if n_k > 0 else np.nan), n_k
