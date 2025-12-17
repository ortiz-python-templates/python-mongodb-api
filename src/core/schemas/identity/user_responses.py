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
    file_url: Optional[str] = None
    size: Optional[int] = None
    content_type: Optional[str] = None
    description: Optional[str] = None
    uploaded_at: Optional[datetime] = None
    user: Optional[UserInfo] = None


    
    '''' {
    is_deleted: false,
    file_name: 'FT-Impressão-FTM 6HN2025_5.pdf',
    size: 17205,
    uploaded_at: ISODate('2025-12-17T18:00:57.676Z'),
    content_type: 'application/pdf',
    object_key: 'users/attachments/ee526dc9-a17e-493a-be1d-94f391e111a6_FT-Impressão-FTM 6HN2025_5.pdf',
    description: 'New File',
    user: {
      id: '7bc73e22-2b7e-4d86-b197-bafa573c65cc',
      email: 'admin.template@gmail.com',
      first_name: 'Super Admin',
      last_name: 'Master'
    },
    id: 'fdf209f9-8a16-4fbf-8d15-1e3da2344ce6',
    user_id: '7bc73e22-2b7e-4d86-b197-bafa573c65cc'
  }
'''