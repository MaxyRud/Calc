import numpy as np
from data import TRIALS, FPS

THETA_DEG, DTHETA_DEG = 3.5, 0.1     # table tilt and digital-level resolution
G_REF = 9.81
DY = 2.0e-3                           # position uncertainty per tracked point [m]


def velocity_points(rows):
    """(t_mid, vy, dt) for each consecutive pair, using the sheet's vy values."""
    out = []
    for (n0, _, _), (n1, _, vy) in zip(rows, rows[1:]):
        t0, t1 = n0 / FPS, n1 / FPS
        out.append((0.5 * (t0 + t1), vy, t1 - t0))
    return np.array(out).T


def linfit(t, v):
    """Unweighted least squares, same as Excel LINEST: slope, intercept and their SEs."""
    n = len(t)
    A = np.vstack([t, np.ones(n)]).T
    (m, c), *_ = np.linalg.lstsq(A, v, rcond=None)
    res = v - (m * t + c)
    s = np.sqrt(np.sum(res**2) / (n - 2))
    sxx = np.sum((t - t.mean())**2)
    return m, c, s / np.sqrt(sxx), s * np.sqrt(1 / n + t.mean()**2 / sxx), s


def g_from_slope(a, da):
    th, dth = np.radians(THETA_DEG), np.radians(DTHETA_DEG)
    g = abs(a) / np.sin(th)
    dg = g * np.sqrt((da / a)**2 + (dth / np.tan(th))**2)
    return g, dg


def analyse(verbose=True):
    results = {}
    for name, rows in TRIALS.items():
        t, v, dt = velocity_points(rows)
        m, c, dm, dc, s = linfit(t, v)
        ev = np.sqrt(2) * DY / dt
        inside = np.mean(np.abs(v - (m * t + c)) <= ev)
        g, dg = g_from_slope(m, dm)
        results[name] = dict(t=t, v=v, ev=ev, m=m, c=c, dm=dm, dc=dc, s=s, g=g, dg=dg,
                             inside=inside, n=len(t))
        if verbose:
            print(f"{name}: N={len(t)} slope={m:.4f}±{dm:.4f} (rel {abs(dm/m)*100:.1f}%) "
                  f"int={c:.4f}±{dc:.4f} resid_sd={s:.3f} errbar={ev[0]:.3f} "
                  f"inside={inside*100:.0f}% g={g:.2f}±{dg:.2f}")
    return results


if __name__ == "__main__":
    r = analyse()
    ms = np.array([x["m"] for x in r.values()])
    dms = np.array([x["dm"] for x in r.values()])
    a = ms.mean()
    da_prop = np.sqrt(np.sum(dms**2)) / 3
    da_sem = ms.std(ddof=1) / np.sqrt(3)
    print(f"\nmean slope {a:.4f}; propagated ±{da_prop:.4f}; SEM ±{da_sem:.4f}; spread(max-min) {ms.max()-ms.min():.4f}")
    # pairwise agreement
    names = list(r)
    for i in range(3):
        for j in range(i + 1, 3):
            d = abs(ms[i] - ms[j]); u = np.hypot(dms[i], dms[j])
            print(f"  {names[i]} vs {names[j]}: diff {d:.4f}, combined unc {u:.4f}, {d/u:.2f} sigma")
    th, dth = np.radians(THETA_DEG), np.radians(DTHETA_DEG)
    for label, da in [("propagated", da_prop), ("SEM", da_sem)]:
        g, dg = g_from_slope(a, da)
        rel_slope = da / abs(a); rel_ang = dth / np.tan(th)
        print(f"g ({label}) = {g:.3f} ± {dg:.3f}  [slope part {rel_slope*100:.2f}%, angle part {rel_ang*100:.2f}%]"
              f"  -> |g-9.81|/dg = {abs(g-G_REF)/dg:.2f}")
    gs = np.array([x["g"] for x in r.values()])
    print("mean of individual g:", gs.mean())
    print("angle needed for 9.81:", np.degrees(np.arcsin(abs(a) / G_REF)))
    # sensitivity: drop first 3 release points
    print("\nSensitivity, excluding first 3 velocity points (launch):")
    for name, x in r.items():
        m, c, dm, *_ = linfit(x["t"][3:], x["v"][3:])
        print(f"  {name}: slope {m:.4f}±{dm:.4f}")
    print("\nSensitivity, plotting vs t2 (spreadsheet time column):")
    for name, rows in TRIALS.items():
        t2 = np.array([n1 / FPS for (n1, _, _) in rows[1:]]); v = np.array([vy for (_, _, vy) in rows[1:]])
        m, c, dm, *_ = linfit(t2, v)
        print(f"  {name}: y = {m:.4f}x + {c:.4f}")
