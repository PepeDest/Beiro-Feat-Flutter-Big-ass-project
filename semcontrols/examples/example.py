"""The README example: the value of information of Kolchinsky and Wolpert (Delta V_KW) and CLD on each control.
Small sizes, so that it runs in under 1 minute."""
import time
import semcontrols as sc
from semcontrols import controls, scores

t0 = time.time()

print("1. Delta V_KW on the linear controls (100 organisms, 50 readers)")
print(sc.report(sc.check(linear_score=scores.kw_value, homeostat_ids=range(100), n_readers=50)), "\n")

print("2. CLD chi_1 on the linear controls (Monte Carlo, 5000 samples, zero means below 0.01)")
cld = lambda s: scores.cld_linear(s, [1.0], n=5_000, seed=0)[1][0]
print(sc.report(sc.check(linear_score=cld, homeostat_ids=range(40), n_readers=40, tol=0.01)), "\n")

print("3. CLD chi_3 on the 840 units: the stored values of the full run (20 000 walkers per group)")
stored = {(u.seed, u.i): u.reference["cld_chi3"] for u in controls.units()}
print(sc.report(sc.check(unit_values=stored)), "\n")

print("4. The flux ratio log(V_on / V_off) on the 840 units, for comparison")
print(sc.report(sc.check(unit_score=scores.flux_ratio)), "\n")

print("5. A small live CLD run on one rock and one oscillator (2000 walkers per group)")
us = controls.units()
for u in (next(u for u in us if u.kind == "rock"), next(u for u in us if u.kind == "oscillator")):
    out = scores.cld_unit(u, n=2_000, n_times=11)
    print(f"{u.kind} (seed {u.seed}, unit {u.i}): chi_3 = {out['chi3']:.4f}, stored value {u.reference['cld_chi3']:.4f}")

print(f"\nTime: {time.time() - t0:.1f} s")
