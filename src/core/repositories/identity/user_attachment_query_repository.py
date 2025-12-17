import re
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.filters.pagination_filter import PaginationFilter
from src.core.schemas.identity.user_responses import UserAttachmentDetail
from src.core.repositories.shared.mongo_query_repository import MongoQueryRepository


class UserAttachmentQueryRepository(MongoQueryRepository[UserAttachmentDetail]):
    
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "view_user_attachment_detail", UserAttachmentDetail)

    async def get_all_by_user(self, user_id: str, pagination_filter: PaginationFilter) -> List[UserAttachmentDetail]:
        page_size, page_index = self._normalize_pagination(pagination_filter.page_size, pagination_filter.page_index)
        cursor = self.collection.find({"is_deleted": False, 'user_id': user_id}).sort("created_at", -1).skip(page_index * page_size).limit(page_size)
        docs = await cursor.to_list(length=None)
        return [self.model_cls.model_validate(doc) for doc in docs]
    
    async def count_by_user(self, user_id: str):
        return await self.count_by_field('user_id', user_id)
    
    def _build_search_query(self, search_param: Optional[str]) -> dict:
        if not search_param:
            return {}
        regex = {"$regex": search_param, "$options": "i"} 
        query = {
            "$or": [
                {"file_name": regex},
                {"user_id": regex},
                {"content_type": regex},
            ]
        }
        return query
    
    