from typing import Optional
from src.core.models.base_mongo_model import BaseMongoModel


class BasicConfigurationModel(BaseMongoModel):
    app_name: str 
    app_acronym: str
    max_records_per_page: int
    max_admin_users: int
    max_super_admin_users: int
    