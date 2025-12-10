from typing import List
from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.filters.pagination_filter import PaginationFilter
from src.core.models.identity.user_model import UserModel
from src.core.repositories.identity.user_command_repository import UserCommandRepository
from src.core.filters.search_filter import SearchFilter
from src.core.schemas.pagination_response import PaginationResponse
from src.common.utils.password_util import PasswordUtil
from src.common.utils.custom_exceptions import *
from src.core.repositories.identity.user_query_repository import UserQueryRepository
from src.core.schemas.identity.user_requests import *
from src.core.schemas.identity.user_responses import *


class UserQueryService:
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.query_repository = UserQueryRepository(db)
        self.command_repository = UserCommandRepository(db)

   
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
    

    async def get_all_users_by_status(self, request: Request, status: bool, pagination_filter: PaginationFilter) -> PaginationResponse[UserDetail]:
        users = await self.query_repository.get_all_by_status(status, pagination_filter.page_size, pagination_filter.page_index)
        return PaginationResponse.create(
            items=users,
            total_items=await self.query_repository.count_by_status(status),
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
            raise NotFoundException(f"No user found with ID '{id}'.")
        return user
    

    async def get_user_by_unique_id(self, unique_id: str) -> UserDetail:
        user = await self.query_repository.get_by_field("id", unique_id)
        if user is None:
            raise NotFoundException(f"User with ID '{unique_id}' was not found.")
        return user
    
    
    async def get_user_by_email(self, email: str) -> UserDetail:
        user = await self.query_repository.get_by_email(email)
        if user is None:
            raise NotFoundException(f"The email '{email}' is not associated with any user.")
        return user
    

    async def get_user_by_recovery_token(self, token: str) -> UserModel:
        user = await self.command_repository.get_by_recovery_token_aux(token)
        if user is None:
            raise NotFoundException("The provided recovery token is invalid or has expired.")
        return user
   

    async def authenticate_user(self, email: str, password: str) -> UserDetail:
        if not email or not password:
            raise BadRequestException("Please provide email and password to continue.")
        user_aux = await self.command_repository.get_by_email_aux(email)
        if not user_aux or not PasswordUtil.verify(password, user_aux.password):
            raise UnauthorizedException("Incorrect email or password. Please try again.")
        user = await self.query_repository.get_by_email(user_aux.email)
        return user
