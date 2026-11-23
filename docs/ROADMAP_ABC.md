# Roadmap A, B, C: three small results for three research groups

Written 2026-11-20. This file sets the goals after the paper (`paper/`). The first programme (S0–S6) is in `ROADMAP.md`.

## The aim in one sentence
Make three small results. Each result uses a recent paper by a specific group and gives that group a tool or a test
that they can use at once.

| Niche | Question | Main readers | Uses our | Cost |
|---|---|---|---|---|
| **A** | Which part of dissipation shortens the life of a structure? | Kolchinsky, Ito, Nagayama (Tokyo) | Linear worlds (S1), σ_A (S2c) | Low. This PC, days |
| **B** | Can we compute semantic information exactly in linear Gaussian systems? | Kolchinsky, Sowinski, Frank, Ghoshal (Rochester), Bartlett | Gaussian code, homeostat (S3) | Medium. Mostly mathematics, weeks |
| **C** | Does a semantic score give zero for structures that persist without use of information? | Bartlett (Caltech), Sowinski | Rocks (S2), no-feedback organisms (S3) | Low for C1, high for C2 (multicore CPU) |

## Rules that stay the same
1. **Pre-registration.** Before each run, write a step file in `docs/` with the question, the rule, the verdict labels
   and our expectations. Commit it before the run. Add the results later, below the rules.
2. **Code.** New experiments go in `experiments/e15_*.py` and later numbers. They write to `results/` and add rows to
   `PROVENANCE.md`. Each new formula gets a reference key or a "novel" flag in `REFERENCES.md`.
3. **Novelty.** Before each niche starts, repeat the literature check (step 0 of each niche) and log it in
   `PROVENANCE.md`. A check can only make a claim less likely to be wrong. It cannot prove that nobody did the work.
4. **Honest scope.** A negative result is a result. Report it with the same care.

## Novelty check of 2026-11-20 (what we know now)
- Semantic Scholar: all 181 papers that cite Kolchinsky & Wolpert 2018, Sowinski et al. 2023 or Bartlett et al. 2025.
  None gives an exact linear Gaussian computation of semantic information. None links it to minimal-information
  control.
- Minimal information for linear Gaussian control **is known**: Tanaka et al. (IEEE TAC 2018), Sabag, Tian, Kostina
  and Hassibi (IEEE TAC 2023). So the mathematics of "how much information is enough" is not new. The link to semantic
  information is the new part.
- Nagayama, Kolchinsky and Ito (arXiv 2606.07263, 2026) split the entropy production of an Ornstein–Uhlenbeck process
  into an oscillatory part and a nonnormal part. Its 5 citing papers do not use it for persistence or exit times.
- Not checked yet: nonnormal amplification of noise and exit times (Trefethen & Embree, tipping literature). Step A0
  must check this.

---
## Niche A. Which dissipation shortens life?

**Why it matters to them.** Their decomposition (Eq. 8–10 of arXiv 2606.07263) is about thermodynamics. It does not say
what each part does to a structure. They show that the nonnormal part goes with faster relaxation. Faster relaxation and
transient amplification can change exit times. Our S2c found that total dissipation has no clear link to life in the S1
baseline and shortens life in the D-test. The decomposition can explain this sign change.

**The two parts, for dx = −Bx dt + √(2D) dW (their K is our B).**
- σ_osc = Σₙ Im(λₙ)² / Re(λₙ), with λₙ the eigenvalues of B (their Eq. 9). Closed form.
- σ_nn = σ − σ_osc, with σ from `gaussian.entropy_production`. It is zero if and only if D^{-1/2} B D^{1/2} is normal.

**Steps**
| Step | Work | Done when |
|---|---|---|
| A0 | Literature check: nonnormality and exit times, nonnormality and persistence. Read the full text of 2606.07263, including the appendix and the supplemental material | A log in `PROVENANCE.md` and a short note in `docs/A.md` |
| A1 | Add `oscillatory_nonnormal_ep(B, D)` to `src/vlife/gaussian.py`. Test: σ_osc + σ_nn = σ. Test their bead-spring example | Tests pass |
| A2 | World level, no new simulation. On the S1 data (`_v2`, `_D3_v2`), relate σ_osc and σ_nn of each world to the mean log V of its structures | Pre-registered rules and results in `docs/A.md` |
| A3 | Controlled worlds. Fix the eigenvalues of B and change only the nonnormality (their construction through K_D). Measure the exit times of the same structures | A plot of log V against σ_nn at fixed σ_osc |
| A4 | Structure level. Apply the decomposition to the local block (B_AA, D_AA) of each structure. This step is our choice and gets a "novel" flag | Pre-registered rules and results |

**Expectation to write in `docs/A.md` before A2 (a draft, not yet fixed).** At fixed eigenvalues, a higher σ_nn gives a
shorter life, because transient amplification pushes the state out of the viability set. σ_osc has a smaller effect.

**Gate.** If σ_nn and σ_osc have the same link to life as total σ, the decomposition adds nothing for persistence.
Report it as a short negative note and move to B.

**Result for the readers.** A figure: life of a structure against σ_nn and σ_osc, with the sign change of S2c
explained or not explained.

---
## Niche B. Exact semantic information in linear Gaussian systems

**Why it matters to them.** Sowinski et al. and Bartlett et al. state that the computation of semantic information is
too expensive for large systems. Kolchinsky (arXiv 2610.07360, 2026) proves that Gaussian channels are optimal for some
information quantities in Gaussian systems. Control theory can compute minimal information for linear Gaussian systems
with semidefinite programs. If these pieces fit, semantic information becomes exact and cheap in linear Gaussian systems
of any size.

