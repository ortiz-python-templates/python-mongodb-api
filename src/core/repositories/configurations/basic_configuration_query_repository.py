from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.schemas.configurations.basic_configuration_responses import BasicConfigurationDetail
from src.core.shared.repositories.mongo_query_repository import MongoQueryRepository


class BasicConfigurationQueryRepository(MongoQueryRepository[BasicConfigurationDetail]):
    
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "view_basic_configuration_detail", BasicConfigurationDetail)

    