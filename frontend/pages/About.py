"""About page for FasalSaarthi."""

from __future__ import annotations

import streamlit as st

from frontend.components.layout import inject_theme


TRANSLATIONS = {
    "en": {
        "page_title": "About FasalSaarthi",
        "hero_title": "🌾 FasalSaarthi",
        "hero_subtitle": "AI-Powered Smart Farming",
        "hero_desc": "Empowering Indian farmers with intelligent crop recommendations, market insights, and sustainable farming practices.",
        "what_is": "What is FasalSaarthi?",
        "what_is_desc": """
FasalSaarthi is an AI-powered agricultural advisory system designed to help Indian farmers make data-driven decisions.
The name combines **Fasal** (crop/harvest) and **Saarthi** (guide/charioteer), representing our mission to guide farmers towards better harvests.

Our platform analyzes soil conditions, weather patterns, and market trends to provide personalized recommendations for:
- **Crop Selection** - Which crops are best suited for your land
- **Fertilizer Planning** - Optimal nutrient management
- **Pest & Disease Management** - Protection strategies
- **Yield Prediction** - Expected output and revenue estimation
- **Market Intelligence** - Current prices and demand trends
        """,
        "features_title": "Key Features",
        "features": [
            ("🌿", "Smart Crop Recommendations", "AI-powered analysis of soil, weather, and market data to suggest the most suitable and profitable crops."),
            ("📊", "Market Intelligence", "Real-time market prices, trends, and demand analysis for 22+ crops across India."),
            ("💧", "Water Management", "Customized irrigation schedules and water requirement calculations."),
            ("🧪", "Fertilizer Planning", "Nutrient-specific recommendations with organic alternatives."),
            ("🐛", "Pest & Disease Control", "Early warning systems and treatment recommendations."),
            ("📈", "Yield Prediction", "ML-based yield estimation with revenue projections."),
        ],
        "tech_title": "Technology Stack",
        "tech_desc": """
- **Machine Learning** - Random Forest and XGBoost-style workflows for agricultural prediction tasks
- **Real-time Weather** - Weather advisory integration
- **Market Data** - Price and demand analysis support
- **Streamlit** - Responsive web app interface
- **Python Backend** - Data processing and model inference services
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

We believe technology should be practical and accessible for every farmer.
FasalSaarthi aims to help farmers:

✅ Reduce crop failures through data-driven decisions  
✅ Maximize yield with optimal input management  
✅ Increase profitability by understanding market dynamics  
✅ Adopt sustainable farming practices  
✅ Access agricultural knowledge in their preferred language
        """,
        "team_title": "About the Team",
        "team_desc": "FasalSaarthi was developed as an agriculture-technology initiative with a focus on practical farmer impact through ML, agronomy knowledge, and software engineering.",
        "contact_title": "Get in Touch",
        "contact_desc": "Have questions or feedback? We would love to hear from you.",
        "language": "Language",
    },
    "hi": {
        "page_title": "फ़सलसारथी के बारे में",
        "hero_title": "🌾 फ़सलसारथी",
        "hero_subtitle": "AI-संचालित स्मार्ट खेती",
        "hero_desc": "भारतीय किसानों को बुद्धिमान फसल सिफारिशों, बाज़ार अंतर्दृष्टि और टिकाऊ खेती प्रथाओं के साथ सशक्त बनाना।",
        "what_is": "फ़सलसारथी क्या है?",
        "what_is_desc": """
फ़सलसारथी एक AI-संचालित कृषि सलाह प्रणाली है, जो भारतीय किसानों को डेटा-आधारित निर्णय लेने में मदद करती है।
इस नाम में **फ़सल** (crop/harvest) और **सारथी** (guide/charioteer) शामिल हैं, जो बेहतर उपज की दिशा में मार्गदर्शन का प्रतीक है।

हमारा प्लेटफ़ॉर्म मिट्टी, मौसम और बाज़ार रुझानों का विश्लेषण करके व्यक्तिगत सिफारिशें देता है:
- **फसल चयन** - आपकी भूमि के लिए उपयुक्त फसलें
- **उर्वरक योजना** - पोषक तत्वों का बेहतर प्रबंधन
- **कीट एवं रोग प्रबंधन** - सुरक्षा रणनीतियाँ
- **उपज पूर्वानुमान** - उत्पादन और आय का अनुमान
- **बाज़ार जानकारी** - कीमत और मांग की दिशा
        """,
        "features_title": "मुख्य विशेषताएँ",
        "features": [
            ("🌿", "स्मार्ट फसल सिफारिश", "मिट्टी, मौसम और बाज़ार डेटा के AI विश्लेषण से उपयुक्त और लाभदायक फसल सुझाव।"),
            ("📊", "बाज़ार इंटेलिजेंस", "भारत में 22+ फसलों के लिए रियल-टाइम कीमत, रुझान और मांग विश्लेषण।"),
            ("💧", "जल प्रबंधन", "अनुकूलित सिंचाई योजना और पानी की आवश्यकता का आकलन।"),
            ("🧪", "उर्वरक योजना", "पोषक तत्व-विशिष्ट सुझाव और जैविक विकल्प।"),
            ("🐛", "कीट एवं रोग नियंत्रण", "प्रारंभिक चेतावनी और उपचार सिफारिशें।"),
            ("📈", "उपज पूर्वानुमान", "ML-आधारित उपज और राजस्व अनुमान।"),
        ],
        "tech_title": "प्रौद्योगिकी स्टैक",
        "tech_desc": """
- **मशीन लर्निंग** - कृषि भविष्यवाणी कार्यों के लिए प्रशिक्षित मॉडल
- **रियल-टाइम मौसम** - मौसम सलाह एकीकरण
- **बाज़ार डेटा** - कीमत और मांग विश्लेषण
- **Streamlit** - उत्तरदायी वेब इंटरफ़ेस
- **Python बैकएंड** - डेटा प्रोसेसिंग और मॉडल इन्फरेंस
        """,
        "crops_title": "समर्थित फसलें (22+)",
        "crops_desc": "हमारा मॉडल भारत में उगाई जाने वाली विभिन्न फसलों के लिए सिफारिशें देता है:",
        "crops_list": [
            "🌾 अनाज: Rice, Wheat, Maize",
            "🫘 दालें: Chickpea, Lentil, Black Gram, Mung Bean, Pigeon Peas, Kidney Beans, Moth Beans",
            "🥭 फल: Mango, Banana, Apple, Orange, Grapes, Papaya, Pomegranate, Watermelon, Muskmelon",
            "☕ नकदी फसलें: Cotton, Jute, Coffee, Coconut",
        ],
        "mission_title": "हमारा मिशन",
        "mission_desc": """
**"सतत और लाभदायक कृषि के लिए हर किसान को AI-संचालित अंतर्दृष्टि से सशक्त बनाना।"**

✅ डेटा-आधारित निर्णयों से फसल विफलता कम करना  
✅ बेहतर इनपुट प्रबंधन से उपज बढ़ाना  
✅ बाज़ार गतिशीलता समझकर लाभ बढ़ाना  
✅ टिकाऊ खेती पद्धतियों को बढ़ावा देना  
✅ पसंदीदा भाषा में कृषि ज्ञान उपलब्ध कराना
        """,
        "team_title": "टीम के बारे में",
        "team_desc": "फ़सलसारथी को व्यावहारिक खेती चुनौतियों के समाधान के लिए मशीन लर्निंग, कृषि विज्ञान और सॉफ़्टवेयर विकास विशेषज्ञता के साथ बनाया गया है।",
        "contact_title": "संपर्क करें",
        "contact_desc": "कोई प्रश्न या सुझाव है? हम आपकी प्रतिक्रिया का स्वागत करते हैं।",
        "language": "भाषा",
    },
    "te": {
        "page_title": "ఫసల్సార్థి గురించి",
        "hero_title": "🌾 ఫసల్సార్థి",
        "hero_subtitle": "AI ఆధారిత స్మార్ట్ సాగు",
        "hero_desc": "భారత రైతులకు తెలివైన పంట సిఫార్సులు, మార్కెట్ అవగాహన మరియు స్థిరమైన సాగు పద్ధతులతో సహాయం చేయడం.",
        "what_is": "ఫసల్సార్థి అంటే ఏమిటి?",
        "what_is_desc": """
ఫసల్సార్థి ఒక AI ఆధారిత వ్యవసాయ సలహా వ్యవస్థ. ఇది భారత రైతులు డేటా ఆధారంగా నిర్ణయాలు తీసుకోవడానికి సహాయపడుతుంది.
**ఫసల్** (crop/harvest) మరియు **సారథి** (guide/charioteer) అనే భావాల కలయికతో ఈ పేరును రూపొందించారు.

మా ప్లాట్‌ఫారమ్ నేల స్థితి, వాతావరణ ధోరణులు మరియు మార్కెట్ మార్పులను విశ్లేషించి వ్యక్తిగత సిఫార్సులు అందిస్తుంది:
- **పంట ఎంపిక** - మీ భూమికి సరైన పంటలు
- **ఎరువు ప్రణాళిక** - పోషక నిర్వహణ
- **పురుగు & వ్యాధి నిర్వహణ** - రక్షణ వ్యూహాలు
- **దిగుబడి అంచనా** - ఉత్పత్తి మరియు ఆదాయం అంచనా
- **మార్కెట్ సమాచారం** - ధరలు మరియు డిమాండ్ ధోరణులు
        """,
        "features_title": "ముఖ్య లక్షణాలు",
        "features": [
            ("🌿", "స్మార్ట్ పంట సిఫార్సులు", "నేల, వాతావరణం, మార్కెట్ డేటాపై AI విశ్లేషణతో అనుకూలమైన మరియు లాభదాయకమైన పంటల సూచనలు."),
            ("📊", "మార్కెట్ ఇంటెలిజెన్స్", "భారతదేశంలో 22+ పంటల కోసం రియల్-టైమ్ ధరలు, ధోరణులు, డిమాండ్ విశ్లేషణ."),
            ("💧", "నీటి నిర్వహణ", "అనుకూలీకరించిన పారుదల షెడ్యూల్ మరియు నీటి అవసరాల అంచనా."),
            ("🧪", "ఎరువు ప్రణాళిక", "పోషక-నిర్దిష్ట సిఫార్సులు మరియు సేంద్రియ ప్రత్యామ్నాయాలు."),
            ("🐛", "పురుగు & వ్యాధి నియంత్రణ", "ముందస్తు హెచ్చరికలు మరియు చికిత్స సూచనలు."),
            ("📈", "దిగుబడి అంచనా", "ML ఆధారిత దిగుబడి మరియు ఆదాయం అంచనా."),
        ],
        "tech_title": "సాంకేతిక స్టాక్",
        "tech_desc": """
- **Machine Learning** - వ్యవసాయ అంచనా పనుల కోసం శిక్షణ పొందిన మోడళ్లు
- **Real-time Weather** - వాతావరణ సలహా ఇంటిగ్రేషన్
- **Market Data** - ధర మరియు డిమాండ్ విశ్లేషణ
- **Streamlit** - రెస్పాన్సివ్ వెబ్ ఇంటర్‌ఫేస్
- **Python Backend** - డేటా ప్రాసెసింగ్ మరియు మోడల్ ఇన్ఫరెన్స్
        """,
        "crops_title": "మద్దతు ఉన్న పంటలు (22+)",
        "crops_desc": "భారతదేశంలో పండే వివిధ పంటల కోసం మా మోడల్ సిఫార్సులు అందిస్తుంది:",
        "crops_list": [
            "🌾 ధాన్యాలు: Rice, Wheat, Maize",
            "🫘 పప్పుధాన్యాలు: Chickpea, Lentil, Black Gram, Mung Bean, Pigeon Peas, Kidney Beans, Moth Beans",
            "🥭 పండ్లు: Mango, Banana, Apple, Orange, Grapes, Papaya, Pomegranate, Watermelon, Muskmelon",
            "☕ నగదు పంటలు: Cotton, Jute, Coffee, Coconut",
        ],
        "mission_title": "మా లక్ష్యం",
        "mission_desc": """
**"స్థిరమైన మరియు లాభదాయక వ్యవసాయం కోసం ప్రతి రైతును AI ఆధారిత అవగాహనతో శక్తివంతం చేయడం."**

✅ డేటా ఆధారిత నిర్ణయాలతో పంట నష్టాలు తగ్గించడం  
✅ సరైన ఇన్‌పుట్ నిర్వహణతో దిగుబడి పెంచడం  
✅ మార్కెట్ ధోరణులు అర్థం చేసుకొని లాభదాయకత పెంచడం  
✅ స్థిరమైన సాగు పద్ధతులను ప్రోత్సహించడం  
✅ రైతుల ఎంపిక చేసిన భాషలో వ్యవసాయ జ్ఞానం అందించడం
        """,
        "team_title": "మా బృందం గురించి",
        "team_desc": "ఫసల్సార్థి ప్రాజెక్ట్‌ను వ్యవసాయ శాస్త్రం, మెషిన్ లెర్నింగ్, సాఫ్ట్‌వేర్ అభివృద్ధి పరిజ్ఞానం కలిగిన బృందం రైతుల కోసం రూపొందించింది.",
        "contact_title": "సంప్రదించండి",
        "contact_desc": "ప్రశ్నలు లేదా అభిప్రాయాలు ఉంటే మాతో సంప్రదించండి.",
        "language": "భాష",
    },
}


