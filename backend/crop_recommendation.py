"""Service for crop recommendation logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from backend.utils import (
    ModelNotReady,
    get_crop_predictor,
    soil_health_insights,
    weather_insights,
)


@dataclass(frozen=True, slots=True)
class CropRecommendation:
    name: str
    score: float
    suitability: str
    rationale: str


@dataclass(frozen=True, slots=True)
class CropRecommendationResponse:
    recommendations: tuple[CropRecommendation, ...]
    soil_tips: tuple[str, ...]
    weather_notes: tuple[str, ...]


def recommend_crops(features: Mapping[str, float]) -> CropRecommendationResponse:
    predictor = get_crop_predictor()
    result = predictor.recommend(features)
    recommendations = tuple(
        CropRecommendation(
            name=entry.crop.title(),
            score=entry.probability,
            suitability=entry.yield_category,
            rationale=(
                "Why this crop? Balanced nutrients and climate indicators favour "
                f"{entry.crop.title()} for the upcoming season."
            ),
        )
        for entry in result.recommendations
    )
    default_crop = recommendations[0].name if recommendations else ""
    soil_tips = soil_health_insights(features)
    weather_notes = weather_insights(features, default_crop)
    return CropRecommendationResponse(
        recommendations=recommendations,
        soil_tips=soil_tips,
        weather_notes=weather_notes,
    )


__all__ = [
    "CropRecommendation",
    "CropRecommendationResponse",
    "recommend_crops",
    "ModelNotReady",
]
