from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.shared.repositories.mongo_command_repository import MongoCommandRepository
from src.core.models.identity.user_model import UserModel


class UserCommandRepository(MongoCommandRepository[UserModel]):
    
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "users", UserModel)

    async def ensure_indexes(self):
        await self.collection.create_index([("email", ASCENDING)], name="idx_user_email")
        await self.collection.create_index([("is_active", ASCENDING)], name="idx_user_is_active")
        await self.collection.create_index([("recovery_token", ASCENDING)], name="idx_user_recovery_token", sparse=True)

    async def get_by_email_aux(self, email: str):
        return await self.get_by_field_aux('email', email)
    
    async def get_by_recovery_token_aux(self, recovery_token: str):
        return await self.get_by_field_aux('recovery_token', recovery_token)
    
    async def exists_excluding_id(self, unique_id: str, email: str):
        return await super().exists_excluding_id(unique_id, {"email": email})
