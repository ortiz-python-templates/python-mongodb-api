from typing import Optional
from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.models.configurations.company_configuration_model import CompanyConfigurationModel
from src.core.shared.repositories.mongo_command_repository import MongoCommandRepository


class CompanyConfigurationCommandRepository(MongoCommandRepository[CompanyConfigurationModel]):
    
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "company_configurations", CompanyConfigurationModel)

    