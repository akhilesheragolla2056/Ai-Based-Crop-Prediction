"""Yield projection utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from backend.utils import get_yield_estimator, weather_insights
from backend.yield_data_utils import predict_yield as predict_yield_from_data
import pandas as pd

CROP_YIELD_CSV = "data/raw/crop_yield.csv"
STATIC_YIELD = {
    "rice": 2.7,
    "wheat": 3.2,
    "maize": 2.5,
    "cotton": 1.8,
    "groundnut": 1.2,
    "sugarcane": 70.0,
    "banana": 30.0,
    "apple": 10.0,
    "mango": 8.0,
    "grapes": 12.0,
    "coffee": 0.8,
    "jute": 2.0,
    "coconut": 10.0,
    "papaya": 40.0,
    "orange": 8.0,
    "chickpea": 1.0,
    "kidneybeans": 1.1,
    "pigeonpeas": 0.9,
    "mothbeans": 0.7,
    "mungbean": 0.8,
    "blackgram": 0.7,
    "lentil": 1.0,
    "pomegranate": 12.0,
    "watermelon": 20.0,
    "muskmelon": 15.0,
}


@dataclass(frozen=True, slots=True)
class YieldProjection:
    crop: str
    level: str
    estimated_output: float
    confidence: float
    reasoning: str
    weather_notes: tuple[str, ...]


def _confidence_from_samples(sample_count: int, state_filtered: bool) -> float:
    """Estimate confidence from available historical sample size."""
    if sample_count <= 0:
        return 0.62 if state_filtered else 0.72
    if state_filtered:
        return min(0.95, 0.66 + min(sample_count, 8) * 0.035)
    return min(0.92, 0.64 + min(sample_count, 10) * 0.028)


def _level_from_confidence(confidence: float) -> str:
    """Map confidence to a user-facing yield category."""
    if confidence >= 0.8:
        return "High"
    if confidence >= 0.65:
        return "Medium"
    return "Low"


def predict_yield(crop: str, features: Mapping[str, float]) -> YieldProjection:
    # Only use crop and state for lookup
    state = features.get("state")
    df = pd.read_csv(CROP_YIELD_CSV)
    df_crop_all_states = df[df["Crop"].str.lower() == crop.lower()]
    df_crop = df_crop_all_states
    used_state_filter = False
    if state:
        state_rows = df_crop_all_states[
            df_crop_all_states["State"].str.lower() == state.lower()
        ]
        if not state_rows.empty:
            df_crop = state_rows
            used_state_filter = True

    if df_crop.empty:
        fallback_yield = STATIC_YIELD.get(crop.lower())
        if fallback_yield is not None:
            fallback_confidence = 0.72
            return YieldProjection(
                crop=crop,
                level=_level_from_confidence(fallback_confidence),
                estimated_output=fallback_yield,
                confidence=fallback_confidence,
                reasoning=f"No historical data found, using static average yield.",
                weather_notes=None,
            )
        return YieldProjection(
            crop=crop,
            level="Low",
            estimated_output=None,
            confidence=0.0,
            reasoning=f"No yield data found for crop '{crop}' and state '{state}'.",
            weather_notes=None,
        )
    avg_yield = df_crop["Yield"].mean()
    avg_production = df_crop["Production"].mean()
    confidence = _confidence_from_samples(len(df_crop), used_state_filter)
    return YieldProjection(
        crop=crop,
        level=_level_from_confidence(confidence),
        estimated_output=avg_yield,
        confidence=confidence,
        reasoning=f"Average yield: {avg_yield:.2f} (quintals/acre), average production: {avg_production:.2f} (kg).",
        weather_notes=None,
    )


__all__ = ["YieldProjection", "predict_yield"]
