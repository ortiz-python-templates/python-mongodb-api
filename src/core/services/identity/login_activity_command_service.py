from datetime import datetime
from bson import ObjectId
from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.models.identity.user_model import UserModel
from src.core.repositories.identity.login_activity_command_repository import LoginActivityCommandRepository


class LoginActivityCommandService:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.command_repository = LoginActivityCommandRepository(db)


    async def update_login(self, request: Request, user: UserModel):
        now = datetime.now()
        ip = request.client.host
        host = request.headers.get("host", "unknown")
        browser = request.headers.get("user-agent", "unknown")
        location = None
        update = {
            "$set": {
                "last_login": now,
                "host": host,
                "browser": browser,
                "ip_address": ip,
                "location": location
            },
            "$inc": {
                "total_login": 1
            }
        }
        await self.command_repository.update_raw({"user_id": user.id}, update, upsert=True)


    async def update_logout(self, request: Request, user: UserModel):
        now = datetime.now()
        update = {
            "$set": {
                "last_logout": now
            },
            "$inc": {
                "total_logout": 1
            }
        }
        await self.command_repository.update_raw({"user_id": user.id}, update)
