from __future__ import annotations
from datetime import timezone
from typing import Mapping
import math
from pathlib import Path
import streamlit as st
from backend.weather_service import (
    WeatherProviderError,
    WeatherSnapshot,
    get_weather_snapshot,
)
from backend.rainfall_lookup import get_avg_rainfall_for_region
from utils.soil_profiles import SOIL_REGION_OPTIONS, get_soil_profile

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MAJOR_CROPS_LOOKUP = {
    # States
    "telangana": ["cotton", "maize", "rice", "sorghum", "red gram"],
    "andhra pradesh": ["rice", "maize", "groundnut", "cotton", "sugarcane"],
    "maharashtra": ["cotton", "sugarcane", "soybean", "turmeric", "jowar"],
    "punjab": ["wheat", "rice", "maize", "cotton", "barley"],
    "karnataka": ["ragi", "jowar", "maize", "rice", "sugarcane"],
    "tamil nadu": ["rice", "sugarcane", "cotton", "groundnut", "millets"],
    "uttar pradesh": ["wheat", "rice", "sugarcane", "maize", "potato"],
    "west bengal": ["rice", "jute", "potato", "sugarcane", "wheat"],
    "bihar": ["rice", "wheat", "maize", "pulses", "potato"],
    "gujarat": ["cotton", "groundnut", "bajra", "wheat", "rice"],
    "kerala": ["rice", "coconut", "rubber", "banana", "pepper"],
    "madhya pradesh": ["wheat", "soybean", "gram", "rice", "maize"],
    "rajasthan": ["bajra", "wheat", "gram", "barley", "mustard"],
    "odisha": ["rice", "pulses", "groundnut", "maize", "sugarcane"],
    "jharkhand": ["rice", "maize", "pulses", "wheat", "oilseeds"],
    "chhattisgarh": ["rice", "maize", "pulses", "oilseeds", "wheat"],
    "haryana": ["wheat", "rice", "sugarcane", "cotton", "barley"],
    "assam": ["rice", "jute", "tea", "pulses", "oilseeds"],
    "uttarakhand": ["rice", "wheat", "maize", "barley", "pulses"],
    # Major cities/districts
    "mumbai": ["rice", "vegetables", "flowers", "fruits"],
    "pune": ["sugarcane", "wheat", "rice", "vegetables"],
    "nagpur": ["cotton", "soybean", "wheat", "oranges"],
    "hyderabad": ["rice", "cotton", "maize", "vegetables"],
    "chennai": ["rice", "groundnut", "millets", "vegetables"],
    "bengaluru": ["ragi", "rice", "vegetables", "flowers"],
    "kolkata": ["rice", "jute", "vegetables", "fruits"],
    "delhi": ["wheat", "vegetables", "fruits", "flowers"],
    # Add more as needed
}

DISEASE_SEVERITIES = ["Low", "Medium", "High"]
"""Form components for capture of agronomic inputs."""

DEFAULT_METRICS: Mapping[str, float] = {
    "N": 90.0,
    "P": 42.0,
    "K": 43.0,
    "ph": 6.5,
    "temperature": 26.0,
    "humidity": 60.0,
    "rainfall": 160.0,
}


CROPS = [
    "Rice",
    "Wheat",
    "Maize",
    "Cotton",
    "Groundnut",
    "Sugarcane",
    "Banana",
    "Apple",
    "Mango",
    "Grapes",
]



