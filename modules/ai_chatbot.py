from __future__ import annotations

import json
import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

_CROP_DETAILS_PATH = Path("data/crop_details.json")
_SOIL_PROFILES_PATH = Path("data/soil_profiles.csv")
_CROP_DATASET_PATH = Path("data/raw/Crop recommendation dataset.csv")
_EMBEDDINGS_CACHE_PATH = Path("data/ai_agri_embeddings.json")
_DATA_DIR = Path("data")
_RAW_DIR = Path("data/raw")

_NON_AGRI_REPLY = (
    "I am your Agricultural Advisory Assistant. Please ask crop or farming related questions."
)

_LAST_AI_ERROR: str | None = None


def _append_ai_error(message: str) -> None:
    global _LAST_AI_ERROR
    if not message:
        return
    if _LAST_AI_ERROR is None:
        _LAST_AI_ERROR = message
        return
    if message in _LAST_AI_ERROR:
        return
    _LAST_AI_ERROR = f"{_LAST_AI_ERROR} | {message}"

_AGRI_KEYWORDS = {
    "crop",
    "farming",
    "farm",
    "agriculture",
    "agri",
    "soil",
    "fertilizer",
    "fertiliser",
    "water",
    "irrigation",
    "pest",
    "disease",
    "season",
    "kharif",
    "rabi",
    "zaid",
    "harvest",
    "cultivation",
    "sowing",
    "yield",
    "grow",
    "best",
    "suitable",
    "recommend",
    "recommended",
    "seed",
    "variety",
    "varieties",
    "nursery",
    "transplant",
    "spacing",
    "weeding",
    "weed",
    "herbicide",
    "pesticide",
    "fungicide",
    "insecticide",
    "organic",
    "compost",
    "vermicompost",
    "mulch",
    "drip",
    "sprinkler",
    "soil test",
    "ph",
    "salinity",
    "health",
    "nutrition",
    "diet",
    "food",
    "edible",
    "human consumption",
    "millet",
    "millets",
    "ragi",
}

_NON_AGRI_KEYWORDS = {
    "politics",
    "election",
    "movie",
    "film",
    "actor",
    "actress",
    "music",
    "song",
    "sports",
    "cricket",
    "football",
    "basketball",
    "coding",
    "programming",
    "python",
    "java",
    "javascript",
    "react",
    "html",
    "css",
    "travel",
    "tourism",
    "bitcoin",
    "crypto",
    "stock",
    "share market",
}

_TOPIC_KEYWORDS = {
    "cultivation": {"cultivation", "how to grow", "planting", "sowing", "stages"},
    "fertilizer": {"fertilizer", "fertiliser", "npk", "nutrient", "manure"},
    "pest": {"pest", "disease", "fungus", "infection", "spray", "pesticide"},
    "water": {"water", "irrigation", "rainfall", "moisture"},
    "season": {"season", "kharif", "rabi", "zaid", "summer", "winter", "monsoon"},
    "soil": {"soil", "ph", "alkaline", "acidic"},
    "harvest": {"harvest", "maturity", "yield", "post-harvest", "post harvest"},
    "utilization": {
        "uses",
        "use",
        "utilization",
        "utilisation",
        "value addition",
        "processing",
        "food",
        "nutrition",
        "health benefits",
        "benefits",
        "byproducts",
        "by-products",
        "human consumption",
    },
}

_NPK_KEYWORDS = {
    "npk",
    "n:p:k",
    "nitrogen",
    "phosphorus",
    "potassium",
}

_CROP_ALIASES = {
    "ragi": "ragi",
    "fingermillet": "ragi",
    "fingermillets": "ragi",
    "mandua": "ragi",
    "nachni": "ragi",
}

_WATER_REQUIREMENT_FALLBACK_MM = {
    "rice": (1200.0, 2500.0),
    "wheat": (450.0, 650.0),
    "maize": (500.0, 800.0),
    "cotton": (700.0, 1300.0),
    "groundnut": (500.0, 700.0),
    "sugarcane": (1500.0, 2500.0),
    "banana": (1200.0, 2200.0),
    "coffee": (800.0, 1200.0),
    "jowar": (350.0, 600.0),
    "ragi": (350.0, 650.0),
}


def _normalize_text(text: str) -> str:
    return " ".join((text or "").strip().lower().split())


def _normalize_crop_key(name: str) -> str:
    return "".join(ch for ch in _normalize_text(name) if ch.isalnum())


def _safe_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _mode_str(series: pd.Series) -> str:
    cleaned = series.astype(str).str.strip()
    cleaned = cleaned[cleaned != ""]
    if cleaned.empty:
        return "Not specified"
    mode = cleaned.mode()
    return str(mode.iloc[0]) if not mode.empty else str(cleaned.iloc[0])


