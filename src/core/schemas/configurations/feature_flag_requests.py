from pydantic import BaseModel, Field
from src.core.shared.schemas.base_schema_config import BaseSchemaConfig


class ManageFeatureFlagRequest(BaseSchemaConfig):
    flag_name: str = Field(..., min_length=1, description="Feature flag name")
    is_enabled: bool = Field(False, description="Indicates if the feature is enabled")
