from datetime import datetime
from typing import Optional
from src.core.shared.schemas.base_schema_config import BaseSchemaConfig


class FileDetail(BaseSchemaConfig):
    # Identity
    id: str

    # File info
    file_name: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None

    category: Optional[str] = None

    # Storage info (safe)
    object_key: Optional[str] = None
    storage_provider: Optional[str] = None

    # Access
    preview_url: Optional[str] = None
    download_url: Optional[str] = None
    can_preview: Optional[bool] = None

    # Visibility
    visibility: Optional[str] = None

    # Integrity
    checksum: Optional[str] = None

    # Ownership
    owner_id: Optional[str] = None
    owner_entity: Optional[str] = None

    # Lifecycle
    uploaded_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    # Optional
    display_name: Optional[str] = None
    description: Optional[str] = None
