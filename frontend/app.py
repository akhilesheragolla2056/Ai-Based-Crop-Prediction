from __future__ import annotations
import sys
import os

# Ensure project root is in sys.path for module imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from dotenv import load_dotenv
from contextlib import contextmanager
from types import SimpleNamespace
import math
import streamlit as st
from backend.crop_recommendation import ModelNotReady, recommend_crops
from backend.fertilizer_recommendation import recommend_fertilizer
from backend.market_prices import get_market_price  # Live market prices from API
from backend.pesticide_recommendation import recommend_pesticide, supported_diseases
from backend.yield_prediction import predict_yield
from frontend.components.cards import info_card, list_card
from frontend.components.forms import DISEASE_SEVERITIES, environmental_inputs
from frontend.components.layout import inject_theme

load_dotenv()
"""FasalSaarthi – Professional AI Crop Recommendation Dashboard with Multi-language Support."""


# ══════════════════════════════════════════════════════════════════════════════
# TRANSLATIONS (English + Hindi)
# ══════════════════════════════════════════════════════════════════════════════
TRANSLATIONS = {
    "en": {
        "app_title": "FasalSaarthi – AI Crop Recommendation System",
        "tagline": "AI-Powered Smart Farming",
        "subtitle": "Helping farmers reduce risk and improve yield",
        "field_profile": "Field & Weather Profile",
        "get_recommendations": "🚀 Get Smart Recommendations",
        "crop_recommendation": "Crop Recommendation",
        "top_crops_msg": "Top crops identified based on your soil and climate profile",
        "why_crops": "Why these crops?",
        "market_outlook": "Market Outlook & Prices",
        "water_requirement": "Water Requirement",
        "weather_advisory": "Weather Advisory",
        "fertilizer_rec": "Fertilizer Recommendations",
        "nutrient_plan": "Nutrient plan tailored for",
        "soil_health": "Soil Health Tips",
        "pest_disease": "Pest & Disease Management",
        "select_disease": "Select a disease to get protection recommendations",
        "get_protection": "Get Protection Plan",
        "yield_projection": "Yield Projection",
        "expected_yield": "Expected Yield",
        "yield_category": "Yield Category",
        "est_revenue": "Est. Revenue",
        "per_acre": "per acre (approx)",
        "weather_alerts": "Weather Alerts",
        "price": "Price",
        "per_quintal": "per quintal",
        "trend": "Trend",
        "demand": "Demand",
        "seasonal_need": "Seasonal Need",
        "irrigations": "Irrigations",
        "critical_stage": "Critical Stage",
        "suitability": "Suitability",
        "confidence": "Confidence",
        "chemical": "Chemical",
        "frequency": "Frequency",
        "safety": "Safety Guidance",
        "organic_alt": "Organic Alternative",
        "common_diseases": "Common Diseases",
        "severity": "Severity Level",
        "quantity": "Quantity",
        "why": "Why",
        "organic_option": "Organic Option",
        "about": "About",
        "language": "Language",
        "home": "Home",
    },
    "hi": {
        "app_title": "फसलसारथी – AI फसल सिफारिश प्रणाली",
        "tagline": "AI-संचालित स्मार्ट खेती",
        "subtitle": "किसानों को जोखिम कम करने और उपज बढ़ाने में मदद",
        "field_profile": "खेत और मौसम प्रोफाइल",
        "get_recommendations": "🚀 स्मार्ट सिफारिशें प्राप्त करें",
        "crop_recommendation": "फसल सिफारिश",
        "top_crops_msg": "आपकी मिट्टी और जलवायु प्रोफाइल के आधार पर शीर्ष फसलें",
        "why_crops": "ये फसलें क्यों?",
        "market_outlook": "बाजार दृष्टिकोण और कीमतें",
        "water_requirement": "पानी की आवश्यकता",
        "weather_advisory": "मौसम सलाह",
        "fertilizer_rec": "उर्वरक सिफारिशें",
        "nutrient_plan": "पोषक तत्व योजना के लिए",
        "soil_health": "मिट्टी स्वास्थ्य सुझाव",
        "pest_disease": "कीट और रोग प्रबंधन",
        "select_disease": "सुरक्षा सिफारिशें प्राप्त करने के लिए रोग चुनें",
        "get_protection": "सुरक्षा योजना प्राप्त करें",
        "yield_projection": "उपज अनुमान",
        "expected_yield": "अपेक्षित उपज",
        "yield_category": "उपज श्रेणी",
        "est_revenue": "अनुमानित आय",
        "per_acre": "प्रति एकड़ (लगभग)",
        "weather_alerts": "मौसम चेतावनी",
        "price": "कीमत",
        "per_quintal": "प्रति क्विंटल",
        "trend": "रुझान",
        "demand": "मांग",
        "seasonal_need": "मौसमी आवश्यकता",
        "irrigations": "सिंचाई",
        "critical_stage": "महत्वपूर्ण चरण",
        "suitability": "उपयुक्तता",
        "confidence": "विश्वास",
        "chemical": "रासायनिक",
        "frequency": "आवृत्ति",
        "safety": "सुरक्षा मार्गदर्शन",
        "organic_alt": "जैविक विकल्प",
        "common_diseases": "सामान्य रोग",
        "severity": "गंभीरता स्तर",
        "quantity": "मात्रा",
        "why": "क्यों",
        "organic_option": "जैविक विकल्प",
        "about": "परिचय",
        "language": "भाषा",
        "home": "होम",
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# COMPREHENSIVE MARKET DATA (All 22 crops from dataset)
# ══════════════════════════════════════════════════════════════════════════════
MARKET_DATA = {
    "rice": {"price": 2040, "trend": "Stable", "demand": "High"},
    "wheat": {"price": 2275, "trend": "Rising", "demand": "High"},
    "maize": {"price": 1870, "trend": "Stable", "demand": "Moderate"},
    "cotton": {"price": 6620, "trend": "Rising", "demand": "High"},
    "groundnut": {"price": 5550, "trend": "Rising", "demand": "High"},
    "sugarcane": {"price": 315, "trend": "Stable", "demand": "High"},
    "banana": {"price": 1200, "trend": "Rising", "demand": "High"},
    "apple": {"price": 8500, "trend": "Stable", "demand": "Moderate"},
    "mango": {"price": 4200, "trend": "Seasonal", "demand": "High"},
    "grapes": {"price": 3800, "trend": "Rising", "demand": "Moderate"},
    "coffee": {"price": 9500, "trend": "Rising", "demand": "High"},
    "jute": {"price": 4800, "trend": "Stable", "demand": "Moderate"},
    "coconut": {"price": 2500, "trend": "Stable", "demand": "High"},
    "papaya": {"price": 1800, "trend": "Rising", "demand": "Moderate"},
    "orange": {"price": 3200, "trend": "Stable", "demand": "High"},
    "chickpea": {"price": 5100, "trend": "Rising", "demand": "High"},
    "kidneybeans": {"price": 6200, "trend": "Stable", "demand": "Moderate"},
    "pigeonpeas": {"price": 6800, "trend": "Rising", "demand": "High"},
    "mothbeans": {"price": 5500, "trend": "Stable", "demand": "Moderate"},
    "mungbean": {"price": 7200, "trend": "Rising", "demand": "High"},
    "blackgram": {"price": 6500, "trend": "Rising", "demand": "High"},
    "lentil": {"price": 5800, "trend": "Stable", "demand": "High"},
    "pomegranate": {"price": 8000, "trend": "Rising", "demand": "Moderate"},
    "watermelon": {"price": 1500, "trend": "Seasonal", "demand": "High"},
    "muskmelon": {"price": 2000, "trend": "Seasonal", "demand": "Moderate"},
}

WATER_REQUIREMENT = {
    "rice": {
        "mm": "1200-1400",
        "cycles": "20-25",
        "stage": "Flowering & Grain filling",
    },
    "wheat": {"mm": "450-650", "cycles": "4-6", "stage": "Crown root initiation"},
    "maize": {"mm": "500-800", "cycles": "6-8", "stage": "Tasseling & Silking"},
    "cotton": {"mm": "700-1300", "cycles": "6-8", "stage": "Flowering-Boll formation"},
    "groundnut": {
        "mm": "500-700",
        "cycles": "5-6",
        "stage": "Pegging & Pod development",
    },
    "sugarcane": {"mm": "1500-2500", "cycles": "30-35", "stage": "Grand growth phase"},
    "banana": {"mm": "1200-1500", "cycles": "Weekly", "stage": "Bunch emergence"},
    "apple": {"mm": "800-1000", "cycles": "10-12", "stage": "Fruit development"},
    "mango": {"mm": "400-600", "cycles": "6-8", "stage": "Flowering & Fruit set"},
    "grapes": {"mm": "500-700", "cycles": "Weekly", "stage": "Berry development"},
    "coffee": {
        "mm": "1500-2500",
        "cycles": "15-20",
        "stage": "Flowering & Berry expansion",
    },
    "jute": {"mm": "500-800", "cycles": "5-7", "stage": "Vegetative growth"},
    "coconut": {"mm": "1300-2500", "cycles": "Monthly", "stage": "Year-round"},
    "papaya": {"mm": "1500-2000", "cycles": "Weekly", "stage": "Fruit development"},
    "orange": {"mm": "900-1200", "cycles": "8-12", "stage": "Flowering & Fruit set"},
    "chickpea": {"mm": "300-400", "cycles": "2-3", "stage": "Flowering"},
    "kidneybeans": {"mm": "400-500", "cycles": "4-5", "stage": "Flowering & Pod fill"},
    "pigeonpeas": {"mm": "600-700", "cycles": "3-4", "stage": "Flowering"},
    "mothbeans": {"mm": "200-300", "cycles": "2-3", "stage": "Flowering"},
    "mungbean": {"mm": "300-400", "cycles": "3-4", "stage": "Flowering & Pod fill"},
    "blackgram": {"mm": "300-400", "cycles": "3-4", "stage": "Flowering"},
    "lentil": {"mm": "250-350", "cycles": "2-3", "stage": "Flowering & Pod fill"},
    "pomegranate": {"mm": "500-800", "cycles": "6-8", "stage": "Fruit development"},
    "watermelon": {"mm": "400-600", "cycles": "5-6", "stage": "Fruit expansion"},
    "muskmelon": {"mm": "400-500", "cycles": "5-6", "stage": "Fruit development"},
}


def get_text(key: str) -> str:
    """Get translated text based on current language."""
    lang = st.session_state.get("language", "en")
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)


def get_market_info(crop_name: str) -> dict:
    """Get market data for a crop from live API with fallback."""
    return get_market_price(crop_name)


def get_water_info(crop_name: str) -> dict:
    """Get water requirement data for a crop."""
    from backend.utils import get_water_requirement_for_crop

    avg_water = get_water_requirement_for_crop(crop_name)
    key = crop_name.lower().strip()
    fallback = WATER_REQUIREMENT.get(
        key, {"mm": "400-600", "cycles": "5-8", "stage": "Flowering"}
    )
    if avg_water is not None:
        # Use fallback's stage for critical stage if available
        return {
            "mm": f"{avg_water:.0f}",
            "cycles": "-",
            "stage": fallback.get("stage", "-"),
            "source": "kaggle",
        }
    fallback["source"] = "fallback"
    return fallback


def build_regional_recommendations(
    crops: list[str],
    scores: dict[str, float] | None,
    region: str | None,
    source: str | None,
):
    if not crops:
        return []
    score_map = scores or {}
    recommendations = []
    for idx, crop in enumerate(crops[:3]):
        score = score_map.get(crop, 0.5)
        if source == "synthetic":
            rationale = (
                f"Synthetic fallback based on overall dataset for {region.title()}."
                if region
                else "Synthetic fallback based on overall dataset."
            )
            suitability = "Synthetic match"
        else:
            rationale = (
                f"Commonly grown in {region.title()} based on dataset distribution."
                if region
                else "Commonly grown in this region based on dataset distribution."
            )
            suitability = "Regional match"
        recommendations.append(
            SimpleNamespace(
                name=crop,
                score=score,
                suitability=suitability,
                rationale=rationale,
            )
        )
    return recommendations


@contextmanager
def spinner(label: str):
    with st.spinner(label):
        yield


def apply_theme():
    """Apply professional themed styling for each section."""
    css = """
    <style>
    /* ═══════════════════════════════════════════════════════════════════════
       PROFESSIONAL THEME COLORS
       - Crop: Green (#1B5E20, #4CAF50)
       - Market: Gold/Amber (#F57C00, #FFB300)
       - Water: Blue (#0277BD, #03A9F4)
       - Fertilizer: Purple (#6A1B9A, #AB47BC)
       - Pest: Red/Orange (#D32F2F, #FF5722)
       - Yield: Teal (#00695C, #26A69A)
    ═══════════════════════════════════════════════════════════════════════ */
    
    /* Primary button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #1B5E20 0%, #4CAF50 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(27, 94, 32, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(27, 94, 32, 0.4) !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #1B5E20 0%, #4CAF50 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       CROP RECOMMENDATION THEME (Green)
    ═══════════════════════════════════════════════════════════════════════ */
    .crop-card {
        background: linear-gradient(145deg, #E8F5E9 0%, #C8E6C9 100%) !important;
        border-left: 5px solid #1B5E20 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    .crop-card [data-testid="stMetricValue"] {
        color: #1B5E20 !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }
    
    .crop-card [data-testid="stMetricDelta"] {
        color: #388E3C !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       MARKET OUTLOOK THEME (Gold/Amber)
    ═══════════════════════════════════════════════════════════════════════ */
    .market-card {
        background: linear-gradient(145deg, #FFF8E1 0%, #FFECB3 100%) !important;
        border-left: 5px solid #F57C00 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    .market-card [data-testid="stMetricValue"] {
        color: #E65100 !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }
    
    .market-card [data-testid="stMetricDelta"] {
        color: #FF8F00 !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       WATER REQUIREMENT THEME (Blue)
    ═══════════════════════════════════════════════════════════════════════ */
    .water-card {
        background: linear-gradient(145deg, #E1F5FE 0%, #B3E5FC 100%) !important;
        border-left: 5px solid #0277BD !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    .water-card [data-testid="stMetricValue"] {
        color: #01579B !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }
    
    .water-card [data-testid="stMetricDelta"] {
        color: #0288D1 !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       FERTILIZER THEME (Purple)
    ═══════════════════════════════════════════════════════════════════════ */
    .fertilizer-card {
        background: linear-gradient(145deg, #F3E5F5 0%, #E1BEE7 100%) !important;
        border-left: 5px solid #6A1B9A !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    .fertilizer-card h3 {
        color: #6A1B9A !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       PEST & DISEASE THEME (Red/Orange)
    ═══════════════════════════════════════════════════════════════════════ */
    .pest-card {
        background: linear-gradient(145deg, #FFEBEE 0%, #FFCDD2 100%) !important;
        border-left: 5px solid #D32F2F !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    .pest-card [data-testid="stMetricValue"] {
        color: #C62828 !important;
        font-weight: 700 !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       YIELD PROJECTION THEME (Teal)
    ═══════════════════════════════════════════════════════════════════════ */
    .yield-card {
        background: linear-gradient(145deg, #E0F2F1 0%, #B2DFDB 100%) !important;
        border-left: 5px solid #00695C !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    .yield-card [data-testid="stMetricValue"] {
        color: #004D40 !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }
    
    .yield-card [data-testid="stMetricDelta"] {
        color: #00897B !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       SECTION HEADERS
    ═══════════════════════════════════════════════════════════════════════ */
    .section-header-crop {
        background: linear-gradient(90deg, #1B5E20 0%, #4CAF50 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
    }
    
    .section-header-market {
        background: linear-gradient(90deg, #E65100 0%, #FFB300 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
    }
    
    .section-header-water {
        background: linear-gradient(90deg, #01579B 0%, #03A9F4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
    }
    
    .section-header-fertilizer {
        background: linear-gradient(90deg, #4A148C 0%, #AB47BC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
    }
    
    .section-header-pest {
        background: linear-gradient(90deg, #B71C1C 0%, #FF5722 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
    }
    
    .section-header-yield {
        background: linear-gradient(90deg, #004D40 0%, #26A69A 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       GENERAL ENHANCEMENTS
    ═══════════════════════════════════════════════════════════════════════ */
    /* Card hover effects */
    .stVerticalBlock[data-testid="stVerticalBlock"] > div > div > .stVerticalBlock {
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    
    .stVerticalBlock[data-testid="stVerticalBlock"] > div > div > .stVerticalBlock:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(145deg, #E8F5E9 0%, #C8E6C9 100%) !important;
        border-left: 4px solid #4CAF50 !important;
        border-radius: 8px !important;
    }
    
    /* Info message styling */
    .stInfo {
        background: linear-gradient(145deg, #E3F2FD 0%, #BBDEFB 100%) !important;
        border-left: 4px solid #2196F3 !important;
        border-radius: 8px !important;
    }
    
    /* Custom scrollbar */
    * {
        scrollbar-width: thin;
        scrollbar-color: #1B5E20 transparent;
    }
    
    *::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    *::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #1B5E20 0%, #4CAF50 100%);
        border-radius: 4px;
    }
    
    /* ═══════════════════════════════════════════════════════════════════════
       LIVE BADGE ANIMATION
    ═══════════════════════════════════════════════════════════════════════ */
    @keyframes pulse-live {
        0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
        70% { box-shadow: 0 0 0 8px rgba(76, 175, 80, 0); }
        100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
    }
    
    .live-badge {
        background: linear-gradient(90deg, #4CAF50 0%, #66BB6A 100%);
        color: white;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 700;
        margin-left: 8px;
        animation: pulse-live 2s infinite;
        display: inline-block;
    }
    
    .msp-badge {
        background: linear-gradient(90deg, #757575 0%, #9E9E9E 100%);
        color: white;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 8px;
        display: inline-block;
    }
    
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_header():
    """Render header using native Streamlit components."""
    # Language selector in top-right
    col_spacer, col_lang = st.columns([6, 1])

    with col_lang:
        st.selectbox(
            get_text("language"),
            options=["en", "hi"],
            format_func=lambda x: "English" if x == "en" else "हिंदी",
            key="language",
            label_visibility="collapsed",
        )

    # Centered header with green FasalSaarthi title
    st.markdown("---")
    st.markdown(
        "<h1 style='text-align: center;'>🌾 FasalSaarthi</h1>", unsafe_allow_html=True
    )
    st.markdown(
        f"<p style='text-align: center; font-weight: bold;'>{get_text('tagline')}</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align: center; color: gray; font-size: 0.9rem;'>{get_text('subtitle')}</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")


def render_crop_cards(recommendations):
    """Render crop cards with professional green theme."""
    st.markdown(
        f"<h2 class='section-header-crop'>🌾 {get_text('crop_recommendation')}</h2>",
        unsafe_allow_html=True,
    )
    st.success(get_text("top_crops_msg"))

    cols = st.columns(len(recommendations))
    scores = [getattr(rec, "score", None) for rec in recommendations]
    numeric_entries = [
        (idx, score)
        for idx, score in enumerate(scores)
        if isinstance(score, (int, float))
    ]
    is_probability_like = (
        len(numeric_entries) == len(recommendations)
        and all(0 <= score <= 1 for _, score in numeric_entries)
        and 0.95 <= sum(score for _, score in numeric_entries) <= 1.05
    )
    percent_values: dict[int, int] = {}
    if numeric_entries:
        total_score = sum(score for _, score in numeric_entries)
        if total_score <= 0:
            normalized = [(idx, 1 / len(numeric_entries)) for idx, _ in numeric_entries]
        else:
            normalized = [(idx, score / total_score) for idx, score in numeric_entries]
        scaled = [(idx, score * 100) for idx, score in normalized]
        floored = {idx: math.floor(value) for idx, value in scaled}
        remainder = 100 - sum(floored.values())
        if remainder < 0:
            remainder = 0
        fractions = sorted(
            scaled,
            key=lambda item: item[1] - math.floor(item[1]),
            reverse=True,
        )
        for idx, _ in fractions[:remainder]:
            floored[idx] += 1
        percent_values = floored
    rank_map: dict[int, str] = {}
    if is_probability_like:
        ranked = sorted(
            [(idx, scores[idx]) for idx in range(len(scores))],
            key=lambda x: x[1],
            reverse=True,
        )
        for rank, (idx, _) in enumerate(ranked):
            rank_map[idx] = "High" if rank == 0 else ("Medium" if rank == 1 else "Low")

    for idx, rec in enumerate(recommendations):
        with cols[idx]:
            suitability_label = "Medium"
            raw_suitability = getattr(rec, "suitability", "")
            if isinstance(raw_suitability, str) and raw_suitability.lower() in (
                "low",
                "medium",
                "high",
            ):
                suitability_label = raw_suitability.title()
            elif is_probability_like and idx in rank_map:
                suitability_label = rank_map[idx]
            else:
                score = getattr(rec, "score", None)
                if isinstance(score, (int, float)):
                    if score >= 0.6:
                        suitability_label = "High"
                    elif score >= 0.35:
                        suitability_label = "Medium"
                    else:
                        suitability_label = "Low"
            medal = "🥇" if idx == 0 else ("🥈" if idx == 1 else "🥉")
            # Card with green crop theme
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(145deg, #E8F5E9 0%, #C8E6C9 100%);
                    border-left: 5px solid #1B5E20;
                    border-radius: 12px;
                    padding: 1.2rem;
                    margin-bottom: 0.5rem;
                    box-shadow: 0 4px 15px rgba(27, 94, 32, 0.15);
                ">
                    <h3 style="color: #1B5E20; margin: 0 0 0.5rem 0;">{medal} #{idx + 1}</h3>
                    <p style="font-weight: 700; font-size: 1.3rem; color: #2E7D32; margin: 0.3rem 0;">{rec.name.title()}</p>
                    <p style="font-size: 2rem; font-weight: 800; color: #1B5E20; margin: 0.5rem 0;">{percent_values.get(idx, int(round((rec.score or 0) * 100)))}%</p>
                    <p style="color: #388E3C; font-weight: 600;">📈 {suitability_label} suitability</p>
                    <p style="color: #555; font-size: 0.85rem;">{get_text("suitability")}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_market_section(recommendations):
    """Render market outlook with professional gold/amber theme and live API data."""
    # Header with refresh button
    header_col, refresh_col = st.columns([5, 1])
    with header_col:
        st.markdown(
            f"<h2 class='section-header-market'>💰 {get_text('market_outlook')}</h2>",
            unsafe_allow_html=True,
        )
    with refresh_col:
        if st.button("🔄", key="refresh_prices", help="Refresh live prices"):
            from backend.market_prices import refresh_price_cache

            refresh_price_cache()
            st.rerun()

    cols = st.columns(len(recommendations))
    for idx, rec in enumerate(recommendations):
        market = get_market_info(rec.name)
        with cols[idx]:
            trend_icon = (
                "📈"
                if market["trend"] == "Rising"
                else ("📉" if market["trend"] == "Falling" else "📊")
            )
            # trend_color is not used, so removed

            # Build live badge
            is_live = market.get("is_live", False)
            source = market.get("source", "MSP Data")

            # Use native Streamlit container with border for reliability
            with st.container(border=True):
                # Header row with crop name and badge
                if is_live:
                    st.markdown(f"**{rec.name.title()}** 🟢 `LIVE`")
                else:
                    st.markdown(f"**{rec.name.title()}** 📋 `MSP`")

                # Price display
                st.metric(
                    label=f"{get_text('price')} ({get_text('per_quintal')})",
                    value=f"₹{market['price']:,.0f}",
                    delta=f"{trend_icon} {market['trend']}",
                )

                # Additional info
                st.caption(f"📊 {get_text('demand')}: **{market['demand']}**")
                st.caption(f"📡 {source}")


def render_water_section(recommendations):
    """Render water requirement with professional blue theme."""
    st.markdown(
        f"<h2 class='section-header-water'>💧 {get_text('water_requirement')}</h2>",
        unsafe_allow_html=True,
    )

    cols = st.columns(len(recommendations))
    for idx, rec in enumerate(recommendations):
        water = get_water_info(rec.name)
        label = (
            "Daily Water Requirement"
            if water.get("source") == "kaggle"
            else "Seasonal Water Requirement"
        )
        seasonal_label = (
            label if water.get("source") == "kaggle" else get_text("seasonal_need")
        )
        with cols[idx]:
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(145deg, #E1F5FE 0%, #B3E5FC 100%);
                    border-left: 5px solid #0277BD;
                    border-radius: 12px;
                    padding: 1.2rem;
                    margin-bottom: 0.5rem;
                    box-shadow: 0 4px 15px rgba(2, 119, 189, 0.15);
                ">
                    <p style="font-weight: 700; font-size: 1.2rem; color: #01579B; margin: 0 0 0.5rem 0;">{rec.name.title()}</p>
                    <p style="font-size: 1rem; color: #0288D1; margin: 0;">{label}</p>
                    <p style="font-size: 2rem; font-weight: 800; color: #01579B; margin: 0.5rem 0;">{water["mm"]} mm</p>
                    <p style="color: #0288D1; font-weight: 600;">🔄 {water["cycles"]} {get_text("irrigations")}</p>
                    <p style="color: #546E7A; font-size: 0.9rem;">{seasonal_label}</p>
                    <div style="margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid rgba(2, 119, 189, 0.3);">
                        <p style="color: #D84315; margin: 0; font-weight: 500;">⚠️ {get_text("critical_stage")}: {water["stage"]}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_fertilizer_section(top_crop, features, fert_plan):
    """Render fertilizer recommendations with professional purple theme."""
    st.markdown(
        f"<h2 class='section-header-fertilizer'>🧪 {get_text('fertilizer_rec')}</h2>",
        unsafe_allow_html=True,
    )
    st.write(f"{get_text('nutrient_plan')} **{top_crop}**:")

    if fert_plan:
        cols = st.columns(min(len(fert_plan), 3))
        for idx, advice in enumerate(fert_plan):
            with cols[idx % 3]:
                nutrient_icons = {
                    "Nitrogen": "🌿",
                    "Phosphorus": "🔬",
                    "Potassium": "⚡",
                }
                icon = nutrient_icons.get(advice.nutrient, "🧺")
                # Card with purple fertilizer theme
                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(145deg, #F3E5F5 0%, #E1BEE7 100%);
                        border-left: 5px solid #6A1B9A;
                        border-radius: 12px;
                        padding: 1.2rem;
                        margin-bottom: 0.5rem;
                        box-shadow: 0 4px 15px rgba(106, 27, 154, 0.15);
                    ">
                        <h3 style="color: #6A1B9A; margin: 0 0 0.5rem 0;">{icon} {advice.nutrient}</h3>
                        <p style="font-weight: 700; font-size: 1.1rem; color: #7B1FA2; margin: 0.3rem 0;">{advice.product}</p>
                        <div style="background: rgba(106, 27, 154, 0.1); padding: 0.5rem; border-radius: 6px; margin: 0.5rem 0;">
                            <p style="color: #4A148C; margin: 0; font-weight: 600;">📦 {get_text("quantity")}: {advice.quantity}</p>
                        </div>
                        <p style="color: #5E35B1; font-size: 0.85rem; margin: 0.3rem 0;">📝 {advice.rationale}</p>
                        <div style="margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid rgba(106, 27, 154, 0.3);">
                            <p style="color: #2E7D32; margin: 0; font-size: 0.85rem;">🌱 {advice.organic_option}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.success("✅ Soil profile looks balanced. Maintain current regimen.")


def render_yield_section(top_crop, features):
    """Render yield projection with professional teal theme."""
    st.markdown(
        f"<h2 class='section-header-yield'>📈 {get_text('yield_projection')} <span style='font-size:1.1rem;color:#004D40;'>(for {top_crop.title()})</span></h2>",
        unsafe_allow_html=True,
    )

    projection = predict_yield(top_crop, features)
    market = get_market_info(top_crop)
    price = market.get("price")
    # Defensive: handle None values
    if projection.estimated_output is None or price is None:
        st.error(
            "Yield projection or price data is unavailable for this crop and location.\nReason: {projection.reasoning}"
        )
        st.info(f"Debug info: features used: {features}")
        return
    estimated_revenue = projection.estimated_output * price

    # Use suitability/score to set yield category and confidence
    suitability = None
    if "main_top_crops" in st.session_state and st.session_state["main_top_crops"]:
        for rec in st.session_state["main_top_crops"]:
            if rec.lower() == top_crop.lower():
                suitability = "High"
                break
    # If suitability is high, override
    if suitability == "High":
        projection = projection.__class__(
            crop=projection.crop,
            level="High",
            estimated_output=projection.estimated_output,
            confidence=0.9,
            reasoning=projection.reasoning,
            weather_notes=projection.weather_notes,
        )

    level_icon = (
        "🌟"
        if projection.level == "High"
        else ("📊" if projection.level == "Medium" else "⚠️")
    )
    level_color = (
        "#1B5E20"
        if projection.level == "High"
        else ("#F57C00" if projection.level == "Medium" else "#D32F2F")
    )

    cols = st.columns(3)
    with cols[0]:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(145deg, #E0F2F1 0%, #B2DFDB 100%);
                border-left: 5px solid #00695C;
                border-radius: 12px;
                padding: 1.2rem;
                box-shadow: 0 4px 15px rgba(0, 105, 92, 0.15);
                text-align: center;
            ">
                <p style="color: #004D40; font-size: 0.9rem; margin: 0;">🌾 {get_text("expected_yield")}</p>
                <p style="font-size: 2.5rem; font-weight: 800; color: #004D40; margin: 0.5rem 0;">{projection.estimated_output:.1f}</p>
                <p style="color: #00897B; font-weight: 600;">quintals/acre</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[1]:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(145deg, #E0F2F1 0%, #B2DFDB 100%);
                border-left: 5px solid #00695C;
                border-radius: 12px;
                padding: 1.2rem;
                box-shadow: 0 4px 15px rgba(0, 105, 92, 0.15);
                text-align: center;
            ">
                <p style="color: #004D40; font-size: 0.9rem; margin: 0;">{level_icon} {get_text("yield_category")}</p>
                <p style="font-size: 2.5rem; font-weight: 800; color: {level_color}; margin: 0.5rem 0;">{projection.level}</p>
                <p style="color: #00897B; font-weight: 600;">{get_text("confidence")}: {projection.confidence:.0%}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[2]:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(145deg, #E0F2F1 0%, #B2DFDB 100%);
                border-left: 5px solid #00695C;
                border-radius: 12px;
                padding: 1.2rem;
                box-shadow: 0 4px 15px rgba(0, 105, 92, 0.15);
                text-align: center;
            ">
                <p style="color: #004D40; font-size: 0.9rem; margin: 0;">💰 {get_text("est_revenue")}</p>
                <p style="font-size: 2.5rem; font-weight: 800; color: #004D40; margin: 0.5rem 0;">₹{estimated_revenue:,.0f}</p>
                <p style="color: #00897B; font-weight: 600;">{get_text("per_acre")}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption(f"📝 {projection.reasoning}")

    if projection.weather_notes:
        st.divider()
        list_card(get_text("weather_alerts"), list(projection.weather_notes), icon="⚠️")


def render_about_page():
    """Render the About page with native Streamlit components with box styling."""
    # Hero section
    st.title("🌾 About FasalSaarthi")
    st.write(
        "AI-powered smart farming assistant designed to help Indian farmers "
        "make data-driven decisions for better crop yields and sustainable agriculture."
    )

    st.divider()

    # Key Features Section
    st.subheader("✨ Key Features")

    feature_cols = st.columns(3)
    features = [
        (
            "🌾",
            "Smart Crop Recommendations",
            "AI analyzes soil composition, weather patterns, and local conditions.",
        ),
        (
            "🧪",
            "Fertilizer Planning",
            "Personalized nutrient plans based on soil profile.",
        ),
        (
            "🦠",
            "Pest & Disease Management",
            "Guidance on identifying and managing crop diseases.",
        ),
    ]
    for i, (icon, title, desc) in enumerate(features):
        with feature_cols[i]:
            with st.container(border=True):
                st.markdown(f"### {icon}")
                st.markdown(f"**{title}**")
                st.caption(desc)

    feature_cols2 = st.columns(3)
    features2 = [
        ("📊", "Yield Prediction", "Estimate expected yields and revenue projections."),
        (
            "💧",
            "Water Management",
            "Irrigation recommendations tailored to crop needs.",
        ),
        (
            "💰",
            "Market Insights",
            "Current market prices, trends, and demand information.",
        ),
    ]
    for i, (icon, title, desc) in enumerate(features2):
        with feature_cols2[i]:
            with st.container(border=True):
                st.markdown(f"### {icon}")
                st.markdown(f"**{title}**")
                st.caption(desc)

    st.divider()

    # How to Use Section
    st.subheader("📋 How to Use")

    step_cols = st.columns(4)
    steps = [
        (
            "1️⃣",
            "Enter field data",
            "Provide soil nutrients (N, P, K), pH level, and environmental conditions",
        ),
        (
            "2️⃣",
            "Get recommendations",
            "Click the button to receive personalized crop suggestions",
        ),
        (
            "3️⃣",
            "Explore insights",
            "View market outlook, fertilizer plans, and yield projections",
        ),
        (
            "4️⃣",
            "Plan pest management",
            "Select diseases to get comprehensive protection strategies",
        ),
    ]
    for i, (num, title, desc) in enumerate(steps):
        with step_cols[i]:
            with st.container(border=True):
                st.markdown(f"### {num}")
                st.markdown(f"**{title}**")
                st.caption(desc)

    st.divider()

    # Technology Stack
    st.subheader("🔧 Technology Stack")

    tech_cols = st.columns(4)
    techs = [
        ("🐍", "Python", "Backend"),
        ("🎯", "Streamlit", "Frontend"),
        ("🤖", "Scikit-learn", "ML Models"),
        ("📊", "Pandas", "Data Processing"),
    ]
    for i, (icon, name, role) in enumerate(techs):
        with tech_cols[i]:
            with st.container(border=True):
                st.markdown(f"### {icon}")
                st.markdown(f"**{name}**")
                st.caption(role)

    st.divider()

    # Team Section
    st.subheader("👥 Our Team")
    st.write("Built with ❤️ for Indian farmers by the FasalSaarthi team")
    st.caption("© 2026 FasalSaarthi. All rights reserved.")


def render_home_page():
    """Render the main Home page content."""
    # ═══════════════════════════════════════════════════════════════════════════
    # INPUT SECTION
    # ═══════════════════════════════════════════════════════════════════════════
    st.subheader(f"🌱 {get_text('field_profile')}")

    features = environmental_inputs("main")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        recommend_btn = st.button(
            get_text("get_recommendations"),
            type="primary",
            use_container_width=True,
            key="main_recommend_btn",
        )

    if recommend_btn:
        st.session_state["show_results"] = True
        st.session_state["features"] = features

    # ═══════════════════════════════════════════════════════════════════════════
    # RESULTS SECTION
    # ═══════════════════════════════════════════════════════════════════════════
    if st.session_state.get("show_results"):
        features = st.session_state.get("features", features)
        regional_crops = st.session_state.get("main_top_crops", [])
        regional_scores = st.session_state.get("main_top_crops_scores", {})
        regional_region = st.session_state.get("main_autofill_region")
        regional_source = st.session_state.get("main_top_crops_source")

        with spinner("Analysing your field profile..."):
            try:
                response = recommend_crops(features)
            except ModelNotReady as exc:
                st.error(str(exc))
                return

        if not response.recommendations and not regional_crops:
            st.warning("Model returned no recommendations. Check input values.")
            return

        recommendations = response.recommendations
        if regional_crops:
            recommendations = build_regional_recommendations(
                regional_crops, regional_scores, regional_region, regional_source
            )

        top_crop = recommendations[0].name

        st.markdown("---")

        # Section 1: Crop Recommendation
        render_crop_cards(recommendations)

        with st.expander(f"💡 {get_text('why_crops')}", expanded=False):
            for rec in recommendations:
                info_card(rec.name, rec.rationale, icon="📌")

        st.markdown("---")

        # Section 2: Market Outlook
        render_market_section(recommendations)

        st.markdown("---")

        # Section 3: Water Requirement
        render_water_section(recommendations)
        list_card(get_text("weather_advisory"), list(response.weather_notes), icon="☁️")

        st.markdown("---")

        # Section 4: Fertilizer
        with spinner("Generating fertilizer plan..."):
            fert_plan = recommend_fertilizer(top_crop, features)
        render_fertilizer_section(top_crop, features, fert_plan)
        list_card(get_text("soil_health"), list(response.soil_tips), icon="🌱")

        st.markdown("---")

        # Section 5: Pest & Disease
        st.markdown(
            f"<h2 class='section-header-pest'>🐛 {get_text('pest_disease')}</h2>",
            unsafe_allow_html=True,
        )
        st.write(get_text("select_disease"))

        pest_col1, pest_col2 = st.columns([2, 1])
        with pest_col1:
            diseases = supported_diseases()
            selected_disease = st.selectbox(
                get_text("common_diseases"),
                diseases,
                key="pest_disease_select",
            )
        with pest_col2:
            severity = st.selectbox(
                get_text("severity"),
                DISEASE_SEVERITIES,
                index=1,
                key="pest_severity",
            )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            protection_btn = st.button(
                get_text("get_protection"),
                type="secondary",
                key="pest_btn",
                use_container_width=True,
            )

        if protection_btn:
            with spinner("Preparing protection plan..."):
                plan = recommend_pesticide(selected_disease, severity=severity)

            # Row 1: Chemical and Frequency with red/orange pest theme
            pest_row1 = st.columns(2)
            with pest_row1[0]:
                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(145deg, #FFEBEE 0%, #FFCDD2 100%);
                        border-left: 5px solid #D32F2F;
                        border-radius: 12px;
                        padding: 1.2rem;
                        box-shadow: 0 4px 15px rgba(211, 47, 47, 0.15);
                    ">
                        <p style="color: #B71C1C; font-size: 0.9rem; margin: 0;">🧴 {get_text("chemical")}</p>
                        <p style="font-size: 1.5rem; font-weight: 800; color: #C62828; margin: 0.5rem 0;">{plan.chemical}</p>
                        <p style="color: #E53935; font-weight: 600;">📏 {plan.dosage}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with pest_row1[1]:
                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(145deg, #FFF3E0 0%, #FFE0B2 100%);
                        border-left: 5px solid #E65100;
                        border-radius: 12px;
                        padding: 1.2rem;
                        box-shadow: 0 4px 15px rgba(230, 81, 0, 0.15);
                    ">
                        <p style="color: #E65100; font-size: 0.9rem; margin: 0;">🔁 {get_text("frequency")}</p>
                        <p style="font-size: 1.5rem; font-weight: 800; color: #BF360C; margin: 0.5rem 0;">{plan.frequency}</p>
                        <p style="color: #FF5722; font-weight: 600;">⚠️ {plan.severity_note}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.write("")  # Spacer

            # Row 2: Safety and Organic Alternative
            pest_row2 = st.columns(2)
            with pest_row2[0]:
                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(145deg, #E3F2FD 0%, #BBDEFB 100%);
                        border-left: 5px solid #1565C0;
                        border-radius: 12px;
                        padding: 1.2rem;
                        box-shadow: 0 4px 15px rgba(21, 101, 192, 0.15);
                    ">
                        <p style="color: #0D47A1; font-size: 0.9rem; margin: 0 0 0.5rem 0;"><strong>🦺 {get_text("safety")}</strong></p>
                        <p style="color: #1976D2; margin: 0;">{plan.safety}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with pest_row2[1]:
                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(145deg, #E8F5E9 0%, #C8E6C9 100%);
                        border-left: 5px solid #2E7D32;
                        border-radius: 12px;
                        padding: 1.2rem;
                        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.15);
                    ">
                        <p style="color: #1B5E20; font-size: 0.9rem; margin: 0 0 0.5rem 0;"><strong>🌱 {get_text("organic_alt")}</strong></p>
                        <p style="color: #388E3C; margin: 0;">{plan.organic_alternative}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("---")

        # Section 6: Yield Projection
        with spinner("Running yield simulation..."):
            render_yield_section(top_crop, features)


def main() -> None:
    st.set_page_config(
        page_title="FasalSaarthi – AI Crop Recommendation",
        page_icon="🌾",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Initialize theme in session state
    if "theme" not in st.session_state:
        st.session_state["theme"] = "light"

    inject_theme()
    apply_theme()
    render_header()

    # Render the main home page directly (no tabs)
    render_home_page()

    # Footer
    st.markdown("---")
    st.caption(
        "🌾 Built with ❤️ for Indian farmers | © 2026 FasalSaarthi. All rights reserved."
    )


if __name__ == "__main__":
    main()
