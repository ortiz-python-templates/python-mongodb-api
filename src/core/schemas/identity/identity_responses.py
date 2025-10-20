from src.core.schemas.base_schema_config import BaseSchemaConfig


class LoginResponse(BaseSchemaConfig):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenResponse(BaseSchemaConfig):
    access_token: str
    token_type: str = "bearer"