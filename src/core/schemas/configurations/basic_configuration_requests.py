from typing import Optional
from pydantic import BaseModel, Field


class UpdateBasicConfigurationRequest(BaseModel):
    app_name: str = Field(..., min_length=1, description="Application name is required")
    app_acronym: Optional[str] = Field(None, min_length=1, description="Application short name or acronym")
    max_records_per_page: Optional[int] = Field(None, ge=1, description="Maximum number of records per page")
    max_admin_users: Optional[int] = Field(None, ge=1, description="Maximum number of admin users allowed")
    max_super_admin_users: Optional[int] = Field(None, ge=1, description="Maximum number of super admin users allowed")
