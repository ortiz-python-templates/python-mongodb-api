from typing import Optional
from src.core.models.base_mongo_model import BaseMongoModel


class CompanyConfigurationModel(BaseMongoModel):
    name: str
    acronym: str
    ident_number: str
    email: str
    phone: str
    address: Optional[str]
    