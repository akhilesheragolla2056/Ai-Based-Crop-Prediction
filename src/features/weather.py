"""Weather-aware advisories for crop planning."""

from __future__ import annotations

from typing import Mapping

__all__ = ["generate_weather_warnings"]


def generate_weather_warnings(
    features: Mapping[str, float], crop: str
) -> tuple[str, ...]:
    """Summarise key weather risks with prescriptive guidance."""

    rainfall = features.get("rainfall", 0.0)
    temperature = features.get("temperature", 0.0)
    humidity = features.get("humidity", 0.0)

    warnings: list[str] = []

    if rainfall < 80:
        warnings.append(
            "Rainfall outlook is low; prefer drought-tolerant crops or secure irrigation before planting {}.".format(
                crop.title()
            )
        )
        warnings.append(
            "Delay puddled rice planting; adopt direct-seeded rice or millets instead."
        )
    elif rainfall > 260:
        warnings.append(
            "Excess rainfall expected; ensure drainage and consider short-duration varieties to escape waterlogging."
        )

    if temperature > 35:
        warnings.append(
            "High temperature stress likely; use mulching and evening irrigation to reduce canopy heat."
        )
    elif temperature < 15:
        warnings.append(
            "Cool spell forecast; raise seedlings in protected nursery before transplanting."
        )

    if humidity > 85:
        warnings.append(
            "Very high humidity may trigger fungal outbreaks; schedule preventive fungicide sprays."
        )
    elif humidity < 30:
        warnings.append(
            "Dry air can cause rapid evapotranspiration; adopt antitranspirant sprays or shade nets for tender crops."
        )

    if not warnings:
        warnings.append(
            "Weather outlook is favourable; maintain routine scouting and irrigation schedule."
        )

    return tuple(dict.fromkeys(warnings))
