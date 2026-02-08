"""Fertilizer recommendations driven by soil diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

__all__ = ["FertilizerAdvice", "recommend_fertilizers"]


@dataclass(frozen=True, slots=True)
class FertilizerAdvice:
    nutrient: str
    fertilizer: str
    quantity_per_acre: str
    explanation: str
    organic_option: str


def recommend_fertilizers(
    crop: str, soil_metrics: Mapping[str, float]
) -> tuple[FertilizerAdvice, ...]:
    """Return smart recommendations describing nutrient gaps and corrective inputs.

    The logic blends agronomy heuristics with the supplied soil test values. For
    hackathon demos this offers explainable outputs while allowing future
    integration with data-driven optimisers.
    """

    n = soil_metrics.get("N", 0.0)
    p = soil_metrics.get("P", 0.0)
    k = soil_metrics.get("K", 0.0)
    ph = soil_metrics.get("ph", 7.0)

    advice: list[FertilizerAdvice] = []

    if n < 60:
        advice.append(
            FertilizerAdvice(
                nutrient="Nitrogen",
                fertilizer="Urea (46% N)",
                quantity_per_acre="40-50 kg broadcast in two splits",
                explanation="Leaf colour indicates nitrogen hunger; boost vegetative growth for {}.".format(
                    crop.title()
                ),
                organic_option="Farmyard manure (1.5 tons/acre) or legume green manure incorporation.",
            )
        )
    elif n > 130:
        advice.append(
            FertilizerAdvice(
                nutrient="Nitrogen",
                fertilizer="Reduce nitrogen inputs",
                quantity_per_acre="Skip top dressing this cycle",
                explanation="Soil already rich in nitrogen; avoid lodging risk for {}.".format(
                    crop.title()
                ),
                organic_option="Adopt foliar bio-stimulants rather than synthetic N sources.",
            )
        )

    if p < 45:
        advice.append(
            FertilizerAdvice(
                nutrient="Phosphorus",
                fertilizer="DAP (18-46-0)",
                quantity_per_acre="25 kg basal dose",
                explanation="Low phosphorus detected; support rooting and early tillering for {}.".format(
                    crop.title()
                ),
                organic_option="Rock phosphate (fine grade) with compost for slow release.",
            )
        )
    elif p > 120:
        advice.append(
            FertilizerAdvice(
                nutrient="Phosphorus",
                fertilizer="Balanced NPK (10-26-26)",
                quantity_per_acre="25 kg basal + 20 kg top dressing",
                explanation="Excess phosphorus; switch to balanced mixes to avoid micronutrient lockout.",
                organic_option="Apply composted poultry manure to improve microbial P utilisation.",
            )
        )

    if k < 50:
        advice.append(
            FertilizerAdvice(
                nutrient="Potassium",
                fertilizer="Muriate of potash (60% K2O)",
                quantity_per_acre="15-20 kg side dressing",
                explanation="Potassium deficiency lowers disease tolerance and grain filling in {}.".format(
                    crop.title()
                ),
                organic_option="Wood ash (150 kg) or banana pseudostem compost for gradual K supply.",
            )
        )
    elif k > 130:
        advice.append(
            FertilizerAdvice(
                nutrient="Potassium",
                fertilizer="Avoid additional potash",
                quantity_per_acre="No potash this season",
                explanation="Soil already saturated with potassium; excessive K antagonises magnesium uptake.",
                organic_option="Focus on micronutrient foliar sprays instead of potash products.",
            )
        )

    if ph < 5.8:
        advice.append(
            FertilizerAdvice(
                nutrient="pH",
                fertilizer="Agricultural lime",
                quantity_per_acre="200 kg split into two applications",
                explanation="Acidic soil reduces nutrient availability; liming will stabilise pH for {}.".format(
                    crop.title()
                ),
                organic_option="Incorporate biochar or composted poultry litter to buffer acidity.",
            )
        )
    elif ph > 7.8:
        advice.append(
            FertilizerAdvice(
                nutrient="pH",
                fertilizer="Elemental sulphur or gypsum",
                quantity_per_acre="40 kg elemental sulphur worked into soil",
                explanation="Alkaline reaction can lock micronutrients; acidifying amendments restore balance.",
                organic_option="Apply acidic compost (coco-peat based) with drip fertigation.",
            )
        )

    if not advice:
        advice.append(
            FertilizerAdvice(
                nutrient="Balanced",
                fertilizer="NPK 10-26-26 + micronutrient foliar mix",
                quantity_per_acre="20 kg basal + micronutrient spray at 30 DAS",
                explanation="Soil nutrients look balanced; maintain through split NPK and foliar micronutrients.",
                organic_option="Vermicompost tea foliar spray with seaweed extract.",
            )
        )

    return tuple(advice)
