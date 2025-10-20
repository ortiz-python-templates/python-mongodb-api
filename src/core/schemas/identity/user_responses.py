from datetime import datetime
from typing import Optional
from pydantic import EmailStr, Field
from src.core.schemas.base_schema_config import BaseSchemaConfig


class UserDetail(BaseSchemaConfig):
    id: str
    email: Optional[str] = None
    role: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserInfo(BaseSchemaConfig):
    id: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None