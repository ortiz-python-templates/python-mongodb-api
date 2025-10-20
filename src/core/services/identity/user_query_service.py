from typing import List
from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.filters.pagination_filter import PaginationFilter
from src.core.models.identity.user_model import UserModel
from src.core.repositories.identity.user_command_repository import UserCommandRepository
from src.core.filters.search_filter  import SearchFilter
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
            raise BadRequestException("Os parâmetros de paginação são inválidos. Verifique o tamanho da página e o índice.")
        users = await self.query_repository.get_all(pagination_filter.page_size, pagination_filter.page_index)
        return PaginationResponse.create(
            items=users,
            total_items=self.query_repository.count(),
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
            total_items=self.query_repository.count_by_status(status),
            page_size=pagination_filter.page_size,
            page_index=pagination_filter.page_index,
            request=request
        )
    

    async def search_users(self, request: Request, search_filter: SearchFilter, pagination_filter: PaginationFilter) -> PaginationResponse[UserDetail]:
        users = await self.query_repository.search(search_filter.search_param, pagination_filter.page_size, pagination_filter.page_index)
        return PaginationResponse.create(
            items=users,
            total_items=self.query_repository.count_search(search_filter.search_param),
            page_size=pagination_filter.page_size,
            page_index=pagination_filter.page_index,
            request=request
        )

    
    async def get_user_by_id(self, id: str) -> UserDetail:
        user = await self.query_repository.get_by_id(id)
        if user is None:
            raise NotFoundException(f"Não encontramos nenhum usuário com o ID '{id}'.")
        return user
    

    async def get_user_by_unique_id(self, unique_id: str) -> UserDetail:
        user = await self.query_repository.get_by_field("id", unique_id)
        if user is None:
            raise NotFoundException(f"O usuário com ID '{unique_id}' não foi encontrado.")
        return user
    
    
    async def get_user_by_email(self, email: str) -> UserDetail:
        user = await self.query_repository.get_by_email(email)
        if user is None:
            raise NotFoundException(f"O email '{email}' não está associado a nenhum usuário.")
        return user
    

    async def get_user_by_recovery_token(self, token: str) -> UserModel:
        user = await self.command_repository.get_by_recovery_token_aux(token)
        if user is None:
            raise NotFoundException("O token de recuperação informado é inválido ou já expirou.")
        return user
   

    async def authenticate_user(self, email: str, password: str) -> UserDetail:
        if not email or not password:
            raise BadRequestException("Por favor, informe o email e a senha para continuar.")
        user = await self.query_repository.get_by_email(email)
        user_aux = await self.command_repository.get_by_email_aux(email)
        if not user or not PasswordUtil.verify(password, user_aux.password):
            raise UnauthorizedException("Email ou senha incorretos. Tente novamente.")
        return user
    
