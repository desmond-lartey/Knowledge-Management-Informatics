"""
sensitivity.py
==============
PQI weighting sensitivity analysis.

Tests whether the spatial diagnostic pattern of the Perceptual Quality Index
is robust to the choice of indicator weights. Reads directly from the
diagnostic output CSV — no re-running of segmentation or aggregation needed.

Reported result: Spearman rho = 0.856-0.980 across alternative weighting
schemes relative to baseline (all 3,116 cells, p < 0.001).
"""

import pandas as pd
import numpy as np
from scipy.stats import spearmanr


# Weighting schemes: (greenness, openness, enclosure_inv, walkability, imageability)
SCHEMES = {
    "Baseline (0.25/0.20/0.20/0.20/0.15)":
        dict(greenness=0.25, openness=0.20, enclosure_inv=0.20,
             walkability=0.20, imageability=0.15),
    "Equal weights (0.20 each)":
        dict(greenness=0.20, openness=0.20, enclosure_inv=0.20,
             walkability=0.20, imageability=0.20),
    "Greenness-dominant (0.40/0.15/0.15/0.15/0.15)":
        dict(greenness=0.40, openness=0.15, enclosure_inv=0.15,
             walkability=0.15, imageability=0.15),
    "Accessibility-dominant (0.15/0.15/0.15/0.40/0.15)":
        dict(greenness=0.15, openness=0.15, enclosure_inv=0.15,
             walkability=0.40, imageability=0.15),
}


def run_sensitivity(csv_path):
    """
    Compute PQI under each weighting scheme and report Spearman rank
    correlations against the baseline.

    Parameters
    ----------
    csv_path : str
        Path to diagnostic CSV containing the five perceptual indicator
        columns (greenness, openness, enclosure, walkability, imageability).

    Returns
    -------
    results_df : DataFrame with columns [Weight scheme, Spearman rho, p-value]
    pqi_df     : DataFrame of PQI scores under each scheme (one column each)
    """
    df = pd.read_csv(csv_path)

    required = ["greenness", "openness", "enclosure", "walkability", "imageability"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df["enclosure_inv"] = 1 - df["enclosure"]

    pqi_scores = {}
    for name, weights in SCHEMES.items():
        pqi = sum(df[col] * w for col, w in weights.items())
        pqi_scores[name] = pqi.clip(0, 1).values
    pqi_df = pd.DataFrame(pqi_scores)

    baseline = list(SCHEMES.keys())[0]
    rows = []
    for col in pqi_df.columns:
        rho, pval = spearmanr(pqi_df[baseline], pqi_df[col])
        rows.append({
            "Weight scheme": col,
            "Spearman rho vs baseline": round(rho, 4),
            "p-value": pval,
        })
    results_df = pd.DataFrame(rows)
    return results_df, pqi_df


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "AL_urban_grid_results.csv"
    results, _ = run_sensitivity(path)
    print(results.to_string(index=False))
