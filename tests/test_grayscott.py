import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import numpy as np
from vlife.grayscott import label_periodic, Tracker, seed_field, step


def test_label_joins_across_edges():
    m = np.zeros((20, 20), bool); m[0:2, 5:8] = True; m[18:20, 5:8] = True; m[10, 10] = True
    lab, n = label_periodic(m)
    assert n == 2 and lab[0, 5] == lab[19, 5]


def test_tracker_finds_a_division():
    c = np.ones((30, 30)); tr = Tracker()
    a = np.zeros((30, 30), bool); a[10:20, 5:25] = True
    tr.update(*label_periodic(a), c, 0)
    b = np.zeros((30, 30), bool); b[10:20, 5:12] = True; b[10:20, 18:25] = True
    tr.update(*label_periodic(b), c, 10)
    assert len(tr.divisions) == 1 and sum(1 for i in tr.info.values() if i["parent"] == tr.divisions[0]) == 2


def test_dye_does_not_act_back():
    u, v, c = seed_field(60, [(30, 30)], [1.0]); u2, v2, c2 = u.copy(), v.copy(), c * 0
    for i in range(50):
        u, v, c = step(u, v, c, 0.0367, 0.0649, np.random.default_rng(i))
        u2, v2, c2 = step(u2, v2, c2, 0.0367, 0.0649, np.random.default_rng(i))
    assert np.array_equal(u, u2) and np.array_equal(v, v2)


def test_numba_kernel_matches_numpy_code():
    # S6b: with no noise and eps = 0, the numba kernel gives the same u, v as the S6 numpy step.
    import vlife.grayscott as gs
    from vlife.grayscott2 import advance
    u, v, c = seed_field(64, [(32, 32)], [1.0]); u2, v2 = u.copy(), v.copy(); a = np.zeros_like(u); b = np.zeros_like(u)
    old = gs.NOISE; gs.NOISE = 0.0
    try:
        for _ in range(300):
            u, v, c = step(u, v, c, 0.0367, 0.0649, np.random.default_rng(0))
    finally:
        gs.NOISE = old
    advance(u2, v2, a, b, 0.0367, 0.0649, 0.0, 300, 0.0)
    assert np.allclose(u, u2, atol=1e-10) and np.allclose(v, v2, atol=1e-10)


def test_types_settle_and_are_kept():
    # Strong cross-competition: a mixed spot settles on its majority dye.
    from vlife.grayscott2 import advance, seed_field as seed2
    u, v, a, b = seed2(64, [(32, 32)], ["A"]); b[28:36, 28:36] = 0.3
    advance(u, v, a, b, 0.0367, 0.0649, 0.0, 400, 0.0)
    s = v > 0.1
    assert a[s].mean() > 0.5 and b[s].mean() < 0.05


def test_gpu_kernel_matches_numba_kernel():
    # S6b: with the noise off, the OpenCL kernel gives the same fields as the numba kernel (float64).
    import pytest
    try:
        from vlife.gs_opencl import GPUGrid
    except Exception:
        pytest.skip("no OpenCL")
    from vlife.grayscott2 import advance, seed_field as seed2
    u, v, a, b = seed2(64, [(20, 20), (44, 44)], ["A", "B"]); g = GPUGrid(u, v, a, b)
    advance(u, v, a, b, 0.0367, 0.0649, 0.002, 300, 0.0)
    g.advance(0.0367, 0.0649, 0.002, 300, 0.0, 1); gu, gv, ga, gb = g.fields()
    for x, y in ((u, gu), (v, gv), (a, ga), (b, gb)):
        assert np.allclose(x, y, atol=1e-10)


def test_mutation_turns_every_A_daughter_into_B():
    # S6c: with mu = 1, every daughter of a type-A parent becomes type B, and B spots stay B.
    import pytest
    try:
        from vlife.gs_opencl import run
    except Exception:
        pytest.skip("no OpenCL")
    r = run(3, 0.001, types=("A",) * 4, n=200, max_steps=4000, stall=10 ** 9, mu=1.0)
    info = r["info"]
    kids = [d for d in info.values() if d["parent"] is not None and info[d["parent"]]["div"] is not None]
    born_of_A = [d for d in kids if info[d["parent"]]["div"]["z"] == 1]
    assert r["mutations"][0] == r["mutations"][1] > 0 and len(born_of_A) > 0
    assert all(d["last"]["z"] == 0 for d in born_of_A if d["div"] is None)


def test_reference_noise_has_no_repeats_and_unit_sd():
    # Fix #8 (docs/code_review.md): the old 32-bit key t*2654435761 + 2c gave identical noise for (t, c) and
    # (t + 10946, c - 41233). The new 64-bit key cannot repeat.
    from vlife.gpu_noise import normal, bits
    K = 2654435761
    t, c = np.arange(0, 2000), 41233 + np.arange(0, 2000) * 37 % 48000
    old = lambda t, c: (t * K + 2 * c) % 2 ** 32
    assert np.array_equal(old(t, c), old(t + 10946, c - 41233))              # the old collision
    assert not np.any(bits(7, t, c) == bits(7, t + 10946, c - 41233))
    tt, cc = np.meshgrid(np.arange(300), np.arange(1000), indexing="ij")
    b = bits(7, tt.ravel(), cc.ravel()); assert len(np.unique(b)) == b.size
    z = normal(7, tt.ravel(), cc.ravel())
    assert abs(z.mean()) < 0.01 and abs(z.std() - 1) < 0.01


def test_opencl_noise_matches_reference():
    import pytest
    try:
        from vlife.gs_opencl import GPUGrid
    except Exception:
        pytest.skip("no OpenCL")
    from vlife.gpu_noise import normal
    n = 64; zero = np.zeros((n, n)); g = GPUGrid(zero, zero, zero, zero)
    g.advance(0.0, 0.0, 0.0, 1, 1.0, 11)                  # u = v = 0, F = k = 0: v after one step = max(noise, 0)
    v = g.fields(which=(1,))[0].ravel()
    ref = normal(11, 0, np.arange(n * n))
    assert np.allclose(v, np.maximum(ref, 0.0), atol=1e-12)


def test_numba_run_mutation_matches_opencl_rule():
    # S6d (docs/S6.md): the numba run has the S6c mutation. With mu = 1 every daughter of a type-A parent becomes B;
    # with mu = 0 nothing is mutated and the run is unchanged by the new code path.
    from vlife.grayscott2 import run
    r = run(3, 0.001, types=("A",) * 4, n=120, max_steps=3000, stall=10 ** 9, mu=1.0)
    info = r["info"]
    born_of_A = [d for d in info.values() if d["parent"] is not None and info[d["parent"]]["div"] is not None
                 and info[d["parent"]]["div"]["z"] == 1]
    assert r["mutations"][0] == r["mutations"][1] > 0 and len(born_of_A) > 0
    assert all(d["last"]["z"] == 0 for d in born_of_A if d["div"] is None)
    r0 = run(3, 0.001, types=("A",) * 4, n=120, max_steps=3000, stall=10 ** 9, mu=0.0)
    assert r0["mutations"] == [0, 0] and r0["counts"][-1][2] == r0["counts"][-1][1]      # all spots stay type A
