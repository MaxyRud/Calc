import sys, numpy as np, cv2
from PIL import Image, ImageFilter
from scipy import ndimage as ndi
src, out_dir = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB"); W, H = im.size
a = np.asarray(im).copy()
hsv = np.asarray(im.convert("HSV")).astype(float) / 255.0
h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
yy, xx = np.mgrid[0:H, 0:W]
# 1) remove the printed logo on the slide plate (white text on pale green) by inpainting
plate = (xx > 330) & (xx < 475) & (yy > 168) & (yy < 262)
text = plate & (s < 0.16) & (v > 0.86)
text = ndi.binary_dilation(text, iterations=2)
a = cv2.inpaint(a, text.astype(np.uint8) * 255, 4, cv2.INPAINT_TELEA)
# 2) foreground mask: saturated & not too dark, or bright (pale highlights)
mask = ((s > 0.28) & (v > 0.16)) | (v > 0.55)
# remove background red light near the hammer (keep the barrel tip on the left)
red = ((h < 0.05) | (h > 0.93)) & (xx > 300)
mask &= ~red
mask = ndi.binary_opening(mask, iterations=1)
mask = ndi.binary_closing(mask, iterations=3)
lab, n = ndi.label(mask); sizes = ndi.sum(mask, lab, range(1, n + 1))
mask = lab == 1 + int(np.argmax(sizes))
# drop thin streaks of background light hanging off the silhouette
core = ndi.binary_opening(mask, structure=np.ones((3,3)), iterations=4)
cl, cn = ndi.label(core); cs = ndi.sum(core, cl, range(1, cn + 1))
core = cl == 1 + int(np.argmax(cs))
mask &= ndi.binary_dilation(core, structure=np.ones((3,3)), iterations=5) | (xx < 300)
holes = ndi.binary_fill_holes(mask) & ~mask
hl, hn = ndi.label(holes); hs = ndi.sum(holes, hl, range(1, hn + 1))
print("holes", sorted(int(x) for x in hs)[-6:])
for i, ar in enumerate(hs, 1):
    if ar < 2500: mask |= hl == i
alpha = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.9))
rgba = Image.fromarray(a); rgba.putalpha(alpha); rgba = rgba.crop(alpha.getbbox())
rgba = rgba.resize((rgba.width * 2, rgba.height * 2), Image.LANCZOS)
print(rgba.size)
rgba.save(f"{out_dir}/blaster.webp", quality=90, method=6)
rgba.save(f"{out_dir}/blaster.png")
bg1 = Image.new("RGBA", rgba.size, "white"); bg2 = Image.new("RGBA", rgba.size, (36, 160, 200, 255))
bg1.alpha_composite(rgba); bg2.alpha_composite(rgba)
c = Image.new("RGB", (rgba.width * 2 + 20, rgba.height), "black")
c.paste(bg1.convert("RGB"), (0, 0)); c.paste(bg2.convert("RGB"), (rgba.width + 20, 0))
c.save(f"{out_dir}/check2.png")
