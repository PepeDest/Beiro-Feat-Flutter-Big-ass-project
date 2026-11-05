import os, subprocess, sys, pathlib
EXP = pathlib.Path(__file__).resolve().parents[1] / "experiments"


def _dt(module, env):
    code = f"import sys; sys.path.insert(0, {str(EXP)!r}); import {module}; print({module}.DT)"
    e = dict(os.environ); e.update(env)
    return float(subprocess.run([sys.executable, "-c", code], env=e, capture_output=True, text=True, check=True).stdout)


def test_dt_defaults_and_override():
    # Night item 8b: the step of S2/S2b and S3 can be set by environment variables; the defaults are unchanged.
    assert _dt("e6_fluxcut", {}) == 0.01 and _dt("e6b_rockmemory", {}) == 0.01 and _dt("e5_agency", {}) == 0.05
    assert _dt("e6_fluxcut", {"VLIFE_S2_DT": "0.005"}) == 0.005 and _dt("e5_agency", {"VLIFE_S3_DT": "0.025"}) == 0.025
