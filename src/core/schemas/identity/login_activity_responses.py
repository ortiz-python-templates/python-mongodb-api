from datetime import datetime
from typing import Optional
from src.core.models.identity.enums import ActivityStatus
from src.core.shared.schemas.base_schema_config import BaseSchemaConfig
from src.core.schemas.identity.user_responses import UserInfo


class DeviceInfo(BaseSchemaConfig):
    type: Optional[str] = None        # desktop, mobile, tablet
    brand: Optional[str] = None
    model: Optional[str] = None
    is_mobile: Optional[bool] = None
    is_tablet: Optional[bool] = None
    is_pc: Optional[bool] = None


class OSInfo(BaseSchemaConfig):
    name: Optional[str] = None       # Windows, Linux, MacOS, Android
    version: Optional[str] = None


class LocationInfo(BaseSchemaConfig):
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class BrowserInfo(BaseSchemaConfig):
    name: Optional[str] = None       # Chrome, Firefox, Safari
    version: Optional[str] = None


class LoginActivityDetail(BaseSchemaConfig):
    id: str
    user_id: Optional[str] = None
    status: Optional[ActivityStatus] = None

    host: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent_raw: Optional[str] = None

    last_login: Optional[datetime] = None
    last_logout: Optional[datetime] = None
    total_login: Optional[int] = None
    total_logout: Optional[int] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_deleted: Optional[bool] = None

    client: Optional[BrowserInfo] = None
    os: Optional[OSInfo] = None
    device: Optional[DeviceInfo] = None
    location: Optional[LocationInfo] = None
    user: Optional[UserInfo] = None


class LoginActivitySimple(BaseSchemaConfig):
    id: str
    user_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: Optional[ActivityStatus] = None
    last_login: Optional[datetime] = None
    total_login: Optional[int] = None


