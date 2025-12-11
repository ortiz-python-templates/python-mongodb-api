from datetime import datetime
from typing import Optional
from core.models.identity.enums import ActivityStatus
from src.core.schemas.base_schema_config import BaseSchemaConfig
from src.core.schemas.identity.user_responses import UserInfo


class LoginActivityDetail(BaseSchemaConfig):
    id: str
    user_id: Optional[str] = None
    status: Optional[ActivityStatus] = None
    host: Optional[str] = None
    browser: Optional[str] = None
    ip_address: Optional[str] = None
    device: Optional[str] = None
    location: Optional[str] = None
    user_agent: Optional[str] = None
    last_login: Optional[datetime] = None
    last_logout: Optional[datetime] = None
    total_login: Optional[int] = None
    total_logout: Optional[int] = None
    is_deleted: Optional[bool] = None
    user: Optional[UserInfo] = None