from typing import Optional
from pydantic import EmailStr, Field
from src.core.schemas.base_schema_config import BaseSchemaConfig


class CreateUserRequest(BaseSchemaConfig):
    email: EmailStr = Field(..., description="A valid email is required")
    role: Optional[str] = Field(None, min_length=1, description="User role or profile")
    first_name: Optional[str] = Field(None, min_length=1, description="User first name")
    last_name: Optional[str] = Field(None, description="User last name")
    password: str = Field(..., min_length=8, description="Password")


class UpdateUserRequest(BaseSchemaConfig):
    first_name: Optional[str] = Field(None, min_length=1, description="User first name")
    last_name: Optional[str] = Field(None, min_length=1, description="User last name")


class RegisterUserRequest(BaseSchemaConfig):
    email: EmailStr = Field(..., description="A valid email is required")
    first_name: Optional[str] = Field(None, min_length=1, description="User first name")
    last_name: Optional[str] = Field(None, min_length=1, description="User last name")
    password: str = Field(..., min_length=8, description="Password")


class ActivateUserRequest(BaseSchemaConfig):
    reason: Optional[str] = Field(None, min_length=1, description="Reason for activation")


class DeactivateUserRequest(BaseSchemaConfig):
    reason: Optional[str] = Field(None, min_length=1, description="Reason for deactivation")


class PasswordRecoveryRequest(BaseSchemaConfig):
    email: EmailStr = Field(..., description="User email for password recovery")


class ChangePasswordRequest(BaseSchemaConfig):
    new_password: str = Field(..., min_length=6, description="New user password")
    password_confirmation: str = Field(..., min_length=6, description="Password Confirmation")


class CreateUserAttachmentRequest(BaseSchemaConfig):
    user_id: str = Field(...,  description="User ID")
    description: Optional[str] = Field(..., description="Attachment Description")
