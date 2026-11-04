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
   0.5826σ√dt [BroadieGlassermanKou97]); the bias is systematic across structures, but affects absolute values.
7. **Censoring / exponential approximation.** Structures with < 5 observed exits are dropped. V = exposure/events assumes
   roughly constant hazard [CoxOakes84]; from a stationary start it is only approximate [ColletMartinezSanMartin13].
8. **Merging definition.** "Alive iff both parts inside their own sets" makes S sensitive to *temporal clustering of
   exits*, which correlates with statistical dependence by construction. H4 therefore compares against static I(A;B).
9. **Selection term only.** No heredity, so T3's transmission term, and replication itself, are untested.
10. **References not machine-verified** (see REFERENCES.md). Novelty claims mean "no source recalled", not "searched".
11. **Single run per world for MFPT** with n_traj Monte-Carlo trajectories: noise sd(log V) ≈ 0.03–0.04 (measured), versus
    signal sd across structures ≈ 0.07–0.12; coefficients are attenuated slightly by this noise.
