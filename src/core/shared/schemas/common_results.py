from src.core.shared.schemas.base_schema_config import BaseSchemaConfig


class CreatedResult(BaseSchemaConfig):
    id: str
    message: str


class UpdatedResult(BaseSchemaConfig):
    id: str
    message: str