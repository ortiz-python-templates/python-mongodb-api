from datetime import datetime
from typing import Optional
from src.core.shared.schemas.base_schema_config import BaseSchemaConfig


class FileDetail(BaseSchemaConfig):
    file_name: str
    size: int
    content_type: str

    object_key: str
    bucket_name: Optional[str] = None

    storage_provider: Optional[str] = None
    is_public: bool = False

    uploaded_at: datetime
    expires_at: Optional[datetime] = None

    checksum: Optional[str] = None

    owner_id: Optional[str] = None
    owner_entity: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[dict] = None