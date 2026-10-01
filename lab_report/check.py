# Sanity check: recompute vy from transcribed y and compare to the spreadsheet vy.
from data import TRIALS, FPS
for name, rows in TRIALS.items():
    bad = 0
    for (n0, y0, _), (n1, y1, vy) in zip(rows, rows[1:]):
        dt = (n1 - n0) / FPS
        v = (y1 - y0) / dt
        # y is shown to 3 s.f., so allow ~1 mm of rounding over one interval
        if abs(v - vy) > 0.001 / dt + 0.006:
            bad += 1
            print(f"{name} frame {n1}: recomputed {v:.3f} vs sheet {vy:.3f}")
    print(name, "rows", len(rows), "velocities", len(rows) - 1, "mismatches", bad)
