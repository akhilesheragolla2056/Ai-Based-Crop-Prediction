"""Form components for capture of agronomic inputs."""

from __future__ import annotations

from typing import Mapping

import streamlit as st


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


DISEASE_SEVERITIES = ["Low", "Medium", "High"]


def environmental_inputs(key_prefix: str = "env") -> dict[str, float]:
    col1, col2, col3 = st.columns(3)

    with col1:
        n_value = st.number_input(
            "Nitrogen (N)",
            min_value=0.0,
            max_value=200.0,
            value=DEFAULT_METRICS["N"],
            key=f"{key_prefix}_nitrogen",
        )
        rainfall = st.number_input(
            "Rainfall (mm)",
            min_value=0.0,
            max_value=400.0,
            value=DEFAULT_METRICS["rainfall"],
            key=f"{key_prefix}_rainfall",
        )
    with col2:
        p_value = st.number_input(
            "Phosphorus (P)",
            min_value=0.0,
            max_value=200.0,
            value=DEFAULT_METRICS["P"],
            key=f"{key_prefix}_phosphorus",
        )
        temperature = st.number_input(
            "Temperature (°C)",
            min_value=0.0,
            max_value=50.0,
            value=DEFAULT_METRICS["temperature"],
            key=f"{key_prefix}_temperature",
        )
    with col3:
        k_value = st.number_input(
            "Potassium (K)",
            min_value=0.0,
            max_value=200.0,
            value=DEFAULT_METRICS["K"],
            key=f"{key_prefix}_potassium",
        )
        humidity = st.number_input(
            "Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=DEFAULT_METRICS["humidity"],
            key=f"{key_prefix}_humidity",
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
