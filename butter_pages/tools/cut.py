# Cut the butter stick out of a white-background listing photo, dropping overlay text and dimension lines.
import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi
src, out, box = sys.argv[1], sys.argv[2], [int(v) for v in sys.argv[3].split(',')]
im = Image.open(src).convert('RGB').crop(box)
a = np.asarray(im).astype(float)
hsv = np.asarray(im.convert('HSV')).astype(float) / 255
s, v = hsv[..., 1], hsv[..., 2]
yel = (s > 0.16) & (v > 0.55) & (a[..., 0] > a[..., 2] + 25)          # butter yellow
m = ndi.binary_closing(yel, iterations=3)
lab, n = ndi.label(m); sz = ndi.sum(m, lab, range(1, n + 1)); m = lab == 1 + int(np.argmax(sz))
m = ndi.binary_fill_holes(m)                                             # keeps the navy print
m = ndi.binary_opening(m, iterations=2)
alpha = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
im.putalpha(alpha); bb = alpha.getbbox(); im = im.crop((bb[0] - 2, bb[1] - 2, bb[2] + 2, bb[3] + 2))
im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
im.save(out); print(out, im.size)
