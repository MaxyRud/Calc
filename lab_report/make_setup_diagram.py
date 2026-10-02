"""Labelled diagram of the experimental setup: annotated photo (top view) + side view with forces."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Polygon, Ellipse, Arc
from PIL import Image

plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 13,
                     "mathtext.fontset": "custom", "mathtext.rm": "Liberation Sans",
                     "mathtext.it": "Liberation Sans:italic"})
INK, CHEETAH, TEAL, RED, BLUE = "#1f2937", "#d97706", "#0f766e", "#b91c1c", "#1d4ed8"

img = np.asarray(Image.open("setup_photo.jpg"))
H, W = img.shape[:2]

fig = plt.figure(figsize=(20, 11.6), dpi=150)
fig.patch.set_facecolor("white")

# ---------------------------------------------------------------- (a) top view
ax = fig.add_axes([0.0, 0.01, 0.56, 0.95])
ax.imshow(img, extent=(0, W, H, 0))
ax.set_xlim(-760, W + 760); ax.set_ylim(H + 40, -60); ax.axis("off")
ax.text(-740, -20, "(a) Top view, from the phone camera", fontsize=19, fontweight="bold", color=INK, va="bottom")

box = dict(boxstyle="round,pad=0.35", fc="white", ec="#9ca3af", lw=1)
def label(text, target, pos, ha="left"):
    ax.annotate(text, xy=target, xytext=pos, fontsize=13.5, color=INK, ha=ha, va="center", bbox=box,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4, shrinkA=2, shrinkB=2))

label("Metre rule (1 m) along the table:\nsets the scale in Tracker", (150, 620), (-740, 620))
label("Hover puck: its fan makes an\nair cushion, so almost no friction", (352, 1195), (-740, 1040))
label("Puck launched by hand from\nthe bottom-left corner", (300, 1390), (-740, 1450))
label("Glass air table, tilted 3.5°\n(this end is higher)", (900, 300), (W + 60, 250))
label("Lower end of the table", (1060, 1600), (W + 60, 1580))
label("Reflections of the ceiling lights\n(can make tracking harder)", (440, 560), (W + 60, 760))
label("Laptop: videos analysed\nin Tracker", (960, 70), (W + 60, 40))
label("Clamp stand holding the phone\n(camera looks straight down)", (700, 1760), (W + 60, 1900))

# axes used in Tracker
ox, oy = 352, 1195
for dx, dy, name, off in [(260, 0, "x (across)", (8, 28)), (0, -260, "y (up the\nslope)", (-150, -55))]:
    ax.add_patch(FancyArrowPatch((ox, oy), (ox + dx, oy + dy), arrowstyle="-|>", mutation_scale=22, color="#facc15", lw=3))
    ax.text(ox + dx + off[0], oy + dy + off[1], name, color="#facc15", fontsize=14, fontweight="bold",
            ha="left", va="center")
# sketch of the puck's path
t = np.linspace(0, 1, 200)
px, py = ox + 700 * t, 3273 * t**2 - 3038 * t + oy
ax.plot(px, py, ls=(0, (6, 5)), color="#22d3ee", lw=2.6)
ax.annotate("", xy=(px[-1], py[-1]), xytext=(px[-8], py[-8]),
            arrowprops=dict(arrowstyle="-|>", color="#22d3ee", lw=2.6, mutation_scale=22))
ax.text(745, 1320, "path of the puck\n(curved, like a projectile)", color="#22d3ee", fontsize=13,
        fontweight="bold", ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="black", ec="none", alpha=0.6))

# ---------------------------------------------------------------- (b) side view
bx = fig.add_axes([0.575, 0.40, 0.42, 0.57])
bx.set_xlim(-1.2, 13.2); bx.set_ylim(-0.9, 9.3); bx.set_aspect("equal"); bx.axis("off")
bx.text(-1.1, 9.2, "(b) Side view with the forces on the puck", fontsize=19, fontweight="bold", color=INK, va="top")
th = np.radians(15)                       # drawn steeper than 3.5° so it can be seen
u = np.array([np.cos(th), np.sin(th)])    # up the slope
n = np.array([-np.sin(th), np.cos(th)])   # out of the table
p0 = np.array([0.3, 0.9]); L = 10.3
p1 = p0 + L * u
bx.plot([-1.0, 12.8], [0, 0], color="#6b7280", lw=2)                          # bench
bx.add_patch(Polygon([p0, p1, p1 - 0.28 * n, p0 - 0.28 * n], closed=True, fc="#111827", ec="#111827"))  # glass table
bx.add_patch(Rectangle((p0[0] - 0.05, 0), 0.35, p0[1] - 0.25, fc="#9ca3af", ec="#6b7280"))   # fixed foot
jx, jtop = p1[0] - 0.95, (p1 - 0.28 * n)[1]
bx.add_patch(Rectangle((jx, 0), 1.0, jtop - 0.25, fc="#e5e7eb", ec="#6b7280", lw=1.5))      # lab jack
bx.plot([jx, jx + 1.0], [0, jtop - 0.25], color="#6b7280", lw=1.2); bx.plot([jx, jx + 1.0], [jtop - 0.25, 0], color="#6b7280", lw=1.2)
bx.text(jx + 0.5, -0.5, "lab jacks", ha="center", fontsize=12.5, color=INK)
lv = p0 + 8.0 * u
bx.add_patch(Polygon([lv, lv + 1.1 * u, lv + 1.1 * u + 0.3 * n, lv + 0.3 * n], closed=True, fc="#fde047", ec="#a16207"))
bx.annotate("digital level\n(measures θ)", xy=lv + 0.55 * u + 0.3 * n, xytext=(10.4, 5.7), fontsize=12.5, ha="center",
            arrowprops=dict(arrowstyle="-", color="#6b7280", lw=1))
# angle at the low end
bx.add_patch(Arc(p0, 3.4, 3.4, theta1=0, theta2=15, color=INK, lw=1.6))
bx.plot([p0[0], p0[0] + 2.4], [p0[1], p0[1]], color=INK, lw=1, ls="--")
bx.text(p0[0] + 1.85, p0[1] + 0.08, "θ", fontsize=16, color=INK, va="bottom", fontweight="bold")
bx.text(-1.0, 7.7, "θ = 3.5° in our experiment\n(drawn steeper here so\nit can be seen)", fontsize=11.5, color="#6b7280",
        style="italic", va="top")
# phone on clamp stand
bx.plot([12.4, 12.4], [0, 8.1], color="#6b7280", lw=4)
bx.plot([12.4, 6.6], [8.1, 8.1], color="#6b7280", lw=3)
bx.add_patch(Rectangle((5.5, 7.95), 1.4, 0.32, fc="#374151", ec="#111827"))
bx.text(6.2, 8.45, "phone camera on clamp stand", ha="center", fontsize=12.5, color=INK)
for q in (p0 + 0.6 * u, p0 + 9.9 * u):
    bx.plot([6.2, q[0]], [7.95, q[1]], color="#9ca3af", lw=1, ls=":")
# puck and forces (true proportions for the drawn angle)
c = p0 + 6.2 * u + 0.2 * n
bx.add_patch(Polygon([c - 0.27 * u - 0.1 * n, c + 0.27 * u - 0.1 * n, c + 0.27 * u + 0.14 * n, c - 0.27 * u + 0.14 * n],
                     closed=True, fc="#2563eb", ec="#ea580c", lw=2, zorder=3))
def arrow(start, vec, color, lw=2.8, ls="-"):
    bx.add_patch(FancyArrowPatch(start, start + vec, arrowstyle="-|>", mutation_scale=22, color=color, lw=lw,
                                 linestyle=ls, zorder=4))
g = 2.7
arrow(c, np.array([0, -g]), RED)                                     # weight
bx.text(c[0] + 0.2, c[1] - 0.55 * g, "mg\n(weight)", color=RED, fontsize=14, fontweight="bold", ha="left", va="center")
arrow(c, -g * np.sin(th) * u, "#ea580c")                            # component down the slope
bx.text(*(c - g * np.sin(th) * u + np.array([-0.25, 0.3])), "mg sin θ", color="#ea580c", fontsize=14,
        fontweight="bold", ha="right", va="bottom")
arrow(c, g * np.cos(th) * n, TEAL)                                   # normal force
bx.text(*(c + g * np.cos(th) * n + np.array([0, 0.2])), "N = mg cos θ\n(air cushion)", color=TEAL, fontsize=14,
        fontweight="bold", ha="center", va="bottom")
a0 = c + 1.45 * n + 0.9 * u
arrow(a0, -1.8 * u, BLUE, lw=2.4)                                    # acceleration
bx.text(*(a0 - 1.8 * u + np.array([-0.15, 0.05])), "a = g sin θ", color=BLUE, fontsize=14, fontweight="bold",
        ha="right", va="center")
bx.annotate("hover puck", xy=c + 0.27 * u, xytext=(8.4, 1.3), fontsize=12.5,
            arrowprops=dict(arrowstyle="-", color="#6b7280", lw=1))

# ---------------------------------------------------------------- notes
tx = fig.add_axes([0.585, 0.02, 0.41, 0.36]); tx.axis("off")
notes = [
    ("How it works", True),
    ("The phone films the puck from directly above. Tracker turns the video into the puck's", False),
    ("position (x, y) in every frame, using the metre rule for the scale.", False),
    ("", False),
    ("Forces on the puck", True),
    ("• Weight mg acts straight down. It splits into mg sin θ down the slope and", False),
    ("  mg cos θ into the table.", False),
    ("• The air cushion pushes back with N = mg cos θ, so those two cancel and", False),
    ("  there is almost no friction.", False),
    ("• Only mg sin θ is left, so the puck accelerates down the slope with a = g sin θ,", False),
    ("  which gives g = a / sin θ.", False),
    ("• Nothing acts across the table, so the puck's x-velocity stays constant.", False),
]
y = 1.0
for text, head in notes:
    tx.text(0.0, y, text, fontsize=15 if head else 13.5, fontweight="bold" if head else "normal", color=INK, va="top",
            transform=tx.transAxes)
    y -= 0.085 if text else 0.045

fig.savefig("setup_diagram.png", dpi=150, facecolor="white")
print("saved")
