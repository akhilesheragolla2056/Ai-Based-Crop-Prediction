"""Feature engineering pipelines for the crop recommendation model."""

from __future__ import annotations

from typing import Sequence

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.data.dataset import FEATURE_COLUMNS

__all__ = ["build_feature_pipeline"]


def build_feature_pipeline(
    feature_names: Sequence[str] | None = None,
) -> ColumnTransformer:
    """Create preprocessing for numeric and categorical features."""

    all_features = list(feature_names or FEATURE_COLUMNS)
    categorical_features = [column for column in all_features if column == "region"]
    numeric_features = [
        column for column in all_features if column not in categorical_features
    ]
    transformers = [
        (
            "numeric_standardize",
            Pipeline([("scaler", StandardScaler())]),
            numeric_features,
        ),
    ]
    if categorical_features:
        transformers.append(
            (
                "categorical_ohe",
                Pipeline(
                    [
                        (
                            "encoder",
                            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                        )
                    ]
                ),
                categorical_features,
            )
        )
    return ColumnTransformer(transformers=transformers, remainder="drop")
