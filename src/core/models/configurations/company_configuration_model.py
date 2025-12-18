from typing import Optional
from src.core.shared.models.base_mongo_model import BaseMongoModel


class CompanyConfigurationModel(BaseMongoModel):
    name: str
    acronym: str
    email: str
    phone: str
    identification_number: Optional[str] = None
    address: Optional[str]
    