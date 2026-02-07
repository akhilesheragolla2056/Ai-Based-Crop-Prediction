"""Streamlit application entry point for the crop recommendation system."""

from pathlib import Path

import streamlit as st


st.set_page_config(page_title="AI Crop Recommendation", layout="wide")

st.title("AI-Based Crop Recommendation")
st.caption("Prototype interface – pipeline implementation pending.")

with st.expander("Current Status", expanded=True):
    st.write(
        """
        The backend model and feature pipeline are not yet connected. Use this UI to
        define input collection requirements while the data science components are
        developed. Future iterations will load the trained model artifact from
        `artifacts/models/` and display ranked crop suggestions with yield insights.
        """
    )

st.subheader("Input Parameters")
col1, col2, col3 = st.columns(3)

with col1:
    n_value = st.number_input(
        "Nitrogen (N)", min_value=0.0, max_value=200.0, value=90.0
    )
    rainfall = st.number_input(
        "Rainfall (mm)", min_value=0.0, max_value=400.0, value=210.0
    )

with col2:
    p_value = st.number_input(
        "Phosphorus (P)", min_value=0.0, max_value=200.0, value=42.0
    )
    temperature = st.number_input(
        "Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0
    )

with col3:
    k_value = st.number_input(
        "Potassium (K)", min_value=0.0, max_value=200.0, value=43.0
    )
    humidity = st.number_input(
        "Humidity (%)", min_value=0.0, max_value=100.0, value=60.0
    )

ph = st.slider("Soil pH", min_value=0.0, max_value=14.0, value=6.5, step=0.1)

if st.button("Predict Best Crops", type="primary"):
    st.warning(
        "Model pipeline not yet connected. Training artifacts will be integrated in a later step."
    )

st.subheader("Roadmap Preview")
st.markdown(
    "- Connect to trained RandomForest model for real predictions.\n"
    "- Surface agronomic tips based on nutrient imbalances.\n"
    "- Add weather API enrichment for adaptive recommendations."
)
