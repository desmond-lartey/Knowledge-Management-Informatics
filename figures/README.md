# Figure Scripts

Publication figure generation scripts. Each reads from the diagnostic output
CSVs and validation output folders and writes 300-dpi PNGs.

| Script | Produces |
|--------|----------|
| `model_performance.py` | Segmentation metrics chart (IoU, F1, precision, recall, accuracy) |
| `system_level_performance.py` | Recommendation distribution + indicator gradients across greenness / risk / PQI classes |
| `validation_figures.py` | Expert acceptance, category agreement, indicator profiles, inter-rater heatmap, cell variability |
| `sensitivity_figures.py` | PQI rank-order stability scatter plots across weighting schemes |

All scripts share a common publication palette:
- PQI / connectivity: `#0A6FA8` (teal)
- Maintain / walkability: `#2E8B57` (green)
- Greenness / greening: `#B45C0A` (amber)
- Risk: `#C0392B` (crimson)
- Integrated / accent: `#6B2AA8` (violet)

Update the `BASE_DIR` path at the top of each script to point to your data.
