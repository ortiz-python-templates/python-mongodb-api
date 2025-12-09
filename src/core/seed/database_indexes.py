from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.repositories.configurations.feature_flag_command_repository import FeatureFlagCommandRepository
from src.core.repositories.identity.user_command_repository import UserCommandRepository


class DatabaseIndexes:

    @staticmethod
    async def setup_indexes(db: AsyncIOMotorDatabase):
        # configurations
        await FeatureFlagCommandRepository(db).ensure_indexes()

        # identity
        await UserCommandRepository(db).ensure_indexes()

        # products