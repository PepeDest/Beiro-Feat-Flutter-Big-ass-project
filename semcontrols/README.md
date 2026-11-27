# semcontrols

Negative controls with known answers for scores of semantic information.

A score of semantic information claims to measure the information that a system **uses** to stay alive. Many systems
hold information that they do not use. `semcontrols` gives three families of such systems, with known answers, and one
function that runs a score on them.

A "pass" on these controls is necessary, not sufficient. The controls test only that a score does not confuse
correlation or passive memory with use.

## Install

From a clone of the repository:

```
pip install ./semcontrols
```

Or with pip from the git URL of the repository, with `#subdirectory=semcontrols` at the end. The package needs
Python 3.10 or later, numpy and scipy.

Run the tests:

```
pip install "./semcontrols[test]"
pytest semcontrols/tests
```

## The controls

| Control | Systems | Known answer |
|---|---|---|
| `controls.homeostat(i, version)` | 400 linear homeostats: a hidden state h, a sensor s, a memory m, an actuator u and a viability variable v. `version` is `"intact"` or `"nofeedback"` (loop gain 0) | Without feedback, the organism uses no information: its actuator reads nothing. The intact organism uses information (a simulated value of information above 0 in 99 % of the organisms) |
| `controls.reader(j)` | 200 linear systems in which the environment reads the agent and does not act on it | The agent cannot use information about the environment. ΔV of Kolchinsky and Wolpert and the stored semantic information are 0 for every time τ |
| `controls.units()` | 840 nonlinear units: rocks (a double well, passive memory) and oscillators (active friction, a driven cycle), in 7 draws of 120 units | No unit uses information about an environment. A score of use must not rate rocks above oscillators of the same life. The flux ratio log(V_on / V_off) is 0 for rocks and above 0 for oscillators |

Each linear control is a `LinearSystem`: dz = −B z dt + √(2D) dW, with the stationary covariance `S` and the index
lists `agent`, `env` and `target` (the coordinates whose spread sets the viability). Each unit is a `Unit` with its
parameters, its mean lifetime with the drive on (`V_on`) and off (`V_off`), the time `tau_star` of its draw, and the
CLD values of the full run in `reference`.

## Add a score

Write a function that takes a control and returns a number. Then call `check`:

```python
import semcontrols as sc

def my_score(system):          # a LinearSystem
    ...

result = sc.check(linear_score=my_score)
print(sc.report(result))
```

For the units, give `unit_score=` (a function of a `Unit`) or `unit_values=` (a dict from `(seed, i)` to a number).

| Test | Question | Verdict |
|---|---|---|
| `homeostat_zero` | Is the score 0 without feedback? | "pass" if \|score\| ≤ `tol` in all organisms |
| `homeostat_order` | Does the score put the intact organism above the one without feedback? | "pass" if the 95 % bootstrap CI of the fraction lies above 0.5 |
| `reader_zero` | Is the score 0 when the environment only reads the agent? | as `homeostat_zero` |
| `rocks_order` | Does the score rate rocks above oscillators of the same life? | the AUC(rock > oscillator) inside tertiles of log V_on, mean over the 7 draws. "fail" if the 95 % CI lies above 0.5 |

## Reference scores

`scores.kw_value` (ΔV of Kolchinsky and Wolpert 2018, Eq. (6)), `scores.kw_stored` (their stored semantic
information, for one environment coordinate), `scores.cld_linear` and `scores.cld_unit` (Causal Leverage Density of
Bartlett 2024 and Sowinski et al. 2025), and `scores.flux_ratio`.

## Example

`python semcontrols/examples/example.py` runs ΔV and CLD on each control with small sizes. It takes about 7 s on a
4-core PC. For the units it uses the stored CLD values of the full run (20 000 walkers in each group, about 2.5 hours
on 4 cores), and it runs CLD on one rock and one oscillator.

| Score | `homeostat_zero` | `homeostat_order` | `reader_zero` | `rocks_order` |
|---|---|---|---|---|
| ΔV of Kolchinsky and Wolpert | fail (negative, F6) | pass | pass | — |
| CLD χ₁ | fail | fail (small sizes in the example) | fail | fail (AUC 0.711) |
| flux ratio | — | — | — | pass (AUC 0) |

With the full sizes (`homeostat_ids` = the 395 organisms of the source study), the order fraction of CLD is 0.600
[0.552, 0.646], a "pass", and the one of ΔV is 0.787 [0.747, 0.823].

## Source

The controls and the reference results come from the repository `variational_life`: `docs/S2.md`, `docs/S3.md`,
`docs/B.md`, `docs/C.md` and `docs/I.md`. The checks of this package against that code are in
`experiments/e32_i_semcontrols.py`.

## References

- A. Kolchinsky, D. H. Wolpert, "Semantic information, autonomous agency and non-equilibrium statistical physics",
  Interface Focus 8, 20180041 (2018).
- S. J. Bartlett, "Causal Leverage Density: a general approach to semantic information", arXiv:2407.07335 (2024).
- D. R. Sowinski et al., "Causal Leverage Density: a universal framework for semantic information", ALIFE 2025,
  article 43 (2025).
