"""Gaussian information bottleneck (GIB) and slow linear modes (TICA/VAMP-type), as INSTRUMENTS.

GIB problem:  min_{T|X}  L = I(T;X) - beta * I(T;Y)  for jointly Gaussian (X,Y). [Tishby99, Chechik05]
Chechik et al. show the optimum is linear, T = A X + xi, xi ~ N(0, I), with
   M = S_{x|y} S_x^{-1}  (eigenvalues 0 < lambda_1 <= ... <= lambda_n <= 1, left eigenvectors v_i),
   critical values  beta_i^c = 1/(1 - lambda_i),
   rows of A:  alpha_i v_i^T, alpha_i = sqrt( (beta(1-lambda_i) - 1) / (lambda_i r_i) ) for beta >= beta_i^c, else 0,
   r_i = v_i^T S_x v_i.
i.e. new effective degrees of freedom switch on at discrete critical trade-off values: a genuine
bifurcation sequence of a variational problem. [Chechik05 Thm 3.1]  This is the cleanest known
instance of 'complexity appears at thresholds' and is the validation target for the project's functional.

Slow modes: generalized eigenproblem  C_tica v = mu S v,  C_tica = E[x_t x_{t+tau}^T]  (TICA, [MolgedeyS94,
PerezHernandez13]); VAMP generalises this to non-reversible dynamics [WuNoe20]. For REVERSIBLE dynamics the
GIB directions (canonical-correlation directions, [Hotelling36]) and TICA directions span the same subspace
(proved in docs/THEORY.md sec 6 for the symmetric case; the numerical check is tests/test_gib.py).
For irreversible dynamics they differ; measuring that difference is experiment E2.
"""
import numpy as np
from scipy.linalg import eig, sqrtm, subspace_angles, eigh


def gib_modes(Sx, Sy, Sxy):
    """Return (lambdas ascending, V (rows = whitened-space-corrected left eigenvectors v_i), beta_crit)."""
    Sx_is = np.linalg.inv(np.real(sqrtm(Sx)))
    Sxgy = Sx - Sxy @ np.linalg.inv(Sy) @ Sxy.T
    Msym = Sx_is @ Sxgy @ Sx_is
    lam, U = eigh((Msym + Msym.T) / 2)
    V = (Sx_is @ U).T                       # row i = v_i, with r_i = v_i^T Sx v_i = 1
    return lam, V, 1.0 / (1.0 - lam)


def gib_projection(Sx, Sy, Sxy, beta):
    lam, V, bc = gib_modes(Sx, Sy, Sxy)
    rows = [np.sqrt((beta * (1 - l) - 1) / l) * v for l, v, b in zip(lam, V, bc) if beta >= b]
    return np.array(rows).reshape(len(rows), Sx.shape[0])


def gib_objective(A, Sx, Sy, Sxy, beta):
    """L = I(T;X) - beta I(T;Y) for T = A X + xi, xi ~ N(0,I)."""
    k = A.shape[0]
    if k == 0:
        return 0.0
    Sxgy = Sx - Sxy @ np.linalg.inv(Sy) @ Sxy.T
    ld = lambda M: np.linalg.slogdet(M)[1]
    ITX = 0.5 * ld(A @ Sx @ A.T + np.eye(k))
    ITY = 0.5 * (ld(A @ Sx @ A.T + np.eye(k)) - ld(A @ Sxgy @ A.T + np.eye(k)))
    return float(ITX - beta * ITY)


def tica_modes(C_tica, S):
    """Solve C_tica v = mu S v; return mu sorted by |mu| descending and the matching v (as rows)."""
    mu, V = eig(C_tica, S)
    order = np.argsort(-np.abs(mu))
    return mu[order], V[:, order].T


def tica_subspace(C_tica, S, k, tol=1e-9):
    """Real basis of the span of the k leading TICA modes (by |mu|), for non-symmetric C_tica.
    A complex mode v spans a real plane {Re v, Im v}; taking np.real(v) alone gives a direction that depends on the
    arbitrary phase LAPACK gives to v (docs/code_review.md, item 3). If the k-th mode is complex and its conjugate is
    the (k+1)-th, the pair is kept together, so the dimension m can be k + 1.
    Returns (mu of the m modes, basis rows (m x n, orthonormal), m). The span is invariant under S^-1 C_tica."""
    mu, V = eig(C_tica, S)
    order = np.argsort(-np.abs(mu), kind="stable"); mu, V = mu[order], V[:, order]
    m = k
    if m < len(mu) and abs(mu[m - 1].imag) > tol * abs(mu[m - 1]) and np.isclose(mu[m], np.conj(mu[m - 1])):
        m += 1
    R = np.hstack([V[:, :m].real, V[:, :m].imag])
    U, s, _ = np.linalg.svd(R, full_matrices=False)
    return mu[:m], U[:, :m].T, m


def subspace_gap(A_rows, B_rows):
    """Largest principal angle (radians) between the row-spaces of A_rows and B_rows. [GolubVanLoan13 ch.6.4]"""
    return float(np.max(subspace_angles(np.real(A_rows).T, np.real(B_rows).T)))
