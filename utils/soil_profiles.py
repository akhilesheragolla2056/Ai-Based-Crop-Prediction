from __future__ import annotations

from functools import lru_cache
from typing import Iterable

import pandas as pd

SOIL_DATASET_PATH = "data/raw/Crop recommendation dataset.csv"
FALLBACK_SOIL_OPTIONS: list[tuple[str, str]] = [
    ("Alluvial soil", "alluvial_soil"),
    ("Black soil", "black_soil"),
    ("Clay soil", "clay_soil"),
    ("Loamy soil", "loamy_soil"),
    ("Sandy soil", "sandy_soil"),
]


def _normalize_region_key(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"_", " "} else " " for ch in value.lower())
    return "_".join(cleaned.split())


def _midpoint_mean(
    frame: pd.DataFrame, base_column: str, max_column: str | None = None
) -> float | None:
    base = pd.to_numeric(frame.get(base_column), errors="coerce")
    if max_column and max_column in frame.columns:
        high = pd.to_numeric(frame.get(max_column), errors="coerce")
        midpoint = (base + high) / 2
        merged = midpoint.where(midpoint.notna(), base)
    else:
        merged = base

    merged = merged.dropna()
    if merged.empty:
        return None
    return float(merged.mean())


@lru_cache(maxsize=1)
def _load_profiles(path: str = SOIL_DATASET_PATH) -> dict[str, dict[str, float]]:
    try:
        df = pd.read_csv(path)
    except Exception:
        return {}
    df.columns = [str(col).strip().upper() for col in df.columns]

    if "SOIL" not in df.columns:
        return {}

    soil_values = df["SOIL"].dropna().astype(str).str.strip()
    soil_values = soil_values[soil_values != ""]
    if soil_values.empty:
        return {}

    working = df.loc[soil_values.index].copy()
    working["SOIL_KEY"] = soil_values.map(_normalize_region_key)

    profiles: dict[str, dict[str, float]] = {}
    for soil_key, group in working.groupby("SOIL_KEY"):
        if not soil_key:
            continue

        n_mean = _midpoint_mean(group, "N", "N_MAX")
        p_mean = _midpoint_mean(group, "P", "P_MAX")
        k_mean = _midpoint_mean(group, "K", "K_MAX")
        ph_mean = _midpoint_mean(group, "SOIL_PH", "SOIL_PH_HIGH")
        temp_mean = _midpoint_mean(group, "TEMP", "MAX_TEMP")
        humidity_mean = _midpoint_mean(
            group, "RELATIVE_HUMIDITY", "RELATIVE_HUMIDITY_MAX"
        )
        # Dataset has no rainfall column; use water requirement midpoint as rainfall proxy.
        rainfall_mean = _midpoint_mean(group, "WATERREQUIRED", "WATERREQUIRED_MAX")

        if None in {n_mean, p_mean, k_mean, ph_mean}:
            continue

        profiles[soil_key] = {
            "N": n_mean,
            "P": p_mean,
            "K": k_mean,
            "ph": ph_mean,
            "temperature": temp_mean if temp_mean is not None else 26.0,
            "humidity": humidity_mean if humidity_mean is not None else 60.0,
            "rainfall": rainfall_mean if rainfall_mean is not None else 160.0,
        }
    return profiles


@lru_cache(maxsize=1)
def _load_region_options(path: str = SOIL_DATASET_PATH) -> list[tuple[str, str]]:
    try:
        df = pd.read_csv(path)
    except Exception:
        return FALLBACK_SOIL_OPTIONS
    df.columns = [str(col).strip().upper() for col in df.columns]
    if "SOIL" not in df.columns:
        return FALLBACK_SOIL_OPTIONS

    soil_values = (
        df["SOIL"].dropna().astype(str).str.strip().tolist()
    )
    options: list[tuple[str, str]] = []
    seen: set[str] = set()
    for value in soil_values:
        if not value:
            continue
        key = _normalize_region_key(value)
        if not key or key in seen:
            continue
        seen.add(key)
        options.append((value, key))
    return sorted(options, key=lambda item: item[0].lower()) or FALLBACK_SOIL_OPTIONS


SOIL_REGION_OPTIONS: list[tuple[str, str]] = _load_region_options()


def get_soil_profile(region_key: str, path: str = SOIL_DATASET_PATH) -> dict[str, float] | None:
    normalized = _normalize_region_key(region_key)
    profiles = _load_profiles(path)
    return profiles.get(normalized)


def list_soil_regions() -> Iterable[str]:
    return [label for label, _ in _load_region_options()]
