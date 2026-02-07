"""Command-line utility to download the crop recommendation dataset."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

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


if __name__ == "__main__":
    sys.exit(main())
