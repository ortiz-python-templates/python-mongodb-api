from typing import Optional
from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.models.configurations.feature_flag_model import FeatureFlagModel
from src.core.shared.repositories.mongo_command_repository import MongoCommandRepository


class FeatureFlagCommandRepository(MongoCommandRepository[FeatureFlagModel]):
    
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "feature_flags", FeatureFlagModel)

    async def ensure_indexes(self):
        await self.collection.create_index([("flag_name", ASCENDING)], name="idx_feature_flag_name")

    async def get_by_name_aux(self, flag_name: str):
        return await self.get_by_field_aux("flag_name", flag_name)