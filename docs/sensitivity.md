---
title: Sensitivity Analysis
---

# Sensitivity Analysis

The Perceptual Quality Index combines five indicators using a weighting scheme. Any weighted composite raises a legitimate question: does the result depend on the specific weights chosen, or would any reasonable weighting produce the same spatial pattern? This analysis answers that question directly.

## Design

Four weighting schemes were tested across all 3,116 grid cells. The baseline scheme is the one used throughout the study; the three alternatives represent distinct governance priorities a city might legitimately adopt.

| Scheme | Greenness | Openness | Enclosure (inv.) | Walkability | Imageability |
|---|---|---|---|---|---|
| **Baseline** | 0.25 | 0.20 | 0.20 | 0.20 | 0.15 |
| Equal weights | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 |
| Greenness-dominant | 0.40 | 0.15 | 0.15 | 0.15 | 0.15 |
| Accessibility-dominant | 0.15 | 0.15 | 0.15 | 0.40 | 0.15 |

For each alternative scheme, PQI was recomputed for every cell and its rank-order agreement with the baseline PQI measured using the Spearman rank correlation coefficient. Rank-order stability is the relevant test: it asks whether the same cells come out as high-quality and low-quality regardless of the weighting, which is what governance conclusions depend on.

## Results

| Scheme vs. baseline | Spearman ρ | p-value |
|---|---|---|
| Equal weights | 0.9804 | < 0.001 |
| Greenness-dominant | 0.9088 | < 0.001 |
| Accessibility-dominant | 0.8563 | < 0.001 |

All three alternative schemes produce very high rank-order agreement with the baseline. The interpretation is direct: even when the weighting is shifted substantially toward environmental or accessibility priorities, the same areas remain low-quality and the same areas remain high-quality. The framework's spatial diagnostic pattern is not an artifact of the specific weighting decision.

## Where divergence occurs

The greatest divergence appears under the accessibility-dominant scheme (ρ = 0.856), concentrated in cells with high road density but limited vegetation. This is expected and interpretable: walkability is the indicator most independent of the building-coverage-derived indicators, so elevating its weight shifts rankings most noticeably in cells where road density and vegetation diverge. The greenness-dominant scheme (ρ = 0.909) introduces moderate divergence in transitional cells where vegetation and built density are balanced.

That the divergence is both modest and interpretable strengthens rather than weakens the framework. It shows that alternative governance priorities produce coherent, predictable shifts — not chaotic reshuffling — which means a city adopting a different priority framework would still receive spatially sensible diagnostics.

## Why this matters for governance

Sensitivity robustness is directly relevant to the framework's governance role. Weighting choices in a composite index are, ultimately, value judgments — a city that prioritises environmental quality will weight greenness differently from one that prioritises accessibility. The finding that the spatial pattern is stable across reasonable weighting variations means that governance conclusions drawn from the framework are not hostage to a single contestable parameter choice. At the same time, the interpretable divergence under the accessibility-dominant scheme shows the framework remains responsive to genuine priority differences where they matter. Both properties are desirable in a decision-support tool intended for institutional use.

## Reproducing the analysis

The sensitivity analysis reads directly from the diagnostic output CSV (`AL_urban_grid_results.csv`) and requires no re-running of the segmentation or aggregation stages. The self-contained script is in `src/sensitivity.py` and `figures/sensitivity_figures.py`. See [Reproducibility](reproducibility).
