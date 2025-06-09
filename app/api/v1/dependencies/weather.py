from app.domains.weather.schemas import FetchCityWeatherFiltersSchema


__all__ = [
    "validate_fetch_city_weather_filters",
]


def validate_fetch_city_weather_filters(city: str) -> FetchCityWeatherFiltersSchema:
    """
    Validate the weather filters for fetching data.

    Args:
        city (str): The city name.

    Returns:
        FetchCityWeatherFiltersSchema: The validated data.
    """
    return FetchCityWeatherFiltersSchema(city=city)
