from typing import Optional
from pydantic import Field
from src.core.models.files.enums import FileOwnerEntity, FileVisibility
from src.core.shared.schemas.base_schema_config import BaseSchemaConfig


class UploadFileRequest(BaseSchemaConfig):
    category: str = Field(None, description="Logical category of the file (e.g. avatar, document, invoice, attachment)")
    owner_entity: Optional[FileOwnerEntity] = Field(None, description="The name of the related entity or collection (e.g., 'users', 'companies', 'products')")
    owner_id: Optional[str] = Field(None, description="The unique identifier (UUID/ObjectId) of the entity that owns this file")
    display_name: Optional[str] = Field(None, description="Optional human-readable name for the file")
    description: Optional[str] = Field(None, description="A brief description of the file's content or purpose")
    visibility: FileVisibility = Field(default=FileVisibility.PRIVATE, description="Controls who can access the file")
