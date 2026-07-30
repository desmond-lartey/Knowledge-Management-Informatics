"""
sensitivity_figures.py
======================
PQI weighting sensitivity scatter plots.

Produces one scatter figure per alternative weighting scheme, showing
rank-order stability against the baseline PQI. Reads directly from the
diagnostic CSV — no dependency on other pipeline stages.
"""

import os
import pandas as pd
import numpy as np
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

# ── Update these two paths ────────────────────────────────────
DATA_PATH   = "AL_urban_grid_results.csv"
OUT_FIG_DIR = "figures_output"
os.makedirs(OUT_FIG_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
df["enclosure_inv"] = 1 - df["enclosure"]

schemes = {
    "Baseline\n(0.25/0.20/0.20/0.20/0.15)":
        dict(greenness=0.25, openness=0.20, enclosure_inv=0.20, walkability=0.20, imageability=0.15),
    "Equal weights\n(0.20 each)":
        dict(greenness=0.20, openness=0.20, enclosure_inv=0.20, walkability=0.20, imageability=0.20),
    "Greenness-dominant\n(0.40/0.15/0.15/0.15/0.15)":
        dict(greenness=0.40, openness=0.15, enclosure_inv=0.15, walkability=0.15, imageability=0.15),
    "Accessibility-dominant\n(0.15/0.15/0.15/0.40/0.15)":
        dict(greenness=0.15, openness=0.15, enclosure_inv=0.15, walkability=0.40, imageability=0.15),
}

pqi_df = pd.DataFrame({
    name: sum(df[c] * w for c, w in wts.items()).clip(0, 1).values
    for name, wts in schemes.items()
})
baseline = list(schemes.keys())[0]

results = []
for col in pqi_df.columns:
    rho, p = spearmanr(pqi_df[baseline], pqi_df[col])
    results.append({"scheme": col.replace("\n", " "), "rho": round(rho, 4)})
results_df = pd.DataFrame(results)

alt_schemes = [k for k in pqi_df.columns if k != baseline]
colors = ["#0A6FA8", "#B45C0A", "#6B2AA8"]

for alt, col in zip(alt_schemes, colors):
    fig, ax = plt.subplots(figsize=(7, 7), facecolor="white")
    ax.scatter(pqi_df[baseline], pqi_df[alt], alpha=0.30, s=18, color=col)
    ax.plot([0, 1], [0, 1], "k--", linewidth=1.2, alpha=0.5)
    rho = results_df.loc[results_df["scheme"] == alt.replace("\n", " "), "rho"].values[0]
    ax.set_title(f"rho = {rho:.4f}", fontsize=16, fontweight="bold", pad=12)
    ax.set_xlabel("Baseline PQI", fontsize=14)
    ax.set_ylabel(alt.replace("\n", " "), fontsize=13)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.suptitle("PQI Sensitivity: Rank-Order Stability", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout(pad=2.0)
    fname = alt.replace("\n", "_").replace(" ", "_").replace("/", "-")
    plt.savefig(os.path.join(OUT_FIG_DIR, f"sensitivity_{fname}.png"), dpi=300, bbox_inches="tight")
    plt.close()

print("Sensitivity figures saved.")
print(results_df.to_string(index=False))
