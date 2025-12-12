from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UpdateCompanyConfigurationRequest(BaseModel):
    name: str = Field(..., min_length=1, description="Company name is required")
    acronym: Optional[str] = Field(None, min_length=1, description="Short acronym for the company")
    email: Optional[EmailStr] = Field(None, description="Company contact email")
    phone: Optional[str] = Field(None, description="Company contact phone")
    identification_number: Optional[str] = Field(None, description="Company identification number (tax ID, etc.)")
    address: Optional[str] = Field(None, description="Company address")
