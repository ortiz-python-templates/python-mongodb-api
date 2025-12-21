from datetime import datetime, timezone, timedelta
from typing import Dict, TypeVar, Generic, List, Optional, Type, Any, Union
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from src.core.shared.filters.date_range_filter import DateRangeFilter
from src.core.shared.filters.search_filter import SearchFilter
from src.core.shared.filters.pagination_filter import PaginationFilter


T = TypeVar('T', bound=BaseModel)

class MongoQueryRepository(Generic[T]):

    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str, model_cls: Type[T]):
        self.collection: AsyncIOMotorCollection = db[collection_name]
        self.model_cls = model_cls
        self.db = db
   
    # Get all
    async def get_all(self, search_filter: Optional[SearchFilter], pagination_filter: Optional[PaginationFilter]) -> List[T]:
        page_size, page_index = self._normalize_pagination(pagination_filter.page_size, pagination_filter.page_index)
        filters = [{"is_deleted": False}]
        if search_filter and search_filter.search_param:
            filters.append(self._build_search_query(search_filter.search_param))
        query = {"$and": filters} if len(filters) > 1 else filters[0]
        sort_direction = -1 if search_filter.sort_order == "desc" else 1
        cursor = self.collection.find(query).sort("created_at", sort_direction).skip(page_index * page_size).limit(page_size)
        docs = await cursor.to_list(length=page_size)
        return [self.model_cls.model_validate(doc) for doc in docs]
    
    async def get_all_by_field(self, field_name: str, field_value: Any, search_filter: Optional[SearchFilter], pagination_filter: Optional[PaginationFilter]) -> List[T]:
        page_size, page_index = self._normalize_pagination(pagination_filter.page_size, pagination_filter.page_index)
        filters = [{"is_deleted": False, **{field_name: field_value}}]
        if search_filter and search_filter.search_param:
            filters.append(self._build_search_query(search_filter.search_param))
        query = {"$and": filters} if len(filters) > 1 else filters[0]
        sort_direction = -1 if search_filter.sort_order == "desc" else 1
        cursor = self.collection.find(query).sort("created_at", sort_direction).skip(page_index * page_size).limit(page_size)
        docs = await cursor.to_list(length=page_size)
        return [self.model_cls.model_validate(doc) for doc in docs]
    
    async def get_all_not_paginated(self) -> List[T]:
        cursor = self.collection.find({"is_deleted": False})
        docs = await cursor.to_list(length=None)
        return [self.model_cls.model_validate(doc) for doc in docs]

    async def get_all_in(self, field: str, values: List[Any]) -> List[T]:
        cursor = self.collection.find({field: {"$in": values}, "is_deleted": False})
        docs = await cursor.to_list(length=None)
        return [self.model_cls.model_validate(doc) for doc in docs]

   
    # Get one
    async def get_by_field_v1(self, field: str, value: Any) -> Optional[T]:
        doc = await self.collection.find_one({field: value, "is_deleted": False})
        return self.model_cls.model_validate(doc) if doc else None
    
    async def get_by_field(self, field: str, value: Any) -> Optional[T]:
        filter = {
            field: value,
            "$or": [
                {"is_deleted": False},{"is_deleted": {"$exists": False}}
            ]
        }
        doc = await self.collection.find_one(filter)
        return self.model_cls.model_validate(doc) if doc else None


    async def get_by_id(self, id: str) -> Optional[T]:
        doc = await self.collection.find_one({'id': id, "is_deleted": False})
        return self.model_cls.model_validate(doc) if doc else None

    async def get_by_unique_id(self, unique_id: str) -> Optional[T]:
        doc = await self.collection.find_one({'unique_id': unique_id, "is_deleted": False})
        return self.model_cls.model_validate(doc) if doc else None

    async def get_last(self) -> Optional[T]:
        doc = await self.collection.find_one({"is_deleted": False}, sort=[("id", -1)])
        return self.model_cls.model_validate(doc) if doc else None

    async def get_first(self) -> Optional[T]:
        doc = await self.collection.find_one({"is_deleted": False}, sort=[("id", 1)])
        return self.model_cls.model_validate(doc) if doc else None
   

    # Pagination helper
    def _normalize_pagination(self, page_size: Optional[Union[int, str]], page_index: Optional[Union[int, str]]) -> tuple[int, int]:
        try:
            page_size = max(1, int(page_size or 10))
        except (ValueError, TypeError):
            page_size = 10

        try:
            page_index = max(0, int(page_index or 0))
        except (ValueError, TypeError):
            page_index = 0

        return page_size, page_index


    # Filters
    async def filter_by_date(self, status_field: Optional[str],  date_filter: DateRangeFilter, pagination_filter: PaginationFilter) -> List[T]:
        page_size, page_index = self._normalize_pagination(pagination_filter.page_size, pagination_filter.page_index)
        query = self._build_date_range_status_filter(status_field, date_filter)
        query["is_deleted"] = False
        cursor = self.collection.find(query).skip(page_index * page_size).limit(page_size)
        docs = await cursor.to_list(length=page_size)
        return [self.model_cls.model_validate(doc) for doc in docs]

    async def filter_by_date_range(self, date_filter: DateRangeFilter, pagination_filter: PaginationFilter) -> List[T]:
        page_size, page_index = self._normalize_pagination(pagination_filter.page_size, pagination_filter.page_index)
        query = self._build_date_range_filter(date_filter.start_date, date_filter.end_date)
        query["is_deleted"] = False
        cursor = self.collection.find(query).skip(page_index * page_size).limit(page_size)
        docs = await cursor.to_list(length=page_size)
        return [self.model_cls.model_validate(doc) for doc in docs]

    async def filter_by_date_range_status(self, status_field: Optional[str], status_value: Optional[str], date_filter: DateRangeFilter, pagination_filter: PaginationFilter) -> List[T]:
        page_size, page_index = self._normalize_pagination(pagination_filter.page_size, pagination_filter.page_index)
        query = self._build_date_range_status_filter(status_field, status_value, date_filter.start_date, date_filter.end_date)
        query["is_deleted"] = False
        cursor = self.collection.find(query).skip(page_index * page_size).limit(page_size)
        docs = await cursor.to_list(length=page_size)
        return [self.model_cls.model_validate(doc) for doc in docs]

   
    # Counts
    async def count_by_date_range_status_filter(self, status_field: Optional[str], status_value: str, date_filter: DateRangeFilter) -> int:
        query = self._build_date_range_status_filter(status_field, status_value, date_filter.start_date, date_filter.end_date)
        query["is_deleted"] = False
        return await self.collection.count_documents(query)

    async def count_by_date_filter(self, date_filter: DateRangeFilter) -> int:
        query = self._build_date_range_filter(date_filter.start_date, date_filter.end_date)
        query["is_deleted"] = False
        return await self.collection.count_documents(query)

    async def count_search(self, search_param: Optional[str]) -> int:
        query = self._build_search_query(search_param)
        query["is_deleted"] = False
        return await self.collection.count_documents(query)
    
    async def count_search_by_field(self, field_name: str, field_value: Any, search_param: Optional[str]) -> int:
        query = self._build_search_query(search_param)
        query["is_deleted"] = False
        query[field_name] = field_value
        return await self.collection.count_documents(query)

    async def count(self) -> int:
        return await self.collection.count_documents({"is_deleted": False})

    async def count_by_field(self, field: str, value: Any) -> int:
        return await self.collection.count_documents({field: value, "is_deleted": False})

   
    # Build filters
    def _build_search_query(self, search_param: Optional[str]) -> dict:
        """Define searchable fields. Always exclude deleted in caller."""
        return {}

    def _build_date_range_filter(self, date_filter: Optional[DateRangeFilter]) -> dict:
        query = {}
        if date_filter.start_date:
            query.setdefault("created_at", {})["$gte"] = datetime.fromisoformat(date_filter.start_date)
        if date_filter.end_date:
            end_dt = datetime.fromisoformat(date_filter.end_date) + timedelta(days=1)
            query.setdefault("created_at", {})["$lt"] = end_dt
        return query

    def _build_date_range_status_filter(self, status: Optional[str], date_filter: DateRangeFilter) -> dict:
        query = self._build_date_range_filter(date_filter.start_date, date_filter.end_date)
        if status:
            query['status'] = status
        return query
