"""Feature engineering pipelines for the crop recommendation model."""

from __future__ import annotations

from typing import Sequence

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.data.dataset import FEATURE_COLUMNS

__all__ = ["build_feature_pipeline"]


def build_feature_pipeline(feature_names: Sequence[str] | None = None) -> ColumnTransformer:
    """Create the preprocessing pipeline for numeric features."""

    numeric_features = list(feature_names or FEATURE_COLUMNS)
    transformers = [
        (
            "numeric_standardize",
            Pipeline([("scaler", StandardScaler())]),
            numeric_features,
        )
    ]
    return ColumnTransformer(transformers=transformers, remainder="drop")
