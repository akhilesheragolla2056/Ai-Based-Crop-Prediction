from __future__ import annotations

import json
import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd
import requests


_CROP_DETAILS_PATH = Path("data/crop_details.json")
_SOIL_PROFILES_PATH = Path("data/soil_profiles.csv")
_CROP_DATASET_PATH = Path("data/raw/Crop recommendation dataset.csv")

_NON_AGRI_REPLY = (
    "I am your Crop Advisory Assistant. Please ask agriculture-related questions."
)

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
}

_TOPIC_KEYWORDS = {
    "cultivation": {"cultivation", "how to grow", "planting", "sowing", "stages"},
    "fertilizer": {"fertilizer", "fertiliser", "npk", "nutrient", "manure"},
    "pest": {"pest", "disease", "fungus", "infection", "spray", "pesticide"},
    "water": {"water", "irrigation", "rainfall", "moisture"},
    "season": {"season", "kharif", "rabi", "zaid", "summer", "winter", "monsoon"},
    "soil": {"soil", "ph", "alkaline", "acidic"},
    "harvest": {"harvest", "maturity", "yield", "post-harvest", "post harvest"},
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


def _openai_response(query: str, context_data: dict[str, Any]) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI  # type: ignore
    except Exception:
        return None

    crop_key, crop = _extract_crop(query, context_data)
    conversation = context_data.get("conversation", [])
    compact_context = {
        "crop": crop if crop else "No exact crop matched. Ask user to mention crop name.",
        "soil_profiles": context_data.get("soil_profiles", []),
        "conversation": conversation[-8:] if isinstance(conversation, list) else [],
    }

    system_prompt = (
        "You are an agriculture-only assistant for Indian farming advisory. "
        "Use only provided context. Do not answer non-agriculture questions. "
        "If question is outside agriculture, reply exactly: "
        "'I am your Crop Advisory Assistant. Please ask agriculture-related questions.' "
        "Provide moderately detailed responses with practical guidance. "
        "If user asks for one specific aspect (for example only water requirement), answer only that aspect and do not add unrelated sections. "
        "For broad crop-specific questions, include sections for season, cultivation, fertilizer, irrigation, pest/disease, and harvest when available. "
        "Avoid invented numeric claims. "
        "Do not use markdown symbols such as #, *, -, or backticks."
    )

    user_prompt = (
        f"User query: {query}\n\n"
        f"Context data (JSON): {json.dumps(compact_context, ensure_ascii=True)}\n\n"
        "Answer in plain text with clear section names and short lines. "
        "If the query is specific, keep answer strictly focused on that requested topic. "
        "Do not include markdown symbols (#, *, -, backticks). "
        "Include one short caution and one actionable next-step tip."
    )

    try:
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        text = completion.choices[0].message.content if completion.choices else None
        return text.strip() if text else None
    except Exception:
        return None


def _gemini_response(query: str, context_data: dict[str, Any]) -> str | None:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    configured_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    model_candidates = [
        configured_model,
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-flash-latest",
    ]

    crop_key, crop = _extract_crop(query, context_data)
    conversation = context_data.get("conversation", [])
    compact_context = {
        "crop": crop if crop else "No exact crop matched. Ask user to mention crop name.",
        "soil_profiles": context_data.get("soil_profiles", []),
        "conversation": conversation[-8:] if isinstance(conversation, list) else [],
    }

    system_text = (
        "You are an agriculture-only assistant for Indian farming advisory. "
        "Use only provided context. Do not answer non-agriculture questions. "
        "If question is outside agriculture, reply exactly: "
        "'I am your Crop Advisory Assistant. Please ask agriculture-related questions.' "
        "Provide moderately detailed responses with practical guidance. "
        "If user asks for one specific aspect (for example only water requirement), answer only that aspect and do not add unrelated sections. "
        "For broad crop-specific questions, include sections for season, cultivation, fertilizer, irrigation, pest/disease, and harvest when available. "
        "Avoid invented numeric claims. "
        "Do not use markdown symbols such as #, *, -, or backticks."
    )

    user_text = (
        f"User query: {query}\n\n"
        f"Context data (JSON): {json.dumps(compact_context, ensure_ascii=True)}\n\n"
        "Answer in plain text with clear section names and short lines. "
        "If the query is specific, keep answer strictly focused on that requested topic. "
        "Do not include markdown symbols (#, *, -, backticks). "
        "Include one short caution and one actionable next-step tip."
    )

    payload = {
        "contents": [{"parts": [{"text": user_text}]}],
        "systemInstruction": {"parts": [{"text": system_text}]},
        "generationConfig": {"temperature": 0.2},
    }

    for raw_model in model_candidates:
        model = str(raw_model or "").strip()
        if not model:
            continue
        if model.startswith("models/"):
            model = model.split("/", 1)[1]

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateContent?key={api_key}"
        )
        try:
            response = requests.post(url, json=payload, timeout=20)
            # Try next candidate for unavailable/rate-limited/transient failures.
            if response.status_code in (404, 408, 409, 429, 500, 502, 503, 504):
                continue
            if response.status_code >= 400:
                continue
            data = response.json()
            candidates = data.get("candidates", [])
            if not candidates:
                continue
            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            text = "".join(str(part.get("text", "")) for part in parts).strip()
            if text:
                return text
        except Exception:
            continue
    return None


def generate_crop_response(user_query: str, context_data: dict[str, Any]) -> str:
    """
    Generate advisory response for user query using local dataset context.
    Falls back to rule-based response if OpenAI is unavailable.
    """
    query = (user_query or "").strip()
    if not query:
        return "Please ask a crop-related question (for example: 'fertilizer plan for cotton')."

    matched_crops = _extract_crops(query, context_data)
    topics = _detect_topics(query)

    # Deterministic mode for comparison queries and strict single-topic queries.
    if len(matched_crops) >= 2 and "water" in topics:
        return _build_rule_based_response(query, context_data)

    # Deterministic strict mode for specific crop-topic questions.
    crop_key, crop = _extract_crop(query, context_data)
    if crop and len(topics) == 1:
        return _build_rule_based_response(query, context_data)

    # Priority: Gemini API -> OpenAI API -> local rule-based advisory.
    ai_reply = _gemini_response(query, context_data)
    if ai_reply:
        return ai_reply

    ai_reply = _openai_response(query, context_data)
    if ai_reply:
        return ai_reply

    return _build_rule_based_response(query, context_data)
