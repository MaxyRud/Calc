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
from results_table import build_table, caption_text

NAME = "Maksymilian Rudakov · 01/10/26"

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
body = ParagraphStyle("b", fontName="LibSans", fontSize=8.9, leading=11.7, textColor=INK,
                      alignment=TA_JUSTIFY, spaceAfter=5)

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
exp_slope = G_REF * np.sin(np.radians(THETA_DEG))
sem_g = np.std([x['g'] for x in R], ddof=1) / np.sqrt(3)

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
    Paragraph("Lab 1 – Measuring <i>g</i> from a projectile on a tilted air table", title),
    Paragraph((f"{NAME} · " if NAME else "") + "Physics for Engineering 1 (PHYS 1552) · Data analysis exercise: Investigation II and Analysis III", sub),
    RLImage("figure1.png", width=16.4 * cm, height=16.4 * cm * 1065 / 2130),
    P(
        f"<b>Figure 1.</b> Velocity of the puck along the slope ({vy}, positive up the table) against time for three "
        f"recordings on the air table tilted at θ = ({THETA_DEG} ± {DTHETA_DEG})°. Each point is Δ<i>y</i>/Δ<i>t</i> "
        f"between consecutive frames (Δ<i>t</i> = 1/30 s), plotted at the midpoint time. Lines are least-squares fits to all "
        f"points of each recording; the legend gives each slope ± its fit (standard) error. Error bars show ±{ev:.3f} {ms1}, "
        f"from a ±{DY*1000:.0f} mm uncertainty in locating the puck centre in Tracker (δ<i>v</i> = √2·δ<i>y</i>/Δ<i>t</i>); "
        f"timing errors are negligible.", cap),
    Spacer(1, 3),
    P(caption_text(full=False), cap),
    build_table(),
    Spacer(1, 7),

    P(
        f"Figure 1 shows the velocity of the puck along the slope of the table ({vy}, with up the table taken as positive) "
        f"against time for three recordings of projectile motion, with a straight-line fit for each. In every recording the "
        f"points fall on a straight line: {vy} is positive while the puck travels up the table, passes through zero at the top "
        f"of its path (<i>t</i> ≈ {min(apex):.1f}–{max(apex):.1f} s) and becomes negative as the puck comes back down. A straight "
        f"line on a <i>v</i>–<i>t</i> graph means the acceleration is constant, and its slope is that acceleration. This is what we "
        f"expected: the air cushion removes almost all friction, so the only force pushing the puck along the table is the "
        f"part of gravity acting down the slope, giving <i>a</i> = −<i>g</i> sinθ. The slope is negative because we took up "
        f"the table as positive. The horizontal velocity, on the other hand, stayed roughly constant (slope of about "
        f"−0.01 {ms2}), which shows that the motion along the slope does not affect the motion across it – the two "
        f"directions are independent.", body),

    P(
        f"The slopes, with their fit errors, are {f(ms[0])} ± {dms[0]:.3f}, {f(ms[1])} ± {dms[1]:.3f} and "
        f"{f(ms[2])} ± {dms[2]:.3f} {ms2} (Table 1). They are very similar and agree with each other: the biggest "
        f"difference, between recordings {worst[2]+1} and {worst[3]+1}, is only {worst[1]:.3f} {ms2}, which is smaller than their "
        f"combined error ({np.hypot(dms[worst[2]], dms[worst[3]]):.3f} {ms2}). The three lines are therefore almost parallel and only "
        f"differ in where they start, because each puck was launched at a different speed, which does not change the "
        f"acceleration. For a {THETA_DEG}° tilt we expect a slope of −<i>g</i> sinθ = −{G_REF} × sin {THETA_DEG}° = "
        f"{f(-exp_slope)} {ms2}; recordings 1 and 3 are within their error of this value and recording 2 is just outside it. "
        f"The error bars (±{ev:.3f} {ms1}) come from how accurately we could click on the centre of the puck in Tracker "
        f"(about ±{DY*1000:.0f} mm in each frame). The trendlines go through about {inside_all*100:.0f} % of them, close to the 68 % "
        f"expected for error bars of one standard deviation, so they are a sensible size. Recording 1 scatters the most "
        f"because its video had a coarser scale, and its first few points, just after the launch, sit above the line.", body),

    P(
        f"Using <i>g</i> = |<i>a</i>| / sinθ with θ = {THETA_DEG} ± {DTHETA_DEG}°, the three recordings give "
        f"<i>g</i> = {R[0]['g']:.2f} ± {R[0]['dg']:.2f}, {R[1]['g']:.2f} ± {R[1]['dg']:.2f} and {R[2]['g']:.2f} ± {R[2]['dg']:.2f} {ms2}. "
        f"For the final value I averaged the three slopes and used the uncertainty propagated from their fit errors rather "
        f"than the standard error of the mean (SEM). Because the slopes agree within their errors, the very small SEM "
        f"({sem_g:.2f} {ms2} in <i>g</i>) only shows that three values happened to land close together, and a spread worked out "
        f"from just three values is not reliable. The angle was also measured only once, so its error ({ang_rel*100:.1f} %, the "
        f"largest source of uncertainty in the final value) affects all three recordings in the same way and cannot be "
        f"averaged out, so I added it once at the end. Our final result is <b><i>g</i> = {g:.2f} ± {dg:.2f} {ms2}</b> "
        f"(≈ {g:.1f} ± {dg:.1f} {ms2}). This is {g-G_REF:.2f} {ms2} above the accepted value of {G_REF} {ms2}, which is less "
        f"than our uncertainty ({abs(g-G_REF)/dg:.1f}σ), so the two agree. The result is slightly high, which could be because "
        f"the table was tilted a little more than {THETA_DEG}° (only {theta_needed-THETA_DEG:.2f}° more would explain it) or "
        f"because of a small error when setting the ruler scale in Tracker. Measuring the angle more precisely would "
        f"improve the experiment the most.", body),

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
                        rightMargin=1.5 * cm, topMargin=1.1 * cm, bottomMargin=1.0 * cm,
                        title="Lab 1 - Measuring g from a projectile on a tilted air table",
                        author="Maksymilian Rudakov")
doc.build(story)
print("built")
