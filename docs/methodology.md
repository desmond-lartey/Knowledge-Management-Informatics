# Methodology

The framework is a five-stage pipeline. Each stage takes the output of the previous one and transforms it into a more governance-relevant form, moving from raw imagery to actionable planning guidance. This page describes each stage in the order the pipeline executes.

## Stage 1 — Data acquisition and study scope

The demonstration draws on two national data sources. High-resolution aerial imagery comes from the National Agriculture Imagery Program (NAIP), which acquires imagery during growing seasons at one-metre ground sample distance with horizontal accuracy within six metres of photo-identifiable control points. Building footprint data comes from the Google-Microsoft Open Buildings dataset, used as semantic labels for supervised segmentation.

Data acquisition was carried out for all contiguous US states to support model training across heterogeneous urban morphologies. The full spatial diagnostic pipeline — grid aggregation, indicator computation, index construction, recommendation generation, and expert validation — is demonstrated for one urban area in Alabama comprising 3,116 grid cells. Alabama was selected as a rapidly developing urban environment with heterogeneous land use, contrasting built-up density and vegetation, and active planning pressures suited to perception- and risk-oriented diagnostics.

This distinction matters: the **segmentation model** is trained on multi-state data, but the **diagnostic demonstration** is single-site. Transferability of specific indicator thresholds to other cities is a direction for future work, not a claim of the present study.

## Stage 2 — Semantic segmentation

Aerial imagery is paired with rasterised building footprints to create supervised training samples. Training tiles of 512×512 pixels are generated with a sliding window at a stride of 256 pixels, increasing sample diversity and reducing boundary artifacts.

A U-Net convolutional neural network with a ResNet-34 backbone pre-trained on ImageNet is trained for binary building segmentation across a multi-state dataset of 2,175 image-label tile pairs, split 80% training (1,740 tiles) and 20% validation (435 tiles). Training uses mini-batch gradient descent with a batch size of 8, a learning rate of 0.001, over 5 epochs.

During inference, images are processed in overlapping windows matching the training tile size, with overlapping predictions averaged to minimise edge effects. The model produces **binary building masks only** — distinguishing built structures from background. Road network data are obtained independently from OpenStreetMap via OSMnx; they are not a segmentation output.

Model performance on the held-out validation set:

| Metric | Value |
|---|---|
| Intersection over Union (IoU) | 0.477 |
| F1-score | 0.646 |
| Precision | 0.570 |
| Recall | 0.746 |
| Pixel Accuracy | 0.805 |

The higher recall relative to precision reflects a model that detects most building pixels at the cost of some false positives — appropriate for planning applications where missed buildings carry greater governance cost than over-detection. Downstream spatial aggregation at the 100-metre grid-cell scale stabilises building coverage estimates across approximately 10,000 pixels per cell, making composite indicators robust to tile-level segmentation noise.

## Stage 3 — Spatial aggregation

The study area is divided into a regular grid of 100 m × 100 m cells. This scale balances sensitivity to local urban morphology against computational feasibility, and aligns with neighbourhood-scale planning used in urban design and transport studies. Each grid cell becomes the aggregation unit for all downstream indicators.

Three primary measurements are extracted per cell:

- **Building coverage** — the proportion of pixels classified as built structures within the cell, from the segmentation mask.
- **Vegetation coverage** — the proportion of pixels exceeding an NDVI threshold of 0.2 (or an excess-green proxy where near-infrared bands are unavailable).
- **Road density** — the total length of drivable road segments intersecting the cell, normalised by cell area, computed in a metric (UTM) coordinate reference system.

Exact formulas are given in [Indicators](indicators.md).

## Stage 4 — Perceptual indicators and composite indices

Five perceptual indicators are derived from the three primary measurements. These are **morphological proxies computed from overhead imagery**, not direct measurements of lived human perception. The perception literature (Lynch, Ewing and Handy, Tuan) provides the conceptual vocabulary for interpreting morphological patterns in governance-relevant terms; the measurements themselves are grounded in overhead spatial data. This approach follows an established strand of GeoAI research using remotely sensed data to derive morphology-based proxies for perceptual qualities at scale.

The five indicators — greenness, openness, enclosure, walkability, imageability — are normalised via min-max scaling and combined into a **Perceptual Quality Index (PQI)**. A parallel set of risk indicators — sprawl, environmental degradation, infrastructure deficiency — is combined into a **Combined Urban Risk Index (CURI)**. Full formulas and weights are in [Indicators](indicators.md).

## Stage 5 — Rule-based recommendations

The composite indices feed a rule-based recommendation layer that translates diagnostic conditions into planning guidance across four intervention categories. The logic is a transparent decision cascade — high-risk low-quality cells receive integrated interventions, infrastructure-deficient cells receive connectivity interventions, environmentally degraded cells receive greening interventions, and stable cells are flagged for monitoring. The complete decision table is in [Recommendation Logic](recommendation-logic.md).

Because the logic is rule-based and every threshold is disclosed, a planner encountering any recommendation can trace exactly which indicator condition produced it, and can contest or adjust the recommendation if the local context warrants. This traceability is the mechanism through which the framework supports transparency and accountability: the reasoning from spatial evidence to planning output is fully visible, not hidden inside a learned model.

## Validation strategy

The framework is assessed along three dimensions, detailed in [Validation](validation.md) and [Sensitivity Analysis](sensitivity.md):

1. **Computational consistency** — correlation analysis confirming that the composite indices behave as designed.
2. **Expert face validity** — eight planning professionals assessing the governance realism of recommendations across 20 randomly sampled cells.
3. **Sensitivity** — testing whether the PQI spatial pattern is robust to alternative indicator weighting schemes.
