"""Step-by-step uncertainty workings (supporting document, not part of the 1-page submission)."""
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
import build_pdf  # registers the LibSans font family (and rebuilds the submission PDF)
from analysis import analyse, THETA_DEG, DTHETA_DEG, DY, G_REF, FPS

INK, MUTED, RULE, TINT = HexColor("#0b0b0b"), HexColor("#52514e"), HexColor("#d9d8d3"), HexColor("#f4f3ef")
title = ParagraphStyle("t", fontName="LibSans-Bold", fontSize=13, leading=16, textColor=INK)
sub = ParagraphStyle("s", fontName="LibSans", fontSize=8.5, leading=11, textColor=MUTED, spaceAfter=6)
h = ParagraphStyle("h", fontName="LibSans-Bold", fontSize=10, leading=13, textColor=INK, spaceBefore=7, spaceAfter=2)
body = ParagraphStyle("b", fontName="LibSans", fontSize=8.8, leading=12, textColor=INK, spaceAfter=2)
eq = ParagraphStyle("e", parent=body, leftIndent=14)
note = ParagraphStyle("n", parent=body, textColor=MUTED, fontSize=8.3, leading=11)
cell = ParagraphStyle("c", fontName="LibSans", fontSize=8.3, leading=10.5, textColor=INK)
cellb = ParagraphStyle("cb", parent=cell, fontName="LibSans-Bold")

M = "−"
def f(v, n=4):
    return f"{v:.{n}f}".replace("-", M)
ms1, ms2 = "m s<super>−1</super>", "m s<super>−2</super>"
vy = "<i>v</i><sub>y</sub>"

def table(rows, widths):
    t = Table([[Paragraph(str(c), cellb if i == 0 else cell) for c in row] for i, row in enumerate(rows)],
              colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.8, RULE), ("LINEBELOW", (0, -1), (-1, -1), 0.8, RULE),
                           ("BACKGROUND", (0, 0), (-1, 0), TINT), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    return t

# ---------------- numbers ----------------
r = analyse(verbose=False)
R = list(r.values())
dt = 1 / FPS
dv = np.sqrt(2) * DY / dt
th, dth = np.radians(THETA_DEG), np.radians(DTHETA_DEG)
sin, tan = np.sin(th), np.tan(th)
ang = dth / tan
for x in R:
    t, v = x["t"], x["v"]
    x["tb"], x["vb"] = t.mean(), v.mean()
    x["stt"] = np.sum((t - x["tb"]) ** 2)
    x["stv"] = np.sum((t - x["tb"]) * (v - x["vb"]))
    x["ssr"] = np.sum((v - x["m"] * t - x["c"]) ** 2)
    x["rel"] = x["dm"] / abs(x["m"])
    x["relg"] = np.hypot(x["rel"], ang)
    x["nin"] = int(np.sum(np.abs(v - x["m"] * t - x["c"]) <= x["ev"]))
ms = np.array([x["m"] for x in R]); dms = np.array([x["dm"] for x in R])
a = ms.mean()
da_prop = np.sqrt(np.sum(dms ** 2)) / 3
sd = ms.std(ddof=1); sem = sd / np.sqrt(3)
g = abs(a) / sin
relA = np.hypot(da_prop / abs(a), ang); relB = np.hypot(sem / abs(a), ang)
dg, dg_sem = g * relA, g * relB
gs = np.array([x["g"] for x in R]); dgs = np.array([x["dg"] for x in R])
naive = np.sqrt(np.sum(dgs ** 2)) / 3
x1 = R[0]

s = []
s += [Paragraph("Uncertainty calculations, step by step", title),
      Paragraph("Supporting workings for the PHYS 1552 Experiment 1 data analysis exercise (Investigation II and Analysis III). "
                "Every number below is computed from the spreadsheet data by <font face='LibSans-Italic'>analysis.py</font>.", sub)]

# Step 1
s += [Paragraph("Step 1: error bar on each velocity point", h),
      Paragraph(f"Each point is {vy} = (<i>y</i><sub>2</sub> − <i>y</i><sub>1</sub>) / Δ<i>t</i>. Two quantities are uncertain:", body),
      Paragraph(f"• Position: δ<i>y</i> = ±{DY*1000:.0f} mm on <i>each</i> tracked position (how precisely the puck centre can be clicked in Tracker, about 1–2 pixels).", eq),
      Paragraph(f"• Time: Δ<i>t</i> = 1/30 s = {dt:.4f} s, set by the camera frame rate, so δ<i>t</i> ≈ 0 (negligible).", eq),
      Paragraph("The difference of two independent errors adds in quadrature:", body),
      Paragraph(f"δ(Δ<i>y</i>) = √(δ<i>y</i><super>2</super> + δ<i>y</i><super>2</super>) = √2·δ<i>y</i> = 1.414 × {DY:.3f} m = {np.sqrt(2)*DY:.5f} m", eq),
      Paragraph(f"δ{vy} = √2·δ<i>y</i> / Δ<i>t</i> = {np.sqrt(2)*DY:.5f} / {dt:.4f} = <b>±{dv:.3f} {ms1}</b>", eq),
      Paragraph(f"Example (recording 1, first point): {vy} = (0.0424 − 0.00385) / {dt:.4f} = 1.16 ± {dv:.3f} {ms1}. "
                f"(Recording 1 has one interval of 0.1 s where frames were skipped; there δ{vy} = {np.sqrt(2)*DY:.5f}/0.1 = {np.sqrt(2)*DY/0.1:.3f} {ms1}.)", note)]

