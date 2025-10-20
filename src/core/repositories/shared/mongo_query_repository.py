from datetime import datetime
from typing import TypeVar, Generic, List, Optional, Type, Any
from bson import ObjectId
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection


T = TypeVar('T', bound=BaseModel)


class MongoQueryRepository(Generic[T]):

    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str, model_cls: Type[T]):
        self._collection: AsyncIOMotorCollection = db[collection_name]
        self._model_cls = model_cls
        self.db = db

    async def get_all(self, page_size: int, page_index: int) -> List[T]:
        if page_size <= 0 or page_index < 0:
            raise ValueError("Invalid pagination parameters.")
        cursor = self._collection.find({}).skip(page_index * page_size).limit(page_size)
        docs = await cursor.to_list(length=page_size)
        return [self._model_cls.model_validate(doc) for doc in docs]

    async def get_all_filtered(self, filters: Optional[dict] = None, projection: Optional[dict] = None) -> List[T]:
        filters = filters or {}
        cursor = self._collection.find(filters, projection)
        docs = await cursor.to_list(length=None)
        return [self._model_cls.model_validate(doc) for doc in docs]

    async def get_all_not_paginated(self) -> List[T]:
        cursor = self._collection.find({})
        docs = await cursor.to_list(length=None)
        return [self._model_cls.model_validate(doc) for doc in docs]
    
    async def get_by_field(self, field: str, value: Any) -> Optional[T]:
        doc = await self._collection.find_one({field: value})
        return self._model_cls.model_validate(doc) if doc else None

    async def get_by_id(self, id: str) -> Optional[T]:
        doc = await self._collection.find_one({'id': id})
        return self._model_cls.model_validate(doc) if doc else None
    
    async def get_by_unique_id(self, unique_id: str) -> Optional[T]:
        doc = await self._collection.find_one({'unique_id': unique_id})
        return self._model_cls.model_validate(doc) if doc else None

    async def get_all_in(self, field: str, values: List[Any]) -> List[T]:
        cursor = self._collection.find({field: {"$in": values}})
        docs = await cursor.to_list(length=None)
        return [self._model_cls.model_validate(doc) for doc in docs]

    async def get_last(self) -> Optional[T]:
        doc = await self._collection.find_one(sort=[("id", -1)])
        return self._model_cls.model_validate(doc) if doc else None

    async def get_first(self) -> Optional[T]:
        doc = await self._collection.find_one(sort=[("id", 1)])
        return self._model_cls.model_validate(doc) if doc else None

    def _build_search_query(self, search_param: Optional[str]) -> dict:
        """Define os campos a serem pesquisados com regex."""
        return {}
    
    def _build_search_query_by_organization(self, unique_id: str, search_param: Optional[str]) -> dict:
        """Define os campos a serem pesquisados com regex."""
        return {}

    async def search(self, search_param: Optional[str], page_size: int, page_index: int) -> List[T]:
        if page_size <= 0 or page_index < 0:
            raise ValueError("Invalid pagination parameters.")
        query = self._build_search_query(search_param)
        cursor = self._collection.find(query).skip(page_index * page_size).limit(page_size)
        docs = await cursor.to_list(length=page_size)
        return [self._model_cls.model_validate(doc) for doc in docs]
    
    async def filter_by_date(self, status_field: Optional[str], status_value: Optional[str], start_date: str, end_date: str, page_size: int, page_index: int) -> List[T]:
        if page_size <= 0 or page_index < 0:
            raise ValueError("Invalid pagination parameters.")
        query = self._build_date_range_status_query(status_field, status_value, start_date, end_date)
        cursor = self._collection.find(query).skip(page_index * page_size).limit(page_size)
        docs = await cursor.to_list(length=page_size)
        return [self._model_cls.model_validate(doc) for doc in docs]
    
    async def count_search(self, search_param: Optional[str]) -> int:
        query = self._build_search_query(search_param)
        return await self._collection.count_documents(query)
    
    async def count_search_by_organization(self, unique_id: str, search_param: Optional[str]) -> int:
        query = self._build_search_query_by_organization(unique_id, search_param)
        return await self._collection.count_documents(query)
    
    async def count(self) -> int:
        return await self._collection.count_documents({})

    async def count_by_field(self, field: str, value: Any) -> int:
        return await self._collection.count_documents({field: value})
    
    async def count_by_organization(self, unique_id: str) -> int:
        return await self._collection.count_documents({'organization_id': unique_id})

    def _build_date_range_query(self, start_date: str, end_date: str) -> dict:
        return {
            "created_at": {
                "$gte": datetime.fromisoformat(start_date),
                "$lte": datetime.fromisoformat(end_date)
            }
        }

    def _build_date_range_status_query(self, status_field: Optional[str], status_value: Optional[str], start_date: str, end_date: str) -> dict:
        query = self._build_date_range_query(start_date, end_date)
        if status_field and status_value:
            query[status_field] = status_value
        return query
    
    async def filter_by_date_range(self, start_date: str, end_date: str, page_size: int, page_index: int) -> List[T]:
        if page_size <= 0 or page_index < 0:
            raise ValueError("Invalid pagination parameters.")
        query = self._build_date_range_query(start_date, end_date)
        cursor = self._collection.find(query).skip(page_index * page_size).limit(page_size)
        docs = await cursor.to_list(length=page_size)
        return [self._model_cls.model_validate(doc) for doc in docs]
    
    async def filter_by_date_range_status(self, status_field: Optional[str], status_value: Optional[str], start_date: str, end_date: str, page_size: int, page_index: int) -> List[T]:
        if page_size <= 0 or page_index < 0:
            raise ValueError("Invalid pagination parameters.")
        query = self._build_date_range_status_query(status_field, status_value, start_date, end_date)
        cursor = self._collection.find(query).skip(page_index * page_size).limit(page_size)
        docs = await cursor.to_list(length=page_size)
        return [self._model_cls.model_validate(doc) for doc in docs]
    
    async def count_by_date_range_status_filter(self, status_field: Optional[str], status_value: Optional[str], start_date: str, end_date: str) -> int:
        query = self._build_date_range_status_query(status_field, status_value, start_date, end_date)
        return await self._collection.count_documents(query)
    
    async def count_by_date_filter(self, start_date: str, end_date: str) -> int:
        query = self._build_date_range_query(start_date, end_date)
        return await self._collection.count_documents(query)
