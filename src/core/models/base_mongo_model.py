from typing import Any, Optional
from uuid import uuid4
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, field_validator
from src.common.utils.encryption_util import EncryptionUtil


class BaseMongoModel(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    unique_id: str = Field(default_factory=lambda: EncryptionUtil.generate_uuid())
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True,
        "validate_assignment": True,
        "extra": "ignore"
    }
