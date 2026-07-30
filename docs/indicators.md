---
title: Indicators
---

# Indicators and Composite Indices

This page discloses every formula used in the framework. Each indicator is computed per grid cell $i$. The framework operates on **three primary measurements** — building coverage, vegetation coverage, and road density — from which five perceptual indicators and two composite indices are derived. This structure is deliberate: the five indicators make three measurements interpretable in planning-relevant terms, rather than representing five independent constructs.

## Primary measurements

### Building coverage

The proportion of pixels classified as built structures within a cell:

$$BC_i = \frac{\sum_{p \in G_i} \mathbf{1}[\hat{y}_p = 1]}{|G_i|}$$

where $G_i$ is the set of pixels in cell $i$, $\hat{y}_p = 1$ denotes a pixel classified as building by the segmentation model, and $|G_i|$ is the total pixel count of the cell.

### Vegetation coverage

Derived from the Normalised Difference Vegetation Index (NDVI):

$$VC_i = \frac{1}{|G_i|} \sum_{p \in G_i} \mathbf{1}\!\left[\frac{NIR_p - R_p}{NIR_p + R_p} > 0.2\right]$$

where $NIR_p$ and $R_p$ are the near-infrared and red band values at pixel $p$. Where near-infrared bands are unavailable, an excess-green proxy is used instead.

### Road density

The total length of drivable road segments intersecting a cell, normalised by cell area:

$$RD_i = \frac{\sum_{e \in E_i} l_e}{A_i}$$

where $E_i$ is the set of road segments (from OpenStreetMap) intersecting cell $i$, $l_e$ is the length of segment $e$ clipped to the cell, and $A_i$ is the cell area in km². Road density is expressed in km/km² and computed in a metric (UTM) coordinate reference system.

## Normalisation

All raw indicators are min-max normalised before compositing, ensuring comparability across cells and preventing any single indicator from dominating an index:

$$\tilde{x}_i = \frac{x_i - \min(x)}{\max(x) - \min(x)}$$

## Perceptual indicators

The five perceptual indicators are morphological proxies. Each is derived from the primary measurements above.

### Greenness

$$G_i = \widetilde{VC}_i$$

Greenness is the normalised vegetation coverage — a proxy for the environmental greenness conditions the perception literature associates with urban quality.

### Openness

$$O_i = 1 - BC_i$$

Openness is inverse building coverage — a morphological proxy for visual permeability and freedom from built-form obstruction.

### Enclosure

$$E_i = BC_i$$

Enclosure is building coverage — a proxy for the degree to which space is bounded by structures.

### Walkability

$$W_i = \widetilde{RD}_i \times (1 - \widetilde{E}_i)$$

Walkability combines normalised road density with inverse normalised enclosure — a network- and morphology-based proxy for how the spatial form supports pedestrian movement.

### Imageability

$$Im_i = \widetilde{\sqrt{BC_i}}$$

Imageability is the normalised square root of building coverage — a proxy for the built intensity and spatial presence that create morphological distinctiveness.

## Perceptual Quality Index (PQI)

The five perceptual indicators are combined into a single composite via weighted linear aggregation:

$$PQI_i = 0.25\,G_i + 0.20\,O_i + 0.20\,(1 - E_i) + 0.20\,W_i + 0.15\,Im_i$$

$PQI_i \in [0, 1]$, with higher values indicating more favourable urban morphological conditions. The weighting scheme is examined for robustness in [Sensitivity Analysis](sensitivity), where the spatial pattern is shown to be stable (Spearman ρ = 0.856–0.980) across alternative weightings.

## Risk indicators

Three risk indicators quantify conditions relevant for planning intervention.

### Sprawl score

$$\text{Sprawl}_i = 1 - PQI_i$$

### Environmental degradation

$$\text{EnvDeg}_i = 1 - G_i$$

### Infrastructure deficiency

$$\text{InfraDef}_i = (1 - \widetilde{RD}_i) \times (1 - W_i)$$

## Combined Urban Risk Index (CURI)

The three risk indicators are combined into a single composite:

$$CURI_i = 0.4\,\text{Sprawl}_i + 0.3\,\text{EnvDeg}_i + 0.3\,\text{InfraDef}_i$$

$CURI_i \in [0, 1]$, with higher values indicating greater concentration of planning-relevant urban problems.

## A note on internal consistency

Because several indicators are algebraic transformations of a small number of underlying measurements (openness, enclosure, and imageability all derive from building coverage; greenness derives from vegetation coverage), strong correlations among them confirm the framework's computational design rather than providing independent construct validity. The correlation analysis in [Validation](validation) is therefore reported as a **computational consistency assessment**, not as construct validation. The framework's practical value rests on expert face validity and sensitivity robustness, both documented in the validation pages.

## Summary table

| Indicator | Symbol | Derived from | Computation |
|---|---|---|---|
| Building coverage | $BC$ | Segmentation mask | Proportion of building pixels |
| Vegetation coverage | $VC$ | NAIP imagery | Proportion of NDVI > 0.2 |
| Road density | $RD$ | OpenStreetMap | Road length / cell area |
| Greenness | $G$ | $VC$ | Min-max normalised |
| Openness | $O$ | $BC$ | $1 - BC$ |
| Enclosure | $E$ | $BC$ | $BC$ |
| Walkability | $W$ | $RD$, $E$ | $\widetilde{RD} \times (1 - \widetilde{E})$ |
| Imageability | $Im$ | $BC$ | $\widetilde{\sqrt{BC}}$ |
| Perceptual Quality Index | $PQI$ | All perceptual | Weighted aggregation |
| Sprawl | — | $PQI$ | $1 - PQI$ |
| Environmental degradation | — | $G$ | $1 - G$ |
| Infrastructure deficiency | — | $RD$, $W$ | $(1-\widetilde{RD})(1-W)$ |
| Combined Urban Risk Index | $CURI$ | All risk | Weighted aggregation |
