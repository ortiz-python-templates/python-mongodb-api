from datetime import datetime, timezone
from bson import ObjectId
from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.models.outbox.outbox_model import OutboxModel
from src.core.repositories.outbox.outbox_command_repository import OutboxCommandRepository
from src.core.shared.schemas.common_results import *
from src.common.utils.custom_exceptions import *


class OutboxCommandService:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.repository = OutboxCommandRepository(db)
      

    async def record_event(self, request: Request):
        pass


    async def mark_published(self, request: Request):
        pass


    async def mark_failed(self, request: Request):
        pass


    async def handle_rety(self, request: Request):
        pass