"""Command-line utility to download the crop recommendation dataset."""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import sys
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.ingestion import DatasetDownloadError, download_dataset
from src.utils.config import PATHS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download the Indian crop recommendation dataset into data/raw.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Optional destination directory. Defaults to the project data/raw folder.",
    )
    parser.add_argument(
        "--url",
        type=str,
        default=None,
        help="Custom dataset URL override (also available via CROP_DATASET_URL env var).",
    )
    parser.add_argument(
        "--checksum",
        type=str,
        default=None,
        help="Expected SHA-256 checksum override (or set CROP_DATASET_SHA256 env var).",
    )
    parser.add_argument(
        "--use-kaggle",
        action="store_true",
        help=(
            "Download via Kaggle API (requires kaggle package and authenticated Kaggle credentials)."
        ),
    )
    parser.add_argument(
        "--kaggle-dataset",
        type=str,
        default="atharvaingle/crop-recommendation-dataset",
        help="Kaggle dataset slug to use with --use-kaggle.",
    )
    parser.add_argument(
        "--kaggle-file",
        type=str,
        default="Crop_recommendation.csv",
        help="Filename inside the Kaggle dataset to download.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Redownload the dataset even when it already exists.",
    )
    parser.add_argument(
        "--skip-checksum",
        action="store_true",
        help="Skip SHA-256 verification (not recommended).",
    )
    return parser.parse_args()


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )


def main() -> int:
    """Entry point for dataset download script."""

    configure_logging()
    args = parse_args()
    destination = args.output_dir or PATHS.data_raw

    if args.use_kaggle:
        try:
            dataset_path = download_with_kaggle(
                dataset=args.kaggle_dataset,
                file_name=args.kaggle_file,
                destination=destination,
                overwrite=args.force,
            )
        except ModuleNotFoundError:
            logging.error(
                "Kaggle Python package not installed. Run 'pip install kaggle' in your environment."
            )
            return 1
        except Exception as error:  # noqa: BLE001 - propagate message to user
            logging.error("Kaggle download failed: %s", error)
            logging.info(
                "Ensure Kaggle credentials are configured (kaggle.json or environment variables)."
            )
            return 1

        logging.info("Dataset saved to %s", dataset_path)
        logging.info(
            "Source mirror: Kaggle | %s::%s", args.kaggle_dataset, args.kaggle_file
        )
        return 0

    if args.url:
        os.environ["CROP_DATASET_URL"] = args.url
    if args.checksum:
        os.environ["CROP_DATASET_SHA256"] = args.checksum

    try:
        dataset_path = download_dataset(
            destination_dir=destination,
            overwrite=args.force,
            verify_checksum=not args.skip_checksum,
        )
    except DatasetDownloadError as error:
        logging.error("Dataset download failed: %s", error)
        if error.__cause__ is not None:
            logging.debug("Root cause: %s", error.__cause__)
        logging.info(
            "Provide a custom URL via --url or CROP_DATASET_URL environment variable."
        )
        return 1

    source_marker = dataset_path.with_suffix(".source")
    source_info = (
        source_marker.read_text(encoding="utf-8")
        if source_marker.exists()
        else "unknown"
    )
    logging.info("Dataset saved to %s", dataset_path)
    logging.info("Source mirror: %s", source_info)
    return 0


def download_with_kaggle(
    *,
    dataset: str,
    file_name: str,
    destination: Path,
    overwrite: bool,
) -> Path:
    """Download the dataset file from Kaggle and place it in ``destination``."""

    from kaggle.api.kaggle_api_extended import KaggleApi

    destination.mkdir(parents=True, exist_ok=True)
    target_path = destination / "crop_recommendation.csv"

    if target_path.exists() and not overwrite:
        return target_path

    api = KaggleApi()
    api.authenticate()

    with TemporaryDirectory(prefix="crop-dataset-") as temp_dir:
        api.dataset_download_file(
            dataset,
            file_name,
            path=temp_dir,
            force=overwrite,
            quiet=False,
        )

        download_dir = Path(temp_dir)
        zipped_path = download_dir / f"{file_name}.zip"
        if zipped_path.exists():
            with zipfile.ZipFile(zipped_path) as archive:
                archive.extractall(download_dir)
            extracted_path = download_dir / file_name
        else:
            extracted_path = download_dir / file_name

        if not extracted_path.exists():
            raise FileNotFoundError(
                "Expected file not found in Kaggle download. Check --kaggle-file name."
            )

        shutil.move(str(extracted_path), target_path)

    target_path.with_suffix(".source").write_text(
        f"Kaggle | {dataset}::{file_name}",
        encoding="utf-8",
    )
    return target_path


if __name__ == "__main__":
    sys.exit(main())
