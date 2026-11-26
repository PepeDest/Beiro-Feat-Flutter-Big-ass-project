"""Export the class and the life of each C2 unit to a small CSV, for the figures of paper_bc.
Source: results/e26_v_dataset.pkl (not in git, rebuilt by e26_c2_rocks.py). No new computation. Added 2026-11-26."""
import csv, pickle
from common import RES

draws = pickle.load(open(RES / "e26_v_dataset.pkl", "rb"))
with open(RES / "e26_units.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["seed", "i", "kind", "V_on", "V_off"])
    for seed, d in sorted(draws.items()):
        for r in d["rows"]:
            w.writerow([seed, r["i"], r["kind"], repr(float(r["V_on"])), repr(float(r["V_off"]))])
print("wrote", RES / "e26_units.csv")