def normalize_language(value: str | None) -> str:
    mapping = {
        "en": "en",
        "english": "en",
        "hi": "hi",
        "hindi": "hi",
        "हिंदी": "hi",
        "te": "te",
        "telugu": "te",
        "తెలుగు": "te",
    }
    return mapping.get(str(value or "").strip().lower(), "en")


def language_label(code: str) -> str:
    return {"en": "English", "hi": "हिंदी", "te": "తెలుగు"}.get(code, code)


def get_text(key: str):
    lang = normalize_language(st.session_state.get("language", "en"))
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, TRANSLATIONS["en"].get(key, key))


def render_language_selector(selector_key: str, label: str) -> None:
    options = ["en", "hi", "te"]
    widget_key = "language_code"
    current = normalize_language(st.session_state.get("language", "en"))
    if widget_key in st.session_state:
        current = normalize_language(st.session_state[widget_key])
        st.session_state["language"] = current
    else:
        st.session_state[widget_key] = current

    selected = st.selectbox(
        label,
        options=options,
        key=widget_key,
        format_func=language_label,
        label_visibility="collapsed",
    )
    st.session_state["language"] = normalize_language(selected)


def get_theme_colors() -> dict[str, str]:
    if st.session_state.get("theme", "light") == "dark":
        return {
            "title_color": "#64ffda",
            "tagline_color": "#80cbc4",
            "text_color": "#e8e8e8",
            "muted_color": "#b0bec5",
            "card_bg": "linear-gradient(135deg, #1e2a4a 0%, #2d3a5a 100%)",
            "card_bg_soft": "linear-gradient(135deg, #0f172a 0%, #1f2937 100%)",
            "card_border": "#334155",
            "crop_card_bg": "#f8fafc",
            "crop_card_text": "#0f172a",
        }
    return {
        "title_color": "#1b5e20",
        "tagline_color": "#4caf50",
        "text_color": "#1f2937",
        "muted_color": "#4b5563",
        "card_bg": "linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%)",
        "card_bg_soft": "linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)",
        "card_border": "#e5e7eb",
        "crop_card_bg": "#f8fafc",
        "crop_card_text": "#0f172a",
    }


