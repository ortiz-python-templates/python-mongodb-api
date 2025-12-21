from typing import Optional
from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.shared.filters.pagination_filter import PaginationFilter
from src.core.shared.filters.search_filter import SearchFilter
from src.core.schemas.files.file_responses import FileDetail
from src.core.shared.repositories.mongo_query_repository import MongoQueryRepository


class FileQueryRepository(MongoQueryRepository[FileDetail]):

    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "view_file_detail", FileDetail)

    async def get_all_by_category(self, category: str, search_filter: Optional[SearchFilter], pagination_filter: Optional[PaginationFilter]):
        return await self.get_all_by_field('category', category, search_filter, pagination_filter)
    
    async def get_all_by_user(self, user_id: str, search_filter: Optional[SearchFilter], pagination_filter: Optional[PaginationFilter]):
        return await self.get_all_by_field('created_by', user_id, search_filter, pagination_filter)
    
    async def get_all_by_owner_entity(self, owner_entity: str, search_filter: Optional[SearchFilter], pagination_filter: Optional[PaginationFilter]):
        return await self.get_all_by_field('owner_entity', owner_entity, search_filter, pagination_filter)
    
    async def get_all_by_owner_id(self, owner_id: str, search_filter: Optional[SearchFilter], pagination_filter: Optional[PaginationFilter]):
        return await self.get_all_by_field('owner_id', owner_id, search_filter, pagination_filter)

    async def count_search_by_category(self, category: str, search_param: Optional[str]) -> int:
        return await self.count_search_by_field('category', category, search_param)
    
    async def count_search_by_user(self, user_id: str, search_param: Optional[str]) -> int:
        return await self.count_search_by_field('created_by', user_id, search_param)
    
    async def count_search_by_owner_entity(self, owner_entity: str, search_param: Optional[str]) -> int:
        return await self.count_search_by_field('owner_entity', owner_entity, search_param)
    
    async def count_search_by_owner_id(self, owner_id: str, search_param: Optional[str]) -> int:
        return await self.count_search_by_field('owner_id', owner_id, search_param)

    async def get_by_name(self, name: str) -> Optional[FileDetail]:
        doc = await self.collection.find_one({'file_name': name, "is_deleted": False})
        return self.model_cls.model_validate(doc) if doc else None

