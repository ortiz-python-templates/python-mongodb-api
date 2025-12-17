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


class UserAttachmentDetail(BaseSchemaConfig):
    id: str
    user_id: Optional[str] = None
    file_name: Optional[str] = None
    size: Optional[int] = None
    content_type: Optional[str] = None
    description: Optional[str] = None
    uploaded_at: Optional[datetime] = None
    user: Optional[UserInfo] = None
