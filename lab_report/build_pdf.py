import numpy as np
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
                                PageBreak, KeepTogether)
from analysis import analyse, linfit, g_from_slope, THETA_DEG, DTHETA_DEG, DY, G_REF

NAME = ""   # e.g. "Name Surname - Student ID"; left blank -> no author line

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for style, f in [("", "Regular"), ("-Bold", "Bold"), ("-Italic", "Italic"), ("-BoldItalic", "BoldItalic")]:
    pdfmetrics.registerFont(TTFont("LibSans" + style, FONT_DIR + f"LiberationSans-{f}.ttf"))
addMapping("LibSans", 0, 0, "LibSans"); addMapping("LibSans", 1, 0, "LibSans-Bold")
addMapping("LibSans", 0, 1, "LibSans-Italic"); addMapping("LibSans", 1, 1, "LibSans-BoldItalic")

INK, MUTED = HexColor("#0b0b0b"), HexColor("#52514e")
title = ParagraphStyle("t", fontName="LibSans-Bold", fontSize=12.5, leading=15, textColor=INK)
sub = ParagraphStyle("s", fontName="LibSans", fontSize=8.5, leading=11, textColor=MUTED, spaceAfter=4)
cap = ParagraphStyle("c", fontName="LibSans", fontSize=8.0, leading=10.4, textColor=MUTED,
                     alignment=TA_JUSTIFY, spaceBefore=2, spaceAfter=5)
body = ParagraphStyle("b", fontName="LibSans", fontSize=8.9, leading=11.9, textColor=INK,
                      alignment=TA_JUSTIFY, spaceAfter=4.2)

# ---- numbers (all computed, nothing typed by hand) ----
r = analyse(verbose=False)
R = list(r.values())
ms = np.array([x["m"] for x in R]); dms = np.array([x["dm"] for x in R])
a = ms.mean(); da_prop = np.sqrt(np.sum(dms**2)) / 3; da_sem = ms.std(ddof=1) / np.sqrt(3)
g, dg = g_from_slope(a, da_prop)
g_sem, dg_sem = g_from_slope(a, da_sem)
ang_rel = np.radians(DTHETA_DEG) / np.tan(np.radians(THETA_DEG))
inside_all = sum(np.sum(np.abs(x["v"] - (x["m"] * x["t"] + x["c"])) <= x["ev"]) for x in R) / sum(x["n"] for x in R)
apex = [x["c"] / -x["m"] for x in R]
# pairwise worst disagreement
pairs = [(abs(ms[i] - ms[j]) / np.hypot(dms[i], dms[j]), abs(ms[i] - ms[j]), i, j)
         for i in range(3) for j in range(i + 1, 3)]
worst = max(pairs)
# robustness: drop first 0.1 s (3 velocity points) of every recording
ms_cut = np.array([linfit(x["t"][3:], x["v"][3:])[0] for x in R])
g_cut, _ = g_from_slope(ms_cut.mean(), da_prop)
theta_needed = np.degrees(np.arcsin(abs(a) / G_REF))
ev = np.sqrt(2) * DY * 30

M = "−"
def f(v, n=3):  # signed number with a real minus sign
    return f"{v:.{n}f}".replace("-", M)
vy = "<i>v</i><sub>y</sub>"
ms2 = "m s<super>−2</super>"
ms1 = "m s<super>−1</super>"

NB = " "
def P(text, style):
    """Paragraph with non-breaking spaces so numbers never split from their units."""
    for a, b in [(" ± ", NB + "±" + NB), (" m s<super>", NB + "m" + NB + "s<super>"),
                 (" %", NB + "%"), (" mm", NB + "mm"), (" s)", NB + "s)"), (" s,", NB + "s,")]:
        text = text.replace(a, b)
    return Paragraph(text, style)

