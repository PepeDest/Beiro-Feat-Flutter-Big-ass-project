"""S6 - Gray-Scott self-replicating spots [Pearson93] with a neutral dye, and a division tracker (docs/S6.md).

u_t = Du lap u - u v^2 + F (1 - u),  v_t = Dv lap v + u v^2 - (F + k) v       (periodic grid, explicit Euler, dt = 1)
c_t = Dc lap c - delta (1 - s) c,   s = 1 where v > V_THR                        (dye: does not act back on u, v)"""
import numpy as np
from scipy import ndimage

DU, DV, DC, DELTA, V_THR, NOISE = 0.16, 0.08, 0.01, 0.05, 0.1, 5e-4


def lap(a):
    return np.roll(a, 1, 0) + np.roll(a, -1, 0) + np.roll(a, 1, 1) + np.roll(a, -1, 1) - 4 * a


def seed_field(n, centers, levels, r=4):
    u = np.ones((n, n)); v = np.zeros((n, n)); c = np.zeros((n, n))
    for (i, j), lv in zip(centers, levels):
        sl = (slice(i - r, i + r), slice(j - r, j + r)); u[sl] = 0.5; v[sl] = 0.25; c[sl] = lv
    return u, v, c


def step(u, v, c, F, k, rng):
    uvv = u * v * v
    u2 = u + DU * lap(u) - uvv + F * (1 - u)
    v2 = v + DV * lap(v) + uvv - (F + k) * v + NOISE * rng.normal(size=v.shape)
    s = v > V_THR
    c2 = c + DC * lap(c) - DELTA * (~s) * c
    return u2, np.clip(v2, 0, None), c2


def label_periodic(mask):
    """Connected regions of mask on a torus: label, then join labels that touch across the edges."""
    lab, n = ndimage.label(mask)
    parent = list(range(n + 1))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for a, b in ((lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])):
        for x, y in zip(a, b):
            if x and y:
                rx, ry = find(x), find(y)
                if rx != ry:
                    parent[max(rx, ry)] = min(rx, ry)
    roots = np.array([find(i) for i in range(n + 1)])
    uniq = {r: i for i, r in enumerate(sorted(set(roots[1:])), start=1)}
    remap = np.array([0] + [uniq[r] for r in roots[1:]])
    return remap[lab], len(uniq)


class Tracker:
    """Follows spots between frames by overlap. Records divisions (one old spot -> two or more new spots)."""

    def __init__(self):
        self.prev = None; self.ids = {}; self.next_id = 0; self.info = {}; self.divisions = []; self.merges = 0

    def _new(self, parent, t):
        i = self.next_id; self.next_id += 1; self.info[i] = dict(parent=parent, born=t, last=None, div=None); return i

    def update(self, lab, n, c, t):
        area = ndimage.sum(np.ones_like(c), lab, range(1, n + 1)) if n else []
        dye = ndimage.mean(c, lab, range(1, n + 1)) if n else []
        new_ids = {}
        if self.prev is None:
            for L in range(1, n + 1):
                new_ids[L] = self._new(None, t)
        else:
            m = (self.prev > 0) & (lab > 0)
            pairs = set(zip(self.prev[m].tolist(), lab[m].tolist()))
            kids, olds = {}, {}
            for a, b in pairs:
                kids.setdefault(a, []).append(b); olds.setdefault(b, []).append(a)
            for L in range(1, n + 1):
                o = olds.get(L, [])
                if len(o) == 1 and len(kids[o[0]]) == 1:
                    new_ids[L] = self.ids[o[0]]                      # continues
                elif len(o) == 1:
                    pid = self.ids[o[0]]
                    if self.info[pid]["div"] is None:
                        self.info[pid]["div"] = dict(t=t, **self.info[pid]["last"])
                        self.divisions.append(pid)
                    new_ids[L] = self._new(pid, t)                   # daughter
                else:
                    self.merges += len(o) > 1; new_ids[L] = self._new(None, t)   # merge or new: no parent
        for L, i in new_ids.items():
            self.info[i]["last"] = dict(area=float(area[L - 1]), z=float(np.log(max(dye[L - 1], 1e-300))))
        self.prev, self.ids = lab, new_ids
        return n


def run(seed, F=0.0367, k=0.0649, n=200, max_steps=100000, every=10, stall=2000):
    rng = np.random.default_rng(seed)
    centers = [(50, 50), (50, 150), (150, 50), (150, 150)]
    levels = np.exp(rng.uniform(np.log(0.5), np.log(2.0), 4))
    u, v, c = seed_field(n, centers, levels)
    tr = Tracker(); counts = []; best, best_t = 0, 0
    for t in range(1, max_steps + 1):
        u, v, c = step(u, v, c, F, k, rng)
        if t % every == 0:
            lab, m = label_periodic(v > V_THR); tr.update(lab, m, c, t); counts.append((t, m))
            if m > best:
                best, best_t = m, t
            elif t - best_t >= stall:
                break
    return dict(counts=counts, info=tr.info, divisions=tr.divisions, merges=tr.merges, F=F, k=k, seed=seed)
