---
title: Validation
---

# Validation

The framework is validated along two independent dimensions: **computational consistency** — whether the composite indices behave as designed — and **expert face validity** — whether the resulting recommendations align with professional planning judgment. A third dimension, robustness to indicator weighting, is documented separately in [Sensitivity Analysis](sensitivity).

## Computational consistency assessment

This assessment verifies that the diagnostic indicators and composite indices behave consistently with their computational design. It is **not** an independent construct validation: several indicators are algebraic transformations of a small number of underlying measurements, so strong correlations among them reflect mathematical structure rather than independent empirical evidence. Reporting this transparently is itself part of the framework's commitment to auditability.

The Pearson and Spearman correlation matrices across all 3,116 grid cells confirm the intended relationships:

| Relationship | Pearson r | Spearman ρ | Interpretation |
|---|---|---|---|
| Building coverage ↔ Enclosure | ≈ 1.00 | ≈ 1.00 | Enclosure operationalised from building density |
| Vegetation coverage ↔ Greenness | ≈ 1.00 | ≈ 1.00 | Greenness derived from vegetative cover |
| Road density ↔ Walkability | 0.98–0.99 | 0.98–0.99 | Walkability incorporates road density |
| Greenness ↔ Environmental degradation | ≈ −1.00 | ≈ −1.00 | Complementary construct by definition |
| **PQI ↔ Combined Risk Index** | **−0.90** | **−0.91** | Risk declines as perceptual quality improves |

The strong negative PQI–risk relationship is the most substantively meaningful result. It confirms that the integrated risk metric consistently declines as perceptual and environmental quality improve, demonstrating that the framework's composite indices behave in a theoretically consistent and non-contradictory manner. Because several risk indicators are constructed partly as inverses of PQI components, this relationship is partly structural by design — it is reported as evidence of internal coherence, not as independent confirmation of validity.

## Expert face validity assessment

Eight planning professionals independently evaluated 20 grid cells randomly sampled from the full Alabama diagnostic dataset. Sampling used a fixed random seed (42) so that all eight experts assessed identical cells, enabling inter-rater reliability analysis.

### Design

Each expert received a standardised rating package: the sampled cells with their full indicator profiles and model-generated recommendations, written rating instructions defining a five-point Likert scale, category-level guidance for each recommendation type, and a professional qualification form. Experts rated whether each recommendation was appropriate given the diagnostic conditions of its cell:

- **1** — Strongly disagree (recommendation inappropriate or misleading)
- **2** — Disagree (unlikely to be useful in practice)
- **3** — Neutral (plausible but with significant reservations)
- **4** — Agree (appropriate given the diagnostic evidence)
- **5** — Strongly agree (clearly appropriate and governance-relevant)

Experts selecting a neutral rating were asked to document their reservations, enabling qualitative analysis of where and why disagreement arises. Ratings of 4–5 were classified as accepted, 3 as neutral, and 1–2 as rejected.

### Overall acceptance

Across 160 ratings (8 experts × 20 cells):

| Outcome | Proportion |
|---|---|
| Accepted (Likert ≥ 4) | 81.9% |
| Neutral (Likert = 3) | 15.0% |
| Rejected (Likert ≤ 2) | 3.1% |
| Mean rating | 4.13 |

This acceptance rate confirms that the framework's recommendation logic is broadly aligned with professional planning judgment.

### Category-level agreement

Acceptance varied systematically across recommendation categories. Connectivity and active-travel interventions received the highest and most consistent endorsement, particularly in cells with low walkability and high infrastructure deficiency where the diagnostic rationale is clearest. Maintain-and-monitor recommendations showed the greatest variation, with neutral responses concentrated in cells of moderate risk where intervention urgency is genuinely ambiguous. The single integrated recommendation — cell 10, the sample's highest-risk and lowest-quality cell — received unanimous strong agreement from all eight experts (mean = 5.0, SD = 0.0), confirming that where diagnostic evidence is unambiguous, expert consensus follows.

### Inter-rater reliability

Inter-rater reliability was assessed using Krippendorff's alpha on ordinal ratings across all eight experts:

| Measure | Value |
|---|---|
| Krippendorff α (ordinal) | 0.252 |
| Mean pairwise Spearman ρ | 0.264 |

These values reflect low but non-trivial agreement, consistent with the inherently context-dependent nature of planning judgment. The reliability figures are reported transparently rather than smoothed over. Critically, disagreement is **systematic rather than random** — it concentrates in two identifiable cell types:

1. **High-greenness, zero-road-density cells**, where experts differ on whether the spatial profile indicates a connectivity deficiency requiring intervention or periurban open space outside the intervention logic.
2. **Borderline maintain cases**, where combined risk falls close to the intervention threshold and professional judgment is genuinely divided.

This clustering is analytically important. It identifies precisely the spatial conditions where AI-generated recommendations require the greatest professional scrutiny — which is exactly the governance role the framework is designed to support. The framework structures deliberation in ambiguous cases rather than replacing it. The low inter-rater agreement in these cases is therefore consistent with, not contradictory to, the framework's governance design logic.

## Diagnostic coherence

Indicator profiles of expert-reviewed cells grouped by recommendation category confirm that the framework assigns recommendations in ways that are internally coherent and professionally legible. Cells assigned connectivity interventions consistently show high infrastructure deficiency and low walkability; greening-oriented recommendations correspond to high environmental degradation and reduced greenness; maintain-and-monitor cells cluster around intermediate values. This coherence between indicator profiles and recommendation categories demonstrates that a planner encountering any recommendation can locate precisely which indicator is driving it.

## Reproducing the validation

The validation materials — the expert rating template, instructions, and scoring code — are provided in the `validation/` directory and the pipeline notebook. The expert rating sheets are distributed with an empty rating column for professionals to complete; the scoring code computes acceptance rates, category-level agreement, Krippendorff's alpha, and inter-rater Spearman correlations once completed sheets are returned. See [Reproducibility](reproducibility) for the full procedure.
