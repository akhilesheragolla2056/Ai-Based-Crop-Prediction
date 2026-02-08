"""Train the crop recommendation model and persist artifacts."""

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import asdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.training import (  # noqa: E402 - import after sys.path change
    TrainingConfig,
    save_metrics,
    save_model,
    train_model,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the crop recommendation model.")
    parser.add_argument(
        "--n-estimators", type=int, default=300, help="Number of trees."
    )
    parser.add_argument(
        "--max-depth", type=int, default=None, help="Maximum tree depth."
    )
    parser.add_argument(
        "--min-samples-split",
        type=int,
        default=2,
        help="Minimum samples required to split an internal node.",
    )
    parser.add_argument(
        "--min-samples-leaf",
        type=int,
        default=1,
        help="Minimum samples required at a leaf node.",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Proportion of data reserved for evaluation.",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random seed for reproducibility.",
    )
    parser.add_argument(
        "--metrics-only",
        action="store_true",
        help="Skip saving the trained model and only output metrics (useful for CI).",
    )
    return parser.parse_args()


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main() -> int:
    configure_logging()
    args = parse_args()

    config = TrainingConfig(
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        min_samples_split=args.min_samples_split,
        min_samples_leaf=args.min_samples_leaf,
        test_size=args.test_size,
        random_state=args.random_state,
    )

    logging.info("Starting training with config: %s", asdict(config))

    try:
        artifacts = train_model(config=config)
    except FileNotFoundError as error:
        logging.error("Dataset not found: %s", error)
        logging.info("Run scripts/download_dataset.py before training.")
        return 1

    metrics_path = save_metrics(artifacts.metrics)
    logging.info("Saved metrics to %s", metrics_path)

    if not args.metrics_only:
        model_path = save_model(artifacts)
        logging.info("Saved model to %s", model_path)
    else:
        logging.info("Skipping model persistence due to --metrics-only flag.")

    logging.info("Training complete. Accuracy: %.3f", artifacts.metrics["accuracy"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
