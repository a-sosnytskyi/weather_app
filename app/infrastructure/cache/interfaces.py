import json
from typing import Literal, Optional, Any

from aiocache import Cache

from app.kernel.logs import logger
from .redis_cache import RedisCacheManager


class CacheManager:
    """
    Universal cache manager with automatic serialization.

    Provides abstraction layer over different cache backends
    with JSON serialization and error handling.
    """

    def __init__(self, engine: Literal["redis"] = "redis"):
        self.engine = engine

    @property
    def _cache(self) -> Cache:
        """
        Get cache instance based on configured engine.

        Returns:
            Cache: Configured aiocache instance.
        """
        if self.engine == "redis":
            return RedisCacheManager.get_aiocache()
        else:
            # default
            return RedisCacheManager.get_aiocache()

    def _serialize_value(self, value: Any) -> Any:
        """
        Serialize value for cache storage.

        Handles primitives directly, converts complex objects to JSON.
        Falls back to string conversion for non-serializable objects.

        Args:
            value: Value to serialize.

        Returns:
            Any: Serialized value ready for cache storage.
        """
        if value is None:
            return None

        if isinstance(value, (str, int, float, bool)):
            return value

        try:
            return json.dumps(value, ensure_ascii=False, default=str)
        except (TypeError, ValueError) as e:
            return str(value)

    def _deserialize_value(self, value: Any) -> Any:
        """
        Deserialize value from cache storage.

        Attempts JSON parsing for string values, returns others as-is.

        Args:
            value: Value retrieved from cache.

        Returns:
            Any: Deserialized original value.
        """
        if value is None:
            return None

        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value

        return value

    async def get(self, key: str) -> Optional[Any]:
        """
        Retrieve value from cache by key.

        Args:
            key: Cache key to retrieve.

        Returns:
            Optional[Any]: Cached value if found, None otherwise.
        """
        try:
            value = await self._cache.get(key)
            return self._deserialize_value(value)
        except Exception as e:
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Store value in cache with optional TTL.

        Args:
            key: Cache key for storage.
            value: Value to cache.
            ttl: Time to live in seconds (optional).

        Returns:
            bool: True if stored successfully, False otherwise.
        """
        try:
            serialized_value = self._serialize_value(value)
            await self._cache.set(key, serialized_value, ttl=ttl)
            logger.debug(f"Set value to cache. Key: {key}. Engine: {self.engine}. TTL: {ttl}")
            return True
        except Exception:
            return False

    async def delete(self, key: str) -> bool:
        """
        Delete value from cache by key.

        Args:
            key: Cache key to delete.

        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        try:
            result = await self._cache.delete(key)
            logger.debug(f"Removed value from cache. Key: {key}. Engine: {self.engine}.")
            return bool(result)
        except Exception as e:
            return False

    async def exists(self, key: str) -> bool:
        """
        Check if key exists in cache.

        Args:
            key: Cache key to check.

        Returns:
            bool: True if key exists, False otherwise.
        """
        try:
            return await self._cache.exists(key)
        except Exception as e:
            return False
