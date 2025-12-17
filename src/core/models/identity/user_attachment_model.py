from datetime import datetime
from typing import Optional
from bson import ObjectId
from src.core.models.base_mongo_model import BaseMongoModel


class UserAttachmentModel(BaseMongoModel):
    user_id: ObjectId
    file_name: str
    size: int
    uploaded_at: datetime
    content_type: str
    object_key: str
    description: Optional[str] = None
    metadata: Optional[dict] = None

    