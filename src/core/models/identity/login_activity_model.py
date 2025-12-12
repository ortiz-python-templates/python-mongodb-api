from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel
from src.core.models.identity.enums import ActivityStatus
from src.core.models.base_mongo_model import BaseMongoModel


class DeviceInfo(BaseModel):
    type: Optional[str] = None        # desktop, mobile, tablet
    brand: Optional[str] = None
    model: Optional[str] = None
    is_mobile: Optional[bool] = None
    is_tablet: Optional[bool] = None
    is_pc: Optional[bool] = None

class OSInfo(BaseModel):
    name: Optional[str] = None       # Windows, Linux, MacOS, Android
    version: Optional[str] = None

class LocationInfo(BaseModel):
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class BrowserInfo(BaseModel):
    name: Optional[str] = None       # Chrome, Firefox, Safari
    version: Optional[str] = None

class LoginActivityModel(BaseMongoModel):
    user_id: ObjectId
    status: ActivityStatus

    client: BrowserInfo
    os: OSInfo
    device: DeviceInfo

    host: str
    ip_address: str
    location: Optional[LocationInfo] = None

    user_agent_raw: str

    last_login: Optional[datetime] = None
    last_logout: Optional[datetime] = None
    total_login: int
    total_logout: int

