import redis.asyncio as redis
from src.common.config.env_config import EnvConfig


class RedisClient:
    _redis = None

    @classmethod
    async def init(cls):
        if cls._redis is None:
            cls._redis = redis.from_url(url=EnvConfig.REDIS_URL, decode_responses=True)

    @classmethod
    async def setex(cls, key: str, ttl: int, value: str):
        await cls.init()
        await cls._redis.setex(key, ttl, value)

    @classmethod
    async def get(cls, key: str):
        await cls.init()
        return await cls._redis.get(key)

    @classmethod
    async def exists(cls, key: str) -> bool:
        await cls.init()
        return await cls._redis.exists(key) == 1
    
    @classmethod
    async def expire(cls, key: str, ttl: int):
        await cls.init()
        await cls._redis.expire(key, ttl)

    @classmethod
    async def incr(cls, key: str) -> int:
        await cls.init()
        return await cls._redis.incr(key)


