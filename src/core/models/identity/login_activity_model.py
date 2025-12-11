from datetime import datetime
from typing import Optional
from bson import ObjectId
from src.core.models.identity.enums import ActivityStatus
from src.core.models.base_mongo_model import BaseMongoModel


class LoginActivityModel(BaseMongoModel):
    user_id: ObjectId
    status: ActivityStatus
    host: str
    browser: str
    ip_address: str
    device: Optional[str] = None
    location: Optional[str] = None
    last_login: Optional[datetime] = None
    last_logout: Optional[datetime] = None
    total_login: int
    total_logout: int
