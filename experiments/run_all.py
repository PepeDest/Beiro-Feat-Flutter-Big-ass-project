"""Run every experiment in order.  --quick uses a small ensemble (~2 min); default is the full ensemble.
Run time of the full ensemble: about 30 min on the PC of README.md (E3 alone took 1631 s there).
(Superseded 2026-11-04: "default is the full ensemble (~12 min)".)
S0 reproduces the SHIPPED results, so E3 runs with the old exit check (--no-crn --no-bridge). Use --corrected for the
corrected method (the default of e3_phi_vs_viability.py since 2026-11-11, docs/RERUN.md)."""
import subprocess, sys, pathlib
here = pathlib.Path(__file__).parent
quick = "--quick" in sys.argv
e3 = ["--n_worlds", "6", "--n_traj", "300", "--t_max", "100"] if quick else ["--n_worlds", "30", "--n_traj", "600", "--t_max", "200"]
e3 += [] if "--corrected" in sys.argv else ["--no-crn", "--no-bridge"]
for cmd in (["e0_audit_legacy.py"], ["e1_estimators.py"], ["e2_gib_slowmodes.py"], ["e3_phi_vs_viability.py"] + e3, ["e4_merging.py"]):
    print("\n=== running", " ".join(cmd), flush=True)
    subprocess.run([sys.executable, str(here / cmd[0])] + cmd[1:], check=True, cwd=here)
