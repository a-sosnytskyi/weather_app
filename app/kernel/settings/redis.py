from pydantic import Field
from pydantic_settings import BaseSettings


class SettingsRedis(BaseSettings):
    """
    Redis connection configuration settings.

    Attributes:
        host: Redis server hostname or IP address.
        password: Redis server authentication password.
        port: Redis server port (default: 6379).
        db: Redis database number (default: 0).
        max_connections: Maximum connections in connection pool (default: 20).
    """
    host: str = Field(default=None, validation_alias="REDIS_HOST")
    password: str = Field(default=None, validation_alias="REDIS_PASSWORD")
    port: int = Field(default=6379, validation_alias="REDIS_PORT")
    db: int = Field(default=0, validation_alias="REDIS_DB")
    max_connections: int = Field(default=20, validation_alias="REDIS_MAX_CONNECTIONS")


redis_settings = SettingsRedis()
