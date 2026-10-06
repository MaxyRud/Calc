# Transparent cutout of the studio shot: background is pure white, the plush never quite reaches 255.
import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi
src, out = sys.argv[1], sys.argv[2]
rgb = np.asarray(Image.open(src).convert("RGB")).astype(float)
mn = rgb.min(-1)
cand = mn >= 249.5                                    # pure-white candidates
lab, n = ndi.label(cand)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bgm = np.isin(lab, list(border))
fg = ~bgm
fg = ndi.binary_opening(fg, iterations=1)
lab2, n2 = ndi.label(fg); sizes = ndi.sum(fg, lab2, range(1, n2 + 1)); fg = lab2 == 1 + int(np.argmax(sizes))
fg = ndi.binary_fill_holes(fg)
# soft edge: pixels on the rim get alpha from how far they are from pure white
d = ndi.distance_transform_edt(fg)
rim = (d > 0) & (d < 2.5)
a = np.where(fg, 1.0, 0.0)
a[rim] = np.clip((255 - mn[rim]) / 18.0, 0.35, 1.0)
alpha = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
# de-fringe: pull edge colours slightly darker so no white halo on dark pages
im = Image.fromarray(rgb.astype(np.uint8)); im.putalpha(alpha)
bbox = alpha.getbbox(); im = im.crop((bbox[0] - 2, bbox[1] - 2, bbox[2] + 2, bbox[3] + 2))
im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
im.save(out); print(im.size)
