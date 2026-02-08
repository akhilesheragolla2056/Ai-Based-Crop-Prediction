"""Shared backend helpers for loading models and normalising inputs."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Mapping

import joblib

from src.features import (
    generate_soil_health_tips,
    generate_weather_warnings,
    recommend_fertilizers,
)
from src.models import (
    CropDiseaseClassifier,
    CropPredictor,
    YieldEstimator,
    load_pipeline,
)

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_MODEL_FALLBACK = _PROJECT_ROOT / "models" / "trained_model.pkl"


class ModelNotReady(RuntimeError):
    """Raised when a required trained asset is missing."""


@lru_cache(maxsize=1)
def get_crop_predictor(top_k: int = 3) -> CropPredictor:
    """Return a cached crop predictor instance."""

    try:
        pipeline = load_pipeline()
    except FileNotFoundError as exc:
        if _MODEL_FALLBACK.exists():
            pipeline = joblib.load(_MODEL_FALLBACK)
        else:
            raise ModelNotReady(
                "Crop recommendation model is missing. Run scripts/train_model.py first."
            ) from exc
    return CropPredictor(pipeline, top_k=top_k)


@lru_cache(maxsize=1)
def get_disease_classifier() -> CropDiseaseClassifier:
    """Create or return a cached disease classifier."""

    return CropDiseaseClassifier()


@lru_cache(maxsize=1)
def get_yield_estimator() -> YieldEstimator:
    """Return the reusable yield estimator."""

    return YieldEstimator()


def soil_health_insights(features: Mapping[str, float]) -> tuple[str, ...]:
    return generate_soil_health_tips(features)


def weather_insights(features: Mapping[str, float], crop: str) -> tuple[str, ...]:
    return generate_weather_warnings(features, crop)


def fertilizer_plan(crop: str, soil_metrics: Mapping[str, float]):
    return recommend_fertilizers(crop, soil_metrics)
