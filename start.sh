#!/usr/bin/env bash
set -euo pipefail

PORT_VALUE="${PORT:-8501}"

exec streamlit run app/main.py \
  --server.address=0.0.0.0 \
  --server.port="${PORT_VALUE}" \
  --server.headless=true