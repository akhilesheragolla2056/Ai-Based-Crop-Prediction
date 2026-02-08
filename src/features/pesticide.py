"""Pesticide advisory logic linked to crop disease detection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

__all__ = [
    "PesticideAdvice",
    "PesticideAdviser",
    "advise_pesticide",
    "list_supported_diseases",
]


@dataclass(frozen=True, slots=True)
class PesticideAdvice:
    disease: str
    chemical_name: str
    chemical_dosage_per_acre: str
    application_frequency: str
    organic_option: str
    safety_guidance: str
    severity_adjustment: str


class PesticideAdviser:
    """Translate disease diagnosis into actionable pesticide plans."""

    _CATALOG: Final[dict[str, dict[str, str]]] = {
        "rice blast": {
            "chemical_name": "Tricyclazole 75% WP",
            "dosage": "0.6 kg in 500 L water",
            "frequency": "Apply at early stages and repeat after 10 days",
            "organic": "Neem oil (3%) with sticking agent",
            "safety": "Avoid inhalation, wear mask and gloves, do not spray near open water bodies.",
        },
        "sheath blight": {
            "chemical_name": "Hexaconazole 5% SC",
            "dosage": "1 L in 500 L water",
            "frequency": "Two sprays at 7-day interval",
            "organic": "Pseudomonas fluorescens foliar spray",
            "safety": "Use protective goggles, avoid evening sprays to reduce drift.",
        },
        "leaf rust": {
            "chemical_name": "Propiconazole 25% EC",
            "dosage": "0.5 L in 400 L water",
            "frequency": "Apply at first signs, repeat in 14 days if needed",
            "organic": "Sulphur dusting (80% WP) at 10 kg/ha",
            "safety": "Wear long sleeves and boots, dispose containers responsibly.",
        },
        "powdery mildew": {
            "chemical_name": "Wettable sulphur 80% WP",
            "dosage": "2.5 kg in 500 L water",
            "frequency": "Repeat at 10-day interval during favourable weather",
            "organic": "Potassium bicarbonate + horticultural oil spray",
            "safety": "Avoid inhalation; sulphur irritates eyes and skin, keep children away.",
        },
        "bacterial leaf blight": {
            "chemical_name": "Copper oxychloride 50% WP",
            "dosage": "3 kg in 600 L water",
            "frequency": "Two sprays at 5-day interval",
            "organic": "Fermented cow dung + asafoetida foliar extract",
            "safety": "Use PPE, copper residues can burn skin; clean equipment thoroughly.",
        },
    }

    _GENERIC: Final[dict[str, str]] = {
        "chemical_name": "Carbendazim 50% WP",
        "dosage": "1 kg in 500 L water",
        "frequency": "Repeat every 12 days if symptoms persist",
        "organic": "Garlic-chilli-kadukkai (GCK) extract foliar spray",
        "safety": "Always use gloves, mask, and avoid spraying under strong wind.",
    }

    def advise(
        self, disease_name: str, *, severity: str | None = None
    ) -> PesticideAdvice:
        """Return pesticide plan adjusted for the reported severity."""

        key = disease_name.strip().lower()
        plan = self._CATALOG.get(key, self._GENERIC)
        severity_note = self._severity_guidance(severity)
        return PesticideAdvice(
            disease=disease_name,
            chemical_name=plan["chemical_name"],
            chemical_dosage_per_acre=plan["dosage"],
            application_frequency=plan["frequency"],
            organic_option=plan["organic"],
            safety_guidance=plan["safety"],
            severity_adjustment=severity_note,
        )

    @staticmethod
    def _severity_guidance(severity: str | None) -> str:
        if severity is None:
            return "Monitor plot after application; adjust based on field scouting."
        normalized = severity.lower()
        if normalized == "high":
            return "High severity detected: tighten spray interval and integrate field sanitation."
        if normalized == "medium":
            return "Medium severity: follow label interval and reassess in 5-7 days."
        if normalized == "low":
            return "Low severity: single spray plus organic alternative may suffice."
        return "Monitor plot after application; adjust based on field scouting."


def advise_pesticide(
    disease_name: str, *, severity: str | None = None
) -> PesticideAdvice:
    """Convenience wrapper for UI code."""

    return PesticideAdviser().advise(disease_name, severity=severity)


def list_supported_diseases() -> tuple[str, ...]:
    """Return catalogued diseases for dropdown menus."""

    return tuple(sorted(PesticideAdviser._CATALOG.keys()))
