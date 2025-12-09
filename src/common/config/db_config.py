from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from src.common.config.env_config import EnvConfig

class DbConfig:
    _client: AsyncIOMotorClient | None = None
    _db: AsyncIOMotorDatabase | None = None

    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        if cls._db is None:
            cls._client = AsyncIOMotorClient(EnvConfig.MONGO_URI)
            cls._db = cls._client[EnvConfig.MONGO_DATABASE]
        return cls._db
