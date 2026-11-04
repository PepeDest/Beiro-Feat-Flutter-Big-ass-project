# NOTE: only change vs. the uploaded file: literal line breaks inside print() strings were
# escaped (\n) so the file parses. Logic is untouched. Kept for the audit (experiment E0).
#!/usr/bin/env python3
"""
Emergent Boundary Discovery
--------------------------
No organism, crystal, or replication rule is hard-coded.

We start from:
    Ω = {x_1,...,x_N}
    microscopic dynamics
    external driving on a subset of variables

For every candidate partition A ⊂ Ω we compute

    C(A) = I(A_t ; A_{t+1})
    P(A) = I(A_t ; E_{t+1})
    K(A) = H(A_t)

    Φ(A) = P(A) + β C(A) - λ K(A)

and discover

    A* = argmax_A Φ(A)

This is the first non-circular implementation of the framework.
"""

import numpy as np
from itertools import combinations
from sklearn.metrics import mutual_info_score
import matplotlib.pyplot as plt

np.random.seed(1)

# -----------------------------
# Information-theoretic tools
# -----------------------------

def discretize(x, bins=12):
    edges = np.histogram_bin_edges(x, bins=bins)
    return np.digitize(x, edges[:-1])


def MI(x, y, bins=12):
    return mutual_info_score(discretize(x,bins), discretize(y,bins))


def H(x, bins=12):
    d = discretize(x,bins)
    _, counts = np.unique(d, return_counts=True)
    p = counts / counts.sum()
    return -(p * np.log2(p + 1e-12)).sum()

# -----------------------------
# Microscopic world Ω
# -----------------------------

T = 3000
N = 8

# external process (not an organism)
E = np.zeros(T)
for t in range(T-1):
    E[t+1] = 0.95*E[t] + np.random.normal(scale=1.0)

# identical microscopic variables
X = np.zeros((T,N))

# interaction matrix
W = np.array([
[0.8,0.2,0.0,0,0,0,0,0],
[0.2,0.8,0.2,0,0,0,0,0],
[0.0,0.2,0.8,0,0,0,0,0],
[0,0,0,0.5,0.2,0,0,0],
[0,0,0,0.2,0.5,0,0,0],
[0,0,0,0,0,0.4,0.1,0],
[0,0,0,0,0,0.1,0.4,0],
[0,0,0,0,0,0,0,0.3]
])

for t in range(T-1):
    coupling = W @ X[t]

    # external drive only enters microscopic variables 0,1,2
    drive = np.zeros(N)
    drive[:3] = 0.35 * E[t]

    X[t+1] = np.tanh(coupling + drive) + 0.08*np.random.randn(N)

# -----------------------------
# Organizational functional
# -----------------------------

beta = 1.0
lam = 0.25

results = []

for r in range(1, N):
    for subset in combinations(range(N), r):

        A = X[:, subset].mean(axis=1)

        C = MI(A[:-1], A[1:])
        P = MI(A[:-1], E[1:])
        K = H(A)

        Phi = P + beta*C - lam*K

        results.append((subset, Phi, P, C, K))

results.sort(key=lambda z: z[1], reverse=True)

best = results[0]

print("\nBest partition A*:", best[0])
print("Phi =", round(best[1],4))
print("P   =", round(best[2],4))
print("C   =", round(best[3],4))
print("K   =", round(best[4],4))

# -----------------------------
# Visualization
# -----------------------------

fig, ax = plt.subplots(2,1,figsize=(10,6))

ax[0].plot(E[:400], label='Environment', lw=2)
for i in range(N):
    ax[0].plot(X[:400,i], alpha=0.6)
ax[0].set_title('Microscopic dynamics')
ax[0].legend()

phis = [r[1] for r in results[:25]]
ax[1].bar(range(len(phis)), phis)
ax[1].set_title('Top 25 partitions ranked by Φ')
ax[1].set_xlabel('Partition rank')
ax[1].set_ylabel('Φ')

plt.tight_layout()
plt.savefig('emergent_boundary_discovery.png', dpi=200)

print('\nSaved: emergent_boundary_discovery.png')
