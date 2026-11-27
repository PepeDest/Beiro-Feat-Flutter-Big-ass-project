"""Use the source tree when semcontrols is not installed. At the repository root, the folder `semcontrols` is seen as
an empty namespace package, so we also check that the found package has a file."""
import importlib.util, pathlib, sys

spec = importlib.util.find_spec("semcontrols")
if spec is None or spec.origin is None:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
    sys.modules.pop("semcontrols", None)
