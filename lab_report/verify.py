"""Independent re-check of every number in the final document.

Deliberately does NOT import analysis.py: different fitting code (scipy.stats.linregress and
numpy.polyfit), a Monte-Carlo test of the uncertainty propagation, and each quoted number
compared with the value the document states.
"""
import numpy as np
from scipy import stats
from data import TRIAL1, TRIAL2, TRIAL3
from data_x import TRIALS_X

FPS, TH, DTH, DY, GREF = 30.0, np.radians(3.5), np.radians(0.1), 0.002, 9.81
ok = lambda c: "OK " if c else "XX "
fails = 0
def check(label, got, claimed, tol):
    global fails
    good = abs(got - claimed) <= tol
    fails += (not good)
    print(f"  {ok(good)} {label:<55} recomputed {got:>10.4f}   document {claimed:>9}")

# ---- 1. data integrity (positions vs the sheet's velocity columns) ----
print("1. Transcription: recompute every velocity from positions and compare with the sheet")
for k, (ry, rx) in enumerate(zip([TRIAL1, TRIAL2, TRIAL3], TRIALS_X), 1):
    assert [r[0] for r in ry] == [r[0] for r in rx], "frame lists differ"
    by = bx = 0
    for (n0, y0, _), (n1, y1, vy), (_, x0, _), (_, x1, vx) in zip(ry, ry[1:], rx, rx[1:]):
        dt = (n1 - n0) / FPS
        by += abs((y1 - y0) / dt - vy) > 0.001 / dt + 0.006
        bx += abs((x1 - x0) / dt - vx) > 0.001 / dt + 0.006
    print(f"  {ok(by == 0 and bx == 0)} recording {k}: {len(ry)-1} intervals, vy mismatches {by}, vx mismatches {bx}")
    fails += (by + bx) > 0

def series(rows, use_mid=True):
    t = np.array([((n0 + n1) / 2 if use_mid else n1) / FPS for (n0, *_), (n1, *_) in zip(rows, rows[1:])])
    v = np.array([r[2] for r in rows[1:]])
    return t, v

# ---- 2. slopes with an independent fitting routine ----
print("\n2. Slopes and fit errors (scipy.stats.linregress, midpoint times)")
claimed_m = [(-0.613, 0.019), (-0.621, 0.018), (-0.606, 0.014)]
fits = []
for k, rows in enumerate([TRIAL1, TRIAL2, TRIAL3]):
    t, v = series(rows)
    lr = stats.linregress(t, v)
    p, cov = np.polyfit(t, v, 1, cov=True)              # second, different routine
    assert abs(p[0] - lr.slope) < 1e-12 and abs(np.sqrt(cov[0, 0]) - lr.stderr) < 1e-12
    fits.append((t, v, lr))
    check(f"recording {k+1} slope", lr.slope, claimed_m[k][0], 0.0005)
    check(f"recording {k+1} fit error", lr.stderr, claimed_m[k][1], 0.0005)
print("  (polyfit and linregress agree to 1e-12)")

print("\n   Cross-check against the group's own Excel trendlines (end-of-interval time, as in the sheet)")
for k, (rows, excel) in enumerate(zip([TRIAL1, TRIAL2, TRIAL3], [-0.6125, -0.6214, -0.6061])):
    t, v = series(rows, use_mid=False)
    check(f"recording {k+1} slope vs Excel chart", stats.linregress(t, v).slope, excel, 0.0005)

print("\n   Robustness: slopes recomputed from raw y (not the sheet's rounded vy column)")
for k, rows in enumerate([TRIAL1, TRIAL2, TRIAL3]):
    t = np.array([(r0[0] + r1[0]) / 2 / FPS for r0, r1 in zip(rows, rows[1:])])
    v = np.array([(r1[1] - r0[1]) / ((r1[0] - r0[0]) / FPS) for r0, r1 in zip(rows, rows[1:])])
    print(f"      recording {k+1}: {stats.linregress(t, v).slope:.4f}  (from sheet vy: {fits[k][2].slope:.4f})")

# ---- 3. g per recording ----
print("\n3. g = |a|/sin(theta) and sigma_g for each recording")
claimed_g = [(10.05, 0.43), (10.18, 0.42), (9.93, 0.37)]
gs, dgs = [], []
for k, (_, _, lr) in enumerate(fits):
    g = abs(lr.slope) / np.sin(TH)
    dg = g * np.hypot(lr.stderr / lr.slope, DTH / np.tan(TH))
    gs.append(g); dgs.append(dg)
    check(f"g{k+1}", g, claimed_g[k][0], 0.005)
    check(f"sigma_g{k+1}", dg, claimed_g[k][1], 0.005)
check("angle term dtheta/tan(theta) in %", 100 * DTH / np.tan(TH), 2.9, 0.05)

# ---- 4. combining ----
print("\n4. Combined slope, SEM and final g")
m = np.array([lr.slope for *_, lr in fits]); dm = np.array([lr.stderr for *_, lr in fits])
a = m.mean(); da = np.sqrt(np.sum(dm ** 2)) / 3; sem = m.std(ddof=1) / np.sqrt(3)
check("mean slope", a, -0.614, 0.0005)
check("propagated slope uncertainty", da, 0.010, 0.0005)
check("SEM of slopes", sem, 0.004, 0.0005)
g = abs(a) / np.sin(TH); dg = g * np.hypot(da / a, DTH / np.tan(TH))
check("final g", g, 10.05, 0.005)
check("final sigma_g (propagated)", dg, 0.33, 0.005)
check("SEM of the three g values", np.std(gs, ddof=1) / np.sqrt(3), 0.07, 0.005)
check("sigma_g if SEM used instead (+ angle)", g * np.hypot(sem / a, DTH / np.tan(TH)), 0.30, 0.005)
check("slope term in % (final)", 100 * da / abs(a), 1.6, 0.05)

