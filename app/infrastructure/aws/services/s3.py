from typing import Dict, Optional, List, Tuple
from botocore.exceptions import ClientError

from ..client import aws_client


class S3Service:
    """Minimal service for working with S3 operations."""

    async def create_bucket(self, bucket_name: str) -> bool:
        """
        Create S3 bucket with region-specific configuration.

        Handles different bucket creation logic for LocalStack vs AWS,
        and region-specific constraints for non-us-east-1 regions.

        Args:
            bucket_name: Name of the bucket to create.

        Returns:
            bool: True if bucket created or already exists.

        Raises:
            ClientError: For S3 operation errors (except BucketAlreadyOwnedByYou).
        """
        async with aws_client.get_s3_client() as s3:
            try:
                if aws_client.is_localstack:
                    await s3.create_bucket(Bucket=bucket_name)
                else:
                    if aws_client.region != 'us-east-1':
                        await s3.create_bucket(
                            Bucket=bucket_name,
                            CreateBucketConfiguration={'LocationConstraint': aws_client.region}
                        )
                    else:
                        await s3.create_bucket(Bucket=bucket_name)
                return True

            except ClientError as ex:
                error_code = ex.response['Error']['Code']
                if error_code in ["BucketAlreadyOwnedByYou"]:
                    return True
                raise

    async def put_object(
            self, bucket_name: str, key: str,
            body: bytes, content_type: Optional[str] = None
    ) -> bool:
        """
        Upload object to S3 bucket.

        Args:
            bucket_name: Target S3 bucket name.
            key: Object key (file path) in the bucket.
            body: File content as bytes.
            content_type: MIME type of the content (optional).

        Returns:
            bool: True if upload successful.

        Raises:
            Exception: For S3 upload errors.
        """
        async with aws_client.get_s3_client() as s3:
            try:
                params = {
                    'Bucket': bucket_name,
                    'Key': key,
                    'Body': body
                }
                if content_type:
                    params['ContentType'] = content_type

                await s3.put_object(**params)
                return True

            except Exception:
                raise

    async def get_object_content(self, bucket_name: str, key: str) -> Optional[Tuple[bytes, Dict]]:
        """
        Get object content from S3 bucket.

        Args:
            bucket_name: Source S3 bucket name.
            key: Object key (file path) in the bucket.

        Returns:
            Optional[bytes]: File content if found, None if object doesn't exist.

        Raises:
            ClientError: For S3 operation errors (except NoSuchKey/NoSuchBucket).
        """
        async with aws_client.get_s3_client() as s3:
            try:
                response = await s3.get_object(Bucket=bucket_name, Key=key)
                # Read the content
                return await response['Body'].read()

            except ClientError as ex:
                error_code = ex.response['Error']['Code']
                if error_code in ("NoSuchKey", "NoSuchBucket"):
                    return None
                raise

    async def list_buckets(self) -> List[Dict[str, str]]:
        """
        List all S3 buckets in the account.

        Returns:
            List[Dict[str, str]]: List of bucket info with name and creation_date.
                                 Returns empty list if operation fails.
        """
        async with aws_client.get_s3_client() as s3:
            try:
                response = await s3.list_buckets()
                buckets = []
                for bucket in response.get('Buckets', []):
                    buckets.append({
                        'name': bucket['Name'],
                        'creation_date': bucket['CreationDate'].isoformat() if bucket.get('CreationDate') else None
                    })
                return buckets
            except Exception:
                return []


s3_service = S3Service()
