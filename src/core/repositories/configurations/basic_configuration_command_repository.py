from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.models.configurations.basic_configuration_model import BasicConfigurationModel
from src.core.shared.repositories.mongo_command_repository import MongoCommandRepository


class BasicConfigurationCommandRepository(MongoCommandRepository[BasicConfigurationModel]):
    
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "basic_configurations", BasicConfigurationModel)