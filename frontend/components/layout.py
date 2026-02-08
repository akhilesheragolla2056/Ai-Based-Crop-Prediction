"""Layout primitives for the Streamlit frontend."""

from __future__ import annotations

import streamlit as st


def inject_theme() -> None:
    """Inject the custom CSS theme into Streamlit - now handled by app.py apply_theme()."""
    # Theme CSS is now handled directly in app.py's apply_theme() function
    pass


def render_header() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="logo">🌾 FasalSaarthi</div>
            <div class="tagline">AI-Powered Smart Farming</div>
            <p class="hero-subtitle">Your AI Guide for Smarter Farming</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
