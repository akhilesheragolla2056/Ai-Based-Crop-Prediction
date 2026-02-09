"""Legacy entry point that forwards to the new frontend app."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_APP = PROJECT_ROOT / "frontend" / "app.py"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> None:
    """Forward execution to frontend.app while providing helpful messaging."""

    try:
        frontend_module = importlib.import_module("frontend.app")
    except ModuleNotFoundError as exc:
        st.error(
            "frontend.app is missing or failed to import. Launch streamlit run frontend/app.py instead."
        )
        if FRONTEND_APP.exists():
            st.info(f"Detected frontend/app.py at {FRONTEND_APP}.")
        raise RuntimeError("frontend.app module unavailable") from exc

    frontend_module.main()


if __name__ == "__main__":
    main()
