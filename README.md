# vlife — Variational Life Lab

A small, tested research code base. It asks one question:

> Does an information-theoretic score of organisation (Φ) predict whether a structure survives, in simple stochastic worlds?

The work follows a roadmap of seven steps (S0–S6). Each step has rules that were written **before** its data existed,
then a run, then results. Post-hoc checks are labelled as such. The full history is in `docs/`.

## Results in short

| Step | Question | Main result | Details |
|---|---|---|---|
| S0 | Do the shipped results reproduce? Are the references right? | Yes (largest change 0.003). All 62 references match Crossref. | `docs/RESULTS.md`, `docs/REFERENCES.md` |
| S1 | Does the result hold when τ, p_out, N and the noise change? | No for the original Φ: its verdict depends on τ and on the noise. Persistence C predicts life in all 9 settings. | `docs/S1.md` |
| S1b | A complexity term that does not depend on units | P + C − 0.25·TC predicts life in all 9 settings. | `docs/S1b_unitfree.md` |
| S2 | Does C rate passive "rocks" like drive-sustained oscillators? | Cutting the drive separates the two classes. At a long lag, C rates rocks higher (weak signal). | `docs/S2.md` |
| S2c | A dissipation term in Φ | Tracks life where the drive builds the structure. Hurts where the drive only stirs it. | `docs/S2c.md` |
| S3 | Does information pay when it is used? | Yes: breaking the sensor–actuator link shortens life about 3.6 times. | `docs/S3.md` |
| S4 | Population growth rate as viability | Ranks like the mean exit time, because lives are near exponential. | `docs/S4.md` |
| S5 | Boundaries by conditional independence | Planted blankets are found. The static blanket breaks down as the drive grows. The dynamic one stays exact. | `docs/S5.md` |
| S6 | Replication, heredity, selection, mutation (Gray–Scott spots) | Selection and transmission terms are measured per generation, with a neutral control. No sharp error threshold in finite colonies. | `docs/S6.md` |

Overall status, and what would count as support for the theory: end of `docs/ROADMAP.md`.

## Layout

| Path | What |
|---|---|
| `src/vlife/` | The library: Gaussian information terms, worlds, viability, estimators, and the models of each step |
| `src/vlife/gaussian.py`, `worlds.py`, `functional.py`, `viability.py` | Linear (OU) worlds, exact information terms, exit-time viability, growth rate |
| `src/vlife/agency.py` | S3: a linear homeostat (sensor, memory, actuator) |
| `src/vlife/nonlinear.py` | S2: inertial units (rocks, active oscillators) |
| `src/vlife/blankets.py` | S5: planted structures and Markov-blanket detectors |
| `src/vlife/grayscott.py`, `grayscott2.py`, `gs_opencl.py` | S6: Gray–Scott spots (numpy, numba, GPU with OpenCL) and the spot tracker |
| `experiments/` | One script per experiment (`e0` … `e12`, plus `s1_*` and `s1b_*`). Each script writes to `results/` |
| `results/` | Reports (`*_report.md`, `*.json`), figures, logs and simulation data (`*.pkl`) |
| `results_shipped/` | The results that came with the original zip, kept to compare against |
| `docs/` | Theory, rules and results of each step, provenance of every formula, references |
| `tests/` | 36 tests (`pytest`) |
| `legacy/` | The original script that started the project |

## How to run

You need Python 3.10 or later. On Windows, use PowerShell or Git Bash.

1. Create an environment and install the packages:

   ```bash
   python -m venv .venv
   .venv/Scripts/python -m pip install -r requirements.txt
   ```

   On Linux or macOS, use `.venv/bin/python` instead of `.venv/Scripts/python`.

2. Run the tests (about 1 minute):

   ```bash
   .venv/Scripts/python -m pytest -q tests
   ```

   The GPU tests are skipped if no OpenCL device is found.

3. Run an experiment from the `experiments` folder:

   ```bash
   cd experiments
   ../.venv/Scripts/python e5_agency.py
   ```

### Experiments and run times

Times are for the PC used here: Intel i5-6500 (4 cores) and AMD RX 580.

| Step | Command (from `experiments/`) | Time |
|---|---|---|
| S0 | `python run_all.py` (E0–E4, baseline) | about 30 min |
| S1 | `python e3_phi_vs_viability.py --n_worlds 30 --n_traj 600 --t_max 200 --p_out 0.2 --tag _p0.2` (one setting; see `docs/S1.md` for all), then `python e4_merging.py --tag _p0.2` and `python s1_summary.py` | 30 min to 3.5 h per setting |
| S1b | `python s1b_unitfree.py` (needs the S1 data) | a few minutes |
| S2 | `python e6_fluxcut.py`, then `python e6b_rockmemory.py` | 11 min, 15 min |
| S2c | `python e7_dissipation.py` (needs the S1, S2 and S2b data) | 1 min |
| S3 | `python e5_agency.py`, then `python e5b_lag.py` | 3 min, 1 min |
| S4 | `python e9_growth.py` (needs the S1 data) | 1 min |
| S5 | `python e8_blankets.py --calibrate`, then `python e8_blankets.py` | 2 min |
| S6 | `python e10_grayscott.py --pilot`, then `python e10_grayscott.py` | 10 min |
| S6b | `python e11_selection.py --pilot`, then `python e11_selection.py --workers 5` (GPU) | 5 min, 11 min |
| S6c | `python e12_mutation.py --workers 5` (GPU, needs `results/e11_runs.pkl` only for the prediction in `docs/S6.md`) | 25 min |

Most scripts use all CPU cores through `--workers` (default 4). Set `OMP_NUM_THREADS=1` when you run several processes
at the same time.

### GPU (S6b, S6c)

`src/vlife/gs_opencl.py` runs the Gray–Scott grid on an OpenCL GPU in double precision (about 65 times faster than the
numba version on the RX 580). It needs `pyopencl` and a GPU driver with OpenCL and float64 support. A test checks the GPU
kernel against the numba kernel, and the numba kernel against the numpy code.

## Notes

- **Seeds.** Every run uses a fixed seed (mostly 2026), so the numbers in `docs/` can be reproduced.
- **Data files.** The simulation data (`*.pkl`, about 250 MB) are not in this repository. The reports, JSON summaries,
  figures and logs in `results/` are. To get the data, run the experiments above. Some analyses (S1b, S2c, S4, S6c)
  read data from earlier steps, so run the steps in order. Load only pickle files that you made yourself or trust.
- **References.** Every formula in the code has a `[Key]` tag. `docs/REFERENCES.md` resolves it (with DOIs), and
  `docs/PROVENANCE.md` says whether it is established, adapted, a hypothesis or new.
- **The original README** of the zip is in `docs/README_v0.md`.
