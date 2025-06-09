from typing import Dict, Any

import httpx

from app.domains.weather.schemas import LocationCoordSchema
from app.exceptions import BadGatewayException, NotFoundException, BadRequestException
from app.kernel.logs import logger
from app.kernel.settings import open_weather_settings
from .schemas import WeatherResponseSchema


class OpenWeatherMapClient:
    """
    Client for interacting with OpenWeatherMap API.

    Provides methods to fetch city coordinates and weather data from OpenWeatherMap service.
    """

    def __init__(self):
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.geo_url = "http://api.openweathermap.org/geo/1.0"
        self.timeout = 10.0

    @property
    def secret_key(self) -> str:
        """Get OpenWeatherMap API key from settings."""
        if not open_weather_settings.secret_key:
            raise ValueError("OpenWeatherMap API key is not configured")

        return open_weather_settings.secret_key

    async def _do_request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute HTTP request to OpenWeatherMap API.

        Args:
            url: API endpoint URL.
            params: Request parameters dictionary.

        Returns:
            Dict[str, Any]: JSON response from the API.

        Raises:
            BadRequestException: For invalid API key or client errors.
            BadGatewayException: For server errors or timeouts.
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.debug(f"Making request to {url} with params: {params}")
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} from {url}: {e.response.text}")
            if e.response.status_code == 401:
                raise BadRequestException("Invalid API key")
            elif e.response.status_code >= 500:
                raise BadGatewayException(
                    f"Weather service server error: {e.response.status_code}")
            else:
                raise

        except httpx.TimeoutException:
            logger.warning(f"Timeout occurred for request to {url}")
            raise BadGatewayException("Weather service timeout")

        except Exception as e:
            logger.error(f"Unexpected error during request to {url}: {e}")
            raise BadRequestException(f"Request failed: {str(e)}")

    async def get_city_geo(self, city_name: str) -> LocationCoordSchema:
        """
        Get geographical coordinates for a city.

        Args:
            city_name: Name of the city to search for.

        Returns:
            LocationCoordSchema: Latitude and longitude coordinates.

        Raises:
            NotFoundException: If city is not found.
            BadRequestException: For invalid requests or API errors.
            BadGatewayException: For service unavailability.
        """
        url = f"{self.geo_url}/direct"
        params = {
            "q": city_name.strip(),
            "limit": 1,
            "appid": self.secret_key
        }

        logger.info(f"Fetching coordinates for city: {city_name}")
        try:
            data = await self._do_request(url, params)
            if not data:
                logger.warning(f"No coordinates found for city: {city_name}")
                raise NotFoundException(f"City '{city_name}' not found")

            logger.info(f"Successfully found coordinates for city: {city_name}")
            geo_data = data[0]
            return LocationCoordSchema(
                lat=geo_data["lat"],
                lon=geo_data["lon"])

        except (BadRequestException, BadGatewayException):
            raise

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise NotFoundException(f"City '{city_name}' not found")

            logger.error(f"HTTP error {e.response.status_code} from {url}: {e.response.text}")
            raise BadRequestException(f"Failed to fetch city coordinates: {e.response.status_code}")

        except Exception as ex:
            logger.error(f"Unexpected error during request to {url}: {str(ex)}")
            raise BadRequestException(f"Failed to fetch city coordinates: {str(ex)}")

    async def get_location_weather(self, coord: LocationCoordSchema) -> WeatherResponseSchema:
        """
        Get current weather data for specific coordinates.

        Args:
            coord: Location coordinates (latitude and longitude).

        Returns:
            WeatherResponseSchema: Current weather information.

        Raises:
            BadRequestException: For invalid coordinates or API errors.
            BadGatewayException: For service unavailability.
        """
        url = f"{self.base_url}/weather"
        params = {
            "lat": coord.lat,
            "lon": coord.lon,
            "appid": self.secret_key,
            "units": "metric",
            "lang": "en"
        }

        logger.info(f"Fetching weather for coord: {str(coord)}")
        try:
            data = await self._do_request(url, params)
            result = WeatherResponseSchema.model_validate(data)
            logger.info(f"Successfully fetched weather for coord: {str(coord)}")
            return result

        except (BadRequestException, BadGatewayException):
            raise

        except httpx.HTTPStatusError as ex:
            if ex.response.status_code == 400:
                raise BadRequestException(f"Invalid coordinates: {coord.lat}, {coord.lon}")

            logger.error(f"HTTP error {ex.response.status_code} from {url}: {ex.response.text}")
            raise BadRequestException(f"Failed to fetch weather data: {ex.response.status_code}")

        except Exception as ex:
            logger.error(f"Unexpected error during request to {url}: {str(ex)}")
            raise BadRequestException(f"Failed to fetch weather data: {str(ex)}")
