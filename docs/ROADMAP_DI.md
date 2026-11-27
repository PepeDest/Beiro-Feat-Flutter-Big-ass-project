# Roadmap D to I: six results that save work for the groups

Written 2026-11-27, after the paper of niches B and C (`paper_bc/`). The roadmap of A, B and C is in `ROADMAP_ABC.md`.
The rules of `ROADMAP_ABC.md` stay the same: pre-registration, code in `experiments/`, novelty checks, honest scope.

## The aim in one sentence
Each niche does a piece of work that a group names as "future work" or does not do, and gives it to them with code.

| Niche | Question | Main readers | Where it runs | Cost |
|---|---|---|---|---|
| **D** | Do the two models of the Rochester group give the published results, and how much of their viability needs no information? | Sowinski, Frank, Ghoshal, Kolchinsky | Xeon machines (`cluster/`) | High: about 10^8 simulated runs |
| **E** | What is the semantic information of a real cell (E. coli chemotaxis)? | Kolchinsky, Wolpert, Emonet, Machta, ten Wolde | This PC | Low |
| **F** | Which free choices of CLD change the verdict on the rocks? | Bartlett, Sowinski | Xeon machines (`cluster/`) | High: 840 units, 3 estimators |
| **G** | Is TE ≤ DT true after the first step? | Tanaka, Kolchinsky | This PC (G1, G2), Xeon machines (G3) | Medium |
| **H** | What does semantic information cost in energy, in linear systems? | Kolchinsky, Ito, Nagayama | This PC | Low |
| **I** | A Python package of negative controls with known answers | All groups | This PC | Low |

## Niche D. Replication and controls in the models of the Rochester group
**Why it matters to them.** Sowinski23 (foraging agent) and SowinskiFrankGhoshal24 (Kuramoto agent) publish no code.
Sowinski23 reports about 8000 core-hours for each set of parameters. Both papers find the semantic threshold by eye, or
by a smoothed curve with no stated method. Both state analytic predictions (η_c = arcsin(r/R)/π, Eq. (11), Eq. (9)
of Sowinski23, K_c^A and the efficacy of SowinskiFrankGhoshal24) that a high-statistics run can test.

| Step | Work | Done when |
|---|---|---|
| D0 | Read the full texts. Write the model of each paper in our notation, with each detail that the paper does not state | A note in `docs/D.md` |
| D1 | Foraging agent: V(η) for 6 speeds and 3 sensing radii, 10^4 runs for each of 200 values of η. A fixed estimator of the threshold with a bootstrap CI. Test Eq. (4), Eq. (9) and Eq. (11) | Pre-registered rules and results |
| D2 | Kuramoto agent: the efficacy on the fully connected, Poisson and scale-free graphs. The viability per bit with a CI. Test the reported values 1.5, 0.25, 0.886 and 0.841, and K_c^A | Pre-registered rules and results |
| D3 | Controls. (a) An agent with the same kicks, or the same turns, but with a random sign or direction (zero information). (b) An agent that reads but does not act. How much of the viability needs no information? | Pre-registered rules and results |

**Result for the readers.** Open code that reproduces their figures in hours, an estimator of the threshold with an
error bar, and the fraction of viability that needs no information.

## Niche E. Semantic information of E. coli chemotaxis
**Why it matters to them.** MattinglyKaminoMachtaEmonet21 measure a linear Gaussian model of the chemotaxis pathway
(signal statistics, kinase response, kinase noise) and find that cells climb at 66 % of the limit set by their
information rate. Their supplementary text splits the information into a part about the current signal and the rest.
Our exact formulas (niche B) apply to this model. So we can compute the semantic information of KolchinskyWolpert18 for
a real cell, with measured parameters.

| Step | Work | Done when |
|---|---|---|
| E0 | Read the full text and the supplementary text. Write the model and Table S1 in our notation | A note in `docs/E.md` |
| E1 | Reproduce their information rate β = 0.22 bits/s/mm^-2 from Table S1 | Our value is inside their error bar |
| E2 | Define the viability (the drift speed) and the intervention (a Gaussian garbling of the signal, with the pathway fixed). Compute the semantic information rate and the efficiency S/I | Pre-registered rules and results |
| E3 | Compare S/I with their split of the information and with their efficiency 66 % | A statement: equal, a bound, or different. With the numbers |

**Gate.** If the semantic information of E2 equals their "current signal" information by a short proof, report E as a
bridge between the two languages. This is still useful, but it is not a new number.