def _build_dataset_crop_details() -> dict[str, dict[str, Any]]:
    if not _CROP_DATASET_PATH.exists():
        return {}
    try:
        df = pd.read_csv(_CROP_DATASET_PATH)
    except Exception:
        return {}

    if "CROPS" not in df.columns:
        return {}

    result: dict[str, dict[str, Any]] = {}
    grouped = df.groupby(df["CROPS"].astype(str).str.strip().str.lower(), dropna=False)

    for crop_name, group in grouped:
        crop_key = _normalize_crop_key(crop_name)
        if not crop_key:
            continue
        type_of_crop = _mode_str(group.get("TYPE_OF_CROP", pd.Series([], dtype=str)))
        season = _mode_str(group.get("SEASON", pd.Series([], dtype=str)))
        soil = _mode_str(group.get("SOIL", pd.Series([], dtype=str)))
        sown = _mode_str(group.get("SOWN", pd.Series([], dtype=str)))
        harvested = _mode_str(group.get("HARVESTED", pd.Series([], dtype=str)))
        water_source = _mode_str(group.get("WATER_SOURCE", pd.Series([], dtype=str)))

        duration_low = pd.to_numeric(group.get("CROPDURATION"), errors="coerce").dropna()
        duration_high = pd.to_numeric(group.get("CROPDURATION_MAX"), errors="coerce").dropna()
        n_vals = pd.to_numeric(group.get("N"), errors="coerce").dropna()
        p_vals = pd.to_numeric(group.get("P"), errors="coerce").dropna()
        k_vals = pd.to_numeric(group.get("K"), errors="coerce").dropna()
        water_low = pd.to_numeric(group.get("WATERREQUIRED"), errors="coerce").dropna()
        water_high = pd.to_numeric(group.get("WATERREQUIRED_MAX"), errors="coerce").dropna()

        duration_text = "Not specified"
        if not duration_low.empty and not duration_high.empty:
            duration_text = f"{duration_low.mean():.0f}-{duration_high.mean():.0f} days"
        elif not duration_low.empty:
            duration_text = f"{duration_low.mean():.0f} days"

        npk_text = "Apply NPK as per soil test."
        if not n_vals.empty and not p_vals.empty and not k_vals.empty:
            npk_text = (
                f"Dataset baseline N:P:K ~ "
                f"{n_vals.mean():.0f}:{p_vals.mean():.0f}:{k_vals.mean():.0f} (adjust by soil test)."
            )

        water_text = "Use local irrigation scheduling."
        if not water_low.empty and not water_high.empty:
            water_text = (
                f"Estimated water demand: {water_low.mean():.0f}-{water_high.mean():.0f} mm."
            )

        title_name = str(crop_name).strip().title()
        result[crop_key] = {
            "name": title_name,
            "type": type_of_crop.title() if type_of_crop else "Not specified",
            "season": season.title() if season else "Not specified",
            "duration": duration_text,
            "stages": [
                {"name": "Sowing", "days": "NA", "activities": f"Sowing window: {sown}."},
                {"name": "Harvest", "days": "NA", "activities": f"Harvest window: {harvested}."},
            ],
            "fertilizer": {
                "basal": npk_text,
                "top_dressing": ["Split nutrients by crop stage and local recommendation."],
                "fertilizers": ["NPK blends as per local guidance"],
                "organic": "Apply FYM/compost based on field condition.",
            },
            "irrigation": {
                "stage_wise": [water_text],
                "frequency": "Adjust based on rainfall and soil moisture.",
                "notes": f"Soil: {soil}. Water source pattern: {water_source}.",
            },
            "pests": {
                "common_pests": [],
                "common_diseases": [],
                "prevention": "Follow local integrated pest and disease management advisories.",
                "pesticides": [],
            },
            "harvest": {
                "indicators": f"Harvest month in dataset: {harvested}.",
                "yield": "Yield varies by variety and management.",
                "post_harvest": "Dry and store produce safely at recommended moisture.",
            },
        }
    return result


