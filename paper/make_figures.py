"""Figures of the paper. Run from the repository root: .venv/Scripts/python paper/make_figures.py
The numbers are copied from the reports named next to each block (all on the corrected code)."""
import pathlib, shutil
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = pathlib.Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8, "legend.fontsize": 7,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "pdf.fonttype": 42})

# ---------------------------------------------------------------- Figure 1: S1 robustness
# Sources: results/c5_summary.md, results/s1b_table_v2.md (mean within-world Spearman rho, 95 % cluster-bootstrap CI)
settings = ["base", r"$\tau$ 0.5", r"$\tau$ 2", r"$p_{\rm out}$ .01", r"$p_{\rm out}$ .2", "N 5", "N 7", "D r 2", "D r 3"]
phi_orig = [(-0.01, -0.12, 0.10), (0.23, 0.12, 0.33), (-0.16, -0.26, -0.07), (0.10, -0.00, 0.21), (-0.19, -0.30, -0.10),
            (-0.01, -0.11, 0.09), (-0.04, -0.15, 0.08), (0.11, 0.02, 0.19), (0.24, 0.16, 0.32)]
p_plus_c = [(0.29, 0.21, 0.37), (0.25, 0.16, 0.34), (0.32, 0.25, 0.40), (0.18, 0.10, 0.26), (0.45, 0.38, 0.52),
            (0.28, 0.21, 0.36), (0.29, 0.20, 0.38), (0.38, 0.33, 0.43), (0.41, 0.38, 0.45)]
phi_tc = [(0.34, 0.27, 0.42), (0.27, 0.18, 0.35), (0.47, 0.42, 0.52), (0.23, 0.16, 0.31), (0.50, 0.44, 0.57),
          (0.34, 0.28, 0.41), (0.34, 0.26, 0.42), (0.43, 0.39, 0.47), (0.46, 0.43, 0.50)]
c_eq = [(0.55, 0.49, 0.61), (0.69, 0.65, 0.73), (0.48, 0.42, 0.55), (0.54, 0.48, 0.60), (0.53, 0.47, 0.59),
        (0.59, 0.52, 0.65), (0.57, 0.53, 0.61), (0.63, 0.58, 0.68), (0.74, 0.69, 0.77)]
phi_tc_eq = [(0.57, 0.52, 0.62), (0.64, 0.59, 0.68), (0.49, 0.44, 0.54), (0.57, 0.51, 0.63), (0.58, 0.53, 0.63),
             (0.57, 0.49, 0.64), (0.63, 0.59, 0.67), (0.69, 0.65, 0.73), (0.73, 0.69, 0.77)]
mkh_eq = [-0.74, -0.74, -0.74, -0.74, -0.74, -0.77, -0.77, -0.28, -0.04]


def series(ax, data, dx, label, marker, color):
    x = np.arange(len(data)) + dx
    m = np.array([d[0] for d in data]); lo = np.array([d[1] for d in data]); hi = np.array([d[2] for d in data])
    ax.errorbar(x, m, yerr=[m - lo, hi - m], fmt=marker, ms=3.5, lw=0.9, capsize=1.5, color=color, label=label)


fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.5), sharey=False)
ax = axs[0]
series(ax, phi_orig, -0.2, r"$\Phi_{\rm orig}$", "o", "#c0392b")
series(ax, p_plus_c, 0.0, r"$P+C$", "s", "#7f8c8d")
series(ax, phi_tc, 0.2, r"$\Phi_{\rm TC}$", "D", "#2c3e50")
ax.axhline(0, color="k", lw=0.5); ax.set_title("(a) all structures")
ax = axs[1]
series(ax, c_eq, -0.15, r"$C$", "o", "#2980b9")
series(ax, phi_tc_eq, 0.15, r"$\Phi_{\rm TC}$", "D", "#2c3e50")
ax.plot(np.arange(9), mkh_eq, "v", ms=3.5, color="#8e44ad", label=r"$-K_H$")
ax.axhline(0, color="k", lw=0.5); ax.set_title("(b) structures of equal size")
for ax in axs:
    ax.set_xticks(range(9)); ax.set_xticklabels(settings, rotation=45, ha="right")
    ax.set_ylabel(r"mean within-world $\rho(\cdot,\log V)$")
