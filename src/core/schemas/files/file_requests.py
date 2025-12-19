from typing import Optional
from pydantic import Field
from src.core.models.files.enums import FileOwnerEntity
from src.core.shared.schemas.base_schema_config import BaseSchemaConfig


class UploadFileRequest(BaseSchemaConfig):
    description: Optional[str] = Field(None, description="A brief description of the file's content or purpose")
    owner_entity: Optional[FileOwnerEntity] = Field(None, description="The name of the related entity or collection (e.g., 'users', 'companies', 'products')")
    owner_id: Optional[str] = Field(None, description="The unique identifier (UUID/ObjectId) of the entity that owns this file")
    is_public: bool = Field(default=False, description="If true, the file can be accessed via a direct link without authentication")