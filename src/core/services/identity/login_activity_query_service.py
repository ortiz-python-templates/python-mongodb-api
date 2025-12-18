from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.shared.filters.search_filter import SearchFilter
from src.common.utils.custom_exceptions import NotFoundException
from src.core.shared.filters.pagination_filter import PaginationFilter
from src.core.schemas.identity.login_activity_responses import LoginActivityDetail
from src.core.shared.schemas.pagination_response import PaginationResponse
from src.core.repositories.identity.login_activity_query_repository import LoginActivityQueryRepository


class LoginActivityQueryService:
     
    def __init__(self, db: AsyncIOMotorDatabase):
        self.query_repository = LoginActivityQueryRepository(db)


    async def get_all_login_activities(self, request: Request, search_filter: SearchFilter, pagination_filter: PaginationFilter) -> PaginationResponse[LoginActivityDetail]:
        activities = await self.query_repository.get_all(search_filter, pagination_filter)
        return PaginationResponse.create(
            items=activities,
            total_items=await self.query_repository.count(),
            page_size=pagination_filter.page_size,
            page_index=pagination_filter.page_index,
            request=request
        )
    
    
    async def get_login_activity_by_id(self, request: Request, id: str) -> LoginActivityDetail:
        activity = await self.query_repository.get_by_id(id)
        if activity is None:
            raise NotFoundException(f"LoginActivity with ID '{id}' was not found.")
        return activity
    

    async def get_login_activity_by_user_id(self, request: Request, user_id: str) -> LoginActivityDetail:
        activity = await self.query_repository.get_by_user_id(user_id)
        if activity is None:
            raise NotFoundException(f"LoginActivity with User ID '{user_id}' was not found.")
        return activity