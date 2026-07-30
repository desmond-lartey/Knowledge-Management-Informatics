---
title: Reproducibility
---

# Reproducibility Guide

This guide reproduces the study end to end. The pipeline is organised so that the computationally heavy stages (tile generation, model training, inference) can be skipped if their outputs already exist, allowing the diagnostic, validation, and sensitivity stages to be reproduced independently.

## Environment

The pipeline was developed and run in Google Colab, which provides GPU acceleration for the segmentation stage. It also runs locally with the dependencies in `requirements.txt`.

```bash
pip install -r requirements.txt
```

Core dependencies: `geoai-py`, `osmnx`, `rasterio`, `geopandas`, `shapely`, `scikit-image`, `numpy`, `pandas`, `matplotlib`, `seaborn`, `scipy`, `krippendorff`, `leafmap`.

## Google Drive folder structure

The notebook expects the following structure. NAIP imagery and building footprints must be supplied by the user (see Data sources below); all other folders are created by the pipeline.

```
MyDrive/
├── NAIP_50_STATES/          NAIP_{STATE}.tif
├── BUILDINGS_50_STATES/     buildings_{STATE}.geojson
└── planner/
    ├── training_tiles/      created by tile generation
    ├── unet_models/         best_model.pth saved here
    ├── predictions/         building masks
    ├── analysis_outputs/    grid GeoJSONs
    ├── analysis_csv/        diagnostic CSVs
    ├── analysis_rasters/    PQI + risk rasters
    └── validation_outputs/  expert packs + results
```

## Pipeline stages

The notebook `notebooks/GeoAI_Urban_Planner_Pipeline.ipynb` is organised into twelve steps. Each has a markdown header explaining what it does and when it can be skipped.

| Step | Action | Skip if |
|---|---|---|
| 0 | Install packages, mount Drive | Drive already mounted |
| 1 | Discover states with both imagery and buildings | — |
| 2 | Set up training tile folders | Folders exist |
| 3 | Generate 512×512 training tiles (stride 256) | Tiles exist in Drive |
| 4 | Merge per-state tiles into global training set | Merged folders exist |
| 5 | Train U-Net (ResNet-34, 5 epochs) | `best_model.pth` exists |
| 6 | Evaluate model (IoU, F1, precision, recall) | Metrics CSV exists |
| 7 | Run inference → building masks | Prediction `.tif`s exist |
| 8 | Spatial aggregation → grid, coverage, road density | `_grid.geojson` exists |
| 9 | Diagnostics → indicators, PQI, risk, recommendations, map | Run per state |
| 10 | Internal construct validation (correlation matrices) | After Step 9 |
| 11 | Expert validation pack (8 experts, 20 cells) | After Step 9 |
| 12 | Download validation outputs | After Step 11 |

## Reproducing individual results

Because intermediate outputs are saved, most results can be reproduced without re-running the whole pipeline.

**Model performance metrics** (IoU, F1, precision, recall, accuracy) — requires `best_model.pth` and the validation tiles. Run Step 6. The evaluation computes metrics on the same 20% held-out validation split used in training (fixed seed).

**Spatial diagnostics** (PQI, risk, recommendations) — requires the per-state grid GeoJSON from Step 8. Run Step 9 for any state by setting `VIS_STATE`.

**Correlation matrices** (computational consistency) — requires only the diagnostic CSV `AL_urban_grid_results.csv`. Run Step 10 or `figures/validation_figures.py`.

**Sensitivity analysis** — requires only `AL_urban_grid_results.csv`. Run `src/sensitivity.py`. No segmentation or aggregation needed.

**Expert validation statistics** — requires the completed expert rating sheets. Place returned sheets in their `validation_outputs/Expert_X/` folders and run the scoring code, which computes acceptance rates, category-level agreement, Krippendorff's alpha, and inter-rater Spearman correlations.

## Data sources

The framework uses two public data sources that users must acquire for their own study area:

- **NAIP aerial imagery** — US Department of Agriculture, available via Google Earth Engine, USGS EarthExplorer, or the NAIP AWS bucket. One-metre resolution, RGB or RGBN.
- **Building footprints** — Google-Microsoft Open Buildings dataset, available via Source Cooperative and Google Earth Engine.

Road networks are retrieved automatically at runtime from OpenStreetMap via OSMnx; no manual download is required.

A small worked example for a subset of the Alabama study area is provided in `data/sample/` so that the diagnostic, validation, and sensitivity stages can be run without acquiring the full national datasets.

## Determinism and seeds

All stochastic steps use fixed seeds for reproducibility:

- Validation tile split: `np.random.seed(42)`
- Expert cell sampling: `np.random.default_rng(42)`

The same 20 cells are therefore sampled for expert review on every run, and the same validation tiles are used for model evaluation, ensuring reported metrics are exactly reproducible.

## Expected runtime

| Stage | Approx. time (Colab) |
|---|---|
| Tile generation (multi-state) | 30–90 min |
| Model training (5 epochs) | 20–60 min (GPU) |
| Inference (per state) | 5–20 min |
| Spatial aggregation (per state) | 10–30 min |
| Diagnostics + validation | < 5 min |
| Sensitivity analysis | < 1 min |

The diagnostic, validation, and sensitivity stages together run in under ten minutes from saved intermediate outputs, making the governance-relevant results fully reproducible without repeating the expensive earlier stages.