def _build_rag_documents(context_data: dict[str, Any]) -> list[dict[str, str]]:
    documents: list[dict[str, str]] = []

    crop_details = context_data.get("crop_details", {})
    for crop_key, crop in crop_details.items():
        name = str(crop.get("name", crop_key)).title()
        fertilizer = crop.get("fertilizer", {})
        irrigation = crop.get("irrigation", {})
        pests = crop.get("pests", {})
        harvest = crop.get("harvest", {})
        stages = crop.get("stages", [])
        stage_text = " | ".join(
            f"{s.get('name', 'Stage')} ({s.get('days', 'NA')})"
            for s in stages[:4]
        )
        text = (
            f"Crop: {name}\n"
            f"Type: {crop.get('type', 'Not specified')}\n"
            f"Season: {crop.get('season', 'Not specified')}\n"
            f"Duration: {crop.get('duration', 'Not specified')}\n"
            f"Stages: {stage_text}\n"
            f"Soil/Notes: {irrigation.get('notes', 'Not specified')}\n"
            f"Fertilizer: {fertilizer.get('basal', 'Not specified')}\n"
            f"Top dressing: {'; '.join(fertilizer.get('top_dressing', [])[:3])}\n"
            f"Irrigation: {'; '.join(irrigation.get('stage_wise', [])[:3])}\n"
            f"Pests: {', '.join(pests.get('common_pests', [])[:6])}\n"
            f"Diseases: {', '.join(pests.get('common_diseases', [])[:6])}\n"
            f"Prevention: {pests.get('prevention', 'Not specified')}\n"
            f"Harvest: {harvest.get('indicators', 'Not specified')}\n"
            f"Post-harvest: {harvest.get('post_harvest', 'Not specified')}"
        )
        documents.append(
            {
                "id": f"crop::{crop_key}",
                "title": f"{name} crop advisory",
                "text": text,
                "source": "crop_details",
            }
        )

    soil_profiles = context_data.get("soil_profiles", [])
    for idx, soil in enumerate(soil_profiles[:200]):
        region = soil.get("REGION") or soil.get("Region") or soil.get("region") or "Region"
        soil_type = soil.get("SOIL_TYPE") or soil.get("Soil") or soil.get("soil") or "Soil"
        ph = soil.get("PH") or soil.get("ph") or soil.get("pH") or "NA"
        n_val = soil.get("N") or soil.get("n") or "NA"
        p_val = soil.get("P") or soil.get("p") or "NA"
        k_val = soil.get("K") or soil.get("k") or "NA"
        text = (
            f"Region: {region}; Soil: {soil_type}; "
            f"pH: {ph}; N: {n_val}; P: {p_val}; K: {k_val}."
        )
        documents.append(
            {
                "id": f"soil::{idx}",
                "title": f"Soil profile {region}",
                "text": text,
                "source": "soil_profiles",
            }
        )

    documents.append(
        {
            "id": "general::seasons",
            "title": "Seasonal cropping overview",
            "text": (
                "Season guide: Kharif (monsoon), Rabi (winter), Zaid (summer). "
                "Match crop to local climate window and rainfall pattern."
            ),
            "source": "general",
        }
    )
    documents.extend(_build_csv_documents())
    return documents


def _build_csv_documents(chunk_size: int = 200) -> list[dict[str, str]]:
    documents: list[dict[str, str]] = []
    if not _DATA_DIR.exists():
        return documents

    csv_paths = list(_DATA_DIR.rglob("*.csv"))
    for csv_path in csv_paths:
        if not csv_path.is_file():
            continue
        # Skip tiny or auxiliary files that are not datasets.
        if csv_path.name.lower().endswith(".source"):
            continue
        try:
            rel_path = csv_path.relative_to(_DATA_DIR)
        except Exception:
            rel_path = csv_path.name

        try:
            reader = pd.read_csv(csv_path, chunksize=chunk_size)
        except Exception:
            continue

        for chunk_idx, chunk in enumerate(reader):
            if chunk.empty:
                continue
            rows_text: list[str] = []
            for row_idx, row in chunk.iterrows():
                parts = []
                for col, val in row.items():
                    if pd.isna(val):
                        continue
                    text_val = str(val).strip()
                    if text_val == "":
                        continue
                    parts.append(f"{col}={text_val}")
                if not parts:
                    continue
                rows_text.append(f"row {row_idx}: " + ", ".join(parts))

            if not rows_text:
                continue
            text = "\n".join(rows_text)
            documents.append(
                {
                    "id": f"csv::{rel_path}::chunk{chunk_idx}",
                    "title": f"Dataset {rel_path} (rows {chunk_idx * chunk_size}-{chunk_idx * chunk_size + len(chunk) - 1})",
                    "text": text,
                    "source": str(rel_path),
                }
            )

    return documents


def _load_embeddings_cache() -> dict[str, Any] | None:
    if not _EMBEDDINGS_CACHE_PATH.exists():
        return None
    try:
        with _EMBEDDINGS_CACHE_PATH.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return None


def _save_embeddings_cache(payload: dict[str, Any]) -> None:
    try:
        _EMBEDDINGS_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with _EMBEDDINGS_CACHE_PATH.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle)
    except Exception:
        return None


def _get_openai_client() -> Any | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI  # type: ignore
    except Exception:
        return None
    return OpenAI(api_key=api_key)


def _embed_texts(texts: list[str], model: str) -> list[list[float]] | None:
    client = _get_openai_client()
    if client is None:
        return None
    try:
        response = client.embeddings.create(
            model=model, input=texts, encoding_format="float"
        )
        return [item.embedding for item in response.data]
    except Exception:
        return None


def _ensure_embeddings(context_data: dict[str, Any]) -> dict[str, Any] | None:
    """
    Use cached embeddings if present. Avoid long rebuilds during chat.
    To force rebuild, set RAG_REBUILD=1 and restart the app.
    """
    model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    cache = _load_embeddings_cache()
    if cache and cache.get("model") == model:
        return cache

    if os.getenv("RAG_REBUILD", "0").strip() != "1":
        return None

    documents = _build_rag_documents(context_data)
    signature = _build_dataset_signature()
    texts = [doc["text"] for doc in documents]
    embeddings = _embed_texts(texts, model)
    if embeddings is None:
        return None
    payload = {
        "model": model,
        "signature": signature,
        "documents": [
            {
                "id": doc["id"],
                "title": doc["title"],
                "text": doc["text"],
                "source": doc["source"],
                "embedding": emb,
            }
            for doc, emb in zip(documents, embeddings)
        ],
    }
    _save_embeddings_cache(payload)
    return payload


