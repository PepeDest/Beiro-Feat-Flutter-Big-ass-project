# Long jobs of niches D, F and G

`run_cluster.py` runs the heavy tasks of `experiments/e27_d_rochester.py` (D1, D2), `experiments/e28_f_cld_map.py` (F1)
and `experiments/e29_g_te_dt.py` (G3) on all cores. The rules of each job are in `docs/D.md`, `docs/F.md` and
`docs/G.md`. They were committed before any run. The instructions for the person who runs the zip are in `LEGGIMI.md`.

| Job | Tasks | Core-hours on the test PC | Output of one task |
|---|---|---|---|
| d1 | 1606 (8 sets × 200 values of η, and 6 deaf agents) | 42 | mean, SE, quantiles and 1000 bootstrap means of the life |
| d2 | 6528 (3 graphs × 64 couplings × (32 η + no agent + still agent)) | 44 | r of each run, information per kick |
| f | 840 (one unit each) | 57 | 5 functionals × 3 histograms × 2 walker numbers × 2 groups, on 83 times |
| g3 | 1200 (300 systems × 4 values of τ) | 228 | S_TE, D_T* and their sensors on the grid |

Each task writes `cluster_out/<job>/<task>.json` atomically, so a stopped run restarts without loss. `--part k/n` splits
the tasks by a hash of their names. `--pack` writes `results_cluster_out_<host>.zip`.

**Analysis (on the home PC).** Unzip all result files into `cluster_out/`, then:

```
python experiments/e27_d_rochester.py cluster_out
python experiments/e28_f_cld_map.py cluster_out
python experiments/e29_g_te_dt.py cluster_out
```

**Reproducibility.** Each run has its own seed from `numpy.random.SeedSequence` of the task key. The results do not
depend on the number of machines or workers. They can depend on the versions of numpy and numba in the last digits.
`machine.json` records the machine of each part.

**Build the zip.** `python cluster/make_bundle.py` writes `cluster_bundle_<date>.zip` with the code, the data file
`cluster/data/f_units.json` and `SHA256SUMS.txt`.
