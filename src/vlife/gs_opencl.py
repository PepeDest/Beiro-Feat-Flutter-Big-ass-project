"""S6b - the grayscott2 equations on the GPU (OpenCL, float64). The CPU does only the spot tracking.
Noise: a counter-based hash (seed, step, cell) gives two uniforms, then Box-Muller. A test checks the kernel against
the numba kernel with the noise off.
Fix #8 (docs/code_review.md): the hash is now splitmix64 on the 64-bit key (step << 32 | cell), see gpu_noise.py, with a
numpy reference that a test compares with the kernel. The old 32-bit key repeated exactly at lags of 10946, 21892, ...
steps. S6b and S6c (results/e11_*, e12_*) were run with the old hash."""
import numpy as np
import pyopencl as cl
from .grayscott import label_periodic, DU, DV, DC, DELTA, V_THR, NOISE
from .grayscott2 import GAMMA, Tracker2, seed_field
from .gpu_noise import OPENCL_SRC as NOISE_SRC

SRC = r"""
#pragma OPENCL EXTENSION cl_khr_fp64 : enable
//NOISE
__kernel void gs_step(__global const double* u, __global const double* v, __global const double* a, __global const double* b,
                   __global double* u2, __global double* v2, __global double* a2, __global double* b2,
                   const double F, const double k, const double eps, const double noise, const uint seed, const uint t, const int n){
  int i = get_global_id(0), j = get_global_id(1); int c = i * n + j;
  int ip = (i + 1 < n) ? i + 1 : 0, im = (i > 0) ? i - 1 : n - 1, jp = (j + 1 < n) ? j + 1 : 0, jm = (j > 0) ? j - 1 : n - 1;
  double uu = u[c], vv = v[c], aa = a[c], bb = b[c];
  double lu = u[ip*n+j] + u[im*n+j] + u[i*n+jp] + u[i*n+jm] - 4.0*uu;
  double lv = v[ip*n+j] + v[im*n+j] + v[i*n+jp] + v[i*n+jm] - 4.0*vv;
  double la = a[ip*n+j] + a[im*n+j] + a[i*n+jp] + a[i*n+jm] - 4.0*aa;
  double lb = b[ip*n+j] + b[im*n+j] + b[i*n+jp] + b[i*n+jm] - 4.0*bb;
  double uvv = uu*vv*vv;
  u2[c] = uu + DU*lu - uvv + F*(1.0 - uu);
  double vn = vv + DV*lv + uvv - (F + k - eps*aa)*vv;
  if (noise > 0.0){
    vn += noise * gauss(seed, t, c);
  }
  v2[c] = vn > 0.0 ? vn : 0.0;
  if (vv > V_THR){ a2[c] = aa + DC*la + GAMMA*aa*(1.0 - aa - 2.0*bb); b2[c] = bb + DC*lb + GAMMA*bb*(1.0 - bb - 2.0*aa); }
  else { a2[c] = aa + DC*la - DELTA*aa; b2[c] = bb + DC*lb - DELTA*bb; }
}
"""


def _ctx():
    for p in cl.get_platforms():
        if "AMD" in p.name:
            return cl.Context(p.get_devices())
    return cl.create_some_context(interactive=False)


class GPUGrid:
    def __init__(self, u, v, a, b):
        self.n = u.shape[0]; self.ctx = _ctx(); self.q = cl.CommandQueue(self.ctx)
        consts = dict(DU=DU, DV=DV, DC=DC, DELTA=DELTA, V_THR=V_THR, GAMMA=GAMMA)
        src = "".join(f"#define {k} {repr(float(v))}\n" for k, v in consts.items()) + SRC.replace("//NOISE", NOISE_SRC)
        self.prg = cl.Program(self.ctx, src).build()
        mf = cl.mem_flags
        self.buf = [[cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=np.ascontiguousarray(x, np.float64)) for x in (u, v, a, b)],
                    [cl.Buffer(self.ctx, mf.READ_WRITE, size=u.size * 8) for _ in range(4)]]
        self.cur = 0; self.t = 0; self.kern = cl.Kernel(self.prg, "gs_step")

    def advance(self, F, k, eps, nsteps, noise, seed):
        for _ in range(nsteps):
            src, dst = self.buf[self.cur], self.buf[1 - self.cur]
            self.kern.set_args(*src, *dst, np.float64(F), np.float64(k), np.float64(eps), np.float64(noise),
                               np.uint32(seed), np.uint32(self.t), np.int32(self.n))
            cl.enqueue_nd_range_kernel(self.q, self.kern, (self.n, self.n), None)
            self.cur = 1 - self.cur; self.t += 1

    def set_fields(self, which, arrays):
        for w, x in zip(which, arrays):
            cl.enqueue_copy(self.q, self.buf[self.cur][w], np.ascontiguousarray(x, np.float64))
        self.q.finish()

    def fields(self, which=(0, 1, 2, 3)):
        out = [np.empty((self.n, self.n)) for _ in which]
        for o, w in zip(out, which):
            cl.enqueue_copy(self.q, o, self.buf[self.cur][w])
        self.q.finish(); return out


def run(seed, eps, types=("A", "B", "B", "A"), n=300, F=0.0367, k=0.0649, max_steps=150000, every=10, stall=2000, mu=0.0):
    """mu: one-way mutation. Each daughter of a type-A parent becomes type B with probability mu (dyes swapped in its
    region at the frame where the division is found). S6c, docs/S6.md."""
    q = n // 4; centers = [(q, q), (q, 3 * q), (3 * q, q), (3 * q, 3 * q)]
    g = GPUGrid(*seed_field(n, centers, types)); mrng = np.random.default_rng([seed, 77])
    tr = Tracker2(); counts = []; best, best_t = 0, 0; t = 0; muts = [0, 0]      # [mutated, daughters of A parents]
    while t < max_steps:
        g.advance(F, k, eps, every, NOISE, seed); t += every
        v, a, b = g.fields(which=(1, 2, 3))          # u is not needed for tracking
        lab, m = label_periodic(v > V_THR)
        new_ids, daughters = tr.assign(lab, m, t)
        if mu > 0 and daughters:
            changed = False
            for L, pid in daughters:
                if tr.info[pid]["last"]["z"] == 1:
                    muts[1] += 1
                    if mrng.random() < mu:
                        r = lab == L; a[r], b[r] = b[r].copy(), a[r].copy(); muts[0] += 1; changed = True
            if changed:
                g.set_fields((2, 3), (a, b))
        tr.record(lab, m, a, b, new_ids)
        nA = sum(1 for i in tr.ids.values() if tr.info[i]["last"]["z"] == 1)
        counts.append((t, m, nA))
        if m > best:
            best, best_t = m, t
        elif t - best_t >= stall:
            break
    return dict(counts=counts, info=tr.info, merges=tr.merges, eps=eps, seed=seed, types=types, n=n, backend="opencl",
                mu=mu, mutations=muts)
