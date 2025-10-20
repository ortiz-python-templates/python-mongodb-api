from typing import Optional
from bson import ObjectId
from pydantic import EmailStr, Field
from src.core.models.base_mongo_model import BaseMongoModel


class UserModel(BaseMongoModel):
    email: EmailStr
    role: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str
    is_active: bool
    recovery_token: Optional[str] = None
