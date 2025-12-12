from typing import Optional
from pydantic import BaseModel, Field


class ManageFeatureFlagRequest(BaseModel):
    flag_name: str = Field(..., min_length=1, description="Feature flag name")
    description: Optional[str] = Field(None, description="Feature flag description")
    is_enabled: Optional[bool] = Field(False, description="Indicates if the feature is enabled")
