import json
from typing import Optional

from botocore.exceptions import ClientError

from app.domains.weather.schemas import CityFileInfoSchema, LocationWeatherSchema
from app.infrastructure.aws import s3_service


class WeatherS3Repository:
    """
    S3 repository for weather data file storage.

    Manages saving and retrieving weather data files in S3
    with automatic bucket creation and JSON serialization.
    """
    bucket_name = "weather-data"

    async def create_bucket(self):
        """Create S3 bucket for weather data storage."""
        await s3_service.create_bucket(self.bucket_name)

    async def save_weather_file(self, file_path: str, weather_data: LocationWeatherSchema) -> bool:
        """
        Save weather data to S3 as JSON file.

        Args:
            file_path: S3 object key for the weather file.
            weather_data: Weather data to save.

        Returns:
            bool: True if saved successfully.

        Raises:
            ClientError: For S3 operation errors (auto-creates bucket if missing).
        """
        content = weather_data.model_dump_json(indent=2)

        put_object_params = {
            "bucket_name": self.bucket_name,
            "key": file_path,
            "body": content.encode('utf-8'),
            "content_type": "application/json",
        }

        try:
            return await s3_service.put_object(**put_object_params)
        except ClientError as ex:
            error_code = ex.response["Error"]["Code"]
            if error_code == "NoSuchBucket":
                await s3_service.create_bucket(self.bucket_name)
                return await s3_service.put_object(**put_object_params)
            raise

    async def get_weather_file_content(self, file_path: str) -> Optional[LocationWeatherSchema]:
        """
        Retrieve weather data from S3 file.

        Args:
            file_path: S3 object key for the weather file.

        Returns:
            Optional[LocationWeatherSchema]: Weather data if file exists, None otherwise.
        """
        content = await s3_service.get_object_content(self.bucket_name, file_path)
        if content:
            return LocationWeatherSchema.model_validate(json.loads(content))
        return None
