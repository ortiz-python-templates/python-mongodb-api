from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.seed.default_configurations import DefaultConfigurations
from src.core.seed.default_user import DefaultUser


class SeedSetup:

    @staticmethod
    async def seed_initial_data(db: AsyncIOMotorDatabase):
        await DefaultUser.seed_admin_users(db)
        await DefaultConfigurations.seed_app_configurations(db)

