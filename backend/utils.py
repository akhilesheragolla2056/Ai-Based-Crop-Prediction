"""Shared backend helpers for loading models and normalising inputs."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Mapping

import joblib
import pandas as pd

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


def load_water_requirements(csv_path: str | Path | None = None) -> pd.DataFrame:
    if csv_path is None:
        csv_path = Path("data") / "raw" / "Crop recommendation dataset.csv"
    dataframe = pd.read_csv(csv_path)
    dataframe.columns = [str(column).strip().upper() for column in dataframe.columns]
    return dataframe


def get_water_requirement_for_crop(
    crop_name: str, dataframe: pd.DataFrame | None = None
) -> Mapping[str, float | str] | None:
    if dataframe is None:
        dataframe = load_water_requirements()

    crop_column = "CROPS" if "CROPS" in dataframe.columns else None
    water_column = "WATERREQUIRED" if "WATERREQUIRED" in dataframe.columns else None
    water_max_column = (
        "WATERREQUIRED_MAX" if "WATERREQUIRED_MAX" in dataframe.columns else None
    )
    soil_column = "SOIL" if "SOIL" in dataframe.columns else None
    water_source_column = "WATER_SOURCE" if "WATER_SOURCE" in dataframe.columns else None

    if not crop_column or not water_column:
        return None

    rows = dataframe[dataframe[crop_column].astype(str).str.lower() == crop_name.lower()]
    if rows.empty:
        return None

    water_values = pd.to_numeric(rows[water_column], errors="coerce").dropna()
    if water_values.empty:
        return None

    soil_type = None
    if soil_column:
        soil_values = rows[soil_column].dropna().astype(str).str.strip()
        filtered = [item for item in soil_values.tolist() if item]
        if filtered:
            soil_type = ", ".join(dict.fromkeys(filtered))

    water_source = None
    if water_source_column:
        water_source_values = rows[water_source_column].dropna().astype(str).str.strip()
        filtered = [item for item in water_source_values.tolist() if item]
        if filtered:
            water_source = ", ".join(dict.fromkeys(filtered))

    result: dict[str, float | str] = {
        "seasonal_mm": float(water_values.mean()),
    }
    if soil_type:
        result["soil_type"] = soil_type
    if water_source:
        result["water_source"] = water_source

    if water_max_column and water_max_column in rows.columns:
        max_values = pd.to_numeric(rows[water_max_column], errors="coerce").dropna()
        if not max_values.empty:
            result["seasonal_mm_max"] = float(max_values.mean())

    return result


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
