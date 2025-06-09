from typing import Optional

from aiocache import Cache
import redis.asyncio as redis

from app.kernel.settings import redis_settings


class RedisCacheManager:
    """
    Redis cache manager with connection pooling and lifecycle management.

    Provides singleton-style Redis connections with proper initialization,
    cleanup, and connection testing for both raw Redis and AIOCache instances.
    """

    _redis_pool: Optional[redis.ConnectionPool] = None
    _aiocache_instance: Optional[Cache] = None
    _initialized: bool = False

    @classmethod
    async def initialize(cls):
        """
        Initialize Redis connection pool and AIOCache instance.

        Creates connection pool, configures AIOCache, and tests connectivity.
        Safe to call multiple times - will skip if already initialized.

        Raises:
            ConnectionError: If Redis connection test fails.
        """
        if cls._initialized:
            return

        # Redis connection pool
        cls._redis_pool = redis.ConnectionPool(
            host=redis_settings.host,
            password=redis_settings.password,
            port=redis_settings.port,
            db=redis_settings.db,
            decode_responses=True,
            max_connections=redis_settings.max_connections)

        # AIOCache instance
        cls._aiocache_instance = Cache(
            Cache.REDIS,
            endpoint=redis_settings.host,
            password=redis_settings.password,
            port=redis_settings.port,
            db=redis_settings.db)

        # Test connections
        redis_client = redis.Redis(connection_pool=cls._redis_pool)
        await redis_client.ping()
        await cls._aiocache_instance.set("test", "ok", ttl=10)

        cls._initialized = True

    @classmethod
    async def cleanup(cls):
        """
        Clean up Redis connections and reset initialization state.

        Properly disconnects connection pool and clears all instances.
        """

        if cls._redis_pool:
            await cls._redis_pool.disconnect()

        cls._redis_pool = None
        cls._aiocache_instance = None
        cls._initialized = False

    @classmethod
    def get_redis_client(cls) -> redis.Redis:
        """
        Get Redis client with connection pooling.

        Returns:
            redis.Redis: Redis client instance using shared connection pool.

        Raises:
            RuntimeError: If cache manager not initialized.
        """
        if not cls._initialized:
            raise RuntimeError("Cache not initialized")
        return redis.Redis(connection_pool=cls._redis_pool)

    @classmethod
    def get_aiocache(cls) -> Cache:
        """
        Get AIOCache instance for Redis.

        Returns:
            Cache: Configured AIOCache instance for Redis operations.

        Raises:
            RuntimeError: If cache manager not initialized.
        """
        if not cls._initialized:
            raise RuntimeError("Cache not initialized")
        return cls._aiocache_instance
