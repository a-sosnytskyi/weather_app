from app.domains.weather.clients import OpenWeatherMapClient
from app.domains.weather.schemas import LocationWeatherSchema, LocationCoordSchema


class WeatherDataService:
    """Service for fetching and processing weather data from external APIs."""

    def __init__(self):
        self._client = OpenWeatherMapClient()

    async def fetch_coord_weather_from_open_weather(self, coord: LocationCoordSchema) -> LocationWeatherSchema:
        """
        Fetch weather data for coordinates from OpenWeatherMap API.

        Args:
            coord: Geographic coordinates for weather data retrieval.

        Returns:
            LocationWeatherSchema: Processed weather data in internal format.
        """
        # Get city coordinates
        weather_resp_data = await self._client.get_location_weather(coord)
        # Convert to our internal schema
        return LocationWeatherSchema.from_open_weather_map_resp(weather_resp_data)

    async def fetch_city_geo(self, city_name: str) -> LocationCoordSchema:
        """
        Fetch geographical coordinates for a city.

        Args:
            city_name: Name of the city to get coordinates for.

        Returns:
            LocationCoordSchema: Geographic coordinates of the city.
        """
        return await self._client.get_city_geo(city_name)