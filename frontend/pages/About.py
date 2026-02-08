"""About Page for FasalSaarthi – AI Crop Recommendation System."""

import streamlit as st

from frontend.components.layout import inject_theme


# ══════════════════════════════════════════════════════════════════════════════
# TRANSLATIONS
# ══════════════════════════════════════════════════════════════════════════════
TRANSLATIONS = {
    "en": {
        "page_title": "About FasalSaarthi",
        "hero_title": "🌾 FasalSaarthi",
        "hero_subtitle": "AI-Powered Smart Farming",
        "hero_desc": "Empowering Indian farmers with intelligent crop recommendations, market insights, and sustainable farming practices.",
        "what_is": "What is FasalSaarthi?",
        "what_is_desc": """
FasalSaarthi (फसलसारथी) is an AI-powered agricultural advisory system designed to help Indian farmers make data-driven decisions. 
The name combines 'Fasal' (crop/harvest) and 'Saarthi' (guide/charioteer), representing our mission to guide farmers towards better harvests.

Our platform analyzes soil conditions, weather patterns, and market trends to provide personalized recommendations for:
- **Crop Selection** – Which crops are best suited for your land
- **Fertilizer Planning** – Optimal nutrient management
- **Pest & Disease Management** – Protection strategies
- **Yield Prediction** – Expected output and revenue estimation
- **Market Intelligence** – Current prices and demand trends
        """,
        "features_title": "Key Features",
        "features": [
            (
                "🌿",
                "Smart Crop Recommendations",
                "AI-powered analysis of soil, weather, and market data to suggest the most suitable and profitable crops.",
            ),
            (
                "📊",
                "Market Intelligence",
                "Real-time market prices, trends, and demand analysis for 22+ crops across India.",
            ),
            (
                "💧",
                "Water Management",
                "Customized irrigation schedules and water requirement calculations.",
            ),
            (
                "🧪",
                "Fertilizer Planning",
                "Nutrient-specific recommendations with organic alternatives.",
            ),
            (
                "🐛",
                "Pest & Disease Control",
                "Early warning systems and treatment recommendations.",
            ),
            (
                "📈",
                "Yield Prediction",
                "ML-based yield estimation with revenue projections.",
            ),
        ],
        "tech_title": "Technology Stack",
        "tech_desc": """
FasalSaarthi leverages cutting-edge technologies to deliver accurate recommendations:

- **Machine Learning** – Random Forest & XGBoost models trained on Indian agricultural data
- **Real-time Weather** – Integration with meteorological services for accurate weather insights
- **Market Data** – APMC mandi prices and demand analysis
- **Streamlit** – Modern, responsive web interface
- **Python Backend** – Robust data processing and model inference
        """,
        "crops_title": "Supported Crops (22+)",
        "crops_desc": "Our model supports recommendations for a wide variety of crops grown across India:",
        "crops_list": [
            "🌾 Cereals: Rice, Wheat, Maize",
            "🫘 Pulses: Chickpea, Lentil, Black Gram, Mung Bean, Pigeon Peas, Kidney Beans, Moth Beans",
            "🥭 Fruits: Mango, Banana, Apple, Orange, Grapes, Papaya, Pomegranate, Watermelon, Muskmelon",
            "☕ Cash Crops: Cotton, Jute, Coffee, Coconut",
        ],
        "mission_title": "Our Mission",
        "mission_desc": """
**"Empowering every farmer with AI-driven insights for sustainable and profitable agriculture."**

We believe that technology should be accessible to all farmers, regardless of their farm size or technical expertise. 
FasalSaarthi aims to bridge the knowledge gap and help farmers:

✅ Reduce crop failures through data-driven decisions  
✅ Maximize yield with optimal input management  
✅ Increase profitability by understanding market dynamics  
✅ Adopt sustainable farming practices  
✅ Access agricultural knowledge in their preferred language
        """,
        "team_title": "About the Team",
        "team_desc": """
FasalSaarthi was developed as part of an agricultural technology initiative to support Indian farmers. 
Our team combines expertise in machine learning, agriculture science, and software development to create 
practical solutions for real farming challenges.
        """,
        "contact_title": "Get in Touch",
        "contact_desc": "Have questions or feedback? We'd love to hear from you!",
        "language": "Language",
    },
    "hi": {
        "page_title": "फसलसारथी के बारे में",
        "hero_title": "🌾 फसलसारथी",
        "hero_subtitle": "AI-संचालित स्मार्ट खेती",
        "hero_desc": "भारतीय किसानों को बुद्धिमान फसल सिफारिशों, बाजार अंतर्दृष्टि और टिकाऊ खेती प्रथाओं के साथ सशक्त बनाना।",
        "what_is": "फसलसारथी क्या है?",
        "what_is_desc": """
फसलसारथी एक AI-संचालित कृषि सलाहकार प्रणाली है जो भारतीय किसानों को डेटा-संचालित निर्णय लेने में मदद करती है।
'फसल' (harvest) और 'सारथी' (guide) का संयोजन हमारे मिशन को दर्शाता है - किसानों को बेहतर फसल की ओर मार्गदर्शन करना।

हमारा प्लेटफॉर्म मिट्टी की स्थिति, मौसम पैटर्न और बाजार रुझानों का विश्लेषण करके व्यक्तिगत सिफारिशें प्रदान करता है:
- **फसल चयन** – आपकी भूमि के लिए कौन सी फसलें सर्वोत्तम हैं
- **उर्वरक योजना** – इष्टतम पोषक तत्व प्रबंधन
- **कीट और रोग प्रबंधन** – सुरक्षा रणनीतियां
- **उपज भविष्यवाणी** – अपेक्षित उत्पादन और राजस्व अनुमान
- **बाजार जानकारी** – वर्तमान कीमतें और मांग रुझान
        """,
        "features_title": "मुख्य विशेषताएं",
        "features": [
            (
                "🌿",
                "स्मार्ट फसल सिफारिशें",
                "मिट्टी, मौसम और बाजार डेटा का AI-संचालित विश्लेषण।",
            ),
            ("📊", "बाजार जानकारी", "22+ फसलों के लिए वास्तविक समय बाजार मूल्य और रुझान।"),
            ("💧", "जल प्रबंधन", "कस्टमाइज़्ड सिंचाई कार्यक्रम और पानी की आवश्यकता।"),
            ("🧪", "उर्वरक योजना", "जैविक विकल्पों के साथ पोषक तत्व-विशिष्ट सिफारिशें।"),
            ("🐛", "कीट और रोग नियंत्रण", "प्रारंभिक चेतावनी प्रणाली और उपचार सिफारिशें।"),
            ("📈", "उपज भविष्यवाणी", "राजस्व अनुमान के साथ ML-आधारित उपज अनुमान।"),
        ],
        "tech_title": "तकनीकी स्टैक",
        "tech_desc": """
फसलसारथी सटीक सिफारिशें देने के लिए अत्याधुनिक तकनीकों का उपयोग करता है:

- **मशीन लर्निंग** – भारतीय कृषि डेटा पर प्रशिक्षित मॉडल
- **वास्तविक समय मौसम** – मौसम विज्ञान सेवाओं के साथ एकीकरण
- **बाजार डेटा** – APMC मंडी कीमतें और मांग विश्लेषण
- **Streamlit** – आधुनिक, उत्तरदायी वेब इंटरफेस
- **Python Backend** – मजबूत डेटा प्रोसेसिंग
        """,
        "crops_title": "समर्थित फसलें (22+)",
        "crops_desc": "हमारा मॉडल भारत भर में उगाई जाने वाली विभिन्न फसलों के लिए सिफारिशों का समर्थन करता है:",
        "crops_list": [
            "🌾 अनाज: चावल, गेहूं, मक्का",
            "🫘 दालें: चना, मसूर, उड़द, मूंग, अरहर, राजमा, मोठ",
            "🥭 फल: आम, केला, सेब, संतरा, अंगूर, पपीता, अनार, तरबूज, खरबूजा",
            "☕ नकदी फसलें: कपास, जूट, कॉफी, नारियल",
        ],
        "mission_title": "हमारा मिशन",
        "mission_desc": """
**"टिकाऊ और लाभदायक कृषि के लिए हर किसान को AI-संचालित अंतर्दृष्टि के साथ सशक्त बनाना।"**

हमारा मानना है कि तकनीक सभी किसानों के लिए सुलभ होनी चाहिए।
फसलसारथी ज्ञान की खाई को पाटने और किसानों की मदद करने का लक्ष्य रखता है:

✅ डेटा-संचालित निर्णयों से फसल विफलताओं को कम करें  
✅ इष्टतम इनपुट प्रबंधन से उपज अधिकतम करें  
✅ बाजार गतिशीलता को समझकर लाभप्रदता बढ़ाएं  
✅ टिकाऊ खेती प्रथाओं को अपनाएं  
✅ अपनी पसंदीदा भाषा में कृषि ज्ञान प्राप्त करें
        """,
        "team_title": "टीम के बारे में",
        "team_desc": """
फसलसारथी को भारतीय किसानों का समर्थन करने के लिए एक कृषि प्रौद्योगिकी पहल के हिस्से के रूप में विकसित किया गया था।
हमारी टीम वास्तविक खेती चुनौतियों के लिए व्यावहारिक समाधान बनाने के लिए मशीन लर्निंग, कृषि विज्ञान और सॉफ्टवेयर विकास में विशेषज्ञता को जोड़ती है।
        """,
        "contact_title": "संपर्क करें",
        "contact_desc": "प्रश्न या प्रतिक्रिया है? हमें आपसे सुनना अच्छा लगेगा!",
        "language": "भाषा",
    },
}


