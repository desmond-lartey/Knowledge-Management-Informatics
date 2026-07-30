"""
validation.py
=============
Expert validation pack generation and scoring.

Two operations:
  1. build_expert_packs — generate rating sheets, instructions, and
     qualification forms for N experts, sampling identical cells (fixed seed)
     so inter-rater reliability can be computed.
  2. score_validation — compute acceptance rates, category-level agreement,
     Krippendorff's alpha, and inter-rater Spearman correlations from
     completed rating sheets.

Paper results: 8 experts, 20 cells, 160 ratings, 81.9% acceptance,
mean 4.13, Krippendorff alpha = 0.252, mean pairwise Spearman rho = 0.264.
"""

import os
import numpy as np
import pandas as pd
from scipy.stats import spearmanr


RECOMMENDATION_SHORT = {
    "Improve connectivity; Pedestrian & cycling infrastructure": "Connectivity + Active travel",
    "Maintain & monitor": "Maintain / Monitor",
    "Green corridors; Walkability retrofit; Mixed-use densification": "Green + Walkability + Mixed-use",
    "Urban greening; Blue-green infrastructure": "Greening + Blue-green",
}

INSTRUCTIONS = """RATING INSTRUCTIONS
====================
You are reviewing AI-generated planning recommendations for 20 urban grid
cells derived from a GeoAI spatial diagnostic framework. Each cell is
100m x 100m.

Rate each recommendation on a 5-point Likert scale:
  1 = Strongly disagree - inappropriate or misleading for this cell
  2 = Disagree - unlikely to be useful in practice
  3 = Neutral - plausible but you have significant reservations
  4 = Agree - appropriate given the diagnostic evidence
  5 = Strongly agree - clearly appropriate and governance-relevant

If you select 3 (Neutral), please use the notes_optional column to explain
what additional context would change your assessment.
"""


def build_expert_packs(diagnostic_df, out_dir, experts, n_sample=20, seed=42):
    """
    Generate one folder per expert with an (empty) rating sheet, instructions,
    and a qualification form. The same `n_sample` cells are drawn for every
    expert using `seed`, enabling inter-rater reliability analysis.
    """
    os.makedirs(out_dir, exist_ok=True)
    df = diagnostic_df.copy()

    reco_col = next((c for c in df.columns if "recommend" in c.lower()), None)
    df["recommendation_short"] = (
        df[reco_col].map(lambda t: RECOMMENDATION_SHORT.get(str(t).strip(), str(t)))
        if reco_col else "None"
    )

    rng = np.random.default_rng(seed)
    idx = rng.choice(df.index.to_numpy(), size=min(n_sample, len(df)), replace=False)
    review = df.loc[idx].reset_index(drop=True)
    review["cell_id"] = np.arange(1, len(review) + 1)

    keep = ["cell_id", "recommendation_short"]
    for c in ["bld_coverage", "veg_coverage", "greenness",
              "road_density_km_per_km2", "walkability", "PQI",
              "combined_risk", "sprawl_score", "envdeg_score", "infra_deficiency"]:
        if c in review.columns:
            keep.append(c)
    pack = review[keep].copy()
    num_cols = [c for c in pack.columns if c not in ("cell_id", "recommendation_short")]
    pack[num_cols] = pack[num_cols].round(3)

    pack.to_csv(os.path.join(out_dir, "expert_review_pack_20cells.csv"), index=False)

    qual = pd.DataFrame([{"Field": f, "Response": ""} for f in [
        "Full name", "Professional title / role",
        "Years of experience in urban planning or related field",
        "Primary area of expertise", "Familiarity with AI-based planning tools",
        "Country / region of primary practice"]])

    for ex in experts:
        ex_dir = os.path.join(out_dir, ex)
        os.makedirs(ex_dir, exist_ok=True)
        sheet = pack.copy()
        sheet["likert_1to5"] = ""      # 1-5, expert completes
        sheet["notes_optional"] = ""    # required when likert = 3
        sheet.to_csv(os.path.join(ex_dir, f"ratings_{ex}.csv"), index=False)
        with open(os.path.join(ex_dir, "INSTRUCTIONS.txt"), "w") as f:
            f.write(INSTRUCTIONS)
        qual.to_csv(os.path.join(ex_dir, f"qualifications_{ex}.csv"), index=False)


def krippendorff_alpha_ordinal(matrix):
    """
    Ordinal Krippendorff's alpha.

    Parameters
    ----------
    matrix : ndarray [n_items x n_raters], np.nan for missing.

    Wraps the `krippendorff` package (level_of_measurement='ordinal'),
    which expects [n_raters x n_items], so the matrix is transposed here.
    """
    import krippendorff
    data = matrix.astype(float).copy()
    data[data == 0] = np.nan          # 0 is not a valid Likert value
    return krippendorff.alpha(reliability_data=data.T,
                              level_of_measurement="ordinal")


def score_validation(out_dir, experts):
    """
    Score completed expert rating sheets.

    Returns a dict of summary statistics and the pivoted rating matrix.
    """
    frames = []
    for ex in experts:
        path = os.path.join(out_dir, ex, f"ratings_{ex}.csv")
        if not os.path.exists(path):
            continue
        d = pd.read_csv(path)
        d["expert"] = ex
        frames.append(d)
    combined = pd.concat(frames, ignore_index=True)
    combined["likert_1to5"] = pd.to_numeric(combined["likert_1to5"], errors="coerce")

    def cat(s):
        return "Accepted" if s >= 4 else ("Neutral" if s == 3 else "Rejected")
    combined["acceptance"] = combined["likert_1to5"].apply(cat)
    pct = combined["acceptance"].value_counts(normalize=True) * 100

    pivot = combined.pivot_table(index="cell_id", columns="expert",
                                 values="likert_1to5")

    alpha = krippendorff_alpha_ordinal(pivot.to_numpy(dtype=float))

    experts_present = pivot.columns.tolist()
    rhos = []
    for i, e1 in enumerate(experts_present):
        for e2 in experts_present[i + 1:]:
            mask = ~(pivot[e1].isna() | pivot[e2].isna())
            if mask.sum() >= 3:
                rho, _ = spearmanr(pivot[e1][mask], pivot[e2][mask])
                rhos.append(rho)

    return {
        "total_ratings": len(combined),
        "experts": len(frames),
        "mean_rating": round(combined["likert_1to5"].mean(), 3),
        "accepted_pct": round(pct.get("Accepted", 0), 1),
        "neutral_pct": round(pct.get("Neutral", 0), 1),
        "rejected_pct": round(pct.get("Rejected", 0), 1),
        "krippendorff_alpha": round(alpha, 4),
        "mean_pairwise_spearman": round(float(np.mean(rhos)), 4) if rhos else None,
    }, pivot
