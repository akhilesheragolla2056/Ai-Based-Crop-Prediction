"""Disease diagnosis services free of UI dependencies."""

from __future__ import annotations

from dataclasses import dataclass

from backend.utils import get_disease_classifier


@dataclass(frozen=True, slots=True)
class DiseaseDiagnosis:
    crop: str
    disease: str
    severity: str
    symptoms: str
    confidence: float


def diagnose_disease(crop: str, image_bytes: bytes) -> DiseaseDiagnosis:
    classifier = get_disease_classifier()
    prediction = classifier.predict(image_bytes)
    return DiseaseDiagnosis(
        crop=crop.title(),
        disease=prediction.disease.title(),
        severity=prediction.severity.title(),
        symptoms=prediction.symptom_summary,
        confidence=prediction.confidence,
    )


__all__ = ["DiseaseDiagnosis", "diagnose_disease"]
