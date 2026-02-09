from __future__ import annotations

DISEASE_SEVERITIES = ["Low", "Medium", "High"]
"""Form components for capture of agronomic inputs."""

from datetime import timezone
from typing import Mapping

import streamlit as st

from backend.weather_service import (
    WeatherProviderError,
    WeatherSnapshot,
    get_weather_snapshot,
)

from backend.npk_lookup import get_npk_for_region
from backend.rainfall_lookup import get_avg_rainfall_for_region
from backend.ph_lookup import get_avg_ph_for_region

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


def environmental_inputs(key_prefix: str = "env") -> dict[str, float]:
    temp_key = f"{key_prefix}_temperature"
    humidity_key = f"{key_prefix}_humidity"
    rainfall_key = f"{key_prefix}_rainfall"
    weather_meta_key = f"{key_prefix}_weather_meta"

    for state_key, default in (
        (temp_key, DEFAULT_METRICS["temperature"]),
        (humidity_key, DEFAULT_METRICS["humidity"]),
        (rainfall_key, DEFAULT_METRICS["rainfall"]),
    ):
        if state_key not in st.session_state:
            st.session_state[state_key] = default

    if weather_meta_key not in st.session_state:
        st.session_state[weather_meta_key] = {}

    with st.expander("🌤 Auto-fill weather", expanded=False):
        location = st.text_input(
            "Location (City, State)",
            value=st.session_state[weather_meta_key].get("location", ""),
            key=f"{key_prefix}_weather_location",
            help="Example: Pune, Maharashtra",
        )

        if st.button("Fetch live weather", key=f"{key_prefix}_weather_fetch"):
            try:
                snapshot: WeatherSnapshot = get_weather_snapshot(location)
            except WeatherProviderError as exc:
                st.error(str(exc))
            else:
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
                # Auto-fill NPK if region found
                npk = get_npk_for_region(region)
                if npk:
                    st.session_state[f"{key_prefix}_nitrogen"] = npk["N"]
                    st.session_state[f"{key_prefix}_phosphorus"] = npk["P"]
                    st.session_state[f"{key_prefix}_potassium"] = npk["K"]
                    st.success(
                        f"Auto-filled NPK for {region.title()} (N={npk['N']}, P={npk['P']}, K={npk['K']})"
                    )
                else:
                    st.info("No NPK data found for this region. Please enter manually.")
                # Auto-fill pH if region found
                avg_ph = get_avg_ph_for_region(region)
                if avg_ph:
                    st.session_state[f"{key_prefix}_ph"] = avg_ph
                    st.success(f"Auto-filled soil pH for {region.title()}: {avg_ph}")
                else:
                    st.info(
                        "No soil pH data found for this region. Please enter manually."
                    )
                observed_local = snapshot.observed_at.astimezone(timezone.utc)
                st.success(
                    f"Loaded weather from {snapshot.provider.title()} (observed {observed_local.strftime('%Y-%m-%d %H:%M')} UTC)."
                )

    # Layout for N, P, K, temperature, humidity, rainfall
    col1, col2, col3 = st.columns(3)
    with col1:
        n_value = st.number_input(
            "Nitrogen (N)",
            min_value=0.0,
            max_value=2000.0,
            value=DEFAULT_METRICS["N"],
            key=f"{key_prefix}_nitrogen",
        )
        rainfall = st.number_input(
            "Rainfall (mm)",
            min_value=0.0,
            max_value=4000.0,
            value=float(st.session_state[rainfall_key]),
            key=rainfall_key,
        )
    with col2:
        p_value = st.number_input(
            "Phosphorus (P)",
            min_value=0.0,
            max_value=2000.0,
            value=DEFAULT_METRICS["P"],
            key=f"{key_prefix}_phosphorus",
        )
        temperature = st.number_input(
            "Temperature (°C)",
            min_value=0.0,
            max_value=50.0,
            value=st.session_state[temp_key],
            key=temp_key,
        )
    with col3:
        k_value = st.number_input(
            "Potassium (K)",
            min_value=0.0,
            max_value=2000.0,
            value=DEFAULT_METRICS["K"],
            key=f"{key_prefix}_potassium",
        )
        humidity = st.number_input(
            "Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state[humidity_key],
            key=humidity_key,
        )

    # Soil pH - Beautiful gradient slider
    # Custom CSS to style the Streamlit slider with gradient background
    st.markdown(
        """
    <style>
        /* Custom pH slider styling - gradient track */
        .stSlider [data-baseweb="slider"] {
            background: linear-gradient(to right, #ff6b6b 0%, #feca57 25%, #48dbfb 50%, #1dd1a1 75%, #5f27cd 100%) !important;
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

    # pH Slider
    ph_value = st.slider(
        "Soil pH",
        min_value=3.5,
        max_value=9.5,
        value=DEFAULT_METRICS["ph"],
        step=0.1,
        format="%.1f",
        key=f"{key_prefix}_ph",
    )

    # pH scale labels
    scale_cols = st.columns(3)
    with scale_cols[0]:
        st.caption("3.5 (Acidic)")
    with scale_cols[1]:
        st.markdown(
            "<p style='text-align: center; font-size: 12px; color: #888;'>6.5 (Neutral)</p>",
            unsafe_allow_html=True,
        )
    with scale_cols[2]:
        st.markdown(
            "<p style='text-align: right; font-size: 12px; color: #888;'>9.5 (Alkaline)</p>",
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


def crop_selector(label: str = "Select Crop", *, key_prefix: str = "crop") -> str:
    return st.selectbox(label, CROPS, key=f"{key_prefix}_select")


def disease_image_form(key_prefix: str = "disease") -> tuple[str, bytes | None]:
    st.subheader("🩺 Leaf Scan")
    crop = crop_selector("Crop for Diagnosis", key_prefix=f"{key_prefix}_crop")
    image = st.file_uploader(
        "Upload leaf image",
        type=["jpg", "jpeg", "png"],
        key=f"{key_prefix}_uploader",
    )
    image_bytes = image.read() if image is not None else None
    return crop, image_bytes


def disease_manual_form(key_prefix: str = "disease_manual") -> tuple[str, str]:
    disease = st.selectbox(
        "Disease",
        CROPS + ["Leaf Rust", "Powdery Mildew", "Bacterial Leaf Blight"],
        key=f"{key_prefix}_name",
    )
    severity = st.selectbox(
        "Severity",
        DISEASE_SEVERITIES,
        index=1,
        key=f"{key_prefix}_severity",
    )
    return disease, severity
