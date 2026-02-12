"""Legacy entry point that forwards to the new frontend app."""

from __future__ import annotations

import sys
from pathlib import Path
import runpy

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_APP = PROJECT_ROOT / "frontend" / "app.py"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> None:
    """Forward execution to frontend.app while providing helpful messaging."""

    if not FRONTEND_APP.exists():
        st.error(
            "frontend/app.py is missing. Launch streamlit run frontend/app.py instead."
        )
        raise RuntimeError("frontend.app module unavailable")

    # Execute the frontend app file directly to avoid package import issues on Streamlit Cloud.
    runpy.run_path(str(FRONTEND_APP), run_name="__main__")


if __name__ == "__main__":
    main()
