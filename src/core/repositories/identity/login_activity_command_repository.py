
from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.models.identity.login_activity_model import LoginActivityModel
from src.core.repositories.shared.mongo_command_repository import MongoCommandRepository


class LoginActivityCommandRepository(MongoCommandRepository[LoginActivityModel]):

    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "login_activities", LoginActivityModel)

    async def ensure_indexes(self):
        await self._collection.create_index([("user_id", ASCENDING)], name="idx_activity_user")
        await self._collection.create_index([("status", ASCENDING)], name="idx_activity_status")
        await self._collection.create_index([("ip_address", ASCENDING)], name="idx_activity_ip_address")
        await self._collection.create_index([("last_login", ASCENDING)], name="idx_activity_last_login")
        await self._collection.create_index([("last_logout", ASCENDING)], name="idx_activity_last_logout")