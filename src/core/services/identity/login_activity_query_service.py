from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.common.utils.custom_exceptions import BadRequestException, NotFoundException
from src.core.filters.pagination_filter import PaginationFilter
from src.core.schemas.identity.login_activity_responses import LoginActivityDetail
from src.core.schemas.pagination_response import PaginationResponse
from src.core.repositories.identity.login_activity_query_repository import LoginActivityQueryRepository


class LoginActivityQueryService:
     
    def __init__(self, db: AsyncIOMotorDatabase):
        self.query_repository = LoginActivityQueryRepository(db)


    async def get_all_login_activities(self, request: Request, pagination_filter: PaginationFilter) -> PaginationResponse[LoginActivityDetail]:
        if pagination_filter.page_size <= 0 or pagination_filter.page_index < 0:
            raise BadRequestException("Invalid pagination parameters. Check page_size and page_index.")
        activities = await self.query_repository.get_all(pagination_filter.page_size, pagination_filter.page_index)
        return PaginationResponse.create(
            items=activities,
            total_items=await self.query_repository.count(),
            page_size=pagination_filter.page_size,
            page_index=pagination_filter.page_index,
            request=request
        )
    
    
    async def get_login_activity_by_id(self, id: str) -> LoginActivityDetail:
        activity = await self.query_repository.get_by_id(id)
        if activity is None:
            raise NotFoundException(f"LoginActivity with ID '{id}' was not found.")
        return activity
    

    async def get_login_activity_by_user_id(self, user_id: str) -> LoginActivityDetail:
        activity = await self.query_repository.get_by_user_id(user_id)
        if activity is None:
            raise NotFoundException(f"LoginActivity with User ID '{id}' was not found.")
        return activity