from pydantic import BaseModel

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.domains.weather.clients.open_weather_map_client import WeatherResponseSchema


__all__ = [
    'LocationWeatherSchema',
]


class Coordinates(BaseModel):
    """
    Geographic coordinates.

    Attributes:
        lon: Longitude coordinate.
        lat: Latitude coordinate.
    """
    lon: float
    lat: float


class Weather(BaseModel):
    """
    Weather condition summary.

    Attributes:
        main: Main weather condition (e.g., Rain, Snow, Clear).
        description: Detailed weather description.
    """
    main: str
    description: str


class Temperature(BaseModel):
    """
    Temperature information in Celsius.

    Attributes:
        temp: Current temperature.
        feels_like: Perceived temperature.
        temp_min: Minimum temperature.
        temp_max: Maximum temperature.
        humidity: Humidity percentage.
    """
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    humidity: int


class Wind(BaseModel):
    """
    Wind information.

    Attributes:
        speed: Wind speed in m/s.
        deg: Wind direction in degrees.
        gust: Wind gust speed in m/s (optional).
    """
    speed: float
    deg: int
    gust: Optional[float] = None


class LocationWeatherSchema(BaseModel):
    """
    Simplified weather data for local use.

    Unified schema for weather information from external APIs.

    Attributes:
        location: City or location name.
        coordinates: Geographic coordinates.
        weather: Weather condition summary.
        temperature: Temperature information.
        wind: Wind information.
        visibility: Visibility in meters.
        timestamp: Unix timestamp of weather data.
    """
    location: str
    coordinates: Coordinates
    weather: Weather
    temperature: Temperature
    wind: Wind
    visibility: int
    timestamp: int

    @classmethod
    def from_open_weather_map_resp(cls, weather_data: "WeatherResponseSchema"):
        """
        Create LocationWeatherSchema from OpenWeatherMap API response.

        Args:
            weather_data: Raw weather response from OpenWeatherMap API.

        Returns:
            LocationWeatherSchema: Converted weather data.

        Raises:
            TypeError: If weather_data is not WeatherResponseSchema.
            ValueError: If weather data is empty or invalid.
        """
        from app.domains.weather.clients.open_weather_map_client import WeatherResponseSchema
        if not isinstance(weather_data, WeatherResponseSchema):
            raise TypeError("WeatherResponseSchema expected")

        # Get first weather item from the list
        first_weather = weather_data.weather[0] if weather_data.weather else None
        if not first_weather:
            raise ValueError("Weather data is empty")

        return cls(
            location=weather_data.name,
            coordinates=Coordinates(
                lon=weather_data.coord.lon,
                lat=weather_data.coord.lat
            ),
            weather=Weather(
                main=first_weather.main,
                description=first_weather.description
            ),
            temperature=Temperature(
                temp=weather_data.main.temp,
                feels_like=weather_data.main.feels_like,
                temp_min=weather_data.main.temp_min,
                temp_max=weather_data.main.temp_max,
                humidity=weather_data.main.humidity
            ),
            wind=Wind(
                speed=weather_data.wind.speed,
                deg=weather_data.wind.deg,
                gust=weather_data.wind.gust
            ),
            visibility=weather_data.visibility,
            timestamp=weather_data.dt)
