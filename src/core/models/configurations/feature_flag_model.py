from typing import Optional
from src.core.models.base_mongo_model import BaseMongoModel


class FeatureFlagModel(BaseMongoModel):
    flag_name: str
    description: Optional[str] = None
    is_enabled: bool
    