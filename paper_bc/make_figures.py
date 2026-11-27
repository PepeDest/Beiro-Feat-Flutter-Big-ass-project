"""Figures of paper_bc. Run from the repository root: .venv/Scripts/python paper_bc/make_figures.py
Data: results/e21_b2_semantic.json, e22_b3_observed.json, e25_c1_homeostat.json, e26_c2_rocks.json, e26_units.csv.
The script prints the counts it plots, so a reader can compare them with the text."""
import csv, json, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
RES, OUT = ROOT / "results", pathlib.Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8, "legend.fontsize": 7,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "pdf.fonttype": 42})
ROCK, OSC, D1, D2 = "#8e6c3a", "#2c6fbb", "#2c3e50", "#c0392b"


def save(fig, name):
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=200)
    plt.close(fig)


# ------------------------------------------------ Figure 1: stored (B2a) and observed (B3) semantic information
b2 = [r for r in json.load(open(RES / "e21_b2_semantic.json"))["b2a"]
      if abs(r["dV"]) >= 1e-3 and r.get("S_general") is not None]
b3 = [r for r in json.load(open(RES / "e22_b3_observed.json"))["rows"] if abs(r["dV"]) >= 1e-3]
print("Fig 1: B2a systems", len(b2), "| B3 systems", len(b3), "| B3 with D_T* attained", sum(r["DT_attained"] for r in b3))

fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.8))
ax = axs[0]
sg = np.array([r["S_general"] for r in b2]); sp = np.array([r["S_proj"] for r in b2]); ic = np.array([r["I_C"] for r in b2])
lo, hi = 1e-4, 2.0
ax.loglog([lo, hi], [lo, hi], color="0.6", lw=0.8)
ax.loglog(sg, ic, "^", ms=3.5, mfc="none", color="0.45", label=r"drive projection $I_C$")
ax.loglog(sg, sp, "o", ms=3.5, color=D1, label=r"best projection $S_{\rm proj}$")
ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
ax.set_xlabel(r"best Gaussian garbling $S_{\rm G}$ (nats)"); ax.set_ylabel("value with a projection (nats)")
ax.set_title(r"(a) stored, $d_x=2$, $d_y=3$ (%d systems)" % len(b2)); ax.legend(loc="upper left", frameon=False)

ax = axs[1]
att = [r for r in b3 if r["DT_attained"]]
for dx, col, lab in ((1, D1, "D1, $d_x=1$"), (2, D2, "D2, $d_x=2$")):
    s = [r for r in att if r["dx"] == dx]
    ax.loglog([r["S_te"] for r in s], [r["S_dt"] for r in s], "o", ms=3.5, color=col, label=lab)
xs = np.array([r["S_te"] for r in att] + [r["S_dt"] for r in att])
lo, hi = xs.min() / 2, xs.max() * 2
ax.loglog([lo, hi], [lo, hi], color="0.6", lw=0.8)
ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
ax.set_xlabel(r"observed semantic information $S_{\rm TE}$ (nats)")
ax.set_ylabel(r"smallest sensor information $D_{\rm T}^\ast$ (nats)")
ax.set_title(r"(b) observed, $\tau=4$ (%d systems with $D_{\rm T}^\ast$ attained)" % len(att))
ax.legend(loc="upper left", frameon=False)
save(fig, "fig_b")

# ------------------------------------------------ Figure 2: negative controls (C1, C2)
c1 = json.load(open(RES / "e25_c1_homeostat.json"))["organisms"]
I = {o["i"]: o for o in c1 if o["version"] == "intact"}; N = {o["i"]: o for o in c1 if o["version"] == "nofeedback"}
ids = sorted(I)
c2 = json.load(open(RES / "e26_c2_rocks.json"))
units = {(int(r["seed"]), int(r["i"])): r for r in csv.DictReader(open(RES / "e26_units.csv", encoding="utf-8"))}
cl = [(u, units[(u["seed"], u["i"])]) for u in c2["units"]]
print("Fig 2: C1 organisms", len(ids), "| C2 units", len(cl), "| rocks", sum(m["kind"] == "rock" for _, m in cl))

fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.5))
ax = axs[0]
x = np.array([I[i]["chi1"] for i in ids]); y = np.array([N[i]["chi1"] for i in ids])
m = max(x.max(), y.max()) * 1.05
ax.plot([0, m], [0, m], color="0.6", lw=0.8)
ax.plot(x, y, "o", ms=2, color=D1, alpha=0.5)
ax.set_xlim(0, m); ax.set_ylim(0, m)
ax.set_xlabel(r"CLD $\chi_1$, intact (bits)"); ax.set_ylabel(r"CLD $\chi_1$, no feedback (bits)")
ax.set_title("(a) homeostat, %d organisms" % len(ids))

ax = axs[1]
grid = np.linspace(0, 1, len(cl[0][0]["curve"]))
for kind, col in (("rock", ROCK), ("oscillator", OSC)):
    for seed in sorted({u["seed"] for u, _ in cl}):
        cur = np.array([u["curve"] for u, meta in cl if meta["kind"] == kind and u["seed"] == seed])
        ax.plot(grid, np.median(cur, axis=0), color=col, lw=0.8, alpha=0.7,
                label=(kind + "s (median of a draw)") if seed == 2026 else None)
ax.set_yscale("symlog", linthresh=1e-3)
ax.set_xlabel(r"time $t/\tau^\ast$"); ax.set_ylabel(r"CLD $\chi(t)$ (bits)")
ax.set_title("(b) units, 7 draws"); ax.legend(loc="lower left", frameon=False)

ax = axs[2]
for kind, col in (("oscillator", OSC), ("rock", ROCK)):
    s = [(float(meta["V_on"]), u["chi3"]) for u, meta in cl if meta["kind"] == kind]
    ax.semilogx([a for a, _ in s], [b for _, b in s], "o", ms=2, color=col, alpha=0.6, label=kind + "s")
ax.set_xlabel(r"life $V$"); ax.set_ylabel(r"$\chi_3(0,\tau^\ast)$ (bits)")
ax.set_title("(c) units, 840 in 7 draws"); ax.legend(loc="upper left", frameon=False)
save(fig, "fig_c")
print("written:", sorted(p.name for p in OUT.iterdir()))
