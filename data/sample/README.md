# Sample Data

This directory holds a small worked example so the diagnostic, validation,
and sensitivity stages can be run without acquiring the full national datasets.

Place here:
- `AL_urban_grid_results_sample.csv` — a subset of the Alabama diagnostic
  output (indicator columns + recommendations), sufficient to run:
  - `src/sensitivity.py`
  - `src/recommendations.py`
  - `figures/sensitivity_figures.py`

The full 3,116-cell diagnostic CSV and the segmentation model are regenerated
by running the pipeline notebook against NAIP imagery and Open Buildings data
(see docs/reproducibility.md for data sources).

Large binary assets (imagery .tif, model .pth) are intentionally excluded from
version control (see .gitignore) and should be obtained from the public data
sources documented in the reproducibility guide.
