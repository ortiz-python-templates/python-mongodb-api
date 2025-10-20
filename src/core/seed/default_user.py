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

        logger.info("Verificando existência do usuário admin...")

        if await repository.exists_record('email', email):
            logger.info("Usuário admin já existe. Ignorando...")
        else:
            logger.info("Usuário admin não encontrado. Criando novo usuário...")

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
                logger.error("Erro ao criar usuário admin. Verifique os campos.")
            else:
                logger.info(f"Usuário admin criado com sucesso. ID: {inserted_id}")
