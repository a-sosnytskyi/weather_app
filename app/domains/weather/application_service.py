import asyncio

from app.domains.weather.data_service import WeatherDataService
from app.kernel.logs import logger
from .repositories import WeatherCacheRepository, WeatherS3Repository, DynamoDBWeatherEventRepository
from .schemas import LocationCoordSchema, LocationWeatherSchema, CityFileInfoSchema


class WeatherApplicationService:
    """
    Application service for weather data operations.

    Orchestrates weather data retrieval with multi-layer caching, persistence to S3, and event logging to DynamoDB.
    """

    def __init__(self):
        self._weather_data_service = WeatherDataService()
        self._cache_repository = WeatherCacheRepository()
        self._s3_repository = WeatherS3Repository()
        self._dynamodb_repository = DynamoDBWeatherEventRepository()

    async def get_city_weather(self, city_name: str) -> LocationWeatherSchema:
        """
        Get weather information for a city with caching.

        Implements multi-level data retrieval strategy:
        1. Check cache for existing weather file
        2. If cached, retrieve from S3
        3. If not cached, fetch from external API
        4. Save new data to S3, cache, and log event

        Args:
            city_name: Name of the city to get weather for.

        Returns:
            LocationWeatherSchema: Current weather data for the city.
        """
        location_weather = None
        file_path_from_cache = await self._cache_repository.get_city_weather_file(city_name)
        if file_path_from_cache:
            try:
                location_weather = await self._s3_repository.get_weather_file_content(file_path_from_cache)
                logger.debug(f"Extracted location weather from cached file: {file_path_from_cache}")
            except:
                pass

        if not location_weather:
            coord = await self.get_city_geo(city_name)
            location_weather = await self._weather_data_service.fetch_coord_weather_from_open_weather(coord)
            city_file_info = CityFileInfoSchema.model_validate({
                "city_name": city_name,
                "timestamp": location_weather.timestamp
            })

            # upload file to s3
            asyncio.create_task(self._s3_repository.save_weather_file(
                file_path=city_file_info.file_name,
                weather_data=location_weather))

            # set filepath to cache
            asyncio.create_task(self._cache_repository.set_city_weather_file(
                city_name=city_name,
                file_path=city_file_info.file_name,
                ttl=300))

            # log dynamo db event
            asyncio.create_task(self._dynamodb_repository.put_weather_event(city_file_info))

        return location_weather

    async def get_city_geo(self, city_name: str) -> LocationCoordSchema:
        """
        Get geographical coordinates for a city with caching.

        Checks cache first, then fetches from external API if needed.
        Automatically caches new coordinate data for future requests.

        Args:
            city_name: Name of the city to get coordinates for.

        Returns:
            LocationCoordSchema: Geographical coordinates of the city.
        """
        data_from_cache = await self._cache_repository.get_city_geo(city_name)
        if data_from_cache:
            return data_from_cache

        data_from_api = await self._weather_data_service.fetch_city_geo(city_name)
        await self._cache_repository.set_city_geo(city_name, coord=data_from_api)
        return data_from_api
