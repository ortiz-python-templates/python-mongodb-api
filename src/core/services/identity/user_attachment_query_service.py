from typing import List
from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.common.storage.storage_bucket import StorageBucket
from src.common.storage.minio_storage import MinioStorage
from src.core.repositories.identity.user_attachment_command_repository import UserAttachmentCommandRepository
from src.core.services.identity.user_command_service import UserCommandService
from src.core.shared.filters.pagination_filter import PaginationFilter
from src.core.shared.filters.search_filter import SearchFilter
from src.core.shared.schemas.pagination_response import PaginationResponse
from src.common.utils.custom_exceptions import *
from src.core.repositories.identity.user_attachment_query_repository import UserAttachmentQueryRepository
from src.core.schemas.identity.user_requests import *
from src.core.schemas.identity.user_responses import *


class UserAttachmentQueryService:
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.query_repository = UserAttachmentQueryRepository(db)
        self.command_repository = UserAttachmentCommandRepository(db)
        self.user_service = UserCommandService(db)
        self.minio_storage = MinioStorage()

   
    async def get_all_user_attachments(self, request: Request, search_filter: SearchFilter, pagination_filter: PaginationFilter) -> PaginationResponse[UserAttachmentDetail]:
        attachments = await self.query_repository.get_all(search_filter, pagination_filter)
        return PaginationResponse.create(
            items=attachments,
            total_items=await self.query_repository.count_search(search_filter.search_param),
            page_size=pagination_filter.page_size,
            page_index=pagination_filter.page_index,
            request=request
        )
    

    async def get_all_attachments_by_user(self, request: Request, user_id: str, pagination_filter: PaginationFilter) -> PaginationResponse[UserAttachmentDetail]:
        attachments = await self.query_repository.get_all_by_user(user_id, pagination_filter)
        return PaginationResponse.create(
            items=attachments,
            total_items=await self.query_repository.count_by_user(user_id),
            page_size=pagination_filter.page_size,
            page_index=pagination_filter.page_index,
            request=request
        )
    
    
    async def get_user_attachment_by_id(self, attachment_id: str) -> UserAttachmentDetail:
        attachment = await self.query_repository.get_by_id(attachment_id)
        if attachment is None:
            raise NotFoundException(f"Attachment with ID '{attachment_id}' was not found.")
        return attachment


    async def display_user_attachment(self, request: Request, attachment_id: str):
        attachment = await self.command_repository.get_by_unique_id_aux(attachment_id)
        if attachment is None:
            raise NotFoundException(f"Attachment with ID '{attachment_id}' was not found.")
        file_url = ""
        if attachment.object_key:
            file_url = self.minio_storage.get_pressigned_url(attachment.object_key)
        return file_url