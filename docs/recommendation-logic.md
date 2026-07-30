# Rule-Based Recommendation Logic

The recommendation layer translates diagnostic indices into planning guidance. It is deliberately **rule-based rather than learned**: every recommendation follows from explicit threshold conditions on the composite indices, so a planner can trace exactly which condition produced any given recommendation and contest it where local context warrants. This traceability is the mechanism through which the framework supports transparency and accountability.

## The decision cascade

The logic is evaluated as an ordered cascade — the first condition that a cell satisfies determines its recommendation. This ordering encodes a governance priority: cells with the most severe combined problems are addressed first with integrated interventions, before the framework considers single-dimension deficiencies.

| Priority | Condition | Recommendation |
|---|---|---|
| 1 | $CURI_i \geq 0.6$ **and** $PQI_i < 0.4$ | Green corridors; Walkability retrofit; Mixed-use densification |
| 2 | $\text{InfraDef}_i > 0.5$ | Improve connectivity; Pedestrian & cycling infrastructure |
| 3 | $\text{EnvDeg}_i > 0.6$ | Urban greening; Blue–green infrastructure |
| 4 | (otherwise) | Maintain & monitor |

## Rationale for each rule

**Priority 1 — Integrated intervention.** A cell with high combined risk ($CURI \geq 0.6$) and low perceptual quality ($PQI < 0.4$) has multiple intersecting problems: morphological, environmental, and infrastructural deficiencies co-occur. Single-dimension interventions would be insufficient, so the framework recommends an integrated package combining greening, walkability retrofitting, and mixed-use densification. This reflects contemporary planning theory emphasising multifunctional interventions for interconnected challenges.

**Priority 2 — Connectivity intervention.** A cell whose dominant problem is infrastructure deficiency ($\text{InfraDef} > 0.5$) — low road density combined with low walkability — needs improved network structure. The recommendation targets pedestrian and cycling infrastructure and street connectivity.

**Priority 3 — Greening intervention.** A cell whose dominant problem is environmental degradation ($\text{EnvDeg} > 0.6$) — low greenness — is matched with nature-based strategies: urban greening and blue-green infrastructure.

**Priority 4 — Maintain and monitor.** A cell that satisfies none of the above conditions is in a stable configuration. It requires only monitoring and incremental management, not active intervention.

## Why the cascade order matters

Because conditions are evaluated in priority order, a cell that satisfies both the integrated-intervention condition and the infrastructure-deficiency condition receives the integrated recommendation, not the connectivity one. This prevents the framework from under-prescribing for the most troubled cells. The ordering is a governance judgment encoded in the logic, and — like every threshold — it is disclosed here so that it can be scrutinised and, if a different governance context requires, recalibrated.

## Threshold calibration and transferability

The specific thresholds (0.6, 0.4, 0.5, 0.6) reflect the design judgment applied to the Alabama demonstration. They are not claimed to be universally optimal. Adapting the framework to a different governance context would involve recalibrating these thresholds in dialogue with local planning institutions and standards. This is a recognised limitation and a direction for future work — the contribution of the framework is the transparent architecture that connects diagnostics to recommendations, not the specific threshold values.

## Distribution of recommendations in the demonstration

Across the 3,116 Alabama grid cells, the recommendation distribution reflects the study area's characteristics: connectivity interventions dominate, indicating that the model most frequently identifies deficiencies in network structure and accessibility, while integrated and greening interventions emerge in more concentrated contexts. The full distribution is reported in the results and reproduced by the figure scripts in the repository.

## Reference implementation

```python
def recommend(row):
    if row["combined_risk"] >= 0.6 and row["PQI"] < 0.4:
        return "Green corridors; Walkability retrofit; Mixed-use densification"
    if row["infra_deficiency"] > 0.5:
        return "Improve connectivity; Pedestrian & cycling infrastructure"
    if row["envdeg_score"] > 0.6:
        return "Urban greening; Blue-green infrastructure"
    return "Maintain & monitor"
```

This exact function is used in the pipeline. Every recommendation in the study output can be reproduced by applying it to the diagnostic CSV.
