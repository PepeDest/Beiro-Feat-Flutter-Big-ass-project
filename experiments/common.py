import sys, pathlib, json
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
RES = ROOT / "results"; RES.mkdir(exist_ok=True)

def save_json(name, obj):
    def conv(o):
        import numpy as np
        if isinstance(o, (np.floating, np.integer)): return o.item()
        if isinstance(o, np.ndarray): return o.tolist()
        raise TypeError(type(o))
    (RES / name).write_text(json.dumps(obj, indent=2, default=conv))
