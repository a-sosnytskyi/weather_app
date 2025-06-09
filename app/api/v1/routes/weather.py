from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends

from app.api.base import BaseAPIRouteWrapper, BaseErrorRSchema
from app.api.v1.dependencies import validate_fetch_city_weather_filters
from app.api.v1.tags import WEATHER_TAG
from app.domains.weather import WeatherApplicationService
from app.domains.weather.schemas import FetchCityWeatherFiltersSchema, LocationWeatherSchema

if TYPE_CHECKING:
    from app.domains.weather.schemas import FetchCityWeatherFiltersSchema


class WeatherEndpointsAPI(BaseAPIRouteWrapper):
    """
    Weather API endpoints for retrieving weather information.
    """
    router = APIRouter(prefix="/weather", tags=[WEATHER_TAG])

    @staticmethod
    @router.get("/", response_model=LocationWeatherSchema, responses={
        400: {"model": BaseErrorRSchema},
        404: {"model": BaseErrorRSchema}
    })
    async def get_city_weather_info(
            query_filters: "FetchCityWeatherFiltersSchema" = Depends(validate_fetch_city_weather_filters)
    ):
        """
        Get weather information for a specific city.

        Args:
            query_filters: Validated query parameters containing city name.

        Returns:
            LocationWeatherSchema: Weather data for the requested city.
        """
        return await (
            WeatherApplicationService()
            .get_city_weather(query_filters.city))
