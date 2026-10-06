# Make the four colourway images from the cutout by rotating hue (the orange safety tip is left untouched).
# usage: python3 colorways.py <blaster.png> <assets_dir>
import sys, numpy as np
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGBA"); W, H = im.size
rgb = im.convert("RGB"); alpha = im.getchannel("A")
hsv = np.asarray(rgb.convert("HSV")).astype(np.int16)
h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
xx = np.mgrid[0:H, 0:W][1]
tip = (((h < 14) | (h > 235)) & (s > 60)) & (xx < W * 0.28)   # orange safety tip stays orange
# name: (hue shift in degrees, saturation gain)
ways = {"pg": (0, 1.0), "bm": (52, 0.95), "om": (-62, 1.0), "lp": (180, 1.0)}
for name, (deg, sg) in ways.items():
    hh = h.copy(); sh = int(round(deg / 360 * 256))
    hh = np.where(tip, h, (h + sh) % 256)
    ss = np.where(tip, s, np.clip(s * sg, 0, 255))
    o = Image.fromarray(np.stack([hh, ss, v], -1).astype(np.uint8), "HSV").convert("RGB")
    o.putalpha(alpha)
    o.save(f"{out}/blaster-{name}.webp", quality=88, method=6)
    o.resize((W // 2, H // 2), Image.LANCZOS).save(f"{out}/blaster-{name}-sm.webp", quality=86, method=6)
# contact sheet for checking
sheet = Image.new("RGB", (W // 2 * 4, H // 2), (24, 22, 30))
for i, n in enumerate(ways):
    t = Image.open(f"{out}/blaster-{n}-sm.webp"); sheet.paste(t, (i * W // 2, 0), t)
sheet.save("sheet.png")
