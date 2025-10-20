from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.common.config.env_config import EnvConfig


class DbConfig:
    
    @classmethod
    def getdb_from_uri(cls, db_uri: str, db_name: str) -> AsyncIOMotorDatabase:
        client = AsyncIOMotorClient(db_uri)
        return client[db_name]
    
    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        return cls.getdb_from_uri(EnvConfig.MONGO_URI, EnvConfig.MONGO_DATABASE)
