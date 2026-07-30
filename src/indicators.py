"""
indicators.py
=============
Perceptual indicators and composite indices (paper Stage 4).

The framework operates on three primary measurements — building coverage,
vegetation coverage, road density — from which five perceptual indicators and
two composite indices are derived. Every formula here corresponds exactly to
an equation in the paper and the docs/indicators.md page.

All indicators are computed per grid cell and normalised to [0, 1].
"""

import numpy as np
import pandas as pd


def minmax(x):
    """Min-max normalise a series to [0, 1]."""
    x = pd.Series(x).astype(float)
    return (x - x.min()) / (x.max() - x.min() + 1e-9)


def compute_perceptual_indicators(grid):
    """
    Compute the five perceptual indicators from primary measurements.

    Requires columns: bld_coverage, veg_coverage, road_density_km_per_km2.
    Adds columns: greenness, openness, enclosure, walkability, imageability.

    Indicators are morphological proxies derived from overhead imagery, not
    direct measures of lived perception (see docs/methodology.md).
    """
    grid = grid.copy()

    # Greenness = normalised vegetation coverage
    grid["greenness"] = minmax(grid["veg_coverage"])

    # Openness = inverse building coverage
    grid["openness"] = (1 - grid["bld_coverage"]).clip(0, 1)

    # Enclosure = building coverage
    grid["enclosure"] = grid["bld_coverage"].clip(0, 1)

    # Walkability = normalised road density x inverse normalised enclosure
    grid["walkability"] = (
        minmax(grid["road_density_km_per_km2"])
        * (1 - minmax(grid["enclosure"]))
    ).clip(0, 1)

    # Imageability = normalised sqrt of building coverage
    grid["imageability"] = minmax(np.sqrt(grid["bld_coverage"].clip(0, 1)))

    return grid


def compute_pqi(grid, weights=(0.25, 0.20, 0.20, 0.20, 0.15)):
    """
    Perceptual Quality Index — weighted linear combination of the five
    perceptual indicators.

    Default weights (greenness, openness, enclosure-inverse, walkability,
    imageability) are the paper baseline. Robustness of the spatial pattern
    to alternative weights is examined in sensitivity.py.
    """
    grid = grid.copy()
    wg, wo, we, ww, wi = weights
    grid["PQI"] = (
        wg * grid["greenness"]
        + wo * grid["openness"]
        + we * (1 - grid["enclosure"])
        + ww * grid["walkability"]
        + wi * grid["imageability"]
    ).clip(0, 1)
    return grid


def compute_risk_indicators(grid, weights=(0.4, 0.3, 0.3)):
    """
    Risk indicators and the Combined Urban Risk Index (CURI).

    Requires PQI, greenness, road_density_km_per_km2, walkability.
    Adds: sprawl_score, envdeg_score, infra_deficiency, combined_risk.

    Default CURI weights (sprawl, environmental degradation, infrastructure
    deficiency) are the paper baseline.
    """
    grid = grid.copy()
    grid["sprawl_score"] = (1 - grid["PQI"]).clip(0, 1)
    grid["envdeg_score"] = (1 - grid["greenness"]).clip(0, 1)
    grid["infra_deficiency"] = (
        (1 - minmax(grid["road_density_km_per_km2"]))
        * (1 - grid["walkability"])
    ).clip(0, 1)

    ws, wd, wi = weights
    grid["combined_risk"] = (
        ws * grid["sprawl_score"]
        + wd * grid["envdeg_score"]
        + wi * grid["infra_deficiency"]
    ).clip(0, 1)
    return grid


def compute_all(grid):
    """
    Full indicator pipeline: perceptual indicators -> PQI -> risk -> CURI.

    Convenience wrapper applying the three functions in order.
    """
    grid = compute_perceptual_indicators(grid)
    grid = compute_pqi(grid)
    grid = compute_risk_indicators(grid)
    return grid