def apply_theme() -> None:
    if st.session_state.get("theme", "light") == "dark":
        st.markdown(
            """
            <style>
                :root, html, body, .stApp {
                    background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #0b1220 100%) !important;
                }
                [data-testid="stAppViewContainer"] {
                    background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #0b1220 100%) !important;
                }
                [data-testid="stHeader"] { background: transparent !important; }
                .stMarkdown, p, span, label { color: #e5e7eb !important; }
                h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )


def main() -> None:
    if "theme" not in st.session_state:
        st.session_state["theme"] = "light"
    st.session_state["language"] = normalize_language(st.session_state.get("language", "en"))

    inject_theme()
    apply_theme()
    colors = get_theme_colors()

    _, col_theme, col_lang = st.columns([5, 1, 1])
    with col_theme:
        dark_mode = st.toggle(
            "Theme",
            value=st.session_state.get("theme") == "dark",
            key="about_dark_mode_toggle",
            label_visibility="collapsed",
        )
        next_theme = "dark" if dark_mode else "light"
        if next_theme != st.session_state.get("theme"):
            st.session_state["theme"] = next_theme
            st.rerun()

    with col_lang:
        render_language_selector("about_language_selector", get_text("language"))

    st.markdown(
        f"""
        <div style="text-align:center; padding:2rem 0;">
            <div style="font-size:3rem; font-weight:800; color:{colors["title_color"]};">
                {get_text("hero_title")}
            </div>
            <div style="font-size:1.2rem; font-weight:700; letter-spacing:3px; color:{colors["tagline_color"]}; text-transform:uppercase; margin-top:.3rem;">
                {get_text("hero_subtitle")}
            </div>
            <p style="max-width:760px; margin:.8rem auto 0; font-size:1.05rem; color:{colors["muted_color"]};">
                {get_text("hero_desc")}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown(
        f"""
        <div style="background:{colors["card_bg"]}; border:1px solid {colors["card_border"]}; border-radius:14px; padding:1.4rem 1.6rem;">
            <h2 style="margin:0; color:{colors["title_color"]};">{get_text("what_is")}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(get_text("what_is_desc"))

    st.markdown("---")
    st.subheader(get_text("features_title"))

    features = get_text("features")
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div style="background:{colors["card_bg_soft"]}; border:1px solid {colors["card_border"]}; border-radius:12px; padding:1rem; margin-bottom:1rem; min-height:170px;">
                    <div style="font-size:1.9rem;">{icon}</div>
                    <div style="font-size:1.05rem; font-weight:700; color:{colors["title_color"]}; margin:.35rem 0;">{title}</div>
                    <div style="font-size:.94rem; color:{colors["muted_color"]}; line-height:1.45;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.subheader(get_text("crops_title"))
    st.write(get_text("crops_desc"))
    crop_cols = st.columns(2)
    for i, item in enumerate(get_text("crops_list")):
        with crop_cols[i % 2]:
            st.markdown(
                f"""
                <div style="background:{colors["crop_card_bg"]}; color:{colors["crop_card_text"]}; border:1px solid {colors["card_border"]}; border-left:4px solid {colors["tagline_color"]}; border-radius:10px; padding:.9rem; margin:.45rem 0; font-weight:600;">
                    {item}
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    col_tech, col_mission = st.columns(2)
    with col_tech:
        st.subheader(get_text("tech_title"))
        st.markdown(get_text("tech_desc"))
    with col_mission:
        st.subheader(get_text("mission_title"))
        st.markdown(get_text("mission_desc"))

    st.markdown("---")
    col_team, col_contact = st.columns(2)
    with col_team:
        st.subheader(get_text("team_title"))
        st.markdown(get_text("team_desc"))
    with col_contact:
        st.subheader(get_text("contact_title"))
        st.write(get_text("contact_desc"))
        st.markdown(
            f"""
            <div style="background:{colors["card_bg"]}; border:1px solid {colors["card_border"]}; border-radius:12px; padding:1rem; margin-top:.6rem;">
                <p style="margin:.35rem 0; color:{colors["text_color"]};">📧 Email: support@fasalsaarthi.in</p>
                <p style="margin:.35rem 0; color:{colors["text_color"]};">🌐 Website: www.fasalsaarthi.in</p>
                <p style="margin:.35rem 0; color:{colors["text_color"]};">📞 Helpline: 1800-XXX-XXXX (Toll Free)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
