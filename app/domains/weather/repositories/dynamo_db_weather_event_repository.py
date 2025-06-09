from botocore.exceptions import ClientError

from app.domains.weather.schemas import CityFileInfoSchema
from app.infrastructure.aws import dynamodb_service


class DynamoDBWeatherEventRepository:
    """
    Repository for weather data persistence in DynamoDB.

    Manages weather event storage and retrieval operations
    in DynamoDB table with automatic table creation.
    """
    table_name = "fetch_weather_history"

    async def create_table(self):
        """
        Create weather events table in DynamoDB.

        Creates table with composite primary key consisting of
        city_name (hash key) and timestamp (range key).

        Returns:
            dict: DynamoDB table creation response.
        """
        key_schema = [
            {'AttributeName': 'city_name', 'KeyType': 'HASH'},
            {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
        ]

        attribute_definitions = [
            {'AttributeName': 'city_name', 'AttributeType': 'S'},
            {'AttributeName': 'timestamp', 'AttributeType': 'N'}
        ]

        return await dynamodb_service.create_table(
            self.table_name,
            key_schema,
            attribute_definitions)

    async def put_weather_event(self, city_file_info: CityFileInfoSchema):
        """
        Store weather event information in DynamoDB.

        Args:
            city_file_info: Schema containing city name, timestamp and file path.

        Returns:
            dict: DynamoDB put_item response.

        Raises:
            ClientError: For DynamoDB operation errors (auto-creates table if missing).
        """

        item = {
            'city_name': city_file_info.city_name,
            'timestamp': city_file_info.timestamp,
            'file_path': city_file_info.file_name
        }

        try:
            return await dynamodb_service.put_item(self.table_name, item)
        except ClientError as ex:
            error_code = ex.response['Error']['Code']
            if error_code == "ResourceNotFoundException":
                await self.create_table()
                return await dynamodb_service.put_item(self.table_name, item)
            raise
