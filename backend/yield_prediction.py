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


def predict_yield(crop: str, features: Mapping[str, float]) -> YieldProjection:
    # Only use crop and state for lookup
    state = features.get("state")
    df = pd.read_csv(CROP_YIELD_CSV)
    df_crop = df[df["Crop"].str.lower() == crop.lower()]
    if state:
        df_crop = df_crop[df_crop["State"].str.lower() == state.lower()]
    if df_crop.empty:
        fallback_yield = STATIC_YIELD.get(crop.lower())
        if fallback_yield is not None:
            return YieldProjection(
                crop=crop,
                level=None,
                estimated_output=fallback_yield,
                confidence=None,
                reasoning=f"No historical data found, using static average yield.",
                weather_notes=None,
            )
        return YieldProjection(
            crop=crop,
            level=None,
            estimated_output=None,
            confidence=None,
            reasoning=f"No yield data found for crop '{crop}' and state '{state}'.",
            weather_notes=None,
        )
    avg_yield = df_crop["Yield"].mean()
    avg_production = df_crop["Production"].mean()
    return YieldProjection(
        crop=crop,
        level=None,
        estimated_output=avg_yield,
        confidence=None,
        reasoning=f"Average yield: {avg_yield:.2f} (quintals/acre), average production: {avg_production:.2f} (kg).",
        weather_notes=None,
    )


__all__ = ["YieldProjection", "predict_yield"]
