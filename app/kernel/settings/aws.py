from pydantic import Field
from pydantic_settings import BaseSettings


class SettingsAws(BaseSettings):
    """
    AWS configuration settings from environment variables.

    Attributes:
        endpoint_url: AWS service endpoint URL (for LocalStack support).
        region: AWS region for service operations.
        secret_access_key: AWS secret access key for authentication.
        access_key_id: AWS access key ID for authentication.
    """
    endpoint_url: str = Field(default=None, validation_alias="AWS_ENDPOINT_URL")
    region: str = Field(default=None, validation_alias="AWS_REGION")
    secret_access_key: str = Field(default=None, validation_alias="AWS_SECRET_ACCESS_KEY")
    access_key_id: str = Field(default=None, validation_alias="AWS_ACCESS_KEY_ID")


aws_settings = SettingsAws()
