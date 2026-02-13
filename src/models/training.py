"""Model training utilities for the crop recommendation project."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.pipeline import Pipeline

from src.data.dataset import DatasetSplit, FEATURE_COLUMNS, split_dataset
from src.features.engineering import build_feature_pipeline
from src.utils.config import PATHS

__all__ = [
    "TrainingConfig",
    "TrainingArtifacts",
    "train_model",
    "save_model",
]


@dataclass(slots=True)
class TrainingConfig:
    """Configuration for training a RandomForest classifier."""

    n_estimators: int = 300
    max_depth: int | None = None
    min_samples_split: int = 2
    min_samples_leaf: int = 1
    test_size: float = 0.2
    random_state: int = 42


@dataclass(slots=True)
class TrainingArtifacts:
    """Outputs produced after training the model."""

    pipeline: Pipeline
    metrics: Mapping[str, Any]
    feature_names: tuple[str, ...] = FEATURE_COLUMNS


def _build_model(config: TrainingConfig) -> Pipeline:
    feature_pipeline = build_feature_pipeline(FEATURE_COLUMNS)
    model = RandomForestClassifier(
        n_estimators=config.n_estimators,
        max_depth=config.max_depth,
        min_samples_split=config.min_samples_split,
        min_samples_leaf=config.min_samples_leaf,
        random_state=config.random_state,
        n_jobs=-1,
    )
    return Pipeline(
        steps=[
            ("features", feature_pipeline),
            ("classifier", model),
        ]
    )


def train_model(
    config: TrainingConfig | None = None, dataset: DatasetSplit | None = None
) -> TrainingArtifacts:
    """Train a RandomForest model and return the fitted pipeline and metrics."""

    config = config or TrainingConfig()
    dataset = dataset or split_dataset(
        test_size=config.test_size,
        random_state=config.random_state,
    )

    model_pipeline = _build_model(config)
    model_pipeline.fit(dataset.x_train, dataset.y_train)

    predictions = model_pipeline.predict(dataset.x_test)
    probabilities = model_pipeline.predict_proba(dataset.x_test)

    accuracy = accuracy_score(dataset.y_test, predictions)
    macro_f1 = f1_score(dataset.y_test, predictions, average="macro")
    report = classification_report(
        dataset.y_test,
        predictions,
        output_dict=True,
        zero_division=0,
    )

    metrics = {
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "classification_report": report,
    }

    # Log sample probability summaries to gauge confidence distribution.
    metrics["probability_summary"] = {
        "max_mean": float(probabilities.max(axis=1).mean()),
        "max_std": float(probabilities.max(axis=1).std()),
    }

    return TrainingArtifacts(
        pipeline=model_pipeline,
        metrics=metrics,
        feature_names=FEATURE_COLUMNS,
    )


def save_model(artifacts: TrainingArtifacts, *, model_dir: Path | None = None) -> Path:
    """Persist the trained pipeline to disk."""

    target_dir = model_dir or PATHS.artifacts_models
    target_dir.mkdir(parents=True, exist_ok=True)
    model_path = target_dir / "crop_recommender.joblib"
    joblib.dump(artifacts.pipeline, model_path)
    return model_path


def save_metrics(
    metrics: Mapping[str, Any], *, metrics_dir: Path | None = None
) -> Path:
    """Persist training metrics to disk as JSON."""

    target_dir = metrics_dir or PATHS.artifacts_metrics
    target_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = target_dir / "training_metrics.json"

    import json

    metrics_path.write_text(
        json.dumps(metrics, indent=2, default=_json_default),
        encoding="utf-8",
    )
    return metrics_path


def _json_default(value: Any) -> Any:
    if isinstance(value, (float, int, str, bool)) or value is None:
        return value
    if hasattr(value, "tolist"):
        return value.tolist()
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")
