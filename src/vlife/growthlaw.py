"""Growth-law fits for spot colonies (S6, docs/S6.md): exponential (log N against t) against power law (log N against log t).

Fix #11 (docs/code_review.md): the exponent of a power law N ~ (t - t0)^p depends on the time origin t0. The pre-registered
rules R1 and H6 fit log N against log t with t0 = 0 (start of the simulation); those fields keep their old meaning.
growth_fits also fits t0 (grid search for the best R2 in log N against log(t - t0), t0 in [0, first time of the window))
and reports the exponent with that t0, as a description. It also returns None when the colony never reaches n_min spots
(E11 did not check this)."""
import numpy as np


def _r2(x, y):
    fit = np.polyval(np.polyfit(x, y, 1), x)
    return 1 - np.sum((y - fit) ** 2) / np.sum((y - y.mean()) ** 2)


def growth_fits(t, N, n_min=8, frac=0.3, n_grid=400):
    """Fit window: from the first time with N >= n_min to the first time with N >= frac * max(N).
    Returns a dict, or None if the window is too short (fewer than 5 points) or N never reaches n_min."""
    t, N = np.asarray(t, float), np.asarray(N, float)
    Nmax = N.max()
    if Nmax < n_min:
        return None
    i0 = int(np.argmax(N >= n_min)); i1 = int(np.argmax(N >= frac * Nmax))
    if i1 <= i0 + 3:
        return None
    tt, nn = t[i0:i1 + 1], np.log(N[i0:i1 + 1])
    out = dict(R2_exp=float(_r2(tt, nn)), R2_pow=float(_r2(np.log(tt), nn)), power=float(np.polyfit(np.log(tt), nn, 1)[0]),
               rate=float(np.polyfit(tt, nn, 1)[0]), N_max=int(Nmax), N_window=[int(N[i0]), int(N[i1])], t_end=float(t[-1]))
    grid = np.linspace(0.0, tt[0], n_grid, endpoint=False)
    r2 = np.array([_r2(np.log(tt - t0), nn) for t0 in grid])
    t0 = float(grid[np.argmax(r2)])
    out.update(t0_fit=t0, R2_pow_t0=float(r2.max()), power_t0=float(np.polyfit(np.log(tt - t0), nn, 1)[0]))
    return out
