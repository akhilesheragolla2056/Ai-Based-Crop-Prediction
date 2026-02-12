from __future__ import annotations

"""Shared backend helpers for loading models and normalising inputs."""
# Ensure src directory is on sys.path for module imports (must be first)
import sys
import os

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from functools import lru_cache
from pathlib import Path
from typing import Mapping

import joblib
import pandas as pd
import os


# Load seasonal water requirements from the crop recommendation dataset
def load_water_requirements(csv_path=None):
    if csv_path is None:
        csv_path = os.path.join("data", "raw", "Crop recommendation dataset.csv")
    df = pd.read_csv(csv_path)
    df.columns = [str(col).strip().upper() for col in df.columns]
    return df


# Get average seasonal water requirement for a crop
def get_water_requirement_for_crop(crop_name, df=None):
    if df is None:
        df = load_water_requirements()

    crop_column = "CROPS" if "CROPS" in df.columns else None
    water_column = "WATERREQUIRED" if "WATERREQUIRED" in df.columns else None
    water_max_column = (
        "WATERREQUIRED_MAX" if "WATERREQUIRED_MAX" in df.columns else None
    )
    soil_column = "SOIL" if "SOIL" in df.columns else None
    water_source_column = "WATER_SOURCE" if "WATER_SOURCE" in df.columns else None
    if not crop_column or not water_column:
        return None

    rows = df[df[crop_column].astype(str).str.lower() == crop_name.lower()]
    if rows.empty:
        return None

    water_values = pd.to_numeric(rows[water_column], errors="coerce").dropna()
    if water_values.empty:
        return None

    soil_type = None
    if soil_column:
        soil_values = rows[soil_column].dropna().astype(str).str.strip()
        soil_values = [s for s in soil_values.tolist() if s]
        if soil_values:
            # Keep unique soil labels in observed order for readability.
            soil_type = ", ".join(dict.fromkeys(soil_values))

             # Ensure project root (parent of src) is on sys.path for module imports (must be first)
    if water_source_column:
        water_source_values = rows[water_source_column].dropna().astype(str).str.strip()
            PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            if PROJECT_ROOT not in sys.path:
                sys.path.insert(0, PROJECT_ROOT)
            water_source = ", ".join(dict.fromkeys(water_source_values))

    avg_water = float(water_values.mean())
    if water_max_column and water_max_column in rows.columns:
        max_values = pd.to_numeric(rows[water_max_column], errors="coerce").dropna()
        if not max_values.empty:
            avg_max = float(max_values.mean())
            return {
                "seasonal_mm": avg_water,
                "seasonal_mm_max": avg_max,
                "soil_type": soil_type,
                "water_source": water_source,
            }

    return {
        "seasonal_mm": avg_water,
        "soil_type": soil_type,
        "water_source": water_source,
    }


from features import (
    generate_soil_health_tips,
    generate_weather_warnings,
    recommend_fertilizers,
)
from models import (
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
