from datetime import datetime, timezone
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.common.storage.base_storage import BaseStorage

from src.core.models.outbox.outbox_model import OutboxModel
from src.core.repositories.outbox.outbox_query_repository import OutboxQueryRepository
from src.core.shared.schemas.common_results import *
from src.common.utils.custom_exceptions import *


class OutboxQueryService:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.repository = OutboxQueryRepository(db)
      

    async def get_all_event(self):
        pass


    async def get_all_pending_events(self):
        pass


    async def get_all_failed_events(self):
        pass


    async def get_all_completed_events(self):
        pass


    async def get_all_events_by_owner_entity(self):
        pass


    async def get_event_by_id(self):
        pass


    async def get_status_report(self):
        pass