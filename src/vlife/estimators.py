"""Sample-based information estimators, used (a) to validate closed forms and (b) to show why the legacy
binned estimator was unreliable.  Everything is in NATS."""
import numpy as np
from scipy.spatial import cKDTree
from scipy.special import digamma


def ksg_mi(x, y, k=4):
    """Kraskov-Stoegbauer-Grassberger estimator, algorithm 1 (eq. 8). [Kraskov04]
    x, y: arrays (n,) or (n,d)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    x = x.reshape(len(x), -1); y = y.reshape(len(y), -1)
    n = len(x)
    z = np.hstack([x, y])
    eps = cKDTree(z).query(z, k=k + 1, p=np.inf)[0][:, -1]
    tx, ty = cKDTree(x), cKDTree(y)
    nx = tx.query_ball_point(x, eps - 1e-12, p=np.inf, return_length=True) - 1
    ny = ty.query_ball_point(y, eps - 1e-12, p=np.inf, return_length=True) - 1
    return float(digamma(k) + digamma(n) - np.mean(digamma(nx + 1) + digamma(ny + 1)))


def binned_mi(x, y, bins=12):
    """Plug-in (histogram) MI in nats: the estimator family used by the legacy script.
    Known to be biased upward by ~ (Bx-1)(By-1)/(2n) nats for independent variables [Treves95, Paninski03]."""
    h, _, _ = np.histogram2d(x, y, bins=bins)
    p = h / h.sum()
    px, py = p.sum(1, keepdims=True), p.sum(0, keepdims=True)
    nz = p > 0
    return float((p[nz] * np.log(p[nz] / (px @ py)[nz])).sum())


def effective_sample_size_ar1(n, rho):
    """N_eff = n (1-rho)/(1+rho) for the mean of an AR(1) series. [BayleyHammersley46]"""
    return n * (1 - rho) / (1 + rho)
