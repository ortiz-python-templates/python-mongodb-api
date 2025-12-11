import time
from src.common.config.db_config import DbConfig
from src.common.config.redis_client import RedisClient


class HealthService:

    @staticmethod
    async def mongo_health():
        start = time.time()
        try:
            db = DbConfig.get_database()
            await db.command("ping")
            return {"status": "up", "latency_ms": round((time.time() - start) * 1000, 2)}
        except Exception:
            return {"status": "down"}


    @staticmethod
    async def redis_health():
        start = time.time()
        try:
            await RedisClient._redis.ping()
            return {"status": "up", "latency_ms": round((time.time() - start) * 1000, 2)}
        except Exception:
            return {"status": "down"}
