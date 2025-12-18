from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.models.identity.user_attachment_model import UserAttachmentModel
from src.core.shared.repositories.mongo_command_repository import MongoCommandRepository


class UserAttachmentCommandRepository(MongoCommandRepository[UserAttachmentModel]):
    
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "user_attachments", UserAttachmentModel)

    async def ensure_indexes(self):
        await self.collection.create_index([("user_id", ASCENDING)], name="idx_user_attachment_user_id")
        await self.collection.create_index([("file_name", ASCENDING)], name="idx_user_attachment_file_name")
        await self.collection.create_index([("object_key", ASCENDING)], name="idx_user_attachment_object_key")
        await self.collection.create_index([("content_type", ASCENDING)], name="idx_user_attachment_content_type")

