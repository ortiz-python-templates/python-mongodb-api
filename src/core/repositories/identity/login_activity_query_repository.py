
from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.schemas.identity.login_activity_responses import LoginActivityDetail
from src.core.repositories.shared.mongo_query_repository import MongoQueryRepository


class LoginActivityQueryRepository(MongoQueryRepository[LoginActivityDetail]):

    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "view_login_activity_detail", LoginActivityDetail)