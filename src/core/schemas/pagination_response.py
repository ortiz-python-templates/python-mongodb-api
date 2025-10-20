from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel
from fastapi import Query, Request
from src.core.schemas.base_schema_config import BaseSchemaConfig


T = TypeVar("T")

class PaginationMetadata(BaseSchemaConfig):
    page_index: int
    total_pages: int
    total_items: int
    first_page_url: Optional[str]
    last_page_url: Optional[str]
    previous_page_url: Optional[str]
    next_page_url: Optional[str]


class PaginationResponse(BaseModel, Generic[T]):
    items: List[T]
    metadata: PaginationMetadata

    @classmethod
    def create(cls, items: List[T], total_items: int, page_index: int, page_size: int, request: Request):
        total_pages = (total_items + page_size - 1) // page_size

        def build_url(index: int) -> Optional[str]:
            if 0 <= index < total_pages:
                return str(request.url.include_query_params(page_index=index, page_size=page_size))
            return None

        metadata = PaginationMetadata(
            page_index=page_index,
            total_items=total_items,
            total_pages=total_pages,
            first_page_url=build_url(0),
            last_page_url=build_url(total_pages - 1),
            previous_page_url=build_url(page_index - 1),
            next_page_url=build_url(page_index + 1)
        )
        return cls(items=items, metadata=metadata)

