from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.schemas.configurations.company_configuration_responses import CompanyConfigurationDetail
from src.core.shared.repositories.mongo_query_repository import MongoQueryRepository


class CompanyConfigurationQueryRepository(MongoQueryRepository[CompanyConfigurationDetail]):
    
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "view_company_configuration_detail", CompanyConfigurationDetail)

    