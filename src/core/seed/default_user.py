from motor.motor_asyncio import AsyncIOMotorDatabase
from src.core.repositories.identity.user_command_repository import UserCommandRepository
from src.common.utils.encryption_util import EncryptionUtil
from src.common.utils.password_util import PasswordUtil
from src.core.models.identity.user_model import UserModel
from src.common.config.log_config import Logger  


class DefaultUser:

    @staticmethod
    async def seed_admin_users(db: AsyncIOMotorDatabase):
        logger = Logger.get_logger("seeder.default_user")
        repository = UserCommandRepository(db)
        email = "admin.template@gmail.com"

        logger.info("Checking if admin user exists...")

        if await repository.exists_record('email', email):
            logger.info("Admin user already exists. Skipping...")
        else:
            logger.info("Admin user not found. Creating new user...")

            user = UserModel(
                email=email,
                role="super-admin",
                first_name="Super Admin",
                last_name="Master",
                country="Angola",
                profile_completed=False,
                password=PasswordUtil.hash("Admin123$"),
                recovery_token=EncryptionUtil.generate_random_token(32),
                is_active=True
            )

            inserted_id = await repository.create(user)

            if inserted_id is None:
                logger.error("Error creating admin user. Please check the fields.")
            else:
                logger.info(f"Admin user created successfully. ID: {inserted_id}")
