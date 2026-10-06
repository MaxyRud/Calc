# Remove an embroidered brand logo + wordmark from a plush photo, keeping the face and other text.
# boxes: [x0,y0,x1,y1,threshold,mode,dilate]; mode "shape" fills an outlined logo (closed outline + interior,
# rebuilt from the surrounding fabric shading), mode "text" removes dark strokes with TELEA inpainting.
# usage: python3 debrand.py <src> <out.png> '<boxes json>' '<keep boxes json>'
import sys, json, numpy as np, cv2
from PIL import Image
from scipy import ndimage as ndi
src, out, boxes, keep = sys.argv[1], sys.argv[2], json.loads(sys.argv[3]), json.loads(sys.argv[4])
rgb = np.asarray(Image.open(src).convert("RGB")).copy()
img = rgb.astype(float); g = img.mean(-1); H, W = g.shape
bg = ndi.median_filter(g, size=41)
BODY = None
if len(sys.argv) > 5:                      # fabric threshold: pixels brighter than this (plus enclosed marks) are plush
    t = float(sys.argv[5]); BODY = ndi.binary_fill_holes(ndi.binary_closing(ndi.binary_opening(g > t, iterations=2), iterations=6))
    Image.fromarray((BODY * 255).astype(np.uint8)).save(out.replace('.png', '_body.png'))
keepm = np.zeros((H, W), bool)
for (x0, y0, x1, y1) in keep: keepm[y0:y1, x0:x1] = True
res = img.copy(); total = np.zeros((H, W), bool)
rng = np.random.default_rng(7)
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import spsolve
def laplace_fill(src_img, m, B=None):
    """Smooth membrane fill: solve Laplace's equation inside m with the surrounding pixels as boundary."""
    ys, xs = np.nonzero(m); n = len(ys); idx = -np.ones(m.shape, int); idx[ys, xs] = np.arange(n)
    A = lil_matrix((n, n)); b = np.zeros((n, 3))
    for k, (y, x) in enumerate(zip(ys, xs)):
        deg = 0
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if not (0 <= yy < m.shape[0] and 0 <= xx < m.shape[1]): continue
            if idx[yy, xx] >= 0: A[k, idx[yy, xx]] = -1; deg += 1
            elif B is None or B[yy, xx]: b[k] += src_img[yy, xx]; deg += 1
        A[k, k] = max(deg, 1)
    A = csr_matrix(A); out = src_img.copy()
    for c in range(3): out[ys, xs, c] = spsolve(A, b[:, c])
    return out
fine = ndi.gaussian_filter(rng.normal(0, 1, (H, W)), 1.0); fine /= fine.std()
mid = ndi.gaussian_filter(rng.normal(0, 1, (H, W)), 4.0); mid /= mid.std()
for (x0, y0, x1, y1, thr, mode, dil) in boxes:
    m = np.zeros((H, W), bool)
    gc = np.clip(res, 0, 255).mean(-1); sub = gc[y0:y1, x0:x1] < bg[y0:y1, x0:x1] - thr
    if mode == "shape":
        sub = ndi.binary_fill_holes(ndi.binary_closing(sub, iterations=5))
    if mode == "rect":                      # whole box with rounded corners
        yy, xx = np.mgrid[0:y1 - y0, 0:x1 - x0]; r = min(28, (x1 - x0) // 3)
        cx = np.clip(xx, r, x1 - x0 - r); cy = np.clip(yy, r, y1 - y0 - r)
        sub = (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r
    m[y0:y1, x0:x1] = sub
    m = ndi.binary_closing(m, iterations=2)
    if dil > 0: m = ndi.binary_dilation(m, iterations=dil)
    m &= ~keepm
    if mode in ("shape", "rect"):
        if BODY is not None: m &= BODY
        fill = laplace_fill(res, m, BODY) + (fine * 1.3 + mid * 2.2)[..., None]
    else:
        fill = cv2.inpaint(np.clip(res, 0, 255).astype(np.uint8), m.astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA).astype(float)
        fill = np.stack([ndi.gaussian_filter(fill[..., c], 1.6) for c in range(3)], -1) + (fine * 1.4 + mid * 1.2)[..., None]
    a = ndi.gaussian_filter(m.astype(float), 3.0 if mode == 'rect' else 1.5)[..., None]
    res = res * (1 - a) + fill * a
    total |= m
Image.fromarray(np.clip(res, 0, 255).astype(np.uint8)).save(out)
print("masked px", int(total.sum()))
