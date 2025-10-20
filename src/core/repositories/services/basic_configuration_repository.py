from typing import Optional
from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.models.configuration.basic_configuration_model import BasicConfigurationModel
from src.core.repositories.shared.mongo_command_repository import MongoCommandRepository


class BasicConfigurationRepository(MongoCommandRepository[BasicConfigurationModel]):
    
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "basic_configurations", BasicConfigurationModel)

    async def get_last(self) -> Optional[BasicConfigurationModel]:
        doc = await self._collection.find_one(sort=[("_id", -1)])
        return self._model_cls.model_validate(doc) if doc else None

    async def get_first(self) -> Optional[BasicConfigurationModel]:
        doc = await self._collection.find_one(sort=[("_id", 1)])
        return self._model_cls.model_validate(doc) if doc else None

    