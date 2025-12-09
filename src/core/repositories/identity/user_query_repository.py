import re
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.schemas.identity.user_responses import UserDetail
from src.core.repositories.shared.mongo_query_repository import MongoQueryRepository
from src.core.models.identity.user_model import UserModel


class UserQueryRepository(MongoQueryRepository[UserDetail]):
    
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "view_user_detail", UserDetail)


    async def get_all_by_status(self, status: bool, page_size: int, page_index: int) -> List[UserDetail]:
        if page_size <= 0 or page_index < 0:
            raise ValueError("Invalid pagination parameters.")
        cursor = await self._collection.find({'is_active': status}).skip(page_index * page_size).limit(page_size)
        docs = cursor.to_list(length=None)
        return [self._model_cls.model_validate(doc) for doc in docs]
    
    async def count_by_status(self, status: bool) -> int:
        return await self.count_by_field('status', status)

    async def get_by_email(self, email: str):
        return await self.get_by_field("email", email)
    
    def _build_search_query(self, search_param: Optional[str]) -> dict:
        if not search_param:
            return {}
        regex = {"$regex": re.escape(search_param), "$options": "i"}
        return {
            "$or": [
                {"first_name": regex},
                {"last_name": regex},
                {"email": regex}
            ]
        }