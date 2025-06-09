import re
from datetime import datetime, timezone

from pydantic import Field, BaseModel

__all__ = [
    "CityFileInfoSchema",
]


class CityFileInfoSchema(BaseModel):
    """
    Schema for city weather file information.

    Contains city name and timestamp for generating
    unique file names for weather data storage.

    Attributes:
        city_name: Name of the city.
        timestamp: UTC timestamp (auto-generated if not provided).
    """
    city_name: str
    timestamp: int = Field(default_factory=lambda: int(datetime.now(timezone.utc).timestamp()))

    @property
    def file_name(self):
        """
        Generate sanitized file name for weather data.

        Creates file name by sanitizing city name and appending timestamp.
        Removes special characters and normalizes underscores.

        Returns:
            str: Sanitized file name in format '{city_name}_{timestamp}.json'.
        """
        prepared_city_name = re.sub(r'[^\w\-_]', '_', self.city_name.lower())
        prepared_city_name = re.sub(r'_+', '_', prepared_city_name).strip('_')
        return f"{prepared_city_name}_{self.timestamp}.json"
