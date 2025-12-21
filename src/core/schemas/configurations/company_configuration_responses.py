from typing import Optional
from datetime import datetime, timezone
from src.core.shared.schemas.base_schema_config import BaseSchemaConfig


class CompanyConfigurationDetail(BaseSchemaConfig):
    id: str
    name: Optional[str] = None
    acronym: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    identification_number: Optional[str] = None
    address: Optional[str] = None
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None