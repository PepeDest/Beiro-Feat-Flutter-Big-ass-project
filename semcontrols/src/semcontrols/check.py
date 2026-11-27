"""The test function: run a score on the controls and compare it with the known answers."""
import numpy as np
from . import controls


def auc(a, b):
    """P(a > b) + P(a = b) / 2."""
    a, b = np.asarray(a), np.asarray(b)
    return float(((a[:, None] > b[None, :]).mean() + 0.5 * (a[:, None] == b[None, :]).mean()))


def strat_auc(s, y, kind):
    """AUC(rock > oscillator) inside tertiles of y. A tertile counts if it has at least 5 units of each class. The
    value is the mean over the tertiles, and NaN if fewer than 2 count. Returns (value, number of tertiles)."""
    cuts = np.quantile(y, [1 / 3, 2 / 3]); b = np.digitize(y, cuts)
    vals = [auc(s[(b == j) & (kind == "rock")], s[(b == j) & (kind == "oscillator")]) for j in range(3)
            if ((b == j) & (kind == "rock")).sum() >= 5 and ((b == j) & (kind == "oscillator")).sum() >= 5]
    return (float(np.mean(vals)) if len(vals) >= 2 else np.nan), len(vals)


def boot(n, fn, n_boot=1000, seed=0):
    """[value, 2.5 %, 97.5 %] of fn over bootstrap resamples of n items."""
    rng = np.random.default_rng(seed)
    pt = float(fn(np.arange(n)))
    bs = np.array([fn(rng.integers(0, n, n)) for _ in range(n_boot)])
    lo, hi = np.nanpercentile(bs, [2.5, 97.5])
    return [pt, float(lo), float(hi)]


def boot_mean(vals, n_boot=10_000, seed=0):
    vals = np.asarray(vals, float); rng = np.random.default_rng(seed)
    bs = [np.nanmean(vals[rng.integers(0, len(vals), len(vals))]) for _ in range(n_boot)]
    lo, hi = np.nanpercentile(bs, [2.5, 97.5])
    return [float(np.nanmean(vals)), float(lo), float(hi)]


def _zero_test(values, tol):
    a = np.abs(np.asarray(values, float))
    return dict(n=int(a.size), max_abs=float(a.max()), frac_zero=float(np.mean(a <= tol)),
                verdict="pass" if bool(np.all(a <= tol)) else "fail")


def check(linear_score=None, unit_score=None, unit_values=None, homeostat_ids=range(400), n_readers=200, tol=1e-9,
          n_boot=1000, n_boot_draws=10_000):
    """Run a score on the controls.

    linear_score(system) -> float, for the linear controls (`homeostat`, `reader`).
    unit_score(unit) -> float, or unit_values: {(seed, i): value} for the 840 units of `controls.units()`.
    Returns a dict with one entry for each test: `homeostat_zero`, `homeostat_order`, `reader_zero`, `rocks_order`.
    Each entry holds the values and a "pass" or "fail" verdict."""
    out = {}
    if linear_score is not None:
        pairs = controls.homeostat_pairs(list(homeostat_ids))
        si = np.array([linear_score(a) for a, _ in pairs], float)
        sn = np.array([linear_score(b) for _, b in pairs], float)
        out["homeostat_zero"] = dict(known="0 without feedback", **_zero_test(sn, tol))
        o = boot(len(pairs), lambda ids: float(np.mean(si[ids] > sn[ids])), n_boot)
        out["homeostat_order"] = dict(known="intact above no feedback", n=len(pairs), frac=o[0], ci=o[1:],
                                      verdict="pass" if o[1] > 0.5 else "fail")
        rv = [linear_score(s) for s in controls.readers(n_readers)]
        out["reader_zero"] = dict(known="0 when the environment only reads the agent", **_zero_test(rv, tol))
    if unit_score is not None or unit_values is not None:
        us = controls.units()
        if unit_values is None:
            unit_values = {(u.seed, u.i): unit_score(u) for u in us}
        per = {}
        for seed in sorted({u.seed for u in us}):
            d = [u for u in us if u.seed == seed]
            s = np.array([unit_values[(u.seed, u.i)] for u in d], float)
            kind = np.array([u.kind for u in d]); y = np.log([u.V_on for u in d])
            per[seed] = strat_auc(s, y, kind)
        a = boot_mean([v[0] for v in per.values()], n_boot_draws)
        out["rocks_order"] = dict(known="rocks not above oscillators of the same life", auc=a[0], ci=a[1:],
                                  per_draw={k: v[0] for k, v in per.items()},
                                  verdict="fail" if a[1] > 0.5 else "pass")
    return out


def report(result):
    """A short text table of a check() result."""
    L = ["test | known answer | value | verdict", "---|---|---|---"]
    for k, r in result.items():
        if "frac" in r:
            val = f"fraction {r['frac']:.3f} [{r['ci'][0]:.3f}, {r['ci'][1]:.3f}]"
        elif "auc" in r:
            val = f"AUC {r['auc']:.3f} [{r['ci'][0]:.3f}, {r['ci'][1]:.3f}]"
        else:
            val = f"max |score| {r['max_abs']:.3g}, zero in {r['frac_zero']:.3f}"
        L.append(f"{k} | {r['known']} | {val} | {r['verdict']}")
    return "\n".join(L)
