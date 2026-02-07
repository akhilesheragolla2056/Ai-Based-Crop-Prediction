"""Utilities for loading and splitting the crop recommendation dataset."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
from sklearn.model_selection import train_test_split

from src.utils.config import PATHS

__all__ = [
    "FEATURE_COLUMNS",
    "TARGET_COLUMN",
    "DatasetSplit",
    "load_dataset",
    "split_dataset",
]

FEATURE_COLUMNS: tuple[str, ...] = (
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall",
)
TARGET_COLUMN = "crop"


@dataclass(slots=True)
class DatasetSplit:
    """Structured dataset split returned by ``split_dataset``."""

    x_train: pd.DataFrame
    x_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series


class DatasetSchemaError(ValueError):
    """Raised when mandatory columns are missing from the dataset."""


def _resolve_dataset_path(path: Path | None) -> Path:
    dataset_path = path or PATHS.data_raw / "crop_recommendation.csv"
    if not dataset_path.exists():
        raise FileNotFoundError(
            "Dataset not found. Download it with scripts/download_dataset.py first."
        )
    return dataset_path


def _validate_schema(frame: pd.DataFrame) -> None:
    missing = [column for column in FEATURE_COLUMNS + ("label",) if column not in frame.columns]
    if missing:
        raise DatasetSchemaError(f"Dataset is missing required columns: {missing}")


def load_dataset(path: Path | None = None) -> pd.DataFrame:
    """Load the raw crop dataset as a pandas DataFrame."""

    dataset_path = _resolve_dataset_path(path)
    frame = pd.read_csv(dataset_path)
    _validate_schema(frame)
    frame = frame.rename(columns={"label": TARGET_COLUMN})
    return frame


def split_dataset(
    *,
    path: Path | None = None,
    test_size: float = 0.2,
    random_state: int = 42,
    stratify: bool = True,
) -> DatasetSplit:
    """Load and split the dataset into train/test partitions."""

    frame = load_dataset(path)
    features = frame.loc[:, FEATURE_COLUMNS]
    target = frame[TARGET_COLUMN]
    stratify_values: Iterable[pd.Series] | None = target if stratify else None

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify_values,
    )
    return DatasetSplit(x_train=x_train, x_test=x_test, y_train=y_train, y_test=y_test)
