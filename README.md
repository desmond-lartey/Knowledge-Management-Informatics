# From GeoAI to Planning Intelligence

**A Spatial Decision-Support Framework for Urban Governance**

[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://desmond-lartey.github.io/Knowledge-Management-Informatics/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This repository contains the complete, reproducible pipeline for the study *"From GeoAI to Planning Intelligence: A Spatial Decision-Support Framework for Urban Governance"* by Desmond Lartey and Kris M.Y. Law. It translates high-resolution aerial imagery into interpretable spatial diagnostics and planning recommendations that align with professional governance judgment.

The framework moves GeoAI beyond pixel-level classification toward governance-relevant decision support by integrating five stages into a single pipeline: semantic segmentation of the built environment, grid-based spatial aggregation, perceptual and functional indicator computation, composite index construction, and rule-based recommendation generation. Every stage is auditable, every indicator is disclosed, and every recommendation can be traced from input to output.

---

## What this framework does

Given aerial imagery and building footprint data for an urban area, the pipeline produces:

- A **U-Net segmentation model** that classifies built structures from NAIP aerial imagery, evaluated with standard metrics (IoU = 0.477, F1 = 0.646, Precision = 0.570, Recall = 0.746, Accuracy = 0.805 on held-out validation).
- A **100-metre spatial grid** in which each cell carries building coverage, vegetation coverage, and road density derived from the imagery and OpenStreetMap.
- Five **perceptual indicators** — greenness, openness, enclosure, walkability, imageability — computed as morphological proxies from overhead data.
- A **Perceptual Quality Index (PQI)** and a **Combined Urban Risk Index (CURI)** synthesising these indicators into composite diagnostics.
- **Rule-based planning recommendations** across four intervention categories, generated from transparent threshold logic.
- A **validation suite** producing expert face-validity statistics, inter-rater reliability, and indicator-weighting sensitivity analysis.

---

## Repository structure

```
Knowledge-Management-Informatics/
├── README.md                        ← this file
├── LICENSE
├── requirements.txt                 ← Python dependencies
├── CITATION.cff                     ← citation metadata
│
├── mkdocs.yml                       ← MkDocs Material site config
├── docs/                            ← documentation source (MkDocs Material)
│   ├── index.md                     ← documentation home
│   ├── methodology.md               ← full method with equations
│   ├── indicators.md                ← every indicator formula, disclosed
│   ├── recommendation-logic.md      ← the rule-based decision table
│   ├── validation.md                ← expert validation & reliability
│   ├── sensitivity.md               ← PQI weighting robustness
│   ├── reproducibility.md           ← step-by-step reproduction guide
│   └── javascripts/mathjax.js       ← equation rendering config
│
├── notebooks/
│   └── GeoAI_Urban_Planner_Pipeline.ipynb   ← full end-to-end pipeline
│
├── src/                            ← modular Python source
│   ├── segmentation.py              ← training, inference, evaluation
│   ├── spatial_aggregation.py       ← grid, coverage, road density
│   ├── indicators.py                ← perceptual indicators + indices
│   ├── recommendations.py           ← rule-based recommendation engine
│   ├── validation.py                ← expert pack generation + scoring
│   └── sensitivity.py               ← PQI weighting sensitivity analysis
│
├── data/
│   └── sample/                      ← small worked example (AL subset)
│
├── figures/                        ← publication figure scripts
│   ├── system_level_performance.py
│   ├── model_performance.py
│   ├── validation_figures.py
│   └── sensitivity_figures.py
│
└── validation/                     ← expert rating templates & outputs
    ├── expert_review_pack_20cells.csv
    └── INSTRUCTIONS.txt
```

---

## Quick start

```bash
# Clone
git clone https://github.com/desmond-lartey/Knowledge-Management-Informatics.git
cd Knowledge-Management-Informatics

# Install
pip install -r requirements.txt

# Run the pipeline (Colab recommended for GPU segmentation)
jupyter notebook notebooks/GeoAI_Urban_Planner_Pipeline.ipynb
```

The full documentation, including every equation, the recommendation logic table, and the reproduction guide, is available at:

**https://desmond-lartey.github.io/Knowledge-Management-Informatics/**

---

## Reproducing the study

The complete demonstration uses NAIP aerial imagery and Google-Microsoft Open Buildings footprint data for one urban area in Alabama (3,116 grid cells), with the segmentation model trained across a multi-state dataset of 2,175 image-label tile pairs. Data acquisition, model training, spatial aggregation, and validation are documented step by step in [`docs/reproducibility.md`](docs/reproducibility.md).

Heavy stages (tile generation, model training, inference) can be skipped if their outputs already exist, so the diagnostic and validation stages can be reproduced independently from the provided intermediate outputs.

---

## Citation

If you use this framework, please cite:

```bibtex
@article{lartey_geoai_planning_intelligence,
  title   = {From GeoAI to Planning Intelligence: A Spatial Decision-Support Framework for Urban Governance},
  author  = {Lartey, Desmond and Law, Kris M. Y.},
  year    = {2026},
  note    = {Manuscript under review}
}
```

See [`CITATION.cff`](CITATION.cff) for machine-readable citation metadata.

---

## Related work

This study is part of a research programme on artificial intelligence in urban governance:

- Lartey, D., & Law, K. M. Y. (2025). Artificial intelligence adoption in urban planning governance: A systematic review. *Landscape and Urban Planning*, 258, 105337.
- Lartey, D., & Law, K. M. Y. (2026). Governing with artificial intelligence: Mapping the knowledge systems shaping urban intelligence. *Technology in Society*, 86, 103321.

---

## License

Released under the MIT License. See [`LICENSE`](LICENSE) for details.

## Contact

Desmond Lartey — larteydesmond3@gmail.com
International School for Social and Business Studies (ISSBS), Celje, Slovenia
