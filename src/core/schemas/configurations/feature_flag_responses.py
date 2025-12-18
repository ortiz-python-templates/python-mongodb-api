from typing import Optional
from datetime import datetime
from src.core.shared.schemas.base_schema_config import BaseSchemaConfig


class FeatureFlagDetail(BaseSchemaConfig):
    id: Optional[str] = None
    flag_name: Optional[str] = None
    description: Optional[str] = None
    is_enabled: Optional[bool] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None
    is_deleted: Optional[bool] = None