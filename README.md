# openmeteo_forecast

build a minimal MCP server with one tool that fetches weather data from Open-Meteo.

## Environment
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
source .venv/bin/activate
uv sync

## Run server
python server.py

## test
pytest -v