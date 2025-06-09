from contextlib import asynccontextmanager

import aioboto3
from app.kernel.settings import aws_settings


class AWSClient:
    """
    AWS client wrapper for managing boto3 sessions and service clients.

    Provides async context managers for AWS services with configurable
    endpoint URLs for LocalStack support and credential management.
    """

    def __init__(self):
        self.endpoint_url = aws_settings.endpoint_url
        self.region = aws_settings.region
        self.access_key_id = aws_settings.access_key_id
        self.secret_access_key = aws_settings.secret_access_key

        self.aws_config = {
            'endpoint_url': self.endpoint_url,
            'region_name': self.region,
            'aws_access_key_id': self.access_key_id,
            'aws_secret_access_key': self.secret_access_key
        }

        self.is_localstack = bool(self.endpoint_url)

        self._session = None

    @property
    def session(self):
        """
        Get or create aioboto3 session.

        Returns:
            aioboto3.Session: Shared session instance for AWS operations.
        """
        if self._session is None:
            self._session = aioboto3.Session()
        return self._session

    @asynccontextmanager
    async def get_dynamodb_resource(self):
        """
        Async context manager for DynamoDB resource.

        Yields:
            DynamoDB resource: Configured DynamoDB resource for table operations.
        """
        async with self.session.resource('dynamodb', **self.aws_config) as resource:
            yield resource

    @asynccontextmanager
    async def get_s3_client(self):
        """
        Async context manager for S3 client.

        Yields:
            S3 client: Configured S3 client for bucket and object operations.
        """
        async with self.session.client('s3', **self.aws_config) as client:
            yield client

    @asynccontextmanager
    async def get_dynamodb_client(self):
        """
        Async context manager for DynamoDB client.

        Yields:
            DynamoDB client: Configured DynamoDB client for low-level operations.
        """
        async with self.session.client('dynamodb', **self.aws_config) as client:
            yield client


aws_client = AWSClient()
