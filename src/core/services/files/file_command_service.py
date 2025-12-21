from datetime import datetime, timezone
from bson import ObjectId
from fastapi import Request, UploadFile
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.common.storage.base_storage import BaseStorage
from src.common.storage.file_checksum import FileChecksum
from src.common.storage.storage_provider_factory import StorageProviderFactory
from src.core.models.files.file_model import FileModel
from src.core.repositories.files.file_command_repository import FileCommandRepository
from src.core.schemas.files.file_requests import UploadFileRequest
from src.common.utils.messages.file_messages import FileMsg
from src.core.shared.schemas.common_results import *
from src.common.utils.custom_exceptions import *


class FileCommandService:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.command_repository = FileCommandRepository(db)
        self.storage_provider: BaseStorage = StorageProviderFactory.get_provider()

    
    async def upload_file(self, request: Request, file: UploadFile, body: UploadFileRequest):
        current_user = request.state.user
        storage_path = self._build_storage_path(body)

        # checksum
        file_bytes = await file.read()
        checksum = FileChecksum.calculate_checksum(file_bytes)
        file.file.seek(0)

        upload_info = await self.storage_provider.upload(
            file=file,
            storage_path=storage_path
        )

        new_file = FileModel(
            file_name=upload_info.file_name,
            size=upload_info.file_size,
            content_type=upload_info.content_type,
            category=body.category,
            storage_provider=self.storage_provider.get_provider_name(),
            object_key=upload_info.object_key,
            bucket_name=upload_info.bucket_name,
            visibility=body.visibility,
            checksum=checksum,
            owner_id=body.owner_id,
            owner_entity=body.owner_entity,
            display_name=body.display_name,
            description=body.description,
            metadata=upload_info.metadata,
            created_by=current_user.id
        )

        await self.command_repository.create(new_file)

        return CreatedResult(
            id=new_file.unique_id,
            message=FileMsg.Success.UPLOADED.format(new_file.unique_id)
        )



    async def download_file(self, request: Request, file_id: str):
        file = await self.command_repository.get_by_unique_id_aux(file_id)
        if file is None:
            raise NotFoundException(f"No file found with ID '{file_id}'.")
        if not self.storage_provider.is_available:
            raise RuntimeError("Storage provider is not available for download")
        current_user = request.state.user
        return await self.storage_provider.download(file.object_key)


    async def display_file(self, request: Request, file_id: str):
        file = await self.command_repository.get_by_unique_id_aux(file_id)
        if file is None:
            raise NotFoundException(f"No file found with ID '{file_id}'.")
        if not self.storage_provider.is_available:
            raise RuntimeError("Storage provider is not available for display")
        current_user = request.state.user
        return self.storage_provider.get_pressigned_url(file.object_key)


    async def delete_file(self, request: Request, file_id: str):
        file = await self.command_repository.get_by_unique_id_aux(file_id)
        if file is None:
            raise NotFoundException(f"No file found with ID '{file_id}'.")
        if not self.storage_provider.is_available:
            raise RuntimeError("Storage provider is not available for delete")
        current_user = request.state.user
        await self.command_repository.soft_delete(file_id, current_user.id)


    def _build_storage_path(self, body: UploadFileRequest) -> str:
        parts = [
            body.owner_entity.value if body.owner_entity else "common",
            body.category or "uncategorized",
            body.owner_id or "anonymous"
        ]
        return "/".join(parts)

