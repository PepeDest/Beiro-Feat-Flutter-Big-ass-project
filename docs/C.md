# Niche C: negative controls, persistence without use of information

This file starts on 2026-11-24. The plan is in `ROADMAP_ABC.md`. As in `A.md` and `B.md`, each step writes its rules
before its runs, and the results come after.

## C0. Literature check (2026-11-24)

### What we read
- **Bartlett24**: S. J. Bartlett, "Causal Leverage Density: A General Approach to Semantic Information", arXiv:2407.07335
  v1 (10 July 2024). One author. A reader agent read the full arXiv HTML. The paper has no numbered sections or
  equations. The roadmap calls this paper "ALIFE 2024". This is not correct: the arXiv page gives no venue, and a
  Crossref search found no ALIFE 2024 paper on CLD.
- **SowinskiEtAl25**: D. R. Sowinski, S. Holler, M. Wong, G. Segal, D. Parkinson, C. Vidal, J. H. Cleaves, P. Sinhadc,
  A. Prabhu, S. Bartlett, "Causal Leverage Density: A Universal Framework for Semantic Information", ALIFE 2025
  (Proceedings of the Artificial Life Conference 2025), article 43, MIT Press. DOI 10.1162/isal.a.871, checked on
  Crossref. The MIT Press page shows a check against robots, so the user downloaded the PDF (10 pages). We extracted
  its text and read all of it ourselves.
- **SowinskiFrankGhoshal24**: the four-step protocol, read in B0 (`docs/B.md`).

### Causal Leverage Density in Bartlett24
- Start from a known state R₀ at t = 0. An intervention scrambles a part of the syntactic information in R₀. This gives
  R̂₀. The stochastic dynamics do not change.
- p is the distribution of the state at t = τ without the intervention, and p̂ is the distribution with it.
- CLD: χ_LD = D_JS(p ‖ p̂) / Ω_scr. D_JS is the Jensen–Shannon divergence in bits. Ω_scr is "the number of bits that
  were scrambled". χ_LD ≥ 0, and it has no upper bound.
- **No viability.** The paper replaces the viability of KolchinskyWolpert18 with a comparison of future trajectories.
- **Free choices.** The user of the measure chooses τ and the degrees of freedom to scramble. The paper does not say how
  to count Ω_scr for continuous variables.
- **No computed example.** The examples are in words only. The paper has no model, no numbers and no negative control.
- Continuous variables: the formulas are sums over discrete states. Stochastic differential equations appear only as an
  example of dynamics.

### SowinskiEtAl25 (full text)
- **Dynamics**, Eq. (3): a master equation d|Ψ, t⟩/dt = R|Ψ, t⟩. For continuous degrees of freedom it becomes a
  Fokker–Planck equation. So our linear Gaussian systems and our S2 units are inside the setting of the paper.
- **Intervention**: at a time t′, a projection Π(t′) removes the correlations of a chosen subspace. This gives an
  intervened law p̂ ≠ p. The dynamics after t′ do not change.
- **Three measures**, Eqs. (4)–(6), each with a functional F_i of the two laws:
  χ₁(t) = F₁ at time t (instantaneous), χ₂(t₁, t₂) = the maximum of F₂ on [t₁, t₂], and
  χ₃(t₁, t₂) = the time average of F₃ on [t₁, t₂].
- **Functional**, Eq. (7): F_i(p, p̂) = JS(p ‖ p̂) / Ω_scr, as in Bartlett24. The paper says that the JS divergence "is
  not the only choice", and other functionals must be compared.
- **Expected behaviour** (Sec. "A Framework for CLD", in words): CLD must be low when the two sets of trajectories come
  together after a short time, and high when they stay apart.
- **Viability**: CLD does not need it. The paper treats the viability approach of KolchinskyWolpert18 as a special
  case, where meaning is the same as viability.
- **Passive systems**: the paper says that fire "carries little SI", because a rearrangement of its molecules does not
  change it. It expects simple protocells to have low viability-based semantic information. But it expects them to have
  a finite CLD when an intervention changes their form.
- **No computed example and no negative control.** The paper states that the mathematical details and the tests are
  future work. Fig. 1 says that it is not yet clear whether CLD has a plateau or a threshold.

