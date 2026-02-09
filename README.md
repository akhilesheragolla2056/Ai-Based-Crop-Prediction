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

1. Create and activate a Python 3.11 environment (Python 3.12+ is not yet supported). See [docs/environment-setup.md](docs/environment-setup.md) for detailed steps on Windows.
2. Install dependencies: `pip install -r requirements.txt`.
3. Download the dataset: `python scripts/download_dataset.py` (use `--url` or `CROP_DATASET_URL` if mirrors are unavailable).
4. Train the baseline model: `python scripts/train_model.py`.
5. Launch the Streamlit app: `streamlit run app/main.py` (requires a trained model under `artifacts/models/`).

### Weather API Setup

The Streamlit UI supports auto-filling temperature, humidity, and rainfall using live weather providers while still allowing manual overrides. Configure one of the following environment variables before launching the app:

- `OPENWEATHER_API_KEY` for [OpenWeather Current Weather](https://openweathermap.org/current)
- `WEATHERBIT_API_KEY` for [Weatherbit Current Conditions](https://www.weatherbit.io/api/weather-current)

Set the variable in your shell (or `.env`) and restart Streamlit:

```powershell
$env:OPENWEATHER_API_KEY = "your-key-here"
streamlit run app/main.py
```

If neither key is set the live fetch button will show an error and the manual inputs remain available.

## Dataset Ingestion

The dataset downloader checks a small set of known public mirrors. If they are unavailable, provide a fallback URL, checksum, or use the Kaggle workflow:

- `python scripts/download_dataset.py --url https://example.com/Crop_recommendation.csv`
- Set `CROP_DATASET_URL` and, optionally, `CROP_DATASET_SHA256` in a `.env` file.
- Pass `--skip-checksum` when working with exploratory or unpublished data sources.
- Use the Kaggle API: `python scripts/download_dataset.py --use-kaggle --kaggle-dataset atharvaingle/crop-recommendation-dataset --kaggle-file Crop_recommendation.csv`

## Model Training

- The training entry point lives at `scripts/train_model.py`. Use `--metrics-only` during CI to skip artifact persistence.
- Models and metrics are stored under `artifacts/models` and `artifacts/metrics` respectively.
- Hyperparameters (estimators, depth, split criteria) are configurable through CLI flags or by extending `TrainingConfig`.
- The resulting pipeline exports class probabilities, enabling top-3 crop recommendations, yield categories, and nutrient advisory overlays in the Streamlit app.

## Roadmap

- Integrate experiment tracking (MLflow or Weights & Biases).
- Enhance weather-driven insights with historical anomaly detection.
- Build RESTful inference service and container orchestration manifests.
- Implement continuous deployment pipeline targeting Azure Web Apps.

## License

To be determined.
