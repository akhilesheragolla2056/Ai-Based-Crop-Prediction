"""Dataset ingestion utilities for the crop recommendation project."""

from __future__ import annotations

import os
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Iterable, Sequence

import requests

from src.utils.config import PATHS

__all__ = [
    "DatasetInfo",
    "DatasetDownloadError",
    "download_dataset",
    "get_default_dataset_path",
]


class DatasetDownloadError(RuntimeError):
    """Raised when the dataset cannot be downloaded or verified."""


@dataclass(slots=True)
class DatasetInfo:
    """Metadata describing a dataset mirror."""

    url: str
    description: str


DATASET_MIRRORS: tuple[DatasetInfo, ...] = (
    DatasetInfo(
        url="https://raw.githubusercontent.com/dphi-official/Datasets/master/Crop_recommendation.csv",
        description="DPhi public GitHub mirror",
    ),
    DatasetInfo(
        url="https://raw.githubusercontent.com/insaid2018/Term-Project/master/Term%202%20-%20Project%20Crop%20Recommendation%20System/Data/Crop_recommendation.csv",
        description="Insaid teaching repository mirror",
    ),
)

DEFAULT_EXPECTED_SHA256 = os.getenv(
    "CROP_DATASET_SHA256",
    "1c75a44aa8562f02d293baff342a2aa4bae442bfc9a7da478f4a45f307319813",
)


def _write_stream_to_file(url: str, target: Path) -> None:
    with requests.get(url, timeout=60, stream=True) as response:
        response.raise_for_status()
        with target.open("wb") as file_handle:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file_handle.write(chunk)


def _compute_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as file_handle:
        for block in iter(lambda: file_handle.read(131072), b""):
            digest.update(block)
    return digest.hexdigest()


def _validate_checksum(path: Path, expected: str | None) -> bool:
    if expected is None:
        return True
    return _compute_sha256(path) == expected


def _attempt_download(mirrors: Sequence[DatasetInfo], target_path: Path) -> DatasetInfo:
    last_error: Exception | None = None
    for mirror in mirrors:
        try:
            _write_stream_to_file(mirror.url, target_path)
            return mirror
        except Exception as error:  # noqa: BLE001 - propagate cause later
            last_error = error
    raise DatasetDownloadError("All dataset mirrors failed") from last_error


def _candidate_mirrors() -> tuple[DatasetInfo, ...]:
    mirrors: list[DatasetInfo] = []
    custom_url = os.getenv("CROP_DATASET_URL")
    if custom_url:
        mirrors.append(
            DatasetInfo(
                url=custom_url,
                description="Custom URL provided via CROP_DATASET_URL",
            )
        )
    mirrors.extend(DATASET_MIRRORS)
    return tuple(mirrors)


def get_default_dataset_path(destination_dir: Path | None = None) -> Path:
    target_dir = destination_dir or PATHS.data_raw
    return target_dir / "crop_recommendation.csv"


def download_dataset(
    destination_dir: Path | None = None,
    *,
    overwrite: bool = False,
    verify_checksum: bool = True,
) -> Path:
    """Download and verify the crop recommendation dataset.

    Parameters
    ----------
    destination_dir:
        Directory where the dataset will be saved. Defaults to ``PATHS.data_raw``.
    overwrite:
        If ``True``, redownload even when the file already exists.
    verify_checksum:
        Skip SHA-256 verification when ``False``.
    """

    target_dir = destination_dir or PATHS.data_raw
    target_dir.mkdir(parents=True, exist_ok=True)
    dataset_path = get_default_dataset_path(target_dir)
    expected_checksum = DEFAULT_EXPECTED_SHA256

    if not overwrite and dataset_path.exists():
        if not verify_checksum or _validate_checksum(dataset_path, expected_checksum):
            source_file = dataset_path.with_suffix(".source")
            if not source_file.exists():
                source_file.write_text("pre-existing", encoding="utf-8")
            return dataset_path

    mirrors = _candidate_mirrors()
    if not mirrors:
        raise DatasetDownloadError(
            "No dataset sources configured. Set CROP_DATASET_URL to a valid CSV URL."
        )

    mirror = _attempt_download(mirrors, dataset_path)

    if verify_checksum and not _validate_checksum(dataset_path, expected_checksum):
        raise DatasetDownloadError("Checksum mismatch after download")

    dataset_path.with_suffix(".source").write_text(
        f"{mirror.description} | {mirror.url}",
        encoding="utf-8",
    )
    return dataset_path
