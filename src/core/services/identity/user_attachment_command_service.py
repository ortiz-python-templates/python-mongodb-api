from datetime import datetime
from fastapi import Request, UploadFile
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.common.storage.storage_bucket import StorageBucket
from src.common.config.env_config import EnvConfig
from src.common.storage.minio_storage import MinioStorage
from src.core.services.identity.user_command_service import UserCommandService
from src.common.utils.messages.identity_messsages import UserAttachmentMsg
from src.core.schemas.common_results import *
from src.common.mail.email_service import EmailService
from src.core.models.identity.user_attachment_model import UserAttachmentModel
from src.common.utils.custom_exceptions import *
from src.core.schemas.identity.user_requests import *
from src.core.repositories.identity.user_attachment_command_repository import UserAttachmentCommandRepository


class UserAttachmentCommandService:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.command_repository = UserAttachmentCommandRepository(db)
        self.user_service = UserCommandService(db)
        self.email_service = EmailService()
        self.minio_storage = MinioStorage()


    async def create_user_attachment(self, request: Request, file: UploadFile, body: CreateUserAttachmentRequest):
        user = await self.user_service.get_user_by_unique_id_aux(body.user_id)
        now = datetime.now()

        upload_info = self.minio_storage.upload(file, StorageBucket.USER_ATTACHMENTS)
        current_user = request.state.user
        attachment = UserAttachmentModel(
            user_id=user.id,
            file_name=upload_info.file_name,
            size=upload_info.file_size,
            content_type=upload_info.content_type,
            object_key=upload_info.object_key,
            metadata=upload_info.metadata,
            description=body.description,
            uploaded_at=now,
            created_at=now,
            created_by=current_user.id
        )
        attachment_id = await self.command_repository.create(attachment)
        if attachment_id is None:
            raise InternalServerErrorException("Unable to create user attachment. Please check the data and try again.")
      
        return CreatedResult(
            id=attachment.unique_id,
            message=UserAttachmentMsg.Success.CREATED.format(body.user_id)
        )
    