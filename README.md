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

## client
follow https://modelcontextprotocol.io/docs/develop/build-server and edit necessary parts

## example request prompt

Get the hourly **temperature** and **windspeed** for Berlin for today and tomorrow in the local timezone.



## Shortage
I plan to put all of the weather parameters in the class ForecastInput(BaseModel) Object, so it would be easier to add new parameters.

But currently, I only find one way to generate tool by using @mcp.tool decorator, so I must write all of the parameters in the function signature of the tool function.
