from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "crop_details.json"

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
    key = normalize_crop_key(crop_name)
    key = _ALIASES.get(key, key)
    return data.get(key)


__all__ = ["get_crop_details", "normalize_crop_key"]