### What this means for niche C
1. **The definition is fixed enough to compute.** We use Eq. (7) with χ₁ and χ₃. The choices that the papers leave
   open (τ, the scrambled degrees of freedom, Ω_scr for continuous variables) are ours, and we write them in the rules.
2. **CLD measures change, not use.** A correlation that decays slowly gives a high CLD, whether or not the system uses
   it. So a rock, which keeps a memory of its well, can get a high CLD with no drive. C2 tests this.
3. **The viability approach has the same risk.** In the S3 organism without feedback, h pushes v and the sensor
   follows h. The value of information ΔV_KW and the stored semantic information do not have to be zero there. C1 tests
   this.

### Search for prior work
- No paper that we found computes CLD for a passive system or for a negative control. Bartlett24 and SowinskiEtAl25
  have no computed values.
- The search used arXiv (title "Causal Leverage Density": one hit, Bartlett24) and Crossref (author Bartlett with
  "semantic information artificial life", 2024 to 2026: one relevant hit, SowinskiEtAl25).
- This is a search result, not a proof that no such work exists.

## C1 and C2: rules (written 2026-11-24, before the runs)

Niche C asks one question: does a semantic score give zero, or a low value, for a system that persists or holds
information without the use of information? We test two scores of the literature on two of our systems.

| Step | System | Negative control | Scores |
|---|---|---|---|
| C1 | S3 homeostat (linear, exact) | the organism without feedback (L = 0) | ΔV_KW, stored semantic information S_KW, CLD |
| C2 | S2b units (nonlinear, simulated) | rocks: memory with no drive | CLD |

### One fact (ours, with a proof)
- **F6. Without feedback, the value of information on v is negative.** Take the S3 organism with L = 0, the agent
  A = (s, m, u, v) and the environment h. Then v_τ = φ_vv v₀ + φ_vh h₀ + φ_vu u₀ + (terms independent of the start).
  Here φ_vv = e^{−k_v τ} > 0 and φ_vh = ∫₀^τ e^{−k_v(τ−s)} e^{−s/T_h} ds > 0. With L = 0, u is independent of h, and
  Cov(v₀, h₀) = ∫₀^∞ e^{−k_v s} e^{−s/T_h} ds > 0 (var(h) = 1). The full scrambling sets Cov(A₀, h₀) to zero, so
  Var(v_τ) falls by 2 φ_vv φ_vh Cov(v₀, h₀) > 0. So the scrambled organism has a higher V = −H(v_τ), and ΔV_KW < 0
  for every τ > 0.
- **With F4 (B4), the stored semantic information is the full information.** The environment is one number and the
  target is one coordinate, so V(p) is monotone. Because ΔV_KW ≠ 0, only p = 1 gives V = V_act. So S_KW = I(A; h) and
  the efficiency is 1, in the organism that uses no information. F4 holds for the intact organism too, so S_KW is
  I(A; h) in both versions whenever ΔV_KW ≠ 0.
- This uses the equality V = V_act of KolchinskyWolpert18, Eq. (9). If a reader uses V ≥ V_act instead, then p = 0
  is enough when ΔV_KW < 0, and S_KW = 0. We report this second reading as a description.

### Our choices for CLD
- **Intervention.** C1: the full scrambling of KolchinskyWolpert18 at t = 0, Cov(A₀, h₀) → 0, from the stationary
  law. C2: the scrambling of one bit, b = sign(x). The start is the stationary law of the unit with x > 0, so b is
  known. The intervention sets b to a fair coin: each walker goes to (−x, −v) with probability ½. Rocks and
  oscillators are symmetric under (x, v) → (−x, −v), so this intervention does not change the dynamics or the
  stationary law.
- **Ω_scr.** C1: I(A₀; h₀) in bits, the information that the scrambling removes. C2: 1 bit.
- **The law p.** The state of the whole system: (A, h) in C1, (x, v) in C2. The agent alone in C1 is a description.
- **JS in C1.** The two laws are Gaussian with mean zero. We compute JS by Monte Carlo with the exact densities
  (200 000 samples from each law, fixed seeds).
- **JS in C2.** A 40 × 40 histogram on a grid that is symmetric about 0. The mirror of the histogram gives
  p̂ = ½(p + Rp) exactly, with R(x, v) = (−x, −v). A second group of walkers starts with b already scrambled, so its
  true CLD is zero. Its value is the bias of the histogram, and we subtract it. Each group has 20 000 walkers.
  dt = 0.01, as in S2b. Burn-in: 50 time units from the S2 start law (S2b uses 200). This is enough for the law inside
  a well or on a cycle. The test of the code ran 20 time units in 3.3 s, so C2 takes about 2 to 3 hours on 4 cores.

