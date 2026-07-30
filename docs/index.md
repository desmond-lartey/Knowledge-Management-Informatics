---
title: Home
---

# From GeoAI to Planning Intelligence

**A Spatial Decision-Support Framework for Urban Governance**

Desmond Lartey · Kris M.Y. Law

---

This is the documentation for the reproducible pipeline accompanying the study *"From GeoAI to Planning Intelligence: A Spatial Decision-Support Framework for Urban Governance."* It explains how the framework translates aerial imagery into interpretable spatial diagnostics and planning recommendations, discloses every indicator formula and decision rule, and provides a step-by-step guide to reproducing the results.

## The problem this framework addresses

Urban governance is increasingly mediated by artificial intelligence, yet a persistent gap separates what AI systems can compute from what planning institutions can actually use. Most Geographic AI applications stop at pixel-level classification — accurate at detecting buildings, roads, or vegetation, but producing outputs that planners cannot readily interpret, contest, or act upon. The result is a body of technically strong but governance-weak urban AI that rarely reaches the point of decision.

This framework closes that gap. It does not treat AI as an autonomous decision-maker, nor as a black box whose outputs must be trusted without scrutiny. Instead it structures AI outputs into a transparent chain of spatial diagnostics — every step of which a planner can follow, question, and adjust — that terminates in explicit, rule-based planning recommendations.

## What the framework produces

Starting from aerial imagery and building footprint data for an urban area, the pipeline generates a sequence of increasingly governance-relevant outputs:

**Segmentation.** A U-Net convolutional neural network classifies built structures from NAIP aerial imagery, producing binary building masks evaluated with standard performance metrics on a held-out validation set.

**Spatial aggregation.** Segmentation outputs are aggregated into a regular 100-metre grid. Each cell carries building coverage from the segmentation mask, vegetation coverage from the imagery, and road density from OpenStreetMap.

**Perceptual indicators.** Five morphological indicators — greenness, openness, enclosure, walkability, and imageability — are computed as overhead proxies for perceptual urban qualities, normalised for comparability across cells.

**Composite indices.** A Perceptual Quality Index synthesises the five perceptual indicators; a Combined Urban Risk Index synthesises sprawl, environmental degradation, and infrastructure deficiency into a single diagnostic of spatial concern.

**Recommendations.** A rule-based layer translates the diagnostic indices into planning recommendations across four intervention categories, using explicit thresholds disclosed in full.

**Validation.** Expert planners assess the recommendations for governance realism, and the framework's internal consistency and robustness are examined through correlation analysis and indicator-weighting sensitivity testing.

## How to use this documentation

If you want to understand **how the framework works**, start with [Methodology](methodology).

If you want the **exact formula for any indicator or index**, see [Indicators](indicators).

If you want to see **how recommendations are generated**, see [Recommendation Logic](recommendation-logic).

If you want to understand **how the framework was validated**, see [Validation](validation) and [Sensitivity Analysis](sensitivity).

If you want to **reproduce the results yourself**, follow [Reproducibility](reproducibility).

## Key results at a glance

| Component | Result |
|---|---|
| Segmentation IoU (building class) | 0.477 |
| Segmentation F1-score | 0.646 |
| PQI–risk internal consistency | Pearson r = −0.90 |
| Expert acceptance rate | 81.9% across 8 planners, 160 ratings |
| Inter-rater reliability | Krippendorff α = 0.252 |
| PQI weighting robustness | Spearman ρ = 0.856–0.980 |
| Study extent | 3,116 grid cells (Alabama demonstration) |
| Training data | 2,175 multi-state image-label tile pairs |

## Repository

The full source, notebook, and figure scripts are available at the [GitHub repository](https://github.com/desmond-lartey/Knowledge-Management-Informatics).
