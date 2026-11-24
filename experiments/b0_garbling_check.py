"""Niche B, B0 (docs/B.md): sampling check of the Gaussian pre-garbling algebra in whitened coordinates.
Z = K Y + N, intervened X drawn from the actual p(x | z). Expected: Cov(X_hat, Y) = C P and
I(X_hat; Y) = -1/2 log det(I - C P^2 C^T), with P = K^T (K K^T + Sigma_N)^-1 K."""
import numpy as np

rng = np.random.default_rng(5); dx, dy, n = 2, 3, 400000
A = rng.normal(size=(dx, dy)); C = A / (1.3 * np.linalg.norm(A, 2))
K = rng.normal(size=(2, dy)); N = np.diag([0.5, 2.0])
P = K.T @ np.linalg.solve(K @ K.T + N, K)
Y = rng.normal(size=(n, dy)); Z = Y @ K.T + rng.normal(size=(n, 2)) @ np.sqrt(N)
Szz = K @ K.T + N; Sxz = C @ K.T
G = Sxz @ np.linalg.inv(Szz); Sxgz = np.eye(dx) - G @ Sxz.T
Xh = Z @ G.T + rng.normal(size=(n, dx)) @ np.linalg.cholesky(Sxgz).T
print("max |Cov(Xh,Y) - C P|", np.abs(Xh.T @ Y / n - C @ P).max())
print("I formula with P^2:", -0.5 * np.linalg.slogdet(np.eye(dx) - C @ P @ P @ C.T)[1],
      " I(X;Z):", -0.5 * np.linalg.slogdet(np.eye(dx) - C @ P @ C.T)[1])
Sj = np.cov(np.hstack([Xh, Y]).T)
print("sampled I(Xh;Y):", 0.5 * (np.linalg.slogdet(Sj[:dx, :dx])[1] + np.linalg.slogdet(Sj[dx:, dx:])[1] - np.linalg.slogdet(Sj)[1]))