### C1. The S3 homeostat
**Data.** The 395 organisms of B4a (`results/e5_dataset_b4.pkl`, rebuilt and checked in B4a). Check A0 of B4a runs
again. Versions: intact and no feedback. The S3 "scrambled" version is the intervention of the S3 VoI, not a separate
system, so C1 does not use it. τ = 1, as in B4a.

**Scores** (for each organism and each version).
- ΔV_KW on v (Eq. (6) of KolchinskyWolpert18, V = −H(v_τ)).
- S_KW on v and the efficiency S_KW / I(A; h), by the root search of B4 with V on v.
- CLD χ₁(τ = 1) on (A, h).

| Rule | Question | Verdict |
|---|---|---|
| A0 | Do the rebuilt S3 data still give the phase C summary? | As in B4a. If not, stop. |
| N1 | Is ΔV_KW zero without feedback? | "zero" if \|ΔV_KW\| < 10^-9 in all organisms, else "not zero". Also the fraction with ΔV_KW < 0. |
| N2 | Is S_KW zero without feedback? | "zero" if S_KW < 10^-9 in all organisms, else "not zero". Also the median efficiency. |
| N3 | Is CLD zero without feedback? | "zero" if χ₁ < 3 times its Monte Carlo standard error in all organisms, else "not zero". |
| N4 | Does each score put the intact organism above the one without feedback? | For each score: the fraction of organisms with score(intact) > score(no feedback), 1000 bootstrap resamples of organisms. "intact higher" if CI low > 0.5, "no feedback higher" if CI high < 0.5, else "no clear order". |

Description only:
- χ₃ on [0, 5] (21 times), and χ₁ on the agent alone.
- ΔV_KW with V on the whole agent, and S_KW in the reading V ≥ V_act.
- The ratio of the median no-feedback score to the median intact score.
- The simulated VoI. It is zero by construction without feedback, because the actuator then reads nothing.

**Expectations.**
- A0: pass.
- N1: "not zero", with ΔV_KW < 0 in all organisms (F6). This is a check of the code.
- N2: "not zero", with efficiency 1 in all organisms (F4 and F6). This is a check of the code too.
- N3: "not zero". The sensor s and the memory m follow h in both versions, and CLD sees this correlation.
- N4: ΔV_KW "intact higher". S_KW and CLD: no firm expectation.

### C2. The S2b rocks and oscillators
**Data.** The S2b units of the 7 draws (seeds 2026 to 2032, 60 rocks and 60 oscillators each). The `.pkl` files of
draws 2027 to 2032 are not on this PC. So we run the V part of `e6b_rockmemory.py` again for all 7 draws, with the
same code and seeds.

**Scores** (for each unit).
- χ₃(0, τ*): the time average of CLD on [0, τ*], on 41 equal steps. τ* = the median rock V of the draw, as in S2b.
- χ₁(τ*): CLD at τ*.

| Rule | Question | Verdict |
|---|---|---|
| T1 | Do the rebuilt data give the S2b values? | "pass" if τ* and the median log(V_on / V_off) of the oscillators equal `e6b_summary*.json` to 10^-9 in all 7 draws. If not, stop. |
| K1 (main) | Does χ₃ rate rocks above oscillators of the same life? | The stratified AUC of S2b in each draw (tertiles of log V, bins with at least 5 units of each class, at least 2 bins, AUC = P(rock > oscillator)). Then the mean over the 7 draws, with 10 000 bootstrap resamples of draws, as in S2b Q3. "CLD mislabels rocks" if CI low > 0.5. "CLD favours oscillators" if CI high < 0.5. Else "no difference". |
| K2 | The same for χ₁(τ*) | As K1. |
| K3 | Does χ₃ follow the memory of a rock? | ρ(χ₃, log V) over the rocks of each draw, mean over draws, bootstrap over draws. "yes" if CI low > 0. |
| Gate (roadmap) | Does CLD pass the control? | "passes" if K1 says "CLD favours oscillators". Else "fails", and we report the flux ratio V_on / V_off as the fix. |

