from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.repositories.shared.mongo_command_repository import MongoCommandRepository
from src.core.models.identity.user_model import UserModel


class UserCommandRepository(MongoCommandRepository[UserModel]):
    
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "users", UserModel)
        self.ensure_indexes()

    def ensure_indexes(self):
        self._collection.create_index([("email", ASCENDING)], name="idx_user_email")
        self._collection.create_index([("first_name", ASCENDING)], name="idx_user_first_name")
        self._collection.create_index([("last_name", ASCENDING)], name="idx_user_last_name")
        self._collection.create_index([("recovery_token", ASCENDING)], name="idx_user_recovery_token", sparse=True)


    async def get_by_email_aux(self, email: str):
        doc = self._collection.find_one({'email': email})
        return self._model_cls.model_validate(doc) if doc else None
    
    async def get_by_recovery_token_aux(self, token: str):
        doc = self._collection.find_one({'recovery_token': token})
        return self._model_cls.model_validate(doc) if doc else None
    
    async def exists_excluding_id(self, unique_id: str, email: str):
        return super().exists_excluding_id(unique_id, {"email": email})
