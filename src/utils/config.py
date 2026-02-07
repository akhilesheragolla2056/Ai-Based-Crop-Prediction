"""Centralized configuration helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from a .env file if present.
load_dotenv()


@dataclass(frozen=True, slots=True)
class Paths:
    """Project path configuration for datasets and artifacts."""

    root: Path = Path(__file__).resolve().parents[2]

    @property
    def data_raw(self) -> Path:
        return self.root / "data" / "raw"

    @property
    def data_processed(self) -> Path:
        return self.root / "data" / "processed"

    @property
    def artifacts_models(self) -> Path:
        return self.root / "artifacts" / "models"

    @property
    def artifacts_metrics(self) -> Path:
        return self.root / "artifacts" / "metrics"


PATHS = Paths()
