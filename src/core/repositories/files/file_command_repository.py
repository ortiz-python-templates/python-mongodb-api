from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.models.files.file_model import FileModel
from src.core.shared.repositories.mongo_command_repository import MongoCommandRepository


class FileCommandRepository(MongoCommandRepository[FileModel]):

    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "files", FileModel)

    async def ensure_indexes(self):
        await self.collection.create_index([("file_name", ASCENDING)], name="idx_file_file_name")
        await self.collection.create_index([("object_key", ASCENDING)], name="idx_file_object_key")
        await self.collection.create_index([("bucket_name", ASCENDING)], name="idx_file_bucket_name")
        await self.collection.create_index([("content_type", ASCENDING)], name="idx_file_content_type")
        await self.collection.create_index([("storage_provider", ASCENDING)], name="idx_file_storage_provider")
        await self.collection.create_index([("owner_entity", ASCENDING)], name="idx_file_owner_entity")
