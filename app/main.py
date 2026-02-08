"""Streamlit interface for the hackathon-ready crop intelligence platform."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    """Legacy entry point retained for backward compatibility.

    The project now uses frontend/app.py as the main Streamlit interface. This stub
    exists to guide developers who may still run ``streamlit run app/main.py``.
    """

    from __future__ import annotations

    import sys
    from pathlib import Path

    import streamlit as st

    ROOT = Path(__file__).resolve().parents[1]

    def main() -> None:
        st.warning(
            "This entry point moved. Launch the new UI via `streamlit run frontend/app.py`."
        )
        st.info(f"Project root: {ROOT}")

    if __name__ == "__main__":
        main()
        st.write(f"☁️ {advisory}")
