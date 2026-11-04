"""S6b - Gray-Scott spots with two competing heritable dyes a, b (types A, B); type A changes the local kill rate.
Compiled with numba (float64). Same u, v equations as grayscott.py (docs/S6.md, S6b).

a_t = Dc lap a + GAMMA s a (1 - a - 2 b) - DELTA (1 - s) a      (b: same with a and b swapped)
v_t = Dv lap v + u v^2 - (F + k - EPS a) v + noise,   s = 1[v > V_THR]"""
import numpy as np
from numba import njit
from scipy import ndimage
from .grayscott import label_periodic, DU, DV, DC, DELTA, V_THR, NOISE

GAMMA = 0.05


@njit(cache=True)
def _seed_rng(seed):
    np.random.seed(seed)


@njit(cache=True)
def advance(u, v, a, b, F, k, eps, nsteps, noise):
    """nsteps explicit Euler steps on a periodic grid, in place (double buffers inside)."""
    n = u.shape[0]
    u2 = np.empty_like(u); v2 = np.empty_like(v); a2 = np.empty_like(a); b2 = np.empty_like(b)
    for _ in range(nsteps):
        for i in range(n):
            ip = i + 1 if i + 1 < n else 0
            im = i - 1 if i > 0 else n - 1
            for j in range(n):
                jp = j + 1 if j + 1 < n else 0
                jm = j - 1 if j > 0 else n - 1
                uu = u[i, j]; vv = v[i, j]; aa = a[i, j]; bb = b[i, j]
                lu = u[ip, j] + u[im, j] + u[i, jp] + u[i, jm] - 4.0 * uu
                lv = v[ip, j] + v[im, j] + v[i, jp] + v[i, jm] - 4.0 * vv
                la = a[ip, j] + a[im, j] + a[i, jp] + a[i, jm] - 4.0 * aa
                lb = b[ip, j] + b[im, j] + b[i, jp] + b[i, jm] - 4.0 * bb
                uvv = uu * vv * vv
                u2[i, j] = uu + DU * lu - uvv + F * (1.0 - uu)
                vn = vv + DV * lv + uvv - (F + k - eps * aa) * vv
                if noise > 0.0:
                    vn += noise * np.random.standard_normal()
                v2[i, j] = vn if vn > 0.0 else 0.0
                if vv > V_THR:
                    a2[i, j] = aa + DC * la + GAMMA * aa * (1.0 - aa - 2.0 * bb)
                    b2[i, j] = bb + DC * lb + GAMMA * bb * (1.0 - bb - 2.0 * aa)
                else:
                    a2[i, j] = aa + DC * la - DELTA * aa
                    b2[i, j] = bb + DC * lb - DELTA * bb
        u[:, :] = u2; v[:, :] = v2; a[:, :] = a2; b[:, :] = b2


def seed_field(n, centers, types, r=4):
    u = np.ones((n, n)); v = np.zeros((n, n)); a = np.zeros((n, n)); b = np.zeros((n, n))
    for (i, j), t in zip(centers, types):
        sl = (slice(i - r, i + r), slice(j - r, j + r)); u[sl] = 0.5; v[sl] = 0.25
        (a if t == "A" else b)[sl] = 0.9
    return u, v, a, b


class Tracker2:
    """Overlap tracking as in grayscott.Tracker; each record also holds the type (1 = A, 0 = B)."""

    def __init__(self):
        self.prev = None; self.ids = {}; self.next_id = 0; self.info = {}; self.merges = 0

    def _new(self, parent, t):
        i = self.next_id; self.next_id += 1; self.info[i] = dict(parent=parent, born=t, last=None, div=None); return i

    def assign(self, lab, n, t):
        """Match labels to spot ids. Returns (new_ids, daughters) with daughters = [(label, parent id)]."""
        idx = range(1, n + 1); new_ids = {}; daughters = []
        if self.prev is None:
            for L in idx:
                new_ids[L] = self._new(None, t)
        else:
            m = (self.prev > 0) & (lab > 0)
            pairs = set(zip(self.prev[m].tolist(), lab[m].tolist())); kids, olds = {}, {}
            for x, y in pairs:
                kids.setdefault(x, []).append(y); olds.setdefault(y, []).append(x)
            for L in idx:
                o = olds.get(L, [])
                if len(o) == 1 and len(kids[o[0]]) == 1:
                    new_ids[L] = self.ids[o[0]]
                elif len(o) == 1:
                    pid = self.ids[o[0]]
                    if self.info[pid]["div"] is None:
                        self.info[pid]["div"] = dict(t=t, **self.info[pid]["last"])
                    new_ids[L] = self._new(pid, t); daughters.append((L, pid))
                else:
                    self.merges += len(o) > 1; new_ids[L] = self._new(None, t)
        return new_ids, daughters

    def record(self, lab, n, a, b, new_ids):
        idx = range(1, n + 1)
        area = ndimage.sum(np.ones_like(a), lab, idx) if n else []
        ma = ndimage.mean(a, lab, idx) if n else []; mb = ndimage.mean(b, lab, idx) if n else []
        for L, i in new_ids.items():
            self.info[i]["last"] = dict(area=float(area[L - 1]), z=int(ma[L - 1] > mb[L - 1]))
        self.prev, self.ids = lab, new_ids

    def update(self, lab, n, a, b, t):
        new_ids, _ = self.assign(lab, n, t); self.record(lab, n, a, b, new_ids)


def run(seed, eps, types=("A", "B", "B", "A"), n=300, F=0.0367, k=0.0649, max_steps=150000, every=10, stall=2000):
    _seed_rng(seed)
    q = n // 4; centers = [(q, q), (q, 3 * q), (3 * q, q), (3 * q, 3 * q)]
    u, v, a, b = seed_field(n, centers, types)
    tr = Tracker2(); counts = []; best, best_t = 0, 0; t = 0
    while t < max_steps:
        advance(u, v, a, b, F, k, eps, every, NOISE); t += every
        lab, m = label_periodic(v > V_THR); tr.update(lab, m, a, b, t)
        nA = sum(1 for i in tr.ids.values() if tr.info[i]["last"]["z"] == 1)
        counts.append((t, m, nA))
        if m > best:
            best, best_t = m, t
        elif t - best_t >= stall:
            break
    return dict(counts=counts, info=tr.info, merges=tr.merges, eps=eps, seed=seed, types=types, n=n)