def get_text(key: str) -> str:
    """Get translated text based on current language."""
    lang = st.session_state.get("language", "en")
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)


def get_theme_colors():
    """Get theme-aware color palette - Professional design."""
    theme = st.session_state.get("theme", "light")
    if theme == "dark":
        # Professional dark theme - Modern blue-gray palette
        return {
            "title_color": "#64ffda",
            "tagline_color": "#80cbc4",
            "text_color": "#e8e8e8",
            "muted_color": "#b0bec5",
            "card_bg": "linear-gradient(135deg, #1e2a4a 0%, #2d3a5a 100%)",
            "white_card": "#1e2a4a",
            "card_border": "#3a506b",
            "feature_card_bg": "#1e2a4a",
        }
    else:
        # Professional light theme - Clean green palette
        return {
            "title_color": "#1b5e20",
            "tagline_color": "#4caf50",
            "text_color": "#333",
            "muted_color": "#666",
            "card_bg": "linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%)",
            "white_card": "#ffffff",
            "card_border": "#e0e0e0",
            "feature_card_bg": "#ffffff",
        }


def apply_theme():
    """Apply the selected theme (light/dark) to the page."""
    theme = st.session_state.get("theme", "light")

    if theme == "dark":
        bg_style = """
            :root, html, body, .stApp {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
            }
            [data-testid="stAppViewContainer"] { 
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important; 
            }
            [data-testid="stHeader"] { background: transparent !important; }
            .stMarkdown, p, span, label { color: #e8e8e8 !important; }
            h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
        """
    else:
        bg_style = ""

    st.markdown(f"<style>{bg_style}</style>", unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="About – FasalSaarthi",
        page_icon="🌾",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Initialize theme in session state
    if "theme" not in st.session_state:
        st.session_state["theme"] = "light"

    inject_theme()
    apply_theme()

    colors = get_theme_colors()

    # Theme toggle and Language selector
    col_spacer, col_theme, col_lang = st.columns([5, 1, 1])

    with col_theme:
        current_theme = st.session_state.get("theme", "light")
        is_dark = current_theme == "dark"

        # Use toggle for theme
        dark_mode = st.toggle(
            "🌙", value=is_dark, key="dark_mode_toggle", label_visibility="collapsed"
        )

        if dark_mode and current_theme != "dark":
            st.session_state["theme"] = "dark"
            st.rerun()
        elif not dark_mode and current_theme != "light":
            st.session_state["theme"] = "light"
            st.rerun()

    with col_lang:
        st.selectbox(
            get_text("language"),
            options=["en", "hi"],
            format_func=lambda x: "English" if x == "en" else "हिंदी",
            key="language",
            label_visibility="collapsed",
        )

    # Hero Section
    st.markdown(
        f"""
        <div style="text-align: center; padding: 2rem 0;">
            <div style="font-family: 'Poppins', sans-serif; font-size: 3rem; font-weight: 700; color: {colors["title_color"]};">
                {get_text("hero_title")}
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 1.2rem; color: {colors["tagline_color"]}; 
                        text-transform: uppercase; letter-spacing: 3px; margin: 0.5rem 0;">
                {get_text("hero_subtitle")}
            </div>
            <p style="color: {colors["muted_color"]}; max-width: 700px; margin: 1rem auto; font-size: 1.1rem;">
                {get_text("hero_desc")}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # What is FasalSaarthi
    st.markdown(
        f"""
        <div style="background: {colors["card_bg"]}; 
                    border-radius: 16px; padding: 2rem; margin: 1rem 0;">
            <h2 style="color: {colors["title_color"]}; margin-bottom: 1rem;">🌱 {get_text("what_is")}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(get_text("what_is_desc"))

    st.markdown("---")

    # Features
    st.subheader(f"⭐ {get_text('features_title')}")

    features = get_text("features")
    cols = st.columns(3)
    theme = st.session_state.get("theme", "light")
    shadow_style = (
        "0 4px 20px rgba(0,0,0,0.3)"
        if theme == "dark"
        else "0 4px 15px rgba(0,0,0,0.08)"
    )

    for idx, (icon, title, desc) in enumerate(features):
        with cols[idx % 3]:
            st.markdown(
                f"""
                <div style="background: {colors["feature_card_bg"]}; border-radius: 12px; padding: 1.5rem; 
                            box-shadow: {shadow_style}; margin-bottom: 1rem;
                            border: 1px solid {colors["card_border"]}; min-height: 180px;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                    <div style="font-weight: 600; color: {colors["title_color"]}; margin-bottom: 0.5rem; font-size: 1.1rem;">
                        {title}
                    </div>
                    <div style="color: {colors["muted_color"]}; font-size: 0.95rem; line-height: 1.5;">
                        {desc}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # Supported Crops
    st.subheader(f"🌾 {get_text('crops_title')}")
    st.write(get_text("crops_desc"))

    crops_list = get_text("crops_list")
    cols = st.columns(2)
    for idx, crop_group in enumerate(crops_list):
        with cols[idx % 2]:
            st.markdown(
                f"""
                <div style="background: {colors["feature_card_bg"]}; border-radius: 8px; padding: 1rem; margin: 0.5rem 0;
                            border-left: 4px solid {colors["tagline_color"]}; color: {colors["text_color"]};">
                    {crop_group}
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # Technology Stack
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"🔧 {get_text('tech_title')}")
        st.markdown(get_text("tech_desc"))

    with col2:
        st.subheader(f"🎯 {get_text('mission_title')}")
        st.markdown(get_text("mission_desc"))

    st.markdown("---")

    # Team & Contact
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"👥 {get_text('team_title')}")
        st.markdown(get_text("team_desc"))

    with col2:
        st.subheader(f"📧 {get_text('contact_title')}")
        st.write(get_text("contact_desc"))
        st.markdown(
            f"""
            <div style="background: {colors["card_bg"]}; border-radius: 12px; padding: 1.5rem; margin-top: 1rem;">
                <p style="margin: 0.5rem 0; color: {colors["text_color"]};">📧 Email: support@fasalsaarthi.in</p>
                <p style="margin: 0.5rem 0; color: {colors["text_color"]};">🌐 Website: www.fasalsaarthi.in</p>
                <p style="margin: 0.5rem 0; color: {colors["text_color"]};">📱 Helpline: 1800-XXX-XXXX (Toll Free)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Footer
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; padding: 1rem; color: {colors["muted_color"]};">
            <p>Made with ❤️ for Indian Farmers | © 2024 FasalSaarthi</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
