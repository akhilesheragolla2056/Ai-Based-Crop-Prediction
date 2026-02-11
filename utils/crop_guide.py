from __future__ import annotations

import csv
import json
from functools import lru_cache
from pathlib import Path
from typing import Any

_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "crop_details.json"
_DATASET_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "Crop recommendation dataset.csv"
)

_ALIASES = {
    "arhar": "pigeonpeas",
    "tur": "pigeonpeas",
    "redgram": "pigeonpeas",
    "moong": "mungbean",
    "greengram": "mungbean",
    "urad": "blackgram",
    "rajma": "kidneybeans",
    "bengalgram": "chickpea",
    "gram": "chickpea",
    "sorghum": "jowar",
}


def normalize_crop_key(name: str) -> str:
    return "".join(ch for ch in name.lower().strip() if ch.isalnum())


def _safe_float(value: str | float | int | None) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def _mode(values: list[str]) -> str | None:
    counts: dict[str, int] = {}
    for value in values:
        key = value.strip()
        if not key:
            continue
        counts[key] = counts.get(key, 0) + 1
    if not counts:
        return None
    return max(counts, key=counts.get)


@lru_cache(maxsize=1)
def _load_dataset_details() -> dict[str, dict[str, Any]]:
    if not _DATASET_PATH.exists():
        return {}

    by_crop: dict[str, list[dict[str, str]]] = {}
    with _DATASET_PATH.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            crop_name = (row.get("CROPS") or "").strip()
            if not crop_name:
                continue
            crop_key = normalize_crop_key(crop_name)
            by_crop.setdefault(crop_key, []).append(row)

    details_by_crop: dict[str, dict[str, Any]] = {}
    for crop_key, rows in by_crop.items():
        crop_name = (rows[0].get("CROPS") or crop_key).strip().title()
        crop_type = _mode([str(r.get("TYPE_OF_CROP", "")) for r in rows]) or "Not specified"
        season = _mode([str(r.get("SEASON", "")) for r in rows]) or "Not specified"
        sown = _mode([str(r.get("SOWN", "")) for r in rows]) or "Not specified"
        harvested = _mode([str(r.get("HARVESTED", "")) for r in rows]) or "Not specified"
        water_source = _mode([str(r.get("WATER_SOURCE", "")) for r in rows]) or "Not specified"
        soil = _mode([str(r.get("SOIL", "")) for r in rows]) or "Not specified"

        n_avg = _mean(
            [x for x in (_safe_float(r.get("N")) for r in rows) if x is not None]
        )
        p_avg = _mean(
            [x for x in (_safe_float(r.get("P")) for r in rows) if x is not None]
        )
        k_avg = _mean(
            [x for x in (_safe_float(r.get("K")) for r in rows) if x is not None]
        )
        ph_low = _mean(
            [x for x in (_safe_float(r.get("SOIL_PH")) for r in rows) if x is not None]
        )
        ph_high = _mean(
            [x for x in (_safe_float(r.get("SOIL_PH_HIGH")) for r in rows) if x is not None]
        )
        duration_low = _mean(
            [x for x in (_safe_float(r.get("CROPDURATION")) for r in rows) if x is not None]
        )
        duration_high = _mean(
            [x for x in (_safe_float(r.get("CROPDURATION_MAX")) for r in rows) if x is not None]
        )
        water_low = _mean(
            [x for x in (_safe_float(r.get("WATERREQUIRED")) for r in rows) if x is not None]
        )
        water_high = _mean(
            [x for x in (_safe_float(r.get("WATERREQUIRED_MAX")) for r in rows) if x is not None]
        )
        temp_avg = _mean(
            [x for x in (_safe_float(r.get("TEMP")) for r in rows) if x is not None]
        )
        temp_max = _mean(
            [x for x in (_safe_float(r.get("MAX_TEMP")) for r in rows) if x is not None]
        )
        humidity_low = _mean(
            [
                x
                for x in (_safe_float(r.get("RELATIVE_HUMIDITY")) for r in rows)
                if x is not None
            ]
        )
        humidity_high = _mean(
            [
                x
                for x in (_safe_float(r.get("RELATIVE_HUMIDITY_MAX")) for r in rows)
                if x is not None
            ]
        )

        duration_txt = "Not specified"
        if duration_low is not None and duration_high is not None:
            duration_txt = f"{duration_low:.0f}-{duration_high:.0f} days"
        elif duration_low is not None:
            duration_txt = f"{duration_low:.0f} days"

        stage_wise = []
        if water_low is not None and water_high is not None:
            stage_wise.append(
                f"Estimated water demand from dataset: {water_low:.0f}-{water_high:.0f} mm."
            )
        if water_source != "Not specified":
            stage_wise.append(f"Water source pattern in dataset: {water_source}.")

        fert_lines = []
        if n_avg is not None and p_avg is not None and k_avg is not None:
            fert_lines.append(
                f"Dataset average NPK baseline: N={n_avg:.1f}, P={p_avg:.1f}, K={k_avg:.1f}."
            )

        weather_summary = []
        if temp_avg is not None:
            weather_summary.append(f"Temp {temp_avg:.1f} C")
        if temp_max is not None:
            weather_summary.append(f"max {temp_max:.1f} C")
        if humidity_low is not None:
            weather_summary.append(f"RH {humidity_low:.1f}%")
        if humidity_high is not None:
            weather_summary.append(f"RH max {humidity_high:.1f}%")

        ph_summary = "Not specified"
        if ph_low is not None and ph_high is not None:
            ph_summary = f"{ph_low:.1f}-{ph_high:.1f}"
        elif ph_low is not None:
            ph_summary = f"{ph_low:.1f}"

        details_by_crop[crop_key] = {
            "name": crop_name,
            "type": crop_type.title(),
            "season": season.title(),
            "duration": duration_txt,
            "stages": [
                {
                    "name": "Sowing window",
                    "days": "NA",
                    "activities": f"Sowing month in dataset: {sown}.",
                },
                {
                    "name": "Harvest window",
                    "days": "NA",
                    "activities": f"Harvest month in dataset: {harvested}.",
                },
            ],
            "fertilizer": {
                "basal": fert_lines[0] if fert_lines else "Use soil-test-based NPK planning.",
                "top_dressing": [
                    "Split nutrient application by growth stage based on local agronomy."
                ],
                "fertilizers": ["NPK blends as per soil test"],
                "organic": "Add compost/FYM based on soil condition.",
            },
            "irrigation": {
                "stage_wise": stage_wise if stage_wise else ["Use local irrigation scheduling."],
                "frequency": "Adjust by rainfall and soil moisture status.",
                "notes": f"Typical soil in dataset: {soil}.",
            },
            "pests": {
                "common_pests": [],
                "common_diseases": [],
                "prevention": "Follow local extension advisories for pest and disease management.",
                "pesticides": [],
            },
            "harvest": {
                "indicators": f"Harvest month in dataset: {harvested}.",
                "yield": "Yield range not provided in this dataset.",
                "post_harvest": (
                    "Dry and store produce safely as per crop-specific best practices."
                ),
            },
        }

        if weather_summary:
            details_by_crop[crop_key]["irrigation"]["notes"] += (
                " Climate profile: " + ", ".join(weather_summary) + "."
            )
        details_by_crop[crop_key]["fertilizer"]["top_dressing"].append(
            f"Soil pH profile in dataset: {ph_summary}."
        )

    return details_by_crop


@lru_cache(maxsize=1)
def _load_details() -> dict[str, dict[str, Any]]:
    if not _DATA_PATH.exists():
        return {}
    with _DATA_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def get_crop_details(crop_name: str) -> dict[str, Any] | None:
    if not crop_name:
        return None
    data = _load_details()
    dataset_data = _load_dataset_details()
    key = normalize_crop_key(crop_name)
    key = _ALIASES.get(key, key)
    return data.get(key) or dataset_data.get(key)


__all__ = ["get_crop_details", "normalize_crop_key"]
