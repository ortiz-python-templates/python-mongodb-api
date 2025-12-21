from typing import List
from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.common.storage.base_storage import BaseStorage
from src.common.storage.storage_provider_factory import StorageProviderFactory
from src.core.repositories.files.file_command_repository import FileCommandRepository
from src.core.shared.filters.pagination_filter import PaginationFilter
from src.core.shared.filters.search_filter import SearchFilter
from src.core.shared.schemas.pagination_response import PaginationResponse
from src.common.utils.custom_exceptions import *
from src.core.repositories.files.file_query_repository import FileQueryRepository
from src.core.schemas.files.file_requests import *
from src.core.schemas.files.file_responses import *


class FileQueryService:
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.query_repository = FileQueryRepository(db)
        self.command_repository = FileCommandRepository(db)
        self.storage_provider: BaseStorage = StorageProviderFactory.get_provider()


   
    async def get_all_files(self, request: Request, search_filter: SearchFilter, pagination_filter: PaginationFilter) -> PaginationResponse[FileDetail]:
        files = await self.query_repository.get_all(search_filter, pagination_filter)
        return PaginationResponse.create(
            items=files,
            total_items=await self.query_repository.count_search(search_filter.search_param),
            page_size=pagination_filter.page_size,
            page_index=pagination_filter.page_index,
            request=request
        )
    

    async def get_all_files_by_category(self, request: Request, category: str, search_filter: SearchFilter, pagination_filter: PaginationFilter) -> PaginationResponse[FileDetail]:
        files = await self.query_repository.get_all_by_category(category, search_filter, pagination_filter)
        return PaginationResponse.create(
            items=files,
            total_items=await self.query_repository.count_search_by_category(category, search_filter),
            page_size=pagination_filter.page_size,
            page_index=pagination_filter.page_index,
            request=request
        )
    

    async def get_all_files_by_user(self, request: Request, user_id: str, search_filter: SearchFilter, pagination_filter: PaginationFilter) -> PaginationResponse[FileDetail]:
        files = await self.query_repository.get_all_by_user(user_id, search_filter, pagination_filter)
        return PaginationResponse.create(
            items=files,
            total_items=await self.query_repository.count_search_by_user(user_id, search_filter),
            page_size=pagination_filter.page_size,
            page_index=pagination_filter.page_index,
            request=request
        )
    

    async def get_all_files_by_owner_entity(self, request: Request, owner_entity: str, search_filter: SearchFilter, pagination_filter: PaginationFilter) -> PaginationResponse[FileDetail]:
        files = await self.query_repository.get_all_by_owner_entity(owner_entity, search_filter, pagination_filter)
        return PaginationResponse.create(
            items=files,
            total_items=await self.query_repository.count_search_by_owner_entity(owner_entity, search_filter),
            page_size=pagination_filter.page_size,
            page_index=pagination_filter.page_index,
            request=request
        )
    

    async def get_all_files_by_owner_id(self, request: Request, owner_id: str, search_filter: SearchFilter, pagination_filter: PaginationFilter) -> PaginationResponse[FileDetail]:
        files = await self.query_repository.get_all_by_owner_id(owner_id, search_filter, pagination_filter)
        return PaginationResponse.create(
            items=files,
            total_items=await self.query_repository.count_search_by_owner_id(owner_id, search_filter),
            page_size=pagination_filter.page_size,
            page_index=pagination_filter.page_index,
            request=request
        )
    
    
    async def get_file_by_id(self, request: Request, file_id: str) -> FileDetail:
        file = await self.query_repository.get_by_id(file_id)
        if file is None:
            raise NotFoundException(f"Attachment with ID '{file_id}' was not found.")
        return file
    

    async def get_file_by_name(self, request: Request, name: str) -> FileDetail:
        file = await self.query_repository.get_by_name(name)
        if file is None:
            raise NotFoundException(f"Attachment with name '{name}' was not found.")
        return file

