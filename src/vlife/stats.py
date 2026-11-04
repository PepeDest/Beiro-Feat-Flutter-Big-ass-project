"""Small statistics helpers: grouped (within-world) analysis and cluster bootstrap."""
import numpy as np
from scipy.stats import spearmanr


def spearman_within(score, y, groups):
    """List of Spearman rho per group (groups with <5 points or constant vectors skipped). [Spearman1904]"""
    rhos = []
    for g in np.unique(groups):
        m = groups == g
        if m.sum() < 5 or np.ptp(score[m]) == 0 or np.ptp(y[m]) == 0:
            continue
        rhos.append(spearmanr(score[m], y[m])[0])
    return np.array(rhos)


def cluster_bootstrap(n_clusters, stat_fn, n_boot=400, rng=None, alpha=0.05):
    """Resample WORLDS (clusters) with replacement; returns (point estimate, lo, hi). [Efron79; cluster
    version e.g. CameronMiller15]"""
    rng = np.random.default_rng(0) if rng is None else rng
    point = np.asarray(stat_fn(np.arange(n_clusters)))
    boots = np.array([stat_fn(rng.integers(0, n_clusters, n_clusters)) for _ in range(n_boot)])
    lo, hi = np.nanpercentile(boots, [100 * alpha / 2, 100 * (1 - alpha / 2)], axis=0)
    return point, lo, hi