# Step 2
s += [Paragraph("Step 2: slope and its fit uncertainty (what Excel LINEST does)", h),
      Paragraph(f"For the <i>N</i> points (<i>t</i>, {vy}) of one recording, with means <i>t̄</i> and <i>v̄</i>:", body),
      Paragraph("<i>S</i><sub>tt</sub> = Σ(<i>t</i> − <i>t̄</i>)<super>2</super>,&nbsp;&nbsp; <i>S</i><sub>tv</sub> = Σ(<i>t</i> − <i>t̄</i>)(<i>v</i> − <i>v̄</i>),&nbsp;&nbsp; "
                "slope <i>m</i> = <i>S</i><sub>tv</sub> / <i>S</i><sub>tt</sub>,&nbsp;&nbsp; intercept <i>c</i> = <i>v̄</i> − <i>m t̄</i>", eq),
      Paragraph("residual standard deviation <i>s</i> = √[ Σ(<i>v</i> − (<i>mt</i> + <i>c</i>))<super>2</super> / (<i>N</i> − 2) ],&nbsp;&nbsp; "
                "slope uncertainty <b>δ<i>m</i> = <i>s</i> / √<i>S</i><sub>tt</sub></b>", eq),
      Paragraph(f"Worked for recording 1: <i>m</i> = {f(x1['stv'],3)} / {x1['stt']:.3f} = {f(x1['m'])} {ms2};&nbsp; "
                f"<i>s</i> = √({x1['ssr']:.4f} / {x1['n']-2}) = {x1['s']:.4f} {ms1};&nbsp; "
                f"δ<i>m</i> = {x1['s']:.4f} / √{x1['stt']:.3f} = {x1['s']:.4f} / {np.sqrt(x1['stt']):.3f} = {x1['dm']:.4f} {ms2}.", body),
      table([["Rec.", "<i>N</i>", "<i>S</i><sub>tt</sub> (s<super>2</super>)", "<i>S</i><sub>tv</sub> (m)",
              "Σ residual<super>2</super>", f"<i>s</i> ({ms1})", f"slope <i>m</i> ({ms2})", f"δ<i>m</i> ({ms2})", "δ<i>m</i>/|<i>m</i>|"]] +
            [[f"{i+1}", x["n"], f"{x['stt']:.3f}", f(x["stv"], 3), f"{x['ssr']:.4f}", f"{x['s']:.4f}", f(x["m"]), f"{x['dm']:.4f}",
              f"{x['rel']*100:.2f} %"] for i, x in enumerate(R)],
            [1.1*cm, 1.0*cm, 1.8*cm, 1.8*cm, 2.2*cm, 1.9*cm, 2.6*cm, 2.2*cm, 2.0*cm])]

# Step 3
pairs = [(i, j) for i in range(3) for j in range(i + 1, 3)]
s += [Paragraph("Step 3: do the three slopes agree?", h),
      Paragraph("Compare each pair using their combined uncertainty: <i>z</i> = |<i>m</i><sub>i</sub> − <i>m</i><sub>j</sub>| / √(δ<i>m</i><sub>i</sub><super>2</super> + δ<i>m</i><sub>j</sub><super>2</super>)", eq),
      Paragraph(";&nbsp;&nbsp; ".join(
          f"{i+1} vs {j+1}: {abs(ms[i]-ms[j]):.4f} / {np.hypot(dms[i],dms[j]):.4f} = <b>{abs(ms[i]-ms[j])/np.hypot(dms[i],dms[j]):.2f}</b>"
          for i, j in pairs) + ".&nbsp; All are below 1, so the slopes agree within their fit uncertainties.", eq)]

