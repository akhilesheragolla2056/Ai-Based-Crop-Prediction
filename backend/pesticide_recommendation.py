"""Translate disease outcomes into pesticide recommendations."""

from __future__ import annotations

from dataclasses import dataclass

from src.features import advise_pesticide, list_supported_diseases


@dataclass(frozen=True, slots=True)
class PesticidePlan:
    disease: str
    chemical: str
    dosage: str
    frequency: str
    organic_alternative: str
    safety: str
    severity_note: str


def recommend_pesticide(disease: str, severity: str | None = None) -> PesticidePlan:
    advice = advise_pesticide(disease, severity=severity)
    return PesticidePlan(
        disease=advice.disease.title(),
        chemical=advice.chemical_name,
        dosage=advice.chemical_dosage_per_acre,
        frequency=advice.application_frequency,
        organic_alternative=advice.organic_option,
        safety=advice.safety_guidance,
        severity_note=advice.severity_adjustment,
    )


def supported_diseases() -> tuple[str, ...]:
    return tuple(d.title() for d in list_supported_diseases())


__all__ = ["PesticidePlan", "recommend_pesticide", "supported_diseases"]
