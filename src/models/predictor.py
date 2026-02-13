"""Inference helpers for the crop recommendation pipeline."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Iterable, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from src.data.dataset import FEATURE_COLUMNS, TARGET_COLUMN
from src.models.training import save_model, train_model
from src.utils.config import PATHS

__all__ = [
    "Recommendation",
    "RecommendationResult",
    "CropPredictor",
    "load_pipeline",
]


@dataclass(slots=True)
class Recommendation:
    crop: str
    probability: float
    yield_category: str


@dataclass(slots=True)
class RecommendationResult:
    recommendations: tuple[Recommendation, ...]


class CropPredictor:
    """Wrapper around the trained scikit-learn pipeline."""

    def __init__(self, pipeline: Pipeline, *, top_k: int = 3) -> None:
        self._pipeline = pipeline
        self._top_k = top_k

    @property
    def top_k(self) -> int:
        return self._top_k

    def recommend(
        self, features: pd.DataFrame | dict[str, float]
    ) -> RecommendationResult:
        frame = self._ensure_frame(features)
        probabilities = self._pipeline.predict_proba(frame)
        classes = self._pipeline.classes_

        # Current UI submits a single sample; pick the first row.
        top_indices = np.argsort(probabilities[0])[::-1][: self._top_k]
        recommendations = tuple(
            Recommendation(
                crop=str(classes[index]),
                probability=float(probabilities[0, index]),
                yield_category=self._probability_to_yield(probabilities[0, index]),
            )
            for index in top_indices
        )
        return RecommendationResult(recommendations=recommendations)

    @staticmethod
    def _probability_to_yield(probability: float) -> str:
        if probability >= 0.7:
            return "High"
        if probability >= 0.4:
            return "Medium"
        return "Low"

    @staticmethod
    def _ensure_frame(features: pd.DataFrame | dict[str, float]) -> pd.DataFrame:
        if isinstance(features, pd.DataFrame):
            missing = [
                column for column in FEATURE_COLUMNS if column not in features.columns
            ]
            if missing:
                raise ValueError(f"Missing feature columns: {missing}")
            frame = features[FEATURE_COLUMNS].copy()
        else:
            frame = pd.DataFrame([features], columns=FEATURE_COLUMNS)

        # Keep preprocessing stable across environments: region must always be string-like.
        if "region" in frame.columns:
            frame["region"] = (
                frame["region"]
                .fillna("unknown")
                .astype(str)
                .str.strip()
                .replace("", "unknown")
                .str.lower()
            )

        return frame


def load_pipeline(model_path: Path | None = None) -> Pipeline:
    path = model_path or PATHS.artifacts_models / "crop_recommender.joblib"
    if not path.exists():
        raise FileNotFoundError(
            "Trained model not found. Run scripts/train_model.py first."
        )
    try:
        pipeline = joblib.load(path)
    except Exception as exc:
        # Handle sklearn/joblib incompatibility (common on cloud when package versions change).
        logging.warning(
            "Model load failed for %s (%s). Re-training a compatible model.",
            path,
            exc.__class__.__name__,
        )
        artifacts = train_model()
        save_model(artifacts, model_dir=path.parent)
        pipeline = artifacts.pipeline
    if not isinstance(pipeline, Pipeline):
        raise TypeError("Loaded object is not a scikit-learn Pipeline")
    return pipeline
