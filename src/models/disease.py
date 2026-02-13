"""Crop disease detection utilities with optional deep-learning backend."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

import numpy as np
from PIL import Image

__all__ = ["DiseasePrediction", "CropDiseaseClassifier"]


@dataclass(frozen=True, slots=True)
class DiseasePrediction:
    """Structured disease output used by the Streamlit experience."""

    disease: str
    severity: str
    confidence: float
    symptom_summary: str


class CropDiseaseClassifier:
    """Predict crop leaf diseases from images.

    This implementation first tries to load a lightweight torchvision MobileNet
    model if PyTorch is available. If those optional dependencies are missing or
    weights cannot be loaded, it falls back to an explainable heuristic based on
    basic colour statistics. Hackathon teams can later plug in their own
    fine-tuned CNN by supplying a callable ``inference_backend``.
    """

    _HEURISTIC_LIBRARY: Final[dict[str, dict[str, Any]]] = {
        "leaf rust": {
            "symptom": "Rust-coloured pustules and brown lesions spreading from margins.",
            "severity_scale": (0.3, 0.6, 0.85),
        },
        "bacterial leaf blight": {
            "symptom": "Yellowing along veins with water-soaked stripes spreading quickly.",
            "severity_scale": (0.25, 0.55, 0.8),
        },
        "powdery mildew": {
            "symptom": "Whitish powdery growth on surfaces, distorted young tissues.",
            "severity_scale": (0.2, 0.5, 0.75),
        },
        "healthy": {
            "symptom": "Leaf appears vigorous with balanced chlorophyll and minimal stress.",
            "severity_scale": (0.0, 0.2, 0.35),
        },
    }

    def __init__(self, inference_backend: Any | None = None) -> None:
        self._backend = inference_backend or self._try_load_torch_backend()

    def predict(
        self, image_source: Path | str | Image.Image | bytes
    ) -> DiseasePrediction:
        image = self._load_image(image_source)
        if self._backend is not None:
            return self._predict_with_backend(image)
        return self._predict_with_heuristics(image)

    @staticmethod
    def _load_image(source: Path | str | Image.Image | bytes) -> Image.Image:
        if isinstance(source, Image.Image):
            return source.convert("RGB")
        if isinstance(source, (str, Path)):
            return Image.open(source).convert("RGB")
        # Assume bytes-like object
        from io import BytesIO

        return Image.open(BytesIO(source)).convert("RGB")

    def _predict_with_backend(self, image: Image.Image) -> DiseasePrediction:
        logits, labels = self._backend(image)
        probabilities = self._softmax(logits)
        index = int(np.argmax(probabilities))
        if index >= len(labels):
            # Backend logits do not align with provided labels; fall back to heuristics.
            return self._predict_with_heuristics(image)

        confidence = float(probabilities[index])
        disease_label = labels[index]
        info = self._HEURISTIC_LIBRARY.get(
            disease_label, self._HEURISTIC_LIBRARY["healthy"]
        )
        severity = self._map_severity(confidence, info["severity_scale"])
        return DiseasePrediction(
            disease=disease_label,
            severity=severity,
            confidence=confidence,
            symptom_summary=info["symptom"],
        )

    def _predict_with_heuristics(self, image: Image.Image) -> DiseasePrediction:
        array = np.asarray(image.resize((224, 224))) / 255.0
        mean_channels = array.mean(axis=(0, 1))
        greenness = mean_channels[1]
        redness = mean_channels[0]
        blueness = mean_channels[2]
        variance = array.var()

        if greenness < 0.35 and redness > 0.35:
            label = "leaf rust"
            score = float(min(0.95, redness + variance))
        elif greenness < 0.4 and blueness > 0.3:
            label = "bacterial leaf blight"
            score = float(min(0.9, blueness + (1 - greenness)))
        elif variance > 0.06 and blueness < 0.45:
            label = "powdery mildew"
            score = float(min(0.85, variance * 4))
        else:
            label = "healthy"
            score = float(max(0.6, greenness))

        library_entry = self._HEURISTIC_LIBRARY[label]
        severity = self._map_severity(score, library_entry["severity_scale"])
        return DiseasePrediction(
            disease=label,
            severity=severity,
            confidence=score,
            symptom_summary=library_entry["symptom"],
        )

    @staticmethod
    def _map_severity(score: float, scale: tuple[float, float, float]) -> str:
        low_threshold, medium_threshold, high_threshold = scale
        if score >= high_threshold:
            return "High"
        if score >= medium_threshold:
            return "Medium"
        if score >= low_threshold:
            return "Low"
        return "Very Low"

    @staticmethod
    def _softmax(logits: np.ndarray) -> np.ndarray:
        exps = np.exp(logits - np.max(logits))
        return exps / np.sum(exps)

    @staticmethod
    def _try_load_torch_backend():
        try:
            import torch
            from torchvision import models, transforms
        except Exception:  # noqa: BLE001 - optional dependency may not exist
            return None

        try:
            model = models.mobilenet_v3_small(
                weights=models.MobileNet_V3_Small_Weights.DEFAULT
            )
        except Exception:  # noqa: BLE001 - download or weight initialisation failed
            return None

        model.eval()
        labels = list(CropDiseaseClassifier._HEURISTIC_LIBRARY.keys())

        preprocess = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)
                ),
            ]
        )

        def _backend(image: Image.Image):
            with torch.no_grad():
                tensor = preprocess(image).unsqueeze(0)
                outputs = model(tensor)
            logits = outputs.squeeze(0).detach().cpu().numpy()
            return logits, labels

        return _backend
