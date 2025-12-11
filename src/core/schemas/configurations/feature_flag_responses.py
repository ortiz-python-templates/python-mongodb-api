from typing import Optional
from datetime import datetime
from src.core.schemas.base_schema_config import BaseSchemaConfig


class FeatureFlagDetail(BaseSchemaConfig):
    id: str
    flag_name: Optional[str] = None
    description: Optional[str] = None
    is_enabled: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None