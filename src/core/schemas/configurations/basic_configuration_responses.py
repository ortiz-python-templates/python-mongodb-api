from typing import Optional
from datetime import datetime, timezone
from src.core.shared.schemas.base_schema_config import BaseSchemaConfig


class BasicConfigurationDetail(BaseSchemaConfig):
    id: str
    app_name: Optional[str] = None
    app_acronym: Optional[str] = None
    max_records_per_page: Optional[int] = None
    max_admin_users: Optional[int] = None
    max_super_admin_users: Optional[int] = None
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None