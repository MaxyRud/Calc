"""js.17 logo concepts, defined as plain SVG geometry on a 100 x 100 grid (no masks, no text)."""
from shapely.geometry import Point, LineString, box
from shapely.ops import unary_union

# Palette sampled from the js.17 website: page background, "Start a project" button, serif headline
ONYX, IVORY, STONE = "#000000", "#EFECE6", "#ADABA5"
INK = ONYX

def wrap(path_d, fill=ONYX, bg=None, size=512, pad=0, rx=0):
    """Square SVG with the mark (drawn in 0..100) and an optional rounded background tile."""
    v = 100 + 2 * pad
    tile = f'<rect x="{-pad}" y="{-pad}" width="{v}" height="{v}" rx="{rx}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {v} {v}" width="{size}" height="{size}">'
            f'{tile}<path fill="{fill}" fill-rule="evenodd" d="{path_d}"/></svg>')

# 1 — Spark Block (recommended): an AI sparkle whose fourth quarter is a solid block.
#     Reads as spark (AI) + building block (web) + cursor (it points up-left like a mouse pointer).
SPARK = "M50 0A50 50 0 0 0 100 50L100 100L50 100A50 50 0 0 0 0 50A50 50 0 0 0 50 0Z"

def _poly_to_d(geom):
    parts = []
    for p in getattr(geom, "geoms", [geom]):
        for ring in [p.exterior, *p.interiors]:
            pts = list(ring.coords)
            parts.append("M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + "Z")
    return "".join(parts)

# 2 — Cut Medal: a medal (award-winning) sliced by three precise cuts; the cuts draw a hidden "17".
def _medal():
    disc = Point(50, 50).buffer(50, quad_segs=96)
    g = 3.6  # half-width of each cut
    one = LineString([(34, -10), (34, 110)]).buffer(g, cap_style="flat")
    seven = LineString([(34, 32), (72, 32), (51.5, 110)]).buffer(g, cap_style="flat", join_style="mitre")
    return _poly_to_d(disc.difference(unary_union([one, seven])))
MEDAL = _medal()

# 3 — Facet 17: a square block assembled from sharp facets: the "1", the "7" and the "." of js.17.
FACET = ("M0 0H26V100H0Z M34 0H100V26H34Z M74 34H100L60 100H34Z "
         "M98 86A10 10 0 1 1 78 86A10 10 0 1 1 98 86Z")

CONCEPTS = [
    ("Spark Block", SPARK, "AI spark + web building block + cursor"),
    ("Cut Medal", MEDAL, "An award medal; its cuts hide a “17”"),
    ("Facet 17", FACET, "Monogram of 1, 7 and the dot of js.17"),
]

# Two-tone Spark Block: the spark and the block quarter as separate shapes.
SPARK_ONLY = "M50 0A50 50 0 0 0 100 50L50 50L50 100A50 50 0 0 0 0 50A50 50 0 0 0 50 0Z"
BLOCK_ONLY = "M50 50H100V100H50Z"

def wrap_two_tone(spark_fill, block_fill, bg=None, size=512, pad=0, rx=0, gap=0):
    v = 100 + 2 * pad
    tile = f'<rect x="{-pad}" y="{-pad}" width="{v}" height="{v}" rx="{rx}" fill="{bg}"/>' if bg else ""
    block = f'M{50 + gap} {50 + gap}H100V100H{50 + gap}Z'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {v} {v}" width="{size}" height="{size}">'
            f'{tile}<path fill="{spark_fill}" d="{SPARK_ONLY}"/><path fill="{block_fill}" d="{block}"/></svg>')
