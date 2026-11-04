# Limitations and known weak points (read before trusting any number)

1. **Linear-Gaussian only.** All information terms are exact, but linear OU worlds cannot hold bistable memory, limit
   cycles, or anything "rock-like". The hard-disk/spin-glass counterexample to C (persistence ≠ organisation) is therefore
   *not tested* here; it needs the non-linear stage (ROADMAP).
2. **Passive world.** Structures never act on their environment, so predictive information has no feedback payoff.
   A null or negative P coefficient must not be read as a refutation of the thermodynamics of prediction [Still12,
   ParrondoHorowitzSagawa15]; it is evidence that prediction needs a use.
3. **Differential entropy K_H is scale-dependent.** Rescaling x shifts K_H by k·log(scale). Within-world comparisons at fixed
   units are fine; across-world comparison of K_H is not meaningful. We demean within worlds for this reason.
4. **Ensemble choice is arbitrary.** Rate range, flux scale, modular block sizes, N = 6, D = I are our choices. Results are
   evidence about *this* ensemble. Report sensitivity (τ, p_out, family) before generalising.
5. **Viability set is operational.** A Mahalanobis ball of fixed stationary occupancy defines "alive". MFPT from it is
   partly a statement about relaxation time and fluctuation geometry; correlation of V with C is expected in part by
   construction (slow structures live long). The flux ratio and the within-world design are the guards; they are not proofs.
6. **Discrete-monitoring bias.** Exit is checked every dt = 0.05; absolute V is biased upward (≈ boundary shift
   0.5826σ√dt [BroadieGlassermanKou97]). ~~The bias is systematic across structures, but affects absolute values.~~
   **Superseded (2026-11-04, docs/code_review.md item 1):** the bias is *not* the same for every structure. The shift
   relative to the radius of the set grows like √(θ·dt), with θ the relaxation rate of the structure. In 1-D
   (dt = 0.05, p_out = 0.05) log V is too high by +0.23 at θ = 0.3, +0.71 at θ = 3 and +1.21 at θ = 9. In four E3 worlds
   the bias ranges from +0.18 to +0.45 between structures of one world, the ranking by V against dt = 0.005 has
   Spearman ρ 0.85–0.98, and ρ(C, log V) moves by up to 0.14. This bias also affects S3 (same dt) and the D-test of S1
   (faster rates).
7. **Censoring / exponential approximation.** Structures with < 5 observed exits are dropped. V = exposure/events assumes
   roughly constant hazard [CoxOakes84]; from a stationary start it is only approximate [ColletMartinezSanMartin13].
8. **Merging definition.** "Alive iff both parts inside their own sets" makes S sensitive to *temporal clustering of
   exits*, which correlates with statistical dependence by construction. H4 therefore compares against static I(A;B).
9. **Selection term only.** No heredity, so T3's transmission term, and replication itself, are untested.
10. **References not machine-verified** (see REFERENCES.md). Novelty claims mean "no source recalled", not "searched".
11. **Single run per world for MFPT** with n_traj Monte-Carlo trajectories: noise sd(log V) ≈ 0.03–0.04 (measured), versus
    signal sd across structures ≈ 0.07–0.12; coefficients are attenuated slightly by this noise.
