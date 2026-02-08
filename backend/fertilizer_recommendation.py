"""Generate fertilizer recommendations using soil diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from backend.utils import fertilizer_plan


@dataclass(frozen=True, slots=True)
class FertilizerAdvice:
    nutrient: str
    product: str
    quantity: str
    rationale: str
    organic_option: str


def recommend_fertilizer(
    crop: str, soil_metrics: Mapping[str, float]
) -> tuple[FertilizerAdvice, ...]:
    plan = fertilizer_plan(crop, soil_metrics)
    return tuple(
        FertilizerAdvice(
            nutrient=item.nutrient,
            product=item.fertilizer,
            quantity=item.quantity_per_acre,
            rationale=item.explanation,
            organic_option=item.organic_option,
        )
        for item in plan
    )


__all__ = ["FertilizerAdvice", "recommend_fertilizer"]
