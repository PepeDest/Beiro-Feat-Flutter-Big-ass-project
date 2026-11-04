"""S5 - planted structures and Markov-blanket detectors (docs/S5.md).

Static detector: zeros of the stationary precision (conditional independence in the stationary law) [Pearl88, Friston13].
Dynamic detector: zeros of the drift matrix, B_hat = -logm(C(delta) S^-1)/delta, exact for an OU process
(C(delta) = expm(-B delta) S, gaussian.lagged_cov). In driven worlds the two differ [AguileraMillidgeTschantzBuckley22]."""
import numpy as np
from scipy.linalg import expm, logm
from .gaussian import stationary_cov

N_ORG, K_INT, K_BL, N_BG = 2, 3, 3, 12


def make_planted_world(family, rng):
    N = N_ORG * (K_INT + K_BL) + N_BG
    adj = np.zeros((N, N), bool); orgs = []
    bg = list(range(N_ORG * (K_INT + K_BL), N))
    for o in range(N_ORG):
        base = o * (K_INT + K_BL)
        I = list(range(base, base + K_INT)); Bl = list(range(base + K_INT, base + K_INT + K_BL))
        for a in I:
            for b in I:
                if a < b:
                    adj[a, b] = True
        for b in Bl:
            for a in rng.choice(I, 2, replace=False):
                adj[min(a, b), max(a, b)] = True
            for e in rng.choice(bg, 2, replace=False):
                adj[min(b, e), max(b, e)] = True
        orgs.append((tuple(I), tuple(Bl)))
    for i in bg:
        for j in bg:
            if i < j and rng.random() < 0.25:
                adj[i, j] = True
    adj = adj | adj.T
    mag = lambda: rng.uniform(0.3, 0.6) * rng.choice([-1.0, 1.0])
    A = np.zeros((N, N)); G = np.zeros((N, N))
    for i, j in zip(*np.where(np.triu(adj))):
        A[i, j] = A[j, i] = mag()
        if family == "driven":
            g = mag(); G[i, j] = g; G[j, i] = -g
    A[np.diag_indices(N)] = np.abs(A).sum(1) + rng.uniform(0.5, 1.5, N)
    B = A + G; D = np.eye(N)
    return dict(B=B, D=D, S=stationary_cov(B, D), adj=adj, orgs=orgs, family=family)


def sample(B, S, n, delta, rng, burn=200):
    Phi = expm(-B * delta); Cn = S - Phi @ S @ Phi.T; L = np.linalg.cholesky((Cn + Cn.T) / 2 + 1e-12 * np.eye(len(S)))
    x = np.linalg.cholesky(S) @ rng.normal(size=len(S)); out = np.empty((n, len(S)))
    noise = rng.normal(size=(n + burn, len(S))) @ L.T
    for t in range(n + burn):
        x = Phi @ x + noise[t]
        if t >= burn:
            out[t - burn] = x
    return out


def estimates(X, delta_steps=1):
    X = X - X.mean(0); S = X.T @ X / len(X)
    C = X[delta_steps:].T @ X[:-delta_steps] / (len(X) - delta_steps)      # E[x_{t+delta} x_t^T]
    return S, C


def static_graph(S, thr):
    P = np.linalg.inv(S); d = np.sqrt(np.diag(P)); r = -P / np.outer(d, d)
    g = np.abs(r) > thr; np.fill_diagonal(g, False); return g, r


def dynamic_graph(S, C, delta, thr):
    Bh = np.real(-logm(C @ np.linalg.inv(S)) / delta)
    m = np.maximum(np.abs(Bh), np.abs(Bh).T); g = m > thr; np.fill_diagonal(g, False); return g, Bh


def blanket_of(g, I):
    I = list(I); return tuple(sorted(set(np.where(g[I].any(0))[0]) - set(I)))


def edge_scores(g, adj):
    iu = np.triu_indices(len(adj), 1); a, b = g[iu], adj[iu]
    tp = (a & b).sum(); prec = tp / max(a.sum(), 1); rec = tp / max(b.sum(), 1)
    return float(prec), float(rec), float(0 if tp == 0 else 2 * prec * rec / (prec + rec))
