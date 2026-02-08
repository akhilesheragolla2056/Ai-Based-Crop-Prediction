"""Reusable result card components."""

from __future__ import annotations

import streamlit as st


def metric_card(
    title: str, value: str, subtitle: str | None = None, icon: str | None = None
) -> None:
    """Render a highlighted metric style card."""

    icon_block = f"<span class='card-icon'>{icon}</span>" if icon else ""
    subtitle_block = f"<div class='card-subtitle'>{subtitle}</div>" if subtitle else ""
    st.markdown(
        f"""
        <div class="card metric-card">
            <div class="card-title">{icon_block}<span>{title}</span></div>
            <div class="card-value">{value}</div>
            {subtitle_block}
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(title: str, body: str, icon: str = "ℹ️") -> None:
    icon_block = f"<span class='card-icon'>{icon}</span>" if icon else ""
    st.markdown(
        f"""
        <div class="card info-card">
            <div class="card-title">{icon_block}<span>{title}</span></div>
            <div class="card-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def list_card(title: str, items: list[str], icon: str = "✅") -> None:
    icon_block = f"<span class='card-icon'>{icon}</span>" if icon else ""
    items_html = "".join(f"<li>{item}</li>" for item in items)
    st.markdown(
        f"""
        <div class="card list-card">
            <div class="card-title">{icon_block}<span>{title}</span></div>
            <ul>{items_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
