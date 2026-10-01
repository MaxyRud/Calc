import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
import numpy as np
from analysis import analyse, THETA_DEG

plt.rcParams.update({
    "font.family": "Liberation Sans",
    "mathtext.fontset": "custom",
    "mathtext.rm": "Liberation Sans",
    "mathtext.it": "Liberation Sans:italic",
    "font.size": 9,
    "axes.edgecolor": "#8a8986",
    "axes.linewidth": 0.8,
    "xtick.color": "#52514e",
    "ytick.color": "#52514e",
    "axes.labelcolor": "#0b0b0b",
})

COLORS = ["#2a78d6", "#eb6834", "#1baf7a"]   # validated categorical slots 1-3
MARKERS = ["o", "s", "^"]

r = analyse(verbose=False)
fig, ax = plt.subplots(figsize=(7.1, 3.55), dpi=300)
ax.axhline(0, color="#b5b4af", lw=0.8, zorder=0)
ax.grid(True, color="#e6e5e0", lw=0.6, zorder=0)

handles, labels = [], []
for (name, x), col, mk in zip(r.items(), COLORS, MARKERS):
    ax.errorbar(x["t"], x["v"], yerr=x["ev"], fmt=mk, ms=3.2, mfc=col, mec="white", mew=0.4,
                ecolor=col, elinewidth=0.6, capsize=1.4, capthick=0.6, alpha=0.9, zorder=2)
    tt = np.array([x["t"].min(), x["t"].max()])
    ax.plot(tt, x["m"] * tt + x["c"], color=col, lw=1.8, zorder=4,
            path_effects=[pe.Stroke(linewidth=3.4, foreground="white"), pe.Normal()])
    handles.append((Line2D([], [], marker=mk, ls="", ms=4, mfc=col, mec="white", mew=0.4),
                    Line2D([], [], color=col, lw=1.8)))
    labels.append(f"{name} (N = {x['n']}):  slope = ({x['m']:.3f} ± {x['dm']:.3f}) m s$^{{-2}}$".replace("-", "\u2212", 1))

from matplotlib.legend_handler import HandlerTuple
leg = ax.legend(handles, labels, handler_map={tuple: HandlerTuple(ndivide=None, pad=0.6)},
                loc="upper right", frameon=True, framealpha=0.95, edgecolor="#d9d8d3",
                fontsize=8, handlelength=3.2, borderpad=0.6, labelspacing=0.45,
                title="Data (points) and least-squares fit (line)", title_fontsize=8)
leg._legend_box.align = "left"

ax.set_xlabel("Time, $t$ (s)")
ax.set_ylabel("Velocity along slope, $v_y$ (m s$^{-1}$)")
ax.set_title(f"Up-slope velocity $v_y$ vs time for three projectile launches (table tilt θ = {THETA_DEG}°)",
             fontsize=10, fontweight="bold", color="#0b0b0b", pad=8)
ax.set_xlim(0, 2.75)
ax.set_ylim(-1.15, 1.3)
ax.set_xticks(np.arange(0, 2.76, 0.25))
ax.set_yticks(np.arange(-1.0, 1.21, 0.25))
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout(pad=0.3)
fig.savefig("figure1.png", dpi=300)
fig.savefig("figure1.pdf")
print("saved")