**Steps**
| Step | Work | Done when |
|---|---|---|
| B0 | Read the full texts: Kolchinsky & Wolpert 2018 (viability function, interventions, information–viability curve), Sowinski 2023 and 2024 (scrambling by sensor noise, transfer entropy), Tanaka 2018, Sabag 2023, Kolchinsky 2026 | A note in `docs/B.md` with each definition in our notation |
| B1 | Static case. Joint Gaussian agent X and environment Y, linear dynamics. Viability = −H(X_τ). Full scrambling sets the X–Y block of the covariance to zero. Write the viability value in closed form | Formula and code agree with Monte Carlo within error |
| B2 | Partial scrambling with Gaussian channels. Compute the information–viability curve and the semantic threshold. On a small discrete case, compare with the brute-force search of Kolchinsky & Wolpert | The two curves agree, or the gap is measured |
| B3 | Dynamic case. Write the scrambling of Sowinski as a problem of minimal directed information, as in Tanaka 2018. State the link as a conjecture and test it numerically | A statement: equal, a bound, or false. With the numbers |
| B4 | Apply it. (a) S3 homeostat: semantic threshold against our VoI. (b) S1 worlds: semantic information against Φ_TC on the same structures (open question 6 of the paper) | Pre-registered rules and results |

**Gate.** If Gaussian channels are not optimal in B2, the result is a bound, not an exact value. Report it as a bound.
If B3 shows no link, keep B1 and B2 as a benchmark with known answers.

**Result for the readers.** Code that gives the exact semantic threshold of any linear Gaussian agent–environment
system. Also a test case with a known answer for their numerical estimators.

---
## Niche C. Negative controls: persistence without use of information

**Why it matters to them.** A semantic score must be zero when a system holds information but does not use it. Our data
has two such classes. S3 organisms without feedback hold information about the hidden state, but the actuator does not
use it. S2 rocks persist for a long time with no drive. In S2b, memory C rated rocks slightly above oscillators. Bartlett
and Sowinski propose Causal Leverage Density (CLD), which does not need viability. CLD can fail on rocks in the same way.

**Steps**
| Step | Work | Done when |
|---|---|---|
| C0 | Read the CLD papers (ALIFE 2024 and 2025) and the protocol of Sowinski, Frank and Ghoshal 2024 (four steps) | A note in `docs/C.md` |
| C1 | With the code of B, compute semantic information for intact, scrambled and no-feedback organisms of S3 | Pre-registered rules and results. Expectation: no-feedback gives zero |
| C2 | Compute CLD for S2 rocks and oscillators. Ask: does CLD rate rocks as high as oscillators? | Pre-registered rules and results. AUC with a CI, as in S2b |

**Gate.** If CLD separates rocks from oscillators, report that it passes the control. If it does not, report the failure
and the flux ratio as a fix.

**Result for the readers.** A set of negative controls, with code, that any semantic or agency score must pass.

---
## Order and dependencies
1. **A** first. It needs no new theory, it runs on this PC, and A2 needs no new simulation.
2. **B** next. B0 and B1 can start during A3.
3. **C1** after B2, because C1 uses the code of B. **C2** can start at any time, but it needs a multicore CPU.

## Output and contact
| Niche | Output | Who to send it to |
|---|---|---|
| A | A short note (letter length) on arXiv | Ryuna Nagayama, Sosuke Ito, Artemy Kolchinsky |
| B | A full paper on arXiv, with the code | Artemy Kolchinsky, Damian Sowinski |
| C | A section of the B paper, or a conference paper (Artificial Life) | Stuart Bartlett, Damian Sowinski |

Send a short email with a one-page summary and the link. Send it only after the result is final and checked.

## What counts as success
- **A:** a clear sign for σ_nn at fixed eigenvalues, with a CI that excludes zero, in worlds made for the test.
- **B:** an exact formula or a proved bound, and code that runs on a system with at least 50 variables.
- **C:** a verdict, pass or fail, for each score on each negative control.

## Hardware
- A and B run on this PC.
- C2 needs many simulations of nonlinear units. A machine with two multicore Xeon processors makes it about 8–12 times
  faster. The Quadro P4000 cards help only if the code moves to single precision.

## References for this roadmap
- Nagayama, Kolchinsky, Ito. Oscillatory-nonnormal decomposition of dissipation in Ornstein–Uhlenbeck processes.
  arXiv 2606.07263 (2026).
- Kolchinsky. Redundancy and synergy in multivariate Gaussians via the Blackwell order. arXiv 2610.07360 (2026).
- Kolchinsky, Wolpert. Interface Focus 8, 20180041 (2018). doi:10.1098/rsfs.2018.0041.
- Sowinski et al. PRX Life 1, 023003 (2023). doi:10.1103/prxlife.1.023003.
- Sowinski, Frank, Ghoshal. Phys. Rev. Research 6, 043188 (2024). arXiv 2404.02221.
- Bartlett et al. PRX Life 3, 037003 (2025). doi:10.1103/rsx4-8x5f.
- Tanaka, Mohajerin Esfahani, Mitter. LQG control with minimum directed information. IEEE TAC (2018).
- Sabag, Tian, Kostina, Hassibi. Reducing the LQG cost with minimal communication. IEEE TAC (2023).
- Sowinski et al. Causal Leverage Density. ALIFE 2025, doi:10.1162/isal.a.871.

The two IEEE TAC entries and the Causal Leverage Density entry are not checked against Crossref yet. Step 0 of each niche
must check them.
