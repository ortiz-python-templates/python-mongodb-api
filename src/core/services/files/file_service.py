from datetime import datetime
from bson import ObjectId
from fastapi import Request, UploadFile
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.repositories.files.file_command_repository import FileCommandRepository
from src.core.schemas.files.file_requests import UploadFileRequest
from common.storage.storage_path import StorageBucket
from src.common.storage.minio_storage import MinioStorage
from src.common.utils.messages.file_messages import FileMsg
from src.core.shared.schemas.common_results import *
from src.common.utils.custom_exceptions import *



class FileCommandService:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.command_repository = FileCommandRepository(db)
        self.minio_storage = MinioStorage()

    
    async def upload_file(self, request: Request, file: UploadFile, body: UploadFileRequest):
        pass