from typing import Optional
from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.models.configuration.company_configuration_model import CompanyConfigurationModel
from src.core.repositories.shared.mongo_command_repository import MongoCommandRepository


class CompanyConfigurationRepository(MongoCommandRepository[CompanyConfigurationModel]):
    
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "company_configurations", CompanyConfigurationModel)

    async def get_last(self) -> Optional[CompanyConfigurationModel]:
        doc = await self._collection.find_one(sort=[("_id", -1)])
        return self._model_cls.model_validate(doc) if doc else None

    async def get_first(self) -> Optional[CompanyConfigurationModel]:
        doc = await self._collection.find_one(sort=[("_id", 1)])
        return self._model_cls.model_validate(doc) if doc else None

    