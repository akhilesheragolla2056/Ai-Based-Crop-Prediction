"""Generate agronomic advisories based on soil and climate inputs."""

from __future__ import annotations

from typing import Iterable, Mapping

__all__ = ["generate_soil_health_tips"]


def generate_soil_health_tips(features: Mapping[str, float]) -> tuple[str, ...]:
    """Return actionable soil-health suggestions derived from feature values."""

    tips: list[str] = []
    tips.extend(_analyze_macro_nutrients(features))
    tips.extend(_analyze_ph(features))
    tips.extend(_analyze_climate(features))
    return tuple(dict.fromkeys(tips))  # Preserve order while removing duplicates.


def _analyze_macro_nutrients(features: Mapping[str, float]) -> Iterable[str]:
    suggestions: list[str] = []

    if features["N"] < 50:
        suggestions.append(
            "Nitrogen levels are low; consider applying urea or incorporating legume cover crops."
        )
    elif features["N"] > 120:
        suggestions.append(
            "Nitrogen is high; reduce nitrogenous fertilizers to avoid foliage burn."
        )

    if features["P"] < 40:
        suggestions.append(
            "Phosphorus deficiency detected; use rock phosphate or DAP before sowing."
        )
    elif features["P"] > 110:
        suggestions.append(
            "Phosphorus is excessive; switch to balanced NPK blends to prevent soil fixation."
        )

    if features["K"] < 40:
        suggestions.append(
            "Potassium is low; supplement with muriate of potash or apply wood ash."
        )
    elif features["K"] > 120:
        suggestions.append(
            "Potassium level is high; avoid additional potassic fertilizers this season."
        )

    return suggestions


def _analyze_ph(features: Mapping[str, float]) -> Iterable[str]:
    ph_value = features["ph"]
    if ph_value < 5.5:
        return (
            "Soil is acidic; add agricultural lime or dolomite to raise pH towards neutral.",
        )
    if ph_value > 7.5:
        return (
            "Soil is alkaline; apply elemental sulfur or organic compost to lower pH gradually.",
        )
    return ("Soil pH is within optimal range for most crops.",)


def _analyze_climate(features: Mapping[str, float]) -> Iterable[str]:
    suggestions: list[str] = []

    if features["humidity"] < 30:
        suggestions.append(
            "Low humidity may stress moisture-loving crops; prioritize drought-tolerant varieties."
        )
    elif features["humidity"] > 85:
        suggestions.append(
            "High humidity increases fungal risk; schedule preventive fungicide sprays."
        )

    if features["rainfall"] < 80:
        suggestions.append(
            "Limited rainfall expected; plan supplemental irrigation or select low-water crops."
        )
    elif features["rainfall"] > 250:
        suggestions.append(
            "Excess rainfall forecast; ensure proper drainage to prevent waterlogging."
        )

    temperature = features["temperature"]
    if temperature < 15:
        suggestions.append(
            "Cool temperatures; opt for Rabi-season crops or use nursery trays to raise seedlings."
        )
    elif temperature > 35:
        suggestions.append(
            "High temperatures predicted; implement mulching to conserve soil moisture."
        )

    return suggestions