def _build_dataset_signature() -> dict[str, Any]:
    signature: dict[str, Any] = {}
    if not _DATA_DIR.exists():
        return signature
    for path in _DATA_DIR.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".csv", ".json"}:
            continue
        if path.name == "ai_chat_history.json":
            continue
        try:
            rel_path = path.relative_to(_DATA_DIR)
        except Exception:
            rel_path = path.name
        try:
            stat = path.stat()
            signature[str(rel_path)] = {
                "mtime": int(stat.st_mtime),
                "size": int(stat.st_size),
            }
        except Exception:
            continue
    return signature


def _retrieve_rag_context(query: str, context_data: dict[str, Any], top_k: int = 4) -> list[dict[str, str]]:
    cache = _ensure_embeddings(context_data)
    if cache is None:
        return []
    model = cache.get("model", "text-embedding-3-small")
    query_embs = _embed_texts([query], model)
    if not query_embs:
        return []

    query_vec = np.array(query_embs[0], dtype=np.float32)
    doc_items = cache.get("documents", [])
    if not doc_items:
        return []

    doc_vectors = np.array([item["embedding"] for item in doc_items], dtype=np.float32)
    norms = np.linalg.norm(doc_vectors, axis=1) * (np.linalg.norm(query_vec) + 1e-8)
    scores = (doc_vectors @ query_vec) / (norms + 1e-8)
    top_idx = np.argsort(scores)[-top_k:][::-1]

    results: list[dict[str, str]] = []
    for idx in top_idx:
        item = doc_items[int(idx)]
        results.append(
            {
                "title": item.get("title", "Context"),
                "text": item.get("text", ""),
                "source": item.get("source", "unknown"),
            }
        )
    return results


@lru_cache(maxsize=1)
def load_context_data() -> dict[str, Any]:
    crop_details: dict[str, dict[str, Any]] = {}
    soil_profiles: list[dict[str, Any]] = []

    if _CROP_DETAILS_PATH.exists():
        with _CROP_DETAILS_PATH.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
        crop_details = {
            _normalize_crop_key(key): value
            for key, value in raw.items()
            if isinstance(value, dict)
        }
    dataset_crop_details = _build_dataset_crop_details()
    for key, value in dataset_crop_details.items():
        if key not in crop_details:
            crop_details[key] = value

    if _SOIL_PROFILES_PATH.exists():
        soil_profiles = pd.read_csv(_SOIL_PROFILES_PATH).to_dict(orient="records")

    return {
        "crop_details": crop_details,
        "soil_profiles": soil_profiles,
    }


def _contains_agri_intent(query: str) -> bool:
    normalized = _normalize_text(query)
    return any(keyword in normalized for keyword in _AGRI_KEYWORDS)


def _detect_topics(query: str) -> list[str]:
    normalized = _normalize_text(query)
    topics: list[str] = []
    for topic, keywords in _TOPIC_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            topics.append(topic)
    return topics


def _is_utilization_query(query: str) -> bool:
    normalized = _normalize_text(query)
    return any(keyword in normalized for keyword in _TOPIC_KEYWORDS["utilization"])


def _is_non_agri_query(query: str) -> bool:
    normalized = _normalize_text(query)
    if not normalized:
        return False
    return any(keyword in normalized for keyword in _NON_AGRI_KEYWORDS)


def _is_npk_query(query: str) -> bool:
    normalized = _normalize_text(query)
    return any(keyword in normalized for keyword in _NPK_KEYWORDS)


def _build_npk_response(crop_key: str, crop: dict[str, Any]) -> str:
    crop_name = str(crop.get("name", crop_key)).title()
    fert = crop.get("fertilizer", {})
    basal = fert.get("basal", "Not specified")
    top_dressing = fert.get("top_dressing", [])
    lines = [f"### NPK Guidance for {crop_name}"]
    lines.append(f"- Basal NPK: {basal}")
    if top_dressing:
        lines.append(f"- Top dressing: {'; '.join(top_dressing[:3])}")
    lines.append(
        "- Note: Adjust final NPK dose based on soil test, variety, and local recommendations."
    )
    lines.append(
        "- Caution: Over-application can reduce soil health; follow label and extension guidance."
    )
    return "\n".join(lines)


def _extract_crop(query: str, context_data: dict[str, Any]) -> tuple[str | None, dict[str, Any] | None]:
    normalized = _normalize_text(query)
    normalized_key = _normalize_crop_key(normalized)
    crop_details = context_data.get("crop_details", {})

    for alias, canonical in _CROP_ALIASES.items():
        if alias in normalized_key and canonical in crop_details:
            return canonical, crop_details.get(canonical)

    for key, details in crop_details.items():
        name = str(details.get("name", key))
        if _normalize_crop_key(name) in normalized_key:
            return key, details
        if key and key in normalized_key:
            return key, details
    return None, None