# Step 4
s += [Paragraph("Step 4: <i>g</i> from each recording", h),
      Paragraph(f"Along the tilted table <i>a</i><sub>y</sub> = −<i>g</i> sinθ, so <b><i>g</i> = |<i>m</i>| / sinθ</b>, with sin {THETA_DEG}° = {sin:.5f}. "
                "Two inputs are uncertain (<i>m</i> and θ), so their <i>relative</i> uncertainties add in quadrature:", body),
      Paragraph("δ<i>g</i>/<i>g</i> = √[ (δ<i>m</i>/<i>m</i>)<super>2</super> + (δ(sinθ)/sinθ)<super>2</super> ],&nbsp;&nbsp; "
                "and since δ(sinθ) = cosθ·δθ,&nbsp; δ(sinθ)/sinθ = δθ/tanθ", eq),
      Paragraph(f"Angle term: δθ = {DTHETA_DEG}° × π/180 = {dth:.6f} rad (must be in radians);&nbsp; tan {THETA_DEG}° = {tan:.5f};&nbsp; "
                f"δθ/tanθ = {dth:.6f} / {tan:.5f} = <b>{ang:.4f} = {ang*100:.2f} %</b>", eq),
      table([["Rec.", f"<i>g</i> = |<i>m</i>| / sinθ ({ms2})", "δ<i>m</i>/|<i>m</i>|", "δθ/tanθ",
              "δ<i>g</i>/<i>g</i> = √(a<super>2</super> + b<super>2</super>)", f"δ<i>g</i> ({ms2})", "Result"]] +
            [[f"{i+1}", f"{abs(x['m']):.4f} / {sin:.5f} = {x['g']:.3f}", f"{x['rel']*100:.2f} %", f"{ang*100:.2f} %",
              f"√({x['rel']*100:.2f}<super>2</super> + {ang*100:.2f}<super>2</super>) = {x['relg']*100:.2f} %",
              f"{x['g']:.3f} × {x['relg']:.4f} = {x['dg']:.2f}", f"<b>{x['g']:.2f} ± {x['dg']:.2f}</b>"] for i, x in enumerate(R)],
            [1.1*cm, 4.3*cm, 1.7*cm, 1.6*cm, 3.8*cm, 3.1*cm, 2.2*cm])]

# Step 5
s += [Paragraph("Step 5: combine the three slopes, two ways", h),
      Paragraph(f"Mean slope: <i>ā</i> = ({f(ms[0])} {f(ms[1])} {f(ms[2])}) / 3 = {f(ms.sum())} / 3 = <b>{f(a)} {ms2}</b>".replace(f" {M}", f" + ({M}", 2)
                .replace(f"{f(ms[1])}", f"{f(ms[1])})").replace(f"{f(ms[2])} /", f"{f(ms[2])}) /"), eq),
      Paragraph(f"<b>A. Propagated from the fit errors.</b> For a mean of three values, δ<i>ā</i> = √(δ<i>m</i><sub>1</sub><super>2</super> + "
                f"δ<i>m</i><sub>2</sub><super>2</super> + δ<i>m</i><sub>3</sub><super>2</super>) / 3 = "
                f"√({dms[0]:.4f}<super>2</super> + {dms[1]:.4f}<super>2</super> + {dms[2]:.4f}<super>2</super>) / 3 = "
                f"√{np.sum(dms**2):.6f} / 3 = {np.sqrt(np.sum(dms**2)):.4f} / 3 = <b>{da_prop:.4f} {ms2}</b>", eq),
      Paragraph(f"<b>B. Statistical (standard error of the mean).</b> Deviations from the mean: "
                f"{', '.join(f(d, 5) for d in ms - a)}; sample standard deviation σ = √[Σ(<i>m</i><sub>i</sub> − <i>ā</i>)<super>2</super> / (3 − 1)] = "
                f"√({np.sum((ms-a)**2):.6f} / 2) = {sd:.5f};&nbsp; SEM = σ/√3 = {sd:.5f} / 1.732 = <b>{sem:.4f} {ms2}</b>", eq),
      Paragraph(f"<b>Which one?</b> A ({da_prop:.4f}) is about {da_prop/sem:.1f}× larger than B ({sem:.4f}). Step 3 showed the slopes agree within their "
                "fit errors, so the scatter between recordings is no bigger than the random error already in each fit. B is small only because three "
                "values happened to land close together, and a standard deviation from just three numbers is itself very uncertain (roughly ±50 %). "
                "So A is the more honest (more conservative) choice.", body)]

