import base64
from bson import ObjectId
from pydantic import BaseModel
from src.common.utils.string_util import StringUtil


class BaseSchemaConfig(BaseModel):
    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
        "alias_generator": StringUtil.to_camel_case,
        "json_encoders": {
            ObjectId: str
        }
    }
