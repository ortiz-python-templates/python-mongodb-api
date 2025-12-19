from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.schemas.files.file_responses import FileDetail
from src.core.shared.repositories.mongo_query_repository import MongoQueryRepository


class FileQueryRepository(MongoQueryRepository[FileDetail]):

    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "view_file_detail", FileDetail)
