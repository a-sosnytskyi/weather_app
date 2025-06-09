from typing import Optional

from app.domains.weather.schemas import LocationCoordSchema, LocationWeatherSchema
from app.infrastructure.cache import CacheManager


class WeatherCacheRepository:
    """
    Cache repository for weather data and city coordinates.

    Manages caching of city geographical data and weather file paths
    with configurable TTL and automatic serialization.
    """
    city_geo_key_prefix = "cityGeo/"
    city_weather_key_prefix = "cityWeather/"

    def _get_city_geo_cache_key(self, city_name: str) -> str:
        """Generate cache key for city geographical coordinates."""
        return f"{self.city_geo_key_prefix}{city_name}"

    def _get_city_weather_cache_key(self, city_name: str) -> str:
        """Generate cache key for city weather data."""
        return f"{self.city_weather_key_prefix}{city_name}"

    async def get_city_geo(self, city_name: str) -> Optional[LocationCoordSchema]:
        """
        Retrieve cached city coordinates.

        Args:
            city_name: Name of the city to lookup.

        Returns:
            Optional[LocationCoordSchema]: City coordinates if cached, None otherwise.
        """
        val = await CacheManager().get(key=self._get_city_geo_cache_key(city_name))
        if val:
            return LocationCoordSchema.model_validate(val)
        return None

    async def set_city_geo(self, city_name, coord: LocationCoordSchema):
        """
        Cache city geographical coordinates.

        Args:
            city_name: Name of the city.
            coord: Location coordinates to cache.
        """
        return await CacheManager().set(
            key=self._get_city_geo_cache_key(city_name),
            value=coord.model_dump_json())

    async def get_city_weather_file(self, city_name: str) -> str:
        """
        Retrieve cached weather file path for city.

        Args:
            city_name: Name of the city.

        Returns:
            str: Cached file path for weather data.
        """
        return await CacheManager().get(key=self._get_city_weather_cache_key(city_name))

    async def set_city_weather_file(self, city_name: str, file_path: str, ttl: Optional[int] = None):
        """
        Cache weather file path for city.

        Args:
            city_name: Name of the city.
            file_path: Path to weather data file.
            ttl: Time to live in seconds (optional).
        """
        return await CacheManager().set(
            key=self._get_city_weather_cache_key(city_name),
            value=file_path,
            ttl=ttl)
