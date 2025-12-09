from typing import Optional
from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.models.configurations.feature_flag_model import FeatureFlagModel
from src.core.repositories.shared.mongo_command_repository import MongoCommandRepository


class FeatureFlagCommandRepository(MongoCommandRepository[FeatureFlagModel]):
    
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "feature_flags", FeatureFlagModel)

    async def ensure_indexes(self):
        await self._collection.create_index([("flag_name", ASCENDING)], name="idx_user_email")