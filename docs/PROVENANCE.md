# Provenance table: every formula, definition and design choice

**Status codes**
- **E** — established: standard textbook / published result, implemented as published.
- **A** — adapted: an established idea applied to a new object; the adaptation is ours and is not guaranteed by the source.
- **H** — project hypothesis: comes from the original proposal; related literature noted; *no established support*.
- **N** — novel: to the authors' knowledge not present in the literature. "Novel" here means *we did not find or recall a source*;
  it does **not** mean a systematic literature search was performed. Treat every N as "needs a literature check".
- **X** — analogy / unproven extension: used heuristically; the cited theorem does not strictly apply.

| # | Item | Where | Status | Source / note |
|---|---|---|---|---|
| 1 | OU world dx = −Bx dt + √(2D) dW | gaussian.py, worlds.py | E | Gardiner04 ch.4; Risken89 ch.6 |
| 2 | Stationary covariance from Lyapunov eq. BS + SBᵀ = 2D | gaussian.stationary_cov | E | Gardiner04; solver BartelsStewart72 |
| 3 | Lagged covariance C(τ) = e^{−Bτ}S | gaussian.lagged_cov | E | Gardiner04 (regression theorem) |
| 4 | Gaussian entropy / MI / conditional MI via log-determinants | gaussian.py | E | CoverThomas06 ch.2, 8 |
| 5 | Entropy production σ = tr(MᵀD⁻¹MS), M = B − DS⁻¹ | gaussian.entropy_production | E (general form) / derivation specialised by us | Tome06, SpinneyFord12; derivation in THEORY §2 |
| 6 | Equilibrium counterpart B_eq = DS⁻¹ (same stationary law, detailed balance) | gaussian.equilibrium_counterpart | E (construction) | Hwang…93/05, Lelièvre…13 compare reversible/irreversible diffusions with the same invariant measure |
| 7 | Ensemble: B = symmetric-PD + antisymmetric; three families | worlds.py | N (design) | Decomposition standard (Lelièvre…13); family choices are ours and reintroduce arbitrariness (see LIMITATIONS) |
| 8 | Environment := complement Ω∖A (not an exogenous process) | functional.py | N (design) | Fixes an inconsistency in the original proposal; resembles blanket/partition language in Friston13, Krakauer20 but is not their definition |
| 9 | C(A) = I(A_t; A_{t+τ}) | functional.py | H | Original proposal. Related: past–future MI / excess entropy (BialekNemenmanTishby01). Close to the autonomy measure of Krakauer20 and to the lagged-MI persistence of TzeliosBishop21 (S0 search) |
| 10 | P(A) = I(A_t; X_{t+τ}) | functional.py | H | Original proposal; predictive information BialekNemenmanTishby01 |
| 11 | K(A) = h(A_t) differential entropy as complexity cost | functional.py | H | Original proposal; scale-dependent (LIMITATIONS §3) |
| 12 | IAX − P as "non-predictive information" | functional.py | X | Still12 bound holds for a system driven by an *exogenous* signal; A and X here are mutually coupled |
| 13 | leak = I(A_{t+τ}; X_t \| A_t) (closure) | functional.structure_features | A | One-step transfer entropy (Schreiber00); closure concept BertschingerOlbrichAyJost08; this scalar is our simplification |
| 14 | Φ_orig = P + βC − λK | functional.phi_orig | H | Original proposal. Structurally a predictive information-bottleneck-type trade-off (Tishby99, BialekNemenmanTishby01) |
| 15 | Viability set = Mahalanobis ball with stationary occupancy 1 − p_out | viability.py | N | Viability-kernel language Aubin91; this operational choice is ours; sensitivity to p_out must be reported |
| 16 | V = mean first-passage time out of the viability set | viability.py | E (MFPT theory) + N (use as viability to compare with Φ) | PontryaginAndronovVitt33, Gardiner04 ch.5, Redner01; the test "does Φ predict V?" is the project's contribution. KolchinskyWolpert18 also relate information to a viability function, but they use a different viability (an entropy-based one) and intervention, not exit times |
| 17 | Exact OU propagator for simulation | viability.simulate_exits | E | Gillespie96 (1-D); multivariate from Gardiner04 |
| 18 | Discrete-monitoring bias ≈ boundary shift 0.5826σ√dt | tests/test_viability.py | E | BroadieGlassermanKou97; Mannella99 |
| 19 | Censoring-aware estimator V = exposure/events | viability.mfpt_from | E | Exponential-survival MLE, CoxOakes84 (approximation: exit times from a stationary start are not exactly exponential; ColletMartinezSanMartin13) |
| 20 | Flux ratio R = V_driven / V_eq | e3 | A (was N; S0 search) | Motivated by Hwang…05, Lelièvre…13, FreidlinWentzell98. Exit times under a non-reversible drift with the same invariant measure are studied in LePeutrecMichelNectoux23 (exit can be faster or slower). The ratio over random *structures* of an ensemble is ours |
| 21 | Merged-entity survival = both parts inside own sets; synergy S = V_union(1/V_A + 1/V_B) | viability.mfpt_union, e4 | N | Definitions ours |
| 22 | h(A∪B) = h(A)+h(B) − I(A;B) ⇒ ΔΦ = (ΔP+βΔC) + λI(A;B) | e4 | E (identity) + N (use) | CoverThomas06; merger/split criterion as superadditivity of Φ is ours |
| 23 | Within-world analysis, regression of log V on features | e3 | E (method) + N (hypothesis) | Standard OLS; "coefficients are positive/positive/negative and universal" is a pre-registered hypothesis of this project |
| 24 | Cluster bootstrap over worlds | stats.py | E | Efron79, CameronMiller15 |
| 25 | Spearman rank correlation | stats.py | E | Spearman1904 |
| 26 | KSG mutual-information estimator | estimators.ksg_mi | E | Kraskov04 (algorithm 1) |
| 27 | Plug-in MI bias | estimators.binned_mi, E0, E1 | E | Treves95, Paninski03 |
| 28 | N_eff = n(1−ρ)/(1+ρ) | estimators.py, E0 | E (AR(1) mean) | BayleyHammersley46 |
| 29 | Gaussian IB: optimal linear map, critical β_i = 1/(1−λ_i), α_i formula | gib.py | E | Chechik05 Thm 3.1 (verified numerically here against direct optimisation: tests/test_gib.py) |
| 30 | TICA / VAMP slow modes | gib.tica_modes | E | MolgedeyS94, PerezHernandez13, WuNoe20 |
| 31 | GIB ≡ TICA subspaces when C(τ) symmetric | THEORY §6, tests/test_gib.py | A (short proof by us; result is a classical CCA fact) | Hotelling36; proof in THEORY |
| 32 | GIB vs TICA subspace gap as a measure of irreversibility | e2 | N (S0 search: no prior found) | Observation made here; not claimed as a theorem. Related: time-lagged bottlenecks (FedericiForreTomiokaVeeling23) and VAMP for non-reversible data (WuNoe20) |
| 33 | Price equation decomposition | price.py | E | Price70, Price72, Frank95 |
| 34 | Cov(w/w̄, Φ) over structures of one world as a 'selection differential' | e3 | N / X | Structures do not reproduce; descriptive statistic only |
| 35 | Telos as T1 (selection effect), T2 (variational postulate), T3 (arrow of organisation) | THEORY §1 | N (framing) | T1 relates to teleonomy: Pittendrigh58, Mayr74 |
| 36 | "Equilibrium, linear-regime and replicator dynamics each have a Lyapunov-type functional; far-from-equilibrium has none in general" | THEORY §1 | E (statement of known facts) | Free energy (textbook), Prigogine55, Fisher30 / Price72 / HofbauerSigmund98 |
| 37 | Growth-rate viability via Euler–Lotka / Leslie matrix | viability.GrowthRateViability (stub) | E (theory) / not implemented | Lotka1907, Leslie45, Charlesworth94, Caswell01 |
| 38 | Heredity requirements, error threshold, constructor logic | ROADMAP.md | E (background) | Eigen71, vonNeumann66, SzathmaryMaynardSmith95 |
| 39 | Good-regulator caveat: successful regulation can *lower* I(output; disturbance) | THEORY §5 | E (background) | ConantAshby70, TouchetteLloyd00 |
| 40 | Gray–Scott and active droplets as physical division models | ROADMAP.md | E (background) | Pearson93, Zwicker17 |

