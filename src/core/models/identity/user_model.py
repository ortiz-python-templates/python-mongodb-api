from typing import Optional
from pydantic import EmailStr, Field
from src.core.models.identity.role import Role
from src.core.models.base_mongo_model import BaseMongoModel


class UserModel(BaseMongoModel):
    email: EmailStr
    role: Optional[Role] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str
    is_active: bool
    avatar_url: Optional[str] = None
    recovery_token: Optional[str] = None
    