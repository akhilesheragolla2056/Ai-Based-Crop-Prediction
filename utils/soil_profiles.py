from __future__ import annotations

import csv
from functools import lru_cache
from typing import Iterable

SOIL_PROFILES_PATH = "data/soil_profiles.csv"

SOIL_REGION_OPTIONS: list[tuple[str, str]] = [
    ("Coastal", "coastal"),
    ("Deccan Plateau", "deccan_plateau"),
    ("Alluvial", "alluvial"),
    ("Black Soil", "black_soil"),
    ("Arid / Semi-Arid", "arid"),
    ("North-East Hill", "north_east_hill"),
]


def _normalize_region_key(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"_", " "} else " " for ch in value.lower())
    return "_".join(cleaned.split())


@lru_cache(maxsize=1)
def _load_profiles(path: str = SOIL_PROFILES_PATH) -> dict[str, dict[str, float]]:
    profiles: dict[str, dict[str, float]] = {}
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            region = _normalize_region_key(str(row.get("region", "")))
            if not region:
                continue
            try:
                profiles[region] = {
                    "N": float(row.get("n_avg", 0.0)),
                    "P": float(row.get("p_avg", 0.0)),
                    "K": float(row.get("k_avg", 0.0)),
                    "ph": float(row.get("ph", 0.0)),
                }
            except (TypeError, ValueError):
                continue
    return profiles


def get_soil_profile(region_key: str, path: str = SOIL_PROFILES_PATH) -> dict[str, float] | None:
    normalized = _normalize_region_key(region_key)
    profiles = _load_profiles(path)
    return profiles.get(normalized)


def list_soil_regions() -> Iterable[str]:
    return [label for label, _ in SOIL_REGION_OPTIONS]
