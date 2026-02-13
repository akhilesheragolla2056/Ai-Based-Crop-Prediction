"""Yield estimation logic combining heuristics and agronomic priors."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np

__all__ = ["YieldPrediction", "YieldEstimator"]


@dataclass(frozen=True, slots=True)
class YieldPrediction:
    crop: str
    yield_level: str
    estimated_quintal_per_acre: float
    confidence: float
    reasoning: str


class YieldEstimator:
    """Estimate yield outcomes using lightweight explainable scores."""

    _TARGETS = {
        "rice": {
            "rainfall": (120, 220),
            "temperature": (20, 32),
            "quintal_per_acre": 22,
        },
        "wheat": {
            "rainfall": (100, 180),
            "temperature": (18, 28),
            "quintal_per_acre": 18,
        },
        "maize": {
            "rainfall": (80, 150),
            "temperature": (21, 34),
            "quintal_per_acre": 20,
        },
        "cotton": {
            "rainfall": (70, 130),
            "temperature": (25, 37),
            "quintal_per_acre": 10,
        },
        "groundnut": {
            "rainfall": (60, 120),
            "temperature": (22, 34),
            "quintal_per_acre": 12,
        },
    }

    def predict(self, crop: str, metrics: Mapping[str, float]) -> YieldPrediction:
        crop_key = crop.strip().lower()
        baseline = self._TARGETS.get(
            crop_key,
            {"rainfall": (80, 180), "temperature": (20, 35), "quintal_per_acre": 15},
        )

        n = metrics.get("N", 90.0)
        p = metrics.get("P", 60.0)
        k = metrics.get("K", 60.0)
        rainfall = metrics.get("rainfall", 120.0)
        temperature = metrics.get("temperature", 28.0)

        nutrient_score = self._nutrient_score(n, p, k)
        climate_score = self._climate_score(rainfall, temperature, baseline)
        aggregate = (0.55 * nutrient_score) + (0.45 * climate_score)
        aggregate = float(np.clip(aggregate, 0.0, 1.0))

        if aggregate >= 0.75:
            level = "High"
        elif aggregate >= 0.45:
            level = "Medium"
        else:
            level = "Low"

        estimated_yield = baseline["quintal_per_acre"] * (0.7 + 0.6 * aggregate)
        confidence = 0.55 + 0.4 * abs(aggregate - 0.5)

        reasoning_parts: list[str] = []
        if nutrient_score < 0.5:
            reasoning_parts.append(
                "Soil nutrients require correction for peak performance."
            )
        else:
            reasoning_parts.append("NPK balance favourable for the crop.")
        if climate_score < 0.5:
            reasoning_parts.append(
                "Weather outlook is a limiting factor; plan risk mitigation."
            )
        else:
            reasoning_parts.append("Weather conditions align with crop comfort zone.")

        return YieldPrediction(
            crop=crop.title(),
            yield_level=level,
            estimated_quintal_per_acre=float(round(estimated_yield, 1)),
            confidence=float(round(confidence, 2)),
            reasoning=" ".join(reasoning_parts),
        )

    @staticmethod
    def _nutrient_score(n: float, p: float, k: float) -> float:
        ideal = np.array([110, 58, 58], dtype=float)
        observed = np.array([n, p, k], dtype=float)
        deviation = np.abs(observed - ideal) / (ideal + 1e-6)
        score = 1.0 - np.mean(np.clip(deviation, 0.0, 1.5)) / 1.5
        return float(np.clip(score, 0.0, 1.0))

    @staticmethod
    def _climate_score(
        rainfall: float, temperature: float, baseline: Mapping[str, tuple[float, float]]
    ) -> float:
        rain_range = baseline["rainfall"]
        temp_range = baseline["temperature"]
        rain_score = YieldEstimator._range_score(rainfall, *rain_range)
        temp_score = YieldEstimator._range_score(temperature, *temp_range)
        return float((rain_score + temp_score) / 2)

    @staticmethod
    def _range_score(value: float, lower: float, upper: float) -> float:
        if lower <= value <= upper:
            return 1.0
        distance = min(abs(value - lower), abs(value - upper))
        spread = (upper - lower) or 1.0
        score = max(0.0, 1 - distance / spread)
        return float(score)
