"""Niche B, B1, post-hoc check (not part of the pass criterion, docs/B.md): remove the first-order bias of the
plug-in Gaussian mutual information, dx * dy / (2 n) with n = 5000 per batch, from the I checks of E20."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
d = json.load(open(ROOT / "results" / "e20_b1_monte_carlo.json"))
bias = 2 * 3 / (2 * 5000)
for r in d["rows"]:
    if r["quantity"] == "I":
        print(r["seed"], r["kind"], f"raw z {r['z']:+.2f}", f"corrected z {((r['mc'] - bias) - r['formula']) / r['se']:+.2f}")
