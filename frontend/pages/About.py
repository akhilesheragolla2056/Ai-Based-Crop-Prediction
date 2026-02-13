"""About Page for FasalSaarthi â€“ AI Crop Recommendation System."""

import streamlit as st

from frontend.components.layout import inject_theme


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TRANSLATIONS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
TRANSLATIONS = {
    "en": {
        "page_title": "About FasalSaarthi",
        "hero_title": "ðŸŒ¾ FasalSaarthi",
        "hero_subtitle": "AI-Powered Smart Farming",
        "hero_desc": "Empowering Indian farmers with intelligent crop recommendations, market insights, and sustainable farming practices.",
        "what_is": "What is FasalSaarthi?",
        "what_is_desc": """
FasalSaarthi (à¤«à¤¸à¤²à¤¸à¤¾à¤°à¤¥à¥€) is an AI-powered agricultural advisory system designed to help Indian farmers make data-driven decisions. 
The name combines 'Fasal' (crop/harvest) and 'Saarthi' (guide/charioteer), representing our mission to guide farmers towards better harvests.

Our platform analyzes soil conditions, weather patterns, and market trends to provide personalized recommendations for:
- **Crop Selection** â€“ Which crops are best suited for your land
- **Fertilizer Planning** â€“ Optimal nutrient management
- **Pest & Disease Management** â€“ Protection strategies
- **Yield Prediction** â€“ Expected output and revenue estimation
- **Market Intelligence** â€“ Current prices and demand trends
        """,
        "features_title": "Key Features",
        "features": [
            (
                "ðŸŒ¿",
                "Smart Crop Recommendations",
                "AI-powered analysis of soil, weather, and market data to suggest the most suitable and profitable crops.",
            ),
            (
                "ðŸ“Š",
                "Market Intelligence",
                "Real-time market prices, trends, and demand analysis for 22+ crops across India.",
            ),
            (
                "ðŸ’§",
                "Water Management",
                "Customized irrigation schedules and water requirement calculations.",
            ),
            (
                "ðŸ§ª",
                "Fertilizer Planning",
                "Nutrient-specific recommendations with organic alternatives.",
            ),
            (
                "ðŸ›",
                "Pest & Disease Control",
                "Early warning systems and treatment recommendations.",
            ),
            (
                "ðŸ“ˆ",
                "Yield Prediction",
                "ML-based yield estimation with revenue projections.",
            ),
        ],
        "tech_title": "Technology Stack",
        "tech_desc": """
FasalSaarthi leverages cutting-edge technologies to deliver accurate recommendations:

- **Machine Learning** â€“ Random Forest & XGBoost models trained on Indian agricultural data
- **Real-time Weather** â€“ Integration with meteorological services for accurate weather insights
- **Market Data** â€“ APMC mandi prices and demand analysis
- **Streamlit** â€“ Modern, responsive web interface
- **Python Backend** â€“ Robust data processing and model inference
        """,
        "crops_title": "Supported Crops (22+)",
        "crops_desc": "Our model supports recommendations for a wide variety of crops grown across India:",
        "crops_list": [
            "ðŸŒ¾ Cereals: Rice, Wheat, Maize",
            "ðŸ«˜ Pulses: Chickpea, Lentil, Black Gram, Mung Bean, Pigeon Peas, Kidney Beans, Moth Beans",
            "ðŸ¥­ Fruits: Mango, Banana, Apple, Orange, Grapes, Papaya, Pomegranate, Watermelon, Muskmelon",
            "â˜• Cash Crops: Cotton, Jute, Coffee, Coconut",
        ],
        "mission_title": "Our Mission",
        "mission_desc": """
**"Empowering every farmer with AI-driven insights for sustainable and profitable agriculture."**

We believe that technology should be accessible to all farmers, regardless of their farm size or technical expertise. 
FasalSaarthi aims to bridge the knowledge gap and help farmers:

âœ… Reduce crop failures through data-driven decisions  
âœ… Maximize yield with optimal input management  
âœ… Increase profitability by understanding market dynamics  
âœ… Adopt sustainable farming practices  
âœ… Access agricultural knowledge in their preferred language
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
        "page_title": "à¤«à¤¸à¤²à¤¸à¤¾à¤°à¤¥à¥€ à¤•à¥‡ à¤¬à¤¾à¤°à¥‡ à¤®à¥‡à¤‚",
        "hero_title": "ðŸŒ¾ à¤«à¤¸à¤²à¤¸à¤¾à¤°à¤¥à¥€",
        "hero_subtitle": "AI-à¤¸à¤‚à¤šà¤¾à¤²à¤¿à¤¤ à¤¸à¥à¤®à¤¾à¤°à¥à¤Ÿ à¤–à¥‡à¤¤à¥€",
        "hero_desc": "à¤­à¤¾à¤°à¤¤à¥€à¤¯ à¤•à¤¿à¤¸à¤¾à¤¨à¥‹à¤‚ à¤•à¥‹ à¤¬à¥à¤¦à¥à¤§à¤¿à¤®à¤¾à¤¨ à¤«à¤¸à¤² à¤¸à¤¿à¤«à¤¾à¤°à¤¿à¤¶à¥‹à¤‚, à¤¬à¤¾à¤œà¤¾à¤° à¤…à¤‚à¤¤à¤°à¥à¤¦à¥ƒà¤·à¥à¤Ÿà¤¿ à¤”à¤° à¤Ÿà¤¿à¤•à¤¾à¤Š à¤–à¥‡à¤¤à¥€ à¤ªà¥à¤°à¤¥à¤¾à¤“à¤‚ à¤•à¥‡ à¤¸à¤¾à¤¥ à¤¸à¤¶à¤•à¥à¤¤ à¤¬à¤¨à¤¾à¤¨à¤¾à¥¤",
        "what_is": "à¤«à¤¸à¤²à¤¸à¤¾à¤°à¤¥à¥€ à¤•à¥à¤¯à¤¾ à¤¹à¥ˆ?",
        "what_is_desc": """
à¤«à¤¸à¤²à¤¸à¤¾à¤°à¤¥à¥€ à¤à¤• AI-à¤¸à¤‚à¤šà¤¾à¤²à¤¿à¤¤ à¤•à¥ƒà¤·à¤¿ à¤¸à¤²à¤¾à¤¹à¤•à¤¾à¤° à¤ªà¥à¤°à¤£à¤¾à¤²à¥€ à¤¹à¥ˆ à¤œà¥‹ à¤­à¤¾à¤°à¤¤à¥€à¤¯ à¤•à¤¿à¤¸à¤¾à¤¨à¥‹à¤‚ à¤•à¥‹ à¤¡à¥‡à¤Ÿà¤¾-à¤¸à¤‚à¤šà¤¾à¤²à¤¿à¤¤ à¤¨à¤¿à¤°à¥à¤£à¤¯ à¤²à¥‡à¤¨à¥‡ à¤®à¥‡à¤‚ à¤®à¤¦à¤¦ à¤•à¤°à¤¤à¥€ à¤¹à¥ˆà¥¤
'à¤«à¤¸à¤²' (harvest) à¤”à¤° 'à¤¸à¤¾à¤°à¤¥à¥€' (guide) à¤•à¤¾ à¤¸à¤‚à¤¯à¥‹à¤œà¤¨ à¤¹à¤®à¤¾à¤°à¥‡ à¤®à¤¿à¤¶à¤¨ à¤•à¥‹ à¤¦à¤°à¥à¤¶à¤¾à¤¤à¤¾ à¤¹à¥ˆ - à¤•à¤¿à¤¸à¤¾à¤¨à¥‹à¤‚ à¤•à¥‹ à¤¬à¥‡à¤¹à¤¤à¤° à¤«à¤¸à¤² à¤•à¥€ à¤“à¤° à¤®à¤¾à¤°à¥à¤—à¤¦à¤°à¥à¤¶à¤¨ à¤•à¤°à¤¨à¤¾à¥¤

à¤¹à¤®à¤¾à¤°à¤¾ à¤ªà¥à¤²à¥‡à¤Ÿà¤«à¥‰à¤°à¥à¤® à¤®à¤¿à¤Ÿà¥à¤Ÿà¥€ à¤•à¥€ à¤¸à¥à¤¥à¤¿à¤¤à¤¿, à¤®à¥Œà¤¸à¤® à¤ªà¥ˆà¤Ÿà¤°à¥à¤¨ à¤”à¤° à¤¬à¤¾à¤œà¤¾à¤° à¤°à¥à¤à¤¾à¤¨à¥‹à¤‚ à¤•à¤¾ à¤µà¤¿à¤¶à¥à¤²à¥‡à¤·à¤£ à¤•à¤°à¤•à¥‡ à¤µà¥à¤¯à¤•à¥à¤¤à¤¿à¤—à¤¤ à¤¸à¤¿à¤«à¤¾à¤°à¤¿à¤¶à¥‡à¤‚ à¤ªà¥à¤°à¤¦à¤¾à¤¨ à¤•à¤°à¤¤à¤¾ à¤¹à¥ˆ:
- **à¤«à¤¸à¤² à¤šà¤¯à¤¨** â€“ à¤†à¤ªà¤•à¥€ à¤­à¥‚à¤®à¤¿ à¤•à¥‡ à¤²à¤¿à¤ à¤•à¥Œà¤¨ à¤¸à¥€ à¤«à¤¸à¤²à¥‡à¤‚ à¤¸à¤°à¥à¤µà¥‹à¤¤à¥à¤¤à¤® à¤¹à¥ˆà¤‚
- **à¤‰à¤°à¥à¤µà¤°à¤• à¤¯à¥‹à¤œà¤¨à¤¾** â€“ à¤‡à¤·à¥à¤Ÿà¤¤à¤® à¤ªà¥‹à¤·à¤• à¤¤à¤¤à¥à¤µ à¤ªà¥à¤°à¤¬à¤‚à¤§à¤¨
- **à¤•à¥€à¤Ÿ à¤”à¤° à¤°à¥‹à¤— à¤ªà¥à¤°à¤¬à¤‚à¤§à¤¨** â€“ à¤¸à¥à¤°à¤•à¥à¤·à¤¾ à¤°à¤£à¤¨à¥€à¤¤à¤¿à¤¯à¤¾à¤‚
- **à¤‰à¤ªà¤œ à¤­à¤µà¤¿à¤·à¥à¤¯à¤µà¤¾à¤£à¥€** â€“ à¤…à¤ªà¥‡à¤•à¥à¤·à¤¿à¤¤ à¤‰à¤¤à¥à¤ªà¤¾à¤¦à¤¨ à¤”à¤° à¤°à¤¾à¤œà¤¸à¥à¤µ à¤…à¤¨à¥à¤®à¤¾à¤¨
- **à¤¬à¤¾à¤œà¤¾à¤° à¤œà¤¾à¤¨à¤•à¤¾à¤°à¥€** â€“ à¤µà¤°à¥à¤¤à¤®à¤¾à¤¨ à¤•à¥€à¤®à¤¤à¥‡à¤‚ à¤”à¤° à¤®à¤¾à¤‚à¤— à¤°à¥à¤à¤¾à¤¨
        """,
        "features_title": "à¤®à¥à¤–à¥à¤¯ à¤µà¤¿à¤¶à¥‡à¤·à¤¤à¤¾à¤à¤‚",
        "features": [
            (
                "ðŸŒ¿",
                "à¤¸à¥à¤®à¤¾à¤°à¥à¤Ÿ à¤«à¤¸à¤² à¤¸à¤¿à¤«à¤¾à¤°à¤¿à¤¶à¥‡à¤‚",
                "à¤®à¤¿à¤Ÿà¥à¤Ÿà¥€, à¤®à¥Œà¤¸à¤® à¤”à¤° à¤¬à¤¾à¤œà¤¾à¤° à¤¡à¥‡à¤Ÿà¤¾ à¤•à¤¾ AI-à¤¸à¤‚à¤šà¤¾à¤²à¤¿à¤¤ à¤µà¤¿à¤¶à¥à¤²à¥‡à¤·à¤£à¥¤",
            ),
            ("ðŸ“Š", "à¤¬à¤¾à¤œà¤¾à¤° à¤œà¤¾à¤¨à¤•à¤¾à¤°à¥€", "22+ à¤«à¤¸à¤²à¥‹à¤‚ à¤•à¥‡ à¤²à¤¿à¤ à¤µà¤¾à¤¸à¥à¤¤à¤µà¤¿à¤• à¤¸à¤®à¤¯ à¤¬à¤¾à¤œà¤¾à¤° à¤®à¥‚à¤²à¥à¤¯ à¤”à¤° à¤°à¥à¤à¤¾à¤¨à¥¤"),
            ("ðŸ’§", "à¤œà¤² à¤ªà¥à¤°à¤¬à¤‚à¤§à¤¨", "à¤•à¤¸à¥à¤Ÿà¤®à¤¾à¤‡à¤œà¤¼à¥à¤¡ à¤¸à¤¿à¤‚à¤šà¤¾à¤ˆ à¤•à¤¾à¤°à¥à¤¯à¤•à¥à¤°à¤® à¤”à¤° à¤ªà¤¾à¤¨à¥€ à¤•à¥€ à¤†à¤µà¤¶à¥à¤¯à¤•à¤¤à¤¾à¥¤"),
            ("ðŸ§ª", "à¤‰à¤°à¥à¤µà¤°à¤• à¤¯à¥‹à¤œà¤¨à¤¾", "à¤œà¥ˆà¤µà¤¿à¤• à¤µà¤¿à¤•à¤²à¥à¤ªà¥‹à¤‚ à¤•à¥‡ à¤¸à¤¾à¤¥ à¤ªà¥‹à¤·à¤• à¤¤à¤¤à¥à¤µ-à¤µà¤¿à¤¶à¤¿à¤·à¥à¤Ÿ à¤¸à¤¿à¤«à¤¾à¤°à¤¿à¤¶à¥‡à¤‚à¥¤"),
            ("ðŸ›", "à¤•à¥€à¤Ÿ à¤”à¤° à¤°à¥‹à¤— à¤¨à¤¿à¤¯à¤‚à¤¤à¥à¤°à¤£", "à¤ªà¥à¤°à¤¾à¤°à¤‚à¤­à¤¿à¤• à¤šà¥‡à¤¤à¤¾à¤µà¤¨à¥€ à¤ªà¥à¤°à¤£à¤¾à¤²à¥€ à¤”à¤° à¤‰à¤ªà¤šà¤¾à¤° à¤¸à¤¿à¤«à¤¾à¤°à¤¿à¤¶à¥‡à¤‚à¥¤"),
            ("ðŸ“ˆ", "à¤‰à¤ªà¤œ à¤­à¤µà¤¿à¤·à¥à¤¯à¤µà¤¾à¤£à¥€", "à¤°à¤¾à¤œà¤¸à¥à¤µ à¤…à¤¨à¥à¤®à¤¾à¤¨ à¤•à¥‡ à¤¸à¤¾à¤¥ ML-à¤†à¤§à¤¾à¤°à¤¿à¤¤ à¤‰à¤ªà¤œ à¤…à¤¨à¥à¤®à¤¾à¤¨à¥¤"),
        ],
        "tech_title": "à¤¤à¤•à¤¨à¥€à¤•à¥€ à¤¸à¥à¤Ÿà¥ˆà¤•",
        "tech_desc": """
à¤«à¤¸à¤²à¤¸à¤¾à¤°à¤¥à¥€ à¤¸à¤Ÿà¥€à¤• à¤¸à¤¿à¤«à¤¾à¤°à¤¿à¤¶à¥‡à¤‚ à¤¦à¥‡à¤¨à¥‡ à¤•à¥‡ à¤²à¤¿à¤ à¤…à¤¤à¥à¤¯à¤¾à¤§à¥à¤¨à¤¿à¤• à¤¤à¤•à¤¨à¥€à¤•à¥‹à¤‚ à¤•à¤¾ à¤‰à¤ªà¤¯à¥‹à¤— à¤•à¤°à¤¤à¤¾ à¤¹à¥ˆ:

- **à¤®à¤¶à¥€à¤¨ à¤²à¤°à¥à¤¨à¤¿à¤‚à¤—** â€“ à¤­à¤¾à¤°à¤¤à¥€à¤¯ à¤•à¥ƒà¤·à¤¿ à¤¡à¥‡à¤Ÿà¤¾ à¤ªà¤° à¤ªà¥à¤°à¤¶à¤¿à¤•à¥à¤·à¤¿à¤¤ à¤®à¥‰à¤¡à¤²
- **à¤µà¤¾à¤¸à¥à¤¤à¤µà¤¿à¤• à¤¸à¤®à¤¯ à¤®à¥Œà¤¸à¤®** â€“ à¤®à¥Œà¤¸à¤® à¤µà¤¿à¤œà¥à¤žà¤¾à¤¨ à¤¸à¥‡à¤µà¤¾à¤“à¤‚ à¤•à¥‡ à¤¸à¤¾à¤¥ à¤à¤•à¥€à¤•à¤°à¤£
- **à¤¬à¤¾à¤œà¤¾à¤° à¤¡à¥‡à¤Ÿà¤¾** â€“ APMC à¤®à¤‚à¤¡à¥€ à¤•à¥€à¤®à¤¤à¥‡à¤‚ à¤”à¤° à¤®à¤¾à¤‚à¤— à¤µà¤¿à¤¶à¥à¤²à¥‡à¤·à¤£
- **Streamlit** â€“ à¤†à¤§à¥à¤¨à¤¿à¤•, à¤‰à¤¤à¥à¤¤à¤°à¤¦à¤¾à¤¯à¥€ à¤µà¥‡à¤¬ à¤‡à¤‚à¤Ÿà¤°à¤«à¥‡à¤¸
- **Python Backend** â€“ à¤®à¤œà¤¬à¥‚à¤¤ à¤¡à¥‡à¤Ÿà¤¾ à¤ªà¥à¤°à¥‹à¤¸à¥‡à¤¸à¤¿à¤‚à¤—
        """,
        "crops_title": "à¤¸à¤®à¤°à¥à¤¥à¤¿à¤¤ à¤«à¤¸à¤²à¥‡à¤‚ (22+)",
        "crops_desc": "à¤¹à¤®à¤¾à¤°à¤¾ à¤®à¥‰à¤¡à¤² à¤­à¤¾à¤°à¤¤ à¤­à¤° à¤®à¥‡à¤‚ à¤‰à¤—à¤¾à¤ˆ à¤œà¤¾à¤¨à¥‡ à¤µà¤¾à¤²à¥€ à¤µà¤¿à¤­à¤¿à¤¨à¥à¤¨ à¤«à¤¸à¤²à¥‹à¤‚ à¤•à¥‡ à¤²à¤¿à¤ à¤¸à¤¿à¤«à¤¾à¤°à¤¿à¤¶à¥‹à¤‚ à¤•à¤¾ à¤¸à¤®à¤°à¥à¤¥à¤¨ à¤•à¤°à¤¤à¤¾ à¤¹à¥ˆ:",
        "crops_list": [
            "ðŸŒ¾ à¤…à¤¨à¤¾à¤œ: à¤šà¤¾à¤µà¤², à¤—à¥‡à¤¹à¥‚à¤‚, à¤®à¤•à¥à¤•à¤¾",
            "ðŸ«˜ à¤¦à¤¾à¤²à¥‡à¤‚: à¤šà¤¨à¤¾, à¤®à¤¸à¥‚à¤°, à¤‰à¤¡à¤¼à¤¦, à¤®à¥‚à¤‚à¤—, à¤…à¤°à¤¹à¤°, à¤°à¤¾à¤œà¤®à¤¾, à¤®à¥‹à¤ ",
            "ðŸ¥­ à¤«à¤²: à¤†à¤®, à¤•à¥‡à¤²à¤¾, à¤¸à¥‡à¤¬, à¤¸à¤‚à¤¤à¤°à¤¾, à¤…à¤‚à¤—à¥‚à¤°, à¤ªà¤ªà¥€à¤¤à¤¾, à¤…à¤¨à¤¾à¤°, à¤¤à¤°à¤¬à¥‚à¤œ, à¤–à¤°à¤¬à¥‚à¤œà¤¾",
            "â˜• à¤¨à¤•à¤¦à¥€ à¤«à¤¸à¤²à¥‡à¤‚: à¤•à¤ªà¤¾à¤¸, à¤œà¥‚à¤Ÿ, à¤•à¥‰à¤«à¥€, à¤¨à¤¾à¤°à¤¿à¤¯à¤²",
        ],
        "mission_title": "à¤¹à¤®à¤¾à¤°à¤¾ à¤®à¤¿à¤¶à¤¨",
        "mission_desc": """
**"à¤Ÿà¤¿à¤•à¤¾à¤Š à¤”à¤° à¤²à¤¾à¤­à¤¦à¤¾à¤¯à¤• à¤•à¥ƒà¤·à¤¿ à¤•à¥‡ à¤²à¤¿à¤ à¤¹à¤° à¤•à¤¿à¤¸à¤¾à¤¨ à¤•à¥‹ AI-à¤¸à¤‚à¤šà¤¾à¤²à¤¿à¤¤ à¤…à¤‚à¤¤à¤°à¥à¤¦à¥ƒà¤·à¥à¤Ÿà¤¿ à¤•à¥‡ à¤¸à¤¾à¤¥ à¤¸à¤¶à¤•à¥à¤¤ à¤¬à¤¨à¤¾à¤¨à¤¾à¥¤"**

à¤¹à¤®à¤¾à¤°à¤¾ à¤®à¤¾à¤¨à¤¨à¤¾ à¤¹à¥ˆ à¤•à¤¿ à¤¤à¤•à¤¨à¥€à¤• à¤¸à¤­à¥€ à¤•à¤¿à¤¸à¤¾à¤¨à¥‹à¤‚ à¤•à¥‡ à¤²à¤¿à¤ à¤¸à¥à¤²à¤­ à¤¹à¥‹à¤¨à¥€ à¤šà¤¾à¤¹à¤¿à¤à¥¤
à¤«à¤¸à¤²à¤¸à¤¾à¤°à¤¥à¥€ à¤œà¥à¤žà¤¾à¤¨ à¤•à¥€ à¤–à¤¾à¤ˆ à¤•à¥‹ à¤ªà¤¾à¤Ÿà¤¨à¥‡ à¤”à¤° à¤•à¤¿à¤¸à¤¾à¤¨à¥‹à¤‚ à¤•à¥€ à¤®à¤¦à¤¦ à¤•à¤°à¤¨à¥‡ à¤•à¤¾ à¤²à¤•à¥à¤·à¥à¤¯ à¤°à¤–à¤¤à¤¾ à¤¹à¥ˆ:

âœ… à¤¡à¥‡à¤Ÿà¤¾-à¤¸à¤‚à¤šà¤¾à¤²à¤¿à¤¤ à¤¨à¤¿à¤°à¥à¤£à¤¯à¥‹à¤‚ à¤¸à¥‡ à¤«à¤¸à¤² à¤µà¤¿à¤«à¤²à¤¤à¤¾à¤“à¤‚ à¤•à¥‹ à¤•à¤® à¤•à¤°à¥‡à¤‚  
âœ… à¤‡à¤·à¥à¤Ÿà¤¤à¤® à¤‡à¤¨à¤ªà¥à¤Ÿ à¤ªà¥à¤°à¤¬à¤‚à¤§à¤¨ à¤¸à¥‡ à¤‰à¤ªà¤œ à¤…à¤§à¤¿à¤•à¤¤à¤® à¤•à¤°à¥‡à¤‚  
âœ… à¤¬à¤¾à¤œà¤¾à¤° à¤—à¤¤à¤¿à¤¶à¥€à¤²à¤¤à¤¾ à¤•à¥‹ à¤¸à¤®à¤à¤•à¤° à¤²à¤¾à¤­à¤ªà¥à¤°à¤¦à¤¤à¤¾ à¤¬à¤¢à¤¼à¤¾à¤à¤‚  
âœ… à¤Ÿà¤¿à¤•à¤¾à¤Š à¤–à¥‡à¤¤à¥€ à¤ªà¥à¤°à¤¥à¤¾à¤“à¤‚ à¤•à¥‹ à¤…à¤ªà¤¨à¤¾à¤à¤‚  
âœ… à¤…à¤ªà¤¨à¥€ à¤ªà¤¸à¤‚à¤¦à¥€à¤¦à¤¾ à¤­à¤¾à¤·à¤¾ à¤®à¥‡à¤‚ à¤•à¥ƒà¤·à¤¿ à¤œà¥à¤žà¤¾à¤¨ à¤ªà¥à¤°à¤¾à¤ªà¥à¤¤ à¤•à¤°à¥‡à¤‚
        """,
        "team_title": "à¤Ÿà¥€à¤® à¤•à¥‡ à¤¬à¤¾à¤°à¥‡ à¤®à¥‡à¤‚",
        "team_desc": """
à¤«à¤¸à¤²à¤¸à¤¾à¤°à¤¥à¥€ à¤•à¥‹ à¤­à¤¾à¤°à¤¤à¥€à¤¯ à¤•à¤¿à¤¸à¤¾à¤¨à¥‹à¤‚ à¤•à¤¾ à¤¸à¤®à¤°à¥à¤¥à¤¨ à¤•à¤°à¤¨à¥‡ à¤•à¥‡ à¤²à¤¿à¤ à¤à¤• à¤•à¥ƒà¤·à¤¿ à¤ªà¥à¤°à¥Œà¤¦à¥à¤¯à¥‹à¤—à¤¿à¤•à¥€ à¤ªà¤¹à¤² à¤•à¥‡ à¤¹à¤¿à¤¸à¥à¤¸à¥‡ à¤•à¥‡ à¤°à¥‚à¤ª à¤®à¥‡à¤‚ à¤µà¤¿à¤•à¤¸à¤¿à¤¤ à¤•à¤¿à¤¯à¤¾ à¤—à¤¯à¤¾ à¤¥à¤¾à¥¤
à¤¹à¤®à¤¾à¤°à¥€ à¤Ÿà¥€à¤® à¤µà¤¾à¤¸à¥à¤¤à¤µà¤¿à¤• à¤–à¥‡à¤¤à¥€ à¤šà¥à¤¨à¥Œà¤¤à¤¿à¤¯à¥‹à¤‚ à¤•à¥‡ à¤²à¤¿à¤ à¤µà¥à¤¯à¤¾à¤µà¤¹à¤¾à¤°à¤¿à¤• à¤¸à¤®à¤¾à¤§à¤¾à¤¨ à¤¬à¤¨à¤¾à¤¨à¥‡ à¤•à¥‡ à¤²à¤¿à¤ à¤®à¤¶à¥€à¤¨ à¤²à¤°à¥à¤¨à¤¿à¤‚à¤—, à¤•à¥ƒà¤·à¤¿ à¤µà¤¿à¤œà¥à¤žà¤¾à¤¨ à¤”à¤° à¤¸à¥‰à¤«à¥à¤Ÿà¤µà¥‡à¤¯à¤° à¤µà¤¿à¤•à¤¾à¤¸ à¤®à¥‡à¤‚ à¤µà¤¿à¤¶à¥‡à¤·à¤œà¥à¤žà¤¤à¤¾ à¤•à¥‹ à¤œà¥‹à¤¡à¤¼à¤¤à¥€ à¤¹à¥ˆà¥¤
        """,
        "contact_title": "à¤¸à¤‚à¤ªà¤°à¥à¤• à¤•à¤°à¥‡à¤‚",
        "contact_desc": "à¤ªà¥à¤°à¤¶à¥à¤¨ à¤¯à¤¾ à¤ªà¥à¤°à¤¤à¤¿à¤•à¥à¤°à¤¿à¤¯à¤¾ à¤¹à¥ˆ? à¤¹à¤®à¥‡à¤‚ à¤†à¤ªà¤¸à¥‡ à¤¸à¥à¤¨à¤¨à¤¾ à¤…à¤šà¥à¤›à¤¾ à¤²à¤—à¥‡à¤—à¤¾!",
        "language": "à¤­à¤¾à¤·à¤¾",
    },
    "te": {
        "page_title": "à°«à°¸à°²à±à°¸à°¾à°°à±à°¥à°¿ à°—à±à°°à°¿à°‚à°šà°¿",
        "hero_title": "ðŸŒ¾ à°«à°¸à°²à±à°¸à°¾à°°à±à°¥à°¿",
        "hero_subtitle": "AI à°†à°§à°¾à°°à°¿à°¤ à°¸à±à°®à°¾à°°à±à°Ÿà± à°¸à°¾à°—à±",
        "hero_desc": "à°­à°¾à°°à°¤ à°°à±ˆà°¤à±à°²à°•à± à°®à±‡à°§à°¸à±à°¸à± à°†à°§à°¾à°°à°¿à°¤ à°ªà°‚à°Ÿ à°¸à°¿à°«à°¾à°°à±à°¸à±à°²à±, à°®à°¾à°°à±à°•à±†à°Ÿà± à°…à°µà°—à°¾à°¹à°¨, à°¸à±à°¥à°¿à°°à°®à±ˆà°¨ à°¸à°¾à°—à± à°µà°¿à°§à°¾à°¨à°¾à°²à± à°…à°‚à°¦à°¿à°‚à°šà°¡à°‚.",
        "what_is": "à°«à°¸à°²à±à°¸à°¾à°°à±à°¥à°¿ à°…à°‚à°Ÿà±‡ à°à°®à°¿à°Ÿà°¿?",
        "what_is_desc": """
à°«à°¸à°²à±à°¸à°¾à°°à±à°¥à°¿ (à°«à°¸à°²à± = à°ªà°‚à°Ÿ, à°¸à°¾à°°à±à°¥à°¿ = à°®à°¾à°°à±à°—à°¦à°°à±à°¶à°•à±à°¡à±) à°­à°¾à°°à°¤ à°°à±ˆà°¤à±à°²à°•à± à°¡à±‡à°Ÿà°¾ à°†à°§à°¾à°°à°¿à°¤ à°¨à°¿à°°à±à°£à°¯à°¾à°²à± à°¤à±€à°¸à±à°•à±à°¨à±‡à°‚à°¦à±à°•à± à°¸à°¹à°¾à°¯à°ªà°¡à±‡ AI à°†à°§à°¾à°°à°¿à°¤ à°µà±à°¯à°µà°¸à°¾à°¯ à°¸à°²à°¹à°¾ à°µà±à°¯à°µà°¸à±à°¥.

à°‡à°¦à°¿ à°¨à±‡à°², à°µà°¾à°¤à°¾à°µà°°à°£à°‚, à°®à°¾à°°à±à°•à±†à°Ÿà± à°§à±‹à°°à°£à±à°²à°¨à± à°µà°¿à°¶à±à°²à±‡à°·à°¿à°‚à°šà°¿ à°ˆ à°µà°¿à°·à°¯à°¾à°²à±à°²à±‹ à°¸à°¿à°«à°¾à°°à±à°¸à±à°²à± à°‡à°¸à±à°¤à±à°‚à°¦à°¿:
- **à°ªà°‚à°Ÿ à°Žà°‚à°ªà°¿à°•** â€“ à°®à±€ à°­à±‚à°®à°¿à°•à°¿ à°¸à°°à°¿à°ªà±‹à°¯à±‡ à°ªà°‚à°Ÿà°²à±
- **à°Žà°°à±à°µà±à°² à°ªà±à°°à°£à°¾à°³à°¿à°•** â€“ à°¸à°°à±ˆà°¨ à°ªà±‹à°·à°• à°¨à°¿à°°à±à°µà°¹à°£
- **à°•à±€à°Ÿà°• & à°°à±‹à°— à°¨à°¿à°°à±à°µà°¹à°£** â€“ à°°à°•à±à°·à°£ à°µà±à°¯à±‚à°¹à°¾à°²à±
- **à°¦à°¿à°—à±à°¬à°¡à°¿ à°…à°‚à°šà°¨à°¾** â€“ à°¦à°¿à°—à±à°¬à°¡à°¿, à°†à°¦à°¾à°¯à°‚ à°…à°‚à°šà°¨à°¾à°²à±
- **à°®à°¾à°°à±à°•à±†à°Ÿà± à°¸à°®à°¾à°šà°¾à°°à°‚** â€“ à°§à°°à°²à±, à°¡à°¿à°®à°¾à°‚à°¡à± à°§à±‹à°°à°£à±à°²à±
        """,
        "features_title": "à°ªà±à°°à°§à°¾à°¨ à°²à°•à±à°·à°£à°¾à°²à±",
        "features": [
            ("ðŸŒ¿", "à°¸à±à°®à°¾à°°à±à°Ÿà± à°ªà°‚à°Ÿ à°¸à°¿à°«à°¾à°°à±à°¸à±à°²à±", "à°¨à±‡à°², à°µà°¾à°¤à°¾à°µà°°à°£à°‚, à°®à°¾à°°à±à°•à±†à°Ÿà± à°¡à±‡à°Ÿà°¾à°¤à±‹ AI à°†à°§à°¾à°°à°¿à°¤ à°¸à°¿à°«à°¾à°°à±à°¸à±à°²à±."),
            ("ðŸ“Š", "à°®à°¾à°°à±à°•à±†à°Ÿà± à°…à°µà°—à°¾à°¹à°¨", "22+ à°ªà°‚à°Ÿà°² à°§à°°à°²à±, à°§à±‹à°°à°£à±à°²à±, à°¡à°¿à°®à°¾à°‚à°¡à± à°µà°¿à°¶à±à°²à±‡à°·à°£."),
            ("ðŸ’§", "à°¨à±€à°Ÿà°¿ à°¨à°¿à°°à±à°µà°¹à°£", "à°ªà°‚à°Ÿ à°…à°µà°¸à°°à°¾à°²à°•à± à°…à°¨à±à°—à±à°£à°‚à°—à°¾ à°¸à°¾à°—à±à°¨à±€à°Ÿà°¿ à°·à±†à°¡à±à°¯à±‚à°²à±."),
            ("ðŸ§ª", "à°Žà°°à±à°µà± à°ªà±à°°à°£à°¾à°³à°¿à°•", "à°ªà±‹à°·à°• à°†à°§à°¾à°°à°¿à°¤ à°¸à°¿à°«à°¾à°°à±à°¸à±à°²à±, à°†à°°à±à°—à°¾à°¨à°¿à°•à± à°ªà±à°°à°¤à±à°¯à°¾à°®à±à°¨à°¾à°¯à°¾à°²à±."),
            ("ðŸ›", "à°•à±€à°Ÿà°• & à°°à±‹à°— à°¨à°¿à°¯à°‚à°¤à±à°°à°£", "à°°à°•à±à°·à°£ à°¸à±‚à°šà°¨à°²à± à°®à°°à°¿à°¯à± à°®à±à°‚à°¦à°¸à±à°¤à± à°¹à±†à°šà±à°šà°°à°¿à°•à°²à±."),
            ("ðŸ“ˆ", "à°¦à°¿à°—à±à°¬à°¡à°¿ à°…à°‚à°šà°¨à°¾", "ML à°†à°§à°¾à°°à°¿à°¤ à°¦à°¿à°—à±à°¬à°¡à°¿/à°†à°¦à°¾à°¯à°‚ à°…à°‚à°šà°¨à°¾à°²à±."),
        ],
        "tech_title": "à°Ÿà±†à°•à±à°¨à°¾à°²à°œà±€ à°¸à±à°Ÿà°¾à°•à±",
        "tech_desc": """
- **Machine Learning** â€“ à°­à°¾à°°à°¤à±€à°¯ à°µà±à°¯à°µà°¸à°¾à°¯ à°¡à±‡à°Ÿà°¾à°ªà±ˆ à°¶à°¿à°•à±à°·à°£ à°ªà±Šà°‚à°¦à°¿à°¨ à°®à±‹à°¡à°³à±à°²à±
- **Weather** â€“ à°µà°¾à°¤à°¾à°µà°°à°£ à°¸à±‡à°µà°² à°¸à°®à±€à°•à°°à°£
- **Market Data** â€“ à°®à°¾à°°à±à°•à±†à°Ÿà± à°§à°°à°²à±, à°¡à°¿à°®à°¾à°‚à°¡à± à°µà°¿à°¶à±à°²à±‡à°·à°£
- **Streamlit** â€“ à°†à°§à±à°¨à°¿à°• à°µà±†à°¬à± à°‡à°‚à°Ÿà°°à±â€Œà°«à±‡à°¸à±
- **Python Backend** â€“ à°¦à±ƒà°¢à°®à±ˆà°¨ à°¡à±‡à°Ÿà°¾ à°ªà±à°°à°¾à°¸à±†à°¸à°¿à°‚à°—à±
        """,
        "crops_title": "à°®à°¦à±à°¦à°¤à± à°ªà°‚à°Ÿà°²à± (22+)",
        "crops_desc": "à°­à°¾à°°à°¤à°¦à±‡à°¶à°‚à°²à±‹ à°µà°¿à°¸à±à°¤à°¾à°°à°‚à°—à°¾ à°ªà±†à°‚à°šà±‡ à°ªà°‚à°Ÿà°²à°•à± à°®à°¾ à°®à±‹à°¡à°²à± à°®à°¦à±à°¦à°¤à± à°‡à°¸à±à°¤à±à°‚à°¦à°¿:",
        "crops_list": [
            "ðŸŒ¾ à°§à°¾à°¨à±à°¯à°¾à°²à±: à°¬à°¿à°¯à±à°¯à°‚, à°—à±‹à°§à±à°®, à°®à±Šà°•à±à°•à°œà±Šà°¨à±à°¨",
            "ðŸ«˜ à°ªà°ªà±à°ªà±à°¦à°¿à°¨à±à°¸à±à°²à±: à°¶à°¨à°—, à°•à°‚à°¦à±à°²à±, à°®à°¿à°¨à±à°®à±à°²à±, à°ªà±†à°¸à°²à±, à°…à°°à°¹à°°à±, à°°à°¾à°œà±à°®à°¾, à°®à±Šà°¥à±",
            "ðŸ‰ à°ªà°‚à°¡à±à°²à±: à°®à°¾à°®à°¿à°¡à°¿, à°…à°°à°Ÿà°¿, à°†à°ªà°¿à°²à±, à°¨à°¾à°°à°¿à°‚à°œ, à°¦à±à°°à°¾à°•à±à°·, à°¬à±Šà°ªà±à°ªà°¾à°¯à°¿, à°¦à°¾à°¨à°¿à°®à±à°®, à°¤à°°à°¬à±‚à°œ, à°–à°°à±à°­à±‚à°œ",
            "â˜• à°¨à°—à°¦à± à°ªà°‚à°Ÿà°²à±: à°ªà°¤à±à°¤à°¿, à°œà±‚à°Ÿà±, à°•à°¾à°«à±€, à°•à±Šà°¬à±à°¬à°°à°¿",
        ],
        "mission_title": "à°®à°¾ à°²à°•à±à°·à±à°¯à°‚",
        "mission_desc": """
**"à°¸à±à°¥à°¿à°°à°®à±ˆà°¨, à°²à°¾à°­à°¦à°¾à°¯à°• à°µà±à°¯à°µà°¸à°¾à°¯à°¾à°¨à°¿à°•à°¿ à°ªà±à°°à°¤à°¿ à°°à±ˆà°¤à±à°•à°¿ AI à°†à°§à°¾à°°à°¿à°¤ à°®à°¾à°°à±à°—à°¦à°°à±à°¶à°¨à°‚."**
        """,
        "team_title": "à°®à°¾ à°Ÿà±€à°®à± à°—à±à°°à°¿à°‚à°šà°¿",
        "team_desc": "à°«à°¸à°²à±à°¸à°¾à°°à±à°¥à°¿ à°µà±à°¯à°µà°¸à°¾à°¯ à°¸à°¾à°‚à°•à±‡à°¤à°¿à°• à°•à°¾à°°à±à°¯à°•à±à°°à°®à°‚à°²à±‹ à°­à°¾à°—à°‚à°—à°¾ à°…à°­à°¿à°µà±ƒà°¦à±à°§à°¿ à°šà±‡à°¯à°¬à°¡à°¿à°‚à°¦à°¿.",
        "contact_title": "à°¸à°‚à°ªà±à°°à°¦à°¿à°‚à°šà°‚à°¡à°¿",
        "contact_desc": "à°®à±€ à°ªà±à°°à°¶à±à°¨à°²à± à°²à±‡à°¦à°¾ à°…à°­à°¿à°ªà±à°°à°¾à°¯à°¾à°²à± à°ªà°‚à°ªà°‚à°¡à°¿!",
        "language": "à°­à°¾à°·",
    },
}


def _repair_mojibake_text(value):
    if isinstance(value, dict):
        return {k: _repair_mojibake_text(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_repair_mojibake_text(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_repair_mojibake_text(item) for item in value)
    if isinstance(value, str):
        try:
            return value.encode("latin1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return value
    return value


TRANSLATIONS = _repair_mojibake_text(TRANSLATIONS)


def language_label(code: str) -> str:
    labels = {
        "en": "English",
        "hi": "\u0939\u093f\u0902\u0926\u0940",
        "te": "\u0c24\u0c46\u0c32\u0c41\u0c17\u0c41",
    }
    return labels.get(code, code)


def get_text(key: str) -> str:
    """Get translated text based on current language."""
    lang = st.session_state.get("language", "en")
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)



def render_language_selector(selector_key: str, label: str) -> None:
    options = ["en", "hi", "te"]
    current_language = st.session_state.get("language", "en")
    if current_language not in options:
        current_language = "en"
        st.session_state["language"] = "en"

    if selector_key not in st.session_state or st.session_state[selector_key] not in options:
        st.session_state[selector_key] = current_language
    elif st.session_state[selector_key] != current_language:
        st.session_state[selector_key] = current_language

    selected = st.selectbox(
        label,
        options=options,
        format_func=language_label,
        key=selector_key,
        label_visibility="collapsed",
    )
    if selected != current_language:
        st.session_state["language"] = selected
        st.rerun()


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
    # Initialize theme in session state
    if "theme" not in st.session_state:
        st.session_state["theme"] = "light"
    if "language" not in st.session_state:
        st.session_state["language"] = "en"

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
            "ðŸŒ™",
            value=is_dark,
            key="about_dark_mode_toggle",
            label_visibility="collapsed",
        )

        if dark_mode and current_theme != "dark":
            st.session_state["theme"] = "dark"
            st.rerun()
        elif not dark_mode and current_theme != "light":
            st.session_state["theme"] = "light"
            st.rerun()

    with col_lang:
        render_language_selector("about_language_selector", get_text("language"))

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
            <h2 style="color: {colors["title_color"]}; margin-bottom: 1rem;">ðŸŒ± {get_text("what_is")}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(get_text("what_is_desc"))

    st.markdown("---")

    # Features
    st.subheader(f"â­ {get_text('features_title')}")

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
    st.subheader(f"ðŸŒ¾ {get_text('crops_title')}")
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
        st.subheader(f"ðŸ”§ {get_text('tech_title')}")
        st.markdown(get_text("tech_desc"))

    with col2:
        st.subheader(f"ðŸŽ¯ {get_text('mission_title')}")
        st.markdown(get_text("mission_desc"))

    st.markdown("---")

    # Team & Contact
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"ðŸ‘¥ {get_text('team_title')}")
        st.markdown(get_text("team_desc"))

    with col2:
        st.subheader(f"ðŸ“§ {get_text('contact_title')}")
        st.write(get_text("contact_desc"))
        st.markdown(
            f"""
            <div style="background: {colors["card_bg"]}; border-radius: 12px; padding: 1.5rem; margin-top: 1rem;">
                <p style="margin: 0.5rem 0; color: {colors["text_color"]};">ðŸ“§ Email: support@fasalsaarthi.in</p>
                <p style="margin: 0.5rem 0; color: {colors["text_color"]};">ðŸŒ Website: www.fasalsaarthi.in</p>
                <p style="margin: 0.5rem 0; color: {colors["text_color"]};">ðŸ“± Helpline: 1800-XXX-XXXX (Toll Free)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Footer handled globally.


if __name__ == "__main__":
    main()

