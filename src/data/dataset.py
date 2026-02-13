"""Utilities for loading and splitting the crop recommendation dataset."""

from dataclasses import dataclass
from pathlib import Path

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
    "region",
)
TARGET_COLUMN = "crop"


def load_dataset(path: Path | None = None) -> pd.DataFrame:
    """Load and combine the original and region-aware crop datasets as a pandas DataFrame."""
    # Load both datasets
    region_path = PATHS.data_raw / "crop_recommendation_region_augmented.csv"
    orig_path = PATHS.data_raw / "crop_recommendation.csv"
    region_df = pd.read_csv(region_path, comment="#")
    orig_df = pd.read_csv(orig_path, comment="#")
    # Ensure column names match
    region_df = region_df.rename(columns={"label": TARGET_COLUMN})
    orig_df = orig_df.rename(columns={"label": TARGET_COLUMN})
    # Add 'region' column to original dataset if missing
    if "region" not in orig_df.columns:
        orig_df["region"] = "unknown"
    # Reorder columns to match region_df
    orig_df = orig_df[
        [
            "N",
            "P",
            "K",
            "temperature",
            "humidity",
            "ph",
            "rainfall",
            "region",
            TARGET_COLUMN,
        ]
    ]
    # Identify major cities/regions from region-aware dataset
    major_regions = region_df["region"].unique()
    # Use region-aware rows for major cities, original for others
    other_orig = orig_df[~orig_df["region"].isin(major_regions)]
    combined = pd.concat([region_df, other_orig], ignore_index=True)
    # Ensure all required columns are present
    for col in FEATURE_COLUMNS:
        if col not in combined.columns:
            combined[col] = "unknown"
    if TARGET_COLUMN not in combined.columns:
        combined[TARGET_COLUMN] = "unknown"
    # Remove rows with invalid numeric data, keep all crops with valid numeric data
    numeric_cols = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    for col in numeric_cols:
        if col in combined.columns:
            combined[col] = pd.to_numeric(combined[col], errors="coerce")
    # Aggressively filter: drop rows with NaN in any numeric column
    combined = combined.dropna(subset=numeric_cols)
    if "region" in combined.columns:
        combined["region"] = (
            combined["region"]
            .fillna("unknown")
            .astype(str)
            .str.strip()
            .replace("", "unknown")
            .str.lower()
        )
    combined[TARGET_COLUMN] = combined[TARGET_COLUMN].fillna(
        combined[TARGET_COLUMN].mode()[0]
        if not combined[TARGET_COLUMN].mode().empty
        else "unknown"
    )
    _validate_schema(combined)
    return combined


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
    dataset_path = path or PATHS.data_raw / "crop_recommendation_region_augmented.csv"
    if not dataset_path.exists():
        raise FileNotFoundError(
            "Dataset not found. Download it with scripts/download_dataset.py first."
        )
    return dataset_path


def _validate_schema(frame: pd.DataFrame) -> None:
    missing = [
        column
        for column in FEATURE_COLUMNS + (TARGET_COLUMN,)
        if column not in frame.columns
    ]
    if missing:
        raise DatasetSchemaError(f"Dataset is missing required columns: {missing}")


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
    # Disable stratification to allow all crops, including rare ones
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
        stratify=None,
    )
    return DatasetSplit(x_train=x_train, x_test=x_test, y_train=y_train, y_test=y_test)