Description only: χ₁ at the own lag V/2 of each unit, the bias of the histogram (the second group), the AUC of each
draw, and the AUC of C(τ*) from the S2b summaries.

**Expectations.**
- T1: pass. The code and the seeds are the same.
- K1 and K2: "CLD mislabels rocks", with a large AUC (above 0.8). An oscillator loses its phase by phase diffusion
  before τ* (in S2b, C(τ*) was about 0 for oscillators). A rock keeps its well for a time of the order of V.
- K3: yes.
- Gate: fails.

**Note.** Neither rocks nor oscillators use information about an environment. C2 asks the question of S2: does a
score rate passive memory as high as persistence that a drive keeps? A score of the use of information must not prefer
the rock.

### Limits of C
- Our choices fix CLD where the papers leave it open: the scrambled bit, Ω_scr, τ and the grid. Another choice can
  give another result. C2 uses one bit, the sign of x, for both classes.
- JS is the functional of Eq. (7). SowinskiEtAl25 say that other functionals need a test. We test only JS.
- C1 uses Gaussian interventions and exact formulas. C2 uses histograms with a bias correction.

### What we saw before the rules
Only checks of the code, on inputs outside the data: the tests, one organism drawn with seed 998 (both versions), one
rock with h = 0.3 for 6 time units, and one synthetic oscillator for the timing. We did not compute any score of the
395 organisms or of the S2b units.

**Code.** `src/vlife/negative_controls.py`, and a `target` option in `semantic_apply.stored_semantic`. Tests:
`tests/test_negative_controls.py` (7 tests). Runs: `experiments/e25_c1_homeostat.py` (a few minutes) and
`experiments/e26_c2_rocks.py` (about 3 to 4 hours: the V rebuild of 7 draws, then CLD).

## C1 and C2. Results (2026-11-26)

### C1. The S3 homeostat
Run: `experiments/e25_c1_homeostat.py`. Output: `results/e25_c1_homeostat.md` and `.json`, log `results/e25_run.log`.
A0 passes. 395 organisms, two versions each (intact, no feedback).

| Rule | Value | Verdict | Expectation |
|---|---|---|---|
| A0 | the rebuilt S3 data equal the phase C summary | pass | pass. Met. |
| N1 | ΔV_KW < 0 in 1.000 of the organisms without feedback, median −0.2551, largest \|ΔV_KW\| 0.32 | not zero | "not zero", ΔV_KW < 0 in all (F6). Met. |
| N2 | smallest S_KW 0.283 nats, efficiency 1 in 1.000 of the organisms | not zero | "not zero", efficiency 1 in all. Met. |
| N3 | smallest χ₁ 0.0303, smallest χ₁ / se 60.4, median χ₁ 0.0943 | not zero | "not zero". Met. |
| N4, ΔV_KW | fraction intact > no feedback 0.787 [0.747, 0.823] | intact higher | "intact higher". Met. |
| N4, S_KW | 0.433 [0.385, 0.481] | no feedback higher | no firm expectation |
| N4, CLD χ₁ | 0.600 [0.552, 0.646] | intact higher | no firm expectation |

Description only (medians, intact / no feedback):
- χ₁: 0.0952 / 0.0943 (ratio 0.99). χ₃ on [0, 5]: 0.0576 / 0.0544. χ₁ on the agent alone: 0.0486 / 0.0381.
- S_KW: 0.7726 / 0.8144 nats (ratio 1.05). S_KW equals I(A; h) in all 790 cases (the root search finds only p = 1).
- ΔV_KW: −0.0230 / −0.2551. The median intact organism also has ΔV_KW < 0.
- ΔV_KW on the whole agent is < 0 in 0.577 of the organisms without feedback.
- In the reading V ≥ V_act, S_KW is 0 in all organisms without feedback, and the median is 0 in the intact version too.
- The simulated VoI is 0 without feedback, by construction.

**What C1 shows.** No score of the three gives zero for the organism that uses no information. ΔV_KW is not zero, but
it is negative, and it ranks the intact organism higher in 79 % of the organisms. So the sign of ΔV_KW carries the
control, not its size. S_KW is the full information I(A; h) in both versions, so it measures correlation, not use.
It is a little higher without feedback. CLD gives the same median value to both versions (ratio 0.99). The sensor and
the memory follow h in both versions, and CLD sees this correlation. The order 0.600 is above 0.5, but it is a small
effect. The second reading of KolchinskyWolpert18 (V ≥ V_act) gives zero without feedback, but it also gives zero for
the median intact organism. So it does not separate the two versions either.