def _extract_crops(query: str, context_data: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    normalized = _normalize_text(query)
    normalized_key = _normalize_crop_key(normalized)
    crop_details = context_data.get("crop_details", {})
    found: list[tuple[int, str, dict[str, Any]]] = []
    seen: set[str] = set()

    for alias, canonical in _CROP_ALIASES.items():
        if alias in normalized_key and canonical in crop_details and canonical not in seen:
            idx = normalized_key.find(alias)
            found.append((idx if idx >= 0 else 10_000, canonical, crop_details[canonical]))
            seen.add(canonical)

    for key, details in crop_details.items():
        name = str(details.get("name", key))
        key_norm = _normalize_crop_key(name)
        if key in seen:
            continue
        idx = normalized_key.find(key)
        idx_name = normalized_key.find(key_norm) if key_norm else -1
        match_idx = idx if idx >= 0 else idx_name
        if match_idx >= 0:
            found.append((match_idx, key, details))
            seen.add(key)

    found.sort(key=lambda x: x[0])
    return [(key, details) for _, key, details in found]


def _estimate_crop_water_range_mm(crop_key: str, crop: dict[str, Any]) -> tuple[float, float] | None:
    irr = crop.get("irrigation", {}) if isinstance(crop, dict) else {}
    possible_texts: list[str] = []
    if isinstance(irr, dict):
        stage_wise = irr.get("stage_wise", [])
        if isinstance(stage_wise, list):
            possible_texts.extend(str(x) for x in stage_wise)
        notes = irr.get("notes")
        if notes:
            possible_texts.append(str(notes))

    for text in possible_texts:
        m_range = re.search(r"(\d+(?:\.\d+)?)\s*[-to]+\s*(\d+(?:\.\d+)?)\s*mm", text, flags=re.IGNORECASE)
        if m_range:
            a = float(m_range.group(1))
            b = float(m_range.group(2))
            low, high = (a, b) if a <= b else (b, a)
            return (low, high)
        m_single = re.search(r"(\d+(?:\.\d+)?)\s*mm", text, flags=re.IGNORECASE)
        if m_single:
            v = float(m_single.group(1))
            return (v, v)

    return _WATER_REQUIREMENT_FALLBACK_MM.get(crop_key)


def _format_soil_profiles(context_data: dict[str, Any]) -> str:
    profiles = context_data.get("soil_profiles", [])
    if not profiles:
        return "- Soil profile reference is not available right now."

    lines = []
    for row in profiles[:6]:
        region = row.get("region", "unknown")
        n_val = row.get("n_avg", "NA")
        p_val = row.get("p_avg", "NA")
        k_val = row.get("k_avg", "NA")
        ph_val = row.get("ph", "NA")
        lines.append(
            f"- {region}: N={n_val}, P={p_val}, K={k_val}, pH={ph_val}"
        )
    return "\n".join(lines)


def _general_agri_response(query: str, context_data: dict[str, Any], topics: list[str]) -> str:
    normalized = _normalize_text(query)
    crop_details = context_data.get("crop_details", {})
    crop_items = [
        (
            key,
            str(value.get("name", key)).title(),
            str(value.get("season", "")).lower(),
            str(value.get("irrigation", {}).get("notes", "")).lower(),
        )
        for key, value in crop_details.items()
    ]
    crop_names = sorted({name for _, name, _, _ in crop_items})

    season_pref = None
    for season_name in ("kharif", "rabi", "zaid"):
        if season_name in normalized:
            season_pref = season_name
            break

    season_candidates = [
        name
        for _, name, season_text, _ in crop_items
        if season_pref and season_pref in season_text
    ]
    season_candidates = sorted(dict.fromkeys(season_candidates))

    soil_terms = [
        "black soil",
        "alluvial soil",
        "loamy soil",
        "sandy soil",
        "sandy loam",
        "clay soil",
        "red soil",
    ]
    soil_pref = next((term for term in soil_terms if term in normalized), None)
    soil_candidates = [
        name for _, name, _, notes in crop_items if soil_pref and soil_pref in notes
    ]
    soil_candidates = sorted(dict.fromkeys(soil_candidates))

    default_priority = [
        "Rice",
        "Wheat",
        "Maize",
        "Cotton",
        "Groundnut",
        "Sugarcane",
        "Soybean",
        "Ragi",
        "Jowar",
        "Banana",
    ]
    featured = [name for name in default_priority if name in crop_names]
    if len(featured) < 8:
        featured.extend([name for name in crop_names if name not in featured][: 8 - len(featured)])

    lines = ["### Crop Advisory"]
    is_best_crop_query = (
        ("best" in normalized or "recommend" in normalized or "suitable" in normalized)
        and ("crop" in normalized or "grow" in normalized)
    )

    if is_best_crop_query:
        if season_pref and season_candidates:
            lines.append(
                f"- Suitable {season_pref.title()} options from dataset: {', '.join(season_candidates[:10])}."
            )
        elif soil_pref and soil_candidates:
            lines.append(
                f"- Suitable options for {soil_pref.title()}: {', '.join(soil_candidates[:10])}."
            )
        else:
            lines.append(
                f"- Common crop options from dataset: {', '.join(featured[:10])}."
            )
        lines.append("- Choose based on local rainfall, soil type/pH, irrigation availability, and market demand.")
        lines.append("- For better accuracy, share your location, season, and whether the field is irrigated.")
    else:
        lines.append("- I can answer cultivation, fertilizer, pest/disease, irrigation, season, soil, and harvest questions.")

    if not topics or "season" in topics:
        lines.append("- Season guide: Kharif (monsoon), Rabi (winter), Zaid (summer). Match crop to local climate window.")
    if not topics or "soil" in topics:
        lines.append("- Soil tip: use pH and texture to shortlist crops; confirm with local soil test if possible.")
        if soil_pref and soil_candidates:
            lines.append(f"- {soil_pref.title()} crop shortlist: {', '.join(soil_candidates[:10])}.")
    if not topics or "water" in topics:
        lines.append("- Water tip: prioritize low-water crops for rainfed fields and water-demanding crops for assured irrigation.")
    if not topics or "fertilizer" in topics:
        lines.append("- Fertilizer tip: apply balanced NPK in splits and adjust final dose using soil-test report.")
    if not topics or "pest" in topics:
        lines.append("- Pest tip: follow integrated pest management with scouting, sanitation, and need-based sprays.")

    preview = ", ".join(crop_names[:12]) if crop_names else "No crop list available"
    lines.append(f"- Available crop catalog examples: {preview}.")
    lines.append("- Ask follow-up like: `best rabi crop for low water` or `top crops for black soil`.")
    lines.append("- Source: data/crop_details.json, data/raw/Crop recommendation dataset.csv, data/soil_profiles.csv")
    return "\n".join(lines)


def _build_rule_based_response(
    query: str,
    context_data: dict[str, Any],
) -> str:
    matched_crops = _extract_crops(query, context_data)
    probe_crop_key, probe_crop = _extract_crop(query, context_data)
    if not _contains_agri_intent(query) and not probe_crop:
        return _NON_AGRI_REPLY

    crop_key, crop = probe_crop_key, probe_crop
    topics = _detect_topics(query)

    # Focused comparison mode for questions like "which needs less water: crop A or crop B?"
    if len(matched_crops) >= 2 and "water" in topics:
        pairs = []
        for ck, cd in matched_crops[:3]:
            est = _estimate_crop_water_range_mm(ck, cd)
            name = str(cd.get("name", ck)).title()
            if est:
                pairs.append((name, est[0], est[1], (est[0] + est[1]) / 2))
            else:
                pairs.append((name, None, None, None))

        lines = ["### Water Comparison Advisory"]
        comparable = [p for p in pairs if p[3] is not None]
        for name, lo, hi, avg in pairs:
            if avg is None:
                lines.append(f"- {name}: water estimate not available in current dataset.")
            elif lo == hi:
                lines.append(f"- {name}: estimated water need ~ {lo:.0f} mm.")
            else:
                lines.append(f"- {name}: estimated water need ~ {lo:.0f}-{hi:.0f} mm.")

        if len(comparable) >= 2:
            lowest = min(comparable, key=lambda x: x[3])
            highest = max(comparable, key=lambda x: x[3])
            lines.append(
                f"- Conclusion: {lowest[0]} generally needs less water than {highest[0]}."
            )
        else:
            lines.append("- Conclusion: not enough comparable data to rank all listed crops.")

        lines.append("- Note: actual requirement varies by soil, climate, irrigation method, and variety.")
        lines.append("- Source: data/crop_details.json, data/raw/Crop recommendation dataset.csv")
        return "\n".join(lines)
    strict_single_topic = bool(crop and len(topics) == 1)

    if not crop:
        return _general_agri_response(query, context_data, topics)

    crop_name = str(crop.get("name", crop_key)).title()
    if strict_single_topic:
        focus_name = topics[0].title()
        lines = [f"### {focus_name} Advisory for {crop_name}"]
    else:
        lines = [f"### Advisory for {crop_name}"]
        lines.append("- This guidance is dataset-based and should be validated with local extension experts.")

    if not topics or "cultivation" in topics:
        stages = crop.get("stages", [])
        if stages:
            stage_text = " | ".join(
                f"{s.get('name', 'Stage')} ({s.get('days', 'NA')})"
                for s in stages[:4]
            )
            lines.append(f"- Cultivation stages: {stage_text}")
        lines.append(f"- Suitable season: {crop.get('season', 'Not specified')}")
        lines.append(f"- Typical duration: {crop.get('duration', 'Not specified')}")

    if not topics or "fertilizer" in topics:
        fert = crop.get("fertilizer", {})
        lines.append(f"- Basal fertilizer: {fert.get('basal', 'Not specified')}")
        top_dressing = fert.get("top_dressing", [])
        if top_dressing:
            lines.append(f"- Top dressing: {'; '.join(top_dressing[:3])}")

    if not topics or "pest" in topics:
        pests = crop.get("pests", {})
        common_pests = pests.get("common_pests", [])
        common_diseases = pests.get("common_diseases", [])
        if common_pests:
            lines.append(f"- Common pests: {', '.join(common_pests[:5])}")
        if common_diseases:
            lines.append(f"- Common diseases: {', '.join(common_diseases[:5])}")
        if pests.get("prevention"):
            lines.append(f"- Prevention: {pests.get('prevention')}")

    if not topics or "water" in topics:
        irrigation = crop.get("irrigation", {})
        stage_wise = irrigation.get("stage_wise", [])
        if stage_wise:
            lines.append(f"- Water management: {' | '.join(stage_wise[:3])}")
        lines.append(f"- Irrigation frequency: {irrigation.get('frequency', 'Not specified')}")

    if not topics or "soil" in topics:
        lines.append("- Soil suitability (regional reference):")
        lines.append(_format_soil_profiles(context_data))

    if not topics or "harvest" in topics:
        harvest = crop.get("harvest", {})
        lines.append(f"- Harvest indicators: {harvest.get('indicators', 'Not specified')}")
        lines.append(f"- Post-harvest: {harvest.get('post_harvest', 'Not specified')}")

    if not strict_single_topic:
        lines.append("- Caution: adapt doses and spray plans to local soil-test and label instructions.")
        lines.append("- Next step: share location and sowing month for a more specific stage-wise action plan.")
    lines.append("- Source: data/crop_details.json, data/soil_profiles.csv")
    return "\n".join(lines)


def _openai_response(
    query: str,
    context_data: dict[str, Any],
    retrieved_docs: list[dict[str, str]] | None = None,
) -> str | None:
    global _LAST_AI_ERROR
    client = _get_openai_client()
    if client is None:
        _append_ai_error("OpenAI API key missing or OpenAI package unavailable.")
        return None

    crop_key, crop = _extract_crop(query, context_data)
    conversation = context_data.get("conversation", [])
    compact_context = {
        "crop": crop if crop else "No exact crop matched. Ask user to mention crop name.",
        "soil_profiles": context_data.get("soil_profiles", [])[:5],
        "conversation": conversation[-6:] if isinstance(conversation, list) else [],
    }

    system_prompt = (
        "You are an expert agricultural advisor focused on crops, soil science, fertilizers, irrigation, "
        "pest and disease management, seasonal cropping systems, organic farming, and sustainable practices. "
        "You ONLY answer agriculture-related questions. If the question is unrelated to agriculture, refuse "
        "with exactly: "
        "'I am your Agricultural Advisory Assistant. Please ask crop or farming related questions.' "
        "Tone: calm, practical, field-ready, and respectful. "
        "Avoid rigid templates. Vary structure naturally based on the question; answer directly. "
        "Use bullets only when it improves clarity. "
        "Avoid overclaiming or inventing real-time facts. If local conditions matter (weather, market, "
        "regulations), ask for location and advise checking local extension advisories. "
        "When suggesting pesticides or nutrient doses, include safety precautions (PPE, label adherence, "
        "waiting period) and prefer integrated pest management."
    )

    rag_context = ""
    if retrieved_docs:
        blocks = []
        for doc in retrieved_docs[:4]:
            title = doc.get("title", "Context")
            text = doc.get("text", "")
            if len(text) > 800:
                text = text[:800] + "..."
            blocks.append(f"[{title}]\n{text}")
        rag_context = "\n\n".join(blocks)

    user_prompt = (
        f"User query: {query}\n\n"
        f"Local dataset context (JSON): {json.dumps(compact_context, ensure_ascii=True)}\n\n"
        f"Retrieved notes (if relevant):\n{rag_context}\n\n"
        "Answer in plain text. Keep the response focused on the user’s question. "
        "Do not follow a fixed template; vary the structure naturally. "
        "Include safety cautions only when recommending pesticides or specific doses. "
        "If retrieved notes are relevant, use them; otherwise rely on general agronomy knowledge."
    )

    try:
        completion = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        text = completion.choices[0].message.content if completion.choices else None
        if text:
            return text.strip()
        _append_ai_error("OpenAI returned an empty response.")
        return None
    except Exception as exc:
        _append_ai_error(f"OpenAI request failed: {exc.__class__.__name__} {exc}")
        return None


def _gemini_response(
    query: str,
    context_data: dict[str, Any],
    retrieved_docs: list[dict[str, str]] | None = None,
) -> str | None:
    global _LAST_AI_ERROR
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        _append_ai_error("GEMINI_API_KEY is missing.")
        return None

    configured_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()
    model = configured_model or "gemini-1.5-flash"
    if model.startswith("models/"):
        model = model.split("/", 1)[1]

    crop_key, crop = _extract_crop(query, context_data)
    conversation = context_data.get("conversation", [])
    compact_context = {
        "crop": crop if crop else "No exact crop matched. Ask user to mention crop name.",
        "soil_profiles": context_data.get("soil_profiles", [])[:5],
        "conversation": conversation[-6:] if isinstance(conversation, list) else [],
    }

    system_text = (
        "You are an expert agricultural advisor focused on crops, soil science, fertilizers, irrigation, "
        "pest and disease management, seasonal cropping systems, organic farming, and sustainable practices. "
        "You ONLY answer agriculture-related questions. If the question is unrelated to agriculture, refuse "
        "with exactly: "
        "'I am your Agricultural Advisory Assistant. Please ask crop or farming related questions.' "
        "Tone: calm, practical, field-ready, and respectful. "
        "Avoid rigid templates. Vary structure naturally based on the question; answer directly. "
        "Use bullets only when it improves clarity. "
        "Avoid overclaiming or inventing real-time facts. If local conditions matter (weather, market, "
        "regulations), ask for location and advise checking local extension advisories. "
        "When suggesting pesticides or nutrient doses, include safety precautions (PPE, label adherence, "
        "waiting period) and prefer integrated pest management."
    )

    rag_context = ""
    if retrieved_docs:
        blocks = []
        for doc in retrieved_docs[:4]:
            title = doc.get("title", "Context")
            text = doc.get("text", "")
            if len(text) > 800:
                text = text[:800] + "..."
            blocks.append(f"[{title}]\n{text}")
        rag_context = "\n\n".join(blocks)

    user_text = (
        f"User query: {query}\n\n"
        f"Local dataset context (JSON): {json.dumps(compact_context, ensure_ascii=True)}\n\n"
        f"Retrieved notes (if relevant):\n{rag_context}\n\n"
        "Answer in plain text. Keep the response focused on the user’s question. "
        "Do not follow a fixed template; vary the structure naturally. "
        "Include safety cautions only when recommending pesticides or specific doses. "
        "If retrieved notes are relevant, use them; otherwise rely on general agronomy knowledge."
    )

    def _call_gemini(text: str, system: str) -> str | None:
        payload = {
            "contents": [{"parts": [{"text": text}]}],
            "systemInstruction": {"parts": [{"text": system}]},
            "generationConfig": {"temperature": 0.2},
        }
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateContent?key={api_key}"
        )
        response = requests.post(url, json=payload, timeout=20)
        if response.status_code >= 400:
            snippet = response.text.strip()
            if len(snippet) > 200:
                snippet = snippet[:200] + "..."
            _append_ai_error(f"Gemini error {response.status_code}: {snippet}")
            return None
        data = response.json()
        candidates = data.get("candidates", [])
        if not candidates:
            _append_ai_error("Gemini returned no candidates.")
            return None
        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        text = "".join(str(part.get("text", "")) for part in parts).strip()
        if text:
            return text
        _append_ai_error("Gemini returned empty text.")
        return None

    try:
        reply = _call_gemini(user_text, system_text)
        if reply:
            return reply
        # Fallback to a slimmer prompt if the request was too large or rejected.
        slim_user_text = (
            f"User query: {query}\n\n"
            "Answer in plain text. Use short sections and bullet points when helpful. "
            "Finish with a short Caution line and a Next step line."
        )
        return _call_gemini(slim_user_text, system_text)
    except Exception as exc:
        _append_ai_error(f"Gemini request failed: {exc.__class__.__name__}")
        return None


