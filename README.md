# AI-Based Crop Recommendation Platform

Production-ready machine learning system that recommends the top three crops and expected yield category based on soil nutrients and climate indicators. Designed for rapid hackathon demos with a clear path to market deployment.

## Key Features

- Automated dataset ingestion from trusted public sources with checksum validation.
- Modular training pipeline supporting experiment tracking and hyperparameter tuning.
- Top-3 crop ranking with yield category heuristics and agronomic tips.
- Streamlit web app for farmer-facing interactions.
- Deployment ready structure with Docker, environment-based configuration, and CI hooks.

## Repository Layout

```
.
├── app/                  # Streamlit UI and deployment assets
├── artifacts/            # Persisted models, metrics, and reports
├── data/                 # Raw and processed datasets
├── docs/                 # Design docs, deployment guides, and presentations
├── notebooks/            # Exploratory data analysis and experimentation
├── scripts/              # Command line utilities (ingest, train, evaluate)
├── src/                  # Core Python package for data, features, models, pipelines
└── README.md
```

## Quick Start

1. Create and activate a Python 3.11 environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Download the dataset: `python scripts/download_dataset.py` (use `--url` or `CROP_DATASET_URL` if mirrors are unavailable).
4. Train the baseline model: `python scripts/train_model.py` (coming soon).
5. Launch the Streamlit app: `streamlit run app/main.py`.

## Dataset Ingestion

The dataset downloader checks a small set of known public mirrors. If they are unavailable, provide a fallback URL or checksum:

- `python scripts/download_dataset.py --url https://example.com/Crop_recommendation.csv`
- Set `CROP_DATASET_URL` and, optionally, `CROP_DATASET_SHA256` in a `.env` file.
- Pass `--skip-checksum` when working with exploratory or unpublished data sources.

## Roadmap

- Integrate experiment tracking (MLflow or Weights & Biases).
- Add weather-API enrichment for near-real-time predictions.
- Build RESTful inference service and container orchestration manifests.
- Implement continuous deployment pipeline targeting Azure Web Apps.

## License

To be determined.