print("\n   Monte-Carlo check of the propagation (shared angle, independent slopes, 200k draws)")
rng = np.random.default_rng(1)
th_s = rng.normal(TH, DTH, 200_000)
m_s = rng.normal(m[:, None], dm[:, None], (3, 200_000))
g_s = np.abs(m_s.mean(axis=0)) / np.sin(th_s)
check("Monte-Carlo mean of g (2nd-order shift ~0.008 expected)", g_s.mean(), 10.05, 0.02)
check("Monte-Carlo std of g", g_s.std(), 0.33, 0.01)
naive = np.sqrt(np.sum(np.square(dgs))) / 3
print(f"      (averaging g1..g3 as if the angle errors were independent would give +/-{naive:.2f}, i.e. too small)")

# ---- 5. every other number in the text ----
print("\n5. Other numbers quoted in the text")
pairs = {(i, j): (abs(m[i] - m[j]), np.hypot(dm[i], dm[j])) for i in range(3) for j in range(i + 1, 3)}
big = max(pairs, key=lambda k: pairs[k][0])
print(f"  {ok(big == (1, 2))} largest slope difference is between recordings {big[0]+1} and {big[1]+1}")
check("largest slope difference", pairs[big][0], 0.015, 0.0005)
check("their combined error", pairs[big][1], 0.023, 0.0005)
print(f"      all pairwise differences in units of combined error: "
      + ", ".join(f"{d/u:.2f}" for d, u in pairs.values()))
exp = GREF * np.sin(TH)
check("expected slope g sin(3.5 deg)", exp, 0.599, 0.0005)
z = [(abs(mi) - exp) / dmi for mi, dmi in zip(m, dm)]
print(f"  {ok(z[0] < 1 and z[2] < 1 and 1 < z[1] < 1.5)} slope vs expected (sigma): rec1 {z[0]:.2f}, rec2 {z[1]:.2f}, rec3 {z[2]:.2f}"
      "   -> text: 1 and 3 within error, 2 just outside")
check("error bar sqrt(2)*dy/dt", np.sqrt(2) * DY * FPS, 0.085, 0.0005)
inside = 0; total = 0
for rows, (t, v, lr) in zip([TRIAL1, TRIAL2, TRIAL3], fits):
    dts = np.array([(r1[0] - r0[0]) / FPS for r0, r1 in zip(rows, rows[1:])])
    inside += np.sum(np.abs(v - (lr.slope * t + lr.intercept)) <= np.sqrt(2) * DY / dts); total += len(t)
check("share of error bars touching the line (%)", 100 * inside / total, 60, 0.5)
apex = [lr.intercept / -lr.slope for *_, lr in fits]
print(f"  {ok(0.85 < min(apex) and max(apex) < 1.35)} apex times {', '.join(f'{x:.2f}' for x in apex)} s  -> text: t = 0.9-1.3 s")
check("final g minus 9.81", g - GREF, 0.24, 0.005)
check("difference in sigma", (g - GREF) / dg, 0.7, 0.05)
check("tilt that would give exactly 9.81 (deg)", np.degrees(np.arcsin(abs(a) / GREF)), 3.59, 0.005)
resid_sd = [np.std(v - (lr.slope * t + lr.intercept), ddof=2) for t, v, lr in fits]
print(f"  {ok(resid_sd[0] == max(resid_sd))} recording 1 scatters most: residual SD {', '.join(f'{s:.3f}' for s in resid_sd)} m/s")
r0 = fits[0][1][:3] - (fits[0][2].slope * fits[0][0][:3] + fits[0][2].intercept)
print(f"  {ok(np.all(r0 > 0))} recording 1 first three points above the line by {', '.join(f'{x:.2f}' for x in r0)} m/s")
for k, rows in enumerate([TRIAL1, TRIAL2, TRIAL3]):
    vs = [abs(r1[2]) for r0, r1 in zip(rows, rows[1:]) if r1[0] - r0[0] == 1]
    best = max([0.0578, 0.0347, 0.0283], key=lambda st: np.mean([abs(x / st - round(x / st)) < 0.06 for x in vs]))
    share = np.mean([abs(x / best - round(x / best)) < 0.06 for x in vs])
    print(f"      recording {k+1}: {share:.0%} of vy values are multiples of {best} m/s -> {1000 * best / FPS:.2f} mm per pixel")
print("\n6. Horizontal velocity (claim: roughly constant)")
for k, rows in enumerate(TRIALS_X):
    t, v = series(rows)
    lr = stats.linregress(t, v)
    print(f"      recording {k+1}: vx slope {lr.slope:+.4f} +/- {lr.stderr:.4f} m/s^2, mean vx {v.mean():.3f} m/s")

print(f"\nRESULT: {'all checks passed' if fails == 0 else f'{fails} check(s) failed'}")
