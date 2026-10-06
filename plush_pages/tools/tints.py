# Pastel colourway previews for a white plush: keep lightness, add the tint's colour only to the fabric
# (dark embroidery stays black). usage: python3 tints.py <plush.png> <assets_dir>
import sys, numpy as np, cv2
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGBA"); a = im.getchannel("A")
rgb = np.asarray(im.convert("RGB"))
lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(float)
L = lab[..., 0]
w = np.clip((L - 95) / 80, 0, 1)                     # fabric gets tint, embroidery (dark) does not
TINTS = {"ar": None, "bl": (244, 182, 204), "gl": (176, 214, 245), "ma": (186, 230, 190)}
for k, t in TINTS.items():
    if t is None: o = rgb.copy()
    else:
        tl = cv2.cvtColor(np.uint8([[t]]), cv2.COLOR_RGB2LAB)[0, 0].astype(float)
        nl = lab.copy()
        nl[..., 1] = 128 + (tl[1] - 128) * w * 1.05
        nl[..., 2] = 128 + (tl[2] - 128) * w * 1.05
        nl[..., 0] = L - w * 6                       # a touch deeper so pastel reads on white pages
        o = cv2.cvtColor(np.clip(nl, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
    img = Image.fromarray(o); img.putalpha(a)
    img.save(f"{out}/plush-{k}.webp", quality=88, method=6)
    img.resize((img.width // 2, img.height // 2), Image.LANCZOS).save(f"{out}/plush-{k}-sm.webp", quality=86, method=6)
print("ok")
