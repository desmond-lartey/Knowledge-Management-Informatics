"""
recommendations.py
==================
Rule-based planning recommendation engine (paper Stage 5).

Translates the composite diagnostic indices into planning recommendations
across four intervention categories using an ordered decision cascade.

Every threshold is disclosed. Because the logic is rule-based rather than
learned, any recommendation can be traced to the exact indicator condition
that produced it — the mechanism through which the framework supports
transparency and accountability (see docs/recommendation-logic.md).
"""

import pandas as pd


# Recommendation category labels
GREEN_INTEGRATED = "Green corridors; Walkability retrofit; Mixed-use densification"
CONNECTIVITY     = "Improve connectivity; Pedestrian & cycling infrastructure"
GREENING         = "Urban greening; Blue-green infrastructure"
MAINTAIN         = "Maintain & monitor"


def recommend(row):
    """
    Assign a planning recommendation to a single grid cell.

    Decision cascade — first satisfied condition wins:
      1. High combined risk (>=0.6) AND low PQI (<0.4)  -> integrated
      2. Infrastructure deficiency (>0.5)               -> connectivity
      3. Environmental degradation (>0.6)               -> greening
      4. otherwise                                      -> maintain

    Ordering encodes a governance priority: the most troubled cells receive
    integrated interventions before single-dimension deficiencies are
    considered.
    """
    if row["combined_risk"] >= 0.6 and row["PQI"] < 0.4:
        return GREEN_INTEGRATED
    if row["infra_deficiency"] > 0.5:
        return CONNECTIVITY
    if row["envdeg_score"] > 0.6:
        return GREENING
    return MAINTAIN


def apply_recommendations(grid):
    """
    Apply the recommendation rule to every cell in a diagnostic grid.

    Requires columns: combined_risk, PQI, infra_deficiency, envdeg_score.
    Adds column: recommendations.
    """
    grid = grid.copy()
    grid["recommendations"] = grid.apply(recommend, axis=1)
    return grid


def recommendation_summary(grid):
    """Return a frequency table of recommendations across the grid."""
    return grid["recommendations"].value_counts().rename_axis(
        "recommendation").reset_index(name="count")