## S0 novelty search log (2026-10-21)
Method: four web searches plus metadata checks through the arXiv API. This is a limited search, not a systematic review.

| Query topic | Items | Result |
|---|---|---|
| MFPT out of a viability set compared with predictive or mutual information of a subsystem | 15, 16 | No direct prior found. KolchinskyWolpert18 is the closest (information against a viability function). |
| Mean exit time under a non-reversible drift with the same invariant measure | 20 | Prior found: LePeutrecMichelNectoux23. Row 20 changed from N to A. |
| Information bottleneck against TICA as a measure of irreversibility | 32 | No direct prior found. Related: FedericiForreTomiokaVeeling23, WuNoe20. Row 32 stays N. |
| Information closure, autonomy and persistence as predictors of survival | 9, 13 | Related: Krakauer20 (autonomy), TzeliosBishop21 (lagged-MI persistence). No test of "persistence predicts exit time" found. |

Not searched: rows 7, 8, 21, 22, 34 and 35. These rows are design choices or definitions of this project. Keep them as N until a search is done.

| # | Item | Where | Status | Source / note |
|---|---|---|---|---|
| 41 | Total correlation TC = −½ log det R_A as a complexity term free of units | gaussian.total_correlation, S1b | E (quantity) + N (use in Φ) | Watanabe60; Gaussian form CoverThomas06. Using it in place of K_H in Φ is ours (docs/S1b_unitfree.md) |
| 42 | Linear homeostat (h → s → m → u → v) and its scrambled and no-feedback versions | agency.py, E5 | N (design) + A (scramble) | Scramble intervention from KolchinskyWolpert18. Good-regulator background ConantAshby70, TouchetteLloyd00. Model and fixed threshold on v are ours (docs/S3.md) |
| 43 | Viability as exit of one variable from a fixed physical limit \|v\| < c | agency.simulate_exit_threshold | E (MFPT) + N (use) | Gardiner04, Redner01. Differs from rows 15–16 on purpose (docs/S3.md) |
| 44 | Inertial units with active Rayleigh friction (drive on) and constant friction (drive off) | nonlinear.py, E6 | E (model) + N (use as flux cut) | SchweitzerEbelingTilch98, Romanczuk12. Off dynamics is Kramers40 equilibrium |
| 45 | Bendixson argument: an overdamped 2D drift −∇U + divergence-free drive has no cycle if U is convex | docs/S2.md | E (Bendixson criterion) + A (applied here) | standard ODE textbook result |
| 46 | Viability set = highest-density region (95 %) of the unit's on-stationary law, smoothed histogram | nonlinear.HDR | N | Generalises the Mahalanobis ball of row 15 (equal for a Gaussian law) |
| 47 | σ = drive power / T for active Rayleigh units (heat into the bath) | e7, docs/S2c.md | E (energy balance) + A | SpinneyFord12 style stochastic energetics. Checked by a unit test |
| 48 | Structure-level entropy production σ_A = Σ_{i∈A} (M S Mᵀ)ᵢᵢ / Dᵢᵢ | gaussian.structure_entropy_production | N (decomposition) | Total form Tome06, SpinneyFord12. The split by coordinates is ours |
| 49 | Static blanket (precision zeros) against dynamic blanket (drift zeros from B̂ = −logm(C(Δ)S⁻¹)/Δ) | blankets.py, E8 | E (both ideas) + N (comparison design) | Pearl88, Friston13, AguileraMillidgeTschantzBuckley22; matrix-log drift estimate follows from Gardiner04 regression theorem |
| 50 | Closure score Cl = TC(I) − I(I; rest) | E8 | N | Related to closure ideas in BertschingerOlbrichAyJost08 and Krakauer20; this scalar is ours |
| 51 | Growth rate r from the survival curve via Euler–Lotka, birth rate b after maturation a_m, same for all structures | viability.GrowthRateViability | E (Euler–Lotka) + N (use) | Lotka1907, Charlesworth94. The common birth rule is our choice (docs/S4.md) |
| 52 | Random-swap offspring map for the Price transmission term | e9 | N | Price70, Frank95 for the identity. The map is ours |
| 53 | Gray–Scott spot replication as a test bed | grayscott.py, E10 | E (model) | Pearson93 |
| 54 | Neutral dye that stays in spots and is split at division (positive control for heredity) | grayscott.py | N | Our design (docs/S6.md) |
| 55 | Spot tracking by overlap, division = one spot to two | grayscott.Tracker | N (simple method) | Our implementation |
| 56 | Two competing dyes as a heritable binary type in Gray–Scott spots, with an effect on the kill rate | grayscott2.py, gs_opencl.py, E11 | N | Our design (docs/S6.md, S6b). Price identity per generation: Price70 |
| 57 | GPU (OpenCL, float64) grid update with a counter-based hash for the noise | gs_opencl.py | N (numerics) | Checked against the numba and numpy versions by tests |
| 58 | One-way mutation at division in Gray–Scott spots; error threshold μ_c = 1 − 2^(T_A/T_B − 1) for regular cycles | gs_opencl.run(mu), E12 | E (single-peak error threshold idea, Eigen71) + N (this growth-rate form and its use) | The formula follows from comparing the lineage growth rates ln(2(1 − μ))/T_A and ln 2/T_B |
