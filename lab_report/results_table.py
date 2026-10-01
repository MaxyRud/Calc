"""Table 1: per-recording slope, angle, g and the combined g (same numbers as Figure 1)."""
import numpy as np
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from reportlab.platypus import Table, TableStyle, Paragraph
from analysis import analyse, g_from_slope, THETA_DEG, DTHETA_DEG

INK, RULE, TINT, HILITE = HexColor("#0b0b0b"), HexColor("#b5b4af"), HexColor("#f1f0eb"), HexColor("#e3eefb")
M = "−"


def numbers():
    r = analyse(verbose=False)
    R = list(r.values())
    ms = np.array([x["m"] for x in R]); dms = np.array([x["dm"] for x in R])
    a = ms.mean(); da = np.sqrt(np.sum(dms ** 2)) / 3
    g, dg = g_from_slope(a, da)
    gs = np.array([x["g"] for x in R])
    sem_g = gs.std(ddof=1) / np.sqrt(3)
    return R, g, dg, sem_g


def build_table(font="LibSans", size=7.6):
    R, g, dg, sem_g = numbers()
    hs = ParagraphStyle("th", fontName=font + "-Bold", fontSize=size, leading=size * 1.7, alignment=TA_CENTER, textColor=INK)
    cs = ParagraphStyle("td", fontName=font, fontSize=size + 0.3, leading=(size + 0.3) * 1.25, alignment=TA_CENTER, textColor=INK)
    cb = ParagraphStyle("tdb", parent=cs, fontName=font + "-Bold")
    P = lambda t, s=cs: Paragraph(t, s)
    u2 = "m s<super>−2</super>"
    th, dth = np.radians(THETA_DEG), np.radians(DTHETA_DEG)
    head = [P("", hs), P(f"Slope <i>a</i><sub>avg</sub><br/>({u2})", hs),
            P(f"Fit error δ<i>a</i><br/>({u2})", hs), P("Angle θ<br/>(rad)", hs), P("Error δθ<br/>(rad)", hs),
            P(f"<i>g</i> = |<i>a</i>|/sinθ<br/>({u2})", hs), P(f"σ<sub><i>g</i></sub><br/>({u2})", hs),
            P(f"Average <i>g</i><br/>({u2})", hs), P(f"σ<sub>SEM</sub> of <i>g</i><br/>({u2})", hs)]
    rows = [head]
    for i, x in enumerate(R):
        rows.append([P(f"Recording {i+1}", cb),
                     P(f"{x['m']:.3f} ± {x['dm']:.3f}".replace("-", M)), P(f"{x['dm']:.3f}"),
                     P(f"{th:.4f}"), P(f"{dth:.5f}"), P(f"{x['g']:.2f}"), P(f"{x['dg']:.2f}"),
                     P(f"<b>{g:.2f} ± {dg:.2f}</b>", cs) if i == 0 else "",
                     P(f"{sem_g:.2f}") if i == 0 else ""])
    t = Table(rows, colWidths=[1.85*cm, 2.55*cm, 1.75*cm, 1.45*cm, 1.55*cm, 1.95*cm, 1.45*cm, 2.35*cm, 2.0*cm],
              hAlign="CENTER")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TINT),
        ("LINEABOVE", (0, 0), (-1, 0), 0.8, RULE), ("LINEBELOW", (0, 0), (-1, 0), 0.8, RULE),
        ("LINEBELOW", (0, -1), (-1, -1), 0.8, RULE),
        ("LINEBEFORE", (7, 0), (7, -1), 0.6, RULE),
        ("SPAN", (7, 1), (7, 3)), ("SPAN", (8, 1), (8, 3)),
        ("BACKGROUND", (7, 1), (7, 3), HILITE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 2.5), ("RIGHTPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    return t


def caption_text(full=True):
    R, g, dg, sem_g = numbers()
    if not full:
        return (f"<b>Table 1.</b> Results for each recording (\u03b8 = {THETA_DEG}\u00b0 = {np.radians(THETA_DEG):.4f} rad, "
                f"\u03b4\u03b8 = {DTHETA_DEG}\u00b0 = {np.radians(DTHETA_DEG):.5f} rad). Average <i>g</i> uses the mean slope; its \u00b1{dg:.2f} is "
                "propagated from the fit errors with the shared angle error added once (reported value). "
                "\u03c3<sub>SEM</sub>\u00a0=\u00a0SD(<i>g</i><sub>1</sub>,\u00a0<i>g</i><sub>2</sub>,\u00a0<i>g</i><sub>3</sub>)/\u221a3 "
                "covers only the scatter between recordings.")
    return (f"<b>Table 1.</b> Results for each recording. θ = {THETA_DEG}° = {np.radians(THETA_DEG):.4f} rad with "
            f"δθ = {DTHETA_DEG}° = {np.radians(DTHETA_DEG):.5f} rad (digital-level resolution); "
            "σ<sub><i>g</i></sub> = <i>g</i>√[(δ<i>a</i>/<i>a</i>)<super>2</super> + (δθ/tanθ)<super>2</super>]. "
            f"Average <i>g</i> is from the mean slope; its ±{dg:.2f} is propagated from the three fit errors with the shared angle "
            f"error added once (the value reported). σ<sub>SEM</sub> = SD(<i>g</i><sub>1</sub>, <i>g</i><sub>2</sub>, "
            f"<i>g</i><sub>3</sub>)/√3 = {sem_g:.2f} shows only the scatter between recordings and leaves out the angle error.")


if __name__ == "__main__":
    # standalone image of the table (to paste into a document)
    from reportlab.platypus import SimpleDocTemplate, Spacer
    import build_pdf  # registers fonts
    from reportlab.lib.colors import HexColor as H
    cap = ParagraphStyle("c", fontName="LibSans", fontSize=7.6, leading=11.2, textColor=H("#52514e"))
    doc = SimpleDocTemplate("table1.pdf", pagesize=(18.6 * cm, 6 * cm), leftMargin=0.3*cm, rightMargin=0.3*cm,
                            topMargin=0.3*cm, bottomMargin=0.2*cm)
    doc.build([build_table(), Spacer(1, 4), Paragraph(caption_text(), cap)])
    print("table1.pdf built")