## Niche F. A map of the free choices of CLD
**Why it matters to them.** SowinskiEtAl25 leave four choices open: the scrambled bit, Ω_scr, the time and the
functional. They say that other functionals need a test. Our niche C tested one choice and found that CLD rates rocks
above oscillators (AUC 0.711).

| Step | Work | Done when |
|---|---|---|
| F1 | On the 840 units of C2: five functionals (JS, both KL, Hellinger, total variation), three histogram sizes, two numbers of walkers, four time choices. Same rules as K1 | Pre-registered rules and results: one AUC with a CI for each choice |
| F2 | Report the choices that pass the control, if any | A table for the readers |

**Gate.** If no choice passes, the failure of C2 is not an artefact of our choice. If some choices pass, we give them a
list of choices to use.

## Niche G. Transfer entropy and the sensor information of Tanaka
**Why it matters to them.** Our paper proves TE ≤ DT for the first step only (F3) and tests it at τ = 4. A check on
2026-11-27, before the rules, found systems where TE > DT at τ = 64 (see `docs/G.md`). So the conjecture is false in
general. The question now is where it holds, and whether S_TE ≤ D_T* still holds.

| Step | Work | Done when |
|---|---|---|
| G1 | Check the counterexample with an independent method (Monte Carlo) | The two methods agree |
| G2 | A map: in which systems and at which τ does TE ≤ DT fail? 20 000 random systems, τ up to 64 | Pre-registered rules and results |
| G3 | At long τ, does S_TE ≤ D_T* still hold? | Pre-registered rules and results |
| G4 | A correction note for the paper of B and C, and a proof of the cases where the bound holds, if we find one | Text in `paper_bc/` |

## Niche H. The energy cost of semantic information
**Why it matters to them.** Kolchinsky and Wolpert relate semantic information to thermodynamics in words.
Nagayama, Kolchinsky and Ito split the entropy production of linear systems. Information thermodynamics bounds the
information flow by the entropy production of the agent (Horowitz and Esposito 2014). In linear systems all these
quantities are exact. So we can say how much of the entropy production pays for the information that the agent uses.

| Step | Work | Done when |
|---|---|---|
| H0 | Literature check: learning rate, information flow, sensory capacity, thermodynamic cost of semantic information | A note in `docs/H.md` |
| H1 | For the S3 homeostat and random linear agents: entropy production, information flow, stored and observed semantic information. Exact, no simulation | Pre-registered rules and results |
| H2 | A bound, or a counterexample, that links the semantic information to the entropy production of the agent | A statement with numbers |

## Niche I. A package of negative controls
**Why it matters to them.** Each new semantic score needs controls. Our controls (the homeostat without feedback, the
rocks, the static Gaussian systems with known answers) are in this repository, mixed with other code.

| Step | Work | Done when |
|---|---|---|
| I1 | A small package `semcontrols` with the controls, their known answers and a test function for any score | Tests pass. Install with pip from the repository |
| I2 | A short README with an example: CLD and the value of information on each control | The example runs in under 1 minute |

## Order and dependencies
1. **D, F and G3 on the Xeon machines** at the same time. One zip (`cluster/`) holds the code for all of them. Each
   job saves each finished task, so a stop loses only the running tasks.
2. **G1, G2 and E on this PC**, while the machines run.
3. **H** after E. **I** last, because it collects the controls of C, D and F.
4. **G4** after G2 and G3, before any email about the paper of B and C.

## Output and contact
| Niche | Output | Who to send it to |
|---|---|---|
| D | A short paper with the code (replication and controls) | Damian Sowinski, Adam Frank, Gourab Ghoshal |
| E | A letter on arXiv | Artemy Kolchinsky, Thierry Emonet, Benjamin Machta |
| F | A section of the paper of D, or an Artificial Life paper | Stuart Bartlett, Damian Sowinski |
| G | A correction in the paper of B and C, and a note | Takashi Tanaka, Artemy Kolchinsky |
| H | A section of the letter of E, or a separate note | Artemy Kolchinsky, Sosuke Ito |
| I | The package, cited in all the papers | All |

Send nothing before an expert checks the proofs.

## Hardware
- The Xeon machines: many cores, 1 to 2 days without stops. The zip of `cluster/` runs on Linux or Windows with
  Python 3.11 or later. It uses all cores, and it can split the work across machines.
- This PC: 4 cores. E, G1, H and I run here.
