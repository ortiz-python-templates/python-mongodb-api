from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.schemas.configurations.feature_flag_responses import FeatureFlagDetail
from src.core.repositories.shared.mongo_query_repository import MongoQueryRepository


class FeatureFlagQueryRepository(MongoQueryRepository[FeatureFlagDetail]):
    
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "view_feature_flag_detail", FeatureFlagDetail)


    async def get_by_name(self, flag_name: str):
        return await self.get_by_field("flag_name", flag_name)