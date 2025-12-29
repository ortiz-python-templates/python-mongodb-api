from pymongo import ASCENDING, DESCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.models.outbox.outbox_model import OutboxModel
from src.core.shared.repositories.mongo_command_repository import MongoCommandRepository


class OutboxCommandRepository(MongoCommandRepository[OutboxModel]):

    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "outbox", OutboxModel)

    async def ensure_indexes(self):
        await self.collection.create_index([("status", ASCENDING), ("scheduled_for", ASCENDING)], name="idx_outbox_status_scheduled")
        await self.collection.create_index([("owner_id", ASCENDING), ("owner_entity", ASCENDING)], name="idx_outbox_owner_trace")
        await self.collection.create_index([("unique_id", ASCENDING)], unique=True, name="idx_outbox_unique_id")
        await self.collection.create_index([("event_type", ASCENDING)], name="idx_outbox_event_type")
        await self.collection.create_index([("created_at", DESCENDING)], name="idx_outbox_created_at")