from pymongo import ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.schemas.outbox.oubox_responses import OutboxDetail
from src.core.shared.repositories.mongo_query_repository import MongoQueryRepository


class OutboxQueryRepository(MongoQueryRepository[OutboxDetail]):

    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "view_outbox_detail", OutboxDetail)