FORM_I18N = {
    "en": {
        "soil_input_method": "Soil Data Input Method:",
        "manual_input": "Manual Input",
        "auto_fetch_location": "Auto Fetch by Location",
        "regional_soil_profile": "Regional Soil Profile",
        "select_soil_type": "Select Soil Type (Dataset)",
        "weather_expander": "Auto-fill weather & region data",
        "location_label": "Location (City, State)",
        "location_help": "Example: Pune, Maharashtra",
        "fetch_live_weather": "Fetch live weather",
        "macronutrients": "Macronutrients (NPK)",
        "weather_climate": "Weather & Climate",
        "soil_ph": "Soil pH",
        "regional_caption": "Regional soil profile values are computed from dataset rows for the selected soil type.",
        "nitrogen_label": "Nitrogen (N)",
        "phosphorus_label": "Phosphorus (P)",
        "potassium_label": "Potassium (K)",
        "temperature_label": "Temperature (C)",
        "humidity_label": "Humidity (%)",
        "rainfall_label": "Rainfall (mm)",
        "nitrogen_help": "Essential for leafy growth. Typical range: 0-200.",
        "phosphorus_help": "Important for root and flowering development. Typical range: 0-200.",
        "potassium_help": "Supports overall plant health. Typical range: 0-200.",
        "temperature_help": "Average temperature in Celsius.",
        "humidity_help": "Relative humidity in percent.",
        "rainfall_help": "Total rainfall in millimeters.",
        "soil_ph_help": "Soil pH affects nutrient availability. 6.5 is neutral.",
        "acidic": "3.5 (Acidic)",
        "neutral": "6.5 (Neutral)",
        "alkaline": "9.5 (Alkaline)",
        "crop_select": "Select Crop",
        "leaf_scan": "Leaf Scan",
        "crop_for_diagnosis": "Crop for diagnosis",
        "upload_leaf_image": "Upload leaf image",
        "disease": "Disease",
        "severity": "Severity",
    },
    "hi": {
        "soil_input_method": "Mitti Data Input Tareeka:",
        "manual_input": "Manual Input",
        "auto_fetch_location": "Location se Auto Fetch",
        "regional_soil_profile": "Regional Mitti Profile",
        "select_soil_type": "Mitti Type Chune (Dataset)",
        "weather_expander": "Mausam aur region data auto-fill",
        "location_label": "Sthan (City, State)",
        "location_help": "Udaharan: Pune, Maharashtra",
        "fetch_live_weather": "Live mausam lao",
        "macronutrients": "Pramukh Poshak Tatva (NPK)",
        "weather_climate": "Mausam aur Jalvayu",
        "soil_ph": "Mitti pH",
        "regional_caption": "Chune gaye mitti type ke liye values dataset se li gayi hain.",
        "nitrogen_label": "Nitrogen (N)",
        "phosphorus_label": "Phosphorus (P)",
        "potassium_label": "Potassium (K)",
        "temperature_label": "Taapman (C)",
        "humidity_label": "Aardrata (%)",
        "rainfall_label": "Varsha (mm)",
        "nitrogen_help": "Patti vikas ke liye zaruri. Samanya range: 0-200.",
        "phosphorus_help": "Jad aur phool vikas ke liye mahatvapurn. Samanya range: 0-200.",
        "potassium_help": "Paudhe ke swasthya ke liye upyogi. Samanya range: 0-200.",
        "temperature_help": "Ausat taapman Celsius me.",
        "humidity_help": "Sapeksh aardrata pratishat me.",
        "rainfall_help": "Kul varsha millimeter me.",
        "soil_ph_help": "Mitti pH poshak uplabdhata ko prabhavit karta hai. 6.5 neutral hai.",
        "acidic": "3.5 (Amliya)",
        "neutral": "6.5 (Santulit)",
        "alkaline": "9.5 (Kshariy)",
        "crop_select": "Fasal Chune",
        "leaf_scan": "Patti Scan",
        "crop_for_diagnosis": "Nidan ke liye fasal",
        "upload_leaf_image": "Patti image upload karein",
        "disease": "Rog",
        "severity": "Gambhirta",
    },
    "te": {
        "soil_input_method": "Nela Data Input Vidhanam:",
        "manual_input": "Manual Input",
        "auto_fetch_location": "Location dwara Auto Fetch",
        "regional_soil_profile": "Regional Nela Profile",
        "select_soil_type": "Nela Type Enchukondi (Dataset)",
        "weather_expander": "Vathavaranam mariyu region data auto-fill",
        "location_label": "Prantham (City, State)",
        "location_help": "Udaharan: Pune, Maharashtra",
        "fetch_live_weather": "Live weather pondandi",
        "macronutrients": "Macro Poshakalu (NPK)",
        "weather_climate": "Vathavaranam mariyu climate",
        "soil_ph": "Nela pH",
        "regional_caption": "Enchukuna nela type values dataset nundi teesukobaddayi.",
        "nitrogen_label": "Nitrogen (N)",
        "phosphorus_label": "Phosphorus (P)",
        "potassium_label": "Potassium (K)",
        "temperature_label": "Ushnograta (C)",
        "humidity_label": "Aardrata (%)",
        "rainfall_label": "Varshapatham (mm)",
        "nitrogen_help": "Aaku perugudala kosam avasaram. Samanya range: 0-200.",
        "phosphorus_help": "Veru mariyu puvvu vikasam kosam mukhyam. Samanya range: 0-200.",
        "potassium_help": "Mokka arogyam kosam upayogakaram. Samanya range: 0-200.",
        "temperature_help": "Sagat u ushnograta Celsius lo.",
        "humidity_help": "Sapeksha aardrata shatam.",
        "rainfall_help": "Mottam varshapatham millimeter lo.",
        "soil_ph_help": "Nela pH poshaka labhyata pai prabhavam chupistundi. 6.5 neutral.",
        "acidic": "3.5 (Amla)",
        "neutral": "6.5 (Neutral)",
        "alkaline": "9.5 (Kshara)",
        "crop_select": "Panta Enchukondi",
        "leaf_scan": "Aaku Scan",
        "crop_for_diagnosis": "Nirdharana kosam panta",
        "upload_leaf_image": "Aaku image upload cheyandi",
        "disease": "Rogam",
        "severity": "Teevrata",
    },
}


