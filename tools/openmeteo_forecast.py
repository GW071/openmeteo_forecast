from pydantic import BaseModel, Field, ValidationError
from typing import Annotated, List, Optional
from utils.http_client import fetch_url
from urllib.parse import urlencode
from . import mcp

BASE_URL = "https://api.open-meteo.com/v1/forecast"



class ForecastInput(BaseModel):
    latitude: float
    longitude: float
    hourly: Annotated[List[str], Field(min_length=1)]
    timezone: str = "auto"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    past_days: Optional[int] = None

def validate_forecast_inputs(args: ForecastInput):
    lat = args.latitude
    lon = args.longitude
    hourly = args.hourly
    if not (-90 <= lat <= 90):
        raise ValueError("Latitude must be between -90 and 90.")
    if not (-180 <= lon <= 180):
        raise ValueError("Longitude must be between -180 and 180.")

def build_url(params: dict) -> str:
    filtered_params = {k: v for k, v in params.items() if v is not None}
    if isinstance(filtered_params.get("hourly"), list):
        filtered_params["hourly"] = ",".join(filtered_params["hourly"])
    query_string = urlencode(filtered_params)
    return f"{BASE_URL}?{query_string}"

@mcp.tool()
async def openmeteo_forecast(latitude: float, longitude: float, hourly: List[str], timezone: str = "auto",
                             start_date: Optional[str] = None, end_date: Optional[str] = None, past_days: Optional[int] = None):
    """
        Get weather forecast data from the Open-Meteo API.

        Parameters:
        - latitude (float): Geographic latitude (-90 to 90)
        - longitude (float): Geographic longitude (-180 to 180)
        - hourly (List[str]): List of weather parameters to request (e.g., temperature_2m)
        - timezone (str): Timezone for data output (default: 'auto')
        - start_date (str, optional): Start date in 'YYYY-MM-DD' format
        - end_date (str, optional): End date in 'YYYY-MM-DD' format
        - past_days (int, optional): Number of past days to include

        Returns:
        - JSON response from Open-Meteo API if successful
        - Error message dictionary if validation or API call fails
    """
    try:
        inputs = ForecastInput(
            latitude=latitude, longitude=longitude, hourly=hourly,
            timezone=timezone, start_date=start_date, end_date=end_date, past_days=past_days
        )
        validate_forecast_inputs(inputs)
        url = build_url(inputs.model_dump(exclude_none=True))
        return await fetch_url(url)
    except ValidationError as e:
        return {"error": "Invalid input parameters", "details": e.errors()}
    except Exception as e:
        return {"error": str(e)}