story = [
    Paragraph("Measuring <i>g</i> from a projectile on a tilted air table", title),
    Paragraph("PHYS 1552 · Experiment 1 · Data analysis exercise: Investigation II and Analysis III"
              + (f" · {NAME}" if NAME else ""), sub),
    RLImage("figure1.png", width=18.0 * cm, height=18.0 * cm * 1065 / 2130),
    P(
        f"<b>Figure 1.</b> Velocity component along the slope, {vy} (positive = up the slope), against time for "
        f"three hand-launched projectile recordings on the air table tilted at θ = ({THETA_DEG} ± {DTHETA_DEG})°. "
        f"Each point is <i>v</i><sub>y,av</sub> = Δ<i>y</i>/Δ<i>t</i> between consecutive video frames "
        f"(Δ<i>t</i> = 1/30 s), plotted at the interval mid-point time. Error bars: ±{ev:.3f} {ms1}, from a "
        f"±{DY*1000:.0f} mm uncertainty in locating the puck centre in Tracker in each frame, "
        f"δ{vy} = √2·δ<i>y</i>/Δ<i>t</i>; the timing uncertainty is negligible, so no horizontal bars are drawn. "
        f"Lines: unweighted least-squares fits to all points of each recording; slope uncertainties are the standard "
        f"errors of the fit (Excel LINEST).", cap),

    P(
        f"<b>What the graph shows.</b> In all three recordings {vy} falls linearly with time: positive while the puck "
        f"moves up the slope, zero at the top of the parabola (<i>t</i> ≈ {min(apex):.1f}–{max(apex):.1f} s) and negative as it "
        f"comes back down. A straight <i>v</i>–<i>t</i> line means a constant acceleration equal to its slope. On the air "
        f"cushion the only force along the table is the component of gravity down the slope, so "
        f"<i>a</i><sub>y</sub> = −<i>g</i> sinθ and <i>g</i> = |slope| / sinθ. Meanwhile <i>v</i><sub>x</sub> stays constant "
        f"(group’s averaged <i>v</i><sub>x</sub> fit: slope ≈ −0.01 {ms2}), so the horizontal motion is unaffected by the "
        f"vertical acceleration — the two components are independent.", body),

    P(
        f"<b>Slopes and their differences.</b> Recording 1: ({f(ms[0])} ± {dms[0]:.3f}) {ms2}; recording 2: "
        f"({f(ms[1])} ± {dms[1]:.3f}) {ms2}; recording 3: ({f(ms[2])} ± {dms[2]:.3f}) {ms2}. The largest difference "
        f"(recordings {worst[2]+1} and {worst[3]+1}, {worst[1]:.3f} {ms2}) is only {worst[0]:.2f}× their combined fit uncertainty, so the "
        f"three slopes agree and the lines are parallel. They differ only in intercept, i.e. the launch velocity "
        f"({R[0]['c']:.2f}, {R[1]['c']:.2f} and {R[2]['c']:.2f} {ms1}): each launch was different, but the acceleration does not "
        f"depend on how the puck was launched.", body),

    P(
        f"<b>Error bars and fit quality.</b> The ±{ev:.3f} {ms1} bars are about 10–15 % of the launch speeds. The fitted "
        f"lines pass through {R[0]['inside']*100:.0f} %, {R[1]['inside']*100:.0f} % and {R[2]['inside']*100:.0f} % of the error bars "
        f"({inside_all*100:.0f} % overall), close to the ≈68 % expected for 1σ bars, so the ±{DY*1000:.0f} mm estimate is realistic. "
        f"Recording 1 scatters more (residual SD {R[0]['s']:.2f} vs {R[2]['s']:.2f} {ms1}): its video scale is coarser (≈1.9 mm per "
        f"pixel vs ≈1 mm) and its first launch points lie 0.1–0.4 {ms1} above the line, so its bars are somewhat underestimated. "
        f"Excluding the first 0.1 s of every recording changes the slopes by ≤ {np.max(np.abs(ms_cut-ms)):.2f} {ms2} and the final "
        f"<i>g</i> to {g_cut:.2f} {ms2}, within its uncertainty, so the conclusion does not depend on this choice.", body),

    P(
        f"<b><i>g</i> from each recording.</b> <i>g</i><sub>i</sub> = |slope<sub>i</sub>| / sinθ, with "
        f"δ<i>g</i>/<i>g</i> = √[(δ<i>a</i>/<i>a</i>)<super>2</super> + (δθ/tanθ)<super>2</super>] and "
        f"δθ = {DTHETA_DEG}° (digital-level resolution), which alone contributes {ang_rel*100:.1f} %: "
        f"<i>g</i><sub>1</sub> = ({R[0]['g']:.2f} ± {R[0]['dg']:.2f}) {ms2}, <i>g</i><sub>2</sub> = ({R[1]['g']:.2f} ± {R[1]['dg']:.2f}) {ms2}, "
        f"<i>g</i><sub>3</sub> = ({R[2]['g']:.2f} ± {R[2]['dg']:.2f}) {ms2}.", body),

    P(
        f"<b>Combined value and choice of uncertainty.</b> I average the three slopes, <i>a</i> = ({f(a)} ± {da_prop:.3f}) {ms2}, "
        f"then convert to <i>g</i>. The ±{da_prop:.3f} is propagated from the fit errors, δ<i>a</i> = √(Σδ<i>a</i><sub>i</sub><super>2</super>)/3; "
        f"the standard error of the mean of the three slopes is smaller, ±{da_sem:.3f} {ms2}. I report the propagated value: the slopes "
        f"agree within their fit errors, so the small SEM only reflects three values happening to land close together, and an SEM from "
        f"just three values is itself very uncertain. The tilt error is shared by all recordings (one angle measurement), so it is "
        f"systematic, does not average down, and is added once after averaging. Result: <b><i>g</i>\u00a0=\u00a0({g:.2f} ± {dg:.2f}) {ms2} "
        f"≈ ({g:.1f} ± {dg:.1f}) {ms2}</b>. The angle term ({ang_rel*100:.1f} %) dominates the slope term "
        f"({da_prop/abs(a)*100:.1f} %), so using the SEM instead would barely change it (±{dg_sem:.2f} {ms2}).", body),

    P(
        f"<b>Comparison with the tabulated value.</b> Our result is {g-G_REF:.2f} {ms2} ({(g-G_REF)/G_REF*100:.1f} %) above "
        f"<i>g</i> = {G_REF} {ms2}, i.e. {abs(g-G_REF)/dg:.1f}σ, so the two agree within one standard uncertainty; each individual "
        f"<i>g</i><sub>i</sub> also agrees within 1σ. The small excess would be fully explained if the true tilt were "
        f"{theta_needed:.2f}° instead of {THETA_DEG:.2f}° (within the level’s resolution) or by a ≈2.5 % error in the "
        f"Tracker length calibration. As the angle now dominates the uncertainty, measuring θ more precisely (e.g. from the "
        f"height difference along the table) would improve the result most.", body),

    PageBreak(),
    Paragraph("Raw data used for Figure 1", title),
    Paragraph("Screenshot of the group spreadsheet (Sheet1): Tracker output <i>t</i>, <i>x</i>, <i>y</i> and the computed "
              "<i>v</i><sub>x</sub>, <i>v</i><sub>y</sub> for recordings (trials) 1–3. Top: rows 1–54; bottom: rows 54–85. "
              "Figure 1 plots the <i>v</i><sub>y</sub> columns (E, L, S) against the mid-point time of each frame interval.", sub),
]

W = A4[0] - 2 * 1.5 * cm
top = Image.open("raw_top.png"); bot = Image.open("raw_bottom.png")
story.append(RLImage("raw_top.png", width=W, height=W * top.size[1] / top.size[0]))
story.append(Spacer(1, 8))
# bottom screenshot was taken more zoomed-out; scale it so rows match the top one's height
bw = W * (bot.size[0] / top.size[0]) * (21.2 / 14.9)
story.append(RLImage("raw_bottom.png", width=bw, height=bw * bot.size[1] / bot.size[0], hAlign="LEFT"))

doc = SimpleDocTemplate("PHYS1552_Exp1_data_analysis.pdf", pagesize=A4, leftMargin=1.5 * cm,
                        rightMargin=1.5 * cm, topMargin=1.3 * cm, bottomMargin=1.2 * cm,
                        title="Measuring g from a projectile on a tilted air table",
                        author=NAME or "PHYS 1552 student")
doc.build(story)
print("built")
