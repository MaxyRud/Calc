import io, cairosvg
from PIL import Image, ImageDraw, ImageFont
from marks import svg, SPARK, medal, FACET

def png(svgtxt, px):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svgtxt.encode(), output_width=px, output_height=px))).convert("RGBA")

INK, VOLT, WHITE = "#0A0A0B", "#C8FF2E", "#FFFFFF"
concepts = [
    ("Spark Block", lambda f: SPARK),
    ("Cut Medal", None),
    ("Facet 17", lambda f: FACET),
]
W, H = 1800, 1250
sheet = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(sheet)
font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 34)
for i, (name, fn) in enumerate(concepts):
    x = 60 + i * 590
    d.text((x, 30), name, fill=INK, font=font)
    def mk(fill, bg=None, pad=0, rx=0):
        body = medal(fill, bg) if fn is None else fn(fill)
        return svg(body, fill=fill, bg=bg, pad=pad, rx=rx)
    sheet.paste(png(mk(INK), 420), (x + 30, 100), png(mk(INK), 420))
    tile = png(mk(VOLT, INK, pad=22, rx=30), 250); sheet.paste(tile, (x, 580), tile)
    tile = png(mk(INK, VOLT, pad=22, rx=30), 250); sheet.paste(tile, (x + 280, 580), tile)
    for j, s in enumerate([64, 32, 16]):
        fav = png(mk(WHITE, INK, pad=14, rx=22), s)
        sheet.paste(fav, (x + 20 + j * 110, 900), fav)
        fav2 = png(mk(INK, None, pad=6), s)
        sheet.paste(fav2, (x + 20 + j * 110, 1020), fav2)
sheet.save("/tmp/claude-0/-home-user-Calc/e6f0d9f7-ab4b-5036-9389-ab206d9e0899/scratchpad/quick_sheet.png")
print("ok")