def _normalize_language(value: str | None) -> str:
    mapping = {
        "en": "en",
        "english": "en",
        "hi": "hi",
        "hindi": "hi",
        "te": "te",
        "telugu": "te",
    }
    return mapping.get(str(value or "").strip().lower(), "en")


def _t(key: str) -> str:
    lang = _normalize_language(st.session_state.get("language", "en"))
    return FORM_I18N.get(lang, FORM_I18N["en"]).get(key, FORM_I18N["en"].get(key, key))


def environmental_inputs(key_prefix: str = "env") -> dict[str, float]:
    weather_meta_key = f"{key_prefix}_weather_meta"
    temp_key = f"{key_prefix}_temperature"
    humidity_key = f"{key_prefix}_humidity"
    rainfall_key = f"{key_prefix}_rainfall"
    input_method_key = f"{key_prefix}_soil_input_method"
    input_method_persist_key = f"{key_prefix}_soil_input_method_persist"
    soil_region_select_key = f"{key_prefix}_soil_region_select"
    soil_region_persist_key = f"{key_prefix}_soil_region_select_persist"

    st.markdown(
        """
    <style>
        /* Custom pH slider styling - gradient track */
        .stSlider [data-baseweb="slider"] {
            background: linear-gradient(to right, #ff6b6b 0%%, #feca57 25%%, #48dbfb 50%%, #1dd1a1 75%%, #5f27cd 100%%) !important;
            height: 8px !important;
            border-radius: 4px !important;
        }
        /* Hide the tick bar with min/max values (3.5 and 9.5) */
        .stSlider [data-testid="stSliderTickBar"] {
            display: none !important;
        }
        /* Hide the filled track portion (the extra colored bar) */
        .stSlider [data-baseweb="slider"] > div:first-child {
            background: transparent !important;
        }
        /* Style the slider thumb */
        .stSlider [role="slider"] {
            background: #4CAF50 !important;
            border: 3px solid white !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3) !important;
            width: 20px !important;
            height: 20px !important;
        }
        /* Style the value bubble */
        .stSlider [data-testid="stSliderThumbValue"] {
            background: #4CAF50 !important;
            color: white !important;
            font-weight: bold !important;
            padding: 4px 10px !important;
            border-radius: 4px !important;
        }
        .stSlider [data-testid="stSliderThumbValue"]::after {
            border-top-color: #4CAF50 !important;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
    # Removed custom Environmental & Soil Inputs header block as requested
    input_method_codes = ["manual", "auto", "regional"]
    legacy_map = {
        "Manual Input": "manual",
        "Auto Fetch by Location": "auto",
        "Regional Soil Profile": "regional",
    }
    if input_method_persist_key not in st.session_state:
        st.session_state[input_method_persist_key] = "manual"
    elif st.session_state[input_method_persist_key] in legacy_map:
        st.session_state[input_method_persist_key] = legacy_map[
            st.session_state[input_method_persist_key]
        ]
    if input_method_key not in st.session_state:
        st.session_state[input_method_key] = st.session_state[input_method_persist_key]
    elif st.session_state[input_method_key] in legacy_map:
        st.session_state[input_method_key] = legacy_map[st.session_state[input_method_key]]

    input_method = st.radio(
        _t("soil_input_method"),
        input_method_codes,
        format_func=lambda code: (
            _t("manual_input")
            if code == "manual"
            else _t("auto_fetch_location")
            if code == "auto"
            else _t("regional_soil_profile")
        ),
        key=input_method_key,
    )
    st.session_state[input_method_persist_key] = input_method

    regional_profile_key = None
    if input_method == "regional":
        region_labels = [label for label, _ in SOIL_REGION_OPTIONS]
        if soil_region_persist_key not in st.session_state:
            st.session_state[soil_region_persist_key] = region_labels[0]
        persisted_region = st.session_state[soil_region_persist_key]
        if persisted_region not in region_labels:
            persisted_region = region_labels[0]
            st.session_state[soil_region_persist_key] = persisted_region
        if soil_region_select_key not in st.session_state:
            st.session_state[soil_region_select_key] = persisted_region
        selected_label = st.selectbox(
            _t("select_soil_type"),
            region_labels,
            key=soil_region_select_key,
        )
        st.session_state[soil_region_persist_key] = selected_label
        label_to_key = {label: key for label, key in SOIL_REGION_OPTIONS}
        regional_profile_key = label_to_key.get(selected_label)
        st.caption(_t("regional_caption"))

    for state_key, default in (
        (temp_key, DEFAULT_METRICS["temperature"]),
        (humidity_key, DEFAULT_METRICS["humidity"]),
        (rainfall_key, DEFAULT_METRICS["rainfall"]),
    ):
        if state_key not in st.session_state:
            st.session_state[state_key] = default

    for key, default in (
        (f"{key_prefix}_nitrogen", DEFAULT_METRICS["N"]),
        (f"{key_prefix}_phosphorus", DEFAULT_METRICS["P"]),
        (f"{key_prefix}_potassium", DEFAULT_METRICS["K"]),
        (f"{key_prefix}_ph", DEFAULT_METRICS["ph"]),
    ):
        if key not in st.session_state:
            st.session_state[key] = default

    if weather_meta_key not in st.session_state:
        st.session_state[weather_meta_key] = {}

    if input_method == "auto":
        with st.expander(_t("weather_expander"), expanded=False):
            location = st.text_input(
                _t("location_label"),
                value=st.session_state[weather_meta_key].get("location", ""),
                key=f"{key_prefix}_weather_location",
                help=_t("location_help"),
            )

            if st.button(_t("fetch_live_weather"), key=f"{key_prefix}_weather_fetch"):
                try:
                    snapshot: WeatherSnapshot = get_weather_snapshot(location)
                except WeatherProviderError as exc:
                    st.error(str(exc))
                else:
                    st.session_state[f"{key_prefix}_force_autofill"] = True
                    st.session_state[f"{key_prefix}_force_autofill_location"] = location
                    st.session_state[temp_key] = round(snapshot.temperature_c, 2)
                    st.session_state[humidity_key] = round(snapshot.humidity_pct, 2)
                    # Rainfall fallback logic
                    region = ""
                    if "," in location:
                        region = location.split(",")[-1].strip().lower()
                    else:
                        region = location.strip().lower()
                    rainfall_val = round(snapshot.rainfall_mm, 2)
                    if rainfall_val == 0:
                        avg_rainfall = get_avg_rainfall_for_region(region)
                        if avg_rainfall:
                            st.session_state[rainfall_key] = avg_rainfall
                            st.info(
                                f"No recent rainfall reported. Using average annual rainfall for {region.title()}: {avg_rainfall} mm. You may override this value."
                            )
                        else:
                            st.session_state[rainfall_key] = 0.0
                            st.warning(
                                "No rainfall data found for this region. Please enter manually."
                            )
                    else:
                        st.session_state[rainfall_key] = rainfall_val
                    st.session_state[weather_meta_key] = {
                        "location": location,
                        "provider": snapshot.provider,
                        "observed_at": snapshot.observed_at.isoformat(),
                    }
                    # NPK/pH are now handled by the dataset-based AutoFetch logic below.
                    observed_local = snapshot.observed_at.astimezone(timezone.utc)
                    st.success(
                        f"Loaded weather from {snapshot.provider.title()} (observed {observed_local.strftime('%Y-%m-%d %H:%M')} UTC)."
                    )

    # AutoFetch: Use region-aware dataset to suggest top 3 crops for the state.
    import pandas as pd

    dataset_region_path = PROJECT_ROOT / "data" / "raw" / "crop_recommendation_region_augmented.csv"
    def _normalize_region(text: str) -> str:
        cleaned = "".join(ch if ch.isalnum() or ch.isspace() else " " for ch in text.lower())
        return " ".join(cleaned.split())

    location_input = st.session_state.get(f"{key_prefix}_weather_location", "")
    location_val = location_input.strip().lower()
    location_match = _normalize_region(location_input)
    city_display = ""
    region_display = ""
    if "," in location_input:
        parts = [part.strip() for part in location_input.split(",") if part.strip()]
        parts = [_normalize_region(part) for part in parts if part]
        if parts:
            city_display = parts[0]
            region_display = parts[-1]
            if region_display in {"india", "bharat"} and len(parts) >= 2:
                region_display = parts[-2]
    else:
        region_display = location_match

    try:
        if not dataset_region_path.exists():
            raise FileNotFoundError(dataset_region_path)
        df_region = pd.read_csv(dataset_region_path, comment="#")
        df_region["region"] = df_region["region"].astype(str).str.strip().str.lower()
        df_region["label"] = df_region["label"].astype(str).str.strip().str.lower()

        region_key = region_display
        region_df = (
            df_region[df_region["region"] == region_key]
            if region_key
            else df_region.iloc[0:0]
        )
        if region_df.empty and city_display:
            region_key = city_display
            region_df = df_region[df_region["region"] == region_key]
        if region_df.empty and location_match:
            region_candidates = (
                df_region["region"].dropna().astype(str).str.strip().str.lower().unique().tolist()
            )
            matches = [
                candidate
                for candidate in region_candidates
                if f" {candidate} " in f" {location_match} "
            ]
            if matches:
                region_key = max(matches, key=len)
                region_df = df_region[df_region["region"] == region_key]

        top_crops: list[str] = []
        top_scores: dict[str, float] = {}
        source = ""

        if not region_df.empty:
            crop_counts = region_df["label"].value_counts()
            if crop_counts.nunique() == 1:
                ordered = list(dict.fromkeys(region_df["label"].tolist()))
                top_crops = ordered[:3]
            else:
                top_crops = crop_counts.head(3).index.tolist()
            source = "dataset"

        if top_crops:
            st.session_state[f"{key_prefix}_top_crops"] = top_crops
            st.session_state[f"{key_prefix}_top_crops_scores"] = {}
            st.session_state[f"{key_prefix}_top_crops_source"] = source

            static_fields = [
                "N",
                "P",
                "K",
                "ph",
                "rainfall",
                "temperature",
                "humidity",
            ]
            dominant_crop = region_df["label"].iloc[0] if not region_df.empty else top_crops[0]
            crop_df = region_df[region_df["label"] == dominant_crop]
            dom_vals: dict[str, float] = {}
            for field in static_fields:
                if field in crop_df.columns and not crop_df.empty:
                    series = pd.to_numeric(crop_df[field], errors="coerce").dropna()
                    if not series.empty:
                        dom_vals[field] = float(series.mean())
                    else:
                        dom_vals[field] = DEFAULT_METRICS.get(field, 0.0)
                else:
                    dom_vals[field] = DEFAULT_METRICS.get(field, 0.0)

            last_autofill_key = f"{key_prefix}_autofill_region"
            previous_region = st.session_state.get(last_autofill_key)
            previous_location = st.session_state.get(f"{key_prefix}_autofill_location_raw")
            signature = (
                region_key,
                dominant_crop,
                round(dom_vals["N"], 4),
                round(dom_vals["P"], 4),
                round(dom_vals["K"], 4),
                round(dom_vals["ph"], 4),
                round(dom_vals["temperature"], 4),
                round(dom_vals["humidity"], 4),
                round(dom_vals["rainfall"], 4),
            )
            previous_signature = st.session_state.get(f"{key_prefix}_autofill_signature")
            location_changed = previous_location != location_input
            signature_changed = previous_signature != signature
            force_autofill = bool(
                st.session_state.get(f"{key_prefix}_force_autofill")
                and st.session_state.get(f"{key_prefix}_force_autofill_location") == location_input
            )
            if previous_region != region_key or location_changed or signature_changed or force_autofill:
                st.session_state[f"{key_prefix}_nitrogen"] = dom_vals["N"]
                st.session_state[f"{key_prefix}_phosphorus"] = dom_vals["P"]
                st.session_state[f"{key_prefix}_potassium"] = dom_vals["K"]
                st.session_state[f"{key_prefix}_ph"] = dom_vals["ph"]
                st.success(
                    f"Auto-filled NPK for {region_key.title()} from dataset "
                    f"(N={dom_vals['N']:.2f}, P={dom_vals['P']:.2f}, K={dom_vals['K']:.2f})"
                )
                st.success(
                    f"Auto-filled soil pH for {region_key.title()} from dataset: {dom_vals['ph']:.2f}"
                )
                weather_meta = st.session_state.get(weather_meta_key, {})
                live_location = weather_meta.get("location", "").strip().lower()
                has_live_weather = bool(
                    weather_meta.get("provider") and live_location == location_val
                )
                if not has_live_weather:
                    st.session_state[temp_key] = dom_vals["temperature"]
                    st.session_state[humidity_key] = dom_vals["humidity"]
                    st.session_state[rainfall_key] = dom_vals["rainfall"]
                st.session_state[last_autofill_key] = region_key
                st.session_state[f"{key_prefix}_autofill_location_raw"] = location_input
                st.session_state[f"{key_prefix}_autofill_signature"] = signature
                st.session_state.pop(f"{key_prefix}_force_autofill", None)
                st.session_state.pop(f"{key_prefix}_force_autofill_location", None)

            # Compute dataset-based suitability scores from current inputs
            current_inputs = {
                "N": float(st.session_state.get(f"{key_prefix}_nitrogen", DEFAULT_METRICS["N"])),
                "P": float(st.session_state.get(f"{key_prefix}_phosphorus", DEFAULT_METRICS["P"])),
                "K": float(st.session_state.get(f"{key_prefix}_potassium", DEFAULT_METRICS["K"])),
                "ph": float(st.session_state.get(f"{key_prefix}_ph", DEFAULT_METRICS["ph"])),
                "temperature": float(st.session_state.get(temp_key, DEFAULT_METRICS["temperature"])),
                "humidity": float(st.session_state.get(humidity_key, DEFAULT_METRICS["humidity"])),
                "rainfall": float(st.session_state.get(rainfall_key, DEFAULT_METRICS["rainfall"])),
            }
            crop_pool = region_df[region_df["label"].isin(top_crops)]
            ranges: dict[str, float] = {}
            for field in static_fields:
                series = pd.to_numeric(crop_pool[field], errors="coerce").dropna()
                if series.empty:
                    ranges[field] = 1.0
                else:
                    min_v = float(series.min())
                    max_v = float(series.max())
                    span = max_v - min_v
                    ranges[field] = span if math.isfinite(span) and span > 0 else 1.0
            distances: dict[str, float] = {}
            for crop in top_crops:
                crop_df = region_df[region_df["label"] == crop]
                means = (
                    crop_df[static_fields]
                    .apply(pd.to_numeric, errors="coerce")
                    .mean(numeric_only=True)
                )
                diffs = []
                for field in static_fields:
                    mean_val = float(means.get(field, current_inputs[field]))
                    if not math.isfinite(mean_val):
                        mean_val = current_inputs[field]
                    range_val = ranges.get(field, 1.0)
                    if not math.isfinite(range_val) or range_val <= 0:
                        range_val = 1.0
                    diff = abs(current_inputs[field] - mean_val) / range_val
                    diffs.append(diff)
                avg_diff = sum(diffs) / len(diffs) if diffs else 1.0
                if not math.isfinite(avg_diff):
                    avg_diff = 10.0
                distances[crop] = avg_diff

            # Convert distances to suitability scores using a softmax over negative distance.
            scores: dict[str, float] = {}
            if distances:
                exps = {crop: math.exp(-dist) for crop, dist in distances.items()}
                total = sum(exps.values())
                if total > 0:
                    scores = {crop: exps[crop] / total for crop in top_crops}
                else:
                    scores = {crop: 1.0 / len(top_crops) for crop in top_crops}
            else:
                scores = {crop: 0.5 for crop in top_crops}

            st.session_state[f"{key_prefix}_top_crops_scores"] = scores
        else:
            st.session_state.pop(f"{key_prefix}_top_crops", None)
            st.session_state.pop(f"{key_prefix}_top_crops_scores", None)
            st.session_state.pop(f"{key_prefix}_top_crops_source", None)
            if location_match:
                st.warning(
                    "Location not found in AutoFetch dataset. Try a state/UT or capital city."
                )
    except Exception as e:
        st.info(f"Regional AutoFetch unavailable: {e}")

    if input_method == "regional" and regional_profile_key:
        profile = get_soil_profile(regional_profile_key)
        if profile:
            last_region_key = f"{key_prefix}_regional_profile_region"
            previous_region = st.session_state.get(last_region_key)
            if previous_region != regional_profile_key:
                st.session_state[f"{key_prefix}_nitrogen"] = profile["N"]
                st.session_state[f"{key_prefix}_phosphorus"] = profile["P"]
                st.session_state[f"{key_prefix}_potassium"] = profile["K"]
                st.session_state[f"{key_prefix}_ph"] = profile["ph"]
                st.session_state[temp_key] = float(
                    profile.get("temperature", DEFAULT_METRICS["temperature"])
                )
                st.session_state[humidity_key] = float(
                    profile.get("humidity", DEFAULT_METRICS["humidity"])
                )
                st.session_state[rainfall_key] = float(
                    profile.get("rainfall", DEFAULT_METRICS["rainfall"])
                )
                st.session_state[last_region_key] = regional_profile_key
                st.success(
                    "Auto-filled climate fields from dataset for selected soil type "
                    f"(Temp={st.session_state[temp_key]:.2f} C, "
                    f"Humidity={st.session_state[humidity_key]:.2f}%, "
                    f"Rainfall={st.session_state[rainfall_key]:.2f} mm)."
                )

            # Use Crop recommendation dataset directly to compute soil-specific top crops.
            try:
                soil_dataset_path = PROJECT_ROOT / "data" / "raw" / "Crop recommendation dataset.csv"
                if not soil_dataset_path.exists():
                    raise FileNotFoundError(soil_dataset_path)
                soil_df = pd.read_csv(soil_dataset_path)
                soil_df.columns = [str(col).strip().upper() for col in soil_df.columns]
                if "SOIL" in soil_df.columns and "CROPS" in soil_df.columns:
                    selected_soil_norm = _normalize_region(selected_label)
                    soil_df["SOIL_NORM"] = (
                        soil_df["SOIL"].astype(str).map(_normalize_region)
                    )
                    match_df = soil_df[soil_df["SOIL_NORM"] == selected_soil_norm]

                    if not match_df.empty:
                        crop_counts = (
                            match_df["CROPS"]
                            .astype(str)
                            .str.strip()
                            .str.lower()
                            .value_counts()
                        )
                        top_crops = crop_counts.head(3).index.tolist()
                        total = float(crop_counts.sum()) if not crop_counts.empty else 0.0
                        scores = (
                            {crop: float(crop_counts[crop] / total) for crop in top_crops}
                            if total > 0
                            else {crop: 1.0 / len(top_crops) for crop in top_crops}
                        )

                        st.session_state[f"{key_prefix}_top_crops"] = top_crops
                        st.session_state[f"{key_prefix}_top_crops_scores"] = scores
                        st.session_state[f"{key_prefix}_top_crops_source"] = "soil_dataset"
                        st.session_state[f"{key_prefix}_autofill_region"] = selected_label
                    else:
                        st.session_state.pop(f"{key_prefix}_top_crops", None)
                        st.session_state.pop(f"{key_prefix}_top_crops_scores", None)
                        st.session_state.pop(f"{key_prefix}_top_crops_source", None)
                        st.session_state[f"{key_prefix}_autofill_region"] = selected_label
                        st.warning(
                            "No crop records found for selected soil type in Crop recommendation dataset."
                        )
            except Exception as exc:
                st.warning(f"Soil-based crop shortlist unavailable: {exc}")
        else:
            st.warning("Regional soil profile not found. Please select another region.")

    st.markdown(
        f"<h5 style='margin-top:1.5em; color:#388e3c;'>{_t('macronutrients')}</h5>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1.1, 1, 1.1])
    with col1:
        n_value = st.number_input(
            f"🧪 {_t('nitrogen_label')}",
            min_value=0.0,
            max_value=200.0,
            step=1.0,
            key=f"{key_prefix}_nitrogen",
            help=_t("nitrogen_help"),
        )
    with col2:
        p_value = st.number_input(
            f"🧪 {_t('phosphorus_label')}",
            min_value=0.0,
            max_value=200.0,
            step=1.0,
            key=f"{key_prefix}_phosphorus",
            help=_t("phosphorus_help"),
        )
    with col3:
        k_value = st.number_input(
            f"🧪 {_t('potassium_label')}",
            min_value=0.0,
            max_value=200.0,
            step=1.0,
            key=f"{key_prefix}_potassium",
            help=_t("potassium_help"),
        )

    st.markdown(
        f"<h5 style='margin-top:1.5em; color:#388e3c;'>{_t('weather_climate')}</h5>",
        unsafe_allow_html=True,
    )
    col4, col5, col6 = st.columns([1.1, 1, 1.1])
    with col4:
        temperature = st.number_input(
            f"🌡️ {_t('temperature_label')}",
            min_value=-10.0,
            max_value=60.0,
            step=0.5,
            key=temp_key,
            help=_t("temperature_help"),
        )
    with col5:
        humidity = st.number_input(
            f"💧 {_t('humidity_label')}",
            min_value=0.0,
            max_value=100.0,
            step=1.0,
            key=humidity_key,
            help=_t("humidity_help"),
        )
    with col6:
        rainfall = st.number_input(
            f"🌧️ {_t('rainfall_label')}",
            min_value=0.0,
            max_value=5000.0,
            step=1.0,
            key=rainfall_key,
            help=_t("rainfall_help"),
        )

    st.markdown(
        f"<h5 style='margin-top:1.5em; color:#388e3c;'>{_t('soil_ph')}</h5>",
        unsafe_allow_html=True,
    )
    ph_value = st.slider(
        f"🧪 {_t('soil_ph')}",
        min_value=3.5,
        max_value=9.5,
        step=0.1,
        format="%.1f",
        key=f"{key_prefix}_ph",
        help=_t("soil_ph_help"),
    )
    scale_cols = st.columns(3)
    with scale_cols[0]:
        st.caption(_t("acidic"))
    with scale_cols[1]:
        st.markdown(
            f"<p style='text-align: center; font-size: 12px; color: #888;'>{_t('neutral')}</p>",
            unsafe_allow_html=True,
        )
    with scale_cols[2]:
        st.markdown(
            f"<p style='text-align: right; font-size: 12px; color: #888;'>{_t('alkaline')}</p>",
            unsafe_allow_html=True,
        )

    return {
        "N": n_value,
        "P": p_value,
        "K": k_value,
        "ph": ph_value,
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall,
    }


def crop_selector(label: str = "", *, key_prefix: str = "crop") -> str:
    return st.selectbox(label or _t("crop_select"), CROPS, key=f"{key_prefix}_select")


def disease_image_form(key_prefix: str = "disease") -> tuple[str, bytes | None]:
    st.subheader(f"🩺 {_t('leaf_scan')}")
    crop = crop_selector(_t("crop_for_diagnosis"), key_prefix=f"{key_prefix}_crop")
    image = st.file_uploader(
        _t("upload_leaf_image"),
        type=["jpg", "jpeg", "png"],
        key=f"{key_prefix}_uploader",
    )
    image_bytes = image.read() if image is not None else None
    return crop, image_bytes


def disease_manual_form(key_prefix: str = "disease_manual") -> tuple[str, str]:
    disease = st.selectbox(
        _t("disease"),
        CROPS + ["Leaf Rust", "Powdery Mildew", "Bacterial Leaf Blight"],
        key=f"{key_prefix}_name",
    )
    severity = st.selectbox(
        _t("severity"),
        DISEASE_SEVERITIES,
        index=1,
        key=f"{key_prefix}_severity",
    )
    return disease, severity

