import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from pydantic import ValidationError
from tools.openmeteo_forecast import ForecastInput, validate_forecast_inputs, build_url, openmeteo_forecast

def test_build_url():
    params = {
        "latitude": 45.0,
        "longitude": 90.0,
        "hourly": ["temperature_2m", "precipitation"],
        "timezone": "auto",
        "start_date": None,
        "end_date": None,
        "past_days": None
    }
    url = build_url(params)
    expected_url = "https://api.open-meteo.com/v1/forecast?latitude=45.0&longitude=90.0&hourly=temperature_2m%2Cprecipitation&timezone=auto"
    assert url == expected_url

def test_forecast_input_validation():
    # Valid input
    valid_input = ForecastInput(
        latitude=45.0,
        longitude=90.0,
        hourly=["temperature_2m", "precipitation"],
        timezone="auto"
    )
    validate_forecast_inputs(valid_input)

    # Invalid latitude
    with pytest.raises(ValueError):
        invalid_lat_input = ForecastInput(
            latitude=100.0,
            longitude=90.0,
            hourly=["temperature_2m"],
            timezone="auto"
        )
        validate_forecast_inputs(invalid_lat_input)

    # Invalid longitude
    with pytest.raises(ValueError):
        invalid_lon_input = ForecastInput(
            latitude=45.0,
            longitude=200.0,
            hourly=["temperature_2m"],
            timezone="auto"
        )
        validate_forecast_inputs(invalid_lon_input)

@pytest.mark.asyncio
async def test_openmeteo_forecast():
    response = await openmeteo_forecast(
        latitude=45.0,
        longitude=90.0,
        hourly=["temperature_2m", "precipitation"],
        timezone="auto"
    )
    assert "latitude" in response
    assert "longitude" in response
    assert "hourly" in response