def generate_crop_response(user_query: str, context_data: dict[str, Any]) -> str:
    """
    Generate advisory response for user query using local dataset context.
    Falls back to rule-based response if OpenAI is unavailable.
    """
    query = (user_query or "").strip()
    if not query:
        return "Please ask a crop-related question (for example: 'fertilizer plan for cotton')."

    probe_crop_key, probe_crop = _extract_crop(query, context_data)
    if _is_non_agri_query(query) and not _contains_agri_intent(query) and not probe_crop:
        return _NON_AGRI_REPLY

    matched_crops = _extract_crops(query, context_data)
    topics = _detect_topics(query)

    if _is_npk_query(query) and probe_crop:
        return _build_npk_response(probe_crop_key, probe_crop)

    if ("utilization" in topics or "nutrition" in query or "health" in query) and not probe_crop:
        retrieved_docs = _retrieve_rag_context(query, context_data)
        ai_reply = _gemini_response(query, context_data, retrieved_docs)
        if ai_reply:
            return ai_reply
        ai_reply = _openai_response(query, context_data, retrieved_docs)
        if ai_reply:
            return ai_reply

    global _LAST_AI_ERROR
    _LAST_AI_ERROR = None
    # Prefer Gemini, then OpenAI; fall back to dataset-based advisory.
    retrieved_docs = _retrieve_rag_context(query, context_data)
    ai_reply = _gemini_response(query, context_data, retrieved_docs)
    if ai_reply:
        return ai_reply
    ai_reply = _openai_response(query, context_data, retrieved_docs)
    if ai_reply:
        return ai_reply

    # If OpenAI is unavailable, fall back to dataset-based advisory.
    fallback = _build_rule_based_response(query, context_data)
    if _LAST_AI_ERROR:
        return f"AI service unavailable ({_LAST_AI_ERROR}). Showing dataset-based advisory.\n{fallback}"
    return (
        "AI service unavailable (no response from providers). "
        "Showing dataset-based advisory.\n"
        f"{fallback}"
    )
