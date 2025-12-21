from datetime import datetime, timezone
from typing import Optional, Dict
from bson import ObjectId
from pydantic import Field
from src.common.storage.storage_provider import StorageProvider
from src.core.models.files.enums import FileOwnerEntity, FileVisibility
from src.core.shared.models.base_mongo_model import BaseMongoModel


class FileModel(BaseMongoModel):
    # Identity
    file_name: str
    size: int  # bytes
    content_type: str

    category: str

    # Storage
    storage_provider: StorageProvider
    object_key: str
    bucket_name: Optional[str] = None

    # Access & visibility
    visibility: FileVisibility = FileVisibility.PRIVATE
    can_preview: bool = False

    # Lifecycle
    uploaded_at: datetime = Field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None

    # Integrity
    checksum: Optional[str] = None
    checksum_algorithm: Optional[str] = "sha256"

    # Ownership / domain
    owner_id: Optional[str] = None
    owner_entity: Optional[FileOwnerEntity] = None

    # Optional info
    display_name: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict] = None
