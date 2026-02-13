# AI Based Crop Prediction

AI-powered crop advisory platform built with Streamlit and ML models for:
- Crop recommendation (top 3 crops)
- Fertilizer guidance
- Water and weather insights
- Pest and disease suggestions
- Yield projection
- AI chat assistant with dataset fallback

## Tech Stack
- Python 3.11
- Streamlit
- Pandas, NumPy, scikit-learn
- Requests, python-dotenv
- OpenWeather API (optional live weather)
- OpenAI/Gemini API (optional AI chat enhancement)

## Project Structure
```text
.
|-- app/                      # Streamlit entry wrapper
|-- backend/                  # Domain services (weather, market, rainfall, etc.)
|-- frontend/                 # Main Streamlit UI and components
|-- modules/                  # AI chatbot logic
|-- src/                      # ML/data pipeline code
|-- scripts/                  # Dataset download and training scripts
|-- data/                     # Raw and processed datasets
|-- artifacts/                # Trained models and metrics
|-- docs/                     # Additional documentation
|-- requirements.txt
|-- pyproject.toml
|-- README.md
```

## Prerequisites
- Python `3.11.x` (project targets `>=3.11,<3.12`)
- Git
- Optional API keys for weather and AI features

## Setup (Local)
1. Clone repository.
```bash
git clone <your-repo-url>
cd "Ai Based Crop Prediction"
```

2. Create virtual environment.
```powershell
py -3.11 -m venv .venv
```

3. Activate environment.
```powershell
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies.
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

5. Configure environment.
```bash
copy .env.example .env
```
Then update `.env` values as needed.

## Environment Variables
Use `.env` in project root.

- `OPENWEATHER_API_KEY`: Optional, enables live weather autofetch.
- `OPENAI_API_KEY`: Optional, enables OpenAI chat responses.
- `OPENAI_MODEL`: Optional, default `gpt-4o-mini`.
- `OPENAI_EMBEDDING_MODEL`: Optional, default `text-embedding-3-small`.
- `GEMINI_API_KEY`: Optional, enables Gemini chat responses.
- `GEMINI_MODEL`: Optional, default `gemini-1.5-flash`.
- `RAG_REBUILD`: Optional, set `1` to rebuild embeddings cache.
- `CROP_DATASET_URL`: Optional custom dataset source URL.
- `CROP_DATASET_SHA256`: Optional checksum for dataset validation.

If AI keys are missing or limits are reached, chatbot falls back to dataset-based advisory.

## Dataset Setup
Download dataset into `data/raw/`:
```bash
python scripts/download_dataset.py
```

Optional custom source:
```bash
python scripts/download_dataset.py --url <csv-url> --checksum <sha256>
```

Optional Kaggle flow:
```bash
python scripts/download_dataset.py --use-kaggle --kaggle-dataset atharvaingle/crop-recommendation-dataset --kaggle-file Crop_recommendation.csv
```

## Train Model
```bash
python scripts/train_model.py
```

Expected artifact:
- `artifacts/models/crop_recommender.joblib`

## Run the App
Use either entry:
```bash
streamlit run app/main.py
```
or
```bash
streamlit run frontend/app.py
```

Default local URL:
- `http://localhost:8501`

## Deployment
### Streamlit Community Cloud
1. Push repo to GitHub.
2. Create new app in Streamlit Cloud.
3. Set main file path to `app/main.py`.
4. Add required secrets/environment variables.
5. Deploy.

### Docker/Render/Railway
1. Build using `Dockerfile`.
2. Start command uses `start.sh` (or Procfile command).
3. Expose `PORT` (defaults to `8501`).

## Common Issues
- `OPENWEATHER_API_KEY is not configured`: add key or use manual input.
- No crop recommendations: verify dataset exists and model artifact is trained.
- Chat AI unavailable: app will still return dataset-based responses.
- Python version issues: use Python 3.11.

## Git Workflow (Suggested)
```bash
git checkout -b docs/update-readme-license
git add README.md .env.example LICENSE
git commit -m "docs: improve README and add MIT license"
git push origin docs/update-readme-license
```

## License
This project is licensed under the MIT License. See `LICENSE`.
