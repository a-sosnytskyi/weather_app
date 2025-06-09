from typing import Dict, Any, Optional
from botocore.exceptions import ClientError

from app.kernel.logs import logger
from ..client import aws_client


class DynamoDBService:
    """Service for working with DynamoDB operations."""

    async def create_table(self, table_name: str, key_schema: list, attribute_definitions: list):
        """
        Create DynamoDB table with pay-per-request billing.

        Args:
            table_name: Name of the table to create.
            key_schema: List of key schema definitions.
            attribute_definitions: List of attribute definitions.

        Returns:
            dict: Table creation response or None if ResourceNotFoundException.

        Raises:
            ClientError: For DynamoDB operation errors.
        """
        async with aws_client.get_dynamodb_client() as client:
            try:
                response = await client.create_table(
                    TableName=table_name,
                    KeySchema=key_schema,
                    AttributeDefinitions=attribute_definitions,
                    BillingMode='PAY_PER_REQUEST'
                )
                logger.info(f"Created DynamoDB table '{table_name}'")
                return response

            except ClientError as ex:
                error_code = ex.response['Error']['Code']
                if error_code == 'ResourceNotFoundException':
                    return None

                logger.error(f"Failed to create DynamoDB table '{table_name}'. Error code: {error_code}")
                raise

            except Exception as ex:
                logger.error(f"Failed to create DynamoDB table '{table_name}'. Error: {str(ex)}")
                raise

    async def delete_table(self, table_name: str):
        """
        Delete DynamoDB table.

        Args:
            table_name: Name of the table to delete.

        Returns:
            dict: Table deletion response or None if table not found.

        Raises:
            ClientError: For DynamoDB operation errors.
        """
        async with aws_client.get_dynamodb_client() as client:
            try:
                response = await client.delete_table(TableName=table_name)
                logger.info(f"Removed DynamoDB table '{table_name}'")
                return response

            except ClientError as ex:
                error_code = ex.response['Error']['Code']
                if error_code == 'ResourceNotFoundException':
                    return None

                logger.error(f"Failed to delete DynamoDB table '{table_name}'. Error code: {error_code}")
                raise

            except Exception as ex:
                logger.error(f"Failed to delete DynamoDB table '{table_name}'. Error: {str(ex)}")
                raise

    async def put_item(self, table_name: str, item: Dict[str, Any]):
        """
        Add item to DynamoDB table.

        Args:
            table_name: Name of the target table.
            item: Item data to insert.

        Returns:
            dict: Put item operation response.
        """
        async with aws_client.get_dynamodb_resource() as dynamodb:
            try:
                table = await dynamodb.Table(table_name)
                result = await table.put_item(Item=item)
                logger.debug(f"Put item in DynamoDB table '{table_name}'")
                return result

            except Exception as ex:
                logger.error(f"Failed to put item into DynamoDB table. Error: {str(ex)}")
                raise

    async def get_item(self, table_name: str, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get item from DynamoDB table by key.

        Args:
            table_name: Name of the source table.
            key: Primary key of the item to retrieve.

        Returns:
            Optional[Dict[str, Any]]: Item data if found, None otherwise.
        """
        async with aws_client.get_dynamodb_resource() as dynamodb:
            try:
                table = await dynamodb.Table(table_name)
                response = await table.get_item(Key=key)
                return response.get('Item')
            except Exception as ex:
                logger.error(f"Failed to get item from DynamoDB table. Error: {str(ex)}")
                raise

    async def delete_item(self, table_name: str, key: Dict[str, Any]):
        """
        Delete item from DynamoDB table.

        Args:
            table_name: Name of the target table.
            key: Primary key of the item to delete.

        Returns:
            dict: Delete item operation response.
        """
        async with aws_client.get_dynamodb_resource() as dynamodb:
            try:
                table = await dynamodb.Table(table_name)
                result = await table.delete_item(Key=key)
                logger.debug(f"Removed item from DynamoDB table '{table_name}', Key '{str(key)}'")
                return result
            except Exception as ex:
                logger.error(f"Failed to put item into DynamoDB table. Error: {str(ex)}")
                raise


dynamodb_service = DynamoDBService()
