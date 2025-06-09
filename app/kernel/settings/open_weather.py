from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class SettingsOpenWeather(BaseSettings):
    """
    OpenWeatherMap API configuration settings.

    Attributes:
        secret_key: API key for OpenWeatherMap service authentication.
    """
    secret_key: Optional[str] = Field(default=None, validation_alias="OPEN_WEATHER_MAP_KEY")


open_weather_settings = SettingsOpenWeather()
