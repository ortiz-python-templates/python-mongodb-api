from datetime import datetime
from typing import Optional

from bson import ObjectId
from src.common.storage.storage_target import StorageProvider
from src.core.shared.models.base_mongo_model import BaseMongoModel


class FileModel(BaseMongoModel):
    file_name: str
    size: int
    content_type: str

    object_key: str
    bucket_name: Optional[str] = None

    storage_provider: StorageProvider = StorageProvider.MINIO

    is_public: bool = False

    uploaded_at: datetime
    expires_at: Optional[datetime] = None

    checksum: Optional[str] = None

    owner_id: Optional[ObjectId] = None
    owner_entity: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[dict] = None
