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
