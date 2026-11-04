"""E0 - audit of the ORIGINAL script (legacy/emergent_boundary_discovery_original.py).
Reproduces the findings quoted in docs/LIMITATIONS.md. Each finding is a measurement, not an opinion."""
import numpy as np
from itertools import combinations
from sklearn.metrics import mutual_info_score
from common import save_json
from vlife.estimators import effective_sample_size_ar1, binned_mi

def disc(x, bins=12):
    e = np.histogram_bin_edges(x, bins=bins); return np.digitize(x, e[:-1])
def MI(x, y, bins=12): return mutual_info_score(disc(x, bins), disc(y, bins))          # nats
def H(x, bins=12):
    _, c = np.unique(disc(x, bins), return_counts=True); p = c / c.sum(); return -(p * np.log2(p + 1e-12)).sum()  # BITS

W = np.array([[0.8,0.2,0,0,0,0,0,0],[0.2,0.8,0.2,0,0,0,0,0],[0,0.2,0.8,0,0,0,0,0],[0,0,0,0.5,0.2,0,0,0],
              [0,0,0,0.2,0.5,0,0,0],[0,0,0,0,0,0.4,0.1,0],[0,0,0,0,0,0.1,0.4,0],[0,0,0,0,0,0,0,0.3]])

def world(seed, T=3000, gain=0.35, burn=200):
    r = np.random.default_rng(seed); N = 8
    E = np.zeros(T + burn)
    for t in range(T + burn - 1): E[t+1] = 0.95 * E[t] + r.normal()
    X = np.zeros((T + burn, N))
    for t in range(T + burn - 1):
        d = np.zeros(N); d[:3] = gain * E[t]; X[t+1] = np.tanh(W @ X[t] + d) + 0.08 * r.normal(size=N)
    return X[burn:], E[burn:]

def rank(X, E, beta=1., lam=.25):
    out = []
    for k in range(1, 8):
        for s in combinations(range(8), k):
            A = X[:, s].mean(1); C = MI(A[:-1], A[1:]); P = MI(A[:-1], E[1:]); K = H(A)
            out.append((s, P + beta*C - lam*K, P, C, K))
    return sorted(out, key=lambda z: -z[1])

res = {}
res["block_spectral_radii"] = [float(np.linalg.eigvalsh(W[i:j, i:j]).max()) for i, j in [(0,3),(3,5),(5,7),(7,8)]]
X, E = world(1); r = rank(X, E)
res["top3"] = [dict(subset=x[0], phi=x[1], P=x[2], C=x[3], K_bits=x[4]) for x in r[:3]]
res["argmax_8_seeds_with_drive"] = [rank(*world(s))[0][0] for s in range(8)]
res["argmax_5_seeds_NO_drive"] = [rank(*world(s, gain=0))[0][0] for s in range(5)]
Es = np.roll(E, 1234); res["null_shifted_E_best_phi"] = rank(X, Es)[0][1]; res["real_best_phi"] = r[0][1]
rho = np.corrcoef(E[:-1], E[1:])[0, 1]
res["E_lag1_autocorr"] = float(rho); res["E_effective_N"] = float(effective_sample_size_ar1(len(E), rho))
A = X[:, :3].mean(1)
def resid(y, x): return y - np.polyval(np.polyfit(x, y, 1), x)
res["partial_corr_A_t_E_t+1_given_E_t"] = float(np.corrcoef(resid(A[:-1], E[:-1]), resid(E[1:], E[:-1]))[0, 1])
res["raw_corr_A_t_E_t+1"] = float(np.corrcoef(A[:-1], E[1:])[0, 1])
z = np.random.default_rng(5).normal(size=(2, 3000)); res["binned_MI_bias_on_independent_noise_nats"] = binned_mi(z[0], z[1], 12)
res["units_note"] = "mutual_info_score returns nats; H uses log2 (bits): beta*C - lambda*K mixes units"
save_json("e0_audit.json", res)
for k, v in res.items(): print(k, ":", v)
