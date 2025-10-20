from typing import Optional
from pydantic import EmailStr, Field
from src.core.schemas.base_schema_config import BaseSchemaConfig


class LoginRequest(BaseSchemaConfig):
    email: EmailStr = Field(..., description="A valid email is required")
    password: str = Field(..., min_length=8, description="Password")


class RefreshTokenRequest(BaseSchemaConfig):
    refresh_token: str = Field(..., description="Token for refresh")
