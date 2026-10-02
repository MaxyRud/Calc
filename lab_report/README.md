# PHYS 1552 Experiment 1: data analysis exercise (Investigation II + Analysis III)

`PHYS1552_Exp1_data_analysis.pdf` is the submission. Page 1 has the figure and commentary, page 2 has the raw-data screenshot.

Rebuild it with:

    pip install matplotlib numpy reportlab pillow pypdf
    python3 make_figure.py && python3 build_pdf.py

- `data.py`: t/y/v_y transcribed from the group spreadsheet. `python3 check.py` re-derives every v_y from y and confirms it matches the sheet.
- `analysis.py`: least-squares fits, g per recording, and the combined g. Assumptions live at the top: θ = 3.5 ± 0.1°, δy = ±2 mm.
- `build_pdf.py`: all numbers in the text are computed, not typed. Put your name in `NAME`.
- `verify.py`: independent re-check of every number in the PDF (different fitting code, Monte-Carlo test of the uncertainty). Run `python3 verify.py`.
- `build_workings.py` builds `Uncertainty_workings.pdf`. It shows every uncertainty step with its numbers and the matching Excel formulas. It is a supporting document, not part of the 1-page submission.
- `results_table.py` builds Table 1 (`table1.png` / `table1.pdf`, ready to paste into a document). The same table appears on page 1 of the submission PDF.
