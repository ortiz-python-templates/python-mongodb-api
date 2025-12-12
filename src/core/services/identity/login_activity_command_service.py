from datetime import datetime
from fastapi import Request
from device_detector import DeviceDetector
from src.core.models.identity.enums import ActivityStatus
from src.core.models.identity.user_model import UserModel
from src.core.models.identity.login_activity_model import *
from src.core.repositories.identity.login_activity_command_repository import LoginActivityCommandRepository


class LoginActivityCommandService:

    def __init__(self, db):
        self.command_repository = LoginActivityCommandRepository(db)


    async def update_login(self, request: Request, user: UserModel):
        now = datetime.now()

        # Raw info
        ip = request.client.host
        host = request.headers.get("host", "unknown")
        user_agent_raw = request.headers.get("user-agent", "")

        # Parse user-agent
        detector = DeviceDetector(user_agent_raw).parse()
        device_type = detector.device_type()

        device_info = DeviceInfo(
            type=device_type,
            brand=detector.device_brand() or None,
            model=detector.device_model() or None,
            is_mobile=device_type == "smartphone",
            is_tablet=device_type == "tablet",
            is_pc=device_type == "desktop"
        )

        os_info = OSInfo(
            name=detector.os_name() or None,
            version=detector.os_version() or None
        )

        browser_info = BrowserInfo(
            name=detector.client_name() or None,
            version=detector.client_version() or None
        )

        # Retrieve existing login activity
        activity = await self.command_repository.get_by_id_aux(user.id)

        if activity:
            # Update existing object
            activity.last_login = now
            activity.status = ActivityStatus.ONLINE
            activity.host = host
            activity.client = browser_info
            activity.os = os_info
            activity.device = device_info
            activity.ip_address = ip
            activity.user_agent_raw = user_agent_raw
            activity.updated_at = now

            # Increment total_login
            await self.command_repository.increase_value(activity.id, "total_login", 1)
            await self.command_repository.update(activity.id, activity)
        else:
            # Create new login activity
            new_activity = LoginActivityModel(
                user_id=user.id,
                status=ActivityStatus.ONLINE,
                host=host,
                client=browser_info,
                os=os_info,
                device=device_info,
                ip_address=ip,
                location=None,
                user_agent_raw=user_agent_raw,
                last_login=now,
                last_logout=None,
                total_login=1,
                total_logout=0,
                created_at=now,
                updated_at=now,
                is_deleted=False
            )
            await self.command_repository.create(new_activity)


    async def update_logout(self, request: Request, user: UserModel):
        now = datetime.now()
        activity = await self.command_repository.get_by_id_aux(user.id)
        if activity:
            activity.last_logout = now
            activity.status = ActivityStatus.OFFLINE
            activity.updated_at = now

            # Increment total_logout
            await self.command_repository.increase_value(activity.id, "total_logout", 1)
            await self.command_repository.update(activity.id, activity)
