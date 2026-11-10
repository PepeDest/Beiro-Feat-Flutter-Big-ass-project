"""Reference (numpy) version of the counter-based noise of the OpenCL kernel in gs_opencl.py (fix #8, docs/code_review.md).

Key = (t << 32) | cell, a 64-bit integer, mixed with splitmix64 after an XOR with splitmix64(seed). splitmix64 is a
bijection of 64-bit integers, so two different (t, cell) pairs never give the same 64-bit value. The old kernel used a
32-bit key t*2654435761 + 2*cell, which repeats exactly at lags of 10946, 21892, ... steps (Fibonacci numbers).
The high 32 bits give r1, the low 32 bits give r2, both in (0, 1); then Box-Muller: sqrt(-2 log r1) cos(2 pi r2)."""
import numpy as np

_M64 = (1 << 64) - 1


def splitmix64(x):
    x = np.asarray(x, dtype=np.uint64)
    with np.errstate(over="ignore"):
        x = x + np.uint64(0x9E3779B97F4A7C15)
        x = (x ^ (x >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
        x = (x ^ (x >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    return x ^ (x >> np.uint64(31))


def bits(seed, t, cell):
    key = (np.asarray(t, dtype=np.uint64) << np.uint64(32)) | np.asarray(cell, dtype=np.uint64)
    return splitmix64(key ^ splitmix64(np.uint64(seed)))


def normal(seed, t, cell):
    z = bits(seed, t, cell)
    r1 = ((z >> np.uint64(32)).astype(np.float64) + 1.0) / 4294967297.0
    r2 = ((z & np.uint64(0xFFFFFFFF)).astype(np.float64) + 1.0) / 4294967297.0
    return np.sqrt(-2.0 * np.log(r1)) * np.cos(6.283185307179586 * r2)


OPENCL_SRC = r"""
ulong sm64(ulong x){ x += 0x9E3779B97F4A7C15UL; x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9UL;
  x = (x ^ (x >> 27)) * 0x94D049BB133111EBUL; return x ^ (x >> 31); }
double gauss(uint seed, uint t, int c){
  ulong z = sm64((((ulong)t) << 32 | (ulong)(uint)c) ^ sm64((ulong)seed));
  double r1 = ((double)(uint)(z >> 32) + 1.0) / 4294967297.0, r2 = ((double)(uint)(z & 0xFFFFFFFFUL) + 1.0) / 4294967297.0;
  return sqrt(-2.0*log(r1)) * cos(6.283185307179586*r2);
}
"""