axs[0].legend(frameon=False, loc="lower left", ncol=3)
axs[1].legend(frameon=False, loc="center left", bbox_to_anchor=(0.0, 0.32), ncol=3)
axs[0].set_ylim(-0.45, 0.75); axs[1].set_ylim(-0.95, 0.95)
fig.tight_layout(); fig.savefig(OUT / "fig_s1.pdf"); plt.close(fig)

# ---------------------------------------------------------------- Figure 3: S6 error threshold
# Sources: results/e12_report.md (S6c), results/e12_report_hash2.md (S6f), results/e13_report.md (S6d),
# docs/S6.md post-hoc table (finite-time mean field)
mu = np.array([0, 0.0285, 0.057, 0.0855, 0.114, 0.1425, 0.171, 0.228, 0.342])
s6c = [(1.0, 1.0, 1.0), (0.893, 0.882, 0.906), (0.794, 0.777, 0.812), (0.689, 0.673, 0.705), (0.579, 0.552, 0.605),
       (0.508, 0.477, 0.538), (0.398, 0.365, 0.430), (0.273, 0.241, 0.303), (0.073, 0.059, 0.087)]
s6f = [(1.0, 1.0, 1.0), (0.899, 0.884, 0.914), (0.799, 0.766, 0.832), (0.678, 0.643, 0.712), (0.563, 0.517, 0.610),
       (0.508, 0.482, 0.536), (0.400, 0.379, 0.419), (0.276, 0.231, 0.313), (0.060, 0.041, 0.083)]
mu_d = np.array([0.057, 0.114, 0.171, 0.228])
s6d = [(0.793, 0.764, 0.816), (0.516, 0.478, 0.555), (0.339, 0.303, 0.376), (0.156, 0.120, 0.193)]
mu_mf = np.array([0, 0.029, 0.057, 0.114, 0.171, 0.228, 0.342]); mf = [1.0, 0.76, 0.60, 0.27, 0.09, 0.03, 0.00]

fig, ax = plt.subplots(figsize=(3.4, 2.5))


def ci(ax, x, d, label, marker, color, dx=0.0):
    m = np.array([v[0] for v in d]); lo = np.array([v[1] for v in d]); hi = np.array([v[2] for v in d])
    ax.errorbar(np.asarray(x) + dx, m, yerr=[m - lo, hi - m], fmt=marker, ms=3.5, lw=0.9, capsize=1.5, color=color, label=label)


ci(ax, mu, s6c, r"300$\times$300, old noise (S6c)", "o", "#2c3e50", -0.002)
ci(ax, mu, s6f, r"300$\times$300, new noise (S6f)", "s", "#2980b9", 0.002)
ci(ax, mu_d, s6d, r"600$\times$600, 2$\times$ generations (S6d)", "D", "#c0392b")
ax.plot(mu_mf, mf, "--", color="#7f8c8d", lw=1.0, label="finite-time mean field")
ax.axvline(0.114, color="k", lw=0.6, ls=":"); ax.text(0.117, 0.93, r"$\mu_c$", fontsize=7)
ax.axhline(0.1, color="k", lw=0.4, ls="-", alpha=0.4)
ax.set_xlabel(r"mutation rate $\mu$ (A$\to$B at division)"); ax.set_ylabel("final fraction of type A")
ax.set_ylim(-0.03, 1.05); ax.legend(frameon=False, fontsize=6, loc="upper right")
fig.tight_layout(); fig.savefig(OUT / "fig_s6.pdf"); plt.close(fig)

# ---------------------------------------------------------------- Figure 2: S3 (existing figure of the corrected run)
shutil.copy(pathlib.Path(__file__).parents[1] / "results" / "e5_agency_v2.png", OUT / "fig_s3.png")
print("figures written to", OUT)
