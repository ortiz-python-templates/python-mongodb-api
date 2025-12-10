from datetime import datetime, timedelta
from typing import TypeVar, Generic, List, Optional, Type, Any, Union
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection


T = TypeVar('T', bound=BaseModel)

class MongoQueryRepository(Generic[T]):

    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str, model_cls: Type[T]):
        self._collection: AsyncIOMotorCollection = db[collection_name]
        self._model_cls = model_cls
        self.db = db

   
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

   
    # Get all
    async def get_all(self, page_size: int, page_index: int) -> List[T]:
        page_size, page_index = self._normalize_pagination(page_size, page_index)
        cursor = self._collection.find({"is_deleted": False}).skip(page_index * page_size).limit(page_size)
        docs = await cursor.to_list(length=page_size)
        return [self._model_cls.model_validate(doc) for doc in docs]

    async def get_all_filtered(self, filters: Optional[dict] = None, projection: Optional[dict] = None) -> List[T]:
        filters = filters or {}
        filters["is_deleted"] = False
        cursor = self._collection.find(filters, projection)
        docs = await cursor.to_list(length=None)
        return [self._model_cls.model_validate(doc) for doc in docs]

    async def get_all_not_paginated(self) -> List[T]:
        cursor = self._collection.find({"is_deleted": False})
        docs = await cursor.to_list(length=None)
        return [self._model_cls.model_validate(doc) for doc in docs]

    async def get_all_in(self, field: str, values: List[Any]) -> List[T]:
        cursor = self._collection.find({field: {"$in": values}, "is_deleted": False})
        docs = await cursor.to_list(length=None)
        return [self._model_cls.model_validate(doc) for doc in docs]

    async def search(self, search_param: Optional[str], page_size: int, page_index: int) -> List[T]:
        page_size, page_index = self._normalize_pagination(page_size, page_index)
        query = self._build_search_query(search_param)
        query["is_deleted"] = False
        cursor = self._collection.find(query).skip(page_index * page_size).limit(page_size)
        docs = await cursor.to_list(length=page_size)
        return [self._model_cls.model_validate(doc) for doc in docs]

   
    # Get one
    '''#async def get_by_field(self, field: str, value: Any) -> Optional[T]:
        doc = await self._collection.find_one({field: value, "is_deleted": False})
        return self._model_cls.model_validate(doc) if doc else None'''
    
    async def get_by_field(self, field: str, value: Any) -> Optional[T]:
        filter = {
            field: value,
            "$or": [
                {"is_deleted": False},{"is_deleted": {"$exists": False}}
            ]
        }
        doc = await self._collection.find_one(filter)
        return self._model_cls.model_validate(doc) if doc else None


    async def get_by_id(self, id: str) -> Optional[T]:
        doc = await self._collection.find_one({'id': id, "is_deleted": False})
        return self._model_cls.model_validate(doc) if doc else None

    async def get_by_unique_id(self, unique_id: str) -> Optional[T]:
        doc = await self._collection.find_one({'unique_id': unique_id, "is_deleted": False})
        return self._model_cls.model_validate(doc) if doc else None

    async def get_last(self) -> Optional[T]:
        doc = await self._collection.find_one({"is_deleted": False}, sort=[("id", -1)])
        return self._model_cls.model_validate(doc) if doc else None

    async def get_first(self) -> Optional[T]:
        doc = await self._collection.find_one({"is_deleted": False}, sort=[("id", 1)])
        return self._model_cls.model_validate(doc) if doc else None

   
    # Filters
    async def filter_by_date(self, status_field: Optional[str], status_value: Optional[str], start_date: str, end_date: str, page_size: int, page_index: int) -> List[T]:
        page_size, page_index = self._normalize_pagination(page_size, page_index)
        query = self._build_date_range_status_filter(status_field, status_value, start_date, end_date)
        query["is_deleted"] = False
        cursor = self._collection.find(query).skip(page_index * page_size).limit(page_size)
        docs = await cursor.to_list(length=page_size)
        return [self._model_cls.model_validate(doc) for doc in docs]

    async def filter_by_date_range(self, start_date: str, end_date: str, page_size: int, page_index: int) -> List[T]:
        page_size, page_index = self._normalize_pagination(page_size, page_index)
        query = self._build_date_range_filter(start_date, end_date)
        query["is_deleted"] = False
        cursor = self._collection.find(query).skip(page_index * page_size).limit(page_size)
        docs = await cursor.to_list(length=page_size)
        return [self._model_cls.model_validate(doc) for doc in docs]

    async def filter_by_date_range_status(self, status_field: Optional[str], status_value: Optional[str], start_date: str, end_date: str, page_size: int, page_index: int) -> List[T]:
        page_size, page_index = self._normalize_pagination(page_size, page_index)
        query = self._build_date_range_status_filter(status_field, status_value, start_date, end_date)
        query["is_deleted"] = False
        cursor = self._collection.find(query).skip(page_index * page_size).limit(page_size)
        docs = await cursor.to_list(length=page_size)
        return [self._model_cls.model_validate(doc) for doc in docs]

   
    # Counts
    async def count_by_date_range_status_filter(self, status_field: Optional[str], status_value: Optional[str], start_date: str, end_date: str) -> int:
        query = self._build_date_range_status_filter(status_field, status_value, start_date, end_date)
        query["is_deleted"] = False
        return await self._collection.count_documents(query)

    async def count_by_date_filter(self, start_date: str, end_date: str) -> int:
        query = self._build_date_range_filter(start_date, end_date)
        query["is_deleted"] = False
        return await self._collection.count_documents(query)

    async def count_search(self, search_param: Optional[str]) -> int:
        query = self._build_search_query(search_param)
        query["is_deleted"] = False
        return await self._collection.count_documents(query)

    async def count(self) -> int:
        return await self._collection.count_documents({"is_deleted": False})

    async def count_by_field(self, field: str, value: Any) -> int:
        return await self._collection.count_documents({field: value, "is_deleted": False})

   
    # Build filters
    def _build_search_query(self, search_param: Optional[str]) -> dict:
        """Define searchable fields. Always exclude deleted in caller."""
        return {}

    def _build_date_range_filter(self, start_date: Optional[str], end_date: Optional[str]) -> dict:
        query = {}
        if start_date:
            query.setdefault("created_at", {})["$gte"] = datetime.fromisoformat(start_date)
        if end_date:
            end_dt = datetime.fromisoformat(end_date) + timedelta(days=1)
            query.setdefault("created_at", {})["$lt"] = end_dt
        return query

    def _build_date_range_status_filter(self, status: Optional[str], start_date: str, end_date: str) -> dict:
        query = self._build_date_range_filter(start_date, end_date)
        if status:
            query['status'] = status
        return query
