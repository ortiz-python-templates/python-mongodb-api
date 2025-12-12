from typing import List
from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.filters.pagination_filter import PaginationFilter
from src.core.filters.search_filter import SearchFilter
from src.core.schemas.pagination_response import PaginationResponse
from src.common.utils.custom_exceptions import *
from src.core.repositories.identity.user_query_repository import UserQueryRepository
from src.core.schemas.identity.user_requests import *
from src.core.schemas.identity.user_responses import *


class UserQueryService:
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.query_repository = UserQueryRepository(db)

   
    async def get_all_users(self, request: Request, pagination_filter: PaginationFilter) -> PaginationResponse[UserDetail]:
        if pagination_filter.page_size <= 0 or pagination_filter.page_index < 0:
            raise BadRequestException("Invalid pagination parameters. Check page_size and page_index.")
        users = await self.query_repository.get_all(pagination_filter.page_size, pagination_filter.page_index)
        return PaginationResponse.create(
            items=users,
            total_items=await self.query_repository.count(),
            page_size=pagination_filter.page_size,
            page_index=pagination_filter.page_index,
            request=request
        )


    async def get_all_users_not_paginated(self) -> List[UserDetail]:
        users = await self.query_repository.get_all_not_paginated()
        return users
    

    async def get_active_users(self, request: Request, pagination_filter: PaginationFilter) -> PaginationResponse[UserDetail]:
        users = await self.query_repository.get_all_by_status(True, pagination_filter.page_size, pagination_filter.page_index)
        return PaginationResponse.create(
            items=users,
            total_items=await self.query_repository.count_by_status(True),
            page_size=pagination_filter.page_size,
            page_index=pagination_filter.page_index,
            request=request
        )
    

    async def get_inactive_users(self, request: Request, pagination_filter: PaginationFilter) -> PaginationResponse[UserDetail]:
        users = await self.query_repository.get_all_by_status(False, pagination_filter.page_size, pagination_filter.page_index)
        return PaginationResponse.create(
            items=users,
            total_items=await self.query_repository.count_by_status(False),
            page_size=pagination_filter.page_size,
            page_index=pagination_filter.page_index,
            request=request
        )
    

    async def search_users(self, request: Request, search_filter: SearchFilter, pagination_filter: PaginationFilter) -> PaginationResponse[UserDetail]:
        users = await self.query_repository.search(search_filter.search_param, pagination_filter.page_size, pagination_filter.page_index)
        return PaginationResponse.create(
            items=users,
            total_items=await self.query_repository.count_search(search_filter.search_param),
            page_size=pagination_filter.page_size,
            page_index=pagination_filter.page_index,
            request=request
        )

    
    async def get_user_by_id(self, id: str) -> UserDetail:
        user = await self.query_repository.get_by_id(id)
        if user is None:
            raise NotFoundException(f"User with ID '{id}' was not found.")
        return user
    

    async def get_user_by_email(self, email: str) -> UserDetail:
        user = await self.query_repository.get_by_email(email)
        if user is None:
            raise NotFoundException(f"The email '{email}' is not associated with any user.")
        return user