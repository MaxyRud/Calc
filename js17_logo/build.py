import io, os, glob, cairosvg
from PIL import Image, ImageDraw, ImageFont
from marks import wrap, wrap_two_tone, CONCEPTS, SPARK, ONYX, IVORY, STONE

os.makedirs("svg", exist_ok=True); os.makedirs("png", exist_ok=True)
for f in glob.glob("svg/js17-*.svg") + glob.glob("png/js17-*.png"):
    os.remove(f)                                     # drop the old lime versions
def png(svgtxt, px):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svgtxt.encode(), output_width=px, output_height=px))).convert("RGBA")
def save_svg(name, txt):
    open(f"svg/{name}.svg", "w").write(txt)

for name, d, _ in CONCEPTS:
    save_svg(f"concept-{name.lower().replace(' ', '-')}", wrap(d, ONYX))

kit = {
    "js17-mark-ivory": wrap(SPARK, IVORY),                     # main logo on the black site
    "js17-mark-stone": wrap(SPARK, STONE),                     # quieter version, e.g. footer
    "js17-mark-onyx": wrap(SPARK, ONYX),                       # on light backgrounds / print
    "js17-mark-two-tone": wrap_two_tone(IVORY, STONE),         # ivory spark + stone block
    "js17-app-icon": wrap(SPARK, IVORY, bg=ONYX, pad=24, rx=30),
    "js17-app-icon-light": wrap(SPARK, ONYX, bg=IVORY, pad=24, rx=30),
    "js17-favicon": wrap(SPARK, IVORY, bg=ONYX, pad=14, rx=22),
}
for k, v in kit.items():
    save_svg(k, v)
for k in ["js17-mark-ivory", "js17-mark-stone", "js17-mark-onyx", "js17-mark-two-tone"]:
    png(kit[k], 1024).save(f"png/{k}-1024.png")
for s in [1024, 512, 180]:
    png(kit["js17-app-icon"], s).save(f"png/js17-app-icon-{s}.png")
for s in [16, 32, 48]:
    png(kit["js17-favicon"], s).save(f"png/js17-favicon-{s}.png")
png(kit["js17-favicon"], 256).save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

# ---------------------------------------------------------------- board
B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F = lambda path, size: ImageFont.truetype(path, size)
W, H = 2400, 1820
bd = Image.new("RGB", (W, H), ONYX)
d = ImageDraw.Draw(bd)
def paste(img, xy): bd.paste(img, xy, img)

d.text((90, 70), "js.17 · logo in your website colours", fill=IVORY, font=F(B, 54))
d.text((90, 140), "Spark Block, recoloured to the palette of the current site: black, warm ivory and stone grey.",
       fill=STONE, font=F(R, 26))

# hero mock in the site's style
hx, hy, hw, hh = 90, 220, 2220, 760
d.rounded_rectangle((hx, hy, hx + hw, hy + hh), radius=24, fill="#050505", outline="#222222", width=2)
paste(png(wrap(SPARK, IVORY), 54), (hx + 50, hy + 45))
d.text((hx + 122, hy + 44), "js.17", fill=IVORY, font=F(R, 26))
d.text((hx + 122, hy + 74), "STORE ATELIER", fill=IVORY, font=F(R, 24))
for k, item in enumerate(["AI", "SERVICES", "WORK", "PRICING", "CONTACT"]):
    d.text((hx + hw - 330, hy + 44 + k * 26), item, fill=IVORY, font=F(R, 22))
tw = d.textlength("START A PROJECT", font=F(R, 24))
bx0 = hx + hw - 100 - tw - 60
d.rounded_rectangle((bx0, hy + 200, hx + hw - 60, hy + 262), radius=31, fill=IVORY)
d.text((bx0 + 34, hy + 216), "START A PROJECT", fill=ONYX, font=F(R, 24))
d.text((bx0 + 34 + tw + 14, hy + 214), "↘", fill=ONYX, font=F("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24))
d.text((hx + 520, hy + 130), "js.17", fill=STONE, font=F(SERIF, 190))
d.text((hx + 300, hy + 360), "Luxury Store", fill=STONE, font=F(SERIF, 190))
paste(png(wrap(SPARK, IVORY), 230), (hx + hw - 560, hy + 420))
d.text((hx + hw - 560, hy + 670), "the mark at hero size", fill=STONE, font=F(R, 22))

# variants row
y0 = 1040
d.text((90, y0), "Versions", fill=IVORY, font=F(B, 34))
tiles = [
    ("Ivory on black (main)", wrap(SPARK, IVORY), ONYX),
    ("Stone (quiet, e.g. footer)", wrap(SPARK, STONE), ONYX),
    ("Two-tone", wrap_two_tone(IVORY, STONE), ONYX),
    ("Black on ivory", wrap(SPARK, ONYX), IVORY),
]
for k, (label, svgtxt, bg) in enumerate(tiles):
    x = 90 + k * 380
    d.rounded_rectangle((x, y0 + 60, x + 340, y0 + 400), radius=20, fill=bg, outline="#2A2A2A", width=2)
    paste(png(svgtxt, 200), (x + 70, y0 + 120))
    d.text((x, y0 + 420), label, fill=STONE, font=F(R, 22))
# app icons + favicons
x = 1660
d.text((x, y0), "App icon & favicon", fill=IVORY, font=F(B, 34))
paste(png(kit["js17-app-icon"], 260), (x, y0 + 70))
d.rounded_rectangle((x, y0 + 70, x + 259, y0 + 329), radius=53, outline="#3A3A3A", width=2)
paste(png(kit["js17-app-icon-light"], 260), (x + 300, y0 + 70))
for j, s in enumerate([48, 32, 16]):
    paste(png(kit["js17-favicon"], s), (x + j * 80, y0 + 380 - s // 2))
d.text((x + 240, y0 + 368), "favicon 48 / 32 / 16 px", fill=STONE, font=F(R, 22))

# palette
y1 = 1560
d.text((90, y1), "Colours (sampled from the site)", fill=IVORY, font=F(B, 34))
for k, (nm, hx_, txt, use) in enumerate([
        ("Onyx", ONYX, IVORY, "page background"),
        ("Ivory", IVORY, ONYX, "buttons, nav text, main logo"),
        ("Stone", STONE, ONYX, "serif headlines, quiet logo")]):
    xx = 90 + k * 560
    d.rounded_rectangle((xx, y1 + 60, xx + 160, y1 + 200), radius=16, fill=hx_, outline="#3A3A3A", width=2)
    d.text((xx + 185, y1 + 85), f"{nm}  {hx_}", fill=IVORY, font=F(B, 26))
    d.text((xx + 185, y1 + 125), use, fill=STONE, font=F(R, 22))
bd.save("js17-logo-board.png")

with __import__("zipfile").ZipFile("js17-logo-kit.zip", "w", 8) as z:
    for f in sorted(glob.glob("svg/*.svg") + glob.glob("png/*.png")) + ["favicon.ico", "js17-logo-board.png"]:
        z.write(f, "js17-logo-kit/" + f)
print("built")