# Step 6
s += [Paragraph("Step 6: combined <i>g</i> and its uncertainty", h),
      Paragraph(f"<i>g</i> = |<i>ā</i>| / sinθ = {abs(a):.4f} / {sin:.5f} = {g:.3f} {ms2}", eq),
      Paragraph(f"δ<i>g</i>/<i>g</i> = √[ (δ<i>ā</i>/<i>ā</i>)<super>2</super> + (δθ/tanθ)<super>2</super> ] = "
                f"√[ ({da_prop:.4f}/{abs(a):.4f})<super>2</super> + {ang:.4f}<super>2</super> ] = √({da_prop/abs(a)*100:.2f}<super>2</super> + "
                f"{ang*100:.2f}<super>2</super>) % = {relA*100:.2f} %", eq),
      Paragraph(f"δ<i>g</i> = {g:.3f} × {relA:.4f} = {dg:.3f} {ms2}&nbsp;&nbsp; →&nbsp;&nbsp; <b><i>g</i> = ({g:.2f} ± {dg:.2f}) {ms2} "
                f"≈ ({g:.1f} ± {dg:.1f}) {ms2}</b> (uncertainty rounded to 1 s.f., value to the same decimal place)", eq),
      Paragraph(f"With the SEM instead: √({sem/abs(a)*100:.2f}<super>2</super> + {ang*100:.2f}<super>2</super>) % = {relB*100:.2f} % → ±{dg_sem:.2f} {ms2}. "
                "The angle term dominates either way.", note),
      Paragraph(f"<b>Why not simply average <i>g</i><sub>1</sub>, <i>g</i><sub>2</sub>, <i>g</i><sub>3</sub> and use √(Σδ<i>g</i><sub>i</sub><super>2</super>)/3?</b> "
                f"That gives ±{naive:.2f} {ms2}, but it wrongly treats the angle error as independent in each recording. All three recordings used the "
                f"<i>same</i> tilt, measured once, so its {ang*100:.2f} % is a shared (systematic) error: it does not shrink when you average. "
                "That is why the slopes are averaged first and the angle uncertainty is added once at the end.", body)]

# Step 7
z = (g - G_REF) / dg
s += [Paragraph("Step 7: compare with the tabulated value", h),
      Paragraph(f"<i>z</i> = |<i>g</i> − <i>g</i><sub>ref</sub>| / δ<i>g</i> = |{g:.3f} − {G_REF}| / {dg:.3f} = {abs(g-G_REF):.3f} / {dg:.3f} = <b>{abs(z):.2f}</b>", eq),
      Paragraph(f"<i>z</i> &lt; 1, so the result agrees with {G_REF} {ms2} within one standard uncertainty (|<i>z</i>| &lt; 2 is the usual threshold). "
                f"Individual recordings: <i>z</i> = {', '.join(f'{abs(v):.2f}' for v in (gs - G_REF) / dgs)}, all &lt; 1.", body)]

# Step 8
tot_in = sum(x["nin"] for x in R); tot = sum(x["n"] for x in R)
s += [Paragraph("Step 8: are the error bars a sensible size?", h),
      Paragraph(f"Count the points whose error bar touches the fitted line, i.e. |<i>v</i> − (<i>mt</i> + <i>c</i>)| ≤ {dv:.3f} {ms1}: "
                + ", ".join(f"recording {i+1}: {x['nin']}/{x['n']} = {x['nin']/x['n']*100:.0f} %" for i, x in enumerate(R))
                + f"; overall {tot_in}/{tot} = {tot_in/tot*100:.0f} %. For 1σ error bars about 68 % should touch the line, so "
                "±2 mm is a realistic position uncertainty (slightly small for recording 1, whose video has a coarser scale).", body)]

# Excel
s += [KeepTogether([Paragraph("Doing the same in Excel", h),
      table([["Quantity", "Excel formula (adjust the cell ranges)"],
             ["Error bar δ<i>v</i><sub>y</sub>", "=SQRT(2)*0.002/(1/30)"],
             ["Mid-point time", "=(A7+A8)/2   (next to each <i>v</i><sub>y</sub>)"],
             ["Slope <i>m</i> and δ<i>m</i>", "=INDEX(LINEST(vy_range, tmid_range, TRUE, TRUE), 1, 1)   and   =INDEX(LINEST(...), 2, 1)"],
             ["<i>g</i>", "=ABS(m)/SIN(RADIANS(3.5))"],
             ["δ<i>g</i>", "=g*SQRT((dm/m)^2 + (RADIANS(0.1)/TAN(RADIANS(3.5)))^2)"],
             ["Propagated δ<i>ā</i>", "=SQRT(SUMSQ(dm1, dm2, dm3))/3"],
             ["SEM", "=STDEV.S(m1, m2, m3)/SQRT(3)"]],
            [3.4*cm, 14.3*cm])])]

doc = SimpleDocTemplate("Uncertainty_workings.pdf", pagesize=A4, leftMargin=1.6*cm, rightMargin=1.6*cm,
                        topMargin=1.4*cm, bottomMargin=1.4*cm, title="Uncertainty calculations, step by step")
doc.build(s)
print("workings built")