### C2. The S2b rocks and oscillators
Run: `experiments/e26_c2_rocks.py --resume`. Output: `results/e26_c2_rocks.md` and `.json`, log `results/e26_run.log`.
T1 passes in all 7 draws. 20 000 walkers in each group, dt = 0.01.

| Rule | Value | Verdict | Expectation |
|---|---|---|---|
| T1 | τ* and the median log(V_on / V_off) equal the S2b summaries in all 7 draws | pass | pass. Met. |
| K1 (main) | stratified AUC of χ₃(0, τ*) 0.711 [0.676, 0.748] | CLD mislabels rocks | "CLD mislabels rocks". Met. AUC above 0.8: not met. |
| K2 | stratified AUC of χ₁(τ*) 0.632 [0.576, 0.696] | CLD mislabels rocks | "CLD mislabels rocks". Met. AUC above 0.8: not met. |
| K3 | ρ(χ₃, log V) over rocks 0.997 [0.996, 0.998] | yes | yes. Met. |
| Gate | K1 is not "CLD favours oscillators" | fails | fails. Met. |

Description only:
- Stratified AUC of χ₃ in each draw: 0.646 to 0.784. All 7 draws are above 0.5. Draws 2026 and 2031 have 2 bins, the
  others 3.
- Unstratified AUC of χ₃ in each draw: 0.706 to 0.835.
- Median χ₃: rocks 0.051 to 0.054 in every draw, oscillators 0.027 to 0.042.
- At τ*, CLD is small. Median χ₁(τ*): rocks 0.0019 to 0.0028 bits, oscillators 0.0003 to 0.0014 bits. The bias of
  the histogram at τ* is about 0.0049 bits, and we subtract it. So K2 rests on a value below the size of the bias.
  K1 uses the whole interval [0, τ*], where CLD is larger, and is the main rule.
- At the own lag V/2 of each unit (unstratified), the mean AUC is 0.341. At this lag CLD rates oscillators higher.
  Each unit has a different lag here, so this is not a test of the same life.
- In S2b, the AUC of memory C(τ*) was 0.575 (mean of the 7 draws). CLD mislabels rocks more strongly than C.
- Time: 150 min for CLD on 4 cores. The V rebuild of the first run took about 55 min.

**Run note.** The first run stopped on 2026-11-24 at 23:50, during the CLD part, because Windows shut down (system
event 1074). T1 had passed in all 7 draws. The V data was saved in `results/e26_v_dataset.pkl`. We added the option
`--resume`: it loads this file, runs T1 again on it, and saves the CLD results after each draw. The rules did not
change. The log of the first run is `results/e26_run_1_shutdown.log`.

**What C2 shows.** CLD rates rocks above oscillators of the same life, in all 7 draws. Among rocks, χ₃ follows log V
almost exactly (ρ = 0.997). So χ₃ measures how long the bit sign(x) stays in memory. A rock keeps its well for a time
of the order of V, and an oscillator loses its phase earlier. Neither class uses information, but CLD prefers the
passive memory. The flux ratio V_on / V_off separates the two classes with no overlap in S2 and S2b (docs/S2.md).
It is the fix that the roadmap gate asks us to report.

### What niche C shows
| Score | Control | Gives zero or a low value? | Verdict |
|---|---|---|---|
| ΔV_KW | S3 without feedback | no: negative, and ranks intact higher (0.787) | fails as a zero test, passes as an order |
| S_KW | S3 without feedback | no: equals I(A; h), a little higher without feedback | fails |
| CLD | S3 without feedback | no: same median as intact (0.99) | fails |
| CLD | S2b rocks | no: rocks above oscillators (0.711) | fails |

No score gives zero for a system that holds information without use. The scores measure correlation or memory. A
test of use needs a term that sees the drive or the feedback. In S3 this is the simulated VoI, which is zero without
feedback by construction. In S2 it is the flux ratio.

**Limits.** The limits of the rules hold (see "Limits of C"). Also:
- K2 is close to the bias of the histogram.
- The expectation "AUC above 0.8" was not met. The verdicts of K1 and K2 do not depend on it.
- We test one choice of the bit, of Ω_scr and of the grid. The CLD papers leave these choices open.
