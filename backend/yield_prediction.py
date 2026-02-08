"""Yield projection utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from backend.utils import get_yield_estimator, weather_insights


@dataclass(frozen=True, slots=True)
class YieldProjection:
    crop: str
    level: str
    estimated_output: float
    confidence: float
    reasoning: str
    weather_notes: tuple[str, ...]


def predict_yield(crop: str, features: Mapping[str, float]) -> YieldProjection:
    estimator = get_yield_estimator()
    outcome = estimator.predict(crop, features)
    notes = weather_insights(features, crop)
    return YieldProjection(
        crop=crop.title(),
        level=outcome.yield_level,
        estimated_output=outcome.estimated_quintal_per_acre,
        confidence=outcome.confidence,
        reasoning=outcome.reasoning,
        weather_notes=notes,
    )


__all__ = ["YieldProjection", "predict_yield"]